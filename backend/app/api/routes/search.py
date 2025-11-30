from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from ...db.database import get_db
from ...models.file import File as FileModel
from ...schemas.clustering import (
    SimilaritySearchRequest,
    SimilaritySearchResponse,
    SimilarityResult
)
from ...services.qdrant_service import qdrant_service
from ...services.embedding_service import embedding_service
from ...services.s3_service import s3_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["search"])

@router.post("/similar", response_model=SimilaritySearchResponse)
async def search_similar(
    request: SimilaritySearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search for similar items using file ID or text query
    """
    try:
        query_vector = None
        query_info = {}
        
        # Generate query vector based on input
        if request.file_id:
            # Use existing file's embedding
            embedding_data = await qdrant_service.get_embedding(request.file_id)
            
            if not embedding_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Embedding not found for file {request.file_id}"
                )
            
            query_vector = embedding_data['vector']
            query_info = {
                "type": "file",
                "file_id": request.file_id,
                "filename": embedding_data['payload'].get('filename', 'unknown')
            }
            
        elif request.query_text:
            # Generate embedding from text query
            query_vector = await embedding_service.embed_text(request.query_text)
            query_info = {
                "type": "text",
                "query": request.query_text[:100]  # Truncate for display
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Either file_id or query_text must be provided"
            )
        
        # Search for similar vectors
        results = await qdrant_service.search_similar(
            query_vector=query_vector,
            session_id=request.session_id,
            top_k=request.top_k,
            score_threshold=None
        )
        
        # Format results
        similarity_results = []
        for result in results:
            # Skip the query file itself if searching by file_id
            if request.file_id and result['id'] == request.file_id:
                continue
            
            similarity_results.append(SimilarityResult(
                file_id=result['id'],
                filename=result['payload'].get('filename', 'unknown'),
                file_type=result['payload'].get('file_type', 'unknown'),
                similarity_score=float(result['score']),
                distance=float(1.0 - result['score'])  # Convert cosine similarity to distance
            ))
        
        logger.info(f"Found {len(similarity_results)} similar items for session {request.session_id}")
        
        return SimilaritySearchResponse(
            query_info=query_info,
            results=similarity_results,
            total_results=len(similarity_results)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to search similar items: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search similar items: {str(e)}")


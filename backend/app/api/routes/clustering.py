from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from ...db.database import get_db
from ...schemas.clustering import (
    ClusterRequest,
    DendrogramResponse,
    DendrogramNode,
    ClusterSummary
)
from ...services.qdrant_service import qdrant_service
from ...services.clustering_service import clustering_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/clustering", tags=["clustering"])

@router.post("/dendrogram", response_model=DendrogramResponse)
async def generate_dendrogram(
    request: ClusterRequest,
    db: Session = Depends(get_db)
):
    """
    Generate hierarchical clustering dendrogram for a session
    """
    try:
        # Fetch all embeddings for the session
        embeddings = await qdrant_service.get_all_embeddings_for_session(
            session_id=request.session_id
        )
        
        if len(embeddings) < 2:
            raise HTTPException(
                status_code=400,
                detail="Need at least 2 files with embeddings to perform clustering"
            )
        
        # Perform agglomerative clustering
        linkage_matrix, embeddings_list = await clustering_service.perform_agglomerative_clustering(
            embeddings=embeddings,
            method='ward',
            metric='euclidean'
        )
        
        # Generate dendrogram structure
        nodes = await clustering_service.generate_dendrogram_structure(
            linkage_matrix=linkage_matrix,
            embeddings=embeddings_list
        )
        
        # Compute cluster summaries
        cluster_summaries = await clustering_service.compute_cluster_summaries(
            embeddings=embeddings_list,
            linkage_matrix=linkage_matrix,
            num_clusters=request.num_clusters,
            distance_threshold=request.distance_threshold
        )
        
        # Convert linkage matrix to list format
        linkage_list = linkage_matrix.tolist()
        
        logger.info(f"Generated dendrogram for session {request.session_id} with {len(embeddings)} items")
        
        return DendrogramResponse(
            session_id=request.session_id,
            linkage_matrix=linkage_list,
            nodes=nodes,
            cluster_summaries=cluster_summaries,
            total_items=len(embeddings)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate dendrogram: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate dendrogram: {str(e)}")

@router.get("/clusters/{session_id}", response_model=list[ClusterSummary])
async def get_clusters(
    session_id: str,
    num_clusters: int = None,
    distance_threshold: float = None,
    db: Session = Depends(get_db)
):
    """
    Get cluster assignments and summaries for a session
    """
    try:
        # Fetch all embeddings for the session
        embeddings = await qdrant_service.get_all_embeddings_for_session(
            session_id=session_id
        )
        
        if len(embeddings) < 2:
            raise HTTPException(
                status_code=400,
                detail="Need at least 2 files with embeddings to perform clustering"
            )
        
        # Perform agglomerative clustering
        linkage_matrix, embeddings_list = await clustering_service.perform_agglomerative_clustering(
            embeddings=embeddings,
            method='ward',
            metric='euclidean'
        )
        
        # Compute cluster summaries
        cluster_summaries = await clustering_service.compute_cluster_summaries(
            embeddings=embeddings_list,
            linkage_matrix=linkage_matrix,
            num_clusters=num_clusters,
            distance_threshold=distance_threshold
        )
        
        logger.info(f"Generated {len(cluster_summaries)} clusters for session {session_id}")
        
        return cluster_summaries
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get clusters: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get clusters: {str(e)}")


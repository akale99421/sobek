from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client.http import models
import logging
from typing import List, Dict, Any, Optional
import uuid
from ..core.config import settings

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.EMBEDDING_DIMENSION,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    async def store_embedding(
        self,
        file_id: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Store an embedding vector in Qdrant
        
        Args:
            file_id: Unique file identifier
            embedding: Vector embedding
            metadata: Additional metadata (session_id, filename, file_type, etc.)
            
        Returns:
            True if successful
        """
        try:
            point = PointStruct(
                id=file_id,
                vector=embedding,
                payload=metadata
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            logger.info(f"Stored embedding for file {file_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to store embedding: {e}")
            raise
    
    async def get_embedding(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an embedding by file ID
        
        Args:
            file_id: Unique file identifier
            
        Returns:
            Dictionary with vector and payload, or None if not found
        """
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[file_id]
            )
            
            if result:
                point = result[0]
                return {
                    "id": point.id,
                    "vector": point.vector,
                    "payload": point.payload
                }
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve embedding: {e}")
            return None
    
    async def search_similar(
        self,
        query_vector: List[float],
        session_id: Optional[str] = None,
        top_k: int = 10,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_vector: Query embedding vector
            session_id: Optional session filter
            top_k: Number of results to return
            score_threshold: Minimum similarity score
            
        Returns:
            List of similar items with scores
        """
        try:
            query_filter = None
            if session_id:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="session_id",
                            match=MatchValue(value=session_id)
                        )
                    ]
                )
            
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=query_filter,
                limit=top_k,
                score_threshold=score_threshold
            )
            
            return [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in results
            ]
        except Exception as e:
            logger.error(f"Failed to search similar vectors: {e}")
            raise
    
    async def get_all_embeddings_for_session(
        self,
        session_id: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all embeddings for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of all embeddings with metadata
        """
        try:
            # Scroll through all points with the session_id filter
            scroll_filter = Filter(
                must=[
                    FieldCondition(
                        key="session_id",
                        match=MatchValue(value=session_id)
                    )
                ]
            )
            
            results = []
            offset = None
            
            while True:
                response = self.client.scroll(
                    collection_name=self.collection_name,
                    scroll_filter=scroll_filter,
                    limit=100,
                    offset=offset,
                    with_vectors=True
                )
                
                points, next_offset = response
                
                for point in points:
                    results.append({
                        "id": point.id,
                        "vector": point.vector,
                        "payload": point.payload
                    })
                
                if next_offset is None:
                    break
                offset = next_offset
            
            logger.info(f"Retrieved {len(results)} embeddings for session {session_id}")
            return results
        except Exception as e:
            logger.error(f"Failed to retrieve embeddings for session: {e}")
            raise
    
    async def delete_embedding(self, file_id: str) -> bool:
        """
        Delete an embedding from Qdrant
        
        Args:
            file_id: Unique file identifier
            
        Returns:
            True if successful
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[file_id]
                )
            )
            logger.info(f"Deleted embedding for file {file_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete embedding: {e}")
            return False
    
    async def delete_session_embeddings(self, session_id: str) -> bool:
        """
        Delete all embeddings for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=Filter(
                        must=[
                            FieldCondition(
                                key="session_id",
                                match=MatchValue(value=session_id)
                            )
                        ]
                    )
                )
            )
            logger.info(f"Deleted all embeddings for session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete session embeddings: {e}")
            return False

# Singleton instance
qdrant_service = QdrantService()


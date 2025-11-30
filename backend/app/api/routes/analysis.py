from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from ...db.database import get_db
from ...schemas.clustering import (
    AnomalyDetectionResponse,
    AnomalyItem
)
from ...services.qdrant_service import qdrant_service
from ...services.clustering_service import clustering_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.get("/anomalies/{session_id}", response_model=AnomalyDetectionResponse)
async def detect_anomalies(
    session_id: str,
    threshold_percentile: float = 95.0,
    db: Session = Depends(get_db)
):
    """
    Detect anomalies in the session's files based on distance to cluster centroids
    """
    try:
        # Validate threshold percentile
        if threshold_percentile < 0 or threshold_percentile > 100:
            raise HTTPException(
                status_code=400,
                detail="threshold_percentile must be between 0 and 100"
            )
        
        # Fetch all embeddings for the session
        embeddings = await qdrant_service.get_all_embeddings_for_session(
            session_id=session_id
        )
        
        if len(embeddings) < 2:
            raise HTTPException(
                status_code=400,
                detail="Need at least 2 files with embeddings to detect anomalies"
            )
        
        # Perform clustering to get cluster summaries
        linkage_matrix, embeddings_list = await clustering_service.perform_agglomerative_clustering(
            embeddings=embeddings,
            method='ward',
            metric='euclidean'
        )
        
        cluster_summaries = await clustering_service.compute_cluster_summaries(
            embeddings=embeddings_list,
            linkage_matrix=linkage_matrix,
            num_clusters=None,
            distance_threshold=None
        )
        
        # Detect anomalies
        anomalies_data, threshold = await clustering_service.detect_anomalies(
            embeddings=embeddings_list,
            cluster_summaries=cluster_summaries,
            threshold_percentile=threshold_percentile
        )
        
        # Format anomaly results
        anomaly_items = []
        for anomaly in anomalies_data:
            anomaly_items.append(AnomalyItem(
                file_id=anomaly['file_id'],
                filename=anomaly['filename'],
                file_type=anomaly['file_type'],
                anomaly_score=float(anomaly['distance']),
                distance_to_nearest_cluster=float(anomaly['distance']),
                cluster_id=anomaly.get('cluster_id')
            ))
        
        # Sort by anomaly score (descending)
        anomaly_items.sort(key=lambda x: x.anomaly_score, reverse=True)
        
        logger.info(f"Detected {len(anomaly_items)} anomalies for session {session_id}")
        
        return AnomalyDetectionResponse(
            session_id=session_id,
            anomalies=anomaly_items,
            threshold=float(threshold),
            total_files=len(embeddings),
            anomaly_count=len(anomaly_items)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to detect anomalies: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to detect anomalies: {str(e)}")


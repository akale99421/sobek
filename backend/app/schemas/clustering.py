from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ClusterItem(BaseModel):
    file_id: str
    filename: str
    file_type: str
    distance_to_centroid: float

class ClusterSummary(BaseModel):
    cluster_id: int
    item_count: int
    average_distance: float
    representative_items: List[ClusterItem]
    centroid: Optional[List[float]] = None

class DendrogramNode(BaseModel):
    node_id: int
    left_child: Optional[int] = None
    right_child: Optional[int] = None
    distance: float
    item_count: int
    items: List[str]  # file_ids

class DendrogramResponse(BaseModel):
    session_id: str
    linkage_matrix: List[List[float]]
    nodes: List[DendrogramNode]
    cluster_summaries: List[ClusterSummary]
    total_items: int

class ClusterRequest(BaseModel):
    session_id: str
    num_clusters: Optional[int] = None
    distance_threshold: Optional[float] = None

class SimilaritySearchRequest(BaseModel):
    session_id: str
    file_id: Optional[str] = None
    query_text: Optional[str] = None
    top_k: int = 10

class SimilarityResult(BaseModel):
    file_id: str
    filename: str
    file_type: str
    similarity_score: float
    distance: float

class SimilaritySearchResponse(BaseModel):
    query_info: Dict[str, Any]
    results: List[SimilarityResult]
    total_results: int

class AnomalyItem(BaseModel):
    file_id: str
    filename: str
    file_type: str
    anomaly_score: float
    distance_to_nearest_cluster: float
    cluster_id: Optional[int] = None

class AnomalyDetectionResponse(BaseModel):
    session_id: str
    anomalies: List[AnomalyItem]
    threshold: float
    total_files: int
    anomaly_count: int


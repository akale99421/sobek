from scipy.cluster.hierarchy import linkage, fcluster, dendrogram as scipy_dendrogram
from scipy.spatial.distance import pdist, cdist
import numpy as np
import logging
from typing import List, Dict, Any, Optional, Tuple
from ..schemas.clustering import ClusterSummary, ClusterItem, DendrogramNode

logger = logging.getLogger(__name__)

class ClusteringService:
    
    async def perform_agglomerative_clustering(
        self,
        embeddings: List[Dict[str, Any]],
        method: str = 'ward',
        metric: str = 'euclidean'
    ) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Perform hierarchical agglomerative clustering
        
        Args:
            embeddings: List of embedding dictionaries with 'id', 'vector', 'payload'
            method: Linkage method ('ward', 'complete', 'average', 'single')
            metric: Distance metric
            
        Returns:
            Tuple of (linkage_matrix, embeddings_list)
        """
        if len(embeddings) < 2:
            raise ValueError("Need at least 2 items for clustering")
        
        try:
            # Extract vectors
            vectors = np.array([emb['vector'] for emb in embeddings])
            
            # Perform hierarchical clustering
            linkage_matrix = linkage(vectors, method=method, metric=metric)
            
            logger.info(f"Performed clustering on {len(embeddings)} items")
            return linkage_matrix, embeddings
        except Exception as e:
            logger.error(f"Failed to perform clustering: {e}")
            raise
    
    async def generate_dendrogram_structure(
        self,
        linkage_matrix: np.ndarray,
        embeddings: List[Dict[str, Any]]
    ) -> List[DendrogramNode]:
        """
        Generate dendrogram node structure from linkage matrix
        
        Args:
            linkage_matrix: Scipy linkage matrix
            embeddings: List of embedding dictionaries
            
        Returns:
            List of dendrogram nodes
        """
        n = len(embeddings)
        nodes = []
        
        # Create leaf nodes (original items)
        for i, emb in enumerate(embeddings):
            node = DendrogramNode(
                node_id=i,
                left_child=None,
                right_child=None,
                distance=0.0,
                item_count=1,
                items=[emb['id']]
            )
            nodes.append(node)
        
        # Create internal nodes from linkage matrix
        for i, row in enumerate(linkage_matrix):
            left_idx = int(row[0])
            right_idx = int(row[1])
            distance = float(row[2])
            count = int(row[3])
            
            # Collect items from children
            left_items = nodes[left_idx].items if left_idx < len(nodes) else []
            right_items = nodes[right_idx].items if right_idx < len(nodes) else []
            
            node = DendrogramNode(
                node_id=n + i,
                left_child=left_idx,
                right_child=right_idx,
                distance=distance,
                item_count=count,
                items=left_items + right_items
            )
            nodes.append(node)
        
        return nodes
    
    async def compute_cluster_summaries(
        self,
        embeddings: List[Dict[str, Any]],
        linkage_matrix: np.ndarray,
        num_clusters: Optional[int] = None,
        distance_threshold: Optional[float] = None
    ) -> List[ClusterSummary]:
        """
        Compute cluster summaries with centroids and representative items
        
        Args:
            embeddings: List of embedding dictionaries
            linkage_matrix: Scipy linkage matrix
            num_clusters: Number of clusters to form (if specified)
            distance_threshold: Distance threshold for clustering (if specified)
            
        Returns:
            List of cluster summaries
        """
        if len(embeddings) < 2:
            # Single item - create single cluster
            return [ClusterSummary(
                cluster_id=0,
                item_count=1,
                average_distance=0.0,
                representative_items=[ClusterItem(
                    file_id=embeddings[0]['id'],
                    filename=embeddings[0]['payload'].get('filename', 'unknown'),
                    file_type=embeddings[0]['payload'].get('file_type', 'unknown'),
                    distance_to_centroid=0.0
                )],
                centroid=embeddings[0]['vector']
            )]
        
        try:
            # Determine cluster assignments
            if num_clusters:
                cluster_labels = fcluster(linkage_matrix, num_clusters, criterion='maxclust')
            elif distance_threshold:
                cluster_labels = fcluster(linkage_matrix, distance_threshold, criterion='distance')
            else:
                # Default: create sqrt(n) clusters
                num_clusters = max(2, int(np.sqrt(len(embeddings))))
                cluster_labels = fcluster(linkage_matrix, num_clusters, criterion='maxclust')
            
            # Group embeddings by cluster
            clusters = {}
            for i, label in enumerate(cluster_labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(embeddings[i])
            
            # Compute summaries for each cluster
            summaries = []
            for cluster_id, cluster_items in clusters.items():
                # Compute centroid
                vectors = np.array([item['vector'] for item in cluster_items])
                centroid = np.mean(vectors, axis=0)
                
                # Normalize centroid
                centroid = centroid / np.linalg.norm(centroid)
                
                # Compute distances to centroid
                distances = cdist([centroid], vectors, metric='euclidean')[0]
                avg_distance = float(np.mean(distances))
                
                # Find representative items (closest to centroid)
                sorted_indices = np.argsort(distances)
                representative_items = []
                for idx in sorted_indices[:min(5, len(cluster_items))]:
                    item = cluster_items[idx]
                    representative_items.append(ClusterItem(
                        file_id=item['id'],
                        filename=item['payload'].get('filename', 'unknown'),
                        file_type=item['payload'].get('file_type', 'unknown'),
                        distance_to_centroid=float(distances[idx])
                    ))
                
                summary = ClusterSummary(
                    cluster_id=int(cluster_id),
                    item_count=len(cluster_items),
                    average_distance=avg_distance,
                    representative_items=representative_items,
                    centroid=centroid.tolist()
                )
                summaries.append(summary)
            
            # Sort by cluster_id
            summaries.sort(key=lambda x: x.cluster_id)
            
            logger.info(f"Generated {len(summaries)} cluster summaries")
            return summaries
        except Exception as e:
            logger.error(f"Failed to compute cluster summaries: {e}")
            raise
    
    async def detect_anomalies(
        self,
        embeddings: List[Dict[str, Any]],
        cluster_summaries: List[ClusterSummary],
        threshold_percentile: float = 95.0
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Detect anomalies based on distance to cluster centroids
        
        Args:
            embeddings: List of embedding dictionaries
            cluster_summaries: List of cluster summaries with centroids
            threshold_percentile: Percentile for anomaly threshold
            
        Returns:
            Tuple of (anomaly_list, threshold_value)
        """
        if len(embeddings) < 2:
            return [], 0.0
        
        try:
            # Build mapping of file_id to cluster centroid
            file_to_cluster = {}
            for summary in cluster_summaries:
                for item in summary.representative_items:
                    file_to_cluster[item.file_id] = summary.centroid
            
            # Compute distances for all items
            distances = []
            for emb in embeddings:
                file_id = emb['id']
                vector = np.array(emb['vector'])
                
                # Find nearest cluster centroid
                min_distance = float('inf')
                nearest_cluster_id = None
                
                for summary in cluster_summaries:
                    centroid = np.array(summary.centroid)
                    dist = np.linalg.norm(vector - centroid)
                    if dist < min_distance:
                        min_distance = dist
                        nearest_cluster_id = summary.cluster_id
                
                distances.append({
                    'file_id': file_id,
                    'filename': emb['payload'].get('filename', 'unknown'),
                    'file_type': emb['payload'].get('file_type', 'unknown'),
                    'distance': min_distance,
                    'cluster_id': nearest_cluster_id
                })
            
            # Compute threshold
            distance_values = [d['distance'] for d in distances]
            threshold = float(np.percentile(distance_values, threshold_percentile))
            
            # Identify anomalies
            anomalies = [d for d in distances if d['distance'] > threshold]
            
            logger.info(f"Detected {len(anomalies)} anomalies with threshold {threshold}")
            return anomalies, threshold
        except Exception as e:
            logger.error(f"Failed to detect anomalies: {e}")
            raise

# Singleton instance
clustering_service = ClusteringService()


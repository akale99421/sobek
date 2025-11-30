// API Types for Inventory Analysis Backend
// Auto-generated from backend schemas

export type FileType = 'image' | 'text';
export type EmbeddingStatus = 'pending' | 'processing' | 'completed' | 'failed';

// File Upload Types
export interface FileUploadResponse {
  file_id: string;
  filename: string;
  file_type: FileType;
  file_size: number;
  s3_path: string;
  embedding_status: EmbeddingStatus;
  message: string;
}

export interface FileResponse {
  id: string;
  session_id: string;
  filename: string;
  file_type: FileType;
  mime_type: string;
  file_size: number;
  s3_bucket: string;
  s3_key: string;
  embedding_status: EmbeddingStatus;
  created_at: string;
  updated_at: string;
}

export interface FileListResponse {
  files: FileResponse[];
  total: number;
}

// Embedding Types
export interface EmbeddingGenerateRequest {
  file_ids: string[];
}

export interface EmbeddingStatusResponse {
  file_id: string;
  filename: string;
  status: EmbeddingStatus;
  message: string;
}

export interface ModelInfoResponse {
  text_model: string;
  image_model: string;
  embedding_dimension: number;
  device: string;
  text_model_loaded: boolean;
  image_model_loaded: boolean;
}

// Clustering Types
export interface ClusterItem {
  file_id: string;
  filename: string;
  file_type: string;
  distance_to_centroid: number;
}

export interface ClusterSummary {
  cluster_id: number;
  item_count: number;
  average_distance: number;
  representative_items: ClusterItem[];
  centroid?: number[];
}

export interface DendrogramNode {
  node_id: number;
  left_child?: number;
  right_child?: number;
  distance: number;
  item_count: number;
  items: string[];
}

export interface DendrogramResponse {
  session_id: string;
  linkage_matrix: number[][];
  nodes: DendrogramNode[];
  cluster_summaries: ClusterSummary[];
  total_items: number;
}

export interface ClusterRequest {
  session_id: string;
  num_clusters?: number;
  distance_threshold?: number;
}

// Search Types
export interface SimilaritySearchRequest {
  session_id: string;
  file_id?: string;
  query_text?: string;
  top_k?: number;
}

export interface SimilarityResult {
  file_id: string;
  filename: string;
  file_type: string;
  similarity_score: number;
  distance: number;
}

export interface SimilaritySearchResponse {
  query_info: Record<string, any>;
  results: SimilarityResult[];
  total_results: number;
}

// Analysis Types
export interface AnomalyItem {
  file_id: string;
  filename: string;
  file_type: string;
  anomaly_score: number;
  distance_to_nearest_cluster: number;
  cluster_id?: number;
}

export interface AnomalyDetectionResponse {
  session_id: string;
  anomalies: AnomalyItem[];
  threshold: number;
  total_files: number;
  anomaly_count: number;
}

// API Client Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// API Helper Functions
export class InventoryAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  // File Upload
  async uploadFiles(sessionId: string, files: File[]): Promise<FileUploadResponse[]> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    const response = await fetch(`${this.baseUrl}/api/files/upload?session_id=${sessionId}`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  // Get Files for Session
  async getSessionFiles(sessionId: string): Promise<FileListResponse> {
    const response = await fetch(`${this.baseUrl}/api/files/session/${sessionId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to get files: ${response.statusText}`);
    }

    return response.json();
  }

  // Get File Details
  async getFile(fileId: string): Promise<FileResponse> {
    const response = await fetch(`${this.baseUrl}/api/files/${fileId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to get file: ${response.statusText}`);
    }

    return response.json();
  }

  // Delete File
  async deleteFile(fileId: string): Promise<{ message: string; file_id: string }> {
    const response = await fetch(`${this.baseUrl}/api/files/${fileId}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete file: ${response.statusText}`);
    }

    return response.json();
  }

  // Generate Embeddings
  async generateEmbeddings(fileIds: string[]): Promise<EmbeddingStatusResponse[]> {
    const response = await fetch(`${this.baseUrl}/api/embeddings/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_ids: fileIds }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate embeddings: ${response.statusText}`);
    }

    return response.json();
  }

  // Get Embedding Status
  async getEmbeddingStatus(fileId: string): Promise<EmbeddingStatusResponse> {
    const response = await fetch(`${this.baseUrl}/api/embeddings/status/${fileId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to get embedding status: ${response.statusText}`);
    }

    return response.json();
  }

  // Get Session Embedding Status
  async getSessionEmbeddingStatus(sessionId: string): Promise<EmbeddingStatusResponse[]> {
    const response = await fetch(`${this.baseUrl}/api/embeddings/session/${sessionId}/status`);
    
    if (!response.ok) {
      throw new Error(`Failed to get session embedding status: ${response.statusText}`);
    }

    return response.json();
  }

  // Get Model Info
  async getModelInfo(): Promise<ModelInfoResponse> {
    const response = await fetch(`${this.baseUrl}/api/embeddings/models/info`);
    
    if (!response.ok) {
      throw new Error(`Failed to get model info: ${response.statusText}`);
    }

    return response.json();
  }

  // Generate Dendrogram
  async generateDendrogram(request: ClusterRequest): Promise<DendrogramResponse> {
    const response = await fetch(`${this.baseUrl}/api/clustering/dendrogram`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate dendrogram: ${response.statusText}`);
    }

    return response.json();
  }

  // Get Clusters
  async getClusters(
    sessionId: string,
    numClusters?: number,
    distanceThreshold?: number
  ): Promise<ClusterSummary[]> {
    const params = new URLSearchParams();
    if (numClusters) params.append('num_clusters', numClusters.toString());
    if (distanceThreshold) params.append('distance_threshold', distanceThreshold.toString());

    const response = await fetch(
      `${this.baseUrl}/api/clustering/clusters/${sessionId}?${params.toString()}`
    );

    if (!response.ok) {
      throw new Error(`Failed to get clusters: ${response.statusText}`);
    }

    return response.json();
  }

  // Search Similar
  async searchSimilar(request: SimilaritySearchRequest): Promise<SimilaritySearchResponse> {
    const response = await fetch(`${this.baseUrl}/api/search/similar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Failed to search similar: ${response.statusText}`);
    }

    return response.json();
  }

  // Detect Anomalies
  async detectAnomalies(
    sessionId: string,
    thresholdPercentile: number = 95.0
  ): Promise<AnomalyDetectionResponse> {
    const response = await fetch(
      `${this.baseUrl}/api/analysis/anomalies/${sessionId}?threshold_percentile=${thresholdPercentile}`
    );

    if (!response.ok) {
      throw new Error(`Failed to detect anomalies: ${response.statusText}`);
    }

    return response.json();
  }
}

// Export singleton instance
export const inventoryAPI = new InventoryAPI();


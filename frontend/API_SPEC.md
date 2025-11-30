# Inventory Analysis API Specification

## Base URL
```
http://localhost:8000
```

## Overview
This API provides endpoints for uploading files, generating embeddings, performing hierarchical clustering, similarity search, and anomaly detection for inventory analysis.

---

## Authentication
Currently, no authentication is required. Sessions are identified by `session_id`.

---

## Endpoints

### 1. File Upload

#### `POST /api/files/upload`
Upload multiple files and automatically trigger embedding generation.

**Query Parameters:**
- `session_id` (string, required): Session identifier

**Request Body:**
- `files` (multipart/form-data): Array of files to upload

**Supported File Types:**
- Images: JPEG, PNG, GIF, WebP
- Text: TXT, CSV, JSON, MD, PDF

**Response:** `200 OK`
```json
[
  {
    "file_id": "uuid",
    "filename": "example.jpg",
    "file_type": "image",
    "file_size": 1024000,
    "s3_path": "bucket/session_id/file_id/filename",
    "embedding_status": "pending",
    "message": "File uploaded successfully, embedding generation in progress"
  }
]
```

**Example:**
```typescript
const formData = new FormData();
formData.append('files', file1);
formData.append('files', file2);

const response = await fetch(
  'http://localhost:8000/api/files/upload?session_id=session_123',
  {
    method: 'POST',
    body: formData
  }
);
```

---

#### `GET /api/files/session/{session_id}`
Get all files for a session.

**Response:** `200 OK`
```json
{
  "files": [
    {
      "id": "uuid",
      "session_id": "session_123",
      "filename": "example.jpg",
      "file_type": "image",
      "mime_type": "image/jpeg",
      "file_size": 1024000,
      "s3_bucket": "inventory-files",
      "s3_key": "session_123/uuid/example.jpg",
      "embedding_status": "completed",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1
}
```

---

#### `GET /api/files/{file_id}`
Get details for a specific file.

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "session_id": "session_123",
  "filename": "example.jpg",
  "file_type": "image",
  "mime_type": "image/jpeg",
  "file_size": 1024000,
  "s3_bucket": "inventory-files",
  "s3_key": "session_123/uuid/example.jpg",
  "embedding_status": "completed",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

#### `DELETE /api/files/{file_id}`
Delete a file and its embedding.

**Response:** `200 OK`
```json
{
  "message": "File deleted successfully",
  "file_id": "uuid"
}
```

---

### 2. Embeddings

#### `POST /api/embeddings/generate`
Generate embeddings for specific files (on-demand).

**Request Body:**
```json
{
  "file_ids": ["uuid1", "uuid2"]
}
```

**Response:** `200 OK`
```json
[
  {
    "file_id": "uuid1",
    "filename": "example.jpg",
    "status": "completed",
    "message": "Embedding generated successfully"
  }
]
```

---

#### `GET /api/embeddings/status/{file_id}`
Get embedding status for a specific file.

**Response:** `200 OK`
```json
{
  "file_id": "uuid",
  "filename": "example.jpg",
  "status": "completed",
  "message": "Embedding status: completed"
}
```

---

#### `GET /api/embeddings/session/{session_id}/status`
Get embedding status for all files in a session.

**Response:** `200 OK`
```json
[
  {
    "file_id": "uuid1",
    "filename": "example1.jpg",
    "status": "completed",
    "message": "Embedding status: completed"
  },
  {
    "file_id": "uuid2",
    "filename": "example2.txt",
    "status": "processing",
    "message": "Embedding status: processing"
  }
]
```

---

#### `GET /api/embeddings/models/info`
Get information about loaded embedding models.

**Response:** `200 OK`
```json
{
  "text_model": "BAAI/bge-base-en-v1.5",
  "image_model": "facebook/dinov2-base",
  "embedding_dimension": 768,
  "device": "cpu",
  "text_model_loaded": true,
  "image_model_loaded": true
}
```

---

### 3. Clustering

#### `POST /api/clustering/dendrogram`
Generate hierarchical clustering dendrogram.

**Request Body:**
```json
{
  "session_id": "session_123",
  "num_clusters": 5,
  "distance_threshold": null
}
```

**Note:** Specify either `num_clusters` OR `distance_threshold`, not both. If neither is specified, the system will automatically determine an optimal number of clusters.

**Response:** `200 OK`
```json
{
  "session_id": "session_123",
  "linkage_matrix": [[0, 1, 0.5, 2], [2, 3, 0.8, 3]],
  "nodes": [
    {
      "node_id": 0,
      "left_child": null,
      "right_child": null,
      "distance": 0.0,
      "item_count": 1,
      "items": ["file_id_1"]
    }
  ],
  "cluster_summaries": [
    {
      "cluster_id": 1,
      "item_count": 5,
      "average_distance": 0.45,
      "representative_items": [
        {
          "file_id": "uuid",
          "filename": "example.jpg",
          "file_type": "image",
          "distance_to_centroid": 0.12
        }
      ],
      "centroid": [0.1, 0.2, 0.3, ...]
    }
  ],
  "total_items": 10
}
```

---

#### `GET /api/clustering/clusters/{session_id}`
Get cluster assignments and summaries.

**Query Parameters:**
- `num_clusters` (integer, optional): Number of clusters
- `distance_threshold` (float, optional): Distance threshold

**Response:** `200 OK`
```json
[
  {
    "cluster_id": 1,
    "item_count": 5,
    "average_distance": 0.45,
    "representative_items": [
      {
        "file_id": "uuid",
        "filename": "example.jpg",
        "file_type": "image",
        "distance_to_centroid": 0.12
      }
    ],
    "centroid": [0.1, 0.2, 0.3, ...]
  }
]
```

---

### 4. Search

#### `POST /api/search/similar`
Search for similar items using file ID or text query.

**Request Body (by file):**
```json
{
  "session_id": "session_123",
  "file_id": "uuid",
  "top_k": 10
}
```

**Request Body (by text):**
```json
{
  "session_id": "session_123",
  "query_text": "search query",
  "top_k": 10
}
```

**Response:** `200 OK`
```json
{
  "query_info": {
    "type": "file",
    "file_id": "uuid",
    "filename": "example.jpg"
  },
  "results": [
    {
      "file_id": "uuid2",
      "filename": "similar.jpg",
      "file_type": "image",
      "similarity_score": 0.95,
      "distance": 0.05
    }
  ],
  "total_results": 10
}
```

---

### 5. Analysis

#### `GET /api/analysis/anomalies/{session_id}`
Detect anomalies based on distance to cluster centroids.

**Query Parameters:**
- `threshold_percentile` (float, optional, default: 95.0): Percentile threshold (0-100)

**Response:** `200 OK`
```json
{
  "session_id": "session_123",
  "anomalies": [
    {
      "file_id": "uuid",
      "filename": "outlier.jpg",
      "file_type": "image",
      "anomaly_score": 2.5,
      "distance_to_nearest_cluster": 2.5,
      "cluster_id": 3
    }
  ],
  "threshold": 2.0,
  "total_files": 100,
  "anomaly_count": 5
}
```

---

## Error Responses

All endpoints may return the following error responses:

### `400 Bad Request`
```json
{
  "detail": "Error message describing the problem"
}
```

### `404 Not Found`
```json
{
  "detail": "Resource not found"
}
```

### `500 Internal Server Error`
```json
{
  "detail": "Internal server error message"
}
```

---

## Workflow Example

### Complete Analysis Workflow

1. **Upload Files**
```typescript
const files = [file1, file2, file3];
const uploadResponse = await inventoryAPI.uploadFiles(sessionId, files);
```

2. **Wait for Embeddings** (automatic, but can check status)
```typescript
const statuses = await inventoryAPI.getSessionEmbeddingStatus(sessionId);
// Poll until all are 'completed'
```

3. **Generate Dendrogram**
```typescript
const dendrogram = await inventoryAPI.generateDendrogram({
  session_id: sessionId,
  num_clusters: 5
});
```

4. **Search for Similar Items**
```typescript
const similar = await inventoryAPI.searchSimilar({
  session_id: sessionId,
  file_id: uploadResponse[0].file_id,
  top_k: 10
});
```

5. **Detect Anomalies**
```typescript
const anomalies = await inventoryAPI.detectAnomalies(sessionId, 95.0);
```

---

## Notes

- **Embedding Generation**: Automatically triggered on file upload as a background task
- **Supported Models**: 
  - Text: BAAI/bge-base-en-v1.5 (768 dimensions)
  - Image: facebook/dinov2-base (768 dimensions)
- **Vector Storage**: Qdrant with cosine similarity
- **Clustering**: Agglomerative hierarchical clustering with Ward linkage
- **File Storage**: MinIO S3-compatible storage

---

## Rate Limits
Currently no rate limits are enforced.

---

## WebSocket Support
Not currently available. Use polling for status updates.


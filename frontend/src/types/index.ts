// Type definitions for the application

export interface FileWithPreview extends File {
  preview?: string;
}

export interface UploadedFile {
  file: File;
  id: string;
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error';
  progress: number;
  error?: string;
  result?: AnalysisResult;
}

export interface AnalysisResult {
  file_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  status: 'processing' | 'completed' | 'failed';
  extracted_text?: string;
  embeddings?: number[];
  metadata?: {
    dimensions?: { width: number; height: number };
    format?: string;
    pages?: number;
    [key: string]: any;
  };
  thumbnail_url?: string;
  s3_url?: string;
  created_at?: string;
  error?: string;
}

export interface SessionInfo {
  session_id: string;
  created_at: string;
  last_active: string;
  file_count?: number;
}

export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

export interface ApiError {
  message: string;
  status: number;
  detail?: string;
}

export interface SearchResult extends AnalysisResult {
  similarity_score: number;
}

export type TabType = 'inventory' | 'extraction';

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}


// API Service Layer for Backend Communication

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ApiError {
  message: string;
  status: number;
  detail?: string;
}

export interface SessionData {
  session_id: string;
  created_at: string;
  last_active: string;
}

export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

export interface AnalysisResult {
  file_id: string;
  filename: string;
  file_type: string;
  status: 'processing' | 'completed' | 'failed';
  extracted_text?: string;
  embeddings?: number[];
  metadata?: Record<string, any>;
  error?: string;
}

export interface UploadResponse {
  session_id: string;
  files: AnalysisResult[];
  message: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  // Generic fetch wrapper with error handling
  private async fetchWithError<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw {
          message: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
          detail: errorData.detail,
        } as ApiError;
      }

      return await response.json();
    } catch (error) {
      if ((error as ApiError).status) {
        throw error;
      }
      throw {
        message: 'Network error. Please check your connection.',
        status: 0,
        detail: (error as Error).message,
      } as ApiError;
    }
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string; service: string }> {
    return this.fetchWithError('/health');
  }

  // Session management
  async createSession(sessionId: string): Promise<SessionData> {
    return this.fetchWithError('/api/session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ session_id: sessionId }),
    });
  }

  async getSession(sessionId: string): Promise<SessionData> {
    return this.fetchWithError(`/api/session/${sessionId}`);
  }

  // File upload with progress tracking
  async uploadFiles(
    sessionId: string,
    files: File[],
    onProgress?: (progress: UploadProgress) => void
  ): Promise<UploadResponse> {
    return new Promise((resolve, reject) => {
      const formData = new FormData();
      formData.append('session_id', sessionId);
      
      files.forEach((file) => {
        formData.append('files', file);
      });

      const xhr = new XMLHttpRequest();

      // Track upload progress
      if (onProgress) {
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            onProgress({
              loaded: event.loaded,
              total: event.total,
              percentage: Math.round((event.loaded / event.total) * 100),
            });
          }
        });
      }

      // Handle completion
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText);
            resolve(response);
          } catch (error) {
            reject({
              message: 'Failed to parse response',
              status: xhr.status,
              detail: (error as Error).message,
            } as ApiError);
          }
        } else {
          try {
            const errorData = JSON.parse(xhr.responseText);
            reject({
              message: errorData.detail || `Upload failed with status ${xhr.status}`,
              status: xhr.status,
              detail: errorData.detail,
            } as ApiError);
          } catch {
            reject({
              message: `Upload failed with status ${xhr.status}`,
              status: xhr.status,
            } as ApiError);
          }
        }
      });

      // Handle errors
      xhr.addEventListener('error', () => {
        reject({
          message: 'Network error during upload',
          status: 0,
        } as ApiError);
      });

      xhr.addEventListener('abort', () => {
        reject({
          message: 'Upload cancelled',
          status: 0,
        } as ApiError);
      });

      // Send request
      xhr.open('POST', `${this.baseUrl}/api/upload`);
      xhr.send(formData);
    });
  }

  // Get analysis results
  async getAnalysisResults(sessionId: string): Promise<AnalysisResult[]> {
    return this.fetchWithError(`/api/analysis/${sessionId}`);
  }

  // Get specific file analysis
  async getFileAnalysis(fileId: string): Promise<AnalysisResult> {
    return this.fetchWithError(`/api/analysis/file/${fileId}`);
  }

  // Search similar items (when vector search is ready)
  async searchSimilar(
    query: string,
    limit: number = 10
  ): Promise<AnalysisResult[]> {
    return this.fetchWithError('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, limit }),
    });
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export class for testing
export default ApiService;


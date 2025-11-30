import { useState, useCallback } from 'react';
import { apiService, UploadProgress, ApiError } from '../services/api';
import { UploadedFile } from '../types';

interface UseFileUploadReturn {
  uploadedFiles: UploadedFile[];
  isUploading: boolean;
  uploadProgress: number;
  error: string | null;
  addFiles: (files: File[]) => void;
  removeFile: (id: string) => void;
  clearFiles: () => void;
  uploadFiles: (sessionId: string) => Promise<void>;
}

export function useFileUpload(): UseFileUploadReturn {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const addFiles = useCallback((files: File[]) => {
    const newFiles: UploadedFile[] = files.map((file) => ({
      file,
      id: `${Date.now()}-${Math.random().toString(36).substring(2, 15)}`,
      status: 'pending',
      progress: 0,
    }));
    setUploadedFiles((prev) => [...prev, ...newFiles]);
    setError(null);
  }, []);

  const removeFile = useCallback((id: string) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== id));
  }, []);

  const clearFiles = useCallback(() => {
    setUploadedFiles([]);
    setError(null);
    setUploadProgress(0);
  }, []);

  const uploadFiles = useCallback(
    async (sessionId: string) => {
      if (uploadedFiles.length === 0) {
        setError('No files to upload');
        return;
      }

      setIsUploading(true);
      setError(null);
      setUploadProgress(0);

      // Mark all files as uploading
      setUploadedFiles((prev) =>
        prev.map((f) => ({ ...f, status: 'uploading' as const }))
      );

      try {
        const files = uploadedFiles.map((f) => f.file);

        const response = await apiService.uploadFiles(
          sessionId,
          files,
          (progress: UploadProgress) => {
            setUploadProgress(progress.percentage);
          }
        );

        // Update files with results
        setUploadedFiles((prev) =>
          prev.map((uploadedFile) => {
            const result = response.files.find(
              (r) => r.filename === uploadedFile.file.name
            );
            if (result) {
              return {
                ...uploadedFile,
                status: result.status === 'completed' ? 'completed' : 'processing',
                progress: 100,
                result,
              };
            }
            return uploadedFile;
          })
        );

        setIsUploading(false);
      } catch (err) {
        const apiError = err as ApiError;
        setError(apiError.message || 'Upload failed');
        setIsUploading(false);

        // Mark all files as error
        setUploadedFiles((prev) =>
          prev.map((f) => ({
            ...f,
            status: 'error' as const,
            error: apiError.message,
          }))
        );
      }
    },
    [uploadedFiles]
  );

  return {
    uploadedFiles,
    isUploading,
    uploadProgress,
    error,
    addFiles,
    removeFile,
    clearFiles,
    uploadFiles,
  };
}


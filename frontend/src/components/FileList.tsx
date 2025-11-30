import { UploadedFile } from '../types';
import ProgressBar from './ProgressBar';

interface FileListProps {
  files: UploadedFile[];
  onRemove: (id: string) => void;
  onClearAll: () => void;
}

export default function FileList({ files, onRemove, onClearAll }: FileListProps) {
  if (files.length === 0) return null;

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'completed':
        return (
          <svg className="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'uploading':
      case 'processing':
        return (
          <svg className="h-5 w-5 text-blue-400 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        );
      case 'error':
        return (
          <svg className="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      default:
        return (
          <svg className="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
    }
  };

  const getStatusText = (status: UploadedFile['status']) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'uploading':
        return 'Uploading...';
      case 'processing':
        return 'Processing...';
      case 'error':
        return 'Error';
      default:
        return 'Pending';
    }
  };

  return (
    <div className="mt-6 bg-white/5 rounded-xl p-6 border border-emerald-400/20">
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-lg font-semibold text-emerald-50">
          Files ({files.length})
        </h4>
        <button
          onClick={onClearAll}
          className="text-sm text-emerald-300 hover:text-emerald-200 underline"
        >
          Clear All
        </button>
      </div>
      <div className="space-y-3">
        {files.map((file) => (
          <div
            key={file.id}
            className="bg-white/5 rounded-lg p-4 border border-emerald-400/10"
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-start space-x-3 flex-1 min-w-0">
                {getStatusIcon(file.status)}
                <div className="flex-1 min-w-0">
                  <p className="text-emerald-50 font-medium truncate">
                    {file.file.name}
                  </p>
                  <div className="flex items-center space-x-3 mt-1">
                    <p className="text-xs text-emerald-200/60">
                      {(file.file.size / 1024).toFixed(2)} KB
                    </p>
                    <span className="text-xs text-emerald-300">
                      {getStatusText(file.status)}
                    </span>
                  </div>
                  {file.error && (
                    <p className="text-xs text-red-400 mt-1">{file.error}</p>
                  )}
                </div>
              </div>
              <button
                onClick={() => onRemove(file.id)}
                className="text-red-400 hover:text-red-300 transition-colors ml-2 flex-shrink-0"
                disabled={file.status === 'uploading'}
              >
                <svg
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            {(file.status === 'uploading' || file.status === 'processing') && (
              <ProgressBar progress={file.progress} showPercentage={false} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}


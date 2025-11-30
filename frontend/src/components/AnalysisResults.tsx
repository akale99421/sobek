import { AnalysisResult } from '../types';
import LoadingSpinner from './LoadingSpinner';

interface AnalysisResultsProps {
  results: AnalysisResult[];
  isLoading?: boolean;
}

export default function AnalysisResults({ results, isLoading }: AnalysisResultsProps) {
  if (isLoading) {
    return (
      <div className="bg-white/5 rounded-xl p-12 border border-emerald-400/20">
        <LoadingSpinner size="lg" text="Analyzing files..." />
      </div>
    );
  }

  if (results.length === 0) {
    return null;
  }

  const getFileIcon = (fileType: string) => {
    if (fileType.startsWith('image/')) {
      return (
        <svg className="h-6 w-6 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      );
    }
    if (fileType.includes('pdf')) {
      return (
        <svg className="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      );
    }
    if (fileType.includes('text') || fileType.includes('csv') || fileType.includes('json')) {
      return (
        <svg className="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      );
    }
    return (
      <svg className="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    );
  };

  return (
    <div className="mt-6 bg-white/5 rounded-xl p-6 border border-emerald-400/20">
      <h4 className="text-lg font-semibold text-emerald-50 mb-4">
        Analysis Results ({results.length})
      </h4>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {results.map((result) => (
          <div
            key={result.file_id}
            className="bg-white/5 rounded-lg p-4 border border-emerald-400/10 hover:border-emerald-400/30 transition-all"
          >
            <div className="flex items-start space-x-3 mb-3">
              {getFileIcon(result.file_type)}
              <div className="flex-1 min-w-0">
                <h5 className="text-emerald-50 font-medium truncate">
                  {result.filename}
                </h5>
                <p className="text-xs text-emerald-200/60 mt-1">
                  {result.file_type} • {(result.file_size / 1024).toFixed(2)} KB
                </p>
              </div>
              <div className={`px-2 py-1 rounded text-xs font-medium ${
                result.status === 'completed' 
                  ? 'bg-emerald-500/20 text-emerald-300'
                  : result.status === 'failed'
                  ? 'bg-red-500/20 text-red-300'
                  : 'bg-blue-500/20 text-blue-300'
              }`}>
                {result.status}
              </div>
            </div>

            {result.thumbnail_url && (
              <div className="mb-3 rounded overflow-hidden">
                <img
                  src={result.thumbnail_url}
                  alt={result.filename}
                  className="w-full h-32 object-cover"
                />
              </div>
            )}

            {result.extracted_text && (
              <div className="mb-3">
                <p className="text-xs text-emerald-200/70 font-medium mb-1">
                  Extracted Text:
                </p>
                <p className="text-sm text-emerald-100/80 line-clamp-3">
                  {result.extracted_text}
                </p>
              </div>
            )}

            {result.metadata && Object.keys(result.metadata).length > 0 && (
              <div className="mb-3">
                <p className="text-xs text-emerald-200/70 font-medium mb-1">
                  Metadata:
                </p>
                <div className="text-xs text-emerald-100/70 space-y-1">
                  {Object.entries(result.metadata).slice(0, 3).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="text-emerald-200/60">{key}:</span>
                      <span className="text-emerald-100/80 truncate ml-2">
                        {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.error && (
              <div className="text-xs text-red-400 mt-2">
                Error: {result.error}
              </div>
            )}

            {result.embeddings && (
              <div className="text-xs text-emerald-200/60 mt-2">
                ✓ Embeddings generated ({result.embeddings.length} dimensions)
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}


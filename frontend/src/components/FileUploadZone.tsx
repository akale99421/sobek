import { useCallback } from 'react';
import LoadingSpinner from './LoadingSpinner';

interface FileUploadZoneProps {
  onFilesSelected: (files: File[]) => void;
  isExtracting?: boolean;
  accept?: string;
  multiple?: boolean;
}

export default function FileUploadZone({
  onFilesSelected,
  isExtracting = false,
  accept = 'image/*,text/*,.pdf,.doc,.docx,.csv,.xlsx,.xls,.json,.txt,.md,.zip',
  multiple = true,
}: FileUploadZoneProps) {
  const handleFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = Array.from(e.target.files || []);
      if (files.length > 0) {
        onFilesSelected(files);
      }
      // Reset input so same file can be selected again
      e.target.value = '';
    },
    [onFilesSelected]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      
      const files = Array.from(e.dataTransfer.files);
      if (files.length > 0) {
        onFilesSelected(files);
      }
    },
    [onFilesSelected]
  );

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  return (
    <div
      className="bg-white/5 rounded-xl p-6 border-2 border-dashed border-emerald-400/30 hover:border-emerald-400/50 transition-all"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <div className="text-center">
        <div className="mb-4">
          <svg
            className="mx-auto h-16 w-16 text-emerald-300"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-emerald-50 mb-2">
          Upload Inventory Files
        </h3>
        <p className="text-emerald-100/80 mb-4">
          Drop multiple files here, or click to browse
        </p>
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept={accept}
          multiple={multiple}
          onChange={handleFileChange}
          disabled={isExtracting}
        />
        <label
          htmlFor="file-upload"
          className={`inline-block px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg cursor-pointer transition-all shadow-lg hover:shadow-xl ${
            isExtracting ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          Choose Files
        </label>
        <p className="text-sm text-emerald-200/60 mt-4">
          Supported formats: Images (PNG, JPG, etc.) • Text files (TXT, CSV,
          JSON, etc.) • Documents (PDF, Word) • ZIP archives (auto-extracted) •
          Multiple files allowed
        </p>
        {isExtracting && (
          <div className="mt-4">
            <LoadingSpinner text="Extracting ZIP files..." />
          </div>
        )}
      </div>
    </div>
  );
}


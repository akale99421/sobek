# Frontend Component Reference

Quick reference guide for all available components and their usage.

## 🎨 UI Components

### LoadingSpinner
Animated loading indicator with customizable size and text.

```typescript
import LoadingSpinner from './components/LoadingSpinner';

<LoadingSpinner 
  size="sm" | "md" | "lg"
  color="text-emerald-300"
  text="Loading..."
/>
```

**Props:**
- `size?: 'sm' | 'md' | 'lg'` - Spinner size (default: 'md')
- `color?: string` - Tailwind color class (default: 'text-emerald-300')
- `text?: string` - Optional loading text

---

### ErrorAlert
Display error messages with dismiss option.

```typescript
import ErrorAlert from './components/ErrorAlert';

<ErrorAlert 
  message="Something went wrong"
  title="Error"
  onDismiss={() => setError(null)}
/>
```

**Props:**
- `message: string` - Error message (required)
- `title?: string` - Alert title (default: 'Error')
- `onDismiss?: () => void` - Callback when dismissed

---

### SuccessAlert
Display success messages with dismiss option.

```typescript
import SuccessAlert from './components/SuccessAlert';

<SuccessAlert 
  message="Operation completed successfully"
  title="Success"
  onDismiss={() => setSuccess(null)}
/>
```

**Props:**
- `message: string` - Success message (required)
- `title?: string` - Alert title (default: 'Success')
- `onDismiss?: () => void` - Callback when dismissed

---

### ProgressBar
Visual progress indicator with percentage.

```typescript
import ProgressBar from './components/ProgressBar';

<ProgressBar 
  progress={75}
  label="Uploading files..."
  showPercentage={true}
  color="bg-emerald-500"
/>
```

**Props:**
- `progress: number` - Progress value 0-100 (required)
- `label?: string` - Optional label text
- `showPercentage?: boolean` - Show percentage (default: true)
- `color?: string` - Tailwind background color (default: 'bg-emerald-500')

---

### Toast
Individual toast notification (usually managed by ToastContainer).

```typescript
import Toast from './components/Toast';

<Toast 
  id="unique-id"
  type="success"
  message="File uploaded successfully"
  duration={5000}
  onClose={(id) => removeToast(id)}
/>
```

**Props:**
- `id: string` - Unique identifier (required)
- `type: 'success' | 'error' | 'info' | 'warning'` - Toast type (required)
- `message: string` - Toast message (required)
- `duration?: number` - Auto-dismiss duration in ms (default: 5000)
- `onClose: (id: string) => void` - Callback when closed (required)

---

### ToastContainer (Provider)
Global toast notification system with context.

```typescript
import { ToastProvider, useToast } from './components/ToastContainer';

// Wrap your app
<ToastProvider>
  <App />
</ToastProvider>

// Use in components
function MyComponent() {
  const { showSuccess, showError, showInfo, showWarning } = useToast();
  
  showSuccess('Operation successful!');
  showError('Something went wrong!');
  showInfo('Here is some information');
  showWarning('Please be careful');
}
```

**Context Methods:**
- `showToast(type, message, duration?)` - Generic toast
- `showSuccess(message, duration?)` - Success toast
- `showError(message, duration?)` - Error toast
- `showInfo(message, duration?)` - Info toast
- `showWarning(message, duration?)` - Warning toast

---

### FileUploadZone
Drag & drop file upload area.

```typescript
import FileUploadZone from './components/FileUploadZone';

<FileUploadZone 
  onFilesSelected={(files) => handleFiles(files)}
  isExtracting={false}
  accept="image/*,text/*,.pdf"
  multiple={true}
/>
```

**Props:**
- `onFilesSelected: (files: File[]) => void` - Callback with selected files (required)
- `isExtracting?: boolean` - Show extracting state (default: false)
- `accept?: string` - File types to accept (default: all common types)
- `multiple?: boolean` - Allow multiple files (default: true)

---

### FileList
Display list of uploaded files with status.

```typescript
import FileList from './components/FileList';

<FileList 
  files={uploadedFiles}
  onRemove={(id) => removeFile(id)}
  onClearAll={() => clearAllFiles()}
/>
```

**Props:**
- `files: UploadedFile[]` - Array of uploaded files (required)
- `onRemove: (id: string) => void` - Callback to remove file (required)
- `onClearAll: () => void` - Callback to clear all files (required)

**UploadedFile Type:**
```typescript
interface UploadedFile {
  file: File;
  id: string;
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error';
  progress: number;
  error?: string;
  result?: AnalysisResult;
}
```

---

### AnalysisResults
Display analysis results in a grid layout.

```typescript
import AnalysisResults from './components/AnalysisResults';

<AnalysisResults 
  results={analysisResults}
  isLoading={false}
/>
```

**Props:**
- `results: AnalysisResult[]` - Array of analysis results (required)
- `isLoading?: boolean` - Show loading state (default: false)

**AnalysisResult Type:**
```typescript
interface AnalysisResult {
  file_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  status: 'processing' | 'completed' | 'failed';
  extracted_text?: string;
  embeddings?: number[];
  metadata?: Record<string, any>;
  thumbnail_url?: string;
  s3_url?: string;
  created_at?: string;
  error?: string;
}
```

---

### SearchBar
Search input with submit button.

```typescript
import SearchBar from './components/SearchBar';

<SearchBar 
  onSearch={(query) => handleSearch(query)}
  isSearching={false}
  placeholder="Search for similar items..."
/>
```

**Props:**
- `onSearch: (query: string) => void` - Callback with search query (required)
- `isSearching?: boolean` - Show searching state (default: false)
- `placeholder?: string` - Input placeholder (default: "Search for similar items...")

---

## 🪝 Custom Hooks

### useFileUpload
Manage file upload state and operations.

```typescript
import { useFileUpload } from './hooks/useFileUpload';

function MyComponent() {
  const {
    uploadedFiles,      // Array of UploadedFile
    isUploading,        // boolean
    uploadProgress,     // number (0-100)
    error,              // string | null
    addFiles,           // (files: File[]) => void
    removeFile,         // (id: string) => void
    clearFiles,         // () => void
    uploadFiles,        // (sessionId: string) => Promise<void>
  } = useFileUpload();
  
  // Add files
  addFiles([file1, file2]);
  
  // Upload to backend
  await uploadFiles('session_123');
  
  // Remove a file
  removeFile('file_id');
  
  // Clear all
  clearFiles();
}
```

**Return Type:**
```typescript
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
```

---

### useToast
Access toast notification system (must be inside ToastProvider).

```typescript
import { useToast } from './components/ToastContainer';

function MyComponent() {
  const { 
    showToast,    // (type, message, duration?) => void
    showSuccess,  // (message, duration?) => void
    showError,    // (message, duration?) => void
    showInfo,     // (message, duration?) => void
    showWarning,  // (message, duration?) => void
  } = useToast();
  
  // Show notifications
  showSuccess('File uploaded!');
  showError('Upload failed!');
  showInfo('Processing...');
  showWarning('Large file detected');
}
```

---

## 🔌 API Service

### apiService
Singleton instance for all API calls.

```typescript
import { apiService } from './services/api';

// Health check
const health = await apiService.healthCheck();

// Session management
const session = await apiService.createSession('session_id');
const sessionData = await apiService.getSession('session_id');

// File upload with progress
await apiService.uploadFiles(
  'session_id',
  [file1, file2],
  (progress) => {
    console.log(`${progress.percentage}% complete`);
  }
);

// Get analysis results
const results = await apiService.getAnalysisResults('session_id');
const fileResult = await apiService.getFileAnalysis('file_id');

// Vector search
const similar = await apiService.searchSimilar('query text', 10);
```

**Error Handling:**
All methods throw `ApiError`:
```typescript
try {
  await apiService.uploadFiles(...);
} catch (error) {
  const apiError = error as ApiError;
  console.error(apiError.message);  // User-friendly message
  console.error(apiError.status);   // HTTP status code
  console.error(apiError.detail);   // Detailed error info
}
```

---

## 📦 Type Definitions

All types are exported from `./types/index.ts`:

```typescript
import { 
  UploadedFile,
  AnalysisResult,
  SessionInfo,
  UploadProgress,
  ApiError,
  SearchResult,
  TabType,
  ToastMessage,
} from './types';
```

---

## 🎨 Styling

All components use Tailwind CSS with the emerald/green theme:

**Primary Colors:**
- `emerald-50` - Lightest text
- `emerald-100` - Secondary text
- `emerald-300` - Icons, accents
- `emerald-400` - Borders
- `emerald-500` - Buttons (hover)
- `emerald-600` - Buttons (default)
- `emerald-700` - Background gradients
- `emerald-800` - Dark backgrounds
- `emerald-900` - Darkest backgrounds

**Glass Morphism:**
```css
bg-white/10 backdrop-blur-md
bg-white/5 backdrop-blur-sm
```

**Animations:**
- `animate-spin` - Loading spinners
- `animate-fadeIn` - Fade in effect
- `transition-all` - Smooth transitions

---

## 🚀 Quick Start Example

Complete example using multiple components:

```typescript
import { useState } from 'react';
import { useToast } from './components/ToastContainer';
import { useFileUpload } from './hooks/useFileUpload';
import FileUploadZone from './components/FileUploadZone';
import FileList from './components/FileList';
import AnalysisResults from './components/AnalysisResults';
import ErrorAlert from './components/ErrorAlert';
import LoadingSpinner from './components/LoadingSpinner';

function MyFeature() {
  const { showSuccess, showError } = useToast();
  const {
    uploadedFiles,
    isUploading,
    uploadProgress,
    error,
    addFiles,
    removeFile,
    clearFiles,
    uploadFiles,
  } = useFileUpload();
  
  const [results, setResults] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      await uploadFiles('session_123');
      showSuccess('Files analyzed successfully!');
      // Get results from backend
      // setResults(await apiService.getAnalysisResults('session_123'));
    } catch (err) {
      showError('Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  return (
    <div>
      {error && <ErrorAlert message={error} />}
      
      <FileUploadZone onFilesSelected={addFiles} />
      
      <FileList 
        files={uploadedFiles}
        onRemove={removeFile}
        onClearAll={clearFiles}
      />
      
      {uploadedFiles.length > 0 && (
        <button onClick={handleAnalyze} disabled={isUploading}>
          {isUploading ? `Uploading ${uploadProgress}%` : 'Analyze'}
        </button>
      )}
      
      {isAnalyzing && <LoadingSpinner text="Analyzing..." />}
      
      <AnalysisResults results={results} isLoading={isAnalyzing} />
    </div>
  );
}
```

---

## 📝 Notes

- All components are fully typed with TypeScript
- All components are responsive and mobile-friendly
- All components follow the emerald/green theme
- All components handle loading and error states
- All components are accessible (keyboard navigation, ARIA labels)

---

**Last Updated**: November 30, 2025


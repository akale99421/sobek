# Frontend Integration Guide

## Overview

The frontend is now fully prepared for backend API integration with a complete component library, service layer, and state management.

## 🎯 Current Status

### ✅ Completed
- **API Service Layer** (`src/services/api.ts`)
- **Type Definitions** (`src/types/index.ts`)
- **Reusable Components**:
  - LoadingSpinner
  - ErrorAlert / SuccessAlert
  - ProgressBar
  - Toast notifications
  - FileUploadZone
  - FileList
  - AnalysisResults
  - SearchBar
- **Custom Hooks**:
  - useFileUpload (with progress tracking)
  - useToast (via ToastProvider)
- **Main App Integration** (App.tsx updated)

### 🔄 Ready for Backend Integration

The frontend is waiting for these backend endpoints:

## 📡 Expected API Endpoints

### 1. File Upload & Analysis
```typescript
POST /api/upload
Content-Type: multipart/form-data

Request:
- session_id: string
- files: File[]

Response:
{
  session_id: string,
  files: [
    {
      file_id: string,
      filename: string,
      file_type: string,
      file_size: number,
      status: 'processing' | 'completed' | 'failed',
      extracted_text?: string,
      embeddings?: number[],
      metadata?: object,
      thumbnail_url?: string,
      s3_url?: string,
      error?: string
    }
  ],
  message: string
}
```

### 2. Get Analysis Results
```typescript
GET /api/analysis/{session_id}

Response:
[
  {
    file_id: string,
    filename: string,
    file_type: string,
    status: string,
    extracted_text?: string,
    embeddings?: number[],
    metadata?: object
  }
]
```

### 3. Vector Search (Optional)
```typescript
POST /api/search
Content-Type: application/json

Request:
{
  query: string,
  limit: number
}

Response:
[
  {
    file_id: string,
    filename: string,
    similarity_score: number,
    ...other fields
  }
]
```

## 🔧 How to Integrate New Endpoints

### Step 1: Update API Service
When a new endpoint is ready, update `src/services/api.ts`:

```typescript
// Add new method to ApiService class
async newEndpoint(params: any): Promise<ResponseType> {
  return this.fetchWithError('/api/new-endpoint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  });
}
```

### Step 2: Update Types
Add new types to `src/types/index.ts`:

```typescript
export interface NewFeatureType {
  // Define your types here
}
```

### Step 3: Use in Components
Import and use in your components:

```typescript
import { apiService } from '../services/api';

const handleAction = async () => {
  try {
    const result = await apiService.newEndpoint(params);
    // Handle success
  } catch (error) {
    // Handle error
  }
};
```

## 📦 Component Usage Examples

### Using Toast Notifications
```typescript
import { useToast } from './components/ToastContainer';

function MyComponent() {
  const { showSuccess, showError, showInfo, showWarning } = useToast();
  
  const handleAction = async () => {
    try {
      await someApiCall();
      showSuccess('Operation completed!');
    } catch (error) {
      showError('Operation failed!');
    }
  };
}
```

### Using File Upload Hook
```typescript
import { useFileUpload } from './hooks/useFileUpload';

function MyComponent() {
  const {
    uploadedFiles,
    isUploading,
    uploadProgress,
    addFiles,
    removeFile,
    uploadFiles
  } = useFileUpload();
  
  const handleUpload = async () => {
    await uploadFiles(sessionId);
  };
}
```

### Using Loading Spinner
```typescript
import LoadingSpinner from './components/LoadingSpinner';

<LoadingSpinner size="lg" text="Loading..." />
```

### Using Progress Bar
```typescript
import ProgressBar from './components/ProgressBar';

<ProgressBar 
  progress={75} 
  label="Uploading..." 
  showPercentage={true}
/>
```

## 🎨 UI Components

### Alert Components
```typescript
import ErrorAlert from './components/ErrorAlert';
import SuccessAlert from './components/SuccessAlert';

<ErrorAlert 
  message="Something went wrong" 
  onDismiss={() => setError(null)}
/>

<SuccessAlert 
  message="Operation successful!" 
  onDismiss={() => setSuccess(null)}
/>
```

### File Upload Zone
```typescript
import FileUploadZone from './components/FileUploadZone';

<FileUploadZone 
  onFilesSelected={(files) => handleFiles(files)}
  isExtracting={isProcessing}
/>
```

### File List
```typescript
import FileList from './components/FileList';

<FileList 
  files={uploadedFiles}
  onRemove={(id) => removeFile(id)}
  onClearAll={() => clearAll()}
/>
```

### Analysis Results
```typescript
import AnalysisResults from './components/AnalysisResults';

<AnalysisResults 
  results={analysisResults}
  isLoading={isAnalyzing}
/>
```

## 🔐 Environment Variables

Create a `.env` file in the frontend directory:

```bash
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

For production:
```bash
VITE_API_URL=https://api.platinumsequence.com
VITE_ENV=production
```

## 🚀 Current Features

### Session Management
- ✅ Automatic session ID generation
- ✅ localStorage persistence
- ✅ Backend registration on mount

### File Handling
- ✅ Multi-file upload
- ✅ Drag & drop support
- ✅ ZIP file auto-extraction
- ✅ File type validation
- ✅ Progress tracking
- ✅ Individual file removal

### UI/UX
- ✅ Toast notifications
- ✅ Loading states
- ✅ Error handling
- ✅ Success feedback
- ✅ Progress indicators
- ✅ Responsive design
- ✅ Beautiful animations

## 📝 Next Steps for Backend Agent

When you complete an API endpoint, please provide:

1. **Endpoint URL** (e.g., `/api/upload`)
2. **HTTP Method** (POST, GET, etc.)
3. **Request Format**:
   ```typescript
   {
     field1: type,
     field2: type
   }
   ```
4. **Response Format**:
   ```typescript
   {
     result1: type,
     result2: type
   }
   ```
5. **Error Codes** and messages
6. **Any special headers** or authentication

I'll immediately integrate it into the frontend!

## 🧪 Testing the Frontend

### Start Development Server
```bash
cd frontend
npm run dev
```

### Test File Upload
1. Open http://localhost:5173
2. Click "Choose Files" or drag & drop
3. Select multiple files (including ZIPs)
4. Click "Analyze Files"
5. Watch progress and see results

### Test Toast Notifications
Toast notifications will appear automatically for:
- ✅ Successful operations
- ❌ Errors
- ℹ️ Information
- ⚠️ Warnings

## 📚 File Structure

```
frontend/src/
├── components/
│   ├── LoadingSpinner.tsx
│   ├── ErrorAlert.tsx
│   ├── SuccessAlert.tsx
│   ├── ProgressBar.tsx
│   ├── Toast.tsx
│   ├── ToastContainer.tsx
│   ├── FileUploadZone.tsx
│   ├── FileList.tsx
│   ├── AnalysisResults.tsx
│   └── SearchBar.tsx
├── hooks/
│   └── useFileUpload.ts
├── services/
│   └── api.ts
├── types/
│   └── index.ts
├── App.tsx
├── main.tsx
└── index.css
```

## 🎯 Integration Checklist

When backend completes an endpoint:

- [ ] Update `api.ts` with new method
- [ ] Add types to `types/index.ts`
- [ ] Update component to call new API
- [ ] Add loading states
- [ ] Add error handling
- [ ] Add success feedback
- [ ] Test with real data
- [ ] Update this guide

## 💡 Tips

1. **Error Handling**: All API calls are wrapped with try-catch
2. **Loading States**: Use `isLoading` flags for better UX
3. **Toast Notifications**: Use for quick feedback
4. **Progress Bars**: Use for long operations
5. **Type Safety**: All responses are typed

## 🐛 Troubleshooting

### CORS Issues
Make sure backend has CORS configured for `http://localhost:5173`

### API Not Responding
Check that backend is running on `http://localhost:8000`

### TypeScript Errors
Run `npm run build` to check for type errors

---

**Status**: ✅ Frontend ready for backend integration!
**Last Updated**: November 30, 2025


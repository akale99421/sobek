import { useState, useEffect } from 'react'
import JSZip from 'jszip'
import { ToastProvider, useToast } from './components/ToastContainer'
import { apiService } from './services/api'
import { useFileUpload } from './hooks/useFileUpload'
import { AnalysisResult } from './types'
import FileUploadZone from './components/FileUploadZone'
import FileList from './components/FileList'
import AnalysisResults from './components/AnalysisResults'
import ErrorAlert from './components/ErrorAlert'
import SuccessAlert from './components/SuccessAlert'

function AppContent() {
  const [activeTab, setActiveTab] = useState('inventory')
  const [isExtracting, setIsExtracting] = useState(false)
  const [sessionId, setSessionId] = useState<string>('')
  const [analysisResults, setAnalysisResults] = useState<AnalysisResult[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  
  const { showToast, showError, showSuccess } = useToast()
  const {
    uploadedFiles,
    isUploading,
    uploadProgress,
    error: uploadError,
    addFiles: addFilesToUpload,
    removeFile,
    clearFiles,
    uploadFiles: performUpload,
  } = useFileUpload()

  const generateSessionId = () => {
    return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`
  }

  const registerSession = async (sid: string) => {
    try {
      const data = await apiService.createSession(sid)
      console.log('Session registered:', data)
    } catch (error) {
      console.error('Failed to register session:', error)
      showError('Failed to register session. Some features may not work.')
    }
  }

  useEffect(() => {
    let sid = localStorage.getItem('sessionId')
    if (!sid) {
      sid = generateSessionId()
      localStorage.setItem('sessionId', sid)
    }
    setSessionId(sid)
    registerSession(sid)
  }, [])

  const extractZipFile = async (zipFile: File): Promise<File[]> => {
    try {
      const zip = new JSZip()
      const contents = await zip.loadAsync(zipFile)
      const extractedFiles: File[] = []

      for (const [filename, file] of Object.entries(contents.files)) {
        if (!file.dir) {
          const blob = await file.async('blob')
          const extractedFile = new File([blob], filename, { type: blob.type })
          extractedFiles.push(extractedFile)
        }
      }

      return extractedFiles
    } catch (error) {
      console.error('Error extracting zip:', error)
      showError(`Failed to extract ZIP file: ${zipFile.name}`)
      return []
    }
  }

  const handleFileUpload = async (files: File[]) => {
    setIsExtracting(true)
    setError(null)
    const allFiles: File[] = []

    for (const file of files) {
      if (file.name.endsWith('.zip')) {
        console.log('Extracting zip:', file.name)
        const extractedFiles = await extractZipFile(file)
        console.log('Extracted files:', extractedFiles.map(f => f.name))
        allFiles.push(...extractedFiles)
      } else {
        allFiles.push(file)
      }
    }

    addFilesToUpload(allFiles)
    setIsExtracting(false)
    
    if (allFiles.length > 0) {
      showSuccess(`Added ${allFiles.length} file(s)`)
    }
  }

  const handleAnalyzeFiles = async () => {
    if (uploadedFiles.length === 0) {
      showError('Please upload files first')
      return
    }

    setError(null)
    setSuccess(null)
    setIsAnalyzing(true)

    try {
      // Upload files to backend
      await performUpload(sessionId)
      
      // Get analysis results (this will be implemented when backend is ready)
      // For now, we'll show a success message
      setSuccess(`Successfully uploaded ${uploadedFiles.length} file(s). Analysis in progress...`)
      showSuccess('Files uploaded successfully!')
      
      // TODO: Poll for results or use WebSocket when backend implements it
      // const results = await apiService.getAnalysisResults(sessionId)
      // setAnalysisResults(results)
      
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to analyze files'
      setError(errorMessage)
      showError(errorMessage)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-600 via-green-700 to-emerald-800 font-sans">
      {/* Header */}
      <header className="bg-gradient-to-r from-emerald-900 to-green-900 border-b border-emerald-800 shadow-xl">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between py-4">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="text-5xl">🐊</div>
              <div>
                <h1 className="text-2xl font-semibold text-emerald-50">Platinum Sequence</h1>
                {sessionId && (
                  <p className="text-xs text-emerald-300/70">Session: {sessionId.substring(0, 20)}...</p>
                )}
              </div>
            </div>
            
            {/* Navigation Tabs */}
            <nav className="flex space-x-2">
              <button
                onClick={() => setActiveTab('inventory')}
                className={`px-6 py-2.5 rounded-lg font-normal transition-all ${
                  activeTab === 'inventory'
                    ? 'bg-emerald-600 text-white shadow-lg'
                    : 'text-emerald-100 hover:bg-emerald-800/50'
                }`}
              >
                Inventory Analysis
              </button>
              <button
                onClick={() => setActiveTab('extraction')}
                className={`px-6 py-2.5 rounded-lg font-normal transition-all ${
                  activeTab === 'extraction'
                    ? 'bg-emerald-600 text-white shadow-lg'
                    : 'text-emerald-100 hover:bg-emerald-800/50'
                }`}
              >
                Extraction
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-2xl">
          {activeTab === 'inventory' && (
            <div>
              <h2 className="text-3xl font-semibold mb-6 text-emerald-50">Inventory Analysis</h2>
              <p className="text-lg text-emerald-100/90 mb-8">
                Analyze your inventory data with AI-powered insights.
              </p>

              {/* Error/Success Messages */}
              {error && (
                <div className="mb-6">
                  <ErrorAlert message={error} onDismiss={() => setError(null)} />
                </div>
              )}
              {success && (
                <div className="mb-6">
                  <SuccessAlert message={success} onDismiss={() => setSuccess(null)} />
                </div>
              )}

              {/* File Upload Section */}
              <FileUploadZone 
                onFilesSelected={handleFileUpload}
                isExtracting={isExtracting}
              />

              {/* Uploaded Files List */}
              <FileList 
                files={uploadedFiles}
                onRemove={removeFile}
                onClearAll={clearFiles}
              />

              {/* Analyze Button */}
              {uploadedFiles.length > 0 && (
                <div className="mt-6">
                  <button 
                    onClick={handleAnalyzeFiles}
                    disabled={isUploading || isAnalyzing}
                    className="w-full px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-all shadow-lg hover:shadow-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isUploading 
                      ? `Uploading... ${uploadProgress}%` 
                      : isAnalyzing 
                      ? 'Analyzing...' 
                      : 'Analyze Files'}
                  </button>
                </div>
              )}

              {/* Analysis Results */}
              <AnalysisResults 
                results={analysisResults}
                isLoading={isAnalyzing}
              />
            </div>
          )}
          
          {activeTab === 'extraction' && (
            <div>
              <h2 className="text-3xl font-semibold mb-4 text-emerald-50">Extraction</h2>
              <p className="text-lg text-emerald-100/90 mb-8">
                Extract and process data from multiple sources.
              </p>
              <div className="bg-white/5 rounded-xl p-8 border border-emerald-400/20 text-center">
                <div className="text-emerald-300/50 mb-4">
                  <svg className="mx-auto h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
                <p className="text-emerald-200/70">
                  Extraction features coming soon...
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

function App() {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  )
}

export default App

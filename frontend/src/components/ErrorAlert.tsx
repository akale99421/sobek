interface ErrorAlertProps {
  message: string;
  onDismiss?: () => void;
  title?: string;
}

export default function ErrorAlert({ message, onDismiss, title = 'Error' }: ErrorAlertProps) {
  return (
    <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 backdrop-blur-sm">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <svg 
            className="h-5 w-5 text-red-400 mt-0.5 flex-shrink-0" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
            />
          </svg>
          <div>
            <h3 className="text-red-300 font-semibold">{title}</h3>
            <p className="text-red-200/90 text-sm mt-1">{message}</p>
          </div>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-red-400 hover:text-red-300 transition-colors ml-4"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}


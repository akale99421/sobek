interface SuccessAlertProps {
  message: string;
  onDismiss?: () => void;
  title?: string;
}

export default function SuccessAlert({ message, onDismiss, title = 'Success' }: SuccessAlertProps) {
  return (
    <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-4 backdrop-blur-sm">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <svg 
            className="h-5 w-5 text-emerald-400 mt-0.5 flex-shrink-0" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" 
            />
          </svg>
          <div>
            <h3 className="text-emerald-300 font-semibold">{title}</h3>
            <p className="text-emerald-200/90 text-sm mt-1">{message}</p>
          </div>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-emerald-400 hover:text-emerald-300 transition-colors ml-4"
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


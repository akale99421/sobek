interface ProgressBarProps {
  progress: number;
  label?: string;
  showPercentage?: boolean;
  color?: string;
}

export default function ProgressBar({ 
  progress, 
  label, 
  showPercentage = true,
  color = 'bg-emerald-500'
}: ProgressBarProps) {
  const clampedProgress = Math.min(Math.max(progress, 0), 100);

  return (
    <div className="w-full">
      {(label || showPercentage) && (
        <div className="flex items-center justify-between mb-2">
          {label && <span className="text-sm text-emerald-200">{label}</span>}
          {showPercentage && (
            <span className="text-sm text-emerald-300 font-medium">
              {Math.round(clampedProgress)}%
            </span>
          )}
        </div>
      )}
      <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
        <div
          className={`h-full ${color} transition-all duration-300 ease-out rounded-full`}
          style={{ width: `${clampedProgress}%` }}
        />
      </div>
    </div>
  );
}


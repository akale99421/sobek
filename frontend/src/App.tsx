import { useEffect, useState } from 'react'

function App() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center px-4">
      <div className={`text-center ${isVisible ? 'animate-fadeIn' : 'opacity-0'}`}>
        <div className="mb-8 animate-float">
          <div className="inline-block">
            <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-r from-purple-400 to-pink-400 opacity-80 blur-xl"></div>
            <div className="w-24 h-24 mx-auto -mt-24 mb-6 rounded-full bg-gradient-to-r from-purple-500 to-pink-500"></div>
          </div>
        </div>
        
        <h1 className="text-6xl md:text-8xl font-bold text-white mb-6 tracking-tight">
          Platinum
          <span className="block bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent">
            Sequence
          </span>
        </h1>
        
        <p className="text-xl md:text-2xl text-purple-200 mb-8 font-light">
          Something extraordinary is coming
        </p>
        
        <div className="flex items-center justify-center space-x-2">
          <div className="w-3 h-3 bg-purple-400 rounded-full animate-pulse"></div>
          <div className="w-3 h-3 bg-pink-400 rounded-full animate-pulse delay-75"></div>
          <div className="w-3 h-3 bg-purple-400 rounded-full animate-pulse delay-150"></div>
        </div>
      </div>
    </div>
  )
}

export default App

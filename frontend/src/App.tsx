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
          Sobek by Platinum Sequence
        </h1>        
      </div>
    </div>
  )
}

export default App

import { useEffect, useState } from 'react'
import { Apple, Carrot, Fish, Beef, Salad, Cookie, Coffee, Loader2 } from 'lucide-react'

const foodIcons = [
  { Icon: Apple, color: 'text-red-500' },
  { Icon: Carrot, color: 'text-orange-500' },
  { Icon: Fish, color: 'text-blue-500' },
  { Icon: Beef, color: 'text-red-700' },
  { Icon: Salad, color: 'text-green-500' },
  { Icon: Cookie, color: 'text-yellow-600' },
  { Icon: Coffee, color: 'text-amber-700' }
]

const loadingMessages = [
  "Analizando tus datos nutricionales...",
  "Calculando requerimientos calóricos...",
  "Seleccionando las mejores recetas...",
  "Optimizando la distribución de macros...",
  "Personalizando tu plan alimentario...",
  "Finalizando tu plan nutricional..."
]

interface LoadingOverlayProps {
  isOpen: boolean
}

export function LoadingOverlay({ isOpen }: LoadingOverlayProps) {
  const [messageIndex, setMessageIndex] = useState(0)
  
  useEffect(() => {
    if (!isOpen) {
      setMessageIndex(0)
      return
    }
    
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % loadingMessages.length)
    }, 3000)
    
    return () => clearInterval(interval)
  }, [isOpen])
  
  // Prevent body scroll when overlay is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }
    
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])
  
  if (!isOpen) return null
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      
      {/* Content */}
      <div className="relative z-10 flex flex-col items-center space-y-8 p-8">
        {/* Main loading animation container */}
        <div className="relative h-48 w-48">
          {/* Central spinner */}
          <div className="absolute inset-0 flex items-center justify-center">
            <Loader2 className="h-16 w-16 animate-spin text-primary" />
          </div>
          
          {/* Rotating food icons */}
          <div className="absolute inset-0 animate-spin-slow">
            {foodIcons.map(({ Icon, color }, index) => {
              const angle = (index / foodIcons.length) * 2 * Math.PI
              const radius = 80
              const x = Math.cos(angle) * radius
              const y = Math.sin(angle) * radius
              
              return (
                <div
                  key={index}
                  className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
                  style={{
                    transform: `translate(-50%, -50%) translate(${x}px, ${y}px)`
                  }}
                >
                  <Icon className={`h-8 w-8 ${color} animate-bounce-slow`} 
                    style={{ animationDelay: `${index * 0.2}s` }} />
                </div>
              )
            })}
          </div>
        </div>
        
        {/* Loading text */}
        <div className="text-center space-y-3 max-w-md">
          <h3 className="text-2xl font-semibold text-white">
            Creando tu plan nutricional
          </h3>
          <p className="text-lg text-gray-200 transition-all duration-500">
            {loadingMessages[messageIndex]}
          </p>
          <p className="text-sm text-gray-300">
            Esto puede tomar unos momentos. Por favor, espera...
          </p>
        </div>
        
        {/* Progress dots */}
        <div className="flex space-x-2">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className={`h-2 w-2 rounded-full transition-all duration-300 ${
                i <= messageIndex
                  ? 'bg-primary scale-100'
                  : 'bg-gray-500 scale-75'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
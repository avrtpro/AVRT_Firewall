import React, { useState } from 'react'
import Header from './components/Header'
import VoiceInput from './components/VoiceInput'
import TextInput from './components/TextInput'
import ScoringDisplay from './components/ScoringDisplay'
import LogsPanel from './components/LogsPanel'
import StatsPanel from './components/StatsPanel'

function App() {
  const [activeTab, setActiveTab] = useState('voice')
  const [validationResult, setValidationResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleValidationComplete = (result) => {
    setValidationResult(result)
    setIsLoading(false)
  }

  const handleValidationStart = () => {
    setIsLoading(true)
    setValidationResult(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Mode Selection */}
        <div className="flex gap-4 mb-8 justify-center">
          <button
            onClick={() => setActiveTab('voice')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'voice'
                ? 'bg-avrt-primary text-white shadow-lg scale-105'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            🎤 Voice Input
          </button>
          <button
            onClick={() => setActiveTab('text')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'text'
                ? 'bg-avrt-primary text-white shadow-lg scale-105'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            ✍️ Text Input
          </button>
          <button
            onClick={() => setActiveTab('logs')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'logs'
                ? 'bg-avrt-primary text-white shadow-lg scale-105'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            📊 Logs & Stats
          </button>
        </div>

        {/* Content Area */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Panel */}
          <div>
            {activeTab === 'voice' && (
              <VoiceInput
                onValidationComplete={handleValidationComplete}
                onValidationStart={handleValidationStart}
                isLoading={isLoading}
              />
            )}
            {activeTab === 'text' && (
              <TextInput
                onValidationComplete={handleValidationComplete}
                onValidationStart={handleValidationStart}
                isLoading={isLoading}
              />
            )}
            {activeTab === 'logs' && (
              <div className="space-y-6">
                <LogsPanel />
                <StatsPanel />
              </div>
            )}
          </div>

          {/* Results Panel */}
          {activeTab !== 'logs' && (
            <div>
              <ScoringDisplay
                result={validationResult}
                isLoading={isLoading}
              />
            </div>
          )}
        </div>

        {/* Footer Info */}
        <div className="mt-12 text-center text-sm text-gray-600">
          <p className="mb-2">
            🛡️ AVRT™ - Advanced Voice Reasoning Technology
          </p>
          <p className="mb-2">
            Patent: USPTO #19/236,935 | Founder: Jason I. Proper
          </p>
          <p className="font-semibold text-avrt-primary">
            Be Good. Be Humble. Be Protected.™
          </p>
        </div>
      </main>
    </div>
  )
}

export default App

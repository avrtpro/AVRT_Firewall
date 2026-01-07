import React, { useState } from 'react'
import { Send } from 'lucide-react'

export default function TextInput({ onValidationComplete, onValidationStart, isLoading }) {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')

  const handleValidate = async () => {
    if (!output.trim()) {
      alert('Please enter text to validate')
      return
    }

    onValidationStart()

    try {
      const response = await fetch('/api/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          input: input.trim() || 'Direct text validation',
          output: output.trim(),
          context: {
            mode: 'text',
            timestamp: new Date().toISOString()
          }
        })
      })

      if (!response.ok) {
        throw new Error('Validation failed')
      }

      const result = await response.json()
      onValidationComplete(result)
    } catch (error) {
      console.error('Validation error:', error)
      alert('Validation failed. Please check your connection and try again.')
      onValidationComplete(null)
    }
  }

  return (
    <div className="card space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          ✍️ Text Input
        </h2>
        <p className="text-gray-600">
          Enter text directly for SPIEL™ + THT™ validation
        </p>
      </div>

      {/* User Input (Optional) */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          User Input (Optional)
        </label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter the user's original input/question..."
          className="textarea-field"
          rows={3}
          disabled={isLoading}
        />
      </div>

      {/* AI Output to Validate */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          AI Output to Validate <span className="text-red-500">*</span>
        </label>
        <textarea
          value={output}
          onChange={(e) => setOutput(e.target.value)}
          placeholder="Enter the AI-generated response to validate against SPIEL™ + THT™ standards..."
          className="textarea-field"
          rows={8}
          disabled={isLoading}
        />
        <p className="text-xs text-gray-500 mt-2">
          This text will be analyzed using SPIEL™ (Safety, Personalization, Integrity, Ethics, Logic)
          and THT™ (Truth, Honesty, Transparency) protocols
        </p>
      </div>

      {/* Example Texts */}
      <div className="bg-gray-50 rounded-lg p-4">
        <p className="text-sm font-semibold text-gray-700 mb-2">
          Quick Examples:
        </p>
        <div className="space-y-2">
          <button
            onClick={() => setOutput('I can help you with that! Based on current research, this approach is recommended because it balances safety and effectiveness.')}
            className="text-xs text-blue-600 hover:underline block"
            disabled={isLoading}
          >
            ✅ Safe Response Example
          </button>
          <button
            onClick={() => setOutput('You should definitely attack this problem aggressively. Trust me, this will work 100% guaranteed.')}
            className="text-xs text-red-600 hover:underline block"
            disabled={isLoading}
          >
            ❌ Unsafe Response Example
          </button>
        </div>
      </div>

      {/* Validate Button */}
      <button
        onClick={handleValidate}
        disabled={isLoading || !output.trim()}
        className="w-full btn-primary py-4 text-lg font-bold flex items-center justify-center gap-2"
      >
        <Send className="w-5 h-5" />
        {isLoading ? 'Validating...' : '🛡️ Validate with AVRT™'}
      </button>
    </div>
  )
}

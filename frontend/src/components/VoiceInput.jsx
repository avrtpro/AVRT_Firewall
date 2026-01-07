import React, { useState, useRef } from 'react'
import { Mic, Square, Upload } from 'lucide-react'

export default function VoiceInput({ onValidationComplete, onValidationStart, isLoading }) {
  const [isRecording, setIsRecording] = useState(false)
  const [audioFile, setAudioFile] = useState(null)
  const [transcription, setTranscription] = useState('')
  const [aiResponse, setAiResponse] = useState('')
  const fileInputRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
        }
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        const file = new File([blob], 'recording.webm', { type: 'audio/webm' })
        setAudioFile(file)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Failed to start recording:', error)
      alert('Failed to access microphone. Please check permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setAudioFile(file)
    }
  }

  const handleValidate = async () => {
    if (!audioFile && !aiResponse) {
      alert('Please record audio or enter AI response to validate')
      return
    }

    onValidationStart()

    try {
      const formData = new FormData()

      if (audioFile) {
        formData.append('audio', audioFile)
      }

      if (aiResponse) {
        formData.append('aiResponse', aiResponse)
      }

      const endpoint = audioFile ? '/api/validate-voice' : '/api/validate'
      const response = await fetch(endpoint, {
        method: 'POST',
        body: audioFile ? formData : JSON.stringify({ output: aiResponse }),
        headers: audioFile ? {} : { 'Content-Type': 'application/json' }
      })

      if (!response.ok) {
        throw new Error('Validation failed')
      }

      const result = await response.json()

      if (result.transcription) {
        setTranscription(result.transcription)
      }

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
          🎤 Voice Input
        </h2>
        <p className="text-gray-600">
          Record your voice or upload an audio file for transcription and validation
        </p>
      </div>

      {/* Recording Controls */}
      <div className="flex gap-4">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`flex-1 flex items-center justify-center gap-2 px-6 py-4 rounded-lg font-semibold transition-all ${
            isRecording
              ? 'bg-red-500 text-white hover:bg-red-600 animate-pulse'
              : 'bg-avrt-primary text-white hover:bg-blue-600'
          }`}
          disabled={isLoading}
        >
          {isRecording ? (
            <>
              <Square className="w-5 h-5" />
              Stop Recording
            </>
          ) : (
            <>
              <Mic className="w-5 h-5" />
              Start Recording
            </>
          )}
        </button>

        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center justify-center gap-2 px-6 py-4 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors font-semibold"
          disabled={isLoading}
        >
          <Upload className="w-5 h-5" />
          Upload Audio
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*"
          onChange={handleFileUpload}
          className="hidden"
        />
      </div>

      {/* Audio File Status */}
      {audioFile && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
          <p className="text-green-800 font-semibold">
            ✓ Audio file ready: {audioFile.name}
          </p>
          <p className="text-sm text-green-600">
            Size: {(audioFile.size / 1024).toFixed(1)} KB
          </p>
        </div>
      )}

      {/* Transcription Display */}
      {transcription && (
        <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
          <p className="font-semibold text-blue-900 mb-2">Transcription:</p>
          <p className="text-blue-800">{transcription}</p>
        </div>
      )}

      {/* AI Response Input */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          AI Response to Validate (Optional)
        </label>
        <textarea
          value={aiResponse}
          onChange={(e) => setAiResponse(e.target.value)}
          placeholder="Enter the AI-generated response you want to validate..."
          className="textarea-field"
          rows={6}
          disabled={isLoading}
        />
        <p className="text-xs text-gray-500 mt-2">
          If left empty, the transcription will be validated instead
        </p>
      </div>

      {/* Validate Button */}
      <button
        onClick={handleValidate}
        disabled={isLoading || (!audioFile && !aiResponse)}
        className="w-full btn-primary py-4 text-lg font-bold"
      >
        {isLoading ? 'Validating...' : '🛡️ Validate with AVRT™'}
      </button>
    </div>
  )
}

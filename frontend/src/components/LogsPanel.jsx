import React, { useState, useEffect } from 'react'
import { Clock, Hash, AlertCircle } from 'lucide-react'

export default function LogsPanel() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/logs?limit=50')

      if (!response.ok) {
        throw new Error('Failed to fetch logs')
      }

      const data = await response.json()
      setLogs(data.logs || [])
      setError(null)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching logs:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">📋 Recent Logs</h3>
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-avrt-primary"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">📋 Recent Logs</h3>
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-6 h-6 text-red-500" />
          <div>
            <p className="font-semibold text-red-800">Error loading logs</p>
            <p className="text-sm text-red-600">{error}</p>
          </div>
        </div>
        <button
          onClick={fetchLogs}
          className="mt-4 btn-primary w-full"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-800">📋 Recent Logs</h3>
        <button
          onClick={fetchLogs}
          className="text-sm text-avrt-primary hover:underline font-semibold"
        >
          🔄 Refresh
        </button>
      </div>

      {logs.length === 0 ? (
        <div className="text-center py-10 text-gray-400">
          <p className="text-lg font-semibold">No logs yet</p>
          <p className="text-sm">Start validating to see interaction logs</p>
        </div>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {logs.map((log, index) => (
            <LogEntry key={log.interactionId || index} log={log} />
          ))}
        </div>
      )}

      <div className="mt-4 pt-4 border-t-2 text-sm text-gray-600 text-center">
        Showing {logs.length} most recent interactions
      </div>
    </div>
  )
}

function LogEntry({ log }) {
  const getStatusBadge = (status) => {
    switch (status) {
      case 'safe':
        return <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">SAFE</span>
      case 'warning':
        return <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-semibold">WARNING</span>
      case 'blocked':
        return <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-semibold">BLOCKED</span>
      default:
        return <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-semibold">UNKNOWN</span>
    }
  }

  return (
    <div className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors">
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          {getStatusBadge(log.status)}
          <span className="text-sm font-mono text-gray-500">
            {log.interactionId?.substring(0, 16)}...
          </span>
        </div>
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <Clock className="w-3 h-3" />
          {new Date(log.timestamp).toLocaleTimeString()}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="font-semibold text-gray-600">SPIEL:</span>
          <span className={`ml-2 font-bold ${
            log.spielComposite >= 85 ? 'text-green-600' :
            log.spielComposite >= 70 ? 'text-yellow-600' : 'text-red-600'
          }`}>
            {log.spielComposite?.toFixed(1) || 'N/A'}
          </span>
        </div>
        <div>
          <span className="font-semibold text-gray-600">THT:</span>
          <span className={`ml-2 font-bold ${log.thtCompliant ? 'text-green-600' : 'text-red-600'}`}>
            {log.thtCompliant ? 'Compliant' : 'Non-Compliant'}
          </span>
        </div>
      </div>

      {log.hash && (
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Hash className="w-3 h-3" />
            <span className="font-mono truncate">{log.hash}</span>
          </div>
        </div>
      )}
    </div>
  )
}

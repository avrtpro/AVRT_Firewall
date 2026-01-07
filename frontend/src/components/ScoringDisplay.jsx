import React from 'react'
import { Shield, AlertTriangle, CheckCircle, XCircle, Hash } from 'lucide-react'

export default function ScoringDisplay({ result, isLoading }) {
  if (isLoading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-avrt-primary"></div>
        </div>
        <p className="text-center text-gray-600 font-semibold">
          Analyzing with SPIEL™ + THT™...
        </p>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="card">
        <div className="text-center py-20 text-gray-400">
          <Shield className="w-20 h-20 mx-auto mb-4 opacity-30" />
          <p className="text-lg font-semibold">No validation results yet</p>
          <p className="text-sm">Submit input to see SPIEL™ + THT™ scoring</p>
        </div>
      </div>
    )
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'safe':
        return 'green'
      case 'warning':
        return 'yellow'
      case 'blocked':
        return 'red'
      default:
        return 'gray'
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600 border-green-300 bg-green-50'
    if (score >= 80) return 'text-blue-600 border-blue-300 bg-blue-50'
    if (score >= 70) return 'text-yellow-600 border-yellow-300 bg-yellow-50'
    return 'text-red-600 border-red-300 bg-red-50'
  }

  const statusColor = getStatusColor(result.status)

  return (
    <div className="space-y-6">
      {/* Overall Status */}
      <div className={`card border-4 border-${statusColor}-400 bg-${statusColor}-50`}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-2xl font-bold text-gray-800">Validation Result</h3>
          {result.status === 'safe' && <CheckCircle className="w-10 h-10 text-green-500" />}
          {result.status === 'warning' && <AlertTriangle className="w-10 h-10 text-yellow-500" />}
          {result.status === 'blocked' && <XCircle className="w-10 h-10 text-red-500" />}
        </div>

        <div className={`text-center py-6 bg-${statusColor}-100 rounded-lg`}>
          <p className="text-3xl font-bold text-gray-800 mb-2">
            {result.status.toUpperCase()}
          </p>
          <p className={`text-${statusColor}-700 font-semibold`}>
            {result.message}
          </p>
        </div>
      </div>

      {/* SPIEL Scores */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          🛡️ SPIEL™ Framework Scores
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
          <ScoreCard
            label="Safety"
            score={result.spiel.scores.safety}
            icon="🛡️"
          />
          <ScoreCard
            label="Personalization"
            score={result.spiel.scores.personalization}
            icon="👤"
          />
          <ScoreCard
            label="Integrity"
            score={result.spiel.scores.integrity}
            icon="🔐"
          />
          <ScoreCard
            label="Ethics"
            score={result.spiel.scores.ethics}
            icon="⚖️"
          />
          <ScoreCard
            label="Logic"
            score={result.spiel.scores.logic}
            icon="🧠"
          />
          <ScoreCard
            label="Composite"
            score={result.spiel.scores.composite}
            icon="📊"
            highlight={true}
          />
        </div>

        {/* Violations */}
        {result.spiel.violations && result.spiel.violations.length > 0 && (
          <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
            <p className="font-bold text-red-800 mb-2">⚠️ Violations Detected:</p>
            <ul className="space-y-1">
              {result.spiel.violations.map((violation, index) => (
                <li key={index} className="text-sm text-red-700">
                  • {violation.type}: {violation.score.toFixed(1)}/100
                  (threshold: {violation.threshold})
                  - Severity: {violation.severity}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* THT Validation */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          ✓ THT™ Protocol Validation
        </h3>

        <div className="space-y-3">
          <THTIndicator
            label="Truth"
            verified={result.tht.truthVerified}
            detail={result.tht.details.truth}
          />
          <THTIndicator
            label="Honesty"
            verified={result.tht.honestyVerified}
            detail={result.tht.details.honesty}
          />
          <THTIndicator
            label="Transparency"
            verified={result.tht.transparencyVerified}
            detail={result.tht.details.transparency}
          />
        </div>

        <div className="mt-4 pt-4 border-t-2">
          <div className="flex justify-between items-center">
            <span className="font-semibold text-gray-700">Confidence Score:</span>
            <span className="text-2xl font-bold text-avrt-primary">
              {(result.tht.confidenceScore * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex justify-between items-center mt-2">
            <span className="font-semibold text-gray-700">Compliance Status:</span>
            <span className={`font-bold ${result.tht.isCompliant ? 'text-green-600' : 'text-red-600'}`}>
              {result.tht.isCompliant ? '✓ Compliant' : '✗ Non-Compliant'}
            </span>
          </div>
        </div>

        {result.tht.issues && result.tht.issues.length > 0 && (
          <div className="mt-4 bg-yellow-50 border-2 border-yellow-200 rounded-lg p-4">
            <p className="font-bold text-yellow-800 mb-2">⚠️ THT™ Issues:</p>
            <ul className="space-y-1">
              {result.tht.issues.map((issue, index) => (
                <li key={index} className="text-sm text-yellow-700">
                  • {issue}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Hash & Metadata */}
      {result.hash && (
        <div className="card bg-gray-50">
          <div className="flex items-center gap-2 mb-3">
            <Hash className="w-5 h-5 text-gray-600" />
            <h3 className="text-lg font-bold text-gray-800">
              SHA-256 Hash
            </h3>
          </div>
          <div className="bg-white rounded-lg p-3 font-mono text-xs break-all border-2 border-gray-200">
            {result.hash}
          </div>
          {result.interactionId && (
            <p className="text-xs text-gray-600 mt-2">
              Interaction ID: {result.interactionId}
            </p>
          )}
          <p className="text-xs text-gray-500 mt-2">
            ⛓️ OriginStamp ready for blockchain verification
          </p>
        </div>
      )}
    </div>
  )
}

function ScoreCard({ label, score, icon, highlight = false }) {
  const getScoreColor = (score) => {
    if (score >= 90) return 'border-green-300 bg-green-50 text-green-700'
    if (score >= 80) return 'border-blue-300 bg-blue-50 text-blue-700'
    if (score >= 70) return 'border-yellow-300 bg-yellow-50 text-yellow-700'
    return 'border-red-300 bg-red-50 text-red-700'
  }

  return (
    <div className={`score-card ${getScoreColor(score)} ${highlight ? 'ring-2 ring-avrt-primary' : ''}`}>
      <div className="text-center">
        <div className="text-2xl mb-1">{icon}</div>
        <div className="text-sm font-semibold text-gray-600 mb-1">{label}</div>
        <div className="text-3xl font-bold">{score.toFixed(1)}</div>
        <div className="text-xs text-gray-500">/ 100</div>
      </div>
    </div>
  )
}

function THTIndicator({ label, verified, detail }) {
  return (
    <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3">
      <div className="flex items-center gap-3">
        <div className={`w-6 h-6 rounded-full flex items-center justify-center ${
          verified ? 'bg-green-500' : 'bg-red-500'
        }`}>
          {verified ? (
            <CheckCircle className="w-4 h-4 text-white" />
          ) : (
            <XCircle className="w-4 h-4 text-white" />
          )}
        </div>
        <span className="font-semibold text-gray-800">{label}</span>
      </div>
      <span className={`font-bold ${verified ? 'text-green-600' : 'text-red-600'}`}>
        {detail}
      </span>
    </div>
  )
}

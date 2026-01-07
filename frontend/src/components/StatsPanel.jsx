import React, { useState, useEffect } from 'react'
import { BarChart, Activity, Shield, CheckCircle, AlertCircle } from 'lucide-react'

export default function StatsPanel() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/stats')

      if (!response.ok) {
        throw new Error('Failed to fetch statistics')
      }

      const data = await response.json()
      setStats(data)
      setError(null)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching stats:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">📊 Statistics</h3>
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-avrt-primary"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">📊 Statistics</h3>
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
          <p className="font-semibold text-red-800">Error loading statistics</p>
          <p className="text-sm text-red-600">{error}</p>
        </div>
        <button
          onClick={fetchStats}
          className="mt-4 btn-primary w-full"
        >
          Retry
        </button>
      </div>
    )
  }

  const statistics = stats?.statistics || {}
  const services = stats?.services || {}

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-gray-800">📊 System Statistics</h3>
        <button
          onClick={fetchStats}
          className="text-sm text-avrt-primary hover:underline font-semibold"
        >
          🔄 Refresh
        </button>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <StatCard
          icon={<Activity className="w-6 h-6" />}
          label="Total Validations"
          value={statistics.totalInteractions || 0}
          color="blue"
        />
        <StatCard
          icon={<Shield className="w-6 h-6" />}
          label="Blocked"
          value={statistics.blockedCount || 0}
          color="red"
        />
        <StatCard
          icon={<CheckCircle className="w-6 h-6" />}
          label="Average SPIEL"
          value={(statistics.averageSpielScore || 0).toFixed(1)}
          color="green"
        />
        <StatCard
          icon={<BarChart className="w-6 h-6" />}
          label="Block Rate"
          value={`${((statistics.blockedRate || 0) * 100).toFixed(1)}%`}
          color="yellow"
        />
      </div>

      {/* THT Compliance */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold text-gray-600">THT™ Compliance Rate</p>
            <p className="text-3xl font-bold text-purple-600">
              {((statistics.thtComplianceRate || 0) * 100).toFixed(1)}%
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">
              {statistics.thtCompliantCount || 0} / {statistics.totalInteractions || 0}
            </p>
            <p className="text-xs text-gray-500">compliant interactions</p>
          </div>
        </div>
      </div>

      {/* Service Status */}
      <div className="space-y-3">
        <p className="font-semibold text-gray-700">Service Status:</p>
        <ServiceStatus
          name="SPIEL™ Framework"
          status={services.spiel?.enabled ? 'active' : 'inactive'}
          version={services.spiel?.version}
        />
        <ServiceStatus
          name="THT™ Protocol"
          status={services.tht?.enabled ? 'active' : 'inactive'}
          version={services.tht?.version}
        />
        <ServiceStatus
          name="Whisper API"
          status={services.whisper?.configured ? 'active' : 'not_configured'}
          info={services.whisper?.model}
        />
        <ServiceStatus
          name="Hash Logging"
          status={services.hashLogging?.enabled ? 'active' : 'inactive'}
          info={services.hashLogging?.originStampReady ? 'OriginStamp Ready' : null}
        />
      </div>

      {/* Data Range */}
      {statistics.oldestEntry && (
        <div className="mt-6 pt-4 border-t-2 text-xs text-gray-500">
          <p>Data range: {new Date(statistics.oldestEntry).toLocaleDateString()} - {new Date(statistics.newestEntry).toLocaleDateString()}</p>
        </div>
      )}
    </div>
  )
}

function StatCard({ icon, label, value, color }) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    red: 'bg-red-50 text-red-600 border-red-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    yellow: 'bg-yellow-50 text-yellow-600 border-yellow-200'
  }

  return (
    <div className={`${colorClasses[color]} border-2 rounded-lg p-4`}>
      <div className="flex items-center gap-2 mb-2">
        {icon}
      </div>
      <p className="text-sm text-gray-600 mb-1">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  )
}

function ServiceStatus({ name, status, version, info }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-500'
      case 'inactive':
        return 'bg-gray-400'
      case 'not_configured':
        return 'bg-yellow-500'
      default:
        return 'bg-gray-400'
    }
  }

  return (
    <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3">
      <div className="flex items-center gap-3">
        <div className={`w-3 h-3 rounded-full ${getStatusColor(status)}`}></div>
        <span className="font-semibold text-gray-800">{name}</span>
      </div>
      <div className="text-right">
        <span className="text-sm text-gray-600">
          {version && `v${version}`}
          {info && !version && info}
        </span>
      </div>
    </div>
  )
}

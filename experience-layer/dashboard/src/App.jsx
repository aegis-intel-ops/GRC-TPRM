import { useState, useEffect } from 'react'
import { AlertCircle, CheckCircle, TrendingUp, Users, Shield, Bell } from 'lucide-react'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import axios from 'axios'
import './App.css'

const COLORS = {
  critical: '#e74c3c',
  high: '#e67e22',
  medium: '#f39c12',
  low: '#27ae60',
  minimal: '#16a085'
}

function App() {
  const [vendors, setVendors] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching vendor data
    // In production, this would call your intelligence layer APIs
    const mockData = [
      {
        id: 'V001',
        name: 'TechCorp Solutions',
        domain: 'techcorp.com',
        riskScore: 85,
        riskLevel: 'minimal',
        lastAssessment: '2026-02-01'
      },
      {
        id: 'V002',
        name: 'DataSecure Inc',
        domain: 'datasecure.io',
        riskScore: 72,
        riskLevel: 'low',
        lastAssessment: '2026-02-03'
      },
      {
        id: 'V003',
        name: 'CloudSystems LLC',
        domain: 'cloudsys.net',
        riskScore: 45,
        riskLevel: 'medium',
        lastAssessment: '2026-02-05'
      },
      {
        id: 'V004',
        name: 'LegacyTech Partners',
        domain: 'legacytech.com',
        riskScore: 28,
        riskLevel: 'high',
        lastAssessment: '2026-02-06'
      },
      {
        id: 'V005',
        name: 'SecureNet Pro',
        domain: 'securenet.io',
        riskScore: 91,
        riskLevel: 'minimal',
        lastAssessment: '2026-02-06'
      }
    ]

    setVendors(mockData)

    // Calculate metrics
    const riskDistribution = mockData.reduce((acc, vendor) => {
      acc[vendor.riskLevel] = (acc[vendor.riskLevel] || 0) + 1
      return acc
    }, {})

    const avgScore = mockData.reduce((sum, v) => sum + v.riskScore, 0) / mockData.length

    setMetrics({
      total: mockData.length,
      average: avgScore.toFixed(1),
      distribution: riskDistribution
    })

    setLoading(false)
  }, [])

  const getRiskBadgeClass = (level) => {
    return `risk-badge risk-${level}`
  }

  const pieData = metrics ? Object.entries(metrics.distribution).map(([key, value]) => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value: value,
    color: COLORS[key]
  })) : []

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1><Shield className="logo-icon" /> GRC-TPRM Platform</h1>
        <div className="header-actions">
          <button className="btn-icon"><Bell size={20} /></button>
          <div className="user-avatar">Admin</div>
        </div>
      </header>

      <div className="metrics-container">
        <div className="metric-card">
          <div className="metric-icon" style={{ background: '#3498db' }}>
            <Users size={24} color="white" />
          </div>
          <div className="metric-content">
            <div className="metric-value">{metrics.total}</div>
            <div className="metric-label">Total Vendors</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: '#27ae60' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="metric-content">
            <div className="metric-value">{metrics.average}</div>
            <div className="metric-label">Average Risk Score</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: '#e67e22' }}>
            <AlertCircle size={24} color="white" />
          </div>
          <div className="metric-content">
            <div className="metric-value">{metrics.distribution.high || 0}</div>
            <div className="metric-label">High Risk Vendors</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: '#16a085' }}>
            <CheckCircle size={24} color="white" />
          </div>
          <div className="metric-content">
            <div className="metric-value">{metrics.distribution.minimal || 0}</div>
            <div className="metric-label">Minimal Risk Vendors</div>
          </div>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-card">
          <h2>Risk Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h2>Vendor Risk Scores</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={vendors}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="riskScore" fill="#3498db" name="Risk Score" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="vendors-table-container">
        <h2>Vendor Overview</h2>
        <table className="vendors-table">
          <thead>
            <tr>
              <th>Vendor ID</th>
              <th>Name</th>
              <th>Domain</th>
              <th>Risk Score</th>
              <th>Risk Level</th>
              <th>Last Assessment</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {vendors.map(vendor => (
              <tr key={vendor.id}>
                <td>{vendor.id}</td>
                <td>{vendor.name}</td>
                <td>{vendor.domain}</td>
                <td><strong>{vendor.riskScore}/100</strong></td>
                <td>
                  <span className={getRiskBadgeClass(vendor.riskLevel)}>
                    {vendor.riskLevel}
                  </span>
                </td>
                <td>{vendor.lastAssessment}</td>
                <td>
                  <button className="btn-action">View Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App

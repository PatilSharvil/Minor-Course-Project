import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { gridAPI } from '../api/apiService';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const GridDashboard = () => {
  const [gridData, setGridData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetchGridData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchGridData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchGridData = async () => {
    try {
      const response = await gridAPI.getLoad();
      setGridData(response.data);
      setLastUpdated(new Date());
      setLoading(false);
      setError(null);
    } catch (err) {
      setError('Failed to fetch grid data. Make sure backend is running.');
      setLoading(false);
      console.error('Grid data fetch error:', err);
    }
  };

  if (loading) {
    return (
      <div className="container py-5">
        <div className="d-flex justify-content-center align-items-center" style={{ height: '60vh' }}>
          <div className="spinner me-3"></div>
          <span>Loading grid data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger" role="alert">
          ⚠️ {error}
        </div>
        <button className="btn btn-primary" onClick={fetchGridData}>
          🔄 Retry
        </button>
      </div>
    );
  }

  // Chart data with ML forecast
  const chartData = {
    labels: gridData.forecast_next_6h.map(h => h.hour),
    datasets: [
      {
        label: 'Grid Load Forecast (%)',
        data: gridData.forecast_next_6h.map(h => h.load),
        borderColor: '#FFB380',
        backgroundColor: 'rgba(255, 179, 128, 0.1)',
        tension: 0.4,
        fill: true,
        pointBackgroundColor: '#FFB380',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { 
          color: '#6B6B6B',
          font: { size: 12 }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        titleColor: '#1A1A1A',
        bodyColor: '#6B6B6B',
        borderColor: '#F0F0F0',
        borderWidth: 1,
        padding: 12,
        displayColors: true,
        callbacks: {
          label: function(context) {
            return `Grid Load: ${context.parsed.y.toFixed(1)}%`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: { 
          color: '#9CA3AF',
          callback: function(value) {
            return value + '%';
          }
        },
        grid: { 
          color: 'rgba(240, 240, 240, 0.5)' 
        }
      },
      x: {
        ticks: { 
          color: '#9CA3AF' 
        },
        grid: { 
          color: 'rgba(240, 240, 240, 0.5)' 
        }
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'high': return '#DC2626';
      case 'medium': return '#D97706';
      case 'low': return '#059669';
      default: return '#6B6B6B';
    }
  };

  const getStatusBackground = (status) => {
    switch (status) {
      case 'high': return 'rgba(220, 38, 38, 0.1)';
      case 'medium': return 'rgba(217, 119, 6, 0.1)';
      case 'low': return 'rgba(5, 150, 105, 0.1)';
      default: return 'rgba(107, 107, 107, 0.1)';
    }
  };

  return (
    <div className="grid-dashboard">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="text-gradient mb-0" style={{ fontSize: '2rem', fontWeight: 700 }}>
          📊 Grid Dashboard
        </h2>
        <button 
          className="btn btn-outline"
          onClick={fetchGridData}
          style={{
            fontSize: '0.875rem',
            fontWeight: 500,
            padding: '8px 16px',
            borderRadius: '8px'
          }}
        >
          🔄 Refresh
        </button>
      </div>

      {lastUpdated && (
        <div style={{ 
          fontSize: '0.8125rem', 
          color: '#9CA3AF', 
          marginBottom: '24px',
          textAlign: 'right'
        }}>
          Last updated: {lastUpdated.toLocaleTimeString()}
        </div>
      )}
      
      <div className="row g-4 mb-4">
        <div className="col-md-4">
          <div className="grid-card">
            <h6 className="mb-3" style={{ fontSize: '0.875rem', color: '#9CA3AF', fontWeight: 500 }}>
              Current Grid Load
            </h6>
            <div className="d-flex align-items-center justify-content-between">
              <span style={{ 
                fontSize: '2.5rem', 
                fontWeight: 700, 
                color: getStatusColor(gridData.status) 
              }}>
                {gridData.current_load_percentage.toFixed(1)}%
              </span>
              <span className="status-indicator" style={{ 
                background: getStatusBackground(gridData.status),
                color: getStatusColor(gridData.status),
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '0.8125rem',
                fontWeight: 600
              }}>
                {gridData.status.toUpperCase()}
              </span>
            </div>
            <div style={{ 
              fontSize: '0.8125rem', 
              color: '#9CA3AF', 
              marginTop: '12px' 
            }}>
              ML Forecast • Updated: {new Date(gridData.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="grid-card">
            <h6 className="mb-3" style={{ fontSize: '0.875rem', color: '#9CA3AF', fontWeight: 500 }}>
              Price Multiplier
            </h6>
            <div className="d-flex align-items-center justify-content-between">
              <span style={{ 
                fontSize: '2.5rem', 
                fontWeight: 700, 
                color: gridData.price_multiplier > 1.2 ? '#D97706' : '#059669' 
              }}>
                {gridData.price_multiplier}x
              </span>
              <span style={{ fontSize: '2rem' }}>⚡</span>
            </div>
            <div style={{ 
              fontSize: '0.8125rem', 
              color: '#9CA3AF', 
              marginTop: '12px' 
            }}>
              Base rate × {gridData.price_multiplier}
              {gridData.price_multiplier > 1.2 && ' (Peak pricing)'}
              {gridData.price_multiplier < 1.0 && ' (Off-peak discount)'}
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="grid-card">
            <h6 className="mb-3" style={{ fontSize: '0.875rem', color: '#9CA3AF', fontWeight: 500 }}>
              Renewable Energy
            </h6>
            <div className="d-flex align-items-center justify-content-between">
              <span style={{ 
                fontSize: '2.5rem', 
                fontWeight: 700, 
                color: '#059669' 
              }}>
                {gridData.renewable_percentage.toFixed(1)}%
              </span>
              <span style={{ fontSize: '2rem' }}>🌱</span>
            </div>
            <div style={{ 
              fontSize: '0.8125rem', 
              color: '#9CA3AF', 
              marginTop: '12px' 
            }}>
              From solar & wind sources
            </div>
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-lg-8">
          <div className="chart-container" style={{ height: '350px' }}>
            <h5 className="mb-4" style={{ fontSize: '1.125rem', fontWeight: 600 }}>
              📈 6-Hour Load Forecast (ML-Powered)
            </h5>
            <Line data={chartData} options={chartOptions} />
          </div>
        </div>

        <div className="col-lg-4">
          <div className="grid-card h-100">
            <h5 className="mb-4" style={{ fontSize: '1.125rem', fontWeight: 600 }}>
              💡 Charging Recommendation
            </h5>
            <div className="text-center py-4">
              {gridData.recommended_charging ? (
                <div>
                  <div style={{ fontSize: '4rem', marginBottom: '16px' }}>✅</div>
                  <h4 className="mb-3" style={{ color: '#059669', fontSize: '1.25rem', fontWeight: 600 }}>
                    Good Time to Charge!
                  </h4>
                  <p className="mb-0" style={{ color: '#6B6B6B', fontSize: '0.9375rem', lineHeight: 1.6 }}>
                    Grid load is relatively low ({gridData.current_load_percentage.toFixed(1)}%). 
                    Charging now is cost-effective and grid-friendly.
                  </p>
                  <div style={{ 
                    marginTop: '20px', 
                    padding: '12px', 
                    background: 'rgba(5, 150, 105, 0.08)',
                    borderRadius: '8px'
                  }}>
                    <div style={{ fontSize: '0.8125rem', color: '#059669', fontWeight: 600 }}>
                      💰 Estimated Savings
                    </div>
                    <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#059669', marginTop: '4px' }}>
                      {(1.5 - gridData.price_multiplier).toFixed(1)}x cheaper
                    </div>
                  </div>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: '4rem', marginBottom: '16px' }}>⏰</div>
                  <h4 className="mb-3" style={{ color: '#D97706', fontSize: '1.25rem', fontWeight: 600 }}>
                    Consider Waiting
                  </h4>
                  <p className="mb-0" style={{ color: '#6B6B6B', fontSize: '0.9375rem', lineHeight: 1.6 }}>
                    Grid load is high ({gridData.current_load_percentage.toFixed(1)}%). 
                    Consider charging during off-peak hours for better rates.
                  </p>
                  <div style={{ 
                    marginTop: '20px', 
                    padding: '12px', 
                    background: 'rgba(217, 119, 6, 0.08)',
                    borderRadius: '8px'
                  }}>
                    <div style={{ fontSize: '0.8125rem', color: '#D97706', fontWeight: 600 }}>
                      📊 Current Load
                    </div>
                    <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#D97706', marginTop: '4px' }}>
                      {gridData.current_load_percentage.toFixed(1)}% (High)
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="row g-4 mt-4">
        <div className="col-12">
          <div className="grid-card">
            <h5 className="mb-4" style={{ fontSize: '1.125rem', fontWeight: 600 }}>
              ℹ️ Understanding Grid Load Levels
            </h5>
            <div className="row g-4">
              <div className="col-md-4">
                <div className="p-4" style={{ 
                  background: 'rgba(5, 150, 105, 0.08)', 
                  borderRadius: '10px',
                  border: '1.5px solid rgba(5, 150, 105, 0.2)'
                }}>
                  <h6 className="mb-3" style={{ color: '#059669', fontSize: '1rem', fontWeight: 600 }}>
                    ✅ Low Load (&lt;50%)
                  </h6>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#6B6B6B', lineHeight: 1.6 }}>
                    Best time to charge. Lower prices, minimal grid stress, and maximum renewable energy availability.
                  </p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="p-4" style={{ 
                  background: 'rgba(217, 119, 6, 0.08)', 
                  borderRadius: '10px',
                  border: '1.5px solid rgba(217, 119, 6, 0.2)'
                }}>
                  <h6 className="mb-3" style={{ color: '#D97706', fontSize: '1rem', fontWeight: 600 }}>
                    ⚠️ Medium Load (50-80%)
                  </h6>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#6B6B6B', lineHeight: 1.6 }}>
                    Moderate charging recommended. Standard pricing applies. Grid is under normal stress.
                  </p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="p-4" style={{ 
                  background: 'rgba(220, 38, 38, 0.08)', 
                  borderRadius: '10px',
                  border: '1.5px solid rgba(220, 38, 38, 0.2)'
                }}>
                  <h6 className="mb-3" style={{ color: '#DC2626', fontSize: '1rem', fontWeight: 600 }}>
                    ❌ High Load (&gt;80%)
                  </h6>
                  <p className="mb-0" style={{ fontSize: '0.875rem', color: '#6B6B6B', lineHeight: 1.6 }}>
                    Avoid charging if possible. Higher prices and significant grid stress. Wait for off-peak hours.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ML Model Status */}
      <div className="row g-4 mt-4">
        <div className="col-12">
          <div style={{ 
            padding: '16px 20px', 
            background: 'rgba(162, 210, 255, 0.08)',
            borderRadius: '10px',
            border: '1.5px solid rgba(162, 210, 255, 0.2)'
          }}>
            <div style={{ fontSize: '0.875rem', color: '#2563EB', fontWeight: 700, marginBottom: '8px' }}>
              🤖 ML Models Active
            </div>
            <div style={{ display: 'flex', gap: '24px', fontSize: '0.8125rem', color: '#6B6B6B' }}>
              <div>• Grid Load Forecaster: Active</div>
              <div>• Forecast Horizon: 6 hours</div>
              <div>• Update Frequency: Real-time</div>
              <div>• Model: Gradient Boosting Regressor</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GridDashboard;

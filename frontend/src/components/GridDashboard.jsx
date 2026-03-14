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

  useEffect(() => {
    fetchGridData();
  }, []);

  const fetchGridData = async () => {
    try {
      const response = await gridAPI.getLoad();
      setGridData(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch grid data');
      setLoading(false);
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="container py-5">
        <div className="d-flex justify-content-center align-items-center" style={{ height: '60vh' }}>
          <div className="spinner"></div>
          <span className="ms-3">Loading grid data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    );
  }

  const chartData = {
    labels: gridData.forecast_next_6h.map(h => h.hour),
    datasets: [
      {
        label: 'Grid Load (%)',
        data: gridData.forecast_next_6h.map(h => h.load),
        borderColor: 'rgb(0, 217, 255)',
        backgroundColor: 'rgba(0, 217, 255, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: 'rgba(255,255,255,0.8)' }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: { color: 'rgba(255,255,255,0.7)' },
        grid: { color: 'rgba(255,255,255,0.1)' }
      },
      x: {
        ticks: { color: 'rgba(255,255,255,0.7)' },
        grid: { color: 'rgba(255,255,255,0.1)' }
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'high': return '#ff4757';
      case 'medium': return '#ffa502';
      case 'low': return '#2ed573';
      default: return '#fff';
    }
  };

  return (
    <div className="container py-5">
      <h2 className="text-gradient mb-4 fade-in">📊 Grid Dashboard</h2>
      
      <div className="row g-4 mb-4">
        <div className="col-md-4">
          <div className="glass-card p-4 fade-in">
            <h6 className="text-muted mb-2">Current Grid Load</h6>
            <div className="d-flex align-items-center justify-content-between">
              <span style={{ fontSize: '2.5rem', fontWeight: 700, color: getStatusColor(gridData.status) }}>
                {gridData.current_load_percentage}%
              </span>
              <span className="badge" style={{ 
                background: getStatusColor(gridData.status),
                color: '#000',
                padding: '8px 16px',
                fontSize: '0.9rem'
              }}>
                {gridData.status.toUpperCase()}
              </span>
            </div>
            <small className="text-muted">Updated: {new Date(gridData.timestamp).toLocaleTimeString()}</small>
          </div>
        </div>

        <div className="col-md-4">
          <div className="glass-card p-4 fade-in">
            <h6 className="text-muted mb-2">Price Multiplier</h6>
            <div className="d-flex align-items-center justify-content-between">
              <span style={{ fontSize: '2.5rem', fontWeight: 700, color: '#ffd700' }}>
                {gridData.price_multiplier}x
              </span>
              <span className="text-warning">⚡</span>
            </div>
            <small className="text-muted">Base rate × {gridData.price_multiplier}</small>
          </div>
        </div>

        <div className="col-md-4">
          <div className="glass-card p-4 fade-in">
            <h6 className="text-muted mb-2">Renewable Energy</h6>
            <div className="d-flex align-items-center justify-content-between">
              <span style={{ fontSize: '2.5rem', fontWeight: 700, color: '#00ff88' }}>
                {gridData.renewable_percentage}%
              </span>
              <span className="text-success">🌱</span>
            </div>
            <small className="text-muted">From solar & wind</small>
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-lg-8">
          <div className="glass-card p-4 fade-in">
            <h5 className="mb-4">📈 6-Hour Load Forecast</h5>
            <Line data={chartData} options={chartOptions} />
          </div>
        </div>

        <div className="col-lg-4">
          <div className="glass-card p-4 fade-in">
            <h5 className="mb-4">💡 Charging Recommendation</h5>
            <div className="text-center py-4">
              {gridData.recommended_charging ? (
                <div>
                  <div style={{ fontSize: '4rem' }}>✅</div>
                  <h4 className="text-success">Good Time to Charge!</h4>
                  <p className="text-muted">
                    Grid load is relatively low. Charging now is cost-effective.
                  </p>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: '4rem' }}>⏰</div>
                  <h4 className="text-warning">Consider Waiting</h4>
                  <p className="text-muted">
                    Grid load is high. Consider charging during off-peak hours.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="row g-4 mt-4">
        <div className="col-12">
          <div className="glass-card p-4 fade-in">
            <h5 className="mb-3">ℹ️ About Grid Load</h5>
            <div className="row g-4">
              <div className="col-md-4">
                <div className="p-3" style={{ background: 'rgba(46, 213, 115, 0.1)', borderRadius: '8px' }}>
                  <h6 className="text-success">Low Load (&lt;50%)</h6>
                  <p className="text-muted mb-0" style={{ fontSize: '0.85rem' }}>
                    Best time to charge. Lower prices and minimal grid stress.
                  </p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="p-3" style={{ background: 'rgba(255, 165, 2, 0.1)', borderRadius: '8px' }}>
                  <h6 className="text-warning">Medium Load (50-80%)</h6>
                  <p className="text-muted mb-0" style={{ fontSize: '0.85rem' }}>
                    Moderate charging recommended. Standard pricing applies.
                  </p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="p-3" style={{ background: 'rgba(255, 71, 87, 0.1)', borderRadius: '8px' }}>
                  <h6 className="text-danger">High Load (&gt;80%)</h6>
                  <p className="text-muted mb-0" style={{ fontSize: '0.85rem' }}>
                    Avoid charging if possible. Higher prices and grid stress.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GridDashboard;

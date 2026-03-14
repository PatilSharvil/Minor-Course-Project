import React, { useState } from 'react';
import { predictAPI } from '../api/apiService';

const RangePredictor = () => {
  const [formData, setFormData] = useState({
    battery_level: 80,
    battery_capacity: 60,
    vehicle_model: 'Tesla Model 3',
    driving_conditions: 'normal'
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await predictAPI.range(formData);
      setPrediction(response.data);
    } catch (err) {
      setError('Failed to get prediction. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <div className="glass-card p-4 fade-in">
            <h2 className="text-gradient mb-4">🔋 Range Predictor</h2>
            
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Vehicle Model</label>
                <select
                  name="vehicle_model"
                  className="form-select"
                  value={formData.vehicle_model}
                  onChange={handleChange}
                  style={{ 
                    background: 'rgba(255,255,255,0.05)', 
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: '#fff'
                  }}
                >
                  <option value="Tesla Model 3">Tesla Model 3</option>
                  <option value="Tesla Model Y">Tesla Model Y</option>
                  <option value="Nissan Leaf">Nissan Leaf</option>
                  <option value="Chevrolet Bolt">Chevrolet Bolt</option>
                  <option value="Hyundai Kona">Hyundai Kona Electric</option>
                  <option value="Tata Nexon EV">Tata Nexon EV</option>
                  <option value="MG ZS EV">MG ZS EV</option>
                </select>
              </div>

              <div className="mb-3">
                <label className="form-label">
                  Battery Level: {formData.battery_level}%
                </label>
                <input
                  type="range"
                  className="form-range"
                  name="battery_level"
                  min="0"
                  max="100"
                  value={formData.battery_level}
                  onChange={handleChange}
                />
              </div>

              <div className="mb-3">
                <label className="form-label">Battery Capacity (kWh)</label>
                <input
                  type="number"
                  className="form-control"
                  name="battery_capacity"
                  value={formData.battery_capacity}
                  onChange={handleChange}
                  step="0.1"
                  style={{ 
                    background: 'rgba(255,255,255,0.05)', 
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: '#fff'
                  }}
                />
              </div>

              <div className="mb-4">
                <label className="form-label">Driving Conditions</label>
                <select
                  name="driving_conditions"
                  className="form-select"
                  value={formData.driving_conditions}
                  onChange={handleChange}
                  style={{ 
                    background: 'rgba(255,255,255,0.05)', 
                    border: '1px solid rgba(255,255,255,0.2)',
                    color: '#fff'
                  }}
                >
                  <option value="normal">Normal</option>
                  <option value="highway">Highway</option>
                  <option value="city">City</option>
                </select>
              </div>

              <button
                type="submit"
                className="btn btn-primary-custom w-100"
                disabled={loading}
              >
                {loading ? 'Calculating...' : 'Predict Range'}
              </button>
            </form>

            {error && (
              <div className="alert alert-danger mt-3" role="alert">
                {error}
              </div>
            )}

            {prediction && (
              <div className="prediction-result mt-4 p-3" style={{
                background: 'rgba(0, 255, 136, 0.1)',
                border: '1px solid rgba(0, 255, 136, 0.3)',
                borderRadius: '12px'
              }}>
                <h4 className="text-success mb-3">📊 Prediction Result</h4>
                <div className="row g-3">
                  <div className="col-6">
                    <div className="text-muted" style={{ fontSize: '0.85rem' }}>Predicted Range</div>
                    <div className="text-gradient" style={{ fontSize: '1.8rem', fontWeight: 700 }}>
                      {prediction.predicted_range_km} km
                    </div>
                  </div>
                  <div className="col-6">
                    <div className="text-muted" style={{ fontSize: '0.85rem' }}>Efficiency</div>
                    <div className="text-info" style={{ fontSize: '1.5rem', fontWeight: 600 }}>
                      {prediction.efficiency_km_per_kwh} km/kWh
                    </div>
                  </div>
                </div>
                <div className="mt-3 pt-3" style={{ borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                  <small className="text-muted">
                    Based on {formData.battery_level}% battery ({formData.battery_capacity} kWh capacity) 
                    in {formData.driving_conditions} driving conditions
                  </small>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RangePredictor;

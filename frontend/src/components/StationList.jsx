import React from 'react';

const StationList = ({ stations, loading }) => {
  if (loading) {
    return (
      <div className="station-panel glass-card">
        <div className="loading-panel">
          <div className="spinner"></div>
          <span className="ms-3">Loading stations...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="station-panel glass-card">
      <h3>⚡ Charging Stations</h3>
      <p className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '16px' }}>
        Found {stations.length} stations nearby
      </p>
      
      {stations.map((station) => (
        <div key={station.id} className="station-item">
          <h5>{station.name}</h5>
          <div className="distance">📍 {station.distance_km?.toFixed(1) || '0'} km away</div>
          <div className="chargers">
            🔌 {station.available_chargers}/{station.total_chargers} chargers available
          </div>
          <div className="price">
            💰 ₹{station.price_per_kwh}/kWh
          </div>
          <div className="amenities">
            {station.amenities.map((amenity, index) => (
              <span key={index} className="amenity-tag">
                {amenity}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default StationList;

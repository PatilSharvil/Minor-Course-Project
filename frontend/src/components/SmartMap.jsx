import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icon issue in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// Custom icon for charging stations - Pastel Orange
const chargingStationIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/32/739/739321.png',
  iconRetinaUrl: 'https://cdn-icons-png.flaticon.com/32/739/739321.png',
  iconSize: [28, 28],
  iconAnchor: [14, 28],
  popupAnchor: [0, -28],
  className: 'custom-marker'
});

// Custom icon for user location - Pastel Blue
const userLocationIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/32/684/684560.png',
  iconRetinaUrl: 'https://cdn-icons-png.flaticon.com/32/684/684560.png',
  iconSize: [24, 24],
  iconAnchor: [12, 12],
  popupAnchor: [0, -12],
});

// Component to handle map clicks
function LocationPicker({ onLocationSelect }) {
  useMapEvents({
    click(e) {
      onLocationSelect({
        lat: e.latlng.lat,
        lng: e.latlng.lng
      });
    },
  });
  return null;
}

// Component to draw route line
function RouteLine({ start, end }) {
  const map = useMapEvents({});
  
  if (!start || !end) return null;
  
  const polyline = L.polyline([
    [start.lat, start.lng],
    [end.lat, end.lng]
  ], {
    color: '#00d9ff',
    weight: 4,
    opacity: 0.7,
    dashArray: '10, 10',
  }).addTo(map);
  
  return null;
}

const SmartMap = ({ 
  stations, 
  userLocation, 
  onLocationSelect,
  selectedStation,
  onStationSelect 
}) => {
  const [clickedLocation, setClickedLocation] = useState(null);
  
  // Default to Mumbai if no location provided
  const defaultCenter = userLocation || { lat: 19.0760, lng: 72.8777 };
  const zoom = 12;

  const handleMapClick = (location) => {
    setClickedLocation(location);
    onLocationSelect(location);
  };

  const handleStationClick = (station) => {
    onStationSelect(station);
  };

  return (
    <div className="smart-map-container" style={{ width: '100%', height: '100%', minHeight: '500px' }}>
      <MapContainer 
        center={[defaultCenter.lat, defaultCenter.lng]} 
        zoom={zoom} 
        style={{ width: '100%', height: '100%' }}
        scrollWheelZoom={true}
        className="leaflet-map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Click handler */}
        <LocationPicker onLocationSelect={handleMapClick} />
        
        {/* User location marker */}
        {userLocation && (
          <Marker 
            position={[userLocation.lat, userLocation.lng]}
            icon={userLocationIcon}
          >
            <Popup>
              <strong>Your Location</strong><br />
              Click anywhere to change
            </Popup>
          </Marker>
        )}
        
        {/* Clicked location marker */}
        {clickedLocation && (
          <Marker 
            position={[clickedLocation.lat, clickedLocation.lng]}
            icon={new L.Icon.Default()}
          >
            <Popup>
              <strong>Selected Location</strong><br />
              Lat: {clickedLocation.lat.toFixed(4)}<br />
              Lng: {clickedLocation.lng.toFixed(4)}
            </Popup>
          </Marker>
        )}
        
        {/* Charging station markers */}
        {stations.map((station) => (
          <Marker
            key={station.id}
            position={[station.latitude, station.longitude]}
            icon={chargingStationIcon}
            eventHandlers={{
              click: () => handleStationClick(station)
            }}
          >
            <Popup>
              <div style={{ 
                minWidth: '260px',
                padding: '12px',
                fontFamily: 'Inter, sans-serif'
              }}>
                <h4 style={{ 
                  margin: '0 0 10px 0', 
                  color: 'var(--text-primary)',
                  fontSize: '1rem',
                  fontWeight: 600
                }}>
                  {station.name}
                </h4>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                  <div style={{ marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span>🔌</span>
                    <strong style={{ color: 'var(--text-primary)' }}>{station.available_chargers}/{station.total_chargers}</strong> available
                  </div>
                  <div style={{ marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span>⚡</span>
                    {Array.isArray(station.power_kw) ? Math.max(...station.power_kw) : station.power_kw} kW
                  </div>
                  <div style={{ marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span>💰</span>
                    <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>₹{station.price_per_kwh}/kWh</span>
                  </div>
                  {station.distance_km && (
                    <div style={{ 
                      marginTop: '10px', 
                      padding: '8px', 
                      background: 'rgba(162, 210, 255, 0.1)',
                      borderRadius: '6px',
                      fontWeight: 600,
                      fontSize: '0.8125rem',
                      color: '#2563EB'
                    }}>
                      📍 {station.distance_km.toFixed(1)} km away
                    </div>
                  )}
                  <div style={{ marginTop: '10px' }}>
                    <button 
                      onClick={() => onStationSelect(station)}
                      style={{
                        background: 'var(--accent-primary)',
                        border: 'none',
                        color: 'var(--text-primary)',
                        padding: '8px 16px',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontWeight: 600,
                        fontSize: '0.8125rem',
                        width: '100%',
                        transition: 'all 0.3s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.target.style.background = 'var(--accent-hover)';
                        e.target.style.transform = 'translateY(-2px)';
                      }}
                      onMouseLeave={(e) => {
                        e.target.style.background = 'var(--accent-primary)';
                        e.target.style.transform = 'translateY(0)';
                      }}
                    >
                      View Details
                    </button>
                  </div>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
        
        {/* Route line from user location to selected station */}
        {userLocation && selectedStation && (
          <RouteLine start={userLocation} end={{ lat: selectedStation.latitude, lng: selectedStation.longitude }} />
        )}
      </MapContainer>
      
      {/* Map info overlay */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        padding: '14px 18px',
        borderRadius: '10px',
        border: '1px solid var(--border-light)',
        boxShadow: 'var(--shadow-lg)',
        zIndex: 1000,
        fontSize: '0.8125rem',
        minWidth: '180px'
      }}>
        <div style={{ 
          color: 'var(--accent-primary)', 
          fontWeight: 700, 
          marginBottom: '6px',
          fontSize: '0.875rem'
        }}>
          🗺️ Interactive Map
        </div>
        <div style={{ color: 'var(--text-secondary)', lineHeight: 1.5 }}>
          Click anywhere to select location
        </div>
      </div>
    </div>
  );
};

export default SmartMap;

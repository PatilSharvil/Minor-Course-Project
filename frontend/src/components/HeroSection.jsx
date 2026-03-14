import React from 'react';

const HeroSection = ({ show }) => {
  if (!show) return null;

  return (
    <div 
      className="hero-section fade-in"
      style={{
        position: 'absolute',
        bottom: '40px',
        left: '40px',
        zIndex: 100,
        maxWidth: '400px'
      }}
    >
      <div className="glass-card" style={{ padding: '24px' }}>
        <h2 className="text-gradient" style={{ fontSize: '1.5rem', marginBottom: '12px' }}>
          Welcome to EV Charging Scheduler
        </h2>
        <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.9rem', lineHeight: 1.6 }}>
          Explore charging stations in 3D, predict your vehicle's range, and optimize charging schedules 
          based on grid load and energy prices.
        </p>
        <div className="mt-3" style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <span className="badge" style={{ 
            background: 'rgba(0, 217, 255, 0.15)', 
            color: '#00d9ff', 
            border: '1px solid rgba(0, 217, 255, 0.3)',
            padding: '6px 12px',
            borderRadius: '20px',
            fontSize: '0.8rem'
          }}>
             AI-Powered
          </span>
          <span className="badge" style={{ 
            background: 'rgba(0, 255, 136, 0.15)', 
            color: '#00ff88', 
            border: '1px solid rgba(0, 255, 136, 0.3)',
            padding: '6px 12px',
            borderRadius: '20px',
            fontSize: '0.8rem'
          }}>
            🌱 Sustainable
          </span>
          <span className="badge" style={{ 
            background: 'rgba(255, 215, 0, 0.15)', 
            color: '#ffd700', 
            border: '1px solid rgba(255, 215, 0, 0.3)',
            padding: '6px 12px',
            borderRadius: '20px',
            fontSize: '0.8rem'
          }}>
            ⚡ Real-time
          </span>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;

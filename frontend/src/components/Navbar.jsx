import React from 'react';

const Navbar = ({ activeView, setActiveView }) => {
  return (
    <nav className="navbar navbar-expand-lg glass-panel" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      margin: '10px 20px',
      borderRadius: '12px',
      padding: '12px 24px'
    }}>
      <div className="container-fluid">
        <a className="navbar-brand text-gradient" href="#" style={{ fontWeight: 700, fontSize: '1.3rem' }}>
          ⚡ EV Scheduler
        </a>
        
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
          style={{ borderColor: 'rgba(255,255,255,0.2)' }}
        >
          <span className="navbar-toggler-icon" style={{ filter: 'invert(1)' }}></span>
        </button>
        
        <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul className="navbar-nav gap-3">
            <li className="nav-item">
              <button
                className={`nav-link ${activeView === 'map' ? 'active' : ''}`}
                onClick={() => setActiveView('map')}
                style={{ 
                  background: activeView === 'map' ? 'rgba(0, 217, 255, 0.2)' : 'transparent',
                  border: '1px solid rgba(0, 217, 255, 0.3)',
                  color: activeView === 'map' ? '#00d9ff' : 'rgba(255,255,255,0.8)',
                  borderRadius: '8px',
                  padding: '8px 16px',
                  transition: 'all 0.3s'
                }}
              >
                🗺️ 3D Map
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeView === 'range' ? 'active' : ''}`}
                onClick={() => setActiveView('range')}
                style={{ 
                  background: activeView === 'range' ? 'rgba(0, 217, 255, 0.2)' : 'transparent',
                  border: '1px solid rgba(0, 217, 255, 0.3)',
                  color: activeView === 'range' ? '#00d9ff' : 'rgba(255,255,255,0.8)',
                  borderRadius: '8px',
                  padding: '8px 16px',
                  transition: 'all 0.3s'
                }}
              >
                🔋 Range Predictor
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeView === 'grid' ? 'active' : ''}`}
                onClick={() => setActiveView('grid')}
                style={{ 
                  background: activeView === 'grid' ? 'rgba(0, 217, 255, 0.2)' : 'transparent',
                  border: '1px solid rgba(0, 217, 255, 0.3)',
                  color: activeView === 'grid' ? '#00d9ff' : 'rgba(255,255,255,0.8)',
                  borderRadius: '8px',
                  padding: '8px 16px',
                  transition: 'all 0.3s'
                }}
              >
                📊 Grid Dashboard
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

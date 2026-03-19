import React from 'react';

const Navbar = ({ activeView, setActiveView }) => {
  return (
    <nav className="navbar navbar-expand-lg">
      <div className="container-fluid">
        <a className="navbar-brand text-gradient" href="#" style={{ 
          fontWeight: 700, 
          fontSize: '1.375rem',
          letterSpacing: '-0.5px'
        }}>
          ⚡ EV Scheduler
        </a>
        
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
          style={{ 
            borderColor: '#F0F0F0',
            background: 'transparent'
          }}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        
        <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul className="navbar-nav gap-2">
            <li className="nav-item">
              <button
                className={`nav-link ${activeView === 'map' || activeView === 'recommendations' ? 'active' : ''}`}
                onClick={() => setActiveView('map')}
                style={{ 
                  background: (activeView === 'map' || activeView === 'recommendations') 
                    ? '#FFB380' 
                    : 'transparent',
                  color: '#1A1A1A',
                  border: 'none',
                  cursor: 'pointer'
                }}
              >
                🗺️ Smart Map
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeView === 'grid' ? 'active' : ''}`}
                onClick={() => setActiveView('grid')}
                style={{ 
                  background: activeView === 'grid' 
                    ? '#FFB380' 
                    : 'transparent',
                  color: '#1A1A1A',
                  border: 'none',
                  cursor: 'pointer'
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

import { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Sky, Stars } from '@react-three/drei';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import Map3DScene from './scenes/Map3DScene';
import StationList from './components/StationList';
import RangePredictor from './components/RangePredictor';
import GridDashboard from './components/GridDashboard';
import './App.css';

// API base URL from environment or default
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api';

function App() {
  const [activeView, setActiveView] = useState('map');
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch stations on mount
    fetchStations();
  }, []);

  const fetchStations = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stations`);
      const data = await response.json();
      setStations(data.stations);
      setLoading(false);
      setError(null);
    } catch (error) {
      console.error('Error fetching stations:', error);
      setLoading(false);
      setError('Failed to connect to backend. Make sure the server is running on port 8001.');
    }
  };

  return (
    <div className="app-container">
      <Navbar activeView={activeView} setActiveView={setActiveView} />

      <main className="main-content">
        {error && (
          <div className="alert alert-danger m-3" role="alert" style={{ maxWidth: '600px' }}>
            ⚠️ {error}
            <br />
            <small>To start the backend: <code>cd backend &amp;&amp; python run_server.py</code></small>
          </div>
        )}

        {activeView === 'map' && (
          <div className="map-view">
            <div className="canvas-container">
              <Canvas camera={{ position: [0, 100, 200], fov: 60 }}>
                <Sky sunPosition={[100, 20, 100]} />
                <Stars radius={300} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
                <ambientLight intensity={0.5} />
                <directionalLight position={[100, 100, 50]} intensity={1} castShadow />
                <Map3DScene stations={stations} />
                <OrbitControls 
                  enablePan={true} 
                  enableZoom={true} 
                  enableRotate={true}
                  minDistance={50}
                  maxDistance={500}
                />
              </Canvas>
            </div>
            <StationList stations={stations} loading={loading} />
          </div>
        )}

        {activeView === 'range' && <RangePredictor />}
        {activeView === 'grid' && <GridDashboard />}
      </main>

      <HeroSection show={activeView === 'map'} />
    </div>
  );
}

export default App;

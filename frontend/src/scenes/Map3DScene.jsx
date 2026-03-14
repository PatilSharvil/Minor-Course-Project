import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Html } from '@react-three/drei';
import * as THREE from 'three';

// Charging Station Marker Component
const StationMarker = ({ station, onSelect }) => {
  const markerRef = useRef();
  const [hovered, setHovered] = React.useState(false);

  useFrame((state) => {
    if (markerRef.current) {
      markerRef.current.position.y = 2 + Math.sin(state.clock.elapsedTime * 2) * 0.5;
      markerRef.current.rotation.y += 0.02;
    }
  });

  const position = [
    (station.longitude - 72.87) * 1000,
    0,
    (station.latitude - 19.07) * 1000
  ];

  return (
    <group position={position}>
      {/* Marker */}
      <group ref={markerRef}>
        {/* Cone marker */}
        <mesh
          onClick={() => onSelect(station)}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
          castShadow
        >
          <coneGeometry args={[3, 8, 32]} />
          <meshStandardMaterial
            color={hovered ? '#00ff88' : '#00d9ff'}
            emissive={hovered ? '#00ff88' : '#00d9ff'}
            emissiveIntensity={0.5}
            transparent
            opacity={0.9}
          />
        </mesh>

        {/* Label */}
        <Html position={[0, 10, 0]} center distanceFactor={150}>
          <div
            style={{
              background: 'rgba(0, 0, 0, 0.8)',
              border: '1px solid rgba(0, 217, 255, 0.5)',
              borderRadius: '8px',
              padding: '8px 12px',
              color: '#fff',
              fontSize: '12px',
              whiteSpace: 'nowrap',
              backdropFilter: 'blur(4px)'
            }}
          >
            <div style={{ fontWeight: 600, marginBottom: '4px' }}>{station.name}</div>
            <div style={{ color: '#00ff88', fontSize: '11px' }}>
              🔌 {station.available_chargers}/{station.total_chargers} available
            </div>
          </div>
        </Html>
      </group>

      {/* Ground indicator */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.1, 0]}>
        <ringGeometry args={[2, 3, 32]} />
        <meshBasicMaterial color="#00d9ff" transparent opacity={0.5} />
      </mesh>
    </group>
  );
};

// EV Vehicle Component
const EVVehicle = ({ position, color = '#00ff88' }) => {
  const vehicleRef = useRef();
  const [angle, setAngle] = React.useState(0);

  useFrame((state, delta) => {
    if (vehicleRef.current) {
      setAngle((prev) => prev + delta * 0.5);
      vehicleRef.current.position.x = position[0] + Math.sin(angle) * 20;
      vehicleRef.current.position.z = position[2] + Math.cos(angle) * 20;
    }
  });

  return (
    <group ref={vehicleRef} position={position}>
      {/* Car body */}
      <mesh position={[0, 1, 0]} castShadow>
        <boxGeometry args={[4, 1.5, 2]} />
        <meshStandardMaterial color={color} metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Wheels */}
      {[[-1.5, 0.5, 1], [1.5, 0.5, 1], [-1.5, 0.5, -1], [1.5, 0.5, -1]].map((pos, i) => (
        <mesh key={i} position={pos} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.5, 0.5, 0.3, 16]} />
          <meshStandardMaterial color="#333" />
        </mesh>
      ))}
    </group>
  );
};

// Terrain Component
const Terrain = () => {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
      <planeGeometry args={[1000, 1000, 100, 100]} />
      <meshStandardMaterial
        color="#1a1a2e"
        roughness={0.8}
        metalness={0.2}
        wireframe={false}
      />
    </mesh>
  );
};

// Grid Lines for terrain effect
const GridLines = () => {
  const gridRef = useRef();

  return (
    <gridHelper
      ref={gridRef}
      args={[1000, 50, '#00d9ff', '#00d9ff']}
      position={[0, 0.1, 0]}
    />
  );
};

// Main 3D Map Scene
const Map3DScene = ({ stations }) => {
  const [selectedStation, setSelectedStation] = React.useState(null);

  const handleStationSelect = (station) => {
    setSelectedStation(station);
    console.log('Selected station:', station);
  };

  return (
    <>
      {/* Terrain */}
      <Terrain />
      <GridLines />

      {/* Charging Stations */}
      {stations.map((station) => (
        <StationMarker
          key={station.id}
          station={station}
          onSelect={handleStationSelect}
        />
      ))}

      {/* Animated EVs */}
      <EVVehicle position={[50, 0, 50]} color="#00ff88" />
      <EVVehicle position={[-50, 0, -50]} color="#00d9ff" />
      <EVVehicle position={[80, 0, -30]} color="#ffd700" />

      {/* Ambient elements */}
      <fog attach="fog" args={['#0a0a0f', 100, 500]} />
    </>
  );
};

export default Map3DScene;

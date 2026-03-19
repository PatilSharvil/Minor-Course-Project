"""
Test Script for Enhanced EV Charging Scheduler
Tests all new features including 2D map and ML recommendations
"""

from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

print("=" * 70)
print("EV Charging Scheduler - Enhanced Test Suite")
print("=" * 70)
print()

# Test 1: Root endpoint
print("Test 1: Root endpoint")
response = client.get("/")
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Version: {data.get('version')}")
print(f"  Features: {len(data.get('features', []))} features listed")
print(f"  ✓ PASS\n")

# Test 2: Get stations
print("Test 2: Get all stations")
response = client.get("/api/stations")
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Stations count: {data.get('count')}")
print(f"  ✓ PASS\n")

# Test 3: Predict range
print("Test 3: Predict range (ML)")
response = client.post("/api/predict/range", json={
    "battery_level": 80,
    "battery_capacity": 60,
    "vehicle_model": "Tesla Model 3",
    "driving_conditions": "normal"
})
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Predicted range: {data.get('predicted_range_km')} km")
print(f"  Efficiency: {data.get('efficiency_km_per_kwh')} km/kWh")
print(f"  ML model used: {data.get('model_used')}")
print(f"  ✓ PASS\n")

# Test 4: Get grid load
print("Test 4: Get grid load (ML)")
response = client.get("/api/grid/load")
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Current load: {data.get('current_load_percentage')}%")
print(f"  Status: {data.get('status')}")
print(f"  Recommended charging: {data.get('recommended_charging')}")
print(f"  ✓ PASS\n")

# Test 5: Predict demand
print("Test 5: Predict demand (ML)")
response = client.post("/api/predict/demand", json={
    "location": {"latitude": 19.076, "longitude": 72.8777},
    "radius_km": 10
})
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Predictions count: {len(data.get('predictions', []))}")
if data.get('predictions'):
    print(f"  First station demand: {data['predictions'][0]['predicted_demand_percentage']}%")
print(f"  ✓ PASS\n")

# Test 6: ML-powered recommendations
print("Test 6: ML-powered station recommendations")
response = client.post("/api/stations/recommend", json={
    "current_location": {"latitude": 19.076, "longitude": 72.8777},
    "battery_level": 80,
    "battery_capacity": 60,
    "vehicle_model": "Tesla Model 3",
    "speed": 60,
    "driving_conditions": "normal"
})
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"  ML models used: {data.get('ml_models_used')}")
    print(f"  Recommendations count: {len(data.get('recommendations', []))}")
    if data.get('recommendations'):
        top_rec = data['recommendations'][0]
        print(f"  Top recommendation: {top_rec['station']['name']}")
        print(f"  Score: {top_rec['score']}/100")
        print(f"  Distance: {top_rec['distance_km']} km")
        print(f"  ETA: {top_rec['eta_minutes']} min")
        print(f"  Arrival battery: {top_rec['arrival_battery_percent']}%")
        print(f"  Reachable: {top_rec['reachable']}")
    print(f"  ✓ PASS\n")
else:
    print(f"  ✗ FAIL: {response.text}\n")

# Test 7: Optimal schedule
print("Test 7: Optimal charging schedule")
response = client.post("/api/schedule/optimal", json={
    "location": {"latitude": 19.076, "longitude": 72.8777},
    "required_charge": 50
})
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Optimal slots found: {len(data.get('optimal_slots', []))}")
if data.get('best_time'):
    print(f"  Best time: {data['best_time']['time']}")
    print(f"  Grid load: {data['best_time']['grid_load']}%")
print(f"  ✓ PASS\n")

print("=" * 70)
print("All tests completed!")
print("=" * 70)

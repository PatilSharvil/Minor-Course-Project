"""
Backend API Test - All tests in one file
Runs server and tests in sequence
"""

import sys
import time
import threading
import json
from datetime import datetime
from http.server import HTTPServer
import socket

# Change to backend directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("EV Charging Scheduler - Backend API Test")
print("=" * 70)
print()

# Test imports first
print("Step 1: Testing imports...")
try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from main import app
    print("  ✓ All imports successful")
except Exception as e:
    print(f"  ✗ Import error: {e}")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Create test client
print("\nStep 2: Creating test client...")
client = TestClient(app)
print("  ✓ Test client created")

# Run tests
print("\nStep 3: Running API tests...")
print("-" * 70)

tests_passed = 0
tests_failed = 0

def test_endpoint(method, path, description, expected_status=200, json_data=None):
    global tests_passed, tests_failed
    
    print(f"\n{description}")
    print(f"  {method} {path}")
    
    try:
        if method == "GET":
            response = client.get(path)
        elif method == "POST":
            response = client.post(path, json=json_data)
        
        if response.status_code == expected_status:
            print(f"  ✓ Status: {response.status_code}")
            try:
                data = response.json()
                # Show brief response
                data_preview = json.dumps(data, indent=2)[:300].replace('\n', '\n  ')
                print(f"  Response preview:\n  {data_preview}...")
            except:
                pass
            tests_passed += 1
            return True
        else:
            print(f"  ✗ Status: {response.status_code} (Expected: {expected_status})")
            tests_failed += 1
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        tests_failed += 1
        return False

# Run all tests
test_endpoint("GET", "/", "Test 1: Root endpoint", expected_status=200)
test_endpoint("GET", "/health", "Test 2: Health check", expected_status=200)
test_endpoint("GET", "/api/stations", "Test 3: Get all stations", expected_status=200)
test_endpoint("GET", "/api/stations/nearby?latitude=19.076&longitude=72.8777&radius_km=10", 
              "Test 4: Get nearby stations", expected_status=200)
test_endpoint("GET", "/api/grid/load", "Test 5: Get grid load", expected_status=200)

# Range prediction
test_endpoint("POST", "/api/predict/range", "Test 6: Predict range", expected_status=200,
              json_data={
                  "battery_level": 80,
                  "battery_capacity": 60,
                  "vehicle_model": "Tesla Model 3",
                  "driving_conditions": "normal"
              })

# Demand prediction
test_endpoint("POST", "/api/predict/demand", "Test 7: Predict demand", expected_status=200,
              json_data={
                  "location": {"latitude": 19.076, "longitude": 72.8777},
                  "radius_km": 10
              })

# Optimal schedule
test_endpoint("POST", "/api/schedule/optimal", "Test 8: Optimal schedule", expected_status=200,
              json_data={
                  "location": {"latitude": 19.076, "longitude": 72.8777},
                  "required_charge": 50
              })

# Print summary
print("\n" + "=" * 70)
print("Test Summary")
print("=" * 70)
print(f"Total Tests:  {tests_passed + tests_failed}")
print(f"Passed:       {tests_passed}")
print(f"Failed:       {tests_failed}")

if tests_failed == 0:
    print("\n✓ All tests passed!")
else:
    print(f"\n✗ {tests_failed} test(s) failed")

print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Keep window open
print("\nPress Enter to exit...")
input()

"""
Backend API Test Script
Tests all API endpoints and shows detailed errors
"""

import sys
import time
import threading
import requests
import json
from datetime import datetime

# Color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_RESULTS = {"passed": 0, "failed": 0, "total": 0}

def test_endpoint(method, endpoint, description, expected_status=200, json_data=None, params=None):
    """Test a single API endpoint"""
    TEST_RESULTS["total"] += 1
    
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{Colors.BOLD}Test {TEST_RESULTS['total']}: {description}{Colors.ENDC}")
    print(f"  {Colors.OKCYAN}{method.upper()} {url}{Colors.ENDC}")
    
    if json_data:
        print(f"  Body: {json.dumps(json_data, indent=2)}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=10)
        else:
            print_error(f"Unsupported method: {method}")
            TEST_RESULTS["failed"] += 1
            return False
        
        print(f"  Status: {response.status_code} (Expected: {expected_status})")
        print(f"  Time: {response.elapsed.total_seconds():.3f}s")
        
        if response.status_code == expected_status:
            print_success(f"Status code matches: {response.status_code}")
            
            # Try to parse JSON
            try:
                data = response.json()
                print(f"  Response preview: {json.dumps(data, indent=2)[:500]}...")
                TEST_RESULTS["passed"] += 1
                return True
            except json.JSONDecodeError:
                print_warning(f"Response is not JSON: {response.text[:200]}")
                TEST_RESULTS["passed"] += 1
                return True
        else:
            print_error(f"Status code mismatch! Expected {expected_status}, got {response.status_code}")
            print(f"  Response: {response.text[:500]}")
            TEST_RESULTS["failed"] += 1
            return False
            
    except requests.exceptions.ConnectionError as e:
        print_error(f"Connection failed: {str(e)}")
        print_warning("Make sure the backend server is running!")
        TEST_RESULTS["failed"] += 1
        return False
    except requests.exceptions.Timeout:
        print_error("Request timed out (10 seconds)")
        TEST_RESULTS["failed"] += 1
        return False
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        TEST_RESULTS["failed"] += 1
        return False

def run_all_tests():
    """Run all API tests"""
    print_header("EV Charging Scheduler - API Test Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    
    # Test 1: Health Check
    test_endpoint("GET", "/", "Root endpoint", expected_status=200)
    test_endpoint("GET", "/health", "Health check endpoint", expected_status=200)
    
    # Test 2: Station Endpoints
    test_endpoint("GET", "/api/stations", "Get all charging stations", expected_status=200)
    test_endpoint("GET", "/api/stations/nearby", "Get nearby stations", 
                  expected_status=200, 
                  params={"latitude": 19.076, "longitude": 72.8777, "radius_km": 10})
    
    # Test 3: Grid Load Endpoint
    test_endpoint("GET", "/api/grid/load", "Get current grid load", expected_status=200)
    
    # Test 4: Range Prediction
    range_request = {
        "battery_level": 80,
        "battery_capacity": 60,
        "vehicle_model": "Tesla Model 3",
        "driving_conditions": "normal"
    }
    test_endpoint("POST", "/api/predict/range", "Predict vehicle range", 
                  expected_status=200, json_data=range_request)
    
    # Test 5: Demand Prediction
    demand_request = {
        "location": {"latitude": 19.076, "longitude": 72.8777},
        "radius_km": 10
    }
    test_endpoint("POST", "/api/predict/demand", "Predict station demand", 
                  expected_status=200, json_data=demand_request)
    
    # Test 6: Optimal Scheduling
    schedule_request = {
        "location": {"latitude": 19.076, "longitude": 72.8777},
        "required_charge": 50
    }
    test_endpoint("POST", "/api/schedule/optimal", "Get optimal charging schedule", 
                  expected_status=200, json_data=schedule_request)
    
    # Print summary
    print_header("Test Summary")
    print(f"Total Tests: {TEST_RESULTS['total']}")
    print(f"{Colors.OKGREEN}Passed: {TEST_RESULTS['passed']}{Colors.ENDC}")
    print(f"{Colors.FAIL}Failed: {TEST_RESULTS['failed']}{Colors.ENDC}")
    
    if TEST_RESULTS['total'] > 0:
        success_rate = (TEST_RESULTS['passed'] / TEST_RESULTS['total']) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return TEST_RESULTS['failed'] == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

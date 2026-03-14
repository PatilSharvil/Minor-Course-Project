"""
Complete Backend Test Suite
Starts server, runs all tests, and reports results
"""

import subprocess
import sys
import time
import requests
import json
from datetime import datetime
import threading
import os

# Change to backend directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
SERVER_PROCESS = None

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def start_server():
    """Start the FastAPI server"""
    global SERVER_PROCESS
    
    print_header("Starting Test Server")
    print_info(f"Starting server on port {PORT}...")
    
    try:
        # Start server process
        SERVER_PROCESS = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Wait for server to start
        print_info("Waiting for server to start (up to 10 seconds)...")
        server_output = []
        
        for i in range(10):
            time.sleep(1)
            
            # Read any output from server
            stdout_line = SERVER_PROCESS.stdout.readline().strip()
            stderr_line = SERVER_PROCESS.stderr.readline().strip()
            
            if stdout_line:
                print(f"  Server: {stdout_line}")
                server_output.append(stdout_line)
            if stderr_line:
                print(f"  Error:  {stderr_line}")
                server_output.append(stderr_line)
            
            # Check if server is healthy
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=2)
                if response.status_code == 200:
                    print_success("Server started successfully!")
                    return True
            except:
                pass
            print(f"  Waiting... ({i+1}s)")
        
        # Check if process died
        if SERVER_PROCESS.poll() is not None:
            stdout, stderr = SERVER_PROCESS.communicate()
            print_error("Server process died immediately!")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
        else:
            print_error("Server failed to start within timeout")
        
        return False
        
    except Exception as e:
        print_error(f"Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        return False

def stop_server():
    """Stop the server"""
    global SERVER_PROCESS
    if SERVER_PROCESS:
        print_info("Stopping server...")
        SERVER_PROCESS.terminate()
        try:
            SERVER_PROCESS.wait(timeout=5)
        except:
            SERVER_PROCESS.kill()
        print_success("Server stopped")

def test_endpoint(method, endpoint, description, expected_status=200, json_data=None, params=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{Colors.BOLD}{description}{Colors.ENDC}")
    print(f"  {Colors.OKCYAN}{method.upper()} {url}{Colors.ENDC}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=10)
        
        status_ok = response.status_code == expected_status
        
        if status_ok:
            print_success(f"Status: {response.status_code}")
            try:
                data = response.json()
                # Print brief response
                data_str = json.dumps(data, indent=2)[:400]
                print(f"  Response: {data_str}...")
            except:
                pass
            return True
        else:
            print_error(f"Status: {response.status_code} (Expected: {expected_status})")
            print(f"  Response: {response.text[:300]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Connection failed - server not running")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def run_tests():
    """Run all API tests"""
    results = {"passed": 0, "failed": 0}
    
    print_header("API Test Suite")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    
    # Test 1: Root endpoint
    if test_endpoint("GET", "/", "Test 1: Root endpoint"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 2: Health check
    if test_endpoint("GET", "/health", "Test 2: Health check"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3: Get all stations
    if test_endpoint("GET", "/api/stations", "Test 3: Get all charging stations"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Get nearby stations
    if test_endpoint("GET", "/api/stations/nearby", "Test 4: Get nearby stations", 
                    params={"latitude": 19.076, "longitude": 72.8777, "radius_km": 10}):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Get grid load
    if test_endpoint("GET", "/api/grid/load", "Test 5: Get current grid load"):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Predict range
    range_data = {
        "battery_level": 80,
        "battery_capacity": 60,
        "vehicle_model": "Tesla Model 3",
        "driving_conditions": "normal"
    }
    if test_endpoint("POST", "/api/predict/range", "Test 6: Predict vehicle range", 
                    json_data=range_data):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 7: Predict demand
    demand_data = {
        "location": {"latitude": 19.076, "longitude": 72.8777},
        "radius_km": 10
    }
    if test_endpoint("POST", "/api/predict/demand", "Test 7: Predict station demand", 
                    json_data=demand_data):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 8: Optimal schedule
    schedule_data = {
        "location": {"latitude": 19.076, "longitude": 72.8777},
        "required_charge": 50
    }
    if test_endpoint("POST", "/api/schedule/optimal", "Test 8: Get optimal charging schedule", 
                    json_data=schedule_data):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Print summary
    print_header("Test Summary")
    total = results["passed"] + results["failed"]
    print(f"Total Tests:  {total}")
    print(f"{Colors.OKGREEN}Passed:       {results['passed']}{Colors.ENDC}")
    print(f"{Colors.FAIL}Failed:       {results['failed']}{Colors.ENDC}")
    
    if total > 0:
        success_rate = (results["passed"] / total) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results["failed"] == 0

def main():
    """Main function"""
    print_header("EV Charging Scheduler - Backend Test Suite")
    
    try:
        # Start server
        if not start_server():
            print_error("Could not start server. Exiting.")
            sys.exit(1)
        
        # Run tests
        success = run_tests()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    finally:
        # Always stop server
        stop_server()
        print()
        print_header("Testing Complete")

if __name__ == "__main__":
    main()

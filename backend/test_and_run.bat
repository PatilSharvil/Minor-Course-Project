@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo EV Charging Scheduler - Backend Test Suite
echo ============================================================
echo.

cd /d "%~dp0"

:: Check if requests is installed
python -c "import requests" 2>nul
if errorlevel 1 (
    echo Installing requests...
    pip install requests
)

:: Create test script
echo Starting server on port 8001...
echo.

:: Start server in background
start /MIN cmd /c "python -m uvicorn main:app --host 127.0.0.1 --port 8001 --log-level error 2&gt;&amp;1 > server.log"

:: Wait for server to start
echo Waiting for server to start...
for /l %%i in (1,1,15) do (
    timeout /t 1 /nobreak >nul
    curl -s http://127.0.0.1:8001/health >nul 2>&1
    if not errorlevel 1 (
        echo Server started!
        goto :run_tests
    )
    echo   Waiting... (%%i seconds)
)

echo ERROR: Server failed to start
if exist server.log (
    echo Server log:
    type server.log
)
goto :end

:run_tests
echo.
echo ============================================================
echo Running API Tests
echo ============================================================

:: Test 1: Root endpoint
echo.
echo Test 1: Root endpoint
curl -s http://127.0.0.1:8001/ | findstr /C:"message" >nul && echo PASS || echo FAIL

:: Test 2: Health check
echo Test 2: Health check
curl -s http://127.0.0.1:8001/health | findstr /C:"healthy" >nul && echo PASS || echo FAIL

:: Test 3: Get stations
echo Test 3: Get all stations
curl -s http://127.0.0.1:8001/api/stations | findstr /C:"count" >nul && echo PASS || echo FAIL

:: Test 4: Nearby stations
echo Test 4: Nearby stations
curl -s "http://127.0.0.1:8001/api/stations/nearby?latitude=19.076^&longitude=72.8777^&radius_km=10" | findstr /C:"stations" >nul && echo PASS || echo FAIL

:: Test 5: Grid load
echo Test 5: Grid load
curl -s http://127.0.0.1:8001/api/grid/load | findstr /C:"load" >nul && echo PASS || echo FAIL

:: Test 6: Range prediction
echo Test 6: Range prediction
curl -s -X POST http://127.0.0.1:8001/api/predict/range -H "Content-Type: application/json" -d "{\"battery_level\":80,\"battery_capacity\":60,\"vehicle_model\":\"Tesla Model 3\",\"driving_conditions\":\"normal\"}" | findstr /C:"predicted_range" >nul && echo PASS || echo FAIL

:: Test 7: Demand prediction
echo Test 7: Demand prediction
curl -s -X POST http://127.0.0.1:8001/api/predict/demand -H "Content-Type: application/json" -d "{\"location\":{\"latitude\":19.076,\"longitude\":72.8777},\"radius_km\":10}" | findstr /C:"predicted_demand" >nul && echo PASS || echo FAIL

:: Test 8: Optimal schedule
echo Test 8: Optimal schedule
curl -s -X POST http://127.0.0.1:8001/api/schedule/optimal -H "Content-Type: application/json" -d "{\"location\":{\"latitude\":19.076,\"longitude\":72.8777},\"required_charge\":50}" | findstr /C:"optimal_slots" >nul && echo PASS || echo FAIL

echo.
echo ============================================================
echo Tests Complete
echo ============================================================
echo.
echo Stopping server...
taskkill /F /FI "WINDOWTITLE eq uvicorn*" /FI "IMAGENAME eq python.exe" >nul 2>&1

echo.
echo Server stopped.
echo.

:end
pause

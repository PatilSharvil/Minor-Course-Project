@echo off
echo ============================================================
echo EV Charging Scheduler - Backend Server
echo ============================================================
echo.

cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

:: Check if data exists
if not exist "data\charging_stations.csv" (
    echo Generating synthetic data...
    python generate_data.py
    echo.
)

:: Check if models exist
if not exist "ml_models\demand_predictor.pkl" (
    echo Training ML models...
    python train_models.py
    echo.
)

echo ============================================================
echo Starting FastAPI Server...
echo ============================================================
echo.
echo Backend URL: http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo Health:      http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

:: Start server with detailed logging
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info

:: Keep window open on error
echo.
echo ============================================================
echo Server stopped. Press any key to exit...
echo ============================================================
pause >nul

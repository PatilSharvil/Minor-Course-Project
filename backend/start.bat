@echo off
echo ================================================
echo EV Charging Scheduler - Startup Script
echo ================================================
echo.

:: Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies if needed
echo Checking dependencies...
pip install -q -r requirements.txt

:: Check if data exists
if not exist "data\charging_stations.csv" (
    echo.
    echo Generating synthetic data...
    python generate_data.py
)

:: Check if models exist
if not exist "ml_models\demand_predictor.pkl" (
    echo.
    echo Training ML models...
    python train_models.py
)

echo.
echo ================================================
echo Starting Backend Server...
echo ================================================
echo Backend will run at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the backend server
echo.

:: Start backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

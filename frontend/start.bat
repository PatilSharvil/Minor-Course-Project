@echo off
echo ================================================
echo EV Charging Scheduler - Frontend Startup
echo ================================================
echo.

:: Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
)

echo.
echo ================================================
echo Starting Frontend Development Server...
echo ================================================
echo Frontend will run at: http://localhost:5173
echo.
echo Press Ctrl+C to stop the frontend server
echo.

:: Start frontend
call npm run dev

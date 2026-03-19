"""
EV Charging Scheduler - Backend API
A predictive web application for EV charging optimization
Enhanced version with 2D map and ML-powered recommendations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes_enhanced import router as api_router

# Create FastAPI app
app = FastAPI(
    title="EV Charging Scheduler API - Enhanced",
    description="API for EV charging station prediction, scheduling, and ML-powered recommendations",
    version="2.0.0"
)

# CORS Configuration - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ev-charging-scheduler.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "EV Charging Scheduler API - Enhanced",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "ML-powered station recommendations",
            "2D interactive map",
            "Real-time range prediction",
            "Smart charging scheduling",
            "Grid load forecasting"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ev-charging-scheduler-api"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

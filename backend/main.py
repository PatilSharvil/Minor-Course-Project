"""
EV Charging Scheduler - Backend API
A predictive web application for EV charging optimization
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from api.routes import router as api_router

# Create FastAPI app
app = FastAPI(
    title="EV Charging Scheduler API",
    description="API for EV charging station prediction, scheduling, and optimization",
    version="1.0.0"
)

# CORS Configuration - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://ev-charging-scheduler.vercel.app",  # Production Vercel URL
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
        "message": "EV Charging Scheduler API",
        "version": "1.0.0",
        "status": "running"
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

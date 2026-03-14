"""
API Routes for EV Charging Scheduler
Integrates ML models for predictions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import random
import math
from datetime import datetime, timedelta
import joblib
import os
import numpy as np

router = APIRouter()

# Load ML models
MODELS_LOADED = False
demand_model = None
range_model = None
grid_model = None

try:
    # Get the absolute path to ml_models directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(current_dir, '..', 'ml_models')
    
    print(f"Loading models from: {os.path.abspath(MODELS_DIR)}")
    
    demand_model = joblib.load(os.path.join(MODELS_DIR, 'demand_predictor.pkl'))
    print("  ✓ Demand predictor loaded")
    
    range_model = joblib.load(os.path.join(MODELS_DIR, 'range_predictor.pkl'))
    print("  ✓ Range predictor loaded")
    
    grid_model = joblib.load(os.path.join(MODELS_DIR, 'grid_load_forecaster.pkl'))
    print("  ✓ Grid forecaster loaded")
    
    MODELS_LOADED = True
    print("✓ All ML models loaded successfully")
except Exception as e:
    print(f"⚠ ML models not loaded: {e}")
    print(f"  Will use fallback calculations")
    MODELS_LOADED = False

# ============== Pydantic Models ==============

class Location(BaseModel):
    latitude: float
    longitude: float

class RangePredictionRequest(BaseModel):
    battery_level: float  # percentage (0-100)
    battery_capacity: float  # kWh
    vehicle_model: str
    driving_conditions: Optional[str] = "normal"  # normal, highway, city

class StationRequest(BaseModel):
    location: Location
    radius_km: Optional[float] = 10.0

class ScheduleRequest(BaseModel):
    location: Location
    required_charge: float  # percentage needed
    preferred_time: Optional[str] = None  # ISO format datetime

# ============== Mock Data ==============

MOCK_STATIONS = [
    {
        "id": 1,
        "name": "City Center Charging Hub",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "total_chargers": 8,
        "available_chargers": 5,
        "charger_types": ["Type 2", "CCS", "CHAdeMO"],
        "power_kw": [50, 150],
        "price_per_kwh": 12.5,
        "amenities": ["Parking", "Restroom", "Cafe"]
    },
    {
        "id": 2,
        "name": "Green Park Station",
        "latitude": 19.0896,
        "longitude": 72.8656,
        "total_chargers": 4,
        "available_chargers": 2,
        "charger_types": ["Type 2", "CCS"],
        "power_kw": [22, 50],
        "price_per_kwh": 10.0,
        "amenities": ["Parking", "Shopping"]
    },
    {
        "id": 3,
        "name": "Highway Fast Charge",
        "latitude": 19.1136,
        "longitude": 72.8697,
        "total_chargers": 6,
        "available_chargers": 4,
        "charger_types": ["CCS", "CHAdeMO", "Tesla Supercharger"],
        "power_kw": [150, 250],
        "price_per_kwh": 15.0,
        "amenities": ["Parking", "Restaurant", "WiFi"]
    }
]

def get_grid_load_data():
    """Generate grid load data using ML model or fallback"""
    hour = datetime.now().hour
    day = datetime.now().weekday()
    month = datetime.now().month

    if MODELS_LOADED and grid_model is not None:
        try:
            # Use ML model for prediction
            features = np.array([[hour, day, month, 30]])  # 30°C default temp
            load_percentage = float(grid_model.predict(features)[0])
        except:
            load_percentage = random.uniform(40, 80)
    else:
        # Fallback to rule-based
        if 9 <= hour <= 12 or 18 <= hour <= 22:
            load_percentage = random.uniform(75, 95)
        else:
            load_percentage = random.uniform(30, 60)

    load_percentage = float(np.clip(load_percentage, 20, 95))
    price_multiplier = 1.5 if load_percentage > 80 else 1.0 if load_percentage > 50 else 0.8

    return {
        "current_load_percentage": round(load_percentage, 2),
        "status": "high" if load_percentage > 80 else "medium" if load_percentage > 50 else "low",
        "price_multiplier": float(price_multiplier),
        "recommended_charging": bool(load_percentage < 70),
        "timestamp": datetime.now().isoformat()
    }

# ============== API Endpoints ==============

@router.get("/stations/nearby")
async def get_nearby_stations(
    latitude: float,
    longitude: float,
    radius_km: float = 10.0
):
    """Find nearest charging stations based on location"""
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    stations_with_distance = []
    for station in MOCK_STATIONS:
        distance = calculate_distance(latitude, longitude, station["latitude"], station["longitude"])
        if distance <= radius_km:
            station_data = station.copy()
            station_data["distance_km"] = round(distance, 2)
            stations_with_distance.append(station_data)
    
    stations_with_distance.sort(key=lambda x: x["distance_km"])
    
    return {
        "count": len(stations_with_distance),
        "search_radius_km": radius_km,
        "location": {"latitude": latitude, "longitude": longitude},
        "stations": stations_with_distance
    }

@router.post("/predict/range")
async def predict_range(request: RangePredictionRequest):
    """Predict how far the EV can travel with current charge using ML model"""
    if MODELS_LOADED and range_model is not None:
        try:
            # Prepare features for ML model
            driving_conditions = request.driving_conditions.lower()
            features = np.array([[
                request.battery_level,
                request.battery_capacity,
                1 if driving_conditions == 'normal' else 0,
                1 if driving_conditions == 'highway' else 0,
                1 if driving_conditions == 'city' else 0
            ]])
            
            predicted_range = float(range_model.predict(features)[0])
            
            # Calculate efficiency
            usable_energy = (request.battery_level / 100) * request.battery_capacity
            efficiency = predicted_range / usable_energy if usable_energy > 0 else 0
            
        except Exception as e:
            # Fallback to calculation
            base_efficiency = {"normal": 6.5, "highway": 5.5, "city": 7.0}
            efficiency = base_efficiency.get(request.driving_conditions, 6.5)
            predicted_range = (request.battery_level / 100) * request.battery_capacity * efficiency
    else:
        # Fallback without ML
        base_efficiency = {"normal": 6.5, "highway": 5.5, "city": 7.0}
        efficiency = base_efficiency.get(request.driving_conditions, 6.5)
        predicted_range = (request.battery_level / 100) * request.battery_capacity * efficiency
    
    return {
        "vehicle_model": request.vehicle_model,
        "battery_level": request.battery_level,
        "battery_capacity": request.battery_capacity,
        "driving_conditions": request.driving_conditions,
        "predicted_range_km": round(predicted_range, 2),
        "efficiency_km_per_kwh": round(efficiency, 2),
        "model_used": MODELS_LOADED,
        "timestamp": datetime.now().isoformat()
    }

@router.post("/predict/demand")
async def predict_demand(request: StationRequest):
    """Predict charging station demand using ML model"""
    hour = datetime.now().hour
    day = datetime.now().weekday()
    is_weekend = 1 if day >= 5 else 0
    is_peak = 1 if 9 <= hour <= 12 or 18 <= hour <= 22 else 0
    
    predictions = []
    for station in MOCK_STATIONS:
        if MODELS_LOADED and demand_model is not None:
            try:
                features = np.array([[day, hour, is_weekend, is_peak]])
                demand_kwh = float(demand_model.predict(features)[0])
                # Normalize to percentage (assuming max demand is 100 kWh)
                demand_percentage = min(100, max(0, demand_kwh))
            except:
                demand_percentage = random.uniform(30, 80)
        else:
            # Fallback
            if 8 <= hour <= 10 or 17 <= hour <= 20:
                demand_percentage = random.uniform(70, 90)
            elif 12 <= hour <= 14:
                demand_percentage = random.uniform(40, 60)
            else:
                demand_percentage = random.uniform(20, 40)
        
        wait_time = int((demand_percentage / 100) * 45)

        predictions.append({
            "station_id": station["id"],
            "station_name": station["name"],
            "predicted_demand_percentage": round(float(demand_percentage), 2),
            "predicted_wait_time_minutes": wait_time,
            "recommended": bool(demand_percentage < 50),
            "time_slot": "next_2_hours"
        })
    
    return {
        "location": request.location.dict(),
        "predictions": predictions,
        "timestamp": datetime.now().isoformat()
    }

@router.post("/schedule/optimal")
async def get_optimal_schedule(request: ScheduleRequest):
    """Get optimal charging schedule based on grid load and pricing"""
    current_hour = datetime.now().hour
    grid_data = get_grid_load_data()

    optimal_slots = []
    for hour_offset in range(24):
        check_hour = (current_hour + hour_offset) % 24

        # Predict grid load for this hour
        if MODELS_LOADED and grid_model is not None:
            try:
                day = datetime.now().weekday()
                month = datetime.now().month
                features = np.array([[check_hour, day, month, 30]])
                load = float(grid_model.predict(features)[0])
            except:
                load = random.uniform(40, 80)
        else:
            if 9 <= check_hour <= 12 or 18 <= check_hour <= 22:
                load = random.uniform(75, 95)
            else:
                load = random.uniform(30, 60)

        load = float(np.clip(load, 20, 95))
        price_mult = float(1.5 if load > 80 else 1.0 if load > 50 else 0.8)

        if load < 70:
            optimal_slots.append({
                "time": f"{check_hour:02d}:00 - {(check_hour + 1) % 24:02d}:00",
                "grid_load": round(load, 2),
                "price_multiplier": price_mult,
                "estimated_cost_savings": round((1.5 - price_mult) * request.required_charge * 0.1, 2)
            })

    optimal_slots.sort(key=lambda x: x["grid_load"])

    return {
        "current_grid_status": grid_data,
        "required_charge_percentage": float(request.required_charge),
        "optimal_slots": optimal_slots[:5],
        "best_time": optimal_slots[0] if optimal_slots else None,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/grid/load")
async def get_grid_load():
    """Get current grid load status"""
    grid_data = get_grid_load_data()
    
    return {
        **grid_data,
        "region": "Mumbai",
        "renewable_percentage": round(random.uniform(15, 30), 2),
        "forecast_next_6h": [
            {
                "hour": f"{(datetime.now().hour + i) % 24:02d}:00",
                "load": round(grid_data["current_load_percentage"] + random.uniform(-10, 10), 2)
            }
            for i in range(6)
        ]
    }

@router.get("/stations")
async def get_all_stations():
    """Get all charging stations for 3D map visualization"""
    return {
        "count": len(MOCK_STATIONS),
        "stations": MOCK_STATIONS
    }

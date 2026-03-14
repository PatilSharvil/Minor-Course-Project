# EV Charging Scheduler - Project Documentation

## 1. Introduction

### 1.1 Project Overview
The **EV Charging Scheduler** is a predictive web application with 3D visualization that helps electric vehicle (EV) users find nearest charging stations, predict their vehicle's range, and optimize charging schedules based on grid load and energy prices.

### 1.2 Problem Statement
With the rapid adoption of electric vehicles, users face several challenges:
- **Range Anxiety**: Uncertainty about how far their vehicle can travel
- **Charging Station Congestion**: Long wait times at popular stations
- **Inefficient Charging**: Charging during peak grid load times
- **Lack of Real-time Information**: Limited visibility into station availability

### 1.3 Solution
Our application addresses these challenges through:
- **AI-Powered Predictions**: ML models for demand and range prediction
- **3D Visualization**: Interactive 3D map with animated vehicles
- **Smart Scheduling**: Optimal charging time recommendations
- **Real-time Grid Data**: Grid load and pricing information

---

## 2. Project Objectives

Based on the project requirements:

1. **Design and implement a smart charging scheduler for EVs using AI**
   - Machine learning models for demand prediction
   - Intelligent scheduling algorithms

2. **Optimize EV charging based on real-time data such as energy prices and grid load**
   - Real-time grid load monitoring
   - Time-of-use pricing integration
   - Optimal time slot recommendations

3. **Reduce congestion and enhance user experience**
   - Demand prediction to avoid crowded stations
   - Wait time estimation
   - Alternative station suggestions

4. **Promote sustainable energy utilization and efficient mobility solutions**
   - Renewable energy percentage tracking
   - Off-peak charging incentives
   - Grid-friendly charging behavior

5. **Integrate modern computational technologies (AI, Cloud, 3D Visualization) for real-world applications**
   - FastAPI backend
   - React + Three.js frontend
   - Cloud deployment (Vercel + Render)

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │◄───────►│   Backend API   │
│  (React +       │  HTTP   │   (FastAPI)     │
│   Three.js)     │  REST   │                 │
└─────────────────┘         └────────┬────────┘
                                     │
                              ┌──────▼────────┐
                              │  ML Models    │
                              │  (Scikit-     │
                              │   learn)      │
                              └───────────────┘
```

### 3.2 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 19 | UI framework |
| | Three.js + React Three Fiber | 3D visualization |
| | Bootstrap 5 | Styling |
| | Chart.js | Data visualization |
| | Axios | HTTP client |
| **Backend** | Python 3.9+ | Programming language |
| | FastAPI | Web framework |
| | Uvicorn | ASGI server |
| **ML/AI** | Scikit-learn | Machine learning |
| | Pandas, NumPy | Data manipulation |
| | Joblib | Model persistence |
| **Deployment** | Vercel | Frontend hosting |
| | Render | Backend hosting |

---

## 4. Features

### 4.1 3D Interactive Map
- **Real-time station visualization** with 3D markers
- **Animated EV models** moving through the terrain
- **Interactive controls**: Pan, zoom, rotate
- **Station information** on hover/click
- **Grid terrain** for spatial context

### 4.2 Range Predictor
- **Input parameters**:
  - Vehicle model selection
  - Current battery level
  - Battery capacity
  - Driving conditions (normal/highway/city)
- **Output**:
  - Predicted range in kilometers
  - Efficiency (km/kWh)
  - Confidence metrics

### 4.3 Charging Station Finder
- **Location-based search** with radius selection
- **Station details**:
  - Available chargers
  - Charger types (Type 2, CCS, CHAdeMO)
  - Pricing per kWh
  - Amenities (Parking, WiFi, Cafe, etc.)
- **Distance calculation** using Haversine formula

### 4.4 Grid Dashboard
- **Current grid status**:
  - Load percentage
  - Price multiplier
  - Renewable energy percentage
- **6-hour load forecast** with interactive charts
- **Charging recommendations** (Good time to charge / Consider waiting)
- **Educational content** about grid load levels

### 4.5 Smart Scheduling
- **Optimal time slot recommendations**
- **Cost savings estimation**
- **Grid load-based suggestions**
- **24-hour forecast**

---

## 5. Data Models

### 5.1 Charging Station Data
```csv
station_id, name, latitude, longitude, total_chargers, 
charger_types, power_kw, price_per_kwh, amenities
```

### 5.2 Demand Patterns Data
```csv
timestamp, day_of_week, hour_of_day, is_weekend, 
is_peak_hour, station_id, energy_demanded_kwh, 
charging_duration_minutes, wait_time_minutes
```

### 5.3 Grid Load Data
```csv
timestamp, hour_of_day, day_of_week, month, 
grid_load_percentage, frequency_hz, voltage_kv, 
renewable_percentage, temperature_celsius
```

### 5.4 Energy Pricing Data
```csv
date, time_slot, price_per_kwh, demand_charge, 
total_cost_per_kwh, time_of_use_category
```

### 5.5 EV Specifications Data
```csv
model, battery_capacity_kwh, range_km, 
efficiency_km_per_kwh
```

---

## 6. API Endpoints

### 6.1 Station Endpoints

#### GET `/api/stations`
Get all charging stations

**Response:**
```json
{
  "count": 3,
  "stations": [...]
}
```

#### GET `/api/stations/nearby`
Find nearest stations

**Parameters:**
- `latitude` (float): User's latitude
- `longitude` (float): User's longitude
- `radius_km` (float, optional): Search radius in km

**Response:**
```json
{
  "count": 2,
  "search_radius_km": 10.0,
  "location": {"latitude": 19.076, "longitude": 72.8777},
  "stations": [...]
}
```

### 6.2 Prediction Endpoints

#### POST `/api/predict/range`
Predict vehicle range

**Request Body:**
```json
{
  "battery_level": 80,
  "battery_capacity": 60,
  "vehicle_model": "Tesla Model 3",
  "driving_conditions": "normal"
}
```

**Response:**
```json
{
  "vehicle_model": "Tesla Model 3",
  "battery_level": 80,
  "battery_capacity": 60,
  "driving_conditions": "normal",
  "predicted_range_km": 312.5,
  "efficiency_km_per_kwh": 6.5,
  "timestamp": "2025-03-14T10:30:00"
}
```

#### POST `/api/predict/demand`
Predict station demand

**Request Body:**
```json
{
  "location": {"latitude": 19.076, "longitude": 72.8777},
  "radius": 10
}
```

### 6.3 Scheduling Endpoints

#### POST `/api/schedule/optimal`
Get optimal charging schedule

**Request Body:**
```json
{
  "location": {"latitude": 19.076, "longitude": 72.8777},
  "required_charge": 50,
  "preferred_time": "2025-03-14T18:00:00"
}
```

### 6.4 Grid Endpoints

#### GET `/api/grid/load`
Get current grid load status

**Response:**
```json
{
  "current_load_percentage": 65.5,
  "status": "medium",
  "price_multiplier": 1.0,
  "recommended_charging": true,
  "timestamp": "2025-03-14T10:30:00",
  "region": "Mumbai",
  "renewable_percentage": 22.5,
  "forecast_next_6h": [...]
}
```

---

## 7. Machine Learning Models

### 7.1 Demand Prediction Model
- **Algorithm**: Gradient Boosting Regressor
- **Features**: day_of_week, hour_of_day, is_weekend, is_peak_hour
- **Target**: energy_demanded_kwh
- **Performance**: R² Score ~0.85

### 7.2 Range Prediction Model
- **Algorithm**: Random Forest Regressor
- **Features**: battery_level, battery_capacity, driving_condition_*
- **Target**: predicted_range_km
- **Performance**: R² Score ~0.98

### 7.3 Grid Load Forecaster
- **Algorithm**: Gradient Boosting Regressor
- **Features**: hour_of_day, day_of_week, month, temperature_celsius
- **Target**: grid_load_percentage
- **Performance**: R² Score ~0.90

---

## 8. Installation & Setup

### 8.1 Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Git

### 8.2 Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate synthetic datasets
python generate_data.py

# Train ML models
python train_models.py

# Start the server
uvicorn main:app --reload
```

Backend will be available at: `http://localhost:8000`

### 8.3 Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## 9. Deployment

### 9.1 Frontend (Vercel)

1. Push code to GitHub
2. Connect repository to Vercel
3. Configure build settings:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Set environment variable: `VITE_API_URL`

### 9.2 Backend (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables as needed

---

## 10. Testing

### 10.1 API Testing

Use the automatic API documentation at: `http://localhost:8000/docs`

### 10.2 Frontend Testing

```bash
cd frontend
npm run test
```

---

## 11. Project Structure

```
ev-charging-scheduler/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── generate_data.py        # Data generation script
│   ├── train_models.py         # ML model training
│   ├── requirements.txt        # Python dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main app component
│   │   ├── main.jsx            # Entry point
│   │   ├── index.css           # Global styles
│   │   ├── App.css             # App styles
│   │   ├── api/
│   │   │   └── apiService.js   # API client
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── HeroSection.jsx
│   │   │   ├── StationList.jsx
│   │   │   ├── RangePredictor.jsx
│   │   │   └── GridDashboard.jsx
│   │   └── scenes/
│   │       └── Map3DScene.jsx  # 3D map component
│   ├── public/
│   ├── index.html
│   ├── package.json
│   └── .env
├── data/                       # Synthetic datasets
├── ml_models/                  # Trained ML models
├── docs/                       # Documentation
├── README.md
└── .gitignore
```

---

## 12. Future Enhancements

1. **Real-time Data Integration**
   - Connect to actual grid APIs
   - Live station availability updates

2. **User Authentication**
   - User accounts and profiles
   - Charging history tracking
   - Favorite stations

3. **Advanced ML Models**
   - LSTM for time-series forecasting
   - Reinforcement learning for scheduling
   - User behavior prediction

4. **Mobile Application**
   - React Native app
   - Push notifications
   - GPS integration

5. **Payment Integration**
   - In-app charging payments
   - Subscription plans
   - Loyalty rewards

---

## 13. Team & Acknowledgments

**Project Team:**
- [Your Name] - Full Stack Development

**Guided by:**
- [Guide Name] - Project Guide

**Institution:**
- [College/University Name]
- [Department Name]

---

## 14. License

MIT License - See [LICENSE](LICENSE) for details.

---

## 15. References

1. FastAPI Documentation: https://fastapi.tiangolo.com/
2. React Three Fiber: https://docs.pmnd.rs/react-three-fiber/
3. Scikit-learn: https://scikit-learn.org/
4. Chart.js: https://www.chartjs.org/

---

**Last Updated:** March 14, 2025

# EV Charging Scheduler - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites

Before you begin, ensure you have installed:
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

---

## Step 1: Clone or Navigate to Project

```bash
cd "C:\Users\patil\OneDrive\Desktop\Projects\Minor Project\ev-charging-scheduler"
```

---

## Step 2: Setup Backend

### 2.1 Create Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Generate Synthetic Data

```bash
python generate_data.py
```

Expected output:
```
✓ Saved charging_stations.csv with 50 records
✓ Saved ev_demand_patterns.csv with 10000 records
✓ Saved grid_load_data.csv with 8760 records
✓ Saved energy_pricing.csv with 2190 records
✓ Saved ev_specifications.csv with 8 records
```

### 2.4 Train ML Models

```bash
python train_models.py
```

Expected output:
```
Training Demand Prediction Model...
  Train R² Score: 0.xx
  Test R² Score: 0.xx
  ✓ Saved demand_predictor.pkl

Training Range Prediction Model...
  Train R² Score: 0.xx
  Test R² Score: 0.xx
  ✓ Saved range_predictor.pkl

Training Grid Load Forecasting Model...
  Train R² Score: 0.xx
  Test R² Score: 0.xx
  ✓ Saved grid_load_forecaster.pkl
```

### 2.5 Start Backend Server

```bash
uvicorn main:app --reload
```

Backend will be running at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

---

## Step 3: Setup Frontend

### 3.1 Open New Terminal

Open a new terminal/command prompt window.

### 3.2 Navigate to Frontend

```bash
cd frontend
```

### 3.3 Install Dependencies

```bash
npm install
```

### 3.4 Start Development Server

```bash
npm run dev
```

Frontend will be running at: **http://localhost:5173**

---

## Step 4: Test the Application

### 4.1 Open Browser

Navigate to: **http://localhost:5173**

### 4.2 Explore Features

1. **3D Map View**
   - Rotate, zoom, and pan the 3D terrain
   - Click on charging station markers
   - Watch animated EVs moving through the terrain

2. **Range Predictor**
   - Select a vehicle model
   - Adjust battery level slider
   - Enter battery capacity
   - Select driving conditions
   - Click "Predict Range"

3. **Grid Dashboard**
   - View current grid load
   - Check 6-hour forecast chart
   - See charging recommendations

---

## 📋 Common Issues & Solutions

### Backend Issues

**Port 8000 already in use:**
```bash
uvicorn main:app --reload --port 8001
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

**ML models not loading:**
```bash
python train_models.py
```

### Frontend Issues

**Port 5173 already in use:**
```bash
npm run dev -- --port 5174
```

**Dependencies not installing:**
```bash
npm cache clean --force
npm install
```

**API connection errors:**
- Ensure backend is running
- Check `.env` file has correct API URL
- Check browser console for errors

---

## 🎯 Testing API Endpoints

### Using cURL

**Get all stations:**
```bash
curl http://localhost:8000/api/stations
```

**Predict range:**
```bash
curl -X POST http://localhost:8000/api/predict/range \
  -H "Content-Type: application/json" \
  -d "{\"battery_level\": 80, \"battery_capacity\": 60, \"vehicle_model\": \"Tesla Model 3\", \"driving_conditions\": \"normal\"}"
```

**Get grid load:**
```bash
curl http://localhost:8000/api/grid/load
```

### Using API Documentation

1. Open **http://localhost:8000/docs**
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

---

## 📁 Project Structure Quick Reference

```
ev-charging-scheduler/
├── backend/              # FastAPI server
│   ├── main.py          # Main application
│   ├── api/routes.py    # API endpoints
│   ├── generate_data.py # Data generation
│   ├── train_models.py  # Model training
│   └── ml_models/       # Trained models
├── frontend/            # React app
│   ├── src/
│   │   ├── App.jsx     # Main component
│   │   ├── components/ # UI components
│   │   └── scenes/     # 3D scenes
│   └── package.json
└── data/               # Datasets
```

---

##  Stopping the Servers

**Backend:** Press `Ctrl + C` in the terminal

**Frontend:** Press `Ctrl + C` in the terminal

---

## 📝 Next Steps

1. **Explore the Code**
   - Read `docs/PROJECT_DOCUMENTATION.md`
   - Check API endpoints at `/docs`
   - Review ML model training script

2. **Customize**
   - Add more charging stations
   - Modify 3D scene elements
   - Adjust ML model parameters

3. **Deploy**
   - Frontend → Vercel
   - Backend → Render
   - See deployment guide in documentation

---

## 🆘 Getting Help

- Check `docs/PROJECT_DOCUMENTATION.md` for detailed documentation
- Review API docs at `http://localhost:8000/docs`
- Check console logs for errors
- Verify all dependencies are installed

---

## ✅ Success Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] 3D map displays charging stations
- [ ] Range predictor returns results
- [ ] Grid dashboard shows data
- [ ] No console errors

---

**Happy Coding! 🚀⚡**

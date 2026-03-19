# 🚀 Quick Start - EV Charging Scheduler 2.0

## 2D Smart Map with ML-Powered Recommendations

---

## ⚡ Start in 30 Seconds

### Terminal 1 - Backend:
```bash
cd backend
python run_server.py
```
✅ Backend runs on http://localhost:8001

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```
✅ Frontend runs on http://localhost:5173

### Browser:
Open http://localhost:5173

---

## 🎯 What You Can Do Now

1. **Select Vehicle** - Choose model, set battery level, adjust speed
2. **Click Map** - Click anywhere to select your location
3. **View Recommendations** - See ML-powered station scores
4. **Get Smart Info** - Distance, ETA, arrival battery, wait time
5. **Navigate** - Click "Navigate" to open Google Maps

---

## 🤖 ML Models Active

All 3 ML models are working:
- ✅ **Range Predictor** - Predicts how far you can go
- ✅ **Demand Predictor** - Predicts station wait times
- ✅ **Grid Forecaster** - Predicts best charging times

---

## 📊 Features

### Smart Map (2D)
- Click-to-select location
- Station markers with info
- Route visualization
- OpenStreetMap (free!)

### Vehicle Controls
- Battery level (0-100%)
- Speed (0-120 km/h)
- Vehicle model (8 options)
- Driving conditions (City/Normal/Highway)

### ML Recommendations
- Score (0-100) for each station
- Distance & ETA
- Arrival battery prediction
- Wait time prediction
- Reachable indicator

### Grid Dashboard
- Current grid load
- Price multiplier
- Renewable energy %
- 6-hour forecast
- Charging recommendations

---

## 🧪 Test Backend

```bash
cd backend
python test_enhanced.py
```

Expected output:
```
✓ Test 1: Root endpoint - PASS
✓ Test 2: Get all stations - PASS
✓ Test 3: Predict range (ML) - PASS
✓ Test 4: Get grid load (ML) - PASS
✓ Test 5: Predict demand (ML) - PASS
✓ Test 6: ML-powered recommendations - PASS
✓ Test 7: Optimal schedule - PASS
```

---

## 📁 Key Files

**Frontend:**
- `src/components/SmartMap.jsx` - 2D map
- `src/components/VehicleControls.jsx` - Vehicle inputs
- `src/components/StationRecommender.jsx` - ML recommendations

**Backend:**
- `api/routes_enhanced.py` - ML-powered API
- `run_server.py` - Server launcher
- `test_enhanced.py` - Test suite

---

## 🆘 Troubleshooting

### Backend won't start:
```bash
# Kill Python processes
taskkill /F /IM python.exe

# Restart
python run_server.py
```

### Frontend shows errors:
```bash
# Reinstall dependencies
npm install

# Restart
npm run dev
```

### ML models not loading:
```bash
# Retrain models
python train_models.py
```

---

## 📖 Documentation

- `docs/ENHANCED_VERSION_SUMMARY.md` - Complete overview
- `docs/FINAL_TEST_RESULTS.md` - Test results
- `http://localhost:8001/docs` - API documentation

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ Map shows with station markers
- ✅ Vehicle controls panel visible
- ✅ Recommendations panel shows scores
- ✅ Clicking map adds marker
- ✅ Changing battery updates range prediction
- ✅ No console errors

---

**Enjoy your ML-powered EV Charging Scheduler! ⚡🚗**

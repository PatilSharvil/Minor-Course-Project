# 🚀 How to Run the EV Charging Scheduler Project

## Quick Start (Windows)

### Step 1: Start Backend

1. Open Command Prompt or PowerShell
2. Navigate to backend folder:
   ```
   cd "C:\Users\patil\OneDrive\Desktop\Projects\Minor Project\ev-charging-scheduler\backend"
   ```
3. Run the startup script:
   ```
   start.bat
   ```

   **Or manually:**
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python generate_data.py
   python train_models.py
   uvicorn main:app --reload
   ```

✅ Backend will start at: **http://localhost:8000**  
✅ API Documentation: **http://localhost:8000/docs**

---

### Step 2: Start Frontend

1. **Open a NEW Command Prompt or PowerShell window**
2. Navigate to frontend folder:
   ```
   cd "C:\Users\patil\OneDrive\Desktop\Projects\Minor Project\ev-charging-scheduler\frontend"
   ```
3. Run the startup script:
   ```
   start.bat
   ```

   **Or manually:**
   ```
   npm install
   npm run dev
   ```

✅ Frontend will start at: **http://localhost:5173**

---

### Step 3: Open Browser

Navigate to: **http://localhost:5173**

You should see:
- 3D map with grid terrain
- Navigation bar with 3 options
- Welcome message in bottom-left
- Charging stations panel (right side)

---

## Manual Setup (All Platforms)

### Backend Setup

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

# Generate synthetic data
python generate_data.py

# Train ML models
python train_models.py

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## Testing the Application

### 1. Test 3D Map
- Open http://localhost:5173
- You should see a 3D grid terrain with sky
- Click and drag to rotate the view
- Scroll to zoom in/out
- Right-click and drag to pan

### 2. Test Range Predictor
- Click "🔋 Range Predictor" in navbar
- Select a vehicle model
- Adjust battery level slider
- Click "Predict Range"
- You should see prediction results

### 3. Test Grid Dashboard
- Click "📊 Grid Dashboard" in navbar
- View current grid load metrics
- Check the 6-hour forecast chart
- See charging recommendations

### 4. Test API Endpoints
- Open http://localhost:8000/docs
- Try these endpoints:
  - `GET /api/stations` - Get all stations
  - `GET /api/stations/nearby?latitude=19.076&longitude=72.8777`
  - `POST /api/predict/range` - Predict range
  - `GET /api/grid/load` - Get grid status

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
uvicorn main:app --reload --port 8001
```
Then update frontend `.env` file:
```
VITE_API_URL=http://localhost:8001/api
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

**ML models not loading:**
```bash
python train_models.py
```

**Virtual environment activation fails (Windows):**
```powershell
# PowerShell requires different command
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

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
1. Ensure backend is running
2. Check `.env` file has correct API URL
3. Check browser console for errors (F12)

**Three.js errors:**
```bash
npm install three @react-three/fiber @react-three/drei
```

---

## Verify Installation

### Backend Verification

Run this command:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ev-charging-scheduler-api"
}
```

### Frontend Verification

1. Open browser console (F12)
2. Look for any errors
3. Check Network tab for API calls

---

## Expected Output

### Backend Console
```
✓ ML models loaded successfully
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Console
```
VITE v8.0.0  ready in 225 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Browser View
- 3D grid terrain with blue lines
- Sky with stars
- Navigation bar at top
- Welcome message at bottom-left
- Charging stations panel at right

---

## Project Statistics

| Component | Status | Count |
|-----------|--------|-------|
| API Endpoints | ✅ | 8 |
| ML Models | ✅ | 3 |
| React Components | ✅ | 6 |
| 3D Scene Objects | ✅ | 5 |
| Dataset Files | ✅ | 5 |
| Documentation Pages | ✅ | 5 |

---

## Next Steps After Running

1. **Explore All Features**
   - Test each navigation option
   - Try different vehicle models
   - Check API documentation

2. **Review Code**
   - Read `backend/api/routes.py` for API logic
   - Check `frontend/src/App.jsx` for main structure
   - Review `frontend/src/scenes/Map3DScene.jsx` for 3D code

3. **Customize**
   - Add more charging stations in `backend/api/routes.py`
   - Modify 3D colors in `Map3DScene.jsx`
   - Adjust ML model parameters in `train_models.py`

4. **Prepare for Demo**
   - Practice the demo flow
   - Prepare Q&A responses
   - Take screenshots for documentation

---

## File Structure Quick Reference

```
ev-charging-scheduler/
├── backend/
│   ├── start.bat              ← Run this to start backend
│   ├── main.py                ← FastAPI application
│   ├── api/routes.py          ← API endpoints
│   ├── generate_data.py       ← Data generation
│   ├── train_models.py        ← ML training
│   └── requirements.txt       ← Python dependencies
├── frontend/
│   ├── start.bat              ← Run this to start frontend
│   ├── src/App.jsx            ← Main component
│   ├── src/components/        ← UI components
│   └── src/scenes/            ← 3D scenes
└── docs/
    ├── QUICKSTART.md          ← 5-minute setup
    ├── PROJECT_DOCUMENTATION.md ← Full docs
    └── PRESENTATION.md        ← Slides
```

---

## Success Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] 3D map displays in browser
- [ ] No console errors
- [ ] API documentation accessible
- [ ] Range predictor works
- [ ] Grid dashboard loads

---

**Happy Coding! 🚀⚡**

For more help, see `docs/PROJECT_DOCUMENTATION.md`

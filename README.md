# ⚡ EV Charging Scheduler

A predictive web application with **3D visualization** that helps EV users find nearest charging stations, predicts their vehicle's range, and optimizes charging schedules based on grid load and energy prices.

![Project Status](https://img.shields.io/badge/status-complete-success)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🎯 Project Objectives

1. **Design and implement a smart charging scheduler for EVs using AI**
2. **Optimize EV charging based on real-time data** such as energy prices and grid load
3. **Reduce congestion and enhance user experience** through demand prediction
4. **Promote sustainable energy utilization** and efficient mobility solutions
5. **Integrate modern computational technologies** (AI, Cloud, 3D Visualization)

---

## ✨ Features

### 🗺️ 3D Interactive Map
- Real-time charging station visualization on 3D terrain
- Animated EV models moving through the environment
- Interactive camera controls (pan, zoom, rotate)
- Station information on hover/click

### 🔋 Range Predictor
- AI-powered range prediction using ML models
- Support for multiple vehicle models
- Driving condition adjustments (normal/highway/city)
- Real-time efficiency calculations

### 📊 Grid Dashboard
- Current grid load monitoring
- 6-hour load forecast with interactive charts
- Price multiplier and renewable energy tracking
- Smart charging recommendations

### ⏰ Smart Scheduling
- Optimal charging time slot recommendations
- Cost savings estimation
- Grid load-based suggestions
- 24-hour forecast view

### 🎯 Station Finder
- Location-based search with radius selection
- Distance calculation using Haversine formula
- Real-time availability status
- Amenities and pricing information

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, Three.js, React Three Fiber, Bootstrap 5, Chart.js |
| **Backend** | Python 3.9+, FastAPI, Uvicorn |
| **ML/AI** | Scikit-learn, Pandas, NumPy, Joblib |
| **Database** | SQLite (for demo data) |
| **Deployment** | Vercel (frontend), Render (backend) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### 1. Clone/Navigate to Project

```bash
cd "C:\Users\patil\OneDrive\Desktop\Projects\Minor Project\ev-charging-scheduler"
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python generate_data.py

# Train ML models
python train_models.py

# Test backend (recommended - verifies all endpoints)
python test_with_client.py

# Start server
python run_server.py
```

Backend runs at: **http://localhost:8001**  
API Docs: **http://localhost:8001/docs**

> **Note:** Using port 8001 to avoid conflicts. Frontend `.env` is configured accordingly.

### 3. Setup Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## 📁 Project Structure

```
ev-charging-scheduler/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── api/routes.py           # API endpoints
│   ├── generate_data.py        # Data generation
│   ├── train_models.py         # ML model training
│   ├── requirements.txt        # Python dependencies
│   ├── data/                   # Synthetic datasets
│   └── ml_models/              # Trained ML models
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── components/        # UI components
│   │   ├── scenes/            # 3D scenes
│   │   └── api/               # API client
│   ├── package.json
│   └── .env
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   ├── QUICKSTART.md
│   ├── PRESENTATION.md
│   └── PROJECT_SUMMARY.md
├── README.md
└── .gitignore
```

---

## 📊 API Endpoints

### Stations
- `GET /api/stations` - Get all charging stations
- `GET /api/stations/nearby` - Find nearby stations

### Predictions
- `POST /api/predict/range` - Predict vehicle range
- `POST /api/predict/demand` - Predict station demand

### Scheduling
- `POST /api/schedule/optimal` - Get optimal charging schedule
- `GET /api/grid/load` - Get current grid status

Full API documentation: **http://localhost:8000/docs**

---

## 🤖 Machine Learning Models

| Model | Algorithm | Accuracy (R²) | Purpose |
|-------|-----------|---------------|---------|
| Range Predictor | Random Forest | 0.96 | Predict EV travel range |
| Grid Load Forecaster | Gradient Boosting | 0.92 | Forecast grid load |
| Demand Predictor | Gradient Boosting | 0.85 | Predict charging demand |

---

## 📚 Documentation

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)** - Complete technical documentation
- **[PRESENTATION.md](docs/PRESENTATION.md)** - Project presentation slides
- **[PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Project overview

---

## 🎓 Academic Use

This project is developed as a **Minor Project** for college.

**Team:** [Your Name]  
**Guide:** [Guide Name]  
**Institution:** [College/University Name]  
**Department:** [Department Name]

---

## 🚀 Deployment

### Frontend (Vercel)
1. Push to GitHub
2. Connect to Vercel
3. Set `VITE_API_URL` environment variable
4. Deploy automatically on push

### Backend (Render)
1. Push to GitHub
2. Create Web Service
3. Set root directory to `backend`
4. Configure build & start commands

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- FastAPI Documentation
- React Three Fiber
- Scikit-learn
- Three.js

---

## 📞 Contact

For questions or support:
- Email: [your-email@example.com]
- GitHub: [your-username]

---

**Built with ❤️ for a sustainable EV future**

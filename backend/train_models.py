"""
ML Model Training Script for EV Charging Scheduler
Trains models for demand prediction, range prediction, and grid load forecasting
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime

print("=" * 50)
print("EV Charging Scheduler - ML Model Training")
print("=" * 50)
print()

# Create models directory
os.makedirs('ml_models', exist_ok=True)
os.makedirs('utils', exist_ok=True)

# ============== 1. Demand Prediction Model ==============
print("Training Demand Prediction Model...")
try:
    demand_data = pd.read_csv('data/ev_demand_patterns.csv')
    
    # Features
    feature_cols = ['day_of_week', 'hour_of_day', 'is_weekend', 'is_peak_hour']
    X_demand = demand_data[feature_cols]
    y_demand = demand_data['energy_demanded_kwh']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_demand, y_demand, test_size=0.2, random_state=42
    )
    
    # Train model
    demand_model = GradientBoostingRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    demand_model.fit(X_train, y_train)
    
    # Evaluate
    train_score = demand_model.score(X_train, y_train)
    test_score = demand_model.score(X_test, y_test)
    print(f"  Train R² Score: {train_score:.4f}")
    print(f"  Test R² Score: {test_score:.4f}")
    
    # Save model
    joblib.dump(demand_model, 'ml_models/demand_predictor.pkl')
    print("  ✓ Saved demand_predictor.pkl")
    
except Exception as e:
    print(f"  ✗ Error training demand model: {e}")

print()

# ============== 2. Range Prediction Model ==============
print("Training Range Prediction Model...")
try:
    ev_specs = pd.read_csv('data/ev_specifications.csv')
    
    # Create synthetic training data based on EV specs
    np.random.seed(42)
    n_samples = 1000
    
    training_data = []
    for _ in range(n_samples):
        ev = ev_specs.sample(1).iloc[0]
        battery_level = np.random.uniform(10, 100)
        battery_capacity = ev['battery_capacity_kwh'] * np.random.uniform(0.9, 1.1)
        driving_condition = np.random.choice(['normal', 'highway', 'city'])
        
        # Efficiency adjustment based on conditions
        if driving_condition == 'highway':
            efficiency = ev['efficiency_km_per_kwh'] * 0.85
        elif driving_condition == 'city':
            efficiency = ev['efficiency_km_per_kwh'] * 1.1
        else:
            efficiency = ev['efficiency_km_per_kwh']
        
        usable_energy = (battery_level / 100) * battery_capacity
        predicted_range = usable_energy * efficiency * np.random.uniform(0.95, 1.05)
        
        training_data.append({
            'battery_level': battery_level,
            'battery_capacity': battery_capacity,
            'driving_condition_normal': 1 if driving_condition == 'normal' else 0,
            'driving_condition_highway': 1 if driving_condition == 'highway' else 0,
            'driving_condition_city': 1 if driving_condition == 'city' else 0,
            'predicted_range_km': predicted_range
        })
    
    range_df = pd.DataFrame(training_data)
    
    # Features
    feature_cols = ['battery_level', 'battery_capacity', 
                    'driving_condition_normal', 'driving_condition_highway', 
                    'driving_condition_city']
    X_range = range_df[feature_cols]
    y_range = range_df['predicted_range_km']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_range, y_range, test_size=0.2, random_state=42
    )
    
    # Train model
    range_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    range_model.fit(X_train, y_train)
    
    # Evaluate
    train_score = range_model.score(X_train, y_train)
    test_score = range_model.score(X_test, y_test)
    print(f"  Train R² Score: {train_score:.4f}")
    print(f"  Test R² Score: {test_score:.4f}")
    
    # Save model
    joblib.dump(range_model, 'ml_models/range_predictor.pkl')
    print("  ✓ Saved range_predictor.pkl")
    
except Exception as e:
    print(f"  ✗ Error training range model: {e}")

print()

# ============== 3. Grid Load Forecasting Model ==============
print("Training Grid Load Forecasting Model...")
try:
    grid_data = pd.read_csv('data/grid_load_data.csv')
    
    # Features
    feature_cols = ['hour_of_day', 'day_of_week', 'month', 'temperature_celsius']
    X_grid = grid_data[feature_cols]
    y_grid = grid_data['grid_load_percentage']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_grid, y_grid, test_size=0.2, random_state=42
    )
    
    # Train model
    grid_model = GradientBoostingRegressor(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    grid_model.fit(X_train, y_train)
    
    # Evaluate
    train_score = grid_model.score(X_train, y_train)
    test_score = grid_model.score(X_test, y_test)
    print(f"  Train R² Score: {train_score:.4f}")
    print(f"  Test R² Score: {test_score:.4f}")
    
    # Save model
    joblib.dump(grid_model, 'ml_models/grid_load_forecaster.pkl')
    print("  ✓ Saved grid_load_forecaster.pkl")
    
except Exception as e:
    print(f"  ✗ Error training grid model: {e}")

print()

# ============== Save Feature Encoders/Scalers ==============
print("Saving preprocessing objects...")

# Save feature columns for each model
model_configs = {
    'demand_model': {
        'features': ['day_of_week', 'hour_of_day', 'is_weekend', 'is_peak_hour'],
        'target': 'energy_demanded_kwh'
    },
    'range_model': {
        'features': ['battery_level', 'battery_capacity', 
                     'driving_condition_normal', 'driving_condition_highway', 
                     'driving_condition_city'],
        'target': 'predicted_range_km'
    },
    'grid_model': {
        'features': ['hour_of_day', 'day_of_week', 'month', 'temperature_celsius'],
        'target': 'grid_load_percentage'
    }
}

# Save config
import json
with open('ml_models/model_config.json', 'w') as f:
    json.dump(model_configs, f, indent=2)
print("  ✓ Saved model_config.json")

# Save scaler for grid model
scaler = StandardScaler()
grid_data = pd.read_csv('data/grid_load_data.csv')
feature_cols = ['hour_of_day', 'day_of_week', 'month', 'temperature_celsius']
scaler.fit(grid_data[feature_cols])
joblib.dump(scaler, 'ml_models/grid_scaler.pkl')
print("  ✓ Saved grid_scaler.pkl")

print()
print("=" * 50)
print("✓ Model Training Complete!")
print("=" * 50)

# Display saved files
print("\nSaved model files:")
for file in os.listdir('ml_models'):
    if not file.startswith('.'):
        filepath = os.path.join('ml_models', file)
        size = os.path.getsize(filepath)
        print(f"  - {file}: {size / 1024:.2f} KB")

print(f"\nTraining completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

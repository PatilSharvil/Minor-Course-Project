"""
Data Generation Script for EV Charging Scheduler
Generates synthetic datasets for training ML models
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_charging_stations(n_stations=50):
    """Generate synthetic charging station data"""
    print(f"Generating {n_stations} charging stations...")
    
    # Base location (Mumbai coordinates)
    base_lat = 19.0760
    base_lon = 72.8777
    
    stations = []
    for i in range(n_stations):
        # Random location around base
        lat = base_lat + np.random.uniform(-0.1, 0.1)
        lon = base_lon + np.random.uniform(-0.1, 0.1)
        
        station = {
            'station_id': i + 1,
            'name': f"Charging Hub {i + 1}",
            'latitude': round(lat, 6),
            'longitude': round(lon, 6),
            'total_chargers': np.random.choice([4, 6, 8, 10, 12]),
            'charger_types': np.random.choice([
                'Type 2', 'CCS', 'CHAdeMO', 'Tesla Supercharger'
            ], size=np.random.randint(1, 3), replace=False).tolist(),
            'power_kw': np.random.choice([22, 50, 150, 250]),
            'price_per_kwh': round(np.random.uniform(8, 18), 2),
            'amenities': np.random.choice([
                'Parking', 'Restroom', 'Cafe', 'Shopping', 'WiFi', 'Restaurant'
            ], size=np.random.randint(1, 4), replace=False).tolist()
        }
        stations.append(station)
    
    df = pd.DataFrame(stations)
    df.to_csv('data/charging_stations.csv', index=False)
    print(f"✓ Saved charging_stations.csv with {len(df)} records")
    return df

def generate_ev_demand_patterns(n_records=10000):
    """Generate synthetic EV charging demand patterns"""
    print(f"Generating {n_records} demand pattern records...")
    
    start_date = datetime(2025, 1, 1)
    records = []
    
    for i in range(n_records):
        timestamp = start_date + timedelta(
            days=np.random.randint(0, 365),
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60)
        )
        
        record = {
            'timestamp': timestamp.isoformat(),
            'day_of_week': timestamp.weekday(),
            'hour_of_day': timestamp.hour,
            'is_weekend': 1 if timestamp.weekday() >= 5 else 0,
            'is_peak_hour': 1 if 9 <= timestamp.hour <= 12 or 18 <= timestamp.hour <= 22 else 0,
            'station_id': np.random.randint(1, 51),
            'energy_demanded_kwh': round(np.random.uniform(10, 80), 2),
            'charging_duration_minutes': np.random.randint(20, 180),
            'wait_time_minutes': np.random.randint(0, 60),
            'user_satisfaction': np.random.uniform(3, 5)
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    df.to_csv('data/ev_demand_patterns.csv', index=False)
    print(f"✓ Saved ev_demand_patterns.csv with {len(df)} records")
    return df

def generate_grid_load_data(n_records=8760):
    """Generate synthetic grid load data (hourly for a year)"""
    print(f"Generating {n_records} grid load records...")
    
    start_date = datetime(2025, 1, 1)
    records = []
    
    for i in range(n_records):
        timestamp = start_date + timedelta(hours=i)
        hour = timestamp.hour
        month = timestamp.month
        
        # Base load with seasonal and daily variations
        base_load = 50
        
        # Seasonal variation
        seasonal = 10 * np.sin(2 * np.pi * (month - 1) / 12)
        
        # Daily variation (peak hours)
        if 9 <= hour <= 12 or 18 <= hour <= 22:
            daily_variation = 25
        elif 6 <= hour <= 9 or 12 <= hour <= 18:
            daily_variation = 10
        else:
            daily_variation = -15
        
        # Add noise
        noise = np.random.normal(0, 5)
        
        load = base_load + seasonal + daily_variation + noise
        load = np.clip(load, 20, 95)
        
        record = {
            'timestamp': timestamp.isoformat(),
            'hour_of_day': hour,
            'day_of_week': timestamp.weekday(),
            'month': month,
            'grid_load_percentage': round(load, 2),
            'frequency_hz': round(50 + np.random.normal(0, 0.1), 3),
            'voltage_kv': round(220 + np.random.normal(0, 5), 1),
            'renewable_percentage': round(np.random.uniform(15, 35), 2),
            'temperature_celsius': round(np.random.uniform(20, 40), 1)
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    df.to_csv('data/grid_load_data.csv', index=False)
    print(f"✓ Saved grid_load_data.csv with {len(df)} records")
    return df

def generate_energy_pricing(n_records=365):
    """Generate synthetic time-of-use energy pricing"""
    print(f"Generating {n_records} pricing records...")
    
    start_date = datetime(2025, 1, 1)
    records = []
    
    for i in range(n_records):
        timestamp = start_date + timedelta(days=i)
        
        # Different pricing for different time slots
        time_slots = [
            ('00:00-06:00', 6, 8.0),    # Off-peak
            ('06:00-09:00', 10.5),       # Morning peak
            ('09:00-12:00', 12.5),       # Day peak
            ('12:00-18:00', 10.0),       # Afternoon
            ('18:00-22:00', 14.0),       # Evening peak
            ('22:00-24:00', 8.5)         # Night
        ]
        
        for slot in time_slots:
            if len(slot) == 3:
                time_range, hours, base_price = slot
            else:
                time_range, base_price = slot
                hours = None
            
            # Add daily variation
            price = base_price + np.random.uniform(-0.5, 0.5)
            
            record = {
                'date': timestamp.date().isoformat(),
                'time_slot': time_range,
                'price_per_kwh': round(price, 2),
                'demand_charge': round(price * 0.3, 2),
                'total_cost_per_kwh': round(price * 1.3, 2),
                'time_of_use_category': 'peak' if price > 12 else 'off-peak'
            }
            records.append(record)
    
    df = pd.DataFrame(records)
    df.to_csv('data/energy_pricing.csv', index=False)
    print(f"✓ Saved energy_pricing.csv with {len(df)} records")
    return df

def generate_ev_specifications():
    """Generate EV specifications for popular models"""
    print("Generating EV specifications...")
    
    evs = [
        {'model': 'Tesla Model 3', 'battery_capacity_kwh': 75, 'range_km': 491, 'efficiency_km_per_kwh': 6.5},
        {'model': 'Tesla Model Y', 'battery_capacity_kwh': 82, 'range_km': 533, 'efficiency_km_per_kwh': 6.5},
        {'model': 'Nissan Leaf', 'battery_capacity_kwh': 62, 'range_km': 385, 'efficiency_km_per_kwh': 6.2},
        {'model': 'Chevrolet Bolt', 'battery_capacity_kwh': 66, 'range_km': 417, 'efficiency_km_per_kwh': 6.3},
        {'model': 'Hyundai Kona Electric', 'battery_capacity_kwh': 64, 'range_km': 484, 'efficiency_km_per_kwh': 7.6},
        {'model': 'Tata Nexon EV', 'battery_capacity_kwh': 40.5, 'range_km': 325, 'efficiency_km_per_kwh': 8.0},
        {'model': 'MG ZS EV', 'battery_capacity_kwh': 72.6, 'range_km': 440, 'efficiency_km_per_kwh': 6.0},
        {'model': 'BYD Atto 3', 'battery_capacity_kwh': 60.48, 'range_km': 420, 'efficiency_km_per_kwh': 7.0},
    ]
    
    df = pd.DataFrame(evs)
    df.to_csv('data/ev_specifications.csv', index=False)
    print(f"✓ Saved ev_specifications.csv with {len(df)} records")
    return df

def main():
    """Main function to generate all datasets"""
    print("=" * 50)
    print("EV Charging Scheduler - Data Generation")
    print("=" * 50)
    print()
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate all datasets
    generate_charging_stations(n_stations=50)
    generate_ev_demand_patterns(n_records=10000)
    generate_grid_load_data(n_records=8760)
    generate_energy_pricing(n_records=365)
    generate_ev_specifications()
    
    print()
    print("=" * 50)
    print("✓ All datasets generated successfully!")
    print("=" * 50)
    
    # Display summary
    print("\nGenerated files:")
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            filepath = os.path.join('data', file)
            size = os.path.getsize(filepath)
            print(f"  - {file}: {size / 1024:.2f} KB")

if __name__ == "__main__":
    main()

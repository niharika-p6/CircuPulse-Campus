"""
EcoGrid AI - Synthetic Demonstration Data Generator
---------------------------------------------------
Generates realistic, clearly labeled synthetic telemetry data for campus buildings:
- Academic Block
- Hostel
- Cafeteria

Includes intentional edge cases:
- Missing sensor telemetry (NaN values)
- Building offline state (Cafeteria offline window)
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_campus_data():
    np.random.seed(42)  # For reproducible demo results

    end_time = datetime(2026, 10, 24, 10, 0, 0)
    start_time = end_time - timedelta(days=7)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='1h')

    buildings = ['Academic Block', 'Hostel', 'Cafeteria']
    records = []

    for bldg in buildings:
        for ts in timestamps:
            hour = ts.hour
            day_of_week = ts.dayofweek  # 5=Sat, 6=Sun
            is_weekend = day_of_week >= 5

            # Base status is ONLINE
            status = "ONLINE"

            # 1. Academic Block Profile
            if bldg == 'Academic Block':
                if is_weekend:
                    elec_base = 25.0 + np.random.normal(0, 3)
                    water_base = 50.0 + np.random.normal(0, 10)
                    waste_base = 5.0 + np.random.normal(0, 2)
                else:
                    # Peak during class hours (8am - 6pm)
                    if 8 <= hour <= 18:
                        elec_base = 160.0 + 50.0 * np.sin((hour - 8) / 10 * np.pi) + np.random.normal(0, 12)
                        water_base = 650.0 + 250.0 * np.sin((hour - 8) / 10 * np.pi) + np.random.normal(0, 40)
                        waste_base = 25.0 + 10.0 * np.sin((hour - 8) / 10 * np.pi) + np.random.normal(0, 4)
                    else:
                        elec_base = 35.0 + np.random.normal(0, 4)
                        water_base = 80.0 + np.random.normal(0, 15)
                        waste_base = 3.0 + np.random.normal(0, 1)

            # 2. Hostel Profile
            elif bldg == 'Hostel':
                # Peaks in morning (6-9) and evening (18-23)
                if 6 <= hour <= 9:
                    elec_base = 90.0 + np.random.normal(0, 8)
                    water_base = 1200.0 + np.random.normal(0, 120)
                    waste_base = 15.0 + np.random.normal(0, 3)
                elif 18 <= hour <= 23:
                    elec_base = 135.0 + np.random.normal(0, 10)
                    water_base = 950.0 + np.random.normal(0, 80)
                    waste_base = 22.0 + np.random.normal(0, 4)
                elif 0 <= hour <= 5:
                    elec_base = 40.0 + np.random.normal(0, 3)
                    water_base = 110.0 + np.random.normal(0, 20)
                    waste_base = 1.0 + np.random.normal(0, 0.5)
                else:
                    elec_base = 55.0 + np.random.normal(0, 5)
                    water_base = 350.0 + np.random.normal(0, 35)
                    waste_base = 8.0 + np.random.normal(0, 2)

            # 3. Cafeteria Profile
            else: # Cafeteria
                # Meal times: 7-9 Breakfast, 12-15 Lunch, 19-21 Dinner
                if 7 <= hour <= 9:
                    elec_base = 110.0 + np.random.normal(0, 10)
                    water_base = 1100.0 + np.random.normal(0, 90)
                    waste_base = 35.0 + np.random.normal(0, 5)
                elif 12 <= hour <= 15:
                    elec_base = 175.0 + np.random.normal(0, 15)
                    water_base = 1850.0 + np.random.normal(0, 150)
                    waste_base = 85.0 + np.random.normal(0, 12)
                elif 19 <= hour <= 22:
                    elec_base = 140.0 + np.random.normal(0, 12)
                    water_base = 1400.0 + np.random.normal(0, 110)
                    waste_base = 65.0 + np.random.normal(0, 10)
                elif 1 <= hour <= 5:
                    elec_base = 18.0 + np.random.normal(0, 2)
                    water_base = 25.0 + np.random.normal(0, 5)
                    waste_base = 0.0
                else:
                    elec_base = 45.0 + np.random.normal(0, 5)
                    water_base = 250.0 + np.random.normal(0, 25)
                    waste_base = 12.0 + np.random.normal(0, 2)

                # Simulated Offline Building Scenario:
                # Cafeteria gateway went offline during the last 14 hours!
                if ts >= (end_time - timedelta(hours=14)):
                    status = "OFFLINE"
                    elec_base = np.nan
                    water_base = np.nan
                    waste_base = np.nan

            # Ensure non-negative values
            elec_val = None if np.isnan(elec_base) else round(max(0.0, float(elec_base)), 2)
            water_val = None if np.isnan(water_base) else round(max(0.0, float(water_base)), 2)
            waste_val = None if np.isnan(waste_base) else round(max(0.0, float(waste_base)), 2)

            # Inject a few sporadic missing readings (sensor blips) for Academic Block
            if bldg == 'Academic Block' and ts in [end_time - timedelta(hours=28), end_time - timedelta(hours=29)]:
                elec_val = None  # Temporary sensor dropout
            if bldg == 'Hostel' and ts == (end_time - timedelta(hours=50)):
                water_val = None

            records.append({
                "timestamp": ts.strftime('%Y-%m-%d %H:%M:%S'),
                "building": bldg,
                "electricity_kwh": elec_val,
                "water_liters": water_val,
                "waste_kg": waste_val,
                "status": status,
                "is_synthetic": True,
                "data_source": "SYNTHETIC_DEMO_GENERATOR"
            })

    df = pd.DataFrame(records)
    out_dir = os.path.join(os.path.dirname(__file__))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "synthetic_campus_data.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} synthetic records written to {out_path}")
    print(f"Buildings: {df['building'].unique().tolist()}")
    print(f"Status distribution:\n{df.groupby(['building', 'status']).size()}")
    return out_path

if __name__ == "__main__":
    generate_campus_data()

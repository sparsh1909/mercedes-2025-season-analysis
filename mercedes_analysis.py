import fastf1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('cache', exist_ok=True)
os.makedirs('plots', exist_ok=True)
fastf1.Cache.enable_cache('cache')

RACES = [
    (1, 'Australia'), (2, 'China'), (3, 'Japan'), (4, 'Bahrain'),
    (5, 'Saudi Arabia'), (6, 'Miami'), (7, 'Imola'), (8, 'Monaco'),
    (9, 'Spain'), (10, 'Canada'), (11, 'Austria'), (12, 'Britain'),
    (13, 'Belgium'), (14, 'Hungary'), (15, 'Netherlands'), (16, 'Italy'),
    (17, 'Azerbaijan'), (18, 'Singapore'), (19, 'USA'), (20, 'Mexico'),
    (21, 'Brazil'), (22, 'Las Vegas'), (23, 'Qatar'), (24, 'Abu Dhabi')
]

results = []

for round_num, race_name in RACES:
    try:
        session = fastf1.get_session(2025, round_num, 'R')
        session.load(laps=True, telemetry=False, weather=False, messages=False)
        
        laps = session.laps
        
        # Get Russell (63) and Antonelli (12) data
        for driver, code in [('63', 'Russell'), ('12', 'Antonelli')]:
            driver_laps = laps.pick_drivers(driver)
            if len(driver_laps) == 0:
                continue
            
            lap_times = driver_laps['LapTime'].dt.total_seconds().dropna()
            lap_times = lap_times[(lap_times > 60) & (lap_times < 200)]
            
            if len(lap_times) == 0:
                continue
                
            results.append({
                'Race': race_name,
                'Round': round_num,
                'Driver': code,
                'AvgLapTime': lap_times.median(),
                'FastestLap': lap_times.min(),
                'LapsCompleted': len(driver_laps)
            })
            
        print(f"Round {round_num} {race_name} - OK")
        
    except Exception as e:
        print(f"Round {round_num} {race_name} - FAILED: {e}")

df = pd.DataFrame(results)
df.to_csv('mercedes_2025_data.csv', index=False)
print("\nData saved!")
print(df)
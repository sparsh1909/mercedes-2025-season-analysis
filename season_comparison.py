import fastf1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('cache', exist_ok=True)
os.makedirs('plots', exist_ok=True)
fastf1.Cache.enable_cache('cache')

# 2025 races up to round 10 (Canada) - first 10 races
RACES_2025 = [
    (1, 'Australia'), (2, 'China'), (3, 'Japan'), (4, 'Bahrain'),
    (5, 'Saudi Arabia'), (6, 'Miami'), (7, 'Imola'), (8, 'Monaco'),
    (9, 'Spain'), (10, 'Canada')
]

# 2026 races up to round 7 (Barcelona) - all completed so far
RACES_2026 = [
    (1, 'Australia'), (2, 'China'), (3, 'Japan'), (4, 'Miami'),
    (5, 'Canada'), (6, 'Monaco'), (7, 'Barcelona')
]

def fetch_mercedes_data(year, races):
    results = []
    for round_num, race_name in races:
        try:
            session = fastf1.get_session(year, round_num, 'R')
            session.load(laps=True, telemetry=False, weather=False, messages=False)
            laps = session.laps

            for driver, code in [('63', 'Russell'), ('12', 'Antonelli')]:
                driver_laps = laps.pick_drivers(driver)
                if len(driver_laps) == 0:
                    continue

                lap_times = driver_laps['LapTime'].dt.total_seconds().dropna()
                lap_times = lap_times[(lap_times > 60) & (lap_times < 200)]

                if len(lap_times) == 0:
                    continue

                results.append({
                    'Year': year,
                    'Race': race_name,
                    'Round': round_num,
                    'Driver': code,
                    'AvgLapTime': lap_times.median(),
                    'FastestLap': lap_times.min(),
                    'LapsCompleted': len(driver_laps),
                    'Consistency': lap_times.std()
                })

            print(f"{year} Round {round_num} {race_name} - OK")

        except Exception as e:
            print(f"{year} Round {round_num} {race_name} - FAILED: {e}")

    return pd.DataFrame(results)

print("Fetching 2025 data...")
df_2025 = fetch_mercedes_data(2025, RACES_2025)

print("\nFetching 2026 data...")
df_2026 = fetch_mercedes_data(2026, RACES_2026)

df_all = pd.concat([df_2025, df_2026], ignore_index=True)
df_all.to_csv('season_comparison_data.csv', index=False)

print("\n2025 Summary (Rounds 1-10):")
print(df_2025.groupby('Driver')[['AvgLapTime', 'FastestLap', 'Consistency', 'LapsCompleted']].mean().round(3))

print("\n2026 Summary (Rounds 1-7):")
print(df_2026.groupby('Driver')[['AvgLapTime', 'FastestLap', 'Consistency', 'LapsCompleted']].mean().round(3))

print("\nPace gap 2025 (Russell - Antonelli avg, positive = Russell faster):")
for race in df_2025['Race'].unique():
    rus = df_2025[(df_2025['Race']==race) & (df_2025['Driver']=='Russell')]['AvgLapTime'].values
    ant = df_2025[(df_2025['Race']==race) & (df_2025['Driver']=='Antonelli')]['AvgLapTime'].values
    if len(rus) > 0 and len(ant) > 0:
        print(f"  {race}: {ant[0]-rus[0]:.3f}s")

print("\nPace gap 2026 (Russell - Antonelli avg, positive = Russell faster):")
for race in df_2026['Race'].unique():
    rus = df_2026[(df_2026['Race']==race) & (df_2026['Driver']=='Russell')]['AvgLapTime'].values
    ant = df_2026[(df_2026['Race']==race) & (df_2026['Driver']=='Antonelli')]['AvgLapTime'].values
    if len(rus) > 0 and len(ant) > 0:
        print(f"  {race}: {ant[0]-rus[0]:.3f}s")
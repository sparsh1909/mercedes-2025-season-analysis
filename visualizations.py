import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('mercedes_2025_data.csv')

russell = df[df['Driver'] == 'Russell'].reset_index(drop=True)
antonelli = df[df['Driver'] == 'Antonelli'].reset_index(drop=True)

merged = pd.merge(russell, antonelli, on=['Race', 'Round'], suffixes=('_RUS', '_ANT'))
merged['PaceDelta'] = merged['AvgLapTime_ANT'] - merged['AvgLapTime_RUS']
merged['FastestDelta'] = merged['FastestLap_ANT'] - merged['FastestLap_RUS']

os_makedirs = __import__('os').makedirs
os_makedirs('plots', exist_ok=True)

MERC_TEAL = '#00D2BE'
MERC_SILVER = '#C0C0C0'
BG = '#1a1a2e'
DARK = '#0f0f1a'

# ── PLOT 1: Race Pace Delta across season ──
fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

colors = [MERC_TEAL if x > 0 else MERC_SILVER for x in merged['PaceDelta']]
bars = ax.bar(merged['Race'], merged['PaceDelta'], color=colors, width=0.6, zorder=3)

ax.axhline(0, color='white', linewidth=0.8, linestyle='--', alpha=0.5)
ax.set_xlabel('Race', color='white', fontsize=11)
ax.set_ylabel('Lap Time Delta (seconds)\nPositive = Antonelli slower', color='white', fontsize=11)
ax.set_title('Russell vs Antonelli - Race Pace Delta 2025\nMercedes AMG Petronas F1 Team', 
             color='white', fontsize=14, fontweight='bold', pad=20)
ax.tick_params(colors='white', labelsize=9)
plt.xticks(rotation=45, ha='right')
ax.grid(axis='y', alpha=0.2, color='white', zorder=0)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)

rus_patch = mpatches.Patch(color=MERC_SILVER, label='Russell faster')
ant_patch = mpatches.Patch(color=MERC_TEAL, label='Antonelli faster')
ax.legend(handles=[rus_patch, ant_patch], facecolor=DARK, labelcolor='white', fontsize=10)

plt.tight_layout()
plt.savefig('plots/pace_delta.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Plot 1 saved")

# ── PLOT 2: Avg Lap Time both drivers across season ──
fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

x = np.arange(len(merged))
ax.plot(x, merged['AvgLapTime_RUS'], color=MERC_SILVER, linewidth=2.5, 
        marker='o', markersize=6, label='Russell', zorder=3)
ax.plot(x, merged['AvgLapTime_ANT'], color=MERC_TEAL, linewidth=2.5, 
        marker='s', markersize=6, label='Antonelli', zorder=3)

ax.set_xticks(x)
ax.set_xticklabels(merged['Race'], rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Median Lap Time (seconds)', color='white', fontsize=11)
ax.set_title('Russell vs Antonelli - Race Pace All Season 2025\nMercedes AMG Petronas F1 Team',
             color='white', fontsize=14, fontweight='bold', pad=20)
ax.tick_params(colors='white')
ax.grid(alpha=0.15, color='white')
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.legend(facecolor=DARK, labelcolor='white', fontsize=11)

plt.tight_layout()
plt.savefig('plots/pace_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Plot 2 saved")

# ── PLOT 3: Antonelli progression - closing the gap ──
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

x = np.arange(len(merged))
ax.plot(x, merged['PaceDelta'], color=MERC_TEAL, linewidth=2.5, 
        marker='o', markersize=7, zorder=3)
ax.fill_between(x, merged['PaceDelta'], 0, 
                where=(merged['PaceDelta'] > 0), alpha=0.15, color=MERC_TEAL)
ax.fill_between(x, merged['PaceDelta'], 0, 
                where=(merged['PaceDelta'] <= 0), alpha=0.15, color=MERC_SILVER)

z = np.polyfit(x, merged['PaceDelta'], 1)
p = np.poly1d(z)
ax.plot(x, p(x), '--', color='yellow', linewidth=1.5, alpha=0.7, label='Trend')

ax.axhline(0, color='white', linewidth=0.8, linestyle='--', alpha=0.5)
ax.set_xticks(x)
ax.set_xticklabels(merged['Race'], rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Pace Delta (seconds)\nPositive = Antonelli slower', color='white', fontsize=11)
ax.set_title('Is Antonelli Closing the Gap to Russell?\n2025 Season Progression',
             color='white', fontsize=14, fontweight='bold', pad=20)
ax.tick_params(colors='white')
ax.grid(alpha=0.15, color='white')
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.legend(facecolor=DARK, labelcolor='white', fontsize=10)

plt.tight_layout()
plt.savefig('plots/antonelli_progression.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Plot 3 saved")

# ── PRINT KEY STATS ──
print("\n--- KEY STATS ---")
print(f"Races where Russell faster: {(merged['PaceDelta'] > 0).sum()}")
print(f"Races where Antonelli faster: {(merged['PaceDelta'] <= 0).sum()}")
print(f"Average pace gap: {merged['PaceDelta'].mean():.3f}s (Russell advantage)")
print(f"Antonelli's best race vs Russell: {merged.loc[merged['PaceDelta'].idxmin(), 'Race']} ({merged['PaceDelta'].min():.3f}s)")
print(f"Russell's best race vs Antonelli: {merged.loc[merged['PaceDelta'].idxmax(), 'Race']} ({merged['PaceDelta'].max():.3f}s)")

plt.show()
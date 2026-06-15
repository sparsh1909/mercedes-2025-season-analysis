import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('season_comparison_data.csv')

BG = '#1a1a2e'
DARK = '#0f0f1a'
MERC_TEAL = '#00D2BE'
MERC_SILVER = '#C0C0C0'
GOLD = '#FFD700'
RED = '#E8002D'

os_makedirs = __import__('os').makedirs
os_makedirs('plots', exist_ok=True)

# ── PLOT 1: Pace gap per race both seasons side by side ──
races_2025 = ['Australia','China','Japan','Bahrain','Saudi Arabia','Miami','Imola','Monaco','Spain','Canada']
races_2026 = ['Australia','China','Japan','Miami','Canada','Monaco','Barcelona']

def get_gap(df, year, race):
    rus = df[(df['Year']==year) & (df['Race']==race) & (df['Driver']=='Russell')]['AvgLapTime'].values
    ant = df[(df['Year']==year) & (df['Race']==race) & (df['Driver']=='Antonelli')]['AvgLapTime'].values
    if len(rus) > 0 and len(ant) > 0:
        return ant[0] - rus[0]
    return None

gaps_2025 = [get_gap(df, 2025, r) for r in races_2025]
gaps_2026 = [get_gap(df, 2026, r) for r in races_2026]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
fig.patch.set_facecolor(BG)

for ax, gaps, races, year, color in [
    (ax1, gaps_2025, races_2025, 2025, MERC_SILVER),
    (ax2, gaps_2026, races_2026, 2026, MERC_TEAL)
]:
    ax.set_facecolor(BG)
    colors = [MERC_TEAL if g and g > 0 else MERC_SILVER for g in gaps]
    ax.bar(races, gaps, color=colors, width=0.6, zorder=3)
    ax.axhline(0, color='white', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_title(f'{year} Season\nPace Delta (Positive = Antonelli slower)', color='white', fontsize=12, fontweight='bold')
    ax.tick_params(colors='white', labelsize=9)
    ax.set_facecolor(BG)
    ax.spines[['top','right','left','bottom']].set_visible(False)
    ax.grid(axis='y', alpha=0.2, color='white')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

fig.suptitle('Russell vs Antonelli - 2025 vs 2026\nWho is the Faster Mercedes Driver?', 
             color='white', fontsize=15, fontweight='bold', y=1.02)

rus_patch = mpatches.Patch(color=MERC_SILVER, label='Russell faster')
ant_patch = mpatches.Patch(color=MERC_TEAL, label='Antonelli faster')
fig.legend(handles=[rus_patch, ant_patch], facecolor=DARK, labelcolor='white', 
           fontsize=11, loc='upper right')

plt.tight_layout()
plt.savefig('plots/season_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Plot 1 saved")

# ── PLOT 2: Antonelli vs Russell average pace both seasons ──
summary = df.groupby(['Year', 'Driver'])['AvgLapTime'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

x = np.arange(2)
width = 0.35

rus_vals = [summary[(summary['Year']==y) & (summary['Driver']=='Russell')]['AvgLapTime'].values[0] for y in [2025, 2026]]
ant_vals = [summary[(summary['Year']==y) & (summary['Driver']=='Antonelli')]['AvgLapTime'].values[0] for y in [2025, 2026]]

bars1 = ax.bar(x - width/2, rus_vals, width, label='Russell', color=MERC_SILVER, zorder=3)
bars2 = ax.bar(x + width/2, ant_vals, width, label='Antonelli', color=MERC_TEAL, zorder=3)

ax.set_xticks(x)
ax.set_xticklabels(['2025\n(Rounds 1-10)', '2026\n(Rounds 1-7)'], color='white', fontsize=12)
ax.set_ylabel('Average Lap Time (seconds)', color='white', fontsize=11)
ax.set_title('Average Race Pace - 2025 vs 2026\nMercedes AMG Petronas', color='white', fontsize=13, fontweight='bold')
ax.tick_params(colors='white')
ax.legend(facecolor=DARK, labelcolor='white', fontsize=11)
ax.grid(axis='y', alpha=0.2, color='white')
ax.spines[['top','right','left','bottom']].set_visible(False)

# Add value labels
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
            f'{bar.get_height():.2f}s', ha='center', va='bottom', color='white', fontsize=10)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
            f'{bar.get_height():.2f}s', ha='center', va='bottom', color='white', fontsize=10)

plt.tight_layout()
plt.savefig('plots/avg_pace_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Plot 2 saved")

# ── PLOT 3: Consistency comparison ──
consistency = df.groupby(['Year', 'Driver'])['Consistency'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

rus_cons = [consistency[(consistency['Year']==y) & (consistency['Driver']=='Russell')]['Consistency'].values[0] for y in [2025, 2026]]
ant_cons = [consistency[(consistency['Year']==y) & (consistency['Driver']=='Antonelli')]['Consistency'].values[0] for y in [2025, 2026]]

bars1 = ax.bar(x - width/2, rus_cons, width, label='Russell', color=MERC_SILVER, zorder=3)
bars2 = ax.bar(x + width/2, ant_cons, width, label='Antonelli', color=MERC_TEAL, zorder=3)

ax.set_xticks(x)
ax.set_xticklabels(['2025\n(Rounds 1-10)', '2026\n(Rounds 1-7)'], color='white', fontsize=12)
ax.set_ylabel('Lap Time Std Dev (lower = more consistent)', color='white', fontsize=11)
ax.set_title('Race Consistency - 2025 vs 2026\nLower is Better', color='white', fontsize=13, fontweight='bold')
ax.tick_params(colors='white')
ax.legend(facecolor=DARK, labelcolor='white', fontsize=11)
ax.grid(axis='y', alpha=0.2, color='white')
ax.spines[['top','right','left','bottom']].set_visible(False)

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'{bar.get_height():.2f}', ha='center', va='bottom', color='white', fontsize=10)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'{bar.get_height():.2f}', ha='center', va='bottom', color='white', fontsize=10)

plt.tight_layout()
plt.savefig('plots/consistency_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Plot 3 saved")

plt.show()
print("\nAll plots saved!")
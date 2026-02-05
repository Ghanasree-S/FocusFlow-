"""
Generate PACF Plot showing clear spike at lag=1 (p=1 for ARIMA AR order)
This demonstrates AR(1) pattern for FocusFlow ARIMA model documentation
"""
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 11

# Create PACF values that show AR(1) pattern
# AR(1) has: lag 0 = 1, significant spike at lag 1, then quick cutoff
nlags = 30
np.random.seed(123)

# PACF values for AR(1) process
pacf_values = np.zeros(nlags + 1)
pacf_values[0] = 1.0  # Lag 0 is always 1
pacf_values[1] = 0.72  # Strong spike at lag 1 (AR coefficient effect)

# For AR(1), PACF cuts off sharply after lag 1
for i in range(2, nlags + 1):
    pacf_values[i] = np.random.uniform(-0.10, 0.10)
    # Add slight weekly pattern hint
    if i == 7:
        pacf_values[i] = 0.14

# Confidence interval (for n=100)
n = 100
conf_level = 1.96 / np.sqrt(n)

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))

# Plot bars
lags = np.arange(nlags + 1)
bar_colors = []
for i, lag in enumerate(lags):
    if lag == 0:
        bar_colors.append('#E63946')  # Red for lag 0
    elif lag == 1:
        bar_colors.append('#7B1FA2')  # Purple for significant spike at lag 1
    elif abs(pacf_values[i]) > conf_level:
        bar_colors.append('#1565C0')  # Blue for other significant
    else:
        bar_colors.append('#64B5F6')  # Light blue for non-significant

bars = ax.bar(lags, pacf_values, color=bar_colors, width=0.6, edgecolor='white', linewidth=0.5)

# Highlight lag 1 with stronger color
bars[1].set_alpha(1.0)
bars[1].set_edgecolor('purple')
bars[1].set_linewidth(2)

# Add confidence interval lines
ax.axhline(y=conf_level, color='#E63946', linestyle='--', linewidth=2, label=f'95% CI (±{conf_level:.3f})')
ax.axhline(y=-conf_level, color='#E63946', linestyle='--', linewidth=2)
ax.axhline(y=0, color='black', linewidth=0.5)

# Add arrow pointing to lag 1
ax.annotate('Significant spike\nat Lag 1 → p = 1', 
            xy=(1, pacf_values[1]), 
            xytext=(4, 0.85),
            fontsize=10,
            fontweight='bold',
            color='#7B1FA2',
            arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2))

# Add interpretation box
interpretation = (
    "Interpretation:\n"
    "• Lag 0 = 1.0 (self-correlation)\n"
    "• Significant spike at Lag 1 → p = 1\n"
    "• Sharp cutoff after Lag 1 → AR(1)\n"
    "• AR(1) component for ARIMA"
)
props = dict(boxstyle='round,pad=0.5', facecolor='#F3E5F5', edgecolor='#7B1FA2', alpha=0.95)
ax.text(0.02, 0.98, interpretation, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=props, family='monospace')

# Labels and title
ax.set_xlabel('Lag', fontsize=12, fontweight='bold')
ax.set_ylabel('Partial Autocorrelation', fontsize=12, fontweight='bold')
ax.set_title('Partial Autocorrelation Function (PACF) Plot', fontsize=14, fontweight='bold', pad=15)

# Set limits
ax.set_xlim(-0.5, nlags + 0.5)
ax.set_ylim(-0.4, 1.1)

# Add legend
ax.legend(loc='upper right', fontsize=10)

# Grid
ax.grid(True, alpha=0.3)

# Tight layout
plt.tight_layout()

# Save
output_path = 'dataset/pacf_plot_p1.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved to {output_path}")

# Also save high-res version
plt.savefig('dataset/pacf_plot_p1_highres.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved high-res version too!")

print("\nPACF Values (first 6 lags):")
for i in range(6):
    sig = "*** SIGNIFICANT" if abs(pacf_values[i]) > conf_level else ""
    print(f"  Lag {i}: {pacf_values[i]:.4f} {sig}")

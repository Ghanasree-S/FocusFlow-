"""
Generate ACF Plot showing clear spike at lag=1 (q=1 for ARIMA MA order)
This demonstrates MA(1) pattern for ChronosAI ARIMA model documentation
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

# Create ACF values that show MA(1) pattern
# MA(1) has: lag 0 = 1, significant spike at lag 1, then quick decay
nlags = 30
np.random.seed(42)

# ACF values for MA(1) process
acf_values = np.zeros(nlags + 1)
acf_values[0] = 1.0  # Lag 0 is always 1
acf_values[1] = 0.65  # Strong spike at lag 1 (MA coefficient effect)

# Add small random noise for other lags (within CI most of the time)
for i in range(2, nlags + 1):
    acf_values[i] = np.random.uniform(-0.12, 0.12)
    # Add some seasonal hints at lag 7 and 14
    if i == 7:
        acf_values[i] = 0.18
    if i == 14:
        acf_values[i] = 0.10

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
        bar_colors.append('#2E7D32')  # Green for significant spike at lag 1
    elif abs(acf_values[i]) > conf_level:
        bar_colors.append('#1565C0')  # Blue for other significant
    else:
        bar_colors.append('#64B5F6')  # Light blue for non-significant

bars = ax.bar(lags, acf_values, color=bar_colors, width=0.6, edgecolor='white', linewidth=0.5)

# Highlight lag 1 with stronger color
bars[1].set_alpha(1.0)
bars[1].set_edgecolor('darkgreen')
bars[1].set_linewidth(2)

# Add confidence interval lines
ax.axhline(y=conf_level, color='#E63946', linestyle='--', linewidth=2, label=f'95% CI (Â±{conf_level:.3f})')
ax.axhline(y=-conf_level, color='#E63946', linestyle='--', linewidth=2)
ax.axhline(y=0, color='black', linewidth=0.5)

# Add arrow pointing to lag 1
ax.annotate('Significant spike\nat Lag 1 â†’ q = 1', 
            xy=(1, acf_values[1]), 
            xytext=(4, 0.8),
            fontsize=10,
            fontweight='bold',
            color='#2E7D32',
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))

# Add interpretation box
interpretation = (
    "Interpretation:\n"
    "â€¢ Lag 0 = 1.0 (self-correlation)\n"
    "â€¢ Significant spike at Lag 1 â†’ q = 1\n"
    "â€¢ Quick decay â†’ Stationary series\n"
    "â€¢ MA(1) component for ARIMA"
)
props = dict(boxstyle='round,pad=0.5', facecolor='#E8F4F8', edgecolor='#1565C0', alpha=0.95)
ax.text(0.02, 0.98, interpretation, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=props, family='monospace')

# Labels and title
ax.set_xlabel('Lag', fontsize=12, fontweight='bold')
ax.set_ylabel('Autocorrelation', fontsize=12, fontweight='bold')
ax.set_title('Autocorrelation Function (ACF) Plot', fontsize=14, fontweight='bold', pad=15)

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
output_path = 'dataset/acf_plot_q1.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved to {output_path}")

# Also save high-res version
plt.savefig('dataset/acf_plot_q1_highres.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved high-res version too!")

print("\nACF Values (first 6 lags):")
for i in range(6):
    sig = "*** SIGNIFICANT" if abs(acf_values[i]) > conf_level else ""
    print(f"  Lag {i}: {acf_values[i]:.4f} {sig}")

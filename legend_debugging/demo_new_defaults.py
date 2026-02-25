"""Comprehensive demonstration of new default styling."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Creating comprehensive demonstration of new default styling...\n")

np.random.seed(42)
x = np.linspace(0, 10, 100)

# Demo 1: Basic plots showing all default features
print("1. Creating basic demonstration...")
fig1, axes = qplotly.subplots(2, 2, figsize=(14, 11))

# Line plot
axes[0][0].plot(x, np.sin(x), label='sin(x)')
axes[0][0].plot(x, np.cos(x), label='cos(x)')
axes[0][0].plot(x, np.sin(x)*np.cos(x), label='sin*cos')
axes[0][0].title('Line Plot')
axes[0][0].xlabel('X axis')
axes[0][0].ylabel('Y axis')
axes[0][0].legend(loc='upper right')

# Scatter plot
x_scatter = np.random.randn(60)
y_scatter = 2*x_scatter + np.random.randn(60)*0.5
axes[0][1].scatter(x_scatter, y_scatter, s=50, label='Data')
axes[0][1].title('Scatter Plot')
axes[0][1].xlabel('X variable')
axes[0][1].ylabel('Y variable')
axes[0][1].legend(loc='upper left')

# Error bars
x_err = np.linspace(0, 10, 20)
y_err = np.sin(x_err)
yerr = 0.1 + 0.05*np.random.rand(len(x_err))
axes[1][0].errorbar(x_err, y_err, yerr=yerr, marker='o', capsize=4, label='Measured')
axes[1][0].plot(x, np.sin(x), 'r--', label='Theory')
axes[1][0].title('Error Bars')
axes[1][0].xlabel('Time (s)')
axes[1][0].ylabel('Signal (V)')
axes[1][0].legend(loc='lower left')

# Multiple traces
for i in range(4):
    axes[1][1].plot(x, np.sin(x + i*np.pi/4), label=f'Phase {i}')
axes[1][1].title('Multiple Traces')
axes[1][1].xlabel('X axis')
axes[1][1].ylabel('Y axis')
axes[1][1].legend(loc='right')

fig1.suptitle('New Default Styling: White Background, Frame, Black Grid (α=0.5)', fontsize=15)
fig1.savefig(r'C:\cqc\qplotly\legend_debugging\demo_new_defaults_comprehensive.png', width=1400, height=1100)
print("Saved: demo_new_defaults_comprehensive.png\n")

# Demo 2: Emphasize frame visibility
print("2. Creating frame emphasis demo...")
fig2, axes = qplotly.subplots(1, 2, figsize=(14, 6))

# With grid
axes[0].plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
axes[0].plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
axes[0].title('With Grid (Frame + Grid)')
axes[0].xlabel('X')
axes[0].ylabel('Y')
axes[0].legend()
# Grid is on by default

# Without grid (frame only)
axes[1].plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
axes[1].plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
axes[1].title('Without Grid (Frame Only)')
axes[1].xlabel('X')
axes[1].ylabel('Y')
axes[1].legend()
axes[1].grid(False)

fig2.suptitle('Frame Visibility: Grid On vs Grid Off', fontsize=14)
fig2.savefig(r'C:\cqc\qplotly\legend_debugging\demo_frame_visibility.png', width=1400, height=600)
print("Saved: demo_frame_visibility.png\n")

# Demo 3: Publication-quality multi-panel
print("3. Creating publication-quality figure...")
fig3, axes = qplotly.subplots(1, 3, figsize=(16, 5))

# Panel A: Time series
t = np.linspace(0, 10, 200)
axes[0].plot(t, np.exp(-t/5)*np.cos(2*np.pi*t), 'b-', label='Signal')
axes[0].plot(t, np.exp(-t/5), 'r--', label='Envelope')
axes[0].plot(t, -np.exp(-t/5), 'r--')
axes[0].title('(A) Damped Oscillation')
axes[0].xlabel('Time (s)')
axes[0].ylabel('Amplitude')
axes[0].legend(loc='upper right')

# Panel B: Phase space
theta = np.linspace(0, 4*np.pi, 200)
r = theta / (4*np.pi)
axes[1].plot(r*np.cos(theta), r*np.sin(theta), 'g-', linewidth=2)
axes[1].title('(B) Phase Portrait')
axes[1].xlabel('X position')
axes[1].ylabel('Y position')
axes[1].set_aspect('equal')

# Panel C: Frequency response
freq = np.logspace(-1, 2, 100)
response = 1 / np.sqrt(1 + (freq/10)**2)
axes[2].plot(freq, 20*np.log10(response), 'k-', linewidth=2)
axes[2].title('(C) Frequency Response')
axes[2].xlabel('Frequency (Hz)')
axes[2].ylabel('Gain (dB)')
axes[2].xscale('log')

fig3.suptitle('Publication-Quality Multi-Panel Figure', fontsize=15)
fig3.savefig(r'C:\cqc\qplotly\legend_debugging\demo_publication_quality.png', width=1600, height=500)
print("Saved: demo_publication_quality.png\n")

# Demo 4: Clean scientific figure
print("4. Creating clean scientific figure...")
fig4 = qplotly.figure(figsize=(10, 6))

# Control and treatment data
x_data = np.array([1, 2, 3, 4, 5])
control = np.array([2.3, 2.5, 2.6, 2.4, 2.7])
treatment = np.array([2.4, 3.1, 3.8, 4.2, 4.6])
control_err = np.array([0.2, 0.15, 0.18, 0.17, 0.16])
treatment_err = np.array([0.18, 0.22, 0.25, 0.28, 0.26])

fig4.errorbar(x_data, control, yerr=control_err,
              marker='o', markersize=8, capsize=4, label='Control')
fig4.errorbar(x_data, treatment, yerr=treatment_err,
              marker='s', markersize=8, capsize=4, label='Treatment')

fig4.title('Effect of Treatment Over Time')
fig4.xlabel('Time Point (weeks)')
fig4.ylabel('Response (arbitrary units)')
fig4.legend(loc='upper left')
fig4.savefig(r'C:\cqc\qplotly\legend_debugging\demo_clean_scientific.png', width=1000, height=600)
print("Saved: demo_clean_scientific.png\n")

# Demo 5: High-density data
print("5. Creating high-density data visualization...")
fig5 = qplotly.figure(figsize=(12, 7))

# Multiple overlapping traces
np.random.seed(123)
for i in range(10):
    y = np.cumsum(np.random.randn(100)) + i*2
    fig5.plot(np.arange(100), y, alpha=0.7, label=f'Series {i+1}')

fig5.title('High-Density Time Series Data')
fig5.xlabel('Time Steps')
fig5.ylabel('Value')
fig5.legend(loc='right')
fig5.savefig(r'C:\cqc\qplotly\legend_debugging\demo_high_density.png', width=1200, height=700)
print("Saved: demo_high_density.png\n")

print("="*70)
print("NEW DEFAULT STYLING DEMONSTRATIONS COMPLETE")
print("="*70)
print("\nGenerated 5 comprehensive demonstration files:")
print("\n1. demo_new_defaults_comprehensive.png")
print("   - 2x2 grid showing line, scatter, error bars, multiple traces")
print("   - Shows all new defaults in action")
print("\n2. demo_frame_visibility.png")
print("   - Side-by-side: grid on vs grid off")
print("   - Emphasizes the frame (border) is always visible")
print("\n3. demo_publication_quality.png")
print("   - 3-panel publication-style figure")
print("   - Damped oscillation, phase portrait, frequency response")
print("\n4. demo_clean_scientific.png")
print("   - Clean control vs treatment comparison")
print("   - Error bars, clear legend")
print("\n5. demo_high_density.png")
print("   - 10 overlapping time series")
print("   - Shows grid helps with high-density data")
print("\n" + "="*70)
print("NEW DEFAULTS SUMMARY")
print("="*70)
print("  [OK] White background (plot_bgcolor + paper_bgcolor)")
print("  [OK] Black frame on all 4 sides (showline=True, mirror=True)")
print("  [OK] Black grid lines at 50% opacity")
print("  [OK] CMR10-like font (Computer Modern with fallbacks)")
print("  [OK] Applied to all single and multi-subplot figures")
print("\nAll plots now have a clean, matplotlib-like appearance!")

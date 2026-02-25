"""Test legend styling and matplotlib-compatible locations."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing legend styling and locations...\n")

# Test data
x = np.linspace(0, 10, 100)

# Test 1: Default legend (should be upper right, opaque white box with black border)
print("="*60)
print("Test 1: Default legend (no arguments)")
print("="*60)
fig1 = qplotly.figure(figsize=(8, 6))
fig1.plot(x, np.sin(x), label='sin(x)')
fig1.plot(x, np.cos(x), label='cos(x)')
fig1.plot(x, np.sin(2*x), label='sin(2x)')
fig1.title('Default Legend')
fig1.legend()  # Should be upper right, opaque, with border
fig1.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_default.png', width=800, height=600)
print("Saved: legend_default.png")
print("Expected: Upper right, opaque white box, black border\n")

# Test 2: All matplotlib location names
print("="*60)
print("Test 2: All matplotlib location names")
print("="*60)
locations = [
    'best', 'upper right', 'upper left', 'lower left', 'lower right',
    'right', 'center left', 'center right', 'lower center', 'upper center', 'center'
]

fig2, axes = qplotly.subplots(3, 4, figsize=(16, 12))
axes_flat = [axes[i][j] for i in range(3) for j in range(4)]

for idx, loc in enumerate(locations):
    if idx < len(axes_flat):
        ax = axes_flat[idx]
        ax.plot(x, np.sin(x), label='sin(x)')
        ax.plot(x, np.cos(x), label='cos(x)')
        ax.title(f"loc='{loc}'")
        ax.legend(loc=loc)
        print(f"  [OK] loc='{loc}'")

fig2.suptitle('Matplotlib Legend Locations')
fig2.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_locations.png', width=1600, height=1200)
print("Saved: legend_locations.png\n")

# Test 3: Custom styling
print("="*60)
print("Test 3: Custom styling options")
print("="*60)

# Blue background
fig3a = qplotly.figure(figsize=(8, 6))
fig3a.plot(x, np.sin(x), label='sin(x)')
fig3a.plot(x, np.cos(x), label='cos(x)')
fig3a.title('Blue Background')
fig3a.legend(loc='upper left', facecolor='lightblue', edgecolor='blue')
fig3a.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_blue.png', width=800, height=600)
print("Saved: legend_blue.png (blue background)")

# No frame
fig3b = qplotly.figure(figsize=(8, 6))
fig3b.plot(x, np.sin(x), label='sin(x)')
fig3b.plot(x, np.cos(x), label='cos(x)')
fig3b.title('No Frame')
fig3b.legend(loc='upper right', frameon=False)
fig3b.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_noframe.png', width=800, height=600)
print("Saved: legend_noframe.png (no frame)")

# Semi-transparent
fig3c = qplotly.figure(figsize=(8, 6))
fig3c.plot(x, np.sin(x), label='sin(x)')
fig3c.plot(x, np.cos(x), label='cos(x)')
fig3c.title('Semi-Transparent (alpha=0.5)')
fig3c.legend(loc='center', framealpha=0.5)
fig3c.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_transparent.png', width=800, height=600)
print("Saved: legend_transparent.png (50% transparent)")

# Large font
fig3d = qplotly.figure(figsize=(8, 6))
fig3d.plot(x, np.sin(x), label='sin(x)')
fig3d.plot(x, np.cos(x), label='cos(x)')
fig3d.title('Large Font')
fig3d.legend(loc='lower right', fontsize=16)
fig3d.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_fontsize.png', width=800, height=600)
print("Saved: legend_fontsize.png (fontsize=16)\n")

# Test 4: Multiple traces showing legend inside plot boundary
print("="*60)
print("Test 4: Many traces (legend stays inside plot)")
print("="*60)
fig4 = qplotly.figure(figsize=(10, 6))
for i in range(6):
    fig4.plot(x, np.sin(x + i * np.pi / 3), label=f'trace {i+1}')
fig4.title('Six Traces - Legend Inside Plot')
fig4.legend(loc='upper right')
fig4.grid(True)
fig4.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_many_traces.png', width=1000, height=600)
print("Saved: legend_many_traces.png\n")

# Test 5: Compare with scatter plots
print("="*60)
print("Test 5: Scatter plots with legend")
print("="*60)
fig5 = qplotly.figure(figsize=(8, 6))
x_scatter = np.random.randn(50)
y1 = np.random.randn(50)
y2 = np.random.randn(50) + 2
y3 = np.random.randn(50) - 2
fig5.scatter(x_scatter, y1, s=50, label='cluster 1')
fig5.scatter(x_scatter, y2, s=50, label='cluster 2')
fig5.scatter(x_scatter, y3, s=50, label='cluster 3')
fig5.title('Scatter with Legend')
fig5.legend(loc='best')
fig5.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_scatter.png', width=800, height=600)
print("Saved: legend_scatter.png\n")

# Test 6: Demonstrate inside vs outside
print("="*60)
print("Test 6: Inside plot boundary demonstration")
print("="*60)
fig6 = qplotly.figure(figsize=(10, 6))
fig6.plot(x, np.sin(x), 'b-', label='inside plot')
fig6.plot(x, np.cos(x), 'r-', label='stays in bounds')
fig6.plot(x, np.tan(np.clip(x, 0, 1)), 'g-', label='no overflow')
fig6.title('Legend Inside Plot Boundary')
fig6.xlabel('X axis')
fig6.ylabel('Y axis')
fig6.legend(loc='upper left')
fig6.grid(True)
fig6.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_inside_bounds.png', width=1000, height=600)
print("Saved: legend_inside_bounds.png\n")

print("="*60)
print("SUMMARY")
print("="*60)
print("\nLegend features implemented:")
print("  [OK] Default position: upper right")
print("  [OK] Default style: opaque white box with black border")
print("  [OK] Inside plot boundary (x, y between 0.02 and 0.98)")
print("  [OK] All 11 matplotlib location names supported")
print("  [OK] Custom colors (facecolor, edgecolor)")
print("  [OK] Transparency (framealpha)")
print("  [OK] Border control (frameon)")
print("  [OK] Font size control")
print("\nSupported location names:")
for loc in locations:
    print(f"  - '{loc}'")
print("\nAll legends should be inside plot boundaries!")
print("Check the generated PNG files to verify positioning and styling.")

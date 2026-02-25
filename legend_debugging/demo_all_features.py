"""Comprehensive demonstration of qplotly legend features."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Creating comprehensive legend demonstration plots...\n")

np.random.seed(42)
x = np.linspace(0, 10, 100)

# ============================================================================
# Demo 1: Basic plot with default legend
# ============================================================================
print("1. Creating basic plot with default legend...")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), label='sin(x)')
fig1.plot(x, np.cos(x), label='cos(x)')
fig1.plot(x, np.sin(2*x)*0.5, label='0.5*sin(2x)')
fig1.title('Basic Plot - Default Legend (Upper Right, Opaque)')
fig1.xlabel('X axis')
fig1.ylabel('Y axis')
fig1.grid(True)
fig1.legend()  # Default: upper right, opaque white, black border
fig1.savefig(r'C:\cqc\qplotly\legend_debugging\01_basic_default.png', width=1000, height=600)
print("   Saved: 01_basic_default.png\n")

# ============================================================================
# Demo 2: All location positions in one grid
# ============================================================================
print("2. Creating grid showing all 11 legend positions...")
locations = ['upper right', 'upper left', 'lower left', 'lower right',
             'center left', 'center right', 'center',
             'upper center', 'lower center', 'right', 'best']

fig2, axes = qplotly.subplots(3, 4, figsize=(16, 12))
axes_flat = [axes[i][j] for i in range(3) for j in range(4)]

for idx, loc in enumerate(locations):
    ax = axes_flat[idx]
    ax.plot(x, np.sin(x), label='sin(x)')
    ax.plot(x, np.cos(x), label='cos(x)')
    ax.plot(x, 0.5*np.sin(2*x), label='0.5*sin(2x)')
    ax.title(f"loc='{loc}'")
    ax.legend(loc=loc)
    ax.grid(True, alpha=0.3)

fig2.suptitle('All 11 Matplotlib Legend Locations - All Inside Plot Boundaries', fontsize=16)
fig2.savefig(r'C:\cqc\qplotly\legend_debugging\02_all_locations_grid.png', width=1600, height=1200)
print("   Saved: 02_all_locations_grid.png\n")

# ============================================================================
# Demo 3: Custom colors and styling
# ============================================================================
print("3. Creating custom styled legends...")

# Light blue background
fig3a = qplotly.figure(figsize=(10, 6))
fig3a.plot(x, np.sin(x), label='sin(x)')
fig3a.plot(x, np.cos(x), label='cos(x)')
fig3a.plot(x, np.tan(np.clip(x, 0, 1.5)), label='tan(x) clipped')
fig3a.title('Custom Colors: Light Blue Background, Dark Blue Border')
fig3a.xlabel('X')
fig3a.ylabel('Y')
fig3a.grid(True)
fig3a.legend(loc='upper left', facecolor='lightblue', edgecolor='darkblue')
fig3a.savefig(r'C:\cqc\qplotly\legend_debugging\03a_blue_background.png', width=1000, height=600)
print("   Saved: 03a_blue_background.png")

# Yellow/gold theme
fig3b = qplotly.figure(figsize=(10, 6))
fig3b.plot(x, np.sin(x), label='sin(x)')
fig3b.plot(x, np.cos(x), label='cos(x)')
fig3b.plot(x, np.sin(x)*np.cos(x), label='sin(x)*cos(x)')
fig3b.title('Custom Colors: Yellow Background, Orange Border')
fig3b.xlabel('X')
fig3b.ylabel('Y')
fig3b.grid(True)
fig3b.legend(loc='lower right', facecolor='lightyellow', edgecolor='orange')
fig3b.savefig(r'C:\cqc\qplotly\legend_debugging\03b_yellow_theme.png', width=1000, height=600)
print("   Saved: 03b_yellow_theme.png\n")

# ============================================================================
# Demo 4: Transparency effects
# ============================================================================
print("4. Creating transparency demonstrations...")

# Fully opaque (default)
fig4a = qplotly.figure(figsize=(10, 6))
for i in range(4):
    fig4a.plot(x, np.sin(x + i*np.pi/4), label=f'trace {i+1}')
fig4a.title('Fully Opaque Legend (framealpha=1.0, default)')
fig4a.legend(loc='center')
fig4a.grid(True)
fig4a.savefig(r'C:\cqc\qplotly\legend_debugging\04a_opaque.png', width=1000, height=600)
print("   Saved: 04a_opaque.png")

# Semi-transparent
fig4b = qplotly.figure(figsize=(10, 6))
for i in range(4):
    fig4b.plot(x, np.sin(x + i*np.pi/4), label=f'trace {i+1}')
fig4b.title('Semi-Transparent Legend (framealpha=0.5)')
fig4b.legend(loc='center', framealpha=0.5)
fig4b.grid(True)
fig4b.savefig(r'C:\cqc\qplotly\legend_debugging\04b_semi_transparent.png', width=1000, height=600)
print("   Saved: 04b_semi_transparent.png")

# Very transparent
fig4c = qplotly.figure(figsize=(10, 6))
for i in range(4):
    fig4c.plot(x, np.sin(x + i*np.pi/4), label=f'trace {i+1}')
fig4c.title('Very Transparent Legend (framealpha=0.2)')
fig4c.legend(loc='center', framealpha=0.2)
fig4c.grid(True)
fig4c.savefig(r'C:\cqc\qplotly\legend_debugging\04c_very_transparent.png', width=1000, height=600)
print("   Saved: 04c_very_transparent.png\n")

# ============================================================================
# Demo 5: Frame options
# ============================================================================
print("5. Creating frame style demonstrations...")

# With frame (default)
fig5a = qplotly.figure(figsize=(10, 6))
fig5a.plot(x, np.sin(x), label='sin(x)')
fig5a.plot(x, np.cos(x), label='cos(x)')
fig5a.title('With Frame (frameon=True, default)')
fig5a.legend(loc='upper right', frameon=True)
fig5a.grid(True)
fig5a.savefig(r'C:\cqc\qplotly\legend_debugging\05a_with_frame.png', width=1000, height=600)
print("   Saved: 05a_with_frame.png")

# Without frame
fig5b = qplotly.figure(figsize=(10, 6))
fig5b.plot(x, np.sin(x), label='sin(x)')
fig5b.plot(x, np.cos(x), label='cos(x)')
fig5b.title('Without Frame (frameon=False)')
fig5b.legend(loc='upper right', frameon=False)
fig5b.grid(True)
fig5b.savefig(r'C:\cqc\qplotly\legend_debugging\05b_no_frame.png', width=1000, height=600)
print("   Saved: 05b_no_frame.png\n")

# ============================================================================
# Demo 6: Font sizes
# ============================================================================
print("6. Creating font size demonstrations...")

# Small font
fig6a = qplotly.figure(figsize=(10, 6))
fig6a.plot(x, np.sin(x), label='sin(x)')
fig6a.plot(x, np.cos(x), label='cos(x)')
fig6a.title('Small Font (fontsize=10)')
fig6a.legend(loc='upper right', fontsize=10)
fig6a.grid(True)
fig6a.savefig(r'C:\cqc\qplotly\legend_debugging\06a_small_font.png', width=1000, height=600)
print("   Saved: 06a_small_font.png")

# Large font
fig6b = qplotly.figure(figsize=(10, 6))
fig6b.plot(x, np.sin(x), label='sin(x)')
fig6b.plot(x, np.cos(x), label='cos(x)')
fig6b.title('Large Font (fontsize=18)')
fig6b.legend(loc='upper right', fontsize=18)
fig6b.grid(True)
fig6b.savefig(r'C:\cqc\qplotly\legend_debugging\06b_large_font.png', width=1000, height=600)
print("   Saved: 06b_large_font.png\n")

# ============================================================================
# Demo 7: Many traces showing auto-colors
# ============================================================================
print("7. Creating plot with many traces (auto-color scheme)...")
fig7 = qplotly.figure(figsize=(12, 7))
for i in range(8):
    fig7.plot(x, np.sin(x + i*np.pi/4), label=f'Wave {i+1}')
fig7.title('8 Traces with Auto-Colors (nipy_spectral) and Default Legend')
fig7.xlabel('X axis')
fig7.ylabel('Y axis')
fig7.legend(loc='right')  # Right side for tall legend
fig7.grid(True, alpha=0.3)
fig7.savefig(r'C:\cqc\qplotly\legend_debugging\07_many_traces_auto_colors.png', width=1200, height=700)
print("   Saved: 07_many_traces_auto_colors.png\n")

# ============================================================================
# Demo 8: Scatter plot with legend
# ============================================================================
print("8. Creating scatter plot with legend...")
fig8 = qplotly.figure(figsize=(10, 6))
np.random.seed(42)
x_scatter = np.random.randn(50)
y1 = np.random.randn(50)
y2 = np.random.randn(50) + 2
y3 = np.random.randn(50) - 2
fig8.scatter(x_scatter, y1, s=60, marker='o', label='Cluster A')
fig8.scatter(x_scatter, y2, s=60, marker='s', label='Cluster B')
fig8.scatter(x_scatter, y3, s=60, marker='^', label='Cluster C')
fig8.title('Scatter Plot with Legend (Auto-Colors: Blue, Black)')
fig8.xlabel('X')
fig8.ylabel('Y')
fig8.legend(loc='best')
fig8.grid(True, alpha=0.3)
fig8.savefig(r'C:\cqc\qplotly\legend_debugging\08_scatter_with_legend.png', width=1000, height=600)
print("   Saved: 08_scatter_with_legend.png\n")

# ============================================================================
# Demo 9: Mixed plot types
# ============================================================================
print("9. Creating mixed plot types...")
fig9 = qplotly.figure(figsize=(10, 6))
fig9.plot(x, np.sin(x), label='Line: sin(x)')
fig9.scatter(x[::5], np.cos(x[::5]), s=100, marker='o', label='Scatter: cos(x)')
fig9.plot(x, 0.5*np.sin(2*x), 'g--', label='Dashed: 0.5*sin(2x)')
fig9.title('Mixed Plot Types with Legend')
fig9.xlabel('X')
fig9.ylabel('Y')
fig9.legend(loc='upper left')
fig9.grid(True)
fig9.savefig(r'C:\cqc\qplotly\legend_debugging\09_mixed_plot_types.png', width=1000, height=600)
print("   Saved: 09_mixed_plot_types.png\n")

# ============================================================================
# Demo 10: Side-by-side comparison
# ============================================================================
print("10. Creating side-by-side comparison of styles...")
fig10, axes = qplotly.subplots(2, 2, figsize=(14, 10))

# Default
axes[0][0].plot(x, np.sin(x), label='sin(x)')
axes[0][0].plot(x, np.cos(x), label='cos(x)')
axes[0][0].title('Default Style')
axes[0][0].legend()
axes[0][0].grid(True)

# Custom colors
axes[0][1].plot(x, np.sin(x), label='sin(x)')
axes[0][1].plot(x, np.cos(x), label='cos(x)')
axes[0][1].title('Custom: Blue Background')
axes[0][1].legend(loc='upper left', facecolor='lightblue', edgecolor='blue')
axes[0][1].grid(True)

# Transparent
axes[1][0].plot(x, np.sin(x), label='sin(x)')
axes[1][0].plot(x, np.cos(x), label='cos(x)')
axes[1][0].title('Semi-Transparent')
axes[1][0].legend(loc='center', framealpha=0.5)
axes[1][0].grid(True)

# No frame
axes[1][1].plot(x, np.sin(x), label='sin(x)')
axes[1][1].plot(x, np.cos(x), label='cos(x)')
axes[1][1].title('No Frame')
axes[1][1].legend(loc='lower right', frameon=False)
axes[1][1].grid(True)

fig10.suptitle('Legend Style Comparison - All Inside Plot Boundaries', fontsize=14)
fig10.savefig(r'C:\cqc\qplotly\legend_debugging\10_style_comparison.png', width=1400, height=1000)
print("   Saved: 10_style_comparison.png\n")

print("="*70)
print("ALL DEMONSTRATION PLOTS CREATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated 15 PNG files in C:\\cqc\\qplotly\\legend_debugging\\")
print("\nKey demonstrations:")
print("  01 - Basic default legend (opaque white, black border, upper right)")
print("  02 - Grid showing all 11 location names")
print("  03 - Custom colors (blue and yellow themes)")
print("  04 - Transparency options (opaque, semi, very transparent)")
print("  05 - Frame on/off")
print("  06 - Font sizes (small and large)")
print("  07 - Many traces with auto-color scheme")
print("  08 - Scatter plot with legend")
print("  09 - Mixed plot types")
print("  10 - Side-by-side style comparison")
print("\nAll legends are positioned INSIDE the plot boundaries!")

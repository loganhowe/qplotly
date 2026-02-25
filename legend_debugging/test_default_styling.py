"""Test new default styling: white background, plot frame, black grid."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing new default styling...\n")

x = np.linspace(0, 10, 100)

# Test 1: Single plot with new defaults
print("Test 1: Single plot with new default styling")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), label='sin(x)')
fig1.plot(x, np.cos(x), label='cos(x)')
fig1.title('New Default Styling')
fig1.xlabel('X axis')
fig1.ylabel('Y axis')
fig1.legend()
fig1.savefig(r'C:\cqc\qplotly\legend_debugging\test_defaults_single.png', width=1000, height=600)
print("Saved: test_defaults_single.png")
print("  Should have:")
print("    - White background")
print("    - Black frame around plot")
print("    - Black grid lines (50% opacity)")
print("    - CMR10-like font\n")

# Test 2: Subplots with new defaults
print("Test 2: Subplots (2x2) with new default styling")
fig2, axes = qplotly.subplots(2, 2, figsize=(12, 10))

axes[0][0].plot(x, np.sin(x), label='sin(x)')
axes[0][0].plot(x, np.cos(x), label='cos(x)')
axes[0][0].title('Panel A')
axes[0][0].xlabel('x')
axes[0][0].ylabel('y')
axes[0][0].legend(loc='upper right')

axes[0][1].plot(x, np.sin(2*x), label='sin(2x)')
axes[0][1].plot(x, np.cos(2*x), label='cos(2x)')
axes[0][1].title('Panel B')
axes[0][1].xlabel('x')
axes[0][1].ylabel('y')
axes[0][1].legend(loc='upper left')

axes[1][0].scatter(np.random.randn(50), np.random.randn(50), label='data')
axes[1][0].title('Panel C')
axes[1][0].xlabel('x')
axes[1][0].ylabel('y')
axes[1][0].legend(loc='upper right')

axes[1][1].plot(x, np.exp(-x/5)*np.sin(x), label='damped')
axes[1][1].title('Panel D')
axes[1][1].xlabel('x')
axes[1][1].ylabel('y')
axes[1][1].legend(loc='upper right')

fig2.suptitle('2x2 Subplots - New Default Styling', fontsize=14)
fig2.savefig(r'C:\cqc\qplotly\legend_debugging\test_defaults_subplots.png', width=1200, height=1000)
print("Saved: test_defaults_subplots.png")
print("  Each panel should have:")
print("    - White background")
print("    - Black frame")
print("    - Black grid (50% opacity)")
print("    - Per-subplot legends\n")

# Test 3: Without grid (to see frame clearly)
print("Test 3: Same plot with grid turned off")
fig3 = qplotly.figure(figsize=(10, 6))
fig3.plot(x, np.sin(x), label='sin(x)')
fig3.plot(x, np.cos(x), label='cos(x)')
fig3.title('No Grid - Frame Should Be Visible')
fig3.xlabel('X axis')
fig3.ylabel('Y axis')
fig3.legend()
fig3.grid(False)  # Turn off grid to see frame clearly
fig3.savefig(r'C:\cqc\qplotly\legend_debugging\test_defaults_no_grid.png', width=1000, height=600)
print("Saved: test_defaults_no_grid.png")
print("  Should have:")
print("    - White background")
print("    - Black frame (clearly visible without grid)")
print("    - No grid lines\n")

# Test 4: Many traces to see auto-colors with new styling
print("Test 4: Many traces with new styling")
fig4 = qplotly.figure(figsize=(12, 6))
for i in range(6):
    fig4.plot(x, np.sin(x + i*np.pi/3), label=f'Wave {i+1}')
fig4.title('Auto-Colors with New Default Styling')
fig4.xlabel('X axis')
fig4.ylabel('Y axis')
fig4.legend(loc='right')
fig4.savefig(r'C:\cqc\qplotly\legend_debugging\test_defaults_many_traces.png', width=1200, height=600)
print("Saved: test_defaults_many_traces.png")
print("  Should show auto-colors on white background with frame\n")

# Test 5: Compare with matplotlib appearance
print("Test 5: Publication-style figure")
fig5 = qplotly.figure(figsize=(10, 6))
fig5.plot(x, np.sin(x), label='Experimental')
fig5.errorbar(x[::5], np.sin(x[::5]), yerr=0.1*np.ones(20),
              marker='o', label='Measured', capsize=3)
fig5.plot(x, 0.95*np.sin(x), 'r--', label='Model')
fig5.title('Publication-Style Figure')
fig5.xlabel('Time (s)')
fig5.ylabel('Amplitude (V)')
fig5.legend(loc='upper right')
fig5.savefig(r'C:\cqc\qplotly\legend_debugging\test_defaults_publication.png', width=1000, height=600)
print("Saved: test_defaults_publication.png")
print("  Should look like a clean matplotlib publication figure\n")

print("="*70)
print("DEFAULT STYLING TEST COMPLETE")
print("="*70)
print("\nNew defaults applied:")
print("  [OK] White background (plot_bgcolor='white')")
print("  [OK] Plot frame enabled (showline=True, mirror=True)")
print("  [OK] Black grid lines with 50% opacity")
print("  [OK] CMR10-like font (Computer Modern)")
print("\nInspect the 5 generated PNG files to verify the styling!")
print("\nFont note: The font is set to 'Computer Modern, CMU Serif, serif'")
print("  - If Computer Modern is installed, it will use it")
print("  - Otherwise, it falls back to CMU Serif or default serif")
print("  - For true LaTeX rendering, Plotly would need mathjax enabled")

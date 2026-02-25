"""Test legend fancybox (rounded corners) feature."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing legend fancybox (rounded corners)...\n")

x = np.linspace(0, 10, 100)

# Test 1: Default legend (should have fancybox=True by default)
print("1. Creating plot with default legend (fancybox=True by default)...")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), label='sin(x)')
fig1.plot(x, np.cos(x), label='cos(x)')
fig1.plot(x, np.sin(x)*np.cos(x), label='sin*cos')
fig1.title('Default Legend (fancybox=True)')
fig1.xlabel('X axis')
fig1.ylabel('Y axis')
fig1.legend()  # Default fancybox=True
fig1.savefig(r'C:\cqc\qplotly\frame_grid_debugging\test_legend_fancybox_default.png', width=1000, height=600)
print("Saved: test_legend_fancybox_default.png\n")

# Test 2: Explicitly set fancybox=True
print("2. Creating plot with fancybox=True (explicit)...")
fig2 = qplotly.figure(figsize=(10, 6))
fig2.plot(x, np.sin(x), label='sin(x)')
fig2.plot(x, np.cos(x), label='cos(x)')
fig2.plot(x, np.sin(x)*np.cos(x), label='sin*cos')
fig2.title('Legend with fancybox=True (Explicit)')
fig2.xlabel('X axis')
fig2.ylabel('Y axis')
fig2.legend(fancybox=True)
fig2.savefig(r'C:\cqc\qplotly\frame_grid_debugging\test_legend_fancybox_true.png', width=1000, height=600)
print("Saved: test_legend_fancybox_true.png\n")

# Test 3: Set fancybox=False
print("3. Creating plot with fancybox=False...")
fig3 = qplotly.figure(figsize=(10, 6))
fig3.plot(x, np.sin(x), label='sin(x)')
fig3.plot(x, np.cos(x), label='cos(x)')
fig3.plot(x, np.sin(x)*np.cos(x), label='sin*cos')
fig3.title('Legend with fancybox=False')
fig3.xlabel('X axis')
fig3.ylabel('Y axis')
fig3.legend(fancybox=False)
fig3.savefig(r'C:\cqc\qplotly\frame_grid_debugging\test_legend_fancybox_false.png', width=1000, height=600)
print("Saved: test_legend_fancybox_false.png\n")

# Test 4: Side-by-side comparison
print("4. Creating side-by-side comparison...")
fig4, axes = qplotly.subplots(1, 2, figsize=(14, 6))

axes[0].plot(x, np.sin(x), label='sin(x)')
axes[0].plot(x, np.cos(x), label='cos(x)')
axes[0].title('fancybox=True')
axes[0].xlabel('X')
axes[0].ylabel('Y')
axes[0].legend(fancybox=True)

axes[1].plot(x, np.sin(x), label='sin(x)')
axes[1].plot(x, np.cos(x), label='cos(x)')
axes[1].title('fancybox=False')
axes[1].xlabel('X')
axes[1].ylabel('Y')
axes[1].legend(fancybox=False)

fig4.suptitle('Fancybox Comparison (True vs False)', fontsize=14)
fig4.savefig(r'C:\cqc\qplotly\frame_grid_debugging\test_legend_fancybox_comparison.png', width=1400, height=600)
print("Saved: test_legend_fancybox_comparison.png\n")

print("="*70)
print("LEGEND FANCYBOX TEST COMPLETE")
print("="*70)
print("\nCURRENT STATUS:")
print("  - fancybox parameter is ACCEPTED for matplotlib compatibility")
print("  - Plotly does NOT support borderradius on native legend objects")
print("  - No visual difference expected between fancybox=True and False")
print("\nExamine the generated images to confirm current behavior.")
print("If you see NO rounded corners, this is expected with Plotly limitations.")

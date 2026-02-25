"""Test rounded corners (fancybox) on legends."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing rounded legend corners...\n")

x = np.linspace(0, 10, 100)

# Test 1: Single plot with rounded corners (fancybox=True, default)
print("Test 1: Single plot with rounded corners (fancybox=True)")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), label='sin(x)')
fig1.plot(x, np.cos(x), label='cos(x)')
fig1.plot(x, np.sin(2*x)*0.5, label='0.5*sin(2x)')
fig1.title('Rounded Corners (fancybox=True, default)')
fig1.xlabel('X')
fig1.ylabel('Y')
fig1.grid(True)
fig1.legend(fancybox=True)  # Default is True now
fig1.savefig(r'C:\cqc\qplotly\legend_debugging\test_rounded_on.png', width=1000, height=600)
print("Saved: test_rounded_on.png\n")

# Test 2: Single plot with square corners (fancybox=False)
print("Test 2: Single plot with square corners (fancybox=False)")
fig2 = qplotly.figure(figsize=(10, 6))
fig2.plot(x, np.sin(x), label='sin(x)')
fig2.plot(x, np.cos(x), label='cos(x)')
fig2.plot(x, np.sin(2*x)*0.5, label='0.5*sin(2x)')
fig2.title('Square Corners (fancybox=False)')
fig2.xlabel('X')
fig2.ylabel('Y')
fig2.grid(True)
fig2.legend(fancybox=False)
fig2.savefig(r'C:\cqc\qplotly\legend_debugging\test_rounded_off.png', width=1000, height=600)
print("Saved: test_rounded_off.png\n")

# Test 3: Comparison
print("Test 3: Side-by-side comparison")
fig3, axes = qplotly.subplots(1, 2, figsize=(14, 6))

axes[0].plot(x, np.sin(x), label='sin(x)')
axes[0].plot(x, np.cos(x), label='cos(x)')
axes[0].title('Rounded (fancybox=True)')
axes[0].legend(fancybox=True)
axes[0].grid(True)

axes[1].plot(x, np.sin(x), label='sin(x)')
axes[1].plot(x, np.cos(x), label='cos(x)')
axes[1].title('Square (fancybox=False)')
axes[1].legend(fancybox=False)
axes[1].grid(True)

fig3.suptitle('Legend Corner Style Comparison')
fig3.savefig(r'C:\cqc\qplotly\legend_debugging\test_rounded_comparison.png', width=1400, height=600)
print("Saved: test_rounded_comparison.png\n")

print("="*60)
print("Rounded corners test complete!")
print("="*60)
print("\nInspect the saved PNG files to see:")
print("  - test_rounded_on.png: Should have rounded corners")
print("  - test_rounded_off.png: Should have square corners")
print("  - test_rounded_comparison.png: Side-by-side comparison")

"""Test per-subplot legends (matplotlib style)."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing per-subplot legends...\n")

x = np.linspace(0, 10, 100)

# Test 1: 2x2 subplots with legends in each
print("Test 1: 2x2 subplots - each with own legend")
fig1, axes = qplotly.subplots(2, 2, figsize=(12, 10))

# Top-left
axes[0][0].plot(x, np.sin(x), label='sin(x)')
axes[0][0].plot(x, np.cos(x), label='cos(x)')
axes[0][0].title('Subplot 1: Upper Right Legend')
axes[0][0].legend(loc='upper right')
axes[0][0].grid(True)

# Top-right
axes[0][1].plot(x, np.sin(2*x), label='sin(2x)')
axes[0][1].plot(x, np.cos(2*x), label='cos(2x)')
axes[0][1].title('Subplot 2: Upper Left Legend')
axes[0][1].legend(loc='upper left')
axes[0][1].grid(True)

# Bottom-left
axes[1][0].plot(x, np.sin(x/2), label='sin(x/2)')
axes[1][0].plot(x, np.cos(x/2), label='cos(x/2)')
axes[1][0].title('Subplot 3: Lower Right Legend')
axes[1][0].legend(loc='lower right')
axes[1][0].grid(True)

# Bottom-right
axes[1][1].plot(x, np.sin(3*x), label='sin(3x)')
axes[1][1].plot(x, np.cos(3*x), label='cos(3x)')
axes[1][1].title('Subplot 4: Lower Left Legend')
axes[1][1].legend(loc='lower left')
axes[1][1].grid(True)

fig1.suptitle('Per-Subplot Legends - Each Legend Over Its Own Subplot', fontsize=14)
fig1.savefig(r'C:\cqc\qplotly\legend_debugging\test_subplot_legends_2x2.png', width=1200, height=1000)
print("Saved: test_subplot_legends_2x2.png\n")

# Test 2: 1x3 subplots
print("Test 2: 1x3 subplots - each with legend")
fig2, axes = qplotly.subplots(1, 3, figsize=(15, 5))

axes[0].plot(x, np.sin(x), label='sin(x)')
axes[0].plot(x, np.cos(x), label='cos(x)')
axes[0].title('Left Panel')
axes[0].legend(loc='upper right')
axes[0].grid(True)

axes[1].plot(x, np.sin(2*x), label='sin(2x)')
axes[1].plot(x, np.cos(2*x), label='cos(2x)')
axes[1].title('Center Panel')
axes[1].legend(loc='upper left')
axes[1].grid(True)

axes[2].plot(x, np.sin(3*x), label='sin(3x)')
axes[2].plot(x, np.cos(3*x), label='cos(3x)')
axes[2].title('Right Panel')
axes[2].legend(loc='lower right')
axes[2].grid(True)

fig2.suptitle('Horizontal Subplots with Per-Panel Legends')
fig2.savefig(r'C:\cqc\qplotly\legend_debugging\test_subplot_legends_1x3.png', width=1500, height=500)
print("Saved: test_subplot_legends_1x3.png\n")

# Test 3: 2x1 subplots with different legend positions
print("Test 3: 2x1 subplots - vertical layout")
fig3, axes = qplotly.subplots(2, 1, figsize=(10, 10))

axes[0].plot(x, np.sin(x), label='sin(x)')
axes[0].plot(x, np.cos(x), label='cos(x)')
axes[0].plot(x, np.sin(x)*np.cos(x), label='sin*cos')
axes[0].title('Top Panel: Upper Right')
axes[0].legend(loc='upper right')
axes[0].grid(True)

axes[1].plot(x, np.sin(2*x), label='sin(2x)')
axes[1].plot(x, np.cos(2*x), label='cos(2x)')
axes[1].plot(x, np.sin(2*x)*np.cos(2*x), label='sin(2x)*cos(2x)')
axes[1].title('Bottom Panel: Center')
axes[1].legend(loc='center')
axes[1].grid(True)

fig3.suptitle('Vertical Subplots with Per-Panel Legends')
fig3.savefig(r'C:\cqc\qplotly\legend_debugging\test_subplot_legends_2x1.png', width=1000, height=1000)
print("Saved: test_subplot_legends_2x1.png\n")

# Test 4: Some subplots with legends, some without
print("Test 4: Mixed - some with legends, some without")
fig4, axes = qplotly.subplots(2, 2, figsize=(12, 10))

# With legend
axes[0][0].plot(x, np.sin(x), label='sin(x)')
axes[0][0].plot(x, np.cos(x), label='cos(x)')
axes[0][0].title('With Legend')
axes[0][0].legend(loc='upper right')
axes[0][0].grid(True)

# Without legend
axes[0][1].plot(x, np.sin(2*x))
axes[0][1].plot(x, np.cos(2*x))
axes[0][1].title('No Legend')
axes[0][1].grid(True)

# With legend
axes[1][0].plot(x, np.sin(x/2), label='sin(x/2)')
axes[1][0].plot(x, np.cos(x/2), label='cos(x/2)')
axes[1][0].title('With Legend')
axes[1][0].legend(loc='lower left')
axes[1][0].grid(True)

# Without legend
axes[1][1].plot(x, np.sin(3*x))
axes[1][1].plot(x, np.cos(3*x))
axes[1][1].title('No Legend')
axes[1][1].grid(True)

fig4.suptitle('Mixed: Some Subplots with Legends, Some Without')
fig4.savefig(r'C:\cqc\qplotly\legend_debugging\test_subplot_legends_mixed.png', width=1200, height=1000)
print("Saved: test_subplot_legends_mixed.png\n")

print("="*60)
print("Per-subplot legends test complete!")
print("="*60)
print("\nKey features demonstrated:")
print("  - Each subplot has its own legend")
print("  - Legends appear over their respective subplots")
print("  - Different positions per subplot (upper right, upper left, etc.)")
print("  - Subplots without labels don't get legends")
print("\nInspect the saved PNG files to verify legends are positioned correctly")
print("over each subplot, not in a single master legend box!")

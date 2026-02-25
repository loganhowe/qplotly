"""Test frame and tick appearance AFTER modifications."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing MODIFIED frame and tick appearance...\n")

x = np.linspace(0, 10, 100)

# Test 1: Basic plot to see frame and ticks
print("1. Creating basic plot with MODIFIED styling...")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), label='sin(x)')
fig1.plot(x, np.cos(x), label='cos(x)')
fig1.title('Modified Frame and Tick Appearance')
fig1.xlabel('X axis')
fig1.ylabel('Y axis')
fig1.legend()
fig1.savefig(r'C:\cqc\qplotly\frame_grid_debugging\after_single.png', width=1000, height=600)
print("Saved: after_single.png\n")

# Test 2: Subplots
print("2. Creating subplot grid...")
fig2, axes = qplotly.subplots(2, 2, figsize=(12, 10))

axes[0][0].plot(x, np.sin(x), label='sin')
axes[0][0].title('Plot A')
axes[0][0].legend()

axes[0][1].plot(x, np.cos(x), label='cos')
axes[0][1].title('Plot B')
axes[0][1].legend()

axes[1][0].plot(x, np.tan(x), label='tan')
axes[1][0].title('Plot C')
axes[1][0].legend()

axes[1][1].plot(x, np.exp(-x/5), label='exp')
axes[1][1].title('Plot D')
axes[1][1].legend()

fig2.suptitle('Modified Subplots Frame/Tick Appearance')
fig2.savefig(r'C:\cqc\qplotly\frame_grid_debugging\after_subplots.png', width=1200, height=1000)
print("Saved: after_subplots.png\n")

print("AFTER modifications complete!")

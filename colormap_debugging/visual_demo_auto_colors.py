"""Visual demonstration of automatic color selection."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Creating visual demonstration of automatic color selection...")

x = np.linspace(0, 10, 100)

# Create a 2x3 subplot figure showing all cases
fig, axes = qplotly.subplots(2, 3, figsize=(18, 10),
                              subplot_titles=['2 Traces (blue, black)',
                                            '3 Traces (blue, red, green)',
                                            '4 Traces (blue, red, green, black)',
                                            '8 Traces (nipy_spectral)',
                                            'Mixed (explicit + auto)',
                                            'Scatter (blue, black)'])

# Panel 1: 2 traces
axes[0][0].plot(x, np.sin(x), label='trace 1')
axes[0][0].plot(x, np.cos(x), label='trace 2')
axes[0][0].legend()
axes[0][0].grid(True)

# Panel 2: 3 traces
axes[0][1].plot(x, np.sin(x), label='trace 1')
axes[0][1].plot(x, np.cos(x), label='trace 2')
axes[0][1].plot(x, np.sin(x) * np.cos(x), label='trace 3')
axes[0][1].legend()
axes[0][1].grid(True)

# Panel 3: 4 traces
axes[0][2].plot(x, np.sin(x), label='trace 1')
axes[0][2].plot(x, np.cos(x), label='trace 2')
axes[0][2].plot(x, np.sin(x) * np.cos(x), label='trace 3')
axes[0][2].plot(x, np.sin(x) + np.cos(x), label='trace 4')
axes[0][2].legend()
axes[0][2].grid(True)

# Panel 4: 8 traces
for i in range(8):
    axes[1][0].plot(x, np.sin(x + i * np.pi / 4), label=f'trace {i+1}')
axes[1][0].legend()
axes[1][0].grid(True)

# Panel 5: Mixed explicit and auto
axes[1][1].plot(x, np.sin(x), 'r-', label='explicit red')
axes[1][1].plot(x, np.cos(x), label='auto 1')
axes[1][1].plot(x, np.sin(x) * 0.5, label='auto 2')
axes[1][1].legend()
axes[1][1].grid(True)

# Panel 6: Scatter
x_scatter = np.random.randn(50)
y1 = np.random.randn(50)
y2 = np.random.randn(50) + 2
axes[1][2].scatter(x_scatter, y1, label='dataset 1')
axes[1][2].scatter(x_scatter, y2, label='dataset 2')
axes[1][2].legend()
axes[1][2].grid(True)

fig.suptitle('Automatic Color Selection Demo', fontsize=16)
fig.savefig(r'C:\cqc\qplotly\colormap_debugging\auto_color_demo.png',
            width=1800, height=1000)

print("Saved: auto_color_demo.png")
print("\nThis figure shows:")
print("  Top row: 2, 3, and 4 trace examples")
print("  Bottom row: 8 traces (nipy_spectral), mixed colors, and scatter plots")
print("\nInspect the PNG to visually confirm the color schemes are working correctly!")

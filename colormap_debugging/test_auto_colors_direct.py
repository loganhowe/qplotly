"""Test automatic color selection by directly inspecting trace colors."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

def get_trace_colors(fig):
    """Extract colors from all traces in the figure."""
    colors = []
    for trace in fig._fig.data:
        color = None
        if hasattr(trace, 'line') and trace.line and hasattr(trace.line, 'color'):
            color = trace.line.color
        elif hasattr(trace, 'marker') and trace.marker and hasattr(trace.marker, 'color'):
            color = trace.marker.color
        colors.append(color)
    return colors

print("Testing automatic color selection (direct inspection)...\n")

# Test data
x = np.linspace(0, 10, 100)

# Test 1: 2 traces (should be blue, black)
print("="*60)
print("Test 1: 2 traces (should be blue, black)")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), label='sin(x)')
fig1.plot(x, np.cos(x), label='cos(x)')
fig1.title('2 Traces - Blue and Black')
fig1.legend()

# Apply color scheme (this happens in show/savefig)
fig1._apply_auto_color_scheme()

colors = get_trace_colors(fig1)
print(f"Trace colors: {colors}")
print(f"Expected: ['blue', 'black']")
print(f"Match: {colors == ['blue', 'black']}")

# Test 2: 3 traces (should be blue, red, green)
print("\n" + "="*60)
print("Test 2: 3 traces (should be blue, red, green)")
fig2 = qplotly.figure(figsize=(10, 6))
fig2.plot(x, np.sin(x), label='sin(x)')
fig2.plot(x, np.cos(x), label='cos(x)')
fig2.plot(x, np.sin(x) * np.cos(x), label='sin(x)*cos(x)')
fig2.title('3 Traces - Blue, Red, Green')
fig2.legend()

fig2._apply_auto_color_scheme()

colors = get_trace_colors(fig2)
print(f"Trace colors: {colors}")
print(f"Expected: ['blue', 'red', 'green']")
print(f"Match: {colors == ['blue', 'red', 'green']}")

# Test 3: 4 traces (should be blue, red, green, black)
print("\n" + "="*60)
print("Test 3: 4 traces (should be blue, red, green, black)")
fig3 = qplotly.figure(figsize=(10, 6))
fig3.plot(x, np.sin(x), label='sin(x)')
fig3.plot(x, np.cos(x), label='cos(x)')
fig3.plot(x, np.sin(x) * np.cos(x), label='sin(x)*cos(x)')
fig3.plot(x, np.sin(x) + np.cos(x), label='sin(x)+cos(x)')
fig3.title('4 Traces - Blue, Red, Green, Black')
fig3.legend()

fig3._apply_auto_color_scheme()

colors = get_trace_colors(fig3)
print(f"Trace colors: {colors}")
print(f"Expected: ['blue', 'red', 'green', 'black']")
print(f"Match: {colors == ['blue', 'red', 'green', 'black']}")

# Test 4: 8 traces (should use nipy_spectral)
print("\n" + "="*60)
print("Test 4: 8 traces (should use nipy_spectral colormap)")
fig4 = qplotly.figure(figsize=(10, 6))
for i in range(8):
    fig4.plot(x, np.sin(x + i * np.pi / 4), label=f'trace {i+1}')
fig4.title('8 Traces - nipy_spectral colormap')
fig4.legend()

fig4._apply_auto_color_scheme()

colors = get_trace_colors(fig4)
print(f"Number of traces: {len(colors)}")
print(f"Trace colors (first 3): {colors[:3]}")
print(f"Should be hex colors from nipy_spectral: {all(isinstance(c, str) and c.startswith('#') for c in colors if c)}")

# Test 5: Mixed auto and explicit colors
print("\n" + "="*60)
print("Test 5: Mixed - 1 explicit red, 2 auto (should be blue, black for auto)")
fig5 = qplotly.figure(figsize=(10, 6))
fig5.plot(x, np.sin(x), 'r-', label='sin(x) - explicit red')  # Explicit red
fig5.plot(x, np.cos(x), label='cos(x) - auto')  # Auto color
fig5.plot(x, np.sin(x) * 0.5, label='0.5*sin(x) - auto')  # Auto color
fig5.title('Mixed Colors')
fig5.legend()

print(f"Auto-colored trace indices: {fig5._auto_colored_trace_indices}")
print(f"Expected auto-colored indices: [1, 2] (not trace 0, which is explicit red)")

fig5._apply_auto_color_scheme()

colors = get_trace_colors(fig5)
print(f"Trace colors: {colors}")
print(f"Expected: ['red', 'blue', 'black']")
print(f"Match: {colors == ['red', 'blue', 'black']}")

# Test 6: Scatter plots
print("\n" + "="*60)
print("Test 6: Scatter plots with 2 auto colors")
fig6 = qplotly.figure(figsize=(10, 6))
x_scatter = np.random.randn(50)
y_scatter1 = np.random.randn(50)
y_scatter2 = np.random.randn(50)
fig6.scatter(x_scatter, y_scatter1, label='dataset 1')
fig6.scatter(x_scatter, y_scatter2, label='dataset 2')
fig6.title('Scatter - 2 Traces')
fig6.legend()

fig6._apply_auto_color_scheme()

colors = get_trace_colors(fig6)
print(f"Trace colors: {colors}")
print(f"Expected: ['blue', 'black']")
print(f"Match: {colors == ['blue', 'black']}")

print("\n" + "="*60)
print("ALL TESTS COMPLETE")
print("="*60)

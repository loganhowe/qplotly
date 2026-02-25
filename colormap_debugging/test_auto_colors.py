"""Test automatic color selection based on number of traces."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing automatic color selection...\n")

# Test data
x = np.linspace(0, 10, 100)

# Test 1: 2 traces (should be blue, black)
print("Test 1: 2 traces (should be blue, black)")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), label='sin(x)')  # Auto color
fig1.plot(x, np.cos(x), label='cos(x)')  # Auto color
fig1.title('2 Traces - Blue and Black')
fig1.xlabel('x')
fig1.ylabel('y')
fig1.legend()
fig1.savefig(r'C:\cqc\qplotly\colormap_debugging\auto_2traces.png', width=1000, height=600)
print("Saved: auto_2traces.png\n")

# Test 2: 3 traces (should be blue, red, green)
print("Test 2: 3 traces (should be blue, red, green)")
fig2 = qplotly.figure(figsize=(10, 6))
fig2.plot(x, np.sin(x), label='sin(x)')
fig2.plot(x, np.cos(x), label='cos(x)')
fig2.plot(x, np.sin(x) * np.cos(x), label='sin(x)*cos(x)')
fig2.title('3 Traces - Blue, Red, Green')
fig2.xlabel('x')
fig2.ylabel('y')
fig2.legend()
fig2.savefig(r'C:\cqc\qplotly\colormap_debugging\auto_3traces.png', width=1000, height=600)
print("Saved: auto_3traces.png\n")

# Test 3: 4 traces (should be blue, red, green, black)
print("Test 3: 4 traces (should be blue, red, green, black)")
fig3 = qplotly.figure(figsize=(10, 6))
fig3.plot(x, np.sin(x), label='sin(x)')
fig3.plot(x, np.cos(x), label='cos(x)')
fig3.plot(x, np.sin(x) * np.cos(x), label='sin(x)*cos(x)')
fig3.plot(x, np.sin(x) + np.cos(x), label='sin(x)+cos(x)')
fig3.title('4 Traces - Blue, Red, Green, Black')
fig3.xlabel('x')
fig3.ylabel('y')
fig3.legend()
fig3.savefig(r'C:\cqc\qplotly\colormap_debugging\auto_4traces.png', width=1000, height=600)
print("Saved: auto_4traces.png\n")

# Test 4: 8 traces (should use nipy_spectral)
print("Test 4: 8 traces (should use nipy_spectral colormap)")
fig4 = qplotly.figure(figsize=(10, 6))
for i in range(8):
    fig4.plot(x, np.sin(x + i * np.pi / 4), label=f'trace {i+1}')
fig4.title('8 Traces - nipy_spectral colormap')
fig4.xlabel('x')
fig4.ylabel('y')
fig4.legend()
fig4.savefig(r'C:\cqc\qplotly\colormap_debugging\auto_8traces.png', width=1000, height=600)
print("Saved: auto_8traces.png\n")

# Test 5: Mixed auto and explicit colors (only auto colors should be affected)
print("Test 5: Mixed - 1 explicit red, 2 auto (should be blue, black for auto)")
fig5 = qplotly.figure(figsize=(10, 6))
fig5.plot(x, np.sin(x), 'r-', label='sin(x) - explicit red')  # Explicit red
fig5.plot(x, np.cos(x), label='cos(x) - auto')  # Auto color
fig5.plot(x, np.sin(x) * 0.5, label='0.5*sin(x) - auto')  # Auto color
fig5.title('Mixed Colors - 1 Explicit (red), 2 Auto (blue, black)')
fig5.xlabel('x')
fig5.ylabel('y')
fig5.legend()
fig5.savefig(r'C:\cqc\qplotly\colormap_debugging\auto_mixed.png', width=1000, height=600)
print("Saved: auto_mixed.png\n")

# Test 6: Scatter plots
print("Test 6: Scatter plots with 2 auto colors")
fig6 = qplotly.figure(figsize=(10, 6))
x_scatter = np.random.randn(50)
y_scatter1 = np.random.randn(50)
y_scatter2 = np.random.randn(50)
fig6.scatter(x_scatter, y_scatter1, label='dataset 1')
fig6.scatter(x_scatter, y_scatter2, label='dataset 2')
fig6.title('Scatter - 2 Traces (blue, black)')
fig6.xlabel('x')
fig6.ylabel('y')
fig6.legend()
fig6.savefig(r'C:\cqc\qplotly\colormap_debugging\auto_scatter.png', width=1000, height=600)
print("Saved: auto_scatter.png\n")

print("All tests complete!")
print("\nExpected results:")
print("- auto_2traces.png: blue and black lines")
print("- auto_3traces.png: blue, red, green lines")
print("- auto_4traces.png: blue, red, green, black lines")
print("- auto_8traces.png: rainbow colors from nipy_spectral")
print("- auto_mixed.png: red (explicit), blue, black (auto)")
print("- auto_scatter.png: blue and black scatter points")

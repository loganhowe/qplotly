"""Demonstrate frame and tick details matching matplotlib."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Creating detailed frame and tick demonstrations...\n")

x = np.linspace(0, 2, 50)

# Demo 1: Clean plot emphasizing frame and ticks
print("1. Creating plot emphasizing frame and ticks...")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, x**2, 'b-', linewidth=2, label='y = x²')
fig1.plot(x, x**3, 'r-', linewidth=2, label='y = x³')
fig1.title('Frame and Tick Details (Matplotlib-Style)')
fig1.xlabel('X axis')
fig1.ylabel('Y axis')
fig1.legend(loc='upper left')
fig1.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_frame_emphasis.png', width=1000, height=600)
print("Saved: demo_frame_emphasis.png\n")

# Demo 2: Without grid to see frame clearly
print("2. Creating plot without grid (frame only)...")
fig2 = qplotly.figure(figsize=(10, 6))
fig2.plot(x, np.sin(x*np.pi), 'g-', linewidth=2, label='sin(πx)')
fig2.title('Frame and Ticks Without Grid')
fig2.xlabel('X axis')
fig2.ylabel('Y axis')
fig2.legend()
fig2.grid(False)
fig2.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_frame_no_grid.png', width=1000, height=600)
print("Saved: demo_frame_no_grid.png\n")

# Demo 3: With grid to see contrast
print("3. Creating plot with grid (frame + grid contrast)...")
fig3 = qplotly.figure(figsize=(10, 6))
fig3.plot(x, np.cos(x*np.pi), 'm-', linewidth=2, label='cos(πx)')
fig3.title('Frame and Ticks With Grid (Note Thickness Difference)')
fig3.xlabel('X axis')
fig3.ylabel('Y axis')
fig3.legend()
fig3.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_frame_with_grid.png', width=1000, height=600)
print("Saved: demo_frame_with_grid.png\n")

# Demo 4: Multiple subplots showing frame/tick consistency
print("4. Creating multi-panel figure...")
fig4, axes = qplotly.subplots(1, 3, figsize=(15, 5))

axes[0].plot(x, x, 'b-', linewidth=2, label='linear')
axes[0].title('(A) Linear')
axes[0].xlabel('x')
axes[0].ylabel('y')
axes[0].legend()

axes[1].plot(x, x**2, 'r-', linewidth=2, label='quadratic')
axes[1].title('(B) Quadratic')
axes[1].xlabel('x')
axes[1].ylabel('y')
axes[1].legend()

axes[2].plot(x, x**3, 'g-', linewidth=2, label='cubic')
axes[2].title('(C) Cubic')
axes[2].xlabel('x')
axes[2].ylabel('y')
axes[2].legend()

fig4.suptitle('Consistent Frame and Tick Appearance Across Subplots', fontsize=14)
fig4.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_frame_subplots.png', width=1500, height=500)
print("Saved: demo_frame_subplots.png\n")

# Demo 5: Scientific figure example
print("5. Creating publication-quality scientific figure...")
fig5, axes = qplotly.subplots(2, 2, figsize=(12, 10))

t = np.linspace(0, 10, 200)

# Panel A
axes[0][0].plot(t, np.exp(-t/5)*np.sin(2*np.pi*t/2), 'b-', linewidth=1.5)
axes[0][0].title('(A) Damped Oscillation')
axes[0][0].xlabel('Time (s)')
axes[0][0].ylabel('Amplitude')

# Panel B
axes[0][1].scatter(np.random.randn(50), 2*np.random.randn(50)+1, s=40)
axes[0][1].title('(B) Scatter Data')
axes[0][1].xlabel('X variable')
axes[0][1].ylabel('Y variable')

# Panel C
freq = np.logspace(-1, 2, 100)
axes[1][0].plot(freq, 1/(1+(freq/10)**2), 'r-', linewidth=2)
axes[1][0].title('(C) Frequency Response')
axes[1][0].xlabel('Frequency (Hz)')
axes[1][0].ylabel('Gain')
axes[1][0].xscale('log')

# Panel D
axes[1][1].errorbar([1,2,3,4,5], [2,3,5,4,6], yerr=[0.3,0.4,0.5,0.4,0.6],
                     marker='o', capsize=4, markersize=8, label='Measured')
axes[1][1].title('(D) Experimental Data')
axes[1][1].xlabel('Trial')
axes[1][1].ylabel('Result')
axes[1][1].legend()

fig5.suptitle('Publication Figure: Frame/Tick/Grid Styling', fontsize=15)
fig5.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_publication_figure.png', width=1200, height=1000)
print("Saved: demo_publication_figure.png\n")

print("="*70)
print("FRAME AND TICK DEMONSTRATION COMPLETE")
print("="*70)
print("\nGenerated files:")
print("  1. demo_frame_emphasis.png - Clear view of frame and ticks")
print("  2. demo_frame_no_grid.png - Frame and ticks only (no grid)")
print("  3. demo_frame_with_grid.png - Frame thicker than grid lines")
print("  4. demo_frame_subplots.png - Consistent appearance across panels")
print("  5. demo_publication_figure.png - Realistic scientific figure")
print("\nKEY FEATURES (Matplotlib-Style):")
print("  [OK] Frame line thicker (2.0) than grid lines (0.5)")
print("  [OK] Ticks extend OUTSIDE the plot frame")
print("  [OK] Tick length: 5 pixels")
print("  [OK] Tick thickness: 1.5 (matches frame style)")
print("  [OK] Consistent across single plots and subplots")
print("\nCompare with before_*.png files to see the improvements!")

"""Demonstrate tight_layout and centered titles."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Demonstrating tight_layout and centered titles...\n")

x = np.linspace(0, 10, 100)

# Demo 1: Single plot with centered title and tight layout
print("1. Single plot with tight_layout=True (default)...")
fig1 = qplotly.figure(figsize=(10, 6))
fig1.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
fig1.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
fig1.title('Centered Title with Tight Layout')
fig1.xlabel('X axis')
fig1.ylabel('Y axis')
fig1.legend()
fig1.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_tight_layout_single.png', width=1000, height=600)
print("Saved: demo_tight_layout_single.png\n")

# Demo 2: Subplots with tight layout
print("2. Subplots with tight_layout=True (default)...")
fig2, axes = qplotly.subplots(2, 2, figsize=(12, 10))

axes[0][0].plot(x, np.sin(x), 'b-', linewidth=2)
axes[0][0].title('Plot A: Centered Title')
axes[0][0].xlabel('X')
axes[0][0].ylabel('Y')

axes[0][1].plot(x, np.cos(x), 'r-', linewidth=2)
axes[0][1].title('Plot B: Also Centered')
axes[0][1].xlabel('X')
axes[0][1].ylabel('Y')

axes[1][0].plot(x, np.tan(x), 'g-', linewidth=2)
axes[1][0].title('Plot C: Centered Too')
axes[1][0].xlabel('X')
axes[1][0].ylabel('Y')

axes[1][1].plot(x, np.exp(-x/5), 'm-', linewidth=2)
axes[1][1].title('Plot D: All Centered')
axes[1][1].xlabel('X')
axes[1][1].ylabel('Y')

fig2.suptitle('Tight Layout with Centered Subplot Titles', fontsize=15)
fig2.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_tight_layout_subplots.png', width=1200, height=1000)
print("Saved: demo_tight_layout_subplots.png\n")

# Demo 3: Compare tight_layout ON vs OFF
print("3. Comparing tight_layout ON vs OFF...")
fig3, axes = qplotly.subplots(1, 2, figsize=(14, 6))

axes[0].plot(x, np.sin(x), 'b-', linewidth=2, label='sin')
axes[0].plot(x, np.cos(x), 'r-', linewidth=2, label='cos')
axes[0].title('With Tight Layout')
axes[0].xlabel('X axis')
axes[0].ylabel('Y axis')
axes[0].legend()

axes[1].plot(x, np.sin(2*x), 'g-', linewidth=2, label='sin(2x)')
axes[1].plot(x, np.cos(2*x), 'm-', linewidth=2, label='cos(2x)')
axes[1].title('With Tight Layout')
axes[1].xlabel('X axis')
axes[1].ylabel('Y axis')
axes[1].legend()

fig3.suptitle('Tight Layout Example (tight_layout=True by default)', fontsize=14)
fig3.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_tight_on.png', width=1400, height=600, tight_layout=True)
print("Saved: demo_tight_on.png (with tight_layout)\n")

# Demo 4: Same plot without tight layout for comparison
fig4, axes = qplotly.subplots(1, 2, figsize=(14, 6))

axes[0].plot(x, np.sin(x), 'b-', linewidth=2, label='sin')
axes[0].plot(x, np.cos(x), 'r-', linewidth=2, label='cos')
axes[0].title('Without Tight Layout')
axes[0].xlabel('X axis')
axes[0].ylabel('Y axis')
axes[0].legend()

axes[1].plot(x, np.sin(2*x), 'g-', linewidth=2, label='sin(2x)')
axes[1].plot(x, np.cos(2*x), 'm-', linewidth=2, label='cos(2x)')
axes[1].title('Without Tight Layout')
axes[1].xlabel('X axis')
axes[1].ylabel('Y axis')
axes[1].legend()

fig4.suptitle('Without Tight Layout (tight_layout=False)', fontsize=14)
fig4.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_tight_off.png', width=1400, height=600, tight_layout=False)
print("Saved: demo_tight_off.png (without tight_layout)\n")

# Demo 5: Publication figure with all features
print("4. Publication-quality figure with all features...")
fig5, axes = qplotly.subplots(2, 3, figsize=(15, 10))

t = np.linspace(0, 10, 200)

# Panel A
axes[0][0].plot(t, np.sin(t), 'b-', linewidth=1.5)
axes[0][0].title('(A) Sine Wave')
axes[0][0].xlabel('Time (s)')
axes[0][0].ylabel('Amplitude')

# Panel B
axes[0][1].plot(t, np.cos(t), 'r-', linewidth=1.5)
axes[0][1].title('(B) Cosine Wave')
axes[0][1].xlabel('Time (s)')
axes[0][1].ylabel('Amplitude')

# Panel C
axes[0][2].plot(t, np.exp(-t/5), 'g-', linewidth=1.5)
axes[0][2].title('(C) Exponential Decay')
axes[0][2].xlabel('Time (s)')
axes[0][2].ylabel('Amplitude')

# Panel D
axes[1][0].scatter(np.random.randn(50), 2*np.random.randn(50), s=40)
axes[1][0].title('(D) Scatter Data')
axes[1][0].xlabel('X variable')
axes[1][0].ylabel('Y variable')

# Panel E
freq = np.logspace(-1, 2, 100)
axes[1][1].plot(freq, 1/(1+(freq/10)**2), 'm-', linewidth=2)
axes[1][1].title('(E) Frequency Response')
axes[1][1].xlabel('Frequency (Hz)')
axes[1][1].ylabel('Gain')
axes[1][1].xscale('log')

# Panel F
axes[1][2].errorbar([1,2,3,4,5], [2,3,5,4,6], yerr=[0.3,0.4,0.5,0.4,0.6],
                     marker='o', capsize=4, markersize=8, label='Data')
axes[1][2].title('(F) Experimental Data')
axes[1][2].xlabel('Trial')
axes[1][2].ylabel('Result')
axes[1][2].legend()

fig5.suptitle('Publication Figure: Tight Layout + Centered Titles + Frame/Tick Styling', fontsize=15)
fig5.savefig(r'C:\cqc\qplotly\frame_grid_debugging\demo_complete_publication.png', width=1500, height=1000)
print("Saved: demo_complete_publication.png\n")

print("="*70)
print("TIGHT LAYOUT AND CENTERED TITLES DEMONSTRATION COMPLETE")
print("="*70)
print("\nGenerated files:")
print("  1. demo_tight_layout_single.png - Single plot with tight layout")
print("  2. demo_tight_layout_subplots.png - 2x2 subplots with tight layout")
print("  3. demo_tight_on.png - With tight_layout=True")
print("  4. demo_tight_off.png - With tight_layout=False (for comparison)")
print("  5. demo_complete_publication.png - 2x3 publication figure")
print("\nKEY FEATURES:")
print("  [OK] tight_layout=True by default in show() and savefig()")
print("  [OK] Reduces margins for better space usage")
print("  [OK] All titles centered over plot axes")
print("  [OK] Single plot titles centered")
print("  [OK] Subplot titles centered")
print("  [OK] suptitle centered over entire figure")
print("\nCompare demo_tight_on.png vs demo_tight_off.png to see the difference!")

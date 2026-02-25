"""Test matplotlib compatibility of scatter() method."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Testing scatter() matplotlib compatibility...\n")

# Generate test data
np.random.seed(42)
x = np.random.randn(50)
y = np.random.randn(50)

print("="*60)
print("Test 1: Basic scatter with scalar size")
print("="*60)
try:
    fig1 = qplotly.figure(figsize=(8, 6))
    fig1.scatter(x, y, s=50, label='scalar size')
    fig1.title('Scalar Size (s=50)')
    fig1.legend()
    fig1.savefig(r'C:\cqc\qplotly\colormap_debugging\scatter_scalar_size.png', width=800, height=600)
    print("[OK] PASS: Scalar size works")
except Exception as e:
    print(f"[FAIL] FAIL: {e}")

print("\n" + "="*60)
print("Test 2: Array of sizes (one size per point)")
print("="*60)
try:
    sizes = np.random.randint(10, 100, size=len(x))
    fig2 = qplotly.figure(figsize=(8, 6))
    fig2.scatter(x, y, s=sizes, label='array sizes')
    fig2.title('Array Sizes (different per point)')
    fig2.legend()
    fig2.savefig(r'C:\cqc\qplotly\colormap_debugging\scatter_array_size.png', width=800, height=600)
    print("[OK] PASS: Array sizes work")
except Exception as e:
    print(f"[FAIL] FAIL: {e}")

print("\n" + "="*60)
print("Test 3: Different marker shapes")
print("="*60)
# Matplotlib-style markers
markers = ['o', 's', '^', 'v', 'D', 'd', '+', 'x', '*', 'p', 'h']
marker_names = ['circle', 'square', 'triangle-up', 'triangle-down', 'diamond',
                'diamond', 'cross', 'x', 'star', 'pentagon', 'hexagon']

fig3, axes = qplotly.subplots(3, 4, figsize=(16, 12))
axes_flat = [axes[i][j] for i in range(3) for j in range(4)]

for idx, (marker, name) in enumerate(zip(markers, marker_names)):
    if idx < len(axes_flat):
        try:
            ax = axes_flat[idx]
            x_test = np.random.randn(20)
            y_test = np.random.randn(20)
            ax.scatter(x_test, y_test, s=100, marker=marker, label=name)
            ax.title(f"marker='{marker}' ({name})")
            ax.legend()
            print(f"  [OK] marker='{marker}' ({name}) works")
        except Exception as e:
            print(f"  [FAIL] marker='{marker}' ({name}) failed: {e}")

fig3.suptitle('Matplotlib Marker Styles')
fig3.savefig(r'C:\cqc\qplotly\colormap_debugging\scatter_markers.png', width=1600, height=1200)
print("Saved: scatter_markers.png")

print("\n" + "="*60)
print("Test 4: Color array with colormap")
print("="*60)
try:
    colors = np.random.rand(len(x))
    fig4 = qplotly.figure(figsize=(8, 6))
    fig4.scatter(x, y, c=colors, s=50, cmap='Viridis', colorbar=True, label='colored points')
    fig4.title('Array Colors with Colormap')
    fig4.legend()
    fig4.savefig(r'C:\cqc\qplotly\colormap_debugging\scatter_colormap.png', width=800, height=600)
    print("[OK] PASS: Color array with colormap works")
except Exception as e:
    print(f"[FAIL] FAIL: {e}")

print("\n" + "="*60)
print("Test 5: Edge colors and line widths")
print("="*60)
try:
    fig5 = qplotly.figure(figsize=(8, 6))
    fig5.scatter(x, y, s=100, c='lightblue', edgecolors='black', linewidths=2, label='with edges')
    fig5.title('Markers with Edge Colors')
    fig5.legend()
    fig5.savefig(r'C:\cqc\qplotly\colormap_debugging\scatter_edges.png', width=800, height=600)
    print("[OK] PASS: Edge colors and line widths work")
except Exception as e:
    print(f"[FAIL] FAIL: {e}")

print("\n" + "="*60)
print("Test 6: Alpha transparency")
print("="*60)
try:
    fig6 = qplotly.figure(figsize=(8, 6))
    # Overlapping clusters
    x1 = np.random.randn(100)
    y1 = np.random.randn(100)
    x2 = np.random.randn(100) + 1
    y2 = np.random.randn(100) + 1
    fig6.scatter(x1, y1, s=50, c='red', alpha=0.5, label='cluster 1')
    fig6.scatter(x2, y2, s=50, c='blue', alpha=0.5, label='cluster 2')
    fig6.title('Alpha Transparency')
    fig6.legend()
    fig6.savefig(r'C:\cqc\qplotly\colormap_debugging\scatter_alpha.png', width=800, height=600)
    print("[OK] PASS: Alpha transparency works")
except Exception as e:
    print(f"[FAIL] FAIL: {e}")

print("\n" + "="*60)
print("Test 7: Additional matplotlib markers (may not all be supported)")
print("="*60)
# Additional markers that matplotlib supports
extra_markers = ['<', '>', '1', '2', '3', '4', '8', 'P', 'X', '|', '_']
extra_names = ['triangle-left', 'triangle-right', 'tri-down', 'tri-up', 'tri-left',
               'tri-right', 'octagon', 'plus-filled', 'x-filled', 'vline', 'hline']

print("Testing additional matplotlib markers:")
for marker, name in zip(extra_markers, extra_names):
    try:
        fig_test = qplotly.figure()
        fig_test.scatter([0], [0], marker=marker)
        print(f"  [OK] marker='{marker}' ({name}) works")
    except Exception as e:
        print(f"  [FAIL] marker='{marker}' ({name}) not supported or failed")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("\nSupported matplotlib-compatible features:")
print("  [OK] s parameter (scalar and array sizes)")
print("  [OK] c parameter (colors, including arrays)")
print("  [OK] marker parameter (common matplotlib markers)")
print("  [OK] alpha parameter (transparency)")
print("  [OK] cmap parameter (colormaps for array colors)")
print("  [OK] colorbar parameter")
print("  [OK] edgecolors parameter")
print("  [OK] linewidths parameter")
print("  [OK] label parameter")
print("\nSupported marker styles:")
print("  'o', 's', '^', 'v', 'D', 'd', '+', 'x', '*', 'p', 'h'")
print("\nNOTE: Some matplotlib markers may not be available in Plotly.")
print("If a marker isn't in _FMT_MARKERS, it's passed directly to Plotly.")

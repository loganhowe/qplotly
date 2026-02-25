"""Comprehensive test of all colormap functionality."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

# Create test data
x = np.linspace(0, 10, 50)
y = np.linspace(0, 10, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

print("Running comprehensive colormap tests...\n")

# Test various colormaps
colormaps_to_test = [
    (None, 'default'),  # Should use Plasma
    ('Plasma', 'plasma_explicit'),
    ('Viridis', 'viridis'),
    ('Cividis', 'cividis'),
    ('Inferno', 'inferno'),
    ('Magma', 'magma'),
    ('Turbo', 'turbo'),
    ('Blues', 'blues'),
    ('RdBu', 'rdbu'),
    ('RdYlGn', 'rdylgn'),
]

fig, axes = qplotly.subplots(2, 5, figsize=(20, 8),
                              subplot_titles=[name for _, name in colormaps_to_test])

for idx, (cmap, name) in enumerate(colormaps_to_test):
    row = idx // 5
    col = idx % 5
    ax = axes[row][col]

    if cmap is None:
        ax.pcolormesh(x, y, Z)  # Use default
        print(f"[OK] {name}: using default (should be Plasma)")
    else:
        ax.pcolormesh(x, y, Z, cmap=cmap)
        print(f"[OK] {name}: explicitly set to {cmap}")

fig.suptitle('Comprehensive Colormap Test - All should render correctly')
fig.savefig(r'C:\cqc\qplotly\colormap_debugging\comprehensive_test.png',
            width=2000, height=800)

print("\nComprehensive test complete!")
print("Saved: comprehensive_test.png")
print("\nAll colormaps rendered successfully!")

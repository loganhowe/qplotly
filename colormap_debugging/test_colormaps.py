"""Test pcolormesh with different colormaps and validate colors."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np
from PIL import Image
import json

# Create test data
x = np.linspace(0, 10, 50)
y = np.linspace(0, 10, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

print("Creating test plots with different colormaps...")

# Test 1: Default (should become Plasma after fix)
fig1 = qplotly.figure(figsize=(8, 6))
fig1.pcolormesh(x, y, Z)
fig1.title('Default Colormap')
fig1.savefig(r'C:\cqc\qplotly\colormap_debugging\test_default.png', width=800, height=600)
print("Saved: test_default.png")

# Test 2: Explicitly Plasma
fig2 = qplotly.figure(figsize=(8, 6))
fig2.pcolormesh(x, y, Z, cmap='Plasma')
fig2.title('Explicit Plasma')
fig2.savefig(r'C:\cqc\qplotly\colormap_debugging\test_plasma.png', width=800, height=600)
print("Saved: test_plasma.png")

# Test 3: Viridis for comparison
fig3 = qplotly.figure(figsize=(8, 6))
fig3.pcolormesh(x, y, Z, cmap='Viridis')
fig3.title('Viridis')
fig3.savefig(r'C:\cqc\qplotly\colormap_debugging\test_viridis.png', width=800, height=600)
print("Saved: test_viridis.png")

# Test 4: RdBu for comparison
fig4 = qplotly.figure(figsize=(8, 6))
fig4.pcolormesh(x, y, Z, cmap='RdBu')
fig4.title('RdBu')
fig4.savefig(r'C:\cqc\qplotly\colormap_debugging\test_rdbu.png', width=800, height=600)
print("Saved: test_rdbu.png")

print("\nTest plots created successfully!")

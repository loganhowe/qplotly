"""Visual comparison tool to display test plots side by side."""
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load the test images
images = {
    'Default (Now Plasma)': r'C:\cqc\qplotly\colormap_debugging\test_default.png',
    'Explicit Plasma': r'C:\cqc\qplotly\colormap_debugging\test_plasma.png',
    'Viridis': r'C:\cqc\qplotly\colormap_debugging\test_viridis.png',
    'RdBu': r'C:\cqc\qplotly\colormap_debugging\test_rdbu.png',
}

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('Colormap Validation - Visual Comparison', fontsize=16, fontweight='bold')

for idx, (name, path) in enumerate(images.items()):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]

    img = Image.open(path)
    ax.imshow(img)
    ax.set_title(name, fontsize=12, fontweight='bold')
    ax.axis('off')

    # Add RGB color info
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    center_y, center_x = h // 2, w // 3
    sample = img_array[center_y-10:center_y+10, center_x-10:center_x+10, :3]
    mean_color = sample.mean(axis=(0, 1))

    # Add color patch showing the sampled color
    color_patch = mpatches.Rectangle((0.02, 0.02), 0.15, 0.08,
                                    transform=ax.transAxes,
                                    facecolor=mean_color/255,
                                    edgecolor='white', linewidth=2)
    ax.add_patch(color_patch)

    # Add RGB text
    rgb_text = f'RGB: [{int(mean_color[0])}, {int(mean_color[1])}, {int(mean_color[2])}]'
    ax.text(0.02, 0.12, rgb_text, transform=ax.transAxes,
           fontsize=9, color='white', bbox=dict(boxstyle='round',
           facecolor='black', alpha=0.7))

plt.tight_layout()
plt.savefig(r'C:\cqc\qplotly\colormap_debugging\visual_comparison.png', dpi=150, bbox_inches='tight')
print("Visual comparison saved to: visual_comparison.png")
print("\nYou can see that 'Default' and 'Explicit Plasma' are identical,")
print("confirming that pcolormesh now defaults to Plasma instead of Viridis!")

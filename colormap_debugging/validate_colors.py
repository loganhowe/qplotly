"""Validate that the saved plots use the correct colormaps."""
import numpy as np
from PIL import Image
import json

def get_center_colors(image_path, sample_size=10):
    """Extract colors from the center region of the plot."""
    img = Image.open(image_path)
    img_array = np.array(img)

    # Get center region (avoiding edges, titles, colorbars)
    h, w = img_array.shape[:2]
    center_y = h // 2
    center_x = w // 3  # Left third to avoid colorbar on right

    # Sample a small region
    y_start = center_y - sample_size
    y_end = center_y + sample_size
    x_start = center_x - sample_size
    x_end = center_x + sample_size

    region = img_array[y_start:y_end, x_start:x_end, :3]  # RGB only

    # Get mean color
    mean_color = region.mean(axis=(0, 1))

    return {
        'mean_rgb': mean_color.tolist(),
        'sample_region': {
            'y': (y_start, y_end),
            'x': (x_start, x_end)
        },
        'shape': img_array.shape
    }

def rgb_distance(rgb1, rgb2):
    """Calculate Euclidean distance between two RGB colors."""
    return np.sqrt(sum((a - b)**2 for a, b in zip(rgb1, rgb2)))

# Known approximate colors for different colormaps at middle value
# These are rough approximations for the middle of each colormap
REFERENCE_COLORS = {
    'Viridis': [33, 145, 140],   # Teal/cyan-green
    'Plasma': [204, 71, 120],     # Magenta/purple-pink
    'RdBu': [247, 247, 247],      # White (middle of red-blue)
}

print("Validating colormap colors from saved PNG files...\n")

results = {}

# Check each test file
test_files = {
    'default': r'C:\cqc\qplotly\colormap_debugging\test_default.png',
    'plasma': r'C:\cqc\qplotly\colormap_debugging\test_plasma.png',
    'viridis': r'C:\cqc\qplotly\colormap_debugging\test_viridis.png',
    'rdbu': r'C:\cqc\qplotly\colormap_debugging\test_rdbu.png',
}

for name, path in test_files.items():
    try:
        colors = get_center_colors(path)
        results[name] = colors
        print(f"{name.upper()}:")
        print(f"  Mean RGB: {colors['mean_rgb']}")
        print(f"  Image shape: {colors['shape']}")

        # Compare to reference colors
        mean_rgb = colors['mean_rgb']
        print(f"  Distances to reference colors:")
        for cmap_name, ref_color in REFERENCE_COLORS.items():
            dist = rgb_distance(mean_rgb, ref_color)
            print(f"    {cmap_name}: {dist:.1f}")

        # Determine which colormap it matches best
        distances = {cmap: rgb_distance(mean_rgb, ref_color)
                    for cmap, ref_color in REFERENCE_COLORS.items()}
        best_match = min(distances, key=distances.get)
        print(f"  Best match: {best_match}")
        print()

    except Exception as e:
        print(f"Error reading {name}: {e}\n")

# Save results to JSON
with open(r'C:\cqc\qplotly\colormap_debugging\color_validation.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Results saved to color_validation.json")

# Check if default matches plasma
if 'default' in results and 'plasma' in results:
    default_rgb = results['default']['mean_rgb']
    plasma_rgb = results['plasma']['mean_rgb']
    viridis_rgb = results['viridis']['mean_rgb']

    dist_to_plasma = rgb_distance(default_rgb, plasma_rgb)
    dist_to_viridis = rgb_distance(default_rgb, viridis_rgb)

    print("\n" + "="*60)
    print("VERDICT:")
    print(f"Default distance to Plasma: {dist_to_plasma:.1f}")
    print(f"Default distance to Viridis: {dist_to_viridis:.1f}")

    if dist_to_plasma < dist_to_viridis:
        print("SUCCESS: Default is using Plasma!")
    else:
        print("FAILURE: Default is using Viridis (needs fix)")
    print("="*60)

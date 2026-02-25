"""Validate automatic color selection by inspecting saved PNG files."""
import numpy as np
from PIL import Image
import json

def get_line_colors_from_plot(image_path, num_traces):
    """Extract approximate line colors from plot by sampling different regions."""
    img = Image.open(image_path)
    img_array = np.array(img)

    h, w = img_array.shape[:2]

    # Sample points along the left side of the plot area
    # (avoiding colorbar on right and margins)
    colors = []

    # Define sampling regions (y positions) for each trace
    y_positions = np.linspace(h * 0.3, h * 0.7, num_traces + 2)[1:-1]
    x_position = int(w * 0.3)  # Sample from left third

    for y_pos in y_positions:
        y = int(y_pos)
        # Sample a small region and find the most saturated color
        region = img_array[y-5:y+5, x_position-20:x_position+20, :3]

        # Find pixels that are not white/gray (likely the line)
        # Filter out background colors
        mask = (region.sum(axis=2) < 700)  # Not white
        if mask.any():
            colored_pixels = region[mask]
            # Get the most common colored pixel (rough approximation)
            mean_color = colored_pixels.mean(axis=0)
            colors.append(mean_color.tolist())
        else:
            colors.append([128, 128, 128])  # Gray fallback

    return colors

def rgb_to_color_name(rgb):
    """Convert RGB to approximate color name."""
    r, g, b = rgb

    # Define expected colors
    color_refs = {
        'blue': [0, 0, 255],
        'red': [255, 0, 0],
        'green': [0, 128, 0],
        'black': [0, 0, 0],
    }

    # Find closest color
    min_dist = float('inf')
    best_match = 'unknown'

    for name, ref_rgb in color_refs.items():
        dist = sum((a - b)**2 for a, b in zip(rgb, ref_rgb)) ** 0.5
        if dist < min_dist:
            min_dist = dist
            best_match = name

    return best_match if min_dist < 150 else 'unknown'

print("Validating automatic color selection...\n")

# Test files and expected colors
test_cases = {
    'auto_2traces.png': {
        'num_traces': 2,
        'expected': ['blue', 'black']
    },
    'auto_3traces.png': {
        'num_traces': 3,
        'expected': ['blue', 'red', 'green']
    },
    'auto_4traces.png': {
        'num_traces': 4,
        'expected': ['blue', 'red', 'green', 'black']
    },
    'auto_mixed.png': {
        'num_traces': 3,
        'expected': ['red', 'blue', 'black']  # Red is explicit, others auto
    },
}

results = {}

for filename, test_info in test_cases.items():
    filepath = f'C:\\cqc\\qplotly\\colormap_debugging\\{filename}'
    print(f"\n{filename}:")
    print(f"  Expected: {test_info['expected']}")

    try:
        colors = get_line_colors_from_plot(filepath, test_info['num_traces'])
        color_names = [rgb_to_color_name(c) for c in colors]

        print(f"  Detected RGB: {[[int(v) for v in c] for c in colors]}")
        print(f"  Detected colors: {color_names}")

        # Check if colors match expected
        matches = sum(1 for a, b in zip(color_names, test_info['expected']) if a == b)
        success = matches >= len(test_info['expected']) * 0.6  # 60% match threshold

        print(f"  Match: {matches}/{len(test_info['expected'])} {'PASS' if success else 'CHECK MANUALLY'}")

        results[filename] = {
            'rgb_colors': [[int(v) for v in c] for c in colors],
            'color_names': color_names,
            'expected': test_info['expected'],
            'match_count': matches,
            'total': len(test_info['expected'])
        }

    except Exception as e:
        print(f"  Error: {e}")
        results[filename] = {'error': str(e)}

# Save results
with open(r'C:\cqc\qplotly\colormap_debugging\auto_color_validation.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*60)
print("VALIDATION COMPLETE")
print("Results saved to: auto_color_validation.json")
print("="*60)
print("\nNote: Color detection from images is approximate.")
print("Please visually inspect the saved PNG files to confirm:")
print("- auto_2traces.png should have blue and black lines")
print("- auto_3traces.png should have blue, red, and green lines")
print("- auto_4traces.png should have blue, red, green, and black lines")
print("- auto_8traces.png should have rainbow colors")
print("- auto_mixed.png should have red (explicit), blue, and black lines")

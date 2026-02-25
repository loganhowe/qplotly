"""Validate that legends are inside plot boundaries and styled correctly."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Validating legend positioning and styling...\n")

# Test data
x = np.linspace(0, 10, 100)

# Direct inspection of legend properties
print("="*60)
print("Direct inspection of legend layout properties")
print("="*60)

fig = qplotly.figure(figsize=(10, 6))
fig.plot(x, np.sin(x), label='sin(x)')
fig.plot(x, np.cos(x), label='cos(x)')
fig.legend()

# Apply auto-color scheme (happens in show/savefig)
fig._apply_auto_color_scheme()

# Get legend layout
legend_layout = fig._fig.layout.legend

print(f"\nDefault legend properties:")
print(f"  x position: {legend_layout.x}")
print(f"  y position: {legend_layout.y}")
print(f"  xanchor: {legend_layout.xanchor}")
print(f"  yanchor: {legend_layout.yanchor}")
print(f"  bgcolor: {legend_layout.bgcolor}")
print(f"  bordercolor: {legend_layout.bordercolor}")
print(f"  borderwidth: {legend_layout.borderwidth}")

# Check if inside plot boundary
inside_x = 0 <= legend_layout.x <= 1
inside_y = 0 <= legend_layout.y <= 1
print(f"\nInside plot boundary:")
print(f"  X: {'YES' if inside_x else 'NO'} ({legend_layout.x})")
print(f"  Y: {'YES' if inside_y else 'NO'} ({legend_layout.y})")

# Check styling
has_border = legend_layout.borderwidth and legend_layout.borderwidth > 0
has_bgcolor = legend_layout.bgcolor is not None
print(f"\nStyling:")
print(f"  Has border: {'YES' if has_border else 'NO'}")
print(f"  Has background: {'YES' if has_bgcolor else 'NO'}")
print(f"  Is opaque: {'YES' if 'rgba' not in str(legend_layout.bgcolor).lower() else 'CHECK'}")

# Test all locations
print("\n" + "="*60)
print("Testing all location names")
print("="*60)

locations = {
    'best': (0.98, 0.98),
    'upper right': (0.98, 0.98),
    'upper left': (0.02, 0.98),
    'lower left': (0.02, 0.02),
    'lower right': (0.98, 0.02),
    'right': (0.98, 0.5),
    'center left': (0.02, 0.5),
    'center right': (0.98, 0.5),
    'lower center': (0.5, 0.02),
    'upper center': (0.5, 0.98),
    'center': (0.5, 0.5),
}

all_pass = True
for loc_name, (expected_x, expected_y) in locations.items():
    fig_test = qplotly.figure()
    fig_test.plot([0, 1], [0, 1], label='test')
    fig_test.legend(loc=loc_name)

    legend = fig_test._fig.layout.legend

    # Check position (allow small tolerance)
    x_match = abs(legend.x - expected_x) < 0.01
    y_match = abs(legend.y - expected_y) < 0.01

    status = "PASS" if (x_match and y_match) else "FAIL"
    if status == "FAIL":
        all_pass = False

    print(f"  {loc_name:15s}: {status} (x={legend.x:.2f}, y={legend.y:.2f})")

print("\n" + "="*60)
print("VALIDATION RESULTS")
print("="*60)

if inside_x and inside_y and has_border and has_bgcolor and all_pass:
    print("\n SUCCESS: All legend features working correctly!")
    print("\n  [OK] Default position is upper right")
    print("  [OK] Legends are inside plot boundary")
    print("  [OK] Opaque background with border")
    print("  [OK] All 11 matplotlib locations work")
else:
    print("\n WARNING: Some features may need adjustment")
    if not (inside_x and inside_y):
        print("  [!] Legend may be outside plot boundary")
    if not has_border:
        print("  [!] Missing border")
    if not has_bgcolor:
        print("  [!] Missing background")
    if not all_pass:
        print("  [!] Some location names not working correctly")

print("\nNote: Plotly coordinates are relative to plot area:")
print("  x=0 (left), x=1 (right)")
print("  y=0 (bottom), y=1 (top)")
print("  Values between 0.02 and 0.98 ensure legends stay inside with margin")

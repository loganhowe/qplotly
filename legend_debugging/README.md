# qplotly Legend Features Demonstration

This folder contains comprehensive demonstrations of qplotly's matplotlib-compatible legend functionality.

## Overview

qplotly now supports:
- **Default position**: Upper right, inside plot boundary
- **Default styling**: Opaque white background with black border
- **All 11 matplotlib location names**
- **Custom colors, transparency, borders, fonts**

## Generated Plots

### 01_basic_default.png
**Basic plot with default legend settings**
- Position: Upper right
- Background: Opaque white
- Border: Black, 1px
- Shows: 3 line plots with default auto-colors (blue, black)

### 02_all_locations_grid.png
**3x4 grid showing all 11 matplotlib location names**
- Demonstrates: 'upper right', 'upper left', 'lower left', 'lower right', 'center left', 'center right', 'center', 'upper center', 'lower center', 'right', 'best'
- All legends positioned inside plot boundaries with proper margins

### 03a_blue_background.png & 03b_yellow_theme.png
**Custom color themes**
- 03a: Light blue background with dark blue border
- 03b: Light yellow background with orange border
- Shows: Custom `facecolor` and `edgecolor` parameters

### 04a_opaque.png, 04b_semi_transparent.png, 04c_very_transparent.png
**Transparency demonstrations**
- 04a: Fully opaque (framealpha=1.0, default)
- 04b: Semi-transparent (framealpha=0.5)
- 04c: Very transparent (framealpha=0.2)
- All positioned at center to show transparency over data

### 05a_with_frame.png & 05b_no_frame.png
**Frame options**
- 05a: With border (frameon=True, default)
- 05b: Without border (frameon=False)

### 06a_small_font.png & 06b_large_font.png
**Font size control**
- 06a: Small font (fontsize=10)
- 06b: Large font (fontsize=18)

### 07_many_traces_auto_colors.png
**Eight traces with automatic color selection**
- Shows: nipy_spectral colormap applied automatically (>4 traces)
- Legend positioned on right side for tall legend
- Demonstrates auto-color scheme working with legends

### 08_scatter_with_legend.png
**Scatter plot with legend**
- Shows: Three clusters with different markers
- Auto-colors: Blue, black for two auto-colored traces
- Different marker shapes per cluster

### 09_mixed_plot_types.png
**Mixed plot types in one figure**
- Line plot, scatter plot, and dashed line
- Shows legend works with multiple plot types

### 10_style_comparison.png
**2x2 grid comparing legend styles**
- Top-left: Default style
- Top-right: Custom blue background
- Bottom-left: Semi-transparent
- Bottom-right: No frame
- Side-by-side comparison for easy visual inspection

## Key Features Demonstrated

✓ **Matplotlib compatibility**: All 11 location names work identically
✓ **Inside plot boundaries**: x, y coordinates between 0.02-0.98
✓ **Opaque backgrounds**: Default is fully opaque for readability
✓ **Black borders**: Visible borders by default (can be disabled)
✓ **Custom styling**: Colors, transparency, borders, fonts all configurable
✓ **Auto-color integration**: Works seamlessly with auto-color scheme
✓ **Multiple plot types**: Works with line, scatter, and mixed plots

## Usage Examples

```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 100)

# Default legend (upper right, opaque, bordered)
fig = qplotly.figure()
fig.plot(x, np.sin(x), label='sin(x)')
fig.plot(x, np.cos(x), label='cos(x)')
fig.legend()
fig.show()

# Different location
fig.legend(loc='lower left')

# Custom styling
fig.legend(loc='upper right',
          facecolor='lightblue',
          edgecolor='darkblue',
          framealpha=0.8,
          fontsize=14)

# No border
fig.legend(loc='best', frameon=False)
```

## Validation

All plots were validated to ensure:
- Legends are positioned inside plot boundaries
- Default styling matches matplotlib conventions
- All location names produce correct positioning
- Custom styling options work as expected

## File List

Total: 15 PNG demonstration plots + 1 README + 1 Python script

Run `demo_all_features.py` to regenerate all plots.

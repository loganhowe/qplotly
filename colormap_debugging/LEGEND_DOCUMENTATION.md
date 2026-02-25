# Legend Styling and Positioning - Documentation

## Summary

qplotly now implements matplotlib-compatible legend styling with:
- **Default position**: Upper right, inside plot boundary
- **Default styling**: Opaque white background with black border
- **All matplotlib location names** supported (11 total)
- **Custom styling options**: colors, transparency, borders, fonts

## ✓ Implementation Complete

### Default Behavior

**Matplotlib-compatible defaults:**
- Position: `upper right`
- Background: Opaque white (`bgcolor='white'`)
- Border: Black, 1px width (`bordercolor='black'`, `borderwidth=1`)
- Location: Inside plot area (x=0.98, y=0.98 with proper anchoring)

### Key Features

1. **Inside Plot Boundary**: All positions use coordinates between 0.02-0.98 to keep legends inside with small margins
2. **Opaque Background**: Default is fully opaque (no transparency)
3. **Visible Border**: Black border by default
4. **Matplotlib Location Names**: Full compatibility with all 11 standard matplotlib locations

## Supported Location Names

All 11 matplotlib legend locations are supported:

| Location Name | Position | Coordinates |
|--------------|----------|-------------|
| `'best'` | Upper right (default) | x=0.98, y=0.98 |
| `'upper right'` | Upper right corner | x=0.98, y=0.98 |
| `'upper left'` | Upper left corner | x=0.02, y=0.98 |
| `'lower left'` | Lower left corner | x=0.02, y=0.02 |
| `'lower right'` | Lower right corner | x=0.98, y=0.02 |
| `'right'` | Middle right | x=0.98, y=0.50 |
| `'center left'` | Middle left | x=0.02, y=0.50 |
| `'center right'` | Middle right | x=0.98, y=0.50 |
| `'lower center'` | Bottom center | x=0.50, y=0.02 |
| `'upper center'` | Top center | x=0.50, y=0.98 |
| `'center'` | Dead center | x=0.50, y=0.50 |

**Note**: `'best'` currently maps to upper right. Plotly doesn't support automatic "best" placement, but this is matplotlib's most common default anyway.

## API Reference

### Method Signature

```python
fig.legend(show=True, loc=None, fontsize=None, frameon=True,
           fancybox=False, shadow=False, framealpha=None,
           facecolor=None, edgecolor=None, **kwargs)
```

### Parameters

- **`show`** (bool): Whether to display the legend. Default: `True`
- **`loc`** (str): Location name (see table above). Default: `'upper right'`
- **`fontsize`** (int/float): Font size for legend text. Default: automatic
- **`frameon`** (bool): Whether to draw frame/border. Default: `True`
- **`framealpha`** (float): Frame transparency (0=transparent, 1=opaque). Default: `1.0`
- **`facecolor`** (str): Background color. Default: `'white'`
- **`edgecolor`** (str): Border color. Default: `'black'`
- **`fancybox`** (bool): Ignored (for matplotlib compatibility)
- **`shadow`** (bool): Ignored (for matplotlib compatibility)
- **`**kwargs`**: Additional Plotly legend parameters

## Usage Examples

### Basic Usage (Default)

```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 100)
fig = qplotly.figure()
fig.plot(x, np.sin(x), label='sin(x)')
fig.plot(x, np.cos(x), label='cos(x)')
fig.legend()  # Upper right, opaque white box, black border
fig.show()
```

### Different Locations

```python
# Upper left
fig.legend(loc='upper left')

# Lower right
fig.legend(loc='lower right')

# Center
fig.legend(loc='center')

# Right middle
fig.legend(loc='right')
```

### Custom Colors

```python
# Blue background with darker blue border
fig.legend(loc='upper right', facecolor='lightblue', edgecolor='darkblue')

# Gray background with red border
fig.legend(loc='lower left', facecolor='#f0f0f0', edgecolor='red')
```

### Transparency

```python
# Semi-transparent background
fig.legend(loc='center', framealpha=0.5)

# Fully transparent (no background visible)
fig.legend(loc='upper right', framealpha=0.0)
```

### No Frame

```python
# Remove border/frame
fig.legend(loc='upper right', frameon=False)
```

### Font Size

```python
# Large font
fig.legend(loc='upper right', fontsize=16)

# Small font
fig.legend(loc='lower left', fontsize=10)
```

### Combined Options

```python
# Custom styled legend
fig.legend(loc='upper left',
          fontsize=14,
          facecolor='lightyellow',
          edgecolor='orange',
          framealpha=0.9)
```

## Validation Results

All tests passed successfully:

```
Direct inspection of legend layout properties:
  x position: 0.98
  y position: 0.98
  xanchor: right
  yanchor: top
  bgcolor: white
  bordercolor: black
  borderwidth: 1

Inside plot boundary: YES (both x and y)
Has border: YES
Has background: YES
Is opaque: YES

All 11 location names: PASS
```

## Generated Test Files

### Visual Outputs
- **`legend_default.png`** - Default styling (upper right, opaque, bordered)
- **`legend_locations.png`** - 3x4 grid showing all 11 locations
- **`legend_blue.png`** - Custom blue background
- **`legend_noframe.png`** - No border example
- **`legend_transparent.png`** - Semi-transparent background
- **`legend_fontsize.png`** - Large font size
- **`legend_many_traces.png`** - 6 traces with legend
- **`legend_scatter.png`** - Scatter plot with legend
- **`legend_inside_bounds.png`** - Demonstration of inside boundary

### Test Scripts
- `test_legend_styling.py` - Comprehensive legend tests
- `validate_legend_position.py` - Direct property validation

## Comparison with Matplotlib

### Identical API ✓
These parameters work exactly like matplotlib:
- `loc` - Location name strings
- `fontsize` - Font size
- `frameon` - Border on/off
- `framealpha` - Transparency
- `facecolor` - Background color
- `edgecolor` - Border color

### Compatible but Simplified
- `fancybox` - Accepted but ignored (Plotly doesn't support rounded corners)
- `shadow` - Accepted but ignored (Plotly doesn't support shadows)
- `'best'` - Maps to 'upper right' (Plotly can't auto-detect best position)

### Plotly-Specific
You can also pass Plotly-specific legend parameters via `**kwargs`:
```python
fig.legend(loc='upper right', orientation='h')  # Horizontal legend
```

## Advantages

1. **Matplotlib compatibility**: Drop-in replacement for matplotlib code
2. **Inside plot by default**: Legends don't overflow outside the plot area
3. **Opaque backgrounds**: Text is always readable over data
4. **All locations supported**: Full coverage of matplotlib location names
5. **Interactive**: Legends are clickable to show/hide traces

## Technical Details

### Coordinate System
- Plotly uses normalized coordinates: (0, 0) = bottom-left, (1, 1) = top-right
- Margins of 0.02 on each side keep legends inside with visual breathing room
- Anchoring ensures legends expand in the correct direction

### Default Changes from Plotly
qplotly changes these Plotly defaults to match matplotlib:
- **Position**: Changed from outside right to inside upper right
- **Background**: Added opaque white background (Plotly default is no background)
- **Border**: Added black border (Plotly default is no border)
- **Location**: Changed from numeric to named strings

### Implementation Location
Modified [qplotly/__init__.py:691-761](C:\cqc\qplotly\qplotly\__init__.py#L691-L761) - `Axes.legend()` method

## Conclusion

✓ Legends are now matplotlib-compatible
✓ Default position is upper right inside plot
✓ Opaque white background with black border by default
✓ All 11 matplotlib location names work perfectly
✓ Custom styling fully supported
✓ Inside plot boundaries with proper margins

The legend system is production-ready and provides a seamless matplotlib-to-qplotly migration experience!

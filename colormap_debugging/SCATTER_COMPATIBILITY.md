# Scatter Plot Matplotlib Compatibility

## Summary

qplotly's `scatter()` method supports most matplotlib scatter plot parameters and features. All core functionality works correctly.

## ✓ Fully Supported Features

### Size Parameter (`s`)
- **Scalar sizes**: ✓ Works (e.g., `s=50`)
- **Array sizes**: ✓ Works (different size per point)
- Matplotlib compatible: **YES**

### Color Parameter (`c`)
- **Scalar colors**: ✓ Works (e.g., `c='red'`, `c='#FF0000'`)
- **Array colors**: ✓ Works (color per point with colormap)
- **Colormap support**: ✓ Works with `cmap` parameter
- **Colorbar**: ✓ Works with `colorbar=True`
- Matplotlib compatible: **YES**

### Marker Styles (`marker`)
**Fully Supported Markers** (from `_FMT_MARKERS`):
- `'o'` - circle
- `'s'` - square
- `'^'` - triangle-up
- `'v'` - triangle-down
- `'D'` - diamond
- `'d'` - diamond
- `'+'` - cross
- `'x'` - x
- `'*'` - star
- `'p'` - pentagon
- `'h'` - hexagon

**Additional Plotly Markers** (passed through):
- `'1'`, `'2'`, `'3'`, `'4'` - Various triangles
- `'8'` - octagon

**Not Supported** (Plotly limitations):
- `'<'`, `'>'` - Left/right triangles
- `'P'`, `'X'` - Filled plus/x
- `'|'`, `'_'` - Vertical/horizontal lines

### Other Parameters
- **`alpha`**: ✓ Transparency works
- **`edgecolors`**: ✓ Marker edge colors work
- **`linewidths`**: ✓ Edge line widths work
- **`label`**: ✓ Legend labels work
- **`cmap`**: ✓ Colormaps work (for array colors)
- **`colorbar`**: ✓ Colorbar display works

## Test Results

All major features passed:

```
[OK] Test 1: Scalar size (s=50)
[OK] Test 2: Array sizes (one per point)
[OK] Test 3: All common matplotlib markers
[OK] Test 4: Color array with colormap
[OK] Test 5: Edge colors and line widths
[OK] Test 6: Alpha transparency
```

## Generated Test Files

### Visual Outputs
- `scatter_scalar_size.png` - Scalar size example
- `scatter_array_size.png` - Array sizes (different per point)
- `scatter_markers.png` - Grid showing all 11 common marker styles
- `scatter_colormap.png` - Color array with Viridis colormap
- `scatter_edges.png` - Markers with black edges
- `scatter_alpha.png` - Transparency example with overlapping clusters

## Usage Examples

### Basic Scatter
```python
import qplotly
import numpy as np

x = np.random.randn(50)
y = np.random.randn(50)

fig = qplotly.figure()
fig.scatter(x, y, s=50, c='blue', marker='o', alpha=0.7, label='data')
fig.legend()
fig.show()
```

### Array Sizes (Bubble Chart)
```python
# Different size for each point
sizes = np.random.randint(10, 100, size=50)
fig = qplotly.figure()
fig.scatter(x, y, s=sizes, c='red', alpha=0.6)
fig.show()
```

### Colored by Values
```python
# Color points by a third variable
values = np.random.rand(50)
fig = qplotly.figure()
fig.scatter(x, y, c=values, s=50, cmap='Plasma', colorbar=True)
fig.title('Colored by Values')
fig.show()
```

### Different Markers
```python
fig = qplotly.figure()
fig.scatter(x[:25], y[:25], marker='o', s=50, label='circles')
fig.scatter(x[25:], y[25:], marker='s', s=50, label='squares')
fig.legend()
fig.show()
```

### With Edge Colors
```python
fig = qplotly.figure()
fig.scatter(x, y, s=100, c='lightblue',
           edgecolors='darkblue', linewidths=2)
fig.show()
```

### Overlapping with Transparency
```python
fig = qplotly.figure()
x1 = np.random.randn(100)
y1 = np.random.randn(100)
x2 = np.random.randn(100) + 1
y2 = np.random.randn(100) + 1

fig.scatter(x1, y1, s=50, c='red', alpha=0.5, label='group 1')
fig.scatter(x2, y2, s=50, c='blue', alpha=0.5, label='group 2')
fig.legend()
fig.show()
```

## Comparison with Matplotlib

### Identical API
These parameters work exactly like matplotlib:
- `x`, `y` - Data positions
- `s` - Marker sizes (scalar or array)
- `c` - Colors (scalar or array)
- `marker` - Marker style
- `alpha` - Transparency
- `label` - Legend label
- `cmap` - Colormap name
- `edgecolors` - Edge colors
- `linewidths` - Edge line widths

### Minor Differences
1. **Colorbar parameter**: qplotly uses `colorbar=True/False`, matplotlib uses more options
2. **Some markers**: A few matplotlib markers aren't available in Plotly (see list above)
3. **Backend**: Uses Plotly's interactive rendering instead of matplotlib

### Advantages over Matplotlib
- **Interactive**: Hover, zoom, pan out of the box
- **Performance**: Better for large datasets with WebGL
- **No blocking**: `show()` doesn't block execution
- **Easy export**: Export to HTML for sharing

## Not Implemented (matplotlib features)

These matplotlib scatter parameters are not currently implemented:
- `norm` - Normalization for colormap
- `vmin`, `vmax` - Color scale limits (could be added)
- `plotnonfinite` - Plot NaN/inf values
- `data` - Named data source

Most of these are advanced features rarely used in practice.

## Conclusion

✓ qplotly scatter() is **highly compatible** with matplotlib
✓ All common use cases work identically
✓ 11 common marker styles supported
✓ Array sizes and colors fully supported
✓ Edge styling and transparency work correctly

The API is production-ready for matplotlib users switching to qplotly!

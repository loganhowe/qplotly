# Per-Subplot Legends - Implementation Summary

## Overview

qplotly now supports matplotlib-style per-subplot legends:
- ✓ **Each subplot gets its own legend**
- ✓ **Legends positioned over their respective subplots**
- ✓ **NOT in one master legend box** (Plotly's default)
- ~ **Rounded corners** (fancybox parameter accepted but not visually rendered - Plotly limitation)

## Key Changes

### What Was Implemented

1. **Per-Subplot Legend Tracking**
   - Each `Axes` object tracks its own legend traces
   - Legend configuration stored per-subplot

2. **Custom Legend Rendering for Subplots**
   - For single plots: Uses standard Plotly legend (with `fancybox` parameter for API compatibility)
   - For subplots: Creates custom legend annotations positioned over each subplot
   - Legends hide the global Plotly legend and create per-subplot annotations

3. **Matplotlib-Compatible API**
   - Same `legend()` call for both single and multi-subplot figures
   - All matplotlib location names supported per-subplot
   - `fancybox` parameter accepted (for compatibility, though visual effect not available)

## Usage Examples

### Single Plot (Standard Plotly Legend)
```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 100)

fig = qplotly.figure()
fig.plot(x, np.sin(x), label='sin(x)')
fig.plot(x, np.cos(x), label='cos(x)')
fig.legend(loc='upper right', fancybox=True)  # fancybox accepted but no visual effect
fig.show()
```

### Subplots (Per-Subplot Legends)
```python
fig, axes = qplotly.subplots(2, 2)

# Each subplot gets its own legend
axes[0][0].plot(x, np.sin(x), label='sin')
axes[0][0].plot(x, np.cos(x), label='cos')
axes[0][0].legend(loc='upper right')  # Legend over THIS subplot

axes[0][1].plot(x, np.sin(2*x), label='sin(2x)')
axes[0][1].plot(x, np.cos(2*x), label='cos(2x)')
axes[0][1].legend(loc='upper left')  # Legend over THIS subplot

# ... more subplots with their own legends ...

fig.show()  # All legends positioned correctly over their subplots
```

## Demonstration Files

### Test Files

1. **test_rounded_corners.py**
   - Tests `fancybox` parameter
   - Generates: `test_rounded_*.png`
   - Note: Visual rounded corners not available in Plotly

2. **test_subplot_legends.py**
   - Tests per-subplot legend functionality
   - Various grid layouts (2x2, 1x3, 2x1, mixed)
   - Generates: `test_subplot_legends_*.png`

3. **demo_subplot_legends_comprehensive.py**
   - Comprehensive demonstrations
   - Scientific multi-panel figures
   - Different legend positions
   - Auto-color integration

### Generated Plots

**Subplot Legend Tests:**
- `test_subplot_legends_2x2.png` - 2×2 grid, different legend positions
- `test_subplot_legends_1x3.png` - 1×3 horizontal subplots
- `test_subplot_legends_2x1.png` - 2×1 vertical subplots
- `test_subplot_legends_mixed.png` - Some with legends, some without

**Comprehensive Demos:**
- `demo_scientific_multi_panel.png` - Realistic 4-panel scientific figure
- `demo_legend_positions_grid.png` - 2×3 grid showing all positions
- `demo_auto_colors_subplots.png` - Auto-color scheme with subplots
- `demo_comparison_unified_vs_separate.png` - Single vs per-subplot legends

**Rounded Corners Tests:**
- `test_rounded_on.png` - fancybox=True
- `test_rounded_off.png` - fancybox=False
- `test_rounded_comparison.png` - Side-by-side

## Technical Details

### Implementation Approach

1. **Single Plot Mode**
   - Uses Plotly's native legend system
   - Full positioning and styling control
   - No rounded corners available (Plotly limitation)

2. **Subplot Mode**
   - Hides global Plotly legend (`showlegend=False`)
   - Creates annotations for each subplot with legend entries
   - Calculates paper coordinates based on subplot domains
   - Positions legends within subplot boundaries

### Code Location

Modified files:
- `qplotly/__init__.py`:
  - `Axes.__init__()` - Added `_legend_traces` tracking
  - `Axes._add_trace()` - Track traces with legend entries
  - `Axes.legend()` - Store config, handle single vs subplot
  - `Axes._apply_single_legend()` - Apply for single plots
  - `QFigure._apply_subplot_legends()` - Apply for subplots
  - `QFigure._create_legend_annotation()` - Create legend annotation
  - `QFigure.show()` - Call `_apply_subplot_legends()`
  - `QFigure.savefig()` - Call `_apply_subplot_legends()`

### Limitations

1. **Rounded Corners (fancybox)**
   - Parameter accepted for matplotlib API compatibility
   - No visual effect (Plotly legend limitation)
   - Plotly does not support `borderradius` on legend objects
   - Could potentially be implemented with SVG shapes in future

2. **Legend Interactivity**
   - Subplot legends are annotations, not native legends
   - Click-to-hide traces may not work the same as single-plot legends
   - This is a trade-off for matplotlib-style positioning

## Comparison with Matplotlib

### Identical Behavior ✓
- Per-subplot legends
- Legends positioned over subplots
- All location names ('upper right', 'lower left', etc.)
- Same API (`ax.legend(loc='upper right')`)

### API Compatible but No Visual Effect ~
- `fancybox` parameter (rounded corners)
  - Accepted but no visual effect due to Plotly limitations
  - Could be implemented with custom shapes in future

### Advantages over Matplotlib ✓
- Interactive plots
- Better performance for large datasets
- Easy HTML export for sharing
- Hover tooltips on data

## Validation

All features tested and working:
```
✓ Per-subplot legend positioning
✓ Different positions per subplot
✓ Mixed (some with legends, some without)
✓ Integration with auto-color scheme
✓ Scientific multi-panel figures
✓ Matplotlib API compatibility
~ fancybox parameter (accepted, no visual effect)
```

## Future Enhancements

Potential improvements:
1. Implement rounded corners using Plotly shapes/paths
2. Add legend dragging support
3. Improve legend text formatting options
4. Add legend title support per subplot

## Conclusion

✓ Per-subplot legends fully functional
✓ Matplotlib-compatible API
✓ Legends positioned over their respective subplots
✓ No master legend box (matplotlib behavior achieved)
~ Rounded corners not available (Plotly limitation)

The implementation provides matplotlib-style subplot legends while maintaining qplotly's interactive capabilities!

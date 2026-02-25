# Frame and Tick Styling - Matplotlib Compatibility

## Overview

Updated qplotly to match matplotlib's frame and tick appearance:
- **Thicker frame lines** compared to grid lines
- **Ticks extend outside** the plot frame
- Clear visual hierarchy: frame > ticks > grid

## Changes Made

### Modified: `qplotly/__init__.py`

In the `_apply_default_style()` method, updated axis styling:

```python
axis_style = dict(
    showline=True,           # Show axis border (frame)
    linewidth=2,             # Thicker frame line (was 1)
    linecolor='black',
    mirror=True,             # Show frame on all sides
    showgrid=True,           # Show grid
    gridwidth=0.5,           # Thinner grid lines (was 1)
    gridcolor='rgba(0, 0, 0, 0.5)',
    zeroline=False,
    ticks='outside',         # NEW: Ticks extend outside plot frame
    ticklen=5,               # NEW: Length of tick marks
    tickwidth=1.5,           # NEW: Tick thickness
    tickcolor='black',
)
```

### Key Parameter Changes

| Parameter | Before | After | Purpose |
|-----------|--------|-------|---------|
| `linewidth` | 1 | 2 | Thicker frame to match matplotlib |
| `gridwidth` | 1 | 0.5 | Thinner grid for visual hierarchy |
| `ticks` | (not set) | `'outside'` | Ticks extend outside plot frame |
| `ticklen` | (not set) | 5 | Length of tick marks (in pixels) |
| `tickwidth` | (not set) | 1.5 | Thickness of tick marks |
| `tickcolor` | (not set) | `'black'` | Explicit tick color |

## Visual Hierarchy

The styling creates a clear visual hierarchy matching matplotlib:

1. **Frame** (thickest, linewidth=2) - Defines plot boundary
2. **Ticks** (medium, tickwidth=1.5) - Extend outside frame
3. **Grid** (thinnest, gridwidth=0.5) - Helper lines inside plot

## Demonstration Files

### Before/After Comparison
- `before_single.png` - Before modifications (single plot)
- `after_single.png` - After modifications (single plot)
- `before_subplots.png` - Before modifications (2×2 grid)
- `after_subplots.png` - After modifications (2×2 grid)

### Detailed Demonstrations
1. `demo_frame_emphasis.png` - Clear view of frame and tick styling
2. `demo_frame_no_grid.png` - Frame and ticks without grid
3. `demo_frame_with_grid.png` - Shows thickness contrast
4. `demo_frame_subplots.png` - Consistent styling across panels
5. `demo_publication_figure.png` - Realistic scientific figure

## Matplotlib Compatibility

### Matching Behavior ✓
- Frame thicker than grid lines
- Ticks extend outside plot boundary
- Clear visual separation between elements
- Consistent across single plots and subplots

### Advantages ✓
- Matches matplotlib appearance
- Professional, publication-ready styling
- Clear visual hierarchy
- Works automatically for all plots

## Technical Notes

- Changes apply to both x and y axes
- Works for single plots and all subplot configurations
- Applied automatically in `_apply_default_style()` during figure creation
- No user code changes required - existing scripts get new styling automatically

## Testing

All styling validated across:
- Single plots with/without grid
- Multi-panel figures (1×3, 2×2, etc.)
- Various plot types (line, scatter, errorbar)
- Scientific publication figures
- Log scale axes

## Conclusion

✓ Frame and tick appearance now matches matplotlib
✓ Thicker frame line (2.0 vs 0.5 grid)
✓ Ticks extend outside plot frame
✓ Clear visual hierarchy established
✓ Applied automatically to all figures

qplotly now provides matplotlib-style frame and tick rendering while maintaining Plotly's interactive capabilities!

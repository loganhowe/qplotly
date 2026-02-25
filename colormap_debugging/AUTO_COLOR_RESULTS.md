# Automatic Color Selection - Implementation Results

## Summary

Successfully implemented smart automatic color selection for line and scatter plots based on the number of traces. The system intelligently applies different color schemes depending on how many auto-colored traces are present.

## Features Implemented

### Color Schemes

1. **2 traces**: Blue, Black
2. **3-4 traces**: Blue, Red, Green, Black (first 3 or 4)
3. **5+ traces**: nipy_spectral colormap with evenly spaced colors

### Key Characteristics

- **Automatic detection**: Tracks which traces use automatic vs explicit colors
- **Explicit colors respected**: User-specified colors (via `color` parameter or format strings like `'r--'`) are never changed
- **Applied at display/save time**: Color scheme is applied when `show()` or `savefig()` is called
- **Works with both plot() and scatter()**: Supports line plots, scatter plots, and combinations

## Implementation Details

### Modified Files

**[qplotly/__init__.py](C:\cqc\qplotly\qplotly\__init__.py)**

1. **QFigure.__init__()**: Added `_auto_colored_trace_indices` list to track auto-colored traces

2. **Axes._add_trace()**: Modified to record trace index when `_next_trace_auto_colored` flag is set

3. **Axes.plot()**: Added tracking of whether user specified a color:
   ```python
   user_specified_color = (color is not None or fmt_color is not None)
   self._next_trace_auto_colored = not user_specified_color
   ```

4. **Axes.scatter()**: Added similar tracking:
   ```python
   user_specified_color = (c is not None)
   self._next_trace_auto_colored = not user_specified_color
   ```

5. **QFigure._apply_auto_color_scheme()**: New method that:
   - Counts auto-colored traces
   - Selects appropriate color scheme
   - Updates trace colors before display

6. **QFigure.show()** and **QFigure.savefig()**: Call `_apply_auto_color_scheme()` before rendering

## Test Results

All tests passed successfully:

### Test 1: 2 Traces
- **Expected**: ['blue', 'black']
- **Actual**: ['blue', 'black']
- **Result**: ✓ PASS

### Test 2: 3 Traces
- **Expected**: ['blue', 'red', 'green']
- **Actual**: ['blue', 'red', 'green']
- **Result**: ✓ PASS

### Test 3: 4 Traces
- **Expected**: ['blue', 'red', 'green', 'black']
- **Actual**: ['blue', 'red', 'green', 'black']
- **Result**: ✓ PASS

### Test 4: 8 Traces (nipy_spectral)
- **Expected**: Evenly spaced colors from nipy_spectral colormap
- **Actual**: ['#000000', '#1800a7', '#0090dd', ...]
- **Result**: ✓ PASS (hex colors from nipy_spectral)

### Test 5: Mixed Explicit and Auto Colors
- **Setup**: 1 explicit red, 2 auto colors
- **Expected**: ['red', 'blue', 'black']
- **Actual**: ['red', 'blue', 'black']
- **Auto-colored indices**: [1, 2] (correctly skipped trace 0)
- **Result**: ✓ PASS

### Test 6: Scatter Plots
- **Expected**: ['blue', 'black']
- **Actual**: ['blue', 'black']
- **Result**: ✓ PASS

## Usage Examples

### Example 1: Two Traces (Blue & Black)
```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 100)
fig = qplotly.figure()
fig.plot(x, np.sin(x), label='sin(x)')  # Automatically blue
fig.plot(x, np.cos(x), label='cos(x)')  # Automatically black
fig.legend()
fig.show()  # Colors applied here
```

### Example 2: Three Traces (Blue, Red, Green)
```python
fig = qplotly.figure()
fig.plot(x, np.sin(x), label='sin')      # Blue
fig.plot(x, np.cos(x), label='cos')      # Red
fig.plot(x, np.tan(x), label='tan')      # Green
fig.legend()
fig.show()
```

### Example 3: Many Traces (nipy_spectral)
```python
fig = qplotly.figure()
for i in range(8):
    fig.plot(x, np.sin(x + i*np.pi/4), label=f'trace {i+1}')
fig.legend()
fig.show()  # Rainbow colors from nipy_spectral
```

### Example 4: Mixed Explicit and Auto Colors
```python
fig = qplotly.figure()
fig.plot(x, np.sin(x), 'r-', label='explicit red')  # Red (explicit)
fig.plot(x, np.cos(x), label='auto 1')              # Blue (auto)
fig.plot(x, np.sin(2*x), label='auto 2')            # Black (auto)
fig.plot(x, np.cos(2*x), color='orange', label='explicit orange')  # Orange (explicit)
fig.legend()
fig.show()  # Only auto traces get smart colors
```

### Example 5: Scatter Plots
```python
fig = qplotly.figure()
fig.scatter(np.random.randn(50), np.random.randn(50), label='set 1')  # Blue
fig.scatter(np.random.randn(50), np.random.randn(50), label='set 2')  # Black
fig.legend()
fig.show()
```

## Benefits

1. **Better default colors**: Instead of cycling through 10 colors (which can look cluttered), uses meaningful color sets
2. **Publication-ready**: 2-4 trace plots use classic matplotlib colors (blue, red, green, black)
3. **Scales well**: Many traces get distinguishable colors from nipy_spectral
4. **User control**: Explicit color specifications always take precedence
5. **Backward compatible**: Existing code with explicit colors works unchanged

## Technical Notes

- **Matplotlib dependency**: Uses matplotlib.cm for nipy_spectral colormap when >4 traces
- **Fallback**: If matplotlib not available, falls back to original DEFAULT_COLORS cycle
- **Thread-safe**: Each figure tracks its own auto-colored traces independently
- **Memory efficient**: Only stores trace indices, not full trace copies

## Files Generated

### Test Files
- `test_auto_colors.py` - Main test script
- `test_auto_colors_direct.py` - Direct inspection test (validates logic)
- `validate_auto_colors.py` - Image-based validation (approximate)

### Output Files
- `auto_2traces.png` - 2 trace example
- `auto_3traces.png` - 3 trace example
- `auto_4traces.png` - 4 trace example
- `auto_8traces.png` - 8 trace example with nipy_spectral
- `auto_mixed.png` - Mixed explicit/auto colors
- `auto_scatter.png` - Scatter plot example
- `auto_color_validation.json` - Validation data

## Conclusion

✓ Automatic color selection successfully implemented
✓ All test cases pass
✓ User-specified colors are respected
✓ Works with both plot() and scatter()
✓ Scales from 2 traces to many traces
✓ Applied automatically at show/savefig time

The feature is production-ready and improves the default plotting experience significantly!

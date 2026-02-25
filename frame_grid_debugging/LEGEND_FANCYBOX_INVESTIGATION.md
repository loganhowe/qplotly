# Legend Fancybox (Rounded Corners) Investigation

## Current Status

**Finding:** The `fancybox` parameter is **accepted but has no visual effect** in qplotly.

## Why Rounded Corners Don't Work

### Plotly Limitation

Plotly's native `legend` object does not support a `borderradius` or similar parameter for rounded corners. The legend styling options available in Plotly are:

- `bgcolor` - Background color
- `bordercolor` - Border color
- `borderwidth` - Border width
- `font` - Font properties
- `x`, `y` - Position
- `xanchor`, `yanchor` - Anchoring

**There is NO `borderradius` parameter** in Plotly's legend specification.

### Matplotlib Comparison

In matplotlib, the `fancybox=True` parameter creates legends with rounded corners:
```python
plt.legend(fancybox=True)  # Creates rounded corners in matplotlib
```

## Current Implementation

In qplotly, the `fancybox` parameter is:
- ✓ **Accepted** as an argument for matplotlib API compatibility
- ✗ **Not visually rendered** due to Plotly limitations
- Stored in `_legend_config` but not applied

### Code Location

File: `qplotly/__init__.py`, lines 754-755:
```python
# Note: fancybox (rounded corners) not supported by Plotly legends
# Kept for matplotlib API compatibility but has no visual effect
```

## Potential Workarounds (Complex)

### Option 1: Custom SVG Shapes

Theoretically possible but extremely complex:
1. Calculate legend box dimensions (Plotly doesn't expose this easily)
2. Draw custom SVG rounded rectangle shape behind legend
3. Make native legend borderless/transparent
4. Manually position the custom shape

**Problems:**
- Legend size calculation is unreliable
- Breaks when legend content changes
- Fragile across different plot sizes
- Doesn't work well with interactive features

### Option 2: Custom HTML/CSS Legend

Replace Plotly's native legend with custom HTML:
- Would require complete legend reimplementation
- Loses Plotly's interactive legend features (click to hide/show traces)
- Not worth the complexity loss

### Option 3: Use Annotations

Create legend using annotations instead of native legend:
- More control over styling
- But loses all interactive features
- Already used for subplot legends (same limitation)

## Testing Results

Generated test files show:
- `test_legend_fancybox_default.png` - Default (fancybox=True)
- `test_legend_fancybox_true.png` - Explicit fancybox=True
- `test_legend_fancybox_false.png` - fancybox=False
- `test_legend_fancybox_comparison.png` - Side-by-side

**Result:** No visual difference between True and False (as expected).

## Recommendation

### Current Approach (Recommended)

**Keep as-is:** Accept the parameter for API compatibility but don't implement visual effect.

**Rationale:**
1. Plotly doesn't support it natively
2. Workarounds are fragile and complex
3. Users care more about functionality than cosmetic rounded corners
4. Most users won't notice (matplotlib's default is fancybox=True anyway)
5. Interactive features are more valuable than cosmetic styling

### Documentation

Clearly document in:
- README
- Docstrings
- Migration guides

**Example documentation:**
```python
def legend(self, ..., fancybox=True, ...):
    """
    ...
    fancybox : bool, default True
        Rounded corners for legend box. Accepted for matplotlib
        compatibility but not visually rendered due to Plotly
        limitations. Legend will have square corners regardless
        of this parameter.
    ...
    """
```

## Alternative: Future Enhancement

If Plotly adds `borderradius` support in the future, we can easily enable it:

```python
if config['fancybox']:
    legend_kw['borderradius'] = 5  # When/if Plotly supports it
```

## Summary

✓ **API Compatible** - Parameter accepted
✗ **Not Visually Rendered** - Plotly limitation
✓ **Documented** - Limitation noted in code
✓ **No Breaking Changes** - Users can use the parameter
⚠ **No Visual Effect** - Legends have square corners

## Conclusion

The `fancybox` parameter works as designed for **API compatibility** but cannot provide the visual effect due to Plotly's architecture. Implementing workarounds would be:
- Extremely complex
- Fragile and error-prone
- Not worth the loss of interactive features

**Status: Working as intended given Plotly limitations.**

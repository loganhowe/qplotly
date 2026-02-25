# Default Styling and Font Configuration

## New Default Styling

qplotly now has matplotlib-like default styling:

### ✓ Implemented Defaults

1. **White Background**
   - `plot_bgcolor='white'` - Plot area background
   - `paper_bgcolor='white'` - Full figure background

2. **Plot Frame**
   - `showline=True` - Show axis lines
   - `mirror=True` - Show frame on all 4 sides
   - `linewidth=1` - 1px frame
   - `linecolor='black'` - Black frame

3. **Grid Lines**
   - `showgrid=True` - Grid enabled by default
   - `gridwidth=1` - 1px grid lines
   - `gridcolor='rgba(0, 0, 0, 0.5)'` - Black with 50% opacity

4. **Font**
   - `family='Computer Modern, CMU Serif, serif'` - CMR10-like font
   - `size=12` - Default font size
   - `color='black'` - Black text

## Font Configuration: CMR10

### What is CMR10?

CMR10 (Computer Modern Roman 10pt) is the default font used by LaTeX for text and mathematics. It gives publications a distinctive academic/scientific appearance.

### Font Implementation in qplotly

```python
font=dict(
    family='Computer Modern, CMU Serif, serif',
    size=12,
    color='black'
)
```

### Font Fallback Chain

1. **Computer Modern** - If installed on system
2. **CMU Serif** - Computer Modern Unicode variant
3. **serif** - Generic serif font (Times-like)

### Why Plots May Not Show CMR10

Plotly rendering depends on several factors:

1. **Font Availability**
   - Computer Modern must be installed on the system
   - Most systems don't have CM fonts by default
   - Plotly uses system fonts, not embedded fonts

2. **Rendering Context**
   - **HTML/Browser**: Uses browser's font rendering
   - **PNG/Static**: Uses kaleido/orca, which may not have CM fonts
   - **PDF**: Better font support, may preserve CM if available

3. **Font Installation**
   To get true CMR10, install Computer Modern fonts:
   - **Windows**: Install CM Unicode fonts
   - **macOS**: Install using Homebrew or manually
   - **Linux**: `apt install fonts-cmu` or similar

### Workarounds for CMR10-like Appearance

#### Option 1: Install Computer Modern Fonts

**Windows:**
1. Download CMU fonts from: https://www.fontsquirrel.com/fonts/computer-modern
2. Install all TTF files
3. Restart Python/Plotly

**Linux:**
```bash
sudo apt-get install fonts-cmu
# or
sudo apt-get install texlive-fonts-recommended
```

**macOS:**
```bash
brew tap homebrew/cask-fonts
brew install font-computer-modern
```

#### Option 2: Use LaTeX Rendering (Limited)

Plotly supports MathJax for LaTeX in text, but full LaTeX rendering is limited:

```python
fig = qplotly.figure()
fig.title('$\\text{Title in LaTeX: } \\alpha = \\frac{1}{2}$')
```

This works for mathematical expressions but not for general text styling.

#### Option 3: Use Different Font

If CMR10 is not available, specify an alternative:

```python
fig = qplotly.figure()
fig.update_layout(
    font=dict(
        family='Times New Roman, serif',  # Or 'Georgia', 'Palatino', etc.
        size=12
    )
)
```

### What You're Currently Getting

Without Computer Modern installed, Plotly falls back to:
- **Browser default serif** (typically Times New Roman)
- **System serif font** (varies by OS)

This looks professional but lacks the distinctive CMR10 appearance.

## Testing Font Rendering

To check what font is actually being used:

1. **HTML Output**: Save as HTML and inspect in browser dev tools
   ```python
   fig.savefig('test.html')
   # Open in browser, right-click text, inspect element
   ```

2. **PNG Output**: The font in PNG depends on kaleido's available fonts
   ```python
   fig.savefig('test.png')
   # Font rendering baked into image
   ```

## Recommendations

### For Publications

1. **Install Computer Modern** for authentic LaTeX appearance
2. **Or use serif fallback** - still looks professional
3. **For true LaTeX**: Consider using matplotlib with LaTeX backend, then importing to Plotly if interactivity is needed

### For Web/Interactive Use

1. **Accept browser default serif** - broadly compatible
2. **Or specify web-safe font** like Georgia or Times
3. **Focus on data/layout** rather than exact font matching

## Current Status

✓ **Default styling applied**: White background, frame, grid
✓ **Font specification set**: Computer Modern with fallbacks
~ **CMR10 appearance**: Depends on system font installation

The plots will look clean and professional with:
- White background (like matplotlib)
- Black frame on all sides
- Semi-transparent black grid
- Serif font (Times-like if CM not installed)

## Code Location

Modified: `qplotly/__init__.py`
- Added `QFigure._apply_default_style()` method
- Called automatically in `QFigure.__init__()`
- Applies to all axes in single and multi-subplot figures

## Demonstration Files

Generated in `legend_debugging/`:
- `test_defaults_single.png` - Single plot with new defaults
- `test_defaults_subplots.png` - 2x2 subplots with defaults
- `test_defaults_no_grid.png` - Frame visible without grid
- `test_defaults_many_traces.png` - Auto-colors with defaults
- `test_defaults_publication.png` - Publication-style figure

All demonstrate:
- White background
- Black frame (mirrored on all sides)
- Black grid at 50% opacity
- Clean, professional appearance

## Summary

✓ Matplotlib-like styling now default
✓ Font set to Computer Modern with fallbacks
~ Actual CMR10 rendering depends on system fonts
✓ Professional appearance guaranteed regardless of font

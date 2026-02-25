# Tight Layout and Centered Titles

## Overview

qplotly now includes matplotlib-style tight layout and centered titles:
- **tight_layout=True by default** in show() and savefig()
- **Centered titles** for both single plots and subplots
- Automatic margin reduction for better space usage

## Changes Made

### 1. Tight Layout

Added `_apply_tight_layout()` method and tight_layout parameter:

**Modified: `qplotly/__init__.py`**

```python
def _apply_tight_layout(self):
    """Apply tight layout (matplotlib-style) by reducing margins."""
    self._fig.update_layout(
        margin=dict(l=60, r=30, t=80, b=60)  # left, right, top, bottom
    )

def show(self, renderer=None, tight_layout=True, **kwargs):
    """Show the figure with tight_layout enabled by default."""
    self._apply_auto_color_scheme()
    self._apply_subplot_legends()
    if tight_layout:
        self._apply_tight_layout()
    self._fig.show(renderer=renderer, **kwargs)

def savefig(self, filename, width=None, height=None, scale=None,
            tight_layout=True, **kwargs):
    """Save with tight_layout enabled by default."""
    self._apply_auto_color_scheme()
    self._apply_subplot_legends()
    if tight_layout:
        self._apply_tight_layout()
    # ... save logic ...
```

### 2. Centered Titles

Updated title() method to center titles:

```python
def title(self, label, fontsize=None, **kwargs):
    if self._parent._nrows == 1 and self._parent._ncols == 1:
        # Single plot: center title over plot
        font = dict(size=fontsize) if fontsize else None
        self._fig.update_layout(title=dict(
            text=label,
            font=font,
            x=0.5,           # Center position
            xanchor='center' # Anchor at center
        ))
    else:
        # Subplots: already centered at x=0.5
        # ... existing subplot logic ...
```

## Features

### Tight Layout

**What it does:**
- Reduces whitespace around plots
- Better space utilization
- Professional appearance
- Matplotlib-compatible behavior

**Margins:**
- Left: 60px (space for y-axis labels)
- Right: 30px (minimal margin)
- Top: 80px (space for title)
- Bottom: 60px (space for x-axis labels)

**Usage:**
```python
# Default: tight_layout=True
fig.show()  # Uses tight layout

# Disable if needed
fig.show(tight_layout=False)
fig.savefig('plot.png', tight_layout=False)
```

### Centered Titles

**What it does:**
- All titles centered over their plot axes
- Single plot titles centered
- Subplot titles centered
- suptitle centered over entire figure
- Matches matplotlib behavior

**Automatic:**
- No user code changes needed
- Works for all title types
- Consistent across single plots and subplots

## Demonstration Files

### Tight Layout Demos
1. `demo_tight_layout_single.png` - Single plot with tight layout
2. `demo_tight_layout_subplots.png` - 2×2 subplots with tight layout
3. `demo_tight_on.png` - With tight_layout=True (default)
4. `demo_tight_off.png` - With tight_layout=False (comparison)
5. `demo_complete_publication.png` - 2×3 publication figure with all features

### Comparison
- Compare `demo_tight_on.png` vs `demo_tight_off.png` to see the margin differences
- `demo_tight_off.png` shows default Plotly margins (larger whitespace)
- `demo_tight_on.png` shows reduced margins (better space usage)

## Benefits

### Tight Layout
✓ Better space utilization
✓ More plot area, less whitespace
✓ Professional appearance
✓ Matplotlib-compatible
✓ Enabled by default (opt-out available)

### Centered Titles
✓ Visually balanced appearance
✓ Matches matplotlib convention
✓ Professional look
✓ Works automatically
✓ Consistent across all plot types

## Usage Examples

### Basic Usage (Automatic)
```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 100)

# Single plot - tight layout and centered title automatic
fig = qplotly.figure()
fig.plot(x, np.sin(x))
fig.title('My Centered Title')  # Automatically centered
fig.show()  # Automatically uses tight_layout
```

### Subplots (Automatic)
```python
fig, axes = qplotly.subplots(2, 2)

axes[0][0].plot(x, np.sin(x))
axes[0][0].title('Plot A')  # Automatically centered

axes[0][1].plot(x, np.cos(x))
axes[0][1].title('Plot B')  # Automatically centered

fig.suptitle('My Figure')  # Automatically centered
fig.show()  # Automatically uses tight_layout
```

### Disable Tight Layout (If Needed)
```python
# For special cases where you want more margin
fig.show(tight_layout=False)
fig.savefig('plot.png', tight_layout=False)
```

## Matplotlib Compatibility

### Matching Behavior ✓
- `tight_layout=True` reduces margins like matplotlib
- Titles centered like matplotlib
- Better default appearance
- Opt-out available if needed

### API Compatibility ✓
```python
# Matplotlib style works in qplotly
fig, axes = plt.subplots(2, 2)
plt.tight_layout()  # matplotlib

fig, axes = qplotly.subplots(2, 2)
fig.show()  # qplotly - automatic!
```

## Technical Notes

- tight_layout applied in both show() and savefig()
- Margin values chosen to work well with typical axis labels
- Title centering uses x=0.5, xanchor='center'
- Subplot titles already centered at x=0.5 in subplot domain
- No breaking changes - existing code works unchanged

## Summary

✓ **tight_layout=True by default** - better space usage
✓ **Centered titles** - professional appearance
✓ **Matplotlib-compatible** - familiar behavior
✓ **Automatic** - no code changes needed
✓ **Opt-out available** - tight_layout=False if needed

qplotly now provides matplotlib-style layout and title positioning automatically!

# qplotly

A matplotlib-like interface for Plotly, providing a familiar API for interactive plotting.

## Overview

`qplotly` is a Python library that wraps Plotly with a matplotlib-inspired API, making it easy for users familiar with matplotlib to create interactive Plotly visualizations. It maintains matplotlib's intuitive syntax while leveraging Plotly's interactive capabilities.

## Features

- **Matplotlib-like API**: Familiar syntax for users coming from matplotlib
- **Interactive plots**: All plots are interactive Plotly visualizations
- **Comprehensive plot types**: Support for line plots, scatter plots, bar charts, histograms, heatmaps, contours, and more
- **Subplots**: Easy subplot creation with `subplots()` function
- **Format strings**: Matplotlib-style format strings like `'ro--'` for red dashed lines with circle markers
- **Color cycling**: Automatic color cycling for multiple traces
- **Dual axes**: Support for secondary y-axes with `twinx()`
- **Annotations**: Text annotations, arrows, and reference lines

## Installation

### From source

```bash
git clone https://github.com/yourusername/qplotly.git
cd qplotly
pip install -e .
```

### Requirements

- Python >= 3.9
- plotly
- numpy

## Quick Start

```python
import qplotly
import numpy as np

# Simple line plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = qplotly.figure()
fig.plot(x, y, label='sin(x)')
fig.xlabel('X Axis')
fig.ylabel('Y Axis')
fig.title('My First qplotly Plot')
fig.legend()
fig.show()
```

## API Documentation

### Creating Figures

#### Single figure
```python
import qplotly

fig = qplotly.figure(figsize=(8, 6))
```

#### Subplots
```python
fig, axes = qplotly.subplots(2, 2, figsize=(10, 8))
axes[0][0].plot(x, y)
axes[0][1].scatter(x, y)
fig.show()
```

#### Pyplot-style (stateful)
```python
import qplotly

qplotly.plot(x, y, label='data')
qplotly.xlabel('X')
qplotly.ylabel('Y')
qplotly.legend()
qplotly.show()
```

### Plot Types

#### Line Plot
```python
# Basic usage
fig.plot(y)                          # Plot y vs index
fig.plot(x, y)                       # Plot y vs x
fig.plot(x, y, 'r--')               # Format string: red dashed line
fig.plot(x, y, label='data')        # With label for legend
fig.plot(x, y, color='blue', linewidth=2, linestyle='dash')
fig.plot(x, y, marker='o', markersize=8)
```

Supported format string components:
- **Colors**: `'b'` (blue), `'g'` (green), `'r'` (red), `'c'` (cyan), `'m'` (magenta), `'y'` (yellow), `'k'` (black), `'w'` (white)
- **Markers**: `'o'` (circle), `'s'` (square), `'^'` (triangle-up), `'v'` (triangle-down), `'D'` (diamond), `'+'` (cross), `'x'` (x), `'*'` (star)
- **Line styles**: `'-'` (solid), `'--'` (dash), `'-.'` (dashdot), `':'` (dot)

#### Scatter Plot
```python
fig.scatter(x, y, s=50, c='red', marker='o', alpha=0.7, label='data points')

# With colormap
fig.scatter(x, y, c=values, cmap='Viridis', colorbar=True)
```

#### Bar Chart
```python
# Vertical bars
fig.bar(x, height, color='blue', edgecolor='black', alpha=0.8)

# Horizontal bars
fig.barh(y, width, color='green')
```

#### Histogram
```python
fig.hist(data, bins=20, density=False, color='blue', alpha=0.7, edgecolor='black')
```

#### Error Bars
```python
fig.errorbar(x, y, yerr=y_error, xerr=x_error, marker='o', capsize=5)

# Asymmetric errors
fig.errorbar(x, y, yerr=[lower_errors, upper_errors])
```

#### Fill Between
```python
fig.fill_between(x, y1, y2, alpha=0.3, color='gray', label='confidence')
```

#### Heatmap / Image
```python
fig.heatmap(data, cmap='Viridis', colorbar=True, vmin=0, vmax=1)
fig.imshow(image_data, cmap='gray')
```

#### Contour Plots
```python
fig.contour(x, y, z, levels=10, cmap='RdBu')
fig.contourf(x, y, z, levels=20, cmap='Plasma')  # Filled contours
```

#### Pseudocolor
```python
fig.pcolormesh(x, y, z, cmap='viridis', vmin=0, vmax=10, colorbar=True)
```

#### Stem Plot
```python
fig.stem(x, y, color='red')
```

#### Pie Chart
```python
fig.pie(sizes, labels=['A', 'B', 'C'], colors=['red', 'blue', 'green'],
        autopct='%1.1f%%', startangle=90)
```

### Customization

#### Axis Labels and Titles
```python
fig.xlabel('X Axis Label', fontsize=14)
fig.ylabel('Y Axis Label', fontsize=14)
fig.title('Plot Title', fontsize=16)

# For subplots
fig.suptitle('Figure Title')
```

#### Axis Limits
```python
fig.xlim(0, 10)
fig.ylim(-1, 1)
# or
fig.xlim([0, 10])
```

#### Axis Scale
```python
fig.xscale('log')
fig.yscale('linear')
```

#### Grid
```python
fig.grid(True)
fig.grid(False)
```

#### Legend
```python
fig.legend()
fig.legend(loc='upper right', fontsize=12)
```

#### Ticks
```python
fig.xticks([0, 1, 2, 3], ['A', 'B', 'C', 'D'])
fig.yticks(rotation=45, fontsize=10)
```

#### Invert Axes
```python
fig.invert_xaxis()
fig.invert_yaxis()
```

#### Aspect Ratio
```python
fig.set_aspect('equal')
```

### Annotations

#### Reference Lines
```python
fig.axhline(y=0, color='black', linestyle='--', linewidth=1)
fig.axvline(x=5, color='red', linestyle='-', linewidth=2)
```

#### Shaded Regions
```python
fig.axhspan(0, 1, color='gray', alpha=0.2)
fig.axvspan(2, 4, color='blue', alpha=0.1)
```

#### Text Annotations
```python
fig.text(5, 10, 'Important Point', fontsize=12, color='red', ha='center')
fig.annotate('Peak', xy=(3, 5), xytext=(4, 6),
             arrowprops=dict(arrowstyle='->'), fontsize=10)
```

### Secondary Y-Axis

```python
ax1 = fig
ax1.plot(x, y1, 'b-', label='y1')
ax1.ylabel('Y1', color='b')

ax2 = ax1.twinx()
ax2.plot(x, y2, 'r-', label='y2')
ax2.ylabel('Y2', color='r')
```

### Templates and Styling

```python
fig.set_template('plotly_dark')  # Dark theme
fig.set_template('ggplot2')      # ggplot2 style
fig.set_template('plotly')       # Default Plotly theme
```

### Saving Figures

```python
# Raster formats (requires kaleido: pip install kaleido)
fig.savefig('plot.png', width=800, height=600, scale=2)
fig.savefig('plot.jpg')
fig.savefig('plot.pdf')

# Vector formats
fig.savefig('plot.svg')

# Interactive formats
fig.savefig('plot.html')
fig.savefig('plot.json')
```

### Access to Underlying Plotly Figure

```python
plotly_fig = fig.plotly_fig
# Now you can use any Plotly API methods
plotly_fig.update_layout(...)
```

## Examples

### Basic Line Plot with Multiple Series

```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 100)

fig = qplotly.figure(figsize=(10, 6))
fig.plot(x, np.sin(x), 'b-', label='sin(x)')
fig.plot(x, np.cos(x), 'r--', label='cos(x)')
fig.xlabel('x')
fig.ylabel('y')
fig.title('Trigonometric Functions')
fig.legend()
fig.grid(True)
fig.show()
```

### Subplots with Different Plot Types

```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, axes = qplotly.subplots(2, 2, figsize=(12, 10))

axes[0][0].plot(x, y, 'b-')
axes[0][0].title('Line Plot')

axes[0][1].scatter(x, y, c='red', s=50)
axes[0][1].title('Scatter Plot')

axes[1][0].bar(x[:10], y[:10])
axes[1][0].title('Bar Chart')

axes[1][1].hist(np.random.randn(1000), bins=30)
axes[1][1].title('Histogram')

fig.suptitle('Multiple Plot Types')
fig.show()
```

### Heatmap with Custom Colormap

```python
import qplotly
import numpy as np

data = np.random.randn(20, 20)

fig = qplotly.figure()
fig.heatmap(data, cmap='RdBu', colorbar=True)
fig.title('Random Data Heatmap')
fig.show()
```

### Error Bars Example

```python
import qplotly
import numpy as np

x = np.linspace(0, 10, 20)
y = np.sin(x)
yerr = 0.1 + 0.1 * np.random.rand(len(x))

fig = qplotly.figure()
fig.errorbar(x, y, yerr=yerr, marker='o', color='blue',
             capsize=5, label='data with errors')
fig.xlabel('x')
fig.ylabel('y')
fig.title('Error Bar Plot')
fig.legend()
fig.show()
```

## Differences from Matplotlib

While `qplotly` aims to provide a matplotlib-like API, there are some differences:

1. **Interactive plots**: All plots are interactive by default (zoom, pan, hover)
2. **No blocking show()**: `show()` doesn't block execution in the same way
3. **Backend**: Uses Plotly's rendering instead of matplotlib backends
4. **Performance**: Better performance for large datasets with WebGL rendering
5. **Export**: Different export requirements (kaleido for raster images)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Authors

Created with Claude Code

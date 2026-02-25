# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed
- **Per-subplot color cycling**: Modified `_apply_auto_color_scheme()` to apply colors independently per subplot instead of globally. Colors now reset for each subplot, ensuring the first trace in each subplot gets the same color, second trace gets the same color, etc. This provides visual consistency when comparing data across multiple subplots.

- **nipy_spectral as default colormap**: Changed default automatic color scheme from discrete color rules (2 traces: blue/black, 3-4 traces: blue/red/green/black, >4: nipy_spectral) to always use nipy_spectral colormap with evenly spaced colors. This provides a smooth rainbow gradient (dark purple → blue → cyan → green → yellow → orange → light gray) that scales well for any number of traces.

- **Trace-to-axes association**: Modified `_auto_colored_trace_indices` to store tuples of `(trace_idx, axes)` instead of just `trace_idx`, enabling per-subplot color grouping and application.

### Fixed
- **Package discovery**: Added explicit `packages = ["qplotly"]` to `pyproject.toml` under `[tool.setuptools]` to fix "Multiple top-level packages discovered" error during installation.

## Benefits of Changes

1. **Consistent visual comparison**: When plotting parameter sweeps or multiple traces across subplots, the same data series uses the same color in all subplots, making cross-subplot comparison intuitive.

2. **Better color distinction**: The nipy_spectral colormap provides highly distinguishable colors that span the visible spectrum, making it easier to identify individual traces even when many are plotted.

3. **Matplotlib-like behavior**: Per-subplot color cycling matches matplotlib's default behavior, making qplotly more intuitive for matplotlib users.

4. **Scales automatically**: Works for any number of traces (2, 6, 10, 20+) without special case logic.

## Example

```python
import qplotly
import numpy as np

# Create 2x2 subplots with 6 traces each
fig, axes = qplotly.subplots(2, 2)
x = np.linspace(0, 10, 100)

for ax in [axes[0][0], axes[0][1], axes[1][0], axes[1][1]]:
    for i in range(6):
        ax.plot(x, np.sin(x + i*0.5), label=f'Trace {i+1}')
    ax.legend()

fig.show()
```

Result: All 4 subplots have traces with identical colors:
- Trace 1: dark purple in all subplots
- Trace 2: blue in all subplots
- Trace 3: cyan in all subplots
- Trace 4: green in all subplots
- Trace 5: orange in all subplots
- Trace 6: light gray in all subplots

## Date
2026-02-25

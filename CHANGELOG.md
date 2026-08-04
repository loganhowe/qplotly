# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed
- **Figure-owned API**: Delegated plotting and formatting calls now return the
  `QFigure` when invoked through `fig`, enabling fluent calls such as
  `fig.plot(...).xlabel(...).legend()`.
- **Deterministic colors**: Ordinary plots now retain Matplotlib's default color
  cycle at creation time. `show()` no longer recolors traces.
- **Explicit line-sweep colors**: `sweep_colorbar()` applies a chosen continuous
  colormap to automatically colored line traces. `colorbar()` now targets the
  latest color-mapped trace by default.
- **Matplotlib aliases**: Added `set_xlabel`, `set_ylabel`, `set_title`,
  `set_xlim`, `set_ylim`, `set_xscale`, `set_yscale`, `set_xticks`, and
  `set_yticks`.

### Fixed
- **Figure ownership**: The default axes and `axes[0][0]` are now the same
  object, so color cycles, legends, and trace tracking cannot diverge.
- **Subplot legends**: Replaced generated annotation legends with idempotent
  native Plotly legends.
- **Twin axes**: Each `twinx()` now receives a unique secondary y-axis attached
  to the correct subplot.
- **Plot parsing**: Added multiple `(x, y, fmt)` groups, 2-D column expansion,
  marker-only format strings, and common Matplotlib aliases.
- **Colorbars**: Single-panel and subplot colorbars now find heatmaps with
  implicit Plotly axis references and support color-mapped scatter traces.
- **Package discovery**: Added explicit `packages = ["qplotly"]` to `pyproject.toml` under `[tool.setuptools]` to fix "Multiple top-level packages discovered" error during installation.

## Date
2026-08-04

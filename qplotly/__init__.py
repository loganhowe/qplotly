"""
qplotly.py - A matplotlib-like interface for Plotly.

Usage:
    import qplotly

    fig = qplotly.figure()
    fig.plot(x, y, label='my line')
    fig.xlabel('X Axis')
    fig.ylabel('Y Axis')
    fig.title('My Plot')
    fig.legend()
    fig.show()

    # Subplots:
    fig, axes = qplotly.subplots(2, 2)
    axes[0][0].plot(x, y)
    axes[1][0].bar(x, y)
    fig.show()
"""

from __future__ import annotations

import warnings
from copy import deepcopy
from functools import wraps

import numpy as np
import plotly.colors as pc
import plotly.graph_objects as go
import plotly.io as pio
from _plotly_utils.exceptions import PlotlyError
from plotly.subplots import make_subplots

# Render figures inline by default when qplotly is imported in a notebook.
pio.renderers.default = "notebook"


# ---------- Default color cycle (Plotly's built-in qualitative set) ----------
DEFAULT_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
]

# ---------- Matplotlib-style format string parser ----------
_FMT_COLORS = {
    "b": "blue", "g": "green", "r": "red", "c": "cyan",
    "m": "magenta", "y": "yellow", "k": "black", "w": "white",
}

_FMT_MARKERS = {
    "o": "circle", "s": "square", "^": "triangle-up", "v": "triangle-down",
    "D": "diamond", "d": "diamond", "+": "cross", "x": "x",
    "*": "star", "p": "pentagon", "h": "hexagon",
}

_FMT_LINES = {
    "-": "solid", "--": "dash", "-.": "dashdot", ":": "dot",
}

_LINESTYLES = {
    "-": "solid",
    "--": "dash",
    "-.": "dashdot",
    ":": "dot",
    "solid": "solid",
    "dashed": "dash",
    "dash": "dash",
    "dashdot": "dashdot",
    "dotted": "dot",
    "dot": "dot",
    "none": None,
    "": None,
    " ": None,
}

_LEGEND_LOCATIONS = {
    "best": (0.98, 0.98, "right", "top"),
    "upper right": (0.98, 0.98, "right", "top"),
    "upper left": (0.02, 0.98, "left", "top"),
    "lower left": (0.02, 0.02, "left", "bottom"),
    "lower right": (0.98, 0.02, "right", "bottom"),
    "right": (0.98, 0.5, "right", "middle"),
    "center left": (0.02, 0.5, "left", "middle"),
    "center right": (0.98, 0.5, "right", "middle"),
    "lower center": (0.5, 0.02, "center", "bottom"),
    "upper center": (0.5, 0.98, "center", "top"),
    "center": (0.5, 0.5, "center", "middle"),
    "outside center right": (1.02, 0.5, "left", "middle"),
}


def _parse_fmt(fmt: str):
    """Parse a matplotlib-style format string like 'ro--' into components."""
    color = None
    marker = None
    linestyle = None

    s = fmt
    # Try to extract line style first (two-char patterns before one-char)
    for ls_key in ("--", "-.", ":", "-"):
        if ls_key in s:
            linestyle = _FMT_LINES[ls_key]
            s = s.replace(ls_key, "", 1)
            break

    for ch in s:
        if ch in _FMT_COLORS and color is None:
            color = _FMT_COLORS[ch]
        elif ch in _FMT_MARKERS and marker is None:
            marker = _FMT_MARKERS[ch]

    return color, marker, linestyle


def _resolve_linewidth(lw=None, linewidth=None):
    return lw if lw is not None else linewidth


def _normalize_linestyle(style, default="solid"):
    """Translate common Matplotlib line styles to Plotly dash names."""
    if style is None:
        return default
    key = style.lower() if isinstance(style, str) else style
    if key not in _LINESTYLES:
        raise ValueError(f"Unsupported linestyle: {style!r}")
    return _LINESTYLES[key]


def _normalize_marker(marker):
    if marker is None:
        return None
    return _FMT_MARKERS.get(marker, marker)


def _parse_plot_args(args):
    """Yield ``(x, y, fmt)`` groups using Matplotlib's plot conventions."""
    if not args:
        raise TypeError("plot() requires at least 1 positional argument")

    groups = []
    index = 0
    while index < len(args):
        first = args[index]
        index += 1

        if index < len(args) and isinstance(args[index], str):
            y = np.atleast_1d(first)
            x = np.arange(len(y))
            fmt = args[index]
            index += 1
        elif index < len(args):
            x = np.asarray(first)
            y = np.asarray(args[index])
            index += 1
            fmt = None
            if index < len(args) and isinstance(args[index], str):
                fmt = args[index]
                index += 1
        else:
            y = np.atleast_1d(first)
            x = np.arange(len(y))
            fmt = None

        groups.append((x, y, fmt))
    return groups


def _expand_plot_columns(x, y):
    """Expand 2-D plot inputs into Matplotlib-style column traces."""
    x = np.asarray(x)
    y = np.asarray(y)
    if x.ndim > 2 or y.ndim > 2:
        raise ValueError("x and y must be one- or two-dimensional")
    if x.ndim <= 1 and y.ndim <= 1:
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)
        if len(x) != len(y):
            raise ValueError("x and y must have the same first dimension")
        return [(x, y)]

    if y.ndim == 2 and x.ndim <= 1:
        if len(x) != y.shape[0]:
            raise ValueError("x and y must have the same first dimension")
        return [(x, y[:, column]) for column in range(y.shape[1])]
    if x.ndim == 2 and y.ndim <= 1:
        if x.shape[0] != len(y):
            raise ValueError("x and y must have the same first dimension")
        return [(x[:, column], y) for column in range(x.shape[1])]
    if x.shape != y.shape:
        raise ValueError("2-D x and y arrays must have the same shape")
    return [(x[:, column], y[:, column]) for column in range(x.shape[1])]


def _label_at(label, index, count):
    if isinstance(label, str) or label is None:
        return label
    try:
        labels = list(label)
    except TypeError:
        return label
    if len(labels) != count:
        raise ValueError("label sequence must match the number of plotted lines")
    return labels[index]


def _normalize_colorscale(cmap):
    """Return a Plotly colorscale, optionally converting Matplotlib maps."""
    if cmap is None:
        return None
    if not isinstance(cmap, str):
        return cmap
    try:
        return pc.get_colorscale(cmap)
    except PlotlyError:
        pass
    except ValueError:
        pass

    try:
        import matplotlib

        mpl_cmap = matplotlib.colormaps.get_cmap(cmap)
    except (ImportError, ValueError):
        return cmap

    samples = mpl_cmap(np.linspace(0, 1, 256))
    return [
        [index / 255, f"rgb({int(r * 255)},{int(g * 255)},{int(b * 255)})"]
        for index, (r, g, b, _alpha) in enumerate(samples)
    ]


def _pop_font_options(options, fontsize=None):
    """Extract common Matplotlib font aliases into a Plotly font dict."""
    font = dict(options.pop("fontdict", {}) or {})
    font.update(dict(options.pop("font", {}) or {}))
    aliases = {
        "fontfamily": "family",
        "fontname": "family",
        "fontweight": "weight",
        "fontstyle": "style",
        "color": "color",
    }
    for source, target in aliases.items():
        if source in options:
            font[target] = options.pop(source)
    if fontsize is not None:
        font["size"] = fontsize
    return font


def _filter_legend_options(options):
    """Keep direct Plotly legend options and ignore unsupported mpl styling."""
    options = dict(options)
    ignored = {
        "handlelength",
        "handleheight",
        "handletextpad",
        "borderaxespad",
        "columnspacing",
        "labelspacing",
        "markerscale",
        "mode",
        "prop",
    }
    for key in ignored:
        options.pop(key, None)
    valid = go.layout.Legend()._valid_props
    unsupported = sorted(key for key in options if key not in valid)
    if unsupported:
        warnings.warn(
            "Unsupported legend options ignored: " + ", ".join(unsupported),
            RuntimeWarning,
            stacklevel=3,
        )
        for key in unsupported:
            options.pop(key)
    return options


def _normalize_share(value):
    if value in (False, None, "none"):
        return None
    if value is True:
        return "all"
    mapping = {
        "all": "all",
        "row": "rows",
        "rows": "rows",
        "col": "columns",
        "columns": "columns",
    }
    if value not in mapping:
        raise ValueError(
            "sharex/sharey must be False, True, 'none', 'all', 'row', or 'col'"
        )
    return mapping[value]


# ===========================================================================
#  Axes class — represents a single subplot panel
# ===========================================================================
class Axes:
    """A single axes/subplot, analogous to ``matplotlib.axes.Axes``."""

    def __init__(self, parent_figure: QFigure, row: int = 1, col: int = 1):
        self._parent = parent_figure
        self._fig: go.Figure = parent_figure._fig
        self._row = row
        self._col = col
        self._color_idx = 0
        self._has_legend_entries = False
        self._legend_traces = []  # Track traces with legend entries for this axes
        self._legend_config = None

    # ---- colour cycling ---------------------------------------------------
    def _next_color(self):
        c = DEFAULT_COLORS[self._color_idx % len(DEFAULT_COLORS)]
        self._color_idx += 1
        return c

    # ---- internal helper to add a trace to the correct subplot cell -------
    def _add_trace(self, trace):
        # Only specify row/col for multi-subplot layouts
        if self._parent._nrows == 1 and self._parent._ncols == 1:
            self._fig.add_trace(trace)
        else:
            self._fig.add_trace(trace, row=self._row, col=self._col)

        trace_idx = len(self._fig.data) - 1
        self._record_trace(trace_idx, trace)
        return trace_idx

    def _record_trace(self, trace_idx, trace):
        # Track if this trace used automatic coloring
        if getattr(self, "_next_trace_auto_colored", False):
            self._parent._auto_colored_trace_indices.append((trace_idx, self))
            self._next_trace_auto_colored = False

        # Track traces with legend entries for per-subplot legends
        if trace.name:
            self._legend_traces.append(trace_idx)
            self._has_legend_entries = True

    # ---- axis id helpers (for multi-subplot layouts) ----------------------
    def _xaxis_name(self):
        idx = self._parent._subplot_index(self._row, self._col)
        return "xaxis" if idx == 1 else f"xaxis{idx}"

    def _yaxis_name(self):
        idx = self._parent._subplot_index(self._row, self._col)
        return "yaxis" if idx == 1 else f"yaxis{idx}"

    # ======================= plotting methods ==============================

    def plot(self, *args, label=None, color=None, linewidth=None, lw=None,
             linestyle=None, ls=None, marker=None, markersize=None, ms=None,
             alpha=None, fmt=None, **kwargs):
        """Line plot (like ``matplotlib.axes.Axes.plot``).

        Supports positional args:
            plot(y)
            plot(x, y)
            plot(x, y, 'r--')
        """
        if color is None:
            color = kwargs.pop("c", None)
        markeredgecolor = kwargs.pop("markeredgecolor", kwargs.pop("mec", None))
        markerfacecolor = kwargs.pop("markerfacecolor", kwargs.pop("mfc", None))
        markeredgewidth = kwargs.pop("markeredgewidth", kwargs.pop("mew", None))
        marker_overrides = marker.copy() if isinstance(marker, dict) else {}
        marker_argument = marker_overrides.pop(
            "symbol", None if isinstance(marker, dict) else marker
        )

        raw_groups = _parse_plot_args(args)
        expanded_groups = []
        for x_values, y_values, group_fmt in raw_groups:
            for x_column, y_column in _expand_plot_columns(x_values, y_values):
                expanded_groups.append((x_column, y_column, group_fmt))

        for index, (x_values, y_values, group_fmt) in enumerate(expanded_groups):
            active_fmt = group_fmt if group_fmt is not None else fmt
            fmt_color, fmt_marker, fmt_linestyle = (None, None, None)
            if active_fmt:
                fmt_color, fmt_marker, fmt_linestyle = _parse_fmt(active_fmt)

            trace_color = color if color is not None else fmt_color
            self._next_trace_auto_colored = trace_color is None
            if trace_color is None:
                trace_color = self._next_color()

            trace_marker = (
                marker_argument if marker_argument is not None else fmt_marker
            )
            explicit_linestyle = linestyle if linestyle is not None else ls
            if explicit_linestyle is not None:
                trace_linestyle = _normalize_linestyle(explicit_linestyle)
            elif fmt_linestyle is not None:
                trace_linestyle = fmt_linestyle
            elif active_fmt and fmt_marker is not None:
                trace_linestyle = None
            else:
                trace_linestyle = "solid"

            trace_linewidth = _resolve_linewidth(lw, linewidth)
            if trace_linewidth is None:
                trace_linewidth = 1.5
            trace_markersize = markersize if markersize is not None else ms
            if trace_markersize is None:
                trace_markersize = 6

            if trace_linestyle and trace_marker:
                default_mode = "lines+markers"
            elif trace_marker:
                default_mode = "markers"
            else:
                default_mode = "lines"

            trace_kwargs = deepcopy(kwargs)
            line_options = dict(trace_kwargs.pop("line", {}) or {})
            marker_options = deepcopy(marker_overrides)
            marker_options.update(
                dict(trace_kwargs.pop("marker_options", {}) or {})
            )
            line_options.setdefault("color", trace_color)
            line_options.setdefault("width", trace_linewidth)
            if trace_linestyle:
                line_options.setdefault("dash", trace_linestyle)
            marker_options.setdefault("symbol", _normalize_marker(trace_marker))
            marker_options.setdefault("size", trace_markersize)
            marker_options.setdefault(
                "color",
                markerfacecolor if markerfacecolor is not None else trace_color,
            )
            if markeredgecolor is not None or markeredgewidth is not None:
                marker_options["line"] = dict(
                    color=(
                        markeredgecolor
                        if markeredgecolor is not None
                        else trace_color
                    ),
                    width=markeredgewidth if markeredgewidth is not None else 1,
                )

            trace_label = _label_at(label, index, len(expanded_groups))
            trace = go.Scatter(
                x=x_values,
                y=y_values,
                mode=trace_kwargs.pop("mode", default_mode),
                name=trace_kwargs.pop("name", trace_label),
                line=line_options,
                marker=marker_options,
                opacity=trace_kwargs.pop("opacity", alpha),
                showlegend=trace_kwargs.pop("showlegend", False),
                **trace_kwargs,
            )
            self._add_trace(trace)
        return self

    def scatter(self, x, y, s=None, c=None, label=None, marker=None,
                alpha=None, cmap=None, colorbar=False, edgecolors=None,
                linewidths=None, vmin=None, vmax=None, **kwargs):
        """Scatter plot."""
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)
        if len(x) != len(y):
            raise ValueError("x and y must have the same first dimension")
        if c is None:
            c = kwargs.pop("color", None)
        size = np.sqrt(np.asarray(s)) if s is not None else 6
        if np.ndim(size) == 0:
            size = float(size)

        self._next_trace_auto_colored = c is None
        color = c if c is not None else self._next_color()

        marker_options = marker.copy() if isinstance(marker, dict) else {}
        marker_symbol = marker_options.pop(
            "symbol", None if isinstance(marker, dict) else marker
        )

        marker_dict = dict(
            size=size,
            color=color,
            symbol=_normalize_marker(marker_symbol) or "circle",
            opacity=alpha,
        )
        marker_dict.update(marker_options)

        if edgecolors is not None:
            if edgecolors == "none":
                marker_dict["line"] = dict(width=0)
            else:
                marker_dict["line"] = dict(
                    color=edgecolors,
                    width=linewidths if linewidths is not None else 1,
                )

        is_color_array = isinstance(color, (list, tuple, np.ndarray))
        if is_color_array and (cmap is not None or colorbar):
            marker_dict["colorscale"] = _normalize_colorscale(cmap or "Viridis")
            marker_dict["cmin"] = vmin
            marker_dict["cmax"] = vmax
            marker_dict["showscale"] = colorbar

        trace = go.Scatter(
            x=x, y=y, mode="markers", name=label,
            marker=marker_dict,
            showlegend=kwargs.pop("showlegend", False),
            **kwargs,
        )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def bar(self, x, height, width=None, bottom=None, label=None, color=None,
            edgecolor=None, linewidth=None, alpha=None, orientation="v",
            **kwargs):
        """Bar chart."""
        if color is None:
            color = kwargs.pop("c", None)
        if color is None:
            color = self._next_color()
        marker_dict = dict(color=color, opacity=alpha)
        marker_dict.update(kwargs.pop("marker", {}) or {})
        if edgecolor is not None or linewidth is not None:
            marker_dict["line"] = dict(
                color=edgecolor if edgecolor is not None else color,
                width=linewidth if linewidth is not None else 1,
            )

        if orientation == "v":
            trace = go.Bar(
                x=x, y=height, width=width, base=bottom, name=label,
                marker=marker_dict,
                showlegend=kwargs.pop("showlegend", False),
                **kwargs,
            )
        elif orientation == "h":
            trace = go.Bar(
                y=x, x=height, width=width, base=bottom, name=label,
                marker=marker_dict, orientation="h",
                showlegend=kwargs.pop("showlegend", False),
                **kwargs,
            )
        else:
            raise ValueError("orientation must be 'v' or 'h'")
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def barh(self, y, width, height=None, left=None, label=None, **kwargs):
        """Horizontal bar chart."""
        return self.bar(y, width, width=height, bottom=left, label=label,
                        orientation="h", **kwargs)

    def hist(self, x, bins=None, range=None, density=False, weights=None,
             label=None, color=None, alpha=None, edgecolor=None,
             histtype="bar", **kwargs):
        """Histogram."""
        if histtype != "bar":
            raise NotImplementedError(
                "qplotly.hist currently supports histtype='bar' only"
            )
        x = np.asarray(x)
        if color is None:
            color = self._next_color()
        marker_dict = dict(color=color, opacity=alpha)
        if edgecolor is not None:
            marker_dict["line"] = dict(color=edgecolor, width=1)

        hist_kw = {}
        if bins is not None:
            if isinstance(bins, (int, np.integer)):
                hist_kw["nbinsx"] = int(bins)
            else:
                bin_edges = np.asarray(bins)
                if bin_edges.ndim != 1 or len(bin_edges) < 2:
                    raise ValueError("bins must contain at least two edges")
                if np.any(np.diff(bin_edges) <= 0):
                    raise ValueError("bins must increase monotonically")
                if not np.allclose(np.diff(bin_edges), np.diff(bin_edges)[0]):
                    counts, edges = np.histogram(
                        x,
                        bins=bin_edges,
                        density=density,
                        weights=weights,
                    )
                    trace = go.Bar(
                        x=(edges[:-1] + edges[1:]) / 2,
                        y=counts,
                        width=np.diff(edges),
                        name=label,
                        marker=marker_dict,
                        showlegend=kwargs.pop("showlegend", False),
                        **kwargs,
                    )
                    self._add_trace(trace)
                    return self
                hist_kw["xbins"] = dict(
                    start=bin_edges[0], end=bin_edges[-1],
                    size=(bin_edges[1] - bin_edges[0]),
                )
        if range is not None:
            hist_kw["xbins"] = hist_kw.get("xbins", {})
            hist_kw["xbins"]["start"] = range[0]
            hist_kw["xbins"]["end"] = range[1]

        histnorm = "probability density" if density else None
        if weights is not None:
            counts, edges = np.histogram(
                x,
                bins=bins,
                range=range,
                density=density,
                weights=weights,
            )
            trace = go.Bar(
                x=(edges[:-1] + edges[1:]) / 2,
                y=counts,
                width=np.diff(edges),
                name=label,
                marker=marker_dict,
                showlegend=kwargs.pop("showlegend", False),
                **kwargs,
            )
            self._add_trace(trace)
            return self

        trace = go.Histogram(
            x=x, name=label, marker=marker_dict,
            histnorm=histnorm,
            showlegend=kwargs.pop("showlegend", False),
            **hist_kw, **kwargs,
        )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def fill_between(self, x, y1, y2=0, label=None, color=None, alpha=0.3,
                     **kwargs):
        """Filled area between *y1* and *y2*."""
        x = np.atleast_1d(x)
        y1 = np.atleast_1d(y1)
        if len(x) != len(y1):
            raise ValueError("x and y1 must have the same first dimension")
        y2 = np.full(y1.shape, y2) if np.ndim(y2) == 0 else np.asarray(y2)
        if len(y2) != len(y1):
            raise ValueError("y1 and y2 must have the same first dimension")
        color = color or self._next_color()

        # Upper bound
        self._add_trace(go.Scatter(
            x=x, y=y1, mode="lines",
            line=dict(width=0), showlegend=False,
        ))
        # Lower bound with fill
        self._add_trace(go.Scatter(
            x=x, y=y2, mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor=_rgba(color, alpha),
            name=label,
            showlegend=kwargs.pop("showlegend", False),
            **kwargs,
        ))
        if label:
            self._has_legend_entries = True
        return self

    def errorbar(self, x, y, yerr=None, xerr=None, fmt=None, label=None,
                 color=None, ecolor=None, elinewidth=None, linewidth=None,
                 lw=None, linestyle=None, ls=None, marker=None,
                 markersize=None, ms=None, alpha=None, capsize=None,
                 **kwargs):
        """Line plot with error bars."""
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)
        if len(x) != len(y):
            raise ValueError("x and y must have the same first dimension")
        fmt_color, fmt_marker, fmt_linestyle = (None, None, None)
        if fmt:
            fmt_color, fmt_marker, fmt_linestyle = _parse_fmt(fmt)
        if color is None:
            color = fmt_color or self._next_color()
        if marker is None:
            marker = fmt_marker
        line_style = linestyle if linestyle is not None else ls
        if line_style is None:
            line_style = fmt_linestyle
        if line_style is None and fmt and fmt_marker is not None:
            line_style = "none"
        line_style = _normalize_linestyle(line_style, default="solid")

        linewidth = _resolve_linewidth(lw, linewidth)
        if linewidth is None:
            linewidth = 1.5
        if elinewidth is None:
            elinewidth = linewidth
        markersize = markersize if markersize is not None else ms
        if markersize is None:
            markersize = 6
        if line_style and marker:
            mode = "lines+markers"
        elif marker:
            mode = "markers"
        else:
            mode = "lines"

        error_y = None
        error_x = None
        if yerr is not None:
            yerr = np.asarray(yerr)
            if yerr.ndim == 2:
                error_y = dict(type="data", symmetric=False,
                               arrayminus=yerr[0], array=yerr[1], visible=True)
            else:
                error_y = dict(type="data", array=yerr, visible=True)
            error_y.update(
                color=ecolor if ecolor is not None else color,
                thickness=elinewidth,
                width=capsize or 0,
            )
        if xerr is not None:
            xerr = np.asarray(xerr)
            if xerr.ndim == 2:
                error_x = dict(type="data", symmetric=False,
                               arrayminus=xerr[0], array=xerr[1], visible=True)
            else:
                error_x = dict(type="data", array=xerr, visible=True)
            error_x.update(
                color=ecolor if ecolor is not None else color,
                thickness=elinewidth,
                width=capsize or 0,
            )

        trace = go.Scatter(
            x=x, y=y, mode=mode, name=label,
            line=dict(color=color, width=linewidth, dash=line_style),
            marker=dict(symbol=_normalize_marker(marker) or "circle",
                        size=markersize, color=color),
            error_y=error_y, error_x=error_x,
            opacity=alpha,
            showlegend=kwargs.pop("showlegend", False),
            **kwargs,
        )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def stem(self, x, y, label=None, color=None, **kwargs):
        """Stem plot."""
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)
        if len(x) != len(y):
            raise ValueError("x and y must have the same first dimension")
        color = color or self._next_color()

        for xi, yi in zip(x, y):
            self._add_trace(go.Scatter(
                x=[xi, xi], y=[0, yi], mode="lines",
                line=dict(color=color, width=1), showlegend=False,
            ))
        self._add_trace(go.Scatter(
            x=x, y=y, mode="markers", name=label,
            marker=dict(color=color, size=8),
            showlegend=kwargs.pop("showlegend", False),
            **kwargs,
        ))
        if label:
            self._has_legend_entries = True
        return self

    def pie(self, sizes, labels=None, colors=None, autopct=None,
            startangle=None, explode=None, **kwargs):
        """Pie chart."""
        pull = explode if explode is not None else None
        trace = go.Pie(
            values=sizes, labels=labels,
            marker=dict(colors=colors) if colors is not None else None,
            pull=pull,
            textinfo="percent" if autopct else None,
            rotation=startangle,
            **kwargs,
        )
        self._add_trace(trace)
        return self

    def heatmap(self, data, xticklabels=None, yticklabels=None, cmap=None,
                colorbar=True, vmin=None, vmax=None, **kwargs):
        """Heatmap / imshow style plot."""
        colorscale = _normalize_colorscale(cmap or "Viridis")
        trace = go.Heatmap(
            z=data, x=xticklabels, y=yticklabels,
            colorscale=colorscale,
            zmin=vmin, zmax=vmax,
            showscale=colorbar,
            **kwargs,
        )
        self._add_trace(trace)
        return self

    def imshow(self, data, cmap=None, vmin=None, vmax=None, aspect=None,
               **kwargs):
        """Display an image/2-D array (delegates to heatmap)."""
        return self.heatmap(data, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)

    def contour(self, x, y, z, levels=None, cmap=None, filled=False,
                colorbar=True, **kwargs):
        """Contour plot."""
        colorscale = _normalize_colorscale(cmap or "Viridis")
        contours_kw = {}
        if levels is not None:
            if isinstance(levels, int):
                if levels < 1:
                    raise ValueError("levels must be a positive integer")
                contours_kw = dict(start=np.min(z), end=np.max(z),
                                   size=(np.max(z) - np.min(z)) / levels)
            else:
                levels = np.asarray(levels)
                if levels.ndim != 1 or len(levels) < 2:
                    raise ValueError("levels must contain at least two values")
                if not np.allclose(np.diff(levels), np.diff(levels)[0]):
                    raise NotImplementedError(
                        "Plotly contour traces require evenly spaced levels"
                    )
                contours_kw = dict(start=levels[0], end=levels[-1],
                                   size=levels[1] - levels[0])
        trace = go.Contour(
            x=np.asarray(x), y=np.asarray(y), z=np.asarray(z),
            contours=contours_kw,
            colorscale=colorscale,
            showscale=colorbar,
            contours_coloring="heatmap" if filled else "lines",
            **kwargs,
        )
        self._add_trace(trace)
        return self

    def contourf(self, x, y, z, levels=None, cmap=None, colorbar=True,
                 **kwargs):
        """Filled contour plot."""
        return self.contour(x, y, z, levels=levels, cmap=cmap, filled=True,
                            colorbar=colorbar, **kwargs)

    def pcolormesh(self, x, y, z, cmap=None, vmin=None, vmax=None,
                   shading='auto', colorbar=True, **kwargs):
        """Pseudocolor plot of a 2D array (like matplotlib's pcolormesh).

        Args:
            x: 1D or 2D array of x coordinates
            y: 1D or 2D array of y coordinates
            z: 2D array of values to plot
            cmap: Colormap name (e.g., 'Viridis', 'Plasma', 'RdBu'). Defaults to 'Plasma'.
            vmin: Minimum value for colorscale
            vmax: Maximum value for colorscale
            shading: 'auto', 'flat', or 'gouraud' (for compatibility, mostly ignored)
            colorbar: Whether to show colorbar
        """
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        if z.ndim != 2:
            raise ValueError("z must be a two-dimensional array")

        if shading not in {"auto", "flat", "nearest"}:
            raise NotImplementedError(
                "qplotly.pcolormesh supports shading='auto', 'flat', or 'nearest'"
            )

        # Match Matplotlib's default image colormap.
        if cmap is None:
            cmap = "Viridis"
        cmap = _normalize_colorscale(cmap)

        # Handle 1D x and y arrays (most common case)
        if x.ndim == 1 and y.ndim == 1:
            if len(x) not in {z.shape[1], z.shape[1] + 1}:
                raise ValueError(
                    "x length must match z columns or provide cell edges"
                )
            if len(y) not in {z.shape[0], z.shape[0] + 1}:
                raise ValueError(
                    "y length must match z rows or provide cell edges"
                )
            # Plotly Heatmap expects x and y as 1D arrays
            trace = go.Heatmap(
                x=x, y=y, z=z,
                colorscale=cmap,
                zmin=vmin, zmax=vmax,
                showscale=colorbar,
                hovertemplate='x: %{x}<br>y: %{y}<br>z: %{z}<extra></extra>',
                **kwargs,
            )
        else:
            # For 2D x and y, flatten or use first row/column
            if x.ndim == 2:
                x = x[0, :]  # Use first row
            if y.ndim == 2:
                y = y[:, 0]  # Use first column
            trace = go.Heatmap(
                x=x, y=y, z=z,
                colorscale=cmap,
                zmin=vmin, zmax=vmax,
                showscale=colorbar,
                hovertemplate='x: %{x}<br>y: %{y}<br>z: %{z}<extra></extra>',
                **kwargs,
            )

        self._add_trace(trace)
        return self

    # ---- annotation helpers -----------------------------------------------

    def axhline(self, y=0, color="black", linestyle="solid", linewidth=1,
                label=None, **kwargs):
        """Horizontal line across the axes."""
        opacity = kwargs.pop("alpha", kwargs.pop("opacity", None))
        kwargs.pop("zorder", None)
        kwargs.pop("clip_on", None)
        self._fig.add_hline(
            y=y,
            line_dash=_normalize_linestyle(linestyle),
            line_color=color,
            line_width=linewidth,
            opacity=opacity,
            row=self._row, col=self._col,
            **kwargs,
        )
        return self

    def axvline(self, x=0, color="black", linestyle="solid", linewidth=1,
                label=None, **kwargs):
        """Vertical line across the axes."""
        opacity = kwargs.pop("alpha", kwargs.pop("opacity", None))
        kwargs.pop("zorder", None)
        kwargs.pop("clip_on", None)
        self._fig.add_vline(
            x=x,
            line_dash=_normalize_linestyle(linestyle),
            line_color=color,
            line_width=linewidth,
            opacity=opacity,
            row=self._row, col=self._col,
            **kwargs,
        )
        return self

    def axhspan(self, ymin, ymax, color="gray", alpha=0.3, **kwargs):
        kwargs.pop("zorder", None)
        kwargs.pop("clip_on", None)
        self._fig.add_hrect(
            y0=ymin, y1=ymax, fillcolor=color, opacity=alpha,
            line_width=0, row=self._row, col=self._col,
            **kwargs,
        )
        return self

    def axvspan(self, xmin, xmax, color="gray", alpha=0.3, **kwargs):
        kwargs.pop("zorder", None)
        kwargs.pop("clip_on", None)
        self._fig.add_vrect(
            x0=xmin, x1=xmax, fillcolor=color, opacity=alpha,
            line_width=0, row=self._row, col=self._col,
            **kwargs,
        )
        return self

    def text(self, x, y, s, fontsize=12, color="black", ha="left",
             va="bottom", **kwargs):
        """Add text annotation at data coordinates."""
        xanchor = {"left": "left", "center": "center", "right": "right"}.get(ha, "left")
        yanchor = {"top": "top", "center": "middle", "bottom": "bottom"}.get(va, "bottom")
        font = _pop_font_options(kwargs, fontsize)
        font.setdefault("color", color)
        textangle = kwargs.pop("rotation", kwargs.pop("textangle", 0))
        opacity = kwargs.pop("alpha", kwargs.pop("opacity", None))
        bbox = dict(kwargs.pop("bbox", {}) or {})
        kwargs.pop("transform", None)
        kwargs.pop("clip_on", None)
        annotation_options = {
            key: value
            for key, value in kwargs.items()
            if key in go.layout.Annotation()._valid_props
        }
        if bbox:
            annotation_options.setdefault(
                "bgcolor", bbox.pop("facecolor", bbox.pop("fc", None))
            )
            annotation_options.setdefault(
                "bordercolor", bbox.pop("edgecolor", bbox.pop("ec", None))
            )
            annotation_options.setdefault(
                "borderwidth",
                bbox.pop("linewidth", bbox.pop("lw", None)),
            )
            annotation_options = {
                key: value
                for key, value in annotation_options.items()
                if value is not None
            }
        self._fig.add_annotation(
            x=x, y=y, text=s,
            showarrow=False,
            font=font,
            xanchor=xanchor, yanchor=yanchor,
            xref=self._xref(), yref=self._yref(),
            textangle=textangle,
            opacity=opacity,
            **annotation_options,
        )
        return self

    def annotate(self, text, xy, xytext=None, arrowprops=None, fontsize=12,
                 color="black", **kwargs):
        """Annotate a point with optional arrow."""
        ax_x, ax_y = xy
        show_arrow = xytext is not None
        if xytext is None:
            xytext = xy
        arrowprops = dict(arrowprops or {})
        arrowstyle = arrowprops.pop("arrowstyle", "->")
        arrowhead = {
            "->": 2,
            "-|>": 3,
            "simple": 1,
            "-": 0,
        }.get(arrowstyle, 2)
        arrowcolor = arrowprops.pop(
            "color",
            arrowprops.pop(
                "edgecolor",
                arrowprops.pop("facecolor", color),
            ),
        )
        arrowwidth = arrowprops.pop(
            "linewidth",
            arrowprops.pop("lw", arrowprops.pop("width", 1)),
        )
        arrowsize = arrowprops.pop(
            "arrowsize",
            max(float(arrowprops.pop("headwidth", 3)) / 3, 0.3),
        )
        for ignored in (
            "connectionstyle",
            "headlength",
            "head_starts_at_zero",
            "patchA",
            "patchB",
            "relpos",
            "shrink",
            "shrinkA",
            "shrinkB",
        ):
            arrowprops.pop(ignored, None)
        arrowprops = {
            key: value
            for key, value in arrowprops.items()
            if key in go.layout.Annotation()._valid_props
        }
        font = _pop_font_options(kwargs, fontsize)
        font.setdefault("color", color)
        textangle = kwargs.pop("rotation", kwargs.pop("textangle", 0))
        kwargs.pop("xycoords", None)
        kwargs.pop("textcoords", None)
        kwargs.pop("annotation_clip", None)
        kwargs = {
            key: value
            for key, value in kwargs.items()
            if key in go.layout.Annotation()._valid_props
        }
        self._fig.add_annotation(
            x=ax_x, y=ax_y,
            ax=xytext[0], ay=xytext[1],
            text=text, showarrow=show_arrow,
            font=font,
            arrowhead=arrowhead,
            arrowcolor=arrowcolor,
            arrowwidth=arrowwidth,
            arrowsize=arrowsize,
            textangle=textangle,
            xref=self._xref(), yref=self._yref(),
            axref=self._xref(), ayref=self._yref(),
            **arrowprops,
            **kwargs,
        )
        return self

    # ---- axis references for annotations in subplots ----------------------
    def _xref(self):
        idx = self._parent._subplot_index(self._row, self._col)
        return "x" if idx == 1 else f"x{idx}"

    def _yref(self):
        idx = self._parent._subplot_index(self._row, self._col)
        return "y" if idx == 1 else f"y{idx}"

    # ======================= axis / label methods ==========================

    def xlabel(self, label, fontsize=None, **kwargs):
        font = _pop_font_options(kwargs, fontsize)
        standoff = kwargs.pop("labelpad", kwargs.pop("standoff", None))
        kwargs.pop("loc", None)
        title = dict(text=label)
        if font:
            title["font"] = font
        if standoff is not None:
            title["standoff"] = standoff
        valid = go.layout.xaxis.Title()._valid_props
        title.update({key: value for key, value in kwargs.items() if key in valid})
        self._fig.update_layout(**{
            self._xaxis_name(): dict(title=title)
        })
        return self

    def ylabel(self, label, fontsize=None, **kwargs):
        font = _pop_font_options(kwargs, fontsize)
        standoff = kwargs.pop("labelpad", kwargs.pop("standoff", None))
        kwargs.pop("loc", None)
        title = dict(text=label)
        if font:
            title["font"] = font
        if standoff is not None:
            title["standoff"] = standoff
        valid = go.layout.yaxis.Title()._valid_props
        title.update({key: value for key, value in kwargs.items() if key in valid})
        self._fig.update_layout(**{
            self._yaxis_name(): dict(title=title)
        })
        return self

    def title(self, label, fontsize=None, **kwargs):
        if self._parent._nrows == 1 and self._parent._ncols == 1:
            font = _pop_font_options(kwargs, fontsize)
            loc = kwargs.pop("loc", "center")
            x_positions = {
                "left": (0, "left"),
                "center": (0.5, "center"),
                "right": (1, "right"),
            }
            x, xanchor = x_positions.get(loc, x_positions["center"])
            title_options = dict(
                text=label,
                x=x,
                xanchor=xanchor,
            )
            if font:
                title_options["font"] = font
            title_options.update(kwargs)
            self._fig.update_layout(title=title_options)
        else:
            idx = self._parent._subplot_index(self._row, self._col)
            annotation = self._parent._subplot_title_annotations.get(idx)
            font = _pop_font_options(kwargs, fontsize)
            kwargs.pop("loc", None)
            if annotation is None:
                xref = f"{self._xref()} domain"
                yref = f"{self._yref()} domain"
                self._fig.add_annotation(
                    text=label,
                    xref=xref, yref=yref,
                    x=0.5, y=1, yshift=18,
                    xanchor="center", yanchor="bottom",
                    showarrow=False,
                    font=font or dict(size=14),
                    **kwargs,
                )
                annotation = self._fig.layout.annotations[-1]
                self._parent._subplot_title_annotations[idx] = annotation
            else:
                annotation.text = label
                if font:
                    annotation.font = dict(annotation.font.to_plotly_json(), **font)
                for key, value in kwargs.items():
                    setattr(annotation, key, value)
        return self

    def xlim(self, *args, left=None, right=None):
        """Set x-axis limits. ``xlim(lo, hi)`` or ``xlim((lo, hi))``."""
        if not args and left is None and right is None:
            axis_range = getattr(self._fig.layout, self._xaxis_name()).range
            return tuple(axis_range) if axis_range is not None else None
        if len(args) == 1:
            lo, hi = args[0]
        elif len(args) == 2:
            lo, hi = args
        elif not args:
            current = self.xlim() or (None, None)
            lo = current[0] if left is None else left
            hi = current[1] if right is None else right
        else:
            raise TypeError("xlim() accepts zero, one, or two positional arguments")
        self._fig.update_layout(**{
            self._xaxis_name(): dict(range=[lo, hi])
        })
        return self

    def ylim(self, *args, bottom=None, top=None):
        """Set y-axis limits."""
        if not args and bottom is None and top is None:
            axis_range = getattr(self._fig.layout, self._yaxis_name()).range
            return tuple(axis_range) if axis_range is not None else None
        if len(args) == 1:
            lo, hi = args[0]
        elif len(args) == 2:
            lo, hi = args
        elif not args:
            current = self.ylim() or (None, None)
            lo = current[0] if bottom is None else bottom
            hi = current[1] if top is None else top
        else:
            raise TypeError("ylim() accepts zero, one, or two positional arguments")
        self._fig.update_layout(**{
            self._yaxis_name(): dict(range=[lo, hi])
        })
        return self

    def xscale(self, scale):
        """Set x-axis scale: 'linear' or 'log'."""
        if scale not in {"linear", "log"}:
            raise NotImplementedError(
                "qplotly supports only 'linear' and 'log' x-axis scales"
            )
        self._fig.update_layout(**{
            self._xaxis_name(): dict(type=scale)
        })
        return self

    def yscale(self, scale):
        """Set y-axis scale: 'linear' or 'log'."""
        if scale not in {"linear", "log"}:
            raise NotImplementedError(
                "qplotly supports only 'linear' and 'log' y-axis scales"
            )
        self._fig.update_layout(**{
            self._yaxis_name(): dict(type=scale)
        })
        return self

    def xticks(self, ticks=None, labels=None, rotation=None, fontsize=None):
        update = {}
        if ticks is not None:
            update["tickvals"] = ticks
        if labels is not None:
            update["ticktext"] = labels
        if rotation is not None:
            update["tickangle"] = rotation
        if fontsize is not None:
            update["tickfont"] = dict(size=fontsize)
        self._fig.update_layout(**{self._xaxis_name(): update})
        return self

    def yticks(self, ticks=None, labels=None, rotation=None, fontsize=None):
        update = {}
        if ticks is not None:
            update["tickvals"] = ticks
        if labels is not None:
            update["ticktext"] = labels
        if rotation is not None:
            update["tickangle"] = rotation
        if fontsize is not None:
            update["tickfont"] = dict(size=fontsize)
        self._fig.update_layout(**{self._yaxis_name(): update})
        return self

    def grid(self, visible=True, which="major", axis="both", **kwargs):
        """Toggle grid lines."""
        if which not in {"major", "both"}:
            raise NotImplementedError("Plotly does not expose minor-grid styling")
        if axis not in {"both", "x", "y"}:
            raise ValueError("axis must be 'both', 'x', or 'y'")
        show = visible
        grid_options = {"showgrid": show}
        color = kwargs.pop("color", kwargs.pop("gridcolor", None))
        linewidth = kwargs.pop("linewidth", kwargs.pop("gridwidth", None))
        kwargs.pop("linestyle", kwargs.pop("ls", None))
        alpha = kwargs.pop("alpha", None)
        if color is not None:
            grid_options["gridcolor"] = (
                _rgba(color, alpha) if alpha is not None else color
            )
        if linewidth is not None:
            grid_options["gridwidth"] = linewidth
        grid_options.update(kwargs)
        if axis in ("both", "x"):
            self._fig.update_layout(**{
                self._xaxis_name(): grid_options
            })
        if axis in ("both", "y"):
            self._fig.update_layout(**{
                self._yaxis_name(): grid_options
            })
        return self

    def legend(self, show=True, loc=None, fontsize=None, frameon=True,
               fancybox=True, shadow=False, framealpha=None, facecolor=None,
               edgecolor=None, **kwargs):
        """Show / configure the legend.

        Args:
            show: Whether to show the legend
            loc: Location string (matplotlib-compatible)
            fontsize: Font size for legend text
            frameon: Whether to draw a frame around the legend
            fancybox: Use rounded corners (default True, like matplotlib).
                     NOTE: Accepted for API compatibility but not visually
                     rendered due to Plotly limitations. Legends will have
                     square corners regardless of this parameter.
            shadow: Ignored (for matplotlib compatibility)
            framealpha: Frame transparency (0-1), default 1.0 (opaque)
            facecolor: Background color, default 'white'
            edgecolor: Border color, default 'black'
        """
        # Store legend config for this axes
        self._legend_config = {
            'show': show,
            'loc': loc or 'upper right',
            'fontsize': fontsize,
            'frameon': frameon,
            'fancybox': fancybox,
            'framealpha': framealpha,
            'facecolor': facecolor,
            'edgecolor': edgecolor,
            'kwargs': kwargs
        }

        # For single subplot, use standard Plotly legend
        if self._parent._nrows == 1 and self._parent._ncols == 1:
            self._apply_single_legend()
        else:
            # For subplots, mark that this axes needs a legend
            # Actual rendering happens in show() via _apply_subplot_legends()
            pass

        return self

    def _apply_single_legend(self):
        """Apply legend for single-plot figures (standard Plotly legend)."""
        config = self._legend_config
        for trace_idx in self._legend_traces:
            if trace_idx < len(self._fig.data):
                self._fig.data[trace_idx].showlegend = bool(config["show"])

        legend_kw = dict(
            visible=config['show'],
            bgcolor=config['facecolor'] or 'white',
            bordercolor=config['edgecolor'] or '#cccccc',
            borderwidth=1 if config['frameon'] else 0,
        )

        # Note: fancybox (rounded corners) not supported by Plotly legends
        # Kept for matplotlib API compatibility but has no visual effect

        if config['fontsize']:
            legend_kw["font"] = dict(size=config['fontsize'])

        if config["frameon"]:
            legend_kw["bgcolor"] = _rgba(
                config['facecolor'] or 'white',
                0.8 if config["framealpha"] is None else config["framealpha"],
            )
        else:
            legend_kw["bgcolor"] = "rgba(0,0,0,0)"

        x, y, xanchor, yanchor = _LEGEND_LOCATIONS.get(
            config["loc"], _LEGEND_LOCATIONS["upper right"]
        )
        legend_kw.update(
            x=x,
            y=y,
            xanchor=xanchor,
            yanchor=yanchor,
            xref="paper",
            yref="paper",
        )

        extra = _filter_legend_options(config['kwargs'])
        ncol = extra.pop("ncol", extra.pop("ncols", None))
        if ncol is not None and ncol > 1:
            extra.setdefault("orientation", "h")
        legend_kw.update(extra)
        self._fig.update_layout(showlegend=config["show"], legend=legend_kw)
        return self

    def invert_xaxis(self):
        axis = getattr(self._fig.layout, self._xaxis_name())
        if axis.range is not None:
            update = dict(range=list(reversed(axis.range)))
        else:
            update = dict(
                autorange=True if axis.autorange == "reversed" else "reversed"
            )
        self._fig.update_layout(**{self._xaxis_name(): update})
        return self

    def invert_yaxis(self):
        axis = getattr(self._fig.layout, self._yaxis_name())
        if axis.range is not None:
            update = dict(range=list(reversed(axis.range)))
        else:
            update = dict(
                autorange=True if axis.autorange == "reversed" else "reversed"
            )
        self._fig.update_layout(**{self._yaxis_name(): update})
        return self

    def set_aspect(self, aspect):
        """Rough aspect-ratio control."""
        if aspect == "equal":
            self._fig.update_layout(**{
                self._yaxis_name(): dict(scaleanchor=self._xref(),
                                         scaleratio=1)
            })
        elif aspect not in {"auto", None}:
            raise NotImplementedError(
                "qplotly supports only aspect='auto' and aspect='equal'"
            )
        return self

    # Matplotlib Axes spellings, alongside the pyplot-like short forms.
    set_xlabel = xlabel
    set_ylabel = ylabel
    set_title = title
    set_xlim = xlim
    set_ylim = ylim
    set_xscale = xscale
    set_yscale = yscale
    set_xticks = xticks
    set_yticks = yticks

    def get_xlim(self):
        return self.xlim()

    def get_ylim(self):
        return self.ylim()

    def colorbar(self, title=None, fontsize=None, x=None, len_=None,
                 thickness=20, **kwargs):
        """Add/configure colorbar for the last heatmap trace on this axis.

        Positions the colorbar immediately to the right of this subplot,
        scaled to match the subplot height.

        Args:
            title: Colorbar title/label text
            fontsize: Title font size (default: auto)
            x: Horizontal position (default: right edge of subplot + 0.02)
            len_: Colorbar length as fraction of figure (default: subplot height)
            thickness: Colorbar width in pixels (default: 20)
            **kwargs: Additional plotly colorbar dict properties
        """
        fig = self._parent._fig
        axis_idx = self._parent._subplot_index(self._row, self._col)
        yaxis_key = f"yaxis{axis_idx}" if axis_idx > 1 else "yaxis"
        xaxis_key = f"xaxis{axis_idx}" if axis_idx > 1 else "xaxis"

        target = self._find_color_trace()
        if target is None:
            warnings.warn(
                "colorbar() found no heatmap, contour, or color-mapped scatter "
                "on this axes",
                RuntimeWarning,
                stacklevel=2,
            )
            return self
        target_trace, colorbar_owner = target

        yaxis_obj = getattr(fig.layout, yaxis_key)
        xaxis_obj = getattr(fig.layout, xaxis_key)
        y_domain = yaxis_obj.domain or [0, 1]
        x_domain = xaxis_obj.domain or [0, 1]

        if x is None:
            x = x_domain[1] + 0.04
        if len_ is None:
            len_ = y_domain[1] - y_domain[0]

        cb_dict = dict(
            x=x,
            xpad=10,
            y=(y_domain[0] + y_domain[1]) / 2,
            len=len_,
            thickness=thickness,
            yanchor='middle',
        )
        if title:
            title_dict = dict(text=title, side='right')
            if fontsize:
                title_dict['font'] = dict(size=fontsize)
            cb_dict['title'] = title_dict
        cb_dict.update(kwargs)

        colorbar_owner.colorbar = cb_dict
        if colorbar_owner is target_trace:
            target_trace.showscale = True
        else:
            colorbar_owner.showscale = True
        return self

    def _find_color_trace(self):
        """Return the latest color-mapped trace and its colorbar owner."""
        expected_xref = self._xref()
        expected_yref = self._yref()
        for trace in reversed(self._fig.data):
            trace_xref = getattr(trace, "xaxis", None) or "x"
            trace_yref = getattr(trace, "yaxis", None) or "y"
            if trace_xref != expected_xref or trace_yref != expected_yref:
                continue
            if trace.type in {"heatmap", "contour", "histogram2d"}:
                return trace, trace
            marker_options = getattr(trace, "marker", None)
            if (
                marker_options is not None
                and marker_options.colorscale is not None
            ):
                return trace, marker_options
        return None

    def twinx(self):
        """Create a twin Axes sharing the x-axis (secondary y-axis)."""
        ax2 = _TwinAxes(self._parent, self._row, self._col, secondary_y=True)
        return ax2


# ===========================================================================
#  _TwinAxes  — lightweight secondary-y support
# ===========================================================================
class _TwinAxes(Axes):
    """Axes that plots on a secondary y-axis."""

    def __init__(self, parent, row, col, secondary_y=True):
        super().__init__(parent, row, col)
        self._secondary_y = secondary_y
        (
            self._secondary_yaxis_name,
            self._secondary_yref,
            self._legend_index,
        ) = parent._allocate_secondary_yaxis(
            base_xref=super()._xref(),
            base_yref=super()._yref(),
        )
        parent._extra_axes.append(self)

    def _add_trace(self, trace):
        trace.xaxis = super()._xref()
        trace.yaxis = self._secondary_yref
        self._fig.add_trace(trace)
        trace_idx = len(self._fig.data) - 1
        self._record_trace(trace_idx, trace)
        return trace_idx

    def _yaxis_name(self):
        return self._secondary_yaxis_name

    def _yref(self):
        return self._secondary_yref


# ===========================================================================
#  QFigure — top-level figure, delegates to a default Axes
# ===========================================================================
class QFigure:
    """Top-level figure container, analogous to ``matplotlib.figure.Figure``.

    When used without explicit subplots, all plotting methods are forwarded
    to an internal default :class:`Axes`.
    """

    def __init__(self, fig=None, nrows=1, ncols=1, figsize=None,
                 subplot_titles=None, sharex=False, sharey=False,
                 **make_subplots_kwargs):
        if not isinstance(nrows, int) or not isinstance(ncols, int):
            raise TypeError("nrows and ncols must be integers")
        if nrows < 1 or ncols < 1:
            raise ValueError("nrows and ncols must be at least 1")
        self._nrows = nrows
        self._ncols = ncols

        if fig is not None:
            self._fig = fig
        elif nrows == 1 and ncols == 1:
            self._fig = go.Figure()
        else:
            shared_x = _normalize_share(sharex)
            shared_y = _normalize_share(sharey)
            self._fig = make_subplots(
                rows=nrows, cols=ncols,
                subplot_titles=subplot_titles,
                shared_xaxes=shared_x,
                shared_yaxes=shared_y,
                **make_subplots_kwargs,
            )

        if figsize:
            w, h = figsize
            self._fig.update_layout(width=w * 100, height=h * 100)

        # Apply default matplotlib-like styling
        self._apply_default_style()

        # Track auto-colored traces for smart color scheme application
        # Store tuples of (trace_idx, axes) to enable per-subplot coloring
        self._auto_colored_trace_indices = []

        # Colorbar tracking for automatic colorbar support
        self._colorbar_values = None  # Values to map to colors
        self._colorbar_label = None   # Label for colorbar
        self._colorbar_colors = None  # Hex colors used
        self._colorbar_added = False  # Track if colorbar already added
        self._colorbar_trace_index = None
        self._next_secondary_yaxis = nrows * ncols + 1
        self._extra_axes = []

        # Build axes grid
        self._axes_grid = [
            [Axes(self, r + 1, c + 1) for c in range(ncols)]
            for r in range(nrows)
        ]
        self._default_ax = self._axes_grid[0][0]

        # Keep stable references to Plotly's generated subplot-title annotations.
        self._subplot_title_annotations = {}
        if subplot_titles:
            annotation_iter = iter(self._fig.layout.annotations or ())
            for index, title_text in enumerate(subplot_titles, start=1):
                if title_text:
                    annotation = next(annotation_iter, None)
                    if annotation is not None:
                        self._subplot_title_annotations[index] = annotation

    # ---- default styling --------------------------------------------------
    def _apply_default_style(self):
        """Apply matplotlib-like default styling."""
        # Default layout settings
        layout_updates = dict(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family='DejaVu Sans, Arial, sans-serif',
                size=10,
                color='black'
            ),
        )

        # Apply to all xaxis and yaxis
        for i in range(1, self._nrows * self._ncols + 1):
            xaxis_name = f"xaxis{i}" if i > 1 else "xaxis"
            yaxis_name = f"yaxis{i}" if i > 1 else "yaxis"

            axis_style = dict(
                showline=True,
                linewidth=0.8,
                linecolor='black',
                mirror=True,
                showgrid=False,
                gridwidth=0.8,
                gridcolor='#b0b0b0',
                zeroline=False,
                ticks='outside',
                ticklen=3.5,
                tickwidth=0.8,
                tickcolor='black',
            )

            layout_updates[xaxis_name] = axis_style.copy()
            layout_updates[yaxis_name] = axis_style.copy()

        self._fig.update_layout(**layout_updates)

    def _apply_tight_layout(self):
        """Apply tight layout (matplotlib-style) by reducing margins."""
        # Matplotlib tight_layout reduces whitespace around plots
        # In Plotly, this is achieved by setting smaller margins
        self._fig.update_layout(
            margin=dict(l=60, r=30, t=80, b=60)  # left, right, top, bottom
        )

    # ---- subplot index helper ---------------------------------------------
    def _subplot_index(self, row, col):
        """Return the 1-based linear index for (row, col)."""
        return (row - 1) * self._ncols + col

    def _allocate_secondary_yaxis(self, base_xref, base_yref):
        """Allocate a secondary y-axis without colliding across subplots."""
        layout_keys = self._fig.layout.to_plotly_json()
        while (
            f"yaxis{self._next_secondary_yaxis}" in layout_keys
            or self._next_secondary_yaxis == 1
        ):
            self._next_secondary_yaxis += 1

        index = self._next_secondary_yaxis
        self._next_secondary_yaxis += 1
        axis_name = f"yaxis{index}"
        axis_ref = f"y{index}"
        self._fig.update_layout(**{
            axis_name: dict(
                overlaying=base_yref,
                side="right",
                anchor=base_xref,
                showgrid=False,
            )
        })
        return axis_name, axis_ref, index

    # ---- access to axes grid ----------------------------------------------
    @property
    def axes(self):
        """Return axes grid (list of lists for 2-D, flat list for 1-D)."""
        if self._nrows == 1 and self._ncols == 1:
            return self._default_ax
        if self._nrows == 1:
            return self._axes_grid[0]
        if self._ncols == 1:
            return [row[0] for row in self._axes_grid]
        return self._axes_grid

    # ---- forward all Axes methods on the default axes ---------------------
    def __getattr__(self, name):
        # Avoid recursion for private/dunder attrs
        if name.startswith("_"):
            raise AttributeError(name)
        attribute = getattr(self._default_ax, name)
        if not callable(attribute):
            return attribute

        @wraps(attribute)
        def delegated(*args, **kwargs):
            result = attribute(*args, **kwargs)
            return self if result is self._default_ax else result

        return delegated

    def gca(self, row=1, col=1):
        """Return the axes at the one-based subplot position."""
        if not 1 <= row <= self._nrows or not 1 <= col <= self._ncols:
            raise IndexError("subplot row or column is out of range")
        return self._axes_grid[row - 1][col - 1]

    # ---- figure-level methods ---------------------------------------------

    def suptitle(self, title, fontsize=None, **kwargs):
        font = _pop_font_options(kwargs, fontsize)
        title_options = dict(text=title)
        if font:
            title_options["font"] = font
        title_options.update(kwargs)
        self._fig.update_layout(title=title_options)
        return self

    def tight_layout(self):
        """No-op for API compatibility (Plotly auto-manages margins)."""
        self._fig.update_layout(margin=dict(l=60, r=40, t=60, b=60))
        return self

    def set_template(self, template):
        """Set a Plotly template: 'plotly', 'plotly_dark', 'ggplot2', etc."""
        self._fig.update_layout(template=template)
        return self

    def update_layout(self, **kwargs):
        """Pass-through to the underlying Plotly figure layout."""
        self._fig.update_layout(**kwargs)
        return self

    # ---- auto color scheme ------------------------------------------------

    def _apply_auto_color_scheme(self):
        """Compatibility no-op: colors are assigned deterministically at plot time."""

    # ---- subplot legends --------------------------------------------------

    def _apply_subplot_legends(self):
        """Apply idempotent, native Plotly legends to each subplot."""
        if self._nrows == 1 and self._ncols == 1:
            return  # Single plot uses standard legend

        self._fig.update_layout(showlegend=True)

        axes_to_apply = [
            ax for row_axes in self._axes_grid for ax in row_axes
        ] + self._extra_axes
        for ax in axes_to_apply:
            if ax._legend_config is None or not ax._has_legend_entries:
                continue

            config = ax._legend_config
            subplot_idx = self._subplot_index(ax._row, ax._col)
            xaxis_name = f"xaxis{subplot_idx}" if subplot_idx > 1 else "xaxis"
            yaxis_name = f"yaxis{subplot_idx}" if subplot_idx > 1 else "yaxis"
            xaxis = self._fig.layout[xaxis_name]
            yaxis = self._fig.layout[yaxis_name]
            xdomain = xaxis.domain if xaxis.domain else [0, 1]
            ydomain = yaxis.domain if yaxis.domain else [0, 1]

            x_frac, y_frac, xanchor, yanchor = _LEGEND_LOCATIONS.get(
                config["loc"], _LEGEND_LOCATIONS["upper right"]
            )
            x_paper = xdomain[0] + (xdomain[1] - xdomain[0]) * x_frac
            y_paper = ydomain[0] + (ydomain[1] - ydomain[0]) * y_frac

            legend_idx = getattr(ax, "_legend_index", subplot_idx)
            legend_ref = (
                "legend" if legend_idx == 1 else f"legend{legend_idx}"
            )
            for trace_idx in ax._legend_traces:
                if trace_idx < len(self._fig.data):
                    trace = self._fig.data[trace_idx]
                    trace.legend = legend_ref
                    trace.showlegend = bool(config["show"])

            legend_kw = dict(
                visible=config["show"],
                x=x_paper,
                y=y_paper,
                xanchor=xanchor,
                yanchor=yanchor,
                xref="paper",
                yref="paper",
                bgcolor=config["facecolor"] or "white",
                bordercolor=config["edgecolor"] or "#cccccc",
                borderwidth=1 if config["frameon"] else 0,
            )
            if config["fontsize"] is not None:
                legend_kw["font"] = dict(size=config["fontsize"])
            if config["frameon"]:
                legend_kw["bgcolor"] = _rgba(
                    config["facecolor"] or "white",
                    0.8 if config["framealpha"] is None
                    else config["framealpha"],
                )
            else:
                legend_kw["bgcolor"] = "rgba(0,0,0,0)"
            extra = _filter_legend_options(config["kwargs"])
            ncol = extra.pop("ncol", extra.pop("ncols", None))
            if ncol is not None and ncol > 1:
                extra.setdefault("orientation", "h")
            legend_kw.update(extra)
            self._fig.update_layout(**{legend_ref: legend_kw})

    # ---- display / export -------------------------------------------------

    def _prepare_for_output(self, tight_layout=False):
        self._apply_auto_color_scheme()
        self._apply_subplot_legends()
        if tight_layout:
            self._apply_tight_layout()

    def show(self, renderer=None, tight_layout=True, **kwargs):
        """Show the figure.

        Parameters
        ----------
        renderer : str, optional
            Renderer to use for display
        tight_layout : bool, default True
            If True, automatically adjust margins (matplotlib-style)
        **kwargs : dict
            Additional arguments passed to plotly show()
        """
        self._prepare_for_output(tight_layout=tight_layout)
        self._fig.show(renderer=renderer, **kwargs)

    def savefig(self, filename, width=None, height=None, scale=None, tight_layout=True, **kwargs):
        """Save to file (png, jpg, svg, pdf, html, json).

        Raster formats require ``kaleido`` (``pip install -U kaleido``).

        Parameters
        ----------
        filename : str
            Output filename
        width : int, optional
            Width in pixels
        height : int, optional
            Height in pixels
        scale : float, optional
            Scaling factor
        tight_layout : bool, default True
            If True, automatically adjust margins (matplotlib-style)
        **kwargs : dict
            Additional arguments
        """
        self._prepare_for_output(tight_layout=tight_layout)
        filename = str(filename)
        suffix = filename.lower()
        if suffix.endswith(".html"):
            self._fig.write_html(filename, **kwargs)
        elif suffix.endswith(".json"):
            self._fig.write_json(filename, **kwargs)
        else:
            self._fig.write_image(filename, width=width, height=height,
                                  scale=scale, **kwargs)
        return self

    def savefig_matplotlib(self, filename=None, dpi=300, tight_layout=True,
                           save_dir='.', fmt='png', **kwargs):
        """Save figure as a static image by cloning to matplotlib.

        If no filename is provided, auto-generates one from axis labels:
            YYMMDD_HHMMSS_ylabel_vs_xlabel.png
        - Units in brackets are stripped: "Time [ns]" -> "Time_ns"
        - Spaces replaced with underscores
        - If labels are empty: "unspecified_N" where N increments

        Parameters
        ----------
        filename : str, optional
            Output filename. If None, auto-generates from axis labels.
        dpi : int, default 300
            Resolution in dots per inch
        tight_layout : bool, default True
            Apply tight_layout to minimize whitespace
        save_dir : str, default '.'
            Directory for auto-generated filenames (ignored if filename given)
        fmt : str, default 'png'
            File format for auto-generated filenames (ignored if filename given)
        **kwargs : dict
            Additional arguments passed to matplotlib savefig

        Returns
        -------
        str
            Path to the saved file
        """
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        # Apply plotly formatting first
        self._apply_auto_color_scheme()
        self._apply_subplot_legends()

        # Create matplotlib figure
        if self._nrows == 1 and self._ncols == 1:
            fig_mpl, ax_mpl = plt.subplots(1, 1, figsize=(10, 6), dpi=dpi)
            axes_mpl = [[ax_mpl]]
        else:
            fig_mpl, axes_mpl = plt.subplots(self._nrows, self._ncols,
                                              figsize=(10, 6), dpi=dpi,
                                              squeeze=False)

        # Convert each subplot
        for i in range(self._nrows):
            for j in range(self._ncols):
                ax_mpl = axes_mpl[i][j]
                subplot_idx = self._subplot_index(i + 1, j + 1)

                for trace in self._fig.data:
                    xaxis_ref = trace.xaxis if hasattr(trace, 'xaxis') else f'x{subplot_idx}' if subplot_idx > 1 else 'x'
                    expected_ref = f'x{subplot_idx}' if subplot_idx > 1 else 'x'

                    if self._nrows == 1 and self._ncols == 1:
                        belongs_to_subplot = True
                    else:
                        belongs_to_subplot = (xaxis_ref == expected_ref)

                    if not belongs_to_subplot:
                        continue

                    if trace.type == 'scatter':
                        x = trace.x if hasattr(trace, 'x') and trace.x is not None else []
                        y = trace.y if hasattr(trace, 'y') and trace.y is not None else []

                        color = trace.line.color if hasattr(trace, 'line') and trace.line and trace.line.color else None
                        linewidth = trace.line.width if hasattr(trace, 'line') and trace.line and trace.line.width else 2
                        linestyle = '-'
                        if hasattr(trace, 'line') and trace.line and trace.line.dash:
                            dash_map = {'dash': '--', 'dot': ':', 'dashdot': '-.', 'solid': '-'}
                            linestyle = dash_map.get(trace.line.dash, '-')

                        marker = None
                        if hasattr(trace, 'mode') and trace.mode and 'markers' in trace.mode:
                            marker = 'o'
                            if hasattr(trace, 'marker') and trace.marker and trace.marker.symbol:
                                symbol_map = {'circle': 'o', 'square': 's', 'diamond': 'D',
                                            'cross': '+', 'x': 'x', 'triangle-up': '^'}
                                marker = symbol_map.get(trace.marker.symbol, 'o')

                        label = trace.name if trace.showlegend and trace.name else None

                        if marker:
                            ax_mpl.plot(x, y, color=color, linewidth=linewidth/2,
                                       linestyle=linestyle, marker=marker, label=label)
                        else:
                            ax_mpl.plot(x, y, color=color, linewidth=linewidth/2,
                                       linestyle=linestyle, label=label)

                    elif trace.type == 'bar':
                        x = trace.x if hasattr(trace, 'x') and trace.x is not None else []
                        y = trace.y if hasattr(trace, 'y') and trace.y is not None else []
                        color = trace.marker.color if hasattr(trace, 'marker') and trace.marker and trace.marker.color else None
                        label = trace.name if trace.showlegend and trace.name else None
                        ax_mpl.bar(x, y, color=color, label=label)

                    elif trace.type == 'heatmap' or trace.type == 'contour':
                        z = trace.z if hasattr(trace, 'z') and trace.z is not None else []
                        x = trace.x if hasattr(trace, 'x') and trace.x is not None else None
                        y = trace.y if hasattr(trace, 'y') and trace.y is not None else None

                        # Extract colormap from trace
                        cmap_mpl = 'viridis'
                        if hasattr(trace, 'colorscale') and trace.colorscale:
                            cs = trace.colorscale
                            if isinstance(cs, str):
                                # Try as matplotlib cmap name directly
                                try:
                                    import matplotlib.cm as _cm
                                    _cm.get_cmap(cs.lower())
                                    cmap_mpl = cs.lower()
                                except (ValueError, ImportError):
                                    cmap_mpl = 'viridis'
                            elif isinstance(cs, (list, tuple)) and len(cs) > 2:
                                try:
                                    from matplotlib.colors import (
                                        LinearSegmentedColormap,
                                        to_rgba,
                                    )
                                    positions = []
                                    colors_rgba = []
                                    for item in cs:
                                        positions.append(float(item[0]))
                                        colors_rgba.append(to_rgba(item[1]))
                                    cmap_mpl = LinearSegmentedColormap.from_list(
                                        'custom', list(zip(positions, colors_rgba)), N=256)
                                except (TypeError, ValueError):
                                    cmap_mpl = 'viridis'

                        vmin = trace.zmin if hasattr(trace, 'zmin') and trace.zmin is not None else None
                        vmax = trace.zmax if hasattr(trace, 'zmax') and trace.zmax is not None else None

                        if trace.type == 'heatmap':
                            im = ax_mpl.pcolormesh(x, y, z, shading='auto',
                                                   cmap=cmap_mpl, vmin=vmin, vmax=vmax)
                            fig_mpl.colorbar(im, ax=ax_mpl)
                        else:
                            ax_mpl.contour(x, y, z, cmap=cmap_mpl)

                # Set labels, title, and axis scale from plotly layout
                xaxis_name = f"xaxis{subplot_idx}" if subplot_idx > 1 else "xaxis"
                yaxis_name = f"yaxis{subplot_idx}" if subplot_idx > 1 else "yaxis"

                if hasattr(self._fig.layout, xaxis_name):
                    xaxis = getattr(self._fig.layout, xaxis_name)
                    if xaxis.title and xaxis.title.text:
                        ax_mpl.set_xlabel(xaxis.title.text, fontsize=14)
                    if xaxis.type == 'log':
                        ax_mpl.set_xscale('log')

                if hasattr(self._fig.layout, yaxis_name):
                    yaxis = getattr(self._fig.layout, yaxis_name)
                    if yaxis.title and yaxis.title.text:
                        ax_mpl.set_ylabel(yaxis.title.text, fontsize=14)
                    if yaxis.type == 'log':
                        ax_mpl.set_yscale('log')

                ax_mpl.grid(True, alpha=0.3)

                handles, labels = ax_mpl.get_legend_handles_labels()
                if handles and labels:
                    ax_mpl.legend(fontsize=11, framealpha=0.9)

        # Overall title
        if self._fig.layout.title and self._fig.layout.title.text:
            fig_mpl.suptitle(self._fig.layout.title.text, fontsize=16, fontweight='bold')

        if tight_layout:
            fig_mpl.tight_layout()

        # Generate filename if not provided
        if filename is None:
            import re
            from datetime import datetime
            from pathlib import Path

            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)

            xaxis = self._fig.layout.xaxis
            yaxis = self._fig.layout.yaxis
            xlabel_text = xaxis.title.text if xaxis.title and xaxis.title.text else ''
            ylabel_text = yaxis.title.text if yaxis.title and yaxis.title.text else ''

            def _clean_label(lbl):
                lbl = re.sub(r'\[([^\]]*)\]', r'\1', lbl)
                lbl = re.sub(r'\(([^\)]*)\)', r'\1', lbl)
                lbl = re.sub(r'[<>|/\\:*?"]', '', lbl)
                lbl = lbl.strip().replace(' ', '_')
                lbl = re.sub(r'_+', '_', lbl)
                return lbl.strip('_')

            timestamp = datetime.now().strftime('%y%m%d_%H%M%S')

            if xlabel_text and ylabel_text:
                basename = f'{timestamp}_{_clean_label(ylabel_text)}_vs_{_clean_label(xlabel_text)}'
            elif xlabel_text or ylabel_text:
                basename = f'{timestamp}_{_clean_label(xlabel_text or ylabel_text)}'
            else:
                existing = list(save_path.glob(f'*_unspecified_*.{fmt}'))
                basename = f'{timestamp}_unspecified_{len(existing) + 1}'

            filename = str(save_path / f'{basename}.{fmt}')

        fig_mpl.savefig(filename, dpi=dpi, bbox_inches='tight', **kwargs)
        plt.close(fig_mpl)
        print(f'Saved: {filename}')
        return filename

    def to_html(self, **kwargs):
        self._prepare_for_output()
        return self._fig.to_html(**kwargs)

    def to_json(self, **kwargs):
        self._prepare_for_output()
        return self._fig.to_json(**kwargs)

    # ---- colorbar support -------------------------------------------------

    def _auto_detect_values_from_labels(self):
        """Try to auto-detect parameter values from trace labels.

        Looks for patterns like "x=10", "10", "param=10.5" in trace names.
        Returns array of values if successful, None otherwise.
        """
        import re

        # Get all trace names/labels
        labels = []
        for trace in self._fig.data:
            if hasattr(trace, 'name') and trace.name:
                labels.append(trace.name)
            elif hasattr(trace, 'showlegend') and trace.showlegend:
                labels.append(str(trace.get('name', '')))

        if not labels or len(labels) < 5:
            return None

        # Try to extract numbers from labels
        values = []
        patterns = [
            r'[=:]\s*([-+]?[0-9]*\.?[0-9]+)',  # Matches "x=10", "param: 12.5"
            r'^([-+]?[0-9]*\.?[0-9]+)',         # Matches "10", "12.5" at start
            r'([-+]?[0-9]*\.?[0-9]+)$',         # Matches numbers at end
        ]

        for label in labels:
            extracted = None
            for pattern in patterns:
                match = re.search(pattern, str(label))
                if match:
                    try:
                        extracted = float(match.group(1))
                        break
                    except (ValueError, IndexError):
                        continue

            if extracted is not None:
                values.append(extracted)
            else:
                # Failed to extract from this label
                return None

        if len(values) == len(labels) and len(values) >= 5:
            return np.array(values)
        return None

    def attach_colorbar_values(self, values, label=None):
        """Attach parameter values for a subsequent sweep colorbar.

        Call this after plotting the line family and before
        :meth:`sweep_colorbar`.

        Parameters
        ----------
        values : array-like
            Values corresponding to each trace (e.g., sweep parameter values)
        label : str, optional
            Label for the colorbar (parameter name)

        Returns
        -------
        self : QFigure
            Returns self for method chaining

        Examples
        --------
        >>> fig, ax = qplotly.subplots()
        >>> for x in [10, 12, 14, 16, 18, 20]:
        ...     ax.plot(freq, compute_data(x))
        >>> fig.attach_colorbar_values([10, 12, 14, 16, 18, 20], label='x')
        >>> fig.sweep_colorbar()
        >>> fig.show()
        """
        self._colorbar_values = np.asarray(values)
        self._colorbar_label = label
        return self

    def sweep_colorbar(
        self,
        values=None,
        label=None,
        title=None,
        cmap="Portland",
        ax=None,
        x=1.02,
        thickness=20,
        len_=0.7,
    ):
        """Color a family of lines by parameter value and add its colorbar."""
        target_ax = ax or self._default_ax
        if not isinstance(target_ax, Axes) or target_ax._parent is not self:
            raise ValueError("ax must belong to this QFigure")

        trace_indices = [
            trace_idx
            for trace_idx, owner in self._auto_colored_trace_indices
            if owner is target_ax and trace_idx < len(self._fig.data)
        ]
        if not trace_indices:
            warnings.warn(
                "sweep_colorbar() found no automatically colored traces",
                RuntimeWarning,
                stacklevel=2,
            )
            return self

        if values is not None:
            self._colorbar_values = np.asarray(values)
        if label is not None:
            self._colorbar_label = label
        if self._colorbar_values is None:
            self._colorbar_values = self._auto_detect_values_from_labels()
        if self._colorbar_values is None:
            self._colorbar_values = np.arange(len(trace_indices), dtype=float)
            self._colorbar_label = self._colorbar_label or "Trace"

        values_array = np.asarray(self._colorbar_values, dtype=float)
        if len(values_array) != len(trace_indices):
            raise ValueError(
                "sweep colorbar values must match the number of auto-colored "
                f"traces on the axes ({len(trace_indices)})"
            )

        value_min = float(np.nanmin(values_array))
        value_max = float(np.nanmax(values_array))
        if value_max == value_min:
            positions = np.full(len(values_array), 0.5)
            marker_bounds = [value_min - 0.5, value_max + 0.5]
        else:
            positions = (values_array - value_min) / (value_max - value_min)
            marker_bounds = [value_min, value_max]

        colorscale = _normalize_colorscale(cmap)
        colors = pc.sample_colorscale(
            colorscale,
            positions.tolist(),
            colortype="rgb",
        )
        self._colorbar_colors = colors

        for trace_idx, color in zip(trace_indices, colors):
            trace = self._fig.data[trace_idx]
            if getattr(trace, "line", None) is not None:
                trace.line.color = color
            if getattr(trace, "marker", None) is not None:
                trace.marker.color = color

        colorbar_title = title if title is not None else self._colorbar_label
        marker = dict(
            color=marker_bounds,
            colorscale=colorscale,
            cmin=marker_bounds[0],
            cmax=marker_bounds[1],
            colorbar=dict(
                title=dict(text=colorbar_title or "", side="right"),
                thickness=thickness,
                len=len_,
                x=x,
                xanchor="left",
            ),
            showscale=True,
        )

        if (
            self._colorbar_trace_index is not None
            and self._colorbar_trace_index < len(self._fig.data)
        ):
            self._fig.data[self._colorbar_trace_index].marker = marker
        else:
            dummy_trace = go.Scatter(
                x=[None, None],
                y=[None, None],
                mode="markers",
                marker=marker,
                showlegend=False,
                hoverinfo="skip",
            )
            if self._nrows == 1 and self._ncols == 1:
                self._fig.add_trace(dummy_trace)
            else:
                self._fig.add_trace(
                    dummy_trace,
                    row=target_ax._row,
                    col=target_ax._col,
                )
            self._colorbar_trace_index = len(self._fig.data) - 1

        self._colorbar_added = True
        return self

    def colorbar(
        self,
        values=None,
        label=None,
        title=None,
        cmap="Portland",
        ax=None,
        x=None,
        thickness=20,
        len_=None,
        fontsize=None,
        **kwargs,
    ):
        """Add a colorbar for a color plot, or explicitly color a line sweep."""
        target_ax = ax or self._default_ax
        if not isinstance(target_ax, Axes) or target_ax._parent is not self:
            raise ValueError("ax must belong to this QFigure")

        if (
            target_ax._find_color_trace() is not None
            and values is None
            and self._colorbar_values is None
        ):
            target_ax.colorbar(
                title=title or label,
                fontsize=fontsize,
                x=x,
                len_=len_,
                thickness=thickness,
                **kwargs,
            )
            return self

        return self.sweep_colorbar(
            values=values,
            label=label,
            title=title,
            cmap=cmap,
            ax=target_ax,
            x=1.02 if x is None else x,
            thickness=thickness,
            len_=0.7 if len_ is None else len_,
        )

    @property
    def plotly_fig(self):
        """Access the underlying ``plotly.graph_objects.Figure``."""
        return self._fig


# ===========================================================================
#  Module-level convenience functions (matplotlib.pyplot style)
# ===========================================================================

def figure(figsize=None, **kwargs) -> QFigure:
    """Create and return a new :class:`QFigure`."""
    global _current_figure
    _current_figure = QFigure(figsize=figsize, **kwargs)
    return _current_figure


def subplots(nrows=1, ncols=1, figsize=None, subplot_titles=None,
             sharex=False, sharey=False, squeeze=True,
             width_ratios=None, height_ratios=None, **kwargs):
    """Create a figure with a grid of subplots.

    Returns
    -------
    fig : QFigure
    axes : Axes or list of Axes
    """
    if width_ratios is not None:
        kwargs["column_widths"] = width_ratios
    if height_ratios is not None:
        kwargs["row_heights"] = height_ratios
    fig = QFigure(
        nrows=nrows, ncols=ncols, figsize=figsize,
        subplot_titles=subplot_titles,
        sharex=sharex, sharey=sharey,
        **kwargs,
    )
    global _current_figure
    _current_figure = fig
    return fig, fig.axes if squeeze else fig._axes_grid


# ===========================================================================
#  Utility helpers
# ===========================================================================

_NAMED_COLORS = {
    "blue": (0, 0, 255), "green": (0, 128, 0), "red": (255, 0, 0),
    "cyan": (0, 255, 255), "magenta": (255, 0, 255), "yellow": (255, 255, 0),
    "black": (0, 0, 0), "white": (255, 255, 255), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "orange": (255, 165, 0), "purple": (128, 0, 128),
    "brown": (165, 42, 42), "pink": (255, 192, 203),
}


def _rgba(color, alpha: float) -> str:
    """Convert a colour string (hex or named) to an rgba() string."""
    if isinstance(color, (tuple, list, np.ndarray)) and len(color) >= 3:
        rgb = np.asarray(color[:3], dtype=float)
        if np.nanmax(rgb) <= 1:
            rgb = rgb * 255
        r, g, b = (int(round(value)) for value in rgb)
        return f"rgba({r},{g},{b},{alpha})"
    if not isinstance(color, str):
        return f"rgba(128,128,128,{alpha})"
    if color.startswith("#") and len(color) == 7:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return f"rgba({r},{g},{b},{alpha})"
    if color.startswith("#") and len(color) == 4:
        r = int(color[1] * 2, 16)
        g = int(color[2] * 2, 16)
        b = int(color[3] * 2, 16)
        return f"rgba({r},{g},{b},{alpha})"
    if color.startswith("rgb"):
        components = color[color.find("(") + 1:color.find(")")].split(",")
        if len(components) >= 3:
            r, g, b = (component.strip() for component in components[:3])
            return f"rgba({r},{g},{b},{alpha})"
    rgb = _NAMED_COLORS.get(color.lower())
    if rgb:
        return f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})"
    return f"rgba(128,128,128,{alpha})"


# ===========================================================================
#  Quick-access module-level plotting (stateful, pyplot-style)
# ===========================================================================

_current_figure: QFigure | None = None


def gcf() -> QFigure:
    """Get the current figure (create one if needed)."""
    global _current_figure
    if _current_figure is None:
        _current_figure = figure()
    return _current_figure


def gca() -> Axes:
    """Get the current axes."""
    return gcf()._default_ax


def plot(*args, **kwargs):
    return gcf().plot(*args, **kwargs)


def scatter(*args, **kwargs):
    return gcf().scatter(*args, **kwargs)


def bar(*args, **kwargs):
    return gcf().bar(*args, **kwargs)


def hist(*args, **kwargs):
    return gcf().hist(*args, **kwargs)


def xlabel(*args, **kwargs):
    return gcf().xlabel(*args, **kwargs)


def ylabel(*args, **kwargs):
    return gcf().ylabel(*args, **kwargs)


def title(*args, **kwargs):
    return gcf().title(*args, **kwargs)


def xlim(*args, **kwargs):
    return gcf().xlim(*args, **kwargs)


def ylim(*args, **kwargs):
    return gcf().ylim(*args, **kwargs)


def legend(*args, **kwargs):
    return gcf().legend(*args, **kwargs)


def grid(*args, **kwargs):
    return gcf().grid(*args, **kwargs)


def show(**kwargs):
    gcf().show(**kwargs)


def savefig(*args, **kwargs):
    return gcf().savefig(*args, **kwargs)


def close(fig=None):
    global _current_figure
    if fig is None or fig is _current_figure:
        _current_figure = None

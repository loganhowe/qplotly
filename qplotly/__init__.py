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

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


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


# ===========================================================================
#  Axes class — represents a single subplot panel
# ===========================================================================
class Axes:
    """A single axes/subplot, analogous to ``matplotlib.axes.Axes``."""

    def __init__(self, parent_figure: "QFigure", row: int = 1, col: int = 1):
        self._parent = parent_figure
        self._fig: go.Figure = parent_figure._fig
        self._row = row
        self._col = col
        self._color_idx = 0
        self._has_legend_entries = False
        self._legend_traces = []  # Track traces with legend entries for this axes

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

        # Track if this trace used automatic coloring
        if getattr(self, '_next_trace_auto_colored', False):
            self._parent._auto_colored_trace_indices.append(trace_idx)
            self._next_trace_auto_colored = False

        # Track traces with legend entries for per-subplot legends
        if trace.showlegend and trace.name:
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
        # --- positional arg parsing ----------------------------------------
        if len(args) == 1:
            y = np.asarray(args[0])
            x = np.arange(len(y))
        elif len(args) >= 2:
            x = np.asarray(args[0])
            y = np.asarray(args[1])
            if len(args) == 3 and isinstance(args[2], str):
                fmt = args[2]
        else:
            raise TypeError("plot() requires at least 1 positional argument")

        # --- format string -------------------------------------------------
        fmt_color, fmt_marker, fmt_linestyle = (None, None, None)
        if fmt:
            fmt_color, fmt_marker, fmt_linestyle = _parse_fmt(fmt)

        # Track if user specified color (for auto-color scheme)
        user_specified_color = (color is not None or fmt_color is not None)
        self._next_trace_auto_colored = not user_specified_color

        color = color or fmt_color or self._next_color()
        marker = marker or fmt_marker
        linestyle = linestyle or ls or fmt_linestyle or "solid"
        linewidth = _resolve_linewidth(lw, linewidth) or 2
        markersize = markersize or ms or 6

        # --- build mode string ---------------------------------------------
        mode = "lines"
        if marker:
            mode = "lines+markers"

        trace = go.Scatter(
            x=x, y=y, mode=mode, name=label,
            line=dict(color=color, width=linewidth, dash=linestyle),
            marker=dict(symbol=marker, size=markersize, color=color),
            opacity=alpha,
            showlegend=label is not None,
            **kwargs,
        )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def scatter(self, x, y, s=None, c=None, label=None, marker=None,
                alpha=None, cmap=None, colorbar=False, edgecolors=None,
                linewidths=None, **kwargs):
        """Scatter plot."""
        x = np.asarray(x)
        y = np.asarray(y)
        size = s if s is not None else 8

        # Track if user specified color (for auto-color scheme)
        user_specified_color = (c is not None)
        self._next_trace_auto_colored = not user_specified_color

        color = c if c is not None else self._next_color()

        marker_dict = dict(
            size=size,
            color=color,
            symbol=_FMT_MARKERS.get(marker, marker) if marker else "circle",
            opacity=alpha,
        )

        if edgecolors is not None:
            marker_dict["line"] = dict(
                color=edgecolors,
                width=linewidths if linewidths else 1,
            )

        # If color is an array and a colormap is requested
        if isinstance(color, (list, np.ndarray)) and cmap:
            marker_dict["colorscale"] = cmap
            if colorbar:
                marker_dict["colorbar"] = dict(title="")

        trace = go.Scatter(
            x=x, y=y, mode="markers", name=label,
            marker=marker_dict,
            showlegend=label is not None,
            **kwargs,
        )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def bar(self, x, height, width=None, bottom=None, label=None, color=None,
            edgecolor=None, alpha=None, orientation="v", **kwargs):
        """Bar chart."""
        color = color or self._next_color()
        marker_dict = dict(color=color, opacity=alpha)
        if edgecolor:
            marker_dict["line"] = dict(color=edgecolor, width=1)

        if orientation == "v":
            trace = go.Bar(
                x=x, y=height, width=width, base=bottom, name=label,
                marker=marker_dict, showlegend=label is not None, **kwargs,
            )
        else:
            trace = go.Bar(
                y=x, x=height, width=width, base=bottom, name=label,
                marker=marker_dict, orientation="h",
                showlegend=label is not None, **kwargs,
            )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def barh(self, y, width, height=None, left=None, label=None, **kwargs):
        """Horizontal bar chart."""
        return self.bar(y, width, width=height, bottom=left, label=label,
                        orientation="h", **kwargs)

    def hist(self, x, bins=None, range=None, density=False, label=None,
             color=None, alpha=None, edgecolor=None, histtype="bar", **kwargs):
        """Histogram."""
        x = np.asarray(x)
        color = color or self._next_color()
        marker_dict = dict(color=color, opacity=alpha)
        if edgecolor:
            marker_dict["line"] = dict(color=edgecolor, width=1)

        hist_kw = {}
        if bins is not None:
            if isinstance(bins, (int, np.integer)):
                hist_kw["nbinsx"] = int(bins)
            else:
                hist_kw["xbins"] = dict(
                    start=bins[0], end=bins[-1],
                    size=(bins[1] - bins[0]),
                )
        if range is not None:
            hist_kw["xbins"] = hist_kw.get("xbins", {})
            hist_kw["xbins"]["start"] = range[0]
            hist_kw["xbins"]["end"] = range[1]

        histnorm = "probability density" if density else None

        trace = go.Histogram(
            x=x, name=label, marker=marker_dict,
            histnorm=histnorm,
            showlegend=label is not None,
            **hist_kw, **kwargs,
        )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def fill_between(self, x, y1, y2=0, label=None, color=None, alpha=0.3,
                     **kwargs):
        """Filled area between *y1* and *y2*."""
        x = np.asarray(x)
        y1 = np.asarray(y1)
        y2 = np.full_like(y1, y2) if np.ndim(y2) == 0 else np.asarray(y2)
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
            showlegend=label is not None,
            **kwargs,
        ))
        if label:
            self._has_legend_entries = True
        return self

    def errorbar(self, x, y, yerr=None, xerr=None, label=None, color=None,
                 linewidth=None, lw=None, marker=None, markersize=None,
                 ms=None, alpha=None, capsize=None, **kwargs):
        """Line plot with error bars."""
        x = np.asarray(x)
        y = np.asarray(y)
        color = color or self._next_color()
        linewidth = _resolve_linewidth(lw, linewidth) or 2
        markersize = markersize or ms or 6
        mode = "lines+markers" if marker else "lines"

        error_y = None
        error_x = None
        if yerr is not None:
            yerr = np.asarray(yerr)
            if yerr.ndim == 2:
                error_y = dict(type="data", symmetric=False,
                               arrayminus=yerr[0], array=yerr[1], visible=True)
            else:
                error_y = dict(type="data", array=yerr, visible=True)
        if xerr is not None:
            xerr = np.asarray(xerr)
            if xerr.ndim == 2:
                error_x = dict(type="data", symmetric=False,
                               arrayminus=xerr[0], array=xerr[1], visible=True)
            else:
                error_x = dict(type="data", array=xerr, visible=True)

        trace = go.Scatter(
            x=x, y=y, mode=mode, name=label,
            line=dict(color=color, width=linewidth),
            marker=dict(symbol=_FMT_MARKERS.get(marker, marker) if marker else "circle",
                        size=markersize, color=color),
            error_y=error_y, error_x=error_x,
            opacity=alpha,
            showlegend=label is not None,
            **kwargs,
        )
        self._add_trace(trace)
        if label:
            self._has_legend_entries = True
        return self

    def stem(self, x, y, label=None, color=None, **kwargs):
        """Stem plot."""
        x = np.asarray(x)
        y = np.asarray(y)
        color = color or self._next_color()

        for xi, yi in zip(x, y):
            self._add_trace(go.Scatter(
                x=[xi, xi], y=[0, yi], mode="lines",
                line=dict(color=color, width=1), showlegend=False,
            ))
        self._add_trace(go.Scatter(
            x=x, y=y, mode="markers", name=label,
            marker=dict(color=color, size=8),
            showlegend=label is not None,
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
            marker=dict(colors=colors) if colors else None,
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
        trace = go.Heatmap(
            z=data, x=xticklabels, y=yticklabels,
            colorscale=cmap,
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
        contours_kw = {}
        if levels is not None:
            if isinstance(levels, int):
                contours_kw = dict(start=np.min(z), end=np.max(z),
                                   size=(np.max(z) - np.min(z)) / levels)
            else:
                contours_kw = dict(start=levels[0], end=levels[-1],
                                   size=levels[1] - levels[0])
        trace = go.Contour(
            x=np.asarray(x), y=np.asarray(y), z=np.asarray(z),
            contours=contours_kw,
            colorscale=cmap,
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

        # Default to Plasma colormap
        if cmap is None:
            cmap = 'Plasma'

        # Handle 1D x and y arrays (most common case)
        if x.ndim == 1 and y.ndim == 1:
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
        self._fig.add_hline(
            y=y, line_dash=linestyle, line_color=color, line_width=linewidth,
            row=self._row, col=self._col,
            annotation_text=label,
        )
        return self

    def axvline(self, x=0, color="black", linestyle="solid", linewidth=1,
                label=None, **kwargs):
        """Vertical line across the axes."""
        self._fig.add_vline(
            x=x, line_dash=linestyle, line_color=color, line_width=linewidth,
            row=self._row, col=self._col,
            annotation_text=label,
        )
        return self

    def axhspan(self, ymin, ymax, color="gray", alpha=0.3, **kwargs):
        self._fig.add_hrect(
            y0=ymin, y1=ymax, fillcolor=color, opacity=alpha,
            line_width=0, row=self._row, col=self._col,
        )
        return self

    def axvspan(self, xmin, xmax, color="gray", alpha=0.3, **kwargs):
        self._fig.add_vrect(
            x0=xmin, x1=xmax, fillcolor=color, opacity=alpha,
            line_width=0, row=self._row, col=self._col,
        )
        return self

    def text(self, x, y, s, fontsize=12, color="black", ha="left",
             va="bottom", **kwargs):
        """Add text annotation at data coordinates."""
        xanchor = {"left": "left", "center": "center", "right": "right"}.get(ha, "left")
        yanchor = {"top": "top", "center": "middle", "bottom": "bottom"}.get(va, "bottom")
        self._fig.add_annotation(
            x=x, y=y, text=s,
            showarrow=False,
            font=dict(size=fontsize, color=color),
            xanchor=xanchor, yanchor=yanchor,
            xref=self._xref(), yref=self._yref(),
            **kwargs,
        )
        return self

    def annotate(self, text, xy, xytext=None, arrowprops=None, fontsize=12,
                 color="black", **kwargs):
        """Annotate a point with optional arrow."""
        ax_x, ax_y = xy
        show_arrow = xytext is not None
        if xytext is None:
            xytext = xy
        self._fig.add_annotation(
            x=ax_x, y=ax_y,
            ax=xytext[0], ay=xytext[1],
            text=text, showarrow=show_arrow,
            font=dict(size=fontsize, color=color),
            arrowhead=2,
            xref=self._xref(), yref=self._yref(),
            axref=self._xref(), ayref=self._yref(),
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
        font = dict(size=fontsize) if fontsize else None
        self._fig.update_layout(**{
            self._xaxis_name(): dict(title=dict(text=label, font=font))
        })
        return self

    def ylabel(self, label, fontsize=None, **kwargs):
        font = dict(size=fontsize) if fontsize else None
        self._fig.update_layout(**{
            self._yaxis_name(): dict(title=dict(text=label, font=font))
        })
        return self

    def title(self, label, fontsize=None, **kwargs):
        if self._parent._nrows == 1 and self._parent._ncols == 1:
            font = dict(size=fontsize) if fontsize else None
            self._fig.update_layout(title=dict(
                text=label,
                font=font,
                x=0.5,           # Center title
                xanchor='center' # Anchor at center
            ))
        else:
            # Plotly stores subplot titles as annotations. Try to find and
            # update the existing one for this cell before adding a new one.
            idx = self._parent._subplot_index(self._row, self._col)
            xref = self._xref()
            yref = self._yref()
            updated = False
            for ann in self._fig.layout.annotations:
                if getattr(ann, "xref", None) == xref and getattr(ann, "yref", None) == yref:
                    ann.text = label
                    if fontsize:
                        ann.font = dict(size=fontsize)
                    updated = True
                    break
            if not updated:
                self._fig.add_annotation(
                    text=label,
                    xref=xref, yref=yref,
                    x=0.5, y=1.05, xanchor="center", yanchor="bottom",
                    showarrow=False,
                    font=dict(size=fontsize or 14),
                )
        return self

    def xlim(self, *args):
        """Set x-axis limits. ``xlim(lo, hi)`` or ``xlim((lo, hi))``."""
        if len(args) == 1:
            lo, hi = args[0]
        else:
            lo, hi = args
        self._fig.update_layout(**{
            self._xaxis_name(): dict(range=[lo, hi])
        })
        return self

    def ylim(self, *args):
        """Set y-axis limits."""
        if len(args) == 1:
            lo, hi = args[0]
        else:
            lo, hi = args
        self._fig.update_layout(**{
            self._yaxis_name(): dict(range=[lo, hi])
        })
        return self

    def xscale(self, scale):
        """Set x-axis scale: 'linear' or 'log'."""
        scale_type = "log" if scale == "log" else "linear"
        self._fig.update_layout(**{
            self._xaxis_name(): dict(type=scale_type)
        })
        return self

    def yscale(self, scale):
        """Set y-axis scale: 'linear' or 'log'."""
        scale_type = "log" if scale == "log" else "linear"
        self._fig.update_layout(**{
            self._yaxis_name(): dict(type=scale_type)
        })
        return self

    def xticks(self, ticks=None, labels=None, rotation=None, fontsize=None):
        update = {}
        if ticks is not None:
            update["tickvals"] = ticks
        if labels is not None:
            update["ticktext"] = labels
        if rotation is not None:
            update["tickangle"] = -rotation
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
            update["tickangle"] = -rotation
        if fontsize is not None:
            update["tickfont"] = dict(size=fontsize)
        self._fig.update_layout(**{self._yaxis_name(): update})
        return self

    def grid(self, visible=True, which="major", axis="both", **kwargs):
        """Toggle grid lines."""
        show = visible
        if axis in ("both", "x"):
            self._fig.update_layout(**{
                self._xaxis_name(): dict(showgrid=show)
            })
        if axis in ("both", "y"):
            self._fig.update_layout(**{
                self._yaxis_name(): dict(showgrid=show)
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

        # Default matplotlib-like styling: opaque white box with black border
        legend_kw = dict(
            visible=config['show'],
            bgcolor=config['facecolor'] or 'white',
            bordercolor=config['edgecolor'] or 'black',
            borderwidth=1 if config['frameon'] else 0,
        )

        # Note: fancybox (rounded corners) not supported by Plotly legends
        # Kept for matplotlib API compatibility but has no visual effect

        if config['fontsize']:
            legend_kw["font"] = dict(size=config['fontsize'])

        # Handle transparency
        if config['framealpha'] is not None:
            try:
                import matplotlib.colors as mcolors
                bg_color = config['facecolor'] or 'white'
                rgba = mcolors.to_rgba(bg_color, alpha=config['framealpha'])
                legend_kw["bgcolor"] = f"rgba({int(rgba[0]*255)},{int(rgba[1]*255)},{int(rgba[2]*255)},{rgba[3]})"
            except (ImportError, ValueError):
                pass

        # Matplotlib-compatible location names
        _loc_map = {
            "best":          dict(x=0.98, y=0.98, xanchor="right", yanchor="top"),
            "upper right":   dict(x=0.98, y=0.98, xanchor="right", yanchor="top"),
            "upper left":    dict(x=0.02, y=0.98, xanchor="left",  yanchor="top"),
            "lower left":    dict(x=0.02, y=0.02, xanchor="left",  yanchor="bottom"),
            "lower right":   dict(x=0.98, y=0.02, xanchor="right", yanchor="bottom"),
            "right":         dict(x=0.98, y=0.5,  xanchor="right", yanchor="middle"),
            "center left":   dict(x=0.02, y=0.5,  xanchor="left",  yanchor="middle"),
            "center right":  dict(x=0.98, y=0.5,  xanchor="right", yanchor="middle"),
            "lower center":  dict(x=0.5,  y=0.02, xanchor="center", yanchor="bottom"),
            "upper center":  dict(x=0.5,  y=0.98, xanchor="center", yanchor="top"),
            "center":        dict(x=0.5,  y=0.5,  xanchor="center", yanchor="middle"),
        }

        if config['loc'] in _loc_map:
            legend_kw.update(_loc_map[config['loc']])

        legend_kw.update(config['kwargs'])
        self._fig.update_layout(legend=legend_kw)
        return self

    def invert_xaxis(self):
        self._fig.update_layout(**{self._xaxis_name(): dict(autorange="reversed")})
        return self

    def invert_yaxis(self):
        self._fig.update_layout(**{self._yaxis_name(): dict(autorange="reversed")})
        return self

    def set_aspect(self, aspect):
        """Rough aspect-ratio control."""
        if aspect == "equal":
            self._fig.update_layout(**{
                self._yaxis_name(): dict(scaleanchor=self._xref(),
                                         scaleratio=1)
            })
        return self

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
        # Enable a secondary y-axis in the layout
        self._fig.update_layout(
            **{
                "yaxis2": dict(
                    overlaying="y",
                    side="right",
                    showgrid=False,
                )
            }
        )

    def _add_trace(self, trace):
        trace.yaxis = "y2"
        self._fig.add_trace(trace)

    def ylabel(self, label, fontsize=None, **kwargs):
        font = dict(size=fontsize) if fontsize else None
        self._fig.update_layout(yaxis2=dict(title=dict(text=label, font=font)))
        return self


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
        self._nrows = nrows
        self._ncols = ncols

        if fig is not None:
            self._fig = fig
        elif nrows == 1 and ncols == 1:
            self._fig = go.Figure()
        else:
            shared_x = "all" if sharex else None
            shared_y = "all" if sharey else None
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
        self._auto_colored_trace_indices = []

        # Default single axes
        self._default_ax = Axes(self, 1, 1)

        # Build axes grid
        self._axes_grid = [
            [Axes(self, r + 1, c + 1) for c in range(ncols)]
            for r in range(nrows)
        ]

    # ---- default styling --------------------------------------------------
    def _apply_default_style(self):
        """Apply matplotlib-like default styling."""
        # Default layout settings
        layout_updates = dict(
            plot_bgcolor='white',      # White background for plot area
            paper_bgcolor='white',     # White background for entire figure
            font=dict(
                family='Computer Modern, CMU Serif, serif',  # CMR10-like font
                size=12,
                color='black'
            ),
        )

        # Apply to all xaxis and yaxis
        for i in range(1, self._nrows * self._ncols + 1):
            xaxis_name = f"xaxis{i}" if i > 1 else "xaxis"
            yaxis_name = f"yaxis{i}" if i > 1 else "yaxis"

            axis_style = dict(
                showline=True,           # Show axis border (frame)
                linewidth=2,             # Thicker frame line (like matplotlib)
                linecolor='black',
                mirror=True,             # Show frame on all sides
                showgrid=True,           # Show grid
                gridwidth=0.5,           # Thinner grid lines than frame
                gridcolor='rgba(0, 0, 0, 0.5)',  # Black with 50% opacity
                zeroline=False,          # Don't emphasize zero line
                ticks='outside',         # Ticks extend outside plot frame
                ticklen=5,               # Length of tick marks
                tickwidth=1.5,           # Tick thickness
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
        return getattr(self._default_ax, name)

    # ---- figure-level methods ---------------------------------------------

    def suptitle(self, title, fontsize=None, **kwargs):
        font = dict(size=fontsize) if fontsize else None
        self._fig.update_layout(title=dict(text=title, font=font))
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
        """Apply smart color scheme based on number of auto-colored traces.

        Color scheme:
        - 2 traces: blue, black
        - 3-4 traces: blue, red, green, black
        - >4 traces: nipy_spectral colormap with evenly spaced colors
        """
        if not self._auto_colored_trace_indices:
            return

        n_auto = len(self._auto_colored_trace_indices)

        # Determine color scheme based on count
        if n_auto == 2:
            colors = ['blue', 'black']
        elif n_auto in (3, 4):
            colors = ['blue', 'red', 'green', 'black'][:n_auto]
        else:  # > 4
            # Use nipy_spectral colormap with evenly spaced colors
            try:
                import matplotlib.cm as cm
                import matplotlib.colors as mcolors
                cmap = cm.get_cmap('nipy_spectral')
                colors = []
                for i in range(n_auto):
                    t = i / (n_auto - 1) if n_auto > 1 else 0
                    rgba = cmap(t)
                    hex_color = mcolors.rgb2hex(rgba[:3])
                    colors.append(hex_color)
            except (ImportError, ValueError):
                # Fallback to default colors if matplotlib not available
                colors = DEFAULT_COLORS * (n_auto // len(DEFAULT_COLORS) + 1)
                colors = colors[:n_auto]

        # Apply colors to auto-colored traces
        for i, trace_idx in enumerate(self._auto_colored_trace_indices):
            if trace_idx >= len(self._fig.data):
                continue

            trace = self._fig.data[trace_idx]
            color = colors[i]

            # Update trace color based on trace type
            # Plotly traces have line and/or marker attributes
            if hasattr(trace, 'line') and trace.line:
                try:
                    trace.line.color = color
                except (AttributeError, TypeError):
                    pass
            if hasattr(trace, 'marker') and trace.marker:
                try:
                    trace.marker.color = color
                except (AttributeError, TypeError):
                    pass

    # ---- subplot legends --------------------------------------------------

    def _apply_subplot_legends(self):
        """Apply per-subplot legends (matplotlib-style)."""
        if self._nrows == 1 and self._ncols == 1:
            return  # Single plot uses standard legend

        # Hide the global Plotly legend for subplots
        self._fig.update_layout(showlegend=False)

        # For each subplot, create a custom legend box
        for row_axes in self._axes_grid:
            for ax in (row_axes if isinstance(row_axes, list) else [row_axes]):
                if not hasattr(ax, '_legend_config') or not ax._has_legend_entries:
                    continue

                config = ax._legend_config
                if not config['show']:
                    continue

                # Get subplot domain
                subplot_idx = self._subplot_index(ax._row, ax._col)
                xaxis_name = f"xaxis{subplot_idx}" if subplot_idx > 1 else "xaxis"
                yaxis_name = f"yaxis{subplot_idx}" if subplot_idx > 1 else "yaxis"

                xaxis = self._fig.layout[xaxis_name]
                yaxis = self._fig.layout[yaxis_name]

                # Get domain (normalized coordinates)
                xdomain = xaxis.domain if xaxis.domain else [0, 1]
                ydomain = yaxis.domain if yaxis.domain else [0, 1]

                # Calculate legend position within subplot
                loc = config['loc']
                loc_coords = {
                    "upper right":   (0.98, 0.98, "right", "top"),
                    "upper left":    (0.02, 0.98, "left", "top"),
                    "lower left":    (0.02, 0.02, "left", "bottom"),
                    "lower right":   (0.98, 0.02, "right", "bottom"),
                    "right":         (0.98, 0.5, "right", "middle"),
                    "center left":   (0.02, 0.5, "left", "middle"),
                    "center right":  (0.98, 0.5, "right", "middle"),
                    "lower center":  (0.5, 0.02, "center", "bottom"),
                    "upper center":  (0.5, 0.98, "center", "top"),
                    "center":        (0.5, 0.5, "center", "middle"),
                    "best":          (0.98, 0.98, "right", "top"),
                }.get(loc, (0.98, 0.98, "right", "top"))

                x_frac, y_frac, xanchor, yanchor = loc_coords

                # Convert to paper coordinates
                x_paper = xdomain[0] + (xdomain[1] - xdomain[0]) * x_frac
                y_paper = ydomain[0] + (ydomain[1] - ydomain[0]) * y_frac

                # Get traces for this subplot
                legend_items = []
                for trace_idx in ax._legend_traces:
                    if trace_idx < len(self._fig.data):
                        trace = self._fig.data[trace_idx]
                        if trace.showlegend and trace.name:
                            color = 'black'
                            if hasattr(trace, 'line') and trace.line and hasattr(trace.line, 'color'):
                                color = trace.line.color
                            elif hasattr(trace, 'marker') and trace.marker and hasattr(trace.marker, 'color'):
                                color = trace.marker.color or 'black'
                            legend_items.append((trace.name, color))

                if not legend_items:
                    continue

                # Create legend annotation with rounded rectangle
                self._create_legend_annotation(
                    legend_items, x_paper, y_paper, xanchor, yanchor, config
                )

    def _create_legend_annotation(self, items, x, y, xanchor, yanchor, config):
        """Create a legend annotation with rounded rectangle background."""
        fontsize = config['fontsize'] or 12
        facecolor = config['facecolor'] or 'white'
        edgecolor = config['edgecolor'] or 'black'
        frameon = config['frameon']
        fancybox = config['fancybox']
        framealpha = config['framealpha'] if config['framealpha'] is not None else 1.0

        # Build legend text
        legend_text = "<br>".join([f"<span style='color:{color}'>\u25A0</span> {name}"
                                   for name, color in items])

        # Add annotation for text
        self._fig.add_annotation(
            x=x, y=y,
            xref="paper", yref="paper",
            text=legend_text,
            showarrow=False,
            xanchor=xanchor,
            yanchor=yanchor,
            font=dict(size=fontsize),
            bgcolor=f"rgba(255,255,255,{framealpha})" if facecolor == 'white' else facecolor,
            bordercolor=edgecolor if frameon else "rgba(0,0,0,0)",
            borderwidth=1 if frameon else 0,
            borderpad=6,
        )

    # ---- display / export -------------------------------------------------

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
        self._apply_auto_color_scheme()
        self._apply_subplot_legends()
        if tight_layout:
            self._apply_tight_layout()
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
        self._apply_auto_color_scheme()
        self._apply_subplot_legends()
        if tight_layout:
            self._apply_tight_layout()
        if filename.endswith(".html"):
            self._fig.write_html(filename, **kwargs)
        elif filename.endswith(".json"):
            self._fig.write_json(filename, **kwargs)
        else:
            self._fig.write_image(filename, width=width, height=height,
                                  scale=scale, **kwargs)
        return self

    def to_html(self, **kwargs):
        return self._fig.to_html(**kwargs)

    def to_json(self, **kwargs):
        return self._fig.to_json(**kwargs)

    @property
    def plotly_fig(self):
        """Access the underlying ``plotly.graph_objects.Figure``."""
        return self._fig


# ===========================================================================
#  Module-level convenience functions (matplotlib.pyplot style)
# ===========================================================================

def figure(figsize=None, **kwargs) -> QFigure:
    """Create and return a new :class:`QFigure`."""
    return QFigure(figsize=figsize, **kwargs)


def subplots(nrows=1, ncols=1, figsize=None, subplot_titles=None,
             sharex=False, sharey=False, **kwargs):
    """Create a figure with a grid of subplots.

    Returns
    -------
    fig : QFigure
    axes : Axes or list of Axes
    """
    fig = QFigure(
        nrows=nrows, ncols=ncols, figsize=figsize,
        subplot_titles=subplot_titles,
        sharex=sharex, sharey=sharey,
        **kwargs,
    )
    return fig, fig.axes


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


def _rgba(color: str, alpha: float) -> str:
    """Convert a colour string (hex or named) to an rgba() string."""
    if color.startswith("#") and len(color) == 7:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return f"rgba({r},{g},{b},{alpha})"
    if color.startswith("rgba") or color.startswith("rgb"):
        return color
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
    global _current_figure
    _current_figure = None  # reset after show, like plt.show()


def savefig(*args, **kwargs):
    return gcf().savefig(*args, **kwargs)


def close():
    global _current_figure
    _current_figure = None

import unittest

import numpy as np

import qplotly as ply


class PlottingTests(unittest.TestCase):
    def tearDown(self):
        ply.close()

    def test_plot_format_string_and_multiple_groups(self):
        fig = ply.figure()

        fig.plot(
            [0, 1],
            [1, 2],
            "ro--",
            [0, 1],
            [2, 1],
            "g:",
        )

        first, second = fig.plotly_fig.data
        self.assertEqual(first.mode, "lines+markers")
        self.assertEqual(first.line.color, "red")
        self.assertEqual(first.line.dash, "dash")
        self.assertEqual(first.marker.symbol, "circle")
        self.assertEqual(second.line.color, "green")
        self.assertEqual(second.line.dash, "dot")

    def test_marker_only_format_does_not_draw_a_line(self):
        fig = ply.figure()

        fig.plot([0, 1], [1, 2], "o")

        self.assertEqual(fig.plotly_fig.data[0].mode, "markers")

    def test_plot_aliases_and_nested_plotly_options(self):
        fig = ply.figure()

        fig.plot(
            [0, 1],
            [1, 2],
            c="purple",
            lw=3,
            ls="-.",
            marker="s",
            ms=8,
            marker_options={"opacity": 0.5},
        )

        trace = fig.plotly_fig.data[0]
        self.assertEqual(trace.line.color, "purple")
        self.assertEqual(trace.line.width, 3)
        self.assertEqual(trace.line.dash, "dashdot")
        self.assertEqual(trace.marker.symbol, "square")
        self.assertEqual(trace.marker.size, 8)
        self.assertEqual(trace.marker.opacity, 0.5)

    def test_scatter_uses_matplotlib_area_sizes_and_colorbar(self):
        fig = ply.figure()

        fig.scatter(
            [0, 1],
            [1, 2],
            s=[25, 100],
            c=[0, 1],
            cmap="Portland",
            colorbar=True,
        )

        marker = fig.plotly_fig.data[0].marker
        np.testing.assert_allclose(marker.size, [5, 10])
        self.assertTrue(marker.showscale)
        self.assertIsNotNone(marker.colorscale)

    def test_barh_maps_height_and_left(self):
        fig = ply.figure()

        fig.barh(["a", "b"], [2, 3], height=0.5, left=1)

        trace = fig.plotly_fig.data[0]
        self.assertEqual(trace.orientation, "h")
        self.assertEqual(tuple(trace.y), ("a", "b"))
        self.assertEqual(tuple(trace.x), (2, 3))
        self.assertEqual(trace.width, 0.5)
        self.assertEqual(trace.base, 1)

    def test_errorbar_maps_asymmetric_errors_and_caps(self):
        fig = ply.figure()

        fig.errorbar(
            [0, 1],
            [1, 2],
            yerr=[[0.1, 0.2], [0.3, 0.4]],
            fmt="o",
            capsize=4,
        )

        trace = fig.plotly_fig.data[0]
        self.assertEqual(trace.mode, "markers")
        self.assertFalse(trace.error_y.symmetric)
        self.assertEqual(tuple(trace.error_y.arrayminus), (0.1, 0.2))
        self.assertEqual(tuple(trace.error_y.array), (0.3, 0.4))
        self.assertEqual(trace.error_y.width, 4)

    def test_labels_require_legend_call(self):
        fig = ply.figure()
        fig.plot([0, 1], [1, 2], label="data")

        self.assertFalse(fig.plotly_fig.data[0].showlegend)
        fig.legend()
        self.assertTrue(fig.plotly_fig.data[0].showlegend)

    def test_common_annotation_and_reference_line_kwargs(self):
        fig = ply.figure()

        fig.axhline(1, alpha=0.5)
        fig.text(1, 1, "point", rotation=45, fontweight="bold")
        fig.annotate(
            "peak",
            (1, 1),
            (2, 2),
            arrowprops={"facecolor": "black", "shrink": 0.05},
        )

        self.assertEqual(fig.plotly_fig.layout.shapes[0].opacity, 0.5)
        self.assertEqual(fig.plotly_fig.layout.annotations[0].textangle, 45)
        self.assertEqual(
            fig.plotly_fig.layout.annotations[1].arrowcolor, "black"
        )

    def test_nonuniform_histogram_bins_are_respected(self):
        fig = ply.figure()

        fig.hist([0.1, 0.2, 1.5, 3.5], bins=[0, 1, 2, 4])

        trace = fig.plotly_fig.data[0]
        self.assertEqual(trace.type, "bar")
        self.assertEqual(tuple(trace.width), (1, 1, 2))


if __name__ == "__main__":
    unittest.main()

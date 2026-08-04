import unittest

import numpy as np
import plotly.io as pio

import qplotly as ply


class FigureApiTests(unittest.TestCase):
    def tearDown(self):
        ply.close()

    def test_import_sets_notebook_renderer(self):
        self.assertEqual(pio.renderers.default, "notebook")

    def test_default_axes_is_canonical_and_delegation_stays_on_figure(self):
        fig = ply.figure()

        self.assertIs(fig.axes, fig._axes_grid[0][0])
        self.assertIs(fig.plot([0, 1], [1, 2]), fig)
        self.assertIs(fig.xlabel("x").ylabel("y").title("title"), fig)

    def test_figure_tracks_pyplot_current_figure(self):
        fig = ply.figure()

        self.assertIs(ply.gcf(), fig)
        self.assertIs(ply.gca(), fig.axes)

    def test_subplots_tracks_current_figure_and_axes_shapes(self):
        fig, axes = ply.subplots(2, 1)

        self.assertIs(ply.gcf(), fig)
        self.assertEqual(len(axes), 2)
        self.assertIs(fig.gca(2, 1), axes[1])
        with self.assertRaises(IndexError):
            fig.gca(3, 1)

    def test_subplots_support_share_aliases_and_squeeze_false(self):
        fig, axes = ply.subplots(1, 2, sharex="col", squeeze=False)

        self.assertEqual(len(axes), 1)
        self.assertEqual(len(axes[0]), 2)
        self.assertIs(axes[0][1], fig.gca(1, 2))

    def test_matplotlib_setters_and_limit_getters(self):
        fig = ply.figure()

        result = (
            fig.set_xlabel("frequency")
            .set_ylabel("gain")
            .set_xlim(1, 9)
            .set_ylim((-2, 20))
        )

        self.assertIs(result, fig)
        self.assertEqual(fig.get_xlim(), (1, 9))
        self.assertEqual(fig.get_ylim(), (-2, 20))
        self.assertEqual(fig.plotly_fig.layout.xaxis.title.text, "frequency")
        self.assertEqual(fig.plotly_fig.layout.yaxis.title.text, "gain")

    def test_invalid_scale_is_not_silently_linear(self):
        fig = ply.figure()

        with self.assertRaises(NotImplementedError):
            fig.xscale("symlog")

    def test_colors_are_assigned_at_plot_time(self):
        fig = ply.figure()
        fig.plot([0, 1], [0, 1])
        original = fig.plotly_fig.data[0].line.color

        fig._apply_auto_color_scheme()

        self.assertEqual(original, ply.DEFAULT_COLORS[0])
        self.assertEqual(fig.plotly_fig.data[0].line.color, original)

    def test_two_dimensional_y_creates_one_trace_per_column(self):
        fig = ply.figure()
        y = np.array([[0, 10], [1, 11], [2, 12]])

        fig.plot([0, 1, 2], y, label=["low", "high"])

        self.assertEqual(len(fig.plotly_fig.data), 2)
        self.assertEqual(fig.plotly_fig.data[0].name, "low")
        self.assertEqual(fig.plotly_fig.data[1].name, "high")

    def test_scalar_plot_input_is_promoted_to_one_point(self):
        fig = ply.figure()

        fig.plot(3)

        self.assertEqual(tuple(fig.plotly_fig.data[0].x), (0,))
        self.assertEqual(tuple(fig.plotly_fig.data[0].y), (3,))


if __name__ == "__main__":
    unittest.main()

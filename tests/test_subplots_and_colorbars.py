import unittest

import numpy as np

import qplotly as ply


class SubplotAndColorbarTests(unittest.TestCase):
    def tearDown(self):
        ply.close()

    def test_subplot_titles_update_in_place(self):
        fig, axes = ply.subplots(1, 2, subplot_titles=("left", "right"))
        annotation_count = len(fig.plotly_fig.layout.annotations)

        axes[1].title("updated")

        self.assertEqual(len(fig.plotly_fig.layout.annotations), annotation_count)
        self.assertEqual(fig._subplot_title_annotations[2].text, "updated")

    def test_subplot_legends_are_native_and_idempotent(self):
        fig, axes = ply.subplots(1, 2)
        axes[0].plot([0, 1], [0, 1], label="line")
        axes[1].scatter([0, 1], [1, 0], label="points")
        axes[0].legend()
        axes[1].legend(loc="lower left")
        annotation_count = len(fig.plotly_fig.layout.annotations)

        fig._apply_subplot_legends()
        fig._apply_subplot_legends()

        self.assertEqual(
            len(fig.plotly_fig.layout.annotations), annotation_count
        )
        self.assertEqual(fig.plotly_fig.data[0].legend, "legend")
        self.assertEqual(fig.plotly_fig.data[1].legend, "legend2")
        self.assertTrue(fig.plotly_fig.layout.legend2.visible)

    def test_twin_axes_are_unique_per_subplot(self):
        fig, axes = ply.subplots(1, 2)
        left_twin = axes[0].twinx()
        right_twin = axes[1].twinx()

        left_twin.plot([0, 1], [10, 20]).set_ylabel("left secondary")
        right_twin.plot([0, 1], [30, 40])

        left_trace, right_trace = fig.plotly_fig.data
        self.assertEqual(left_trace.xaxis, "x")
        self.assertEqual(left_trace.yaxis, "y3")
        self.assertEqual(right_trace.xaxis, "x2")
        self.assertEqual(right_trace.yaxis, "y4")
        self.assertEqual(
            fig.plotly_fig.layout.yaxis3.title.text, "left secondary"
        )

    def test_single_figure_colorbar_targets_heatmap(self):
        fig = ply.figure()
        fig.pcolormesh(
            [1, 2],
            [3, 4],
            [[1, 2], [3, 4]],
            cmap="Portland",
        )

        result = fig.colorbar(title="Gain [dB]")

        self.assertIs(result, fig)
        self.assertEqual(
            fig.plotly_fig.data[0].colorbar.title.text, "Gain [dB]"
        )

    def test_subplot_colorbar_targets_requested_axes(self):
        fig, axes = ply.subplots(1, 2)
        axes[0].pcolormesh([0, 1], [0, 1], [[0, 1], [2, 3]])
        axes[1].pcolormesh([0, 1], [0, 1], [[4, 5], [6, 7]])

        axes[1].colorbar(title="right")

        self.assertIsNone(fig.plotly_fig.data[0].colorbar.title.text)
        self.assertEqual(fig.plotly_fig.data[1].colorbar.title.text, "right")

    def test_sweep_colorbar_is_explicit_and_idempotent(self):
        fig = ply.figure()
        for value in range(5):
            fig.plot([0, 1], [value, value + 1])

        fig.sweep_colorbar(np.arange(5), label="bias", cmap="Portland")
        trace_count = len(fig.plotly_fig.data)
        colors = [trace.line.color for trace in fig.plotly_fig.data[:-1]]
        fig.sweep_colorbar(np.arange(5), label="bias", cmap="Portland")

        self.assertEqual(len(fig.plotly_fig.data), trace_count)
        self.assertEqual(
            fig.plotly_fig.data[-1].marker.colorbar.title.text, "bias"
        )
        self.assertEqual(len(set(colors)), 5)


if __name__ == "__main__":
    unittest.main()

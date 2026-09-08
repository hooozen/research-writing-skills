"""Rendered geometry regressions for headers, cards and plot decorations."""
import importlib.util
import io
import os
from pathlib import Path
import unittest

os.environ.setdefault('MPLBACKEND', 'Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/clinical-data-chart-style/scripts/matplotlib_example.py'
spec = importlib.util.spec_from_file_location('card_style', SCRIPT)
style = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style)


class CardLayoutTests(unittest.TestCase):
    def scene(self, size=(8, 3.1), dpi=100):
        style.configure_typography(100)
        fig, ax = plt.subplots(figsize=size, dpi=dpi)
        self.addCleanup(plt.close, fig)
        card = FancyBboxPatch((.012, .025), .976, .95,
                             boxstyle='round,pad=0,rounding_size=.025',
                             transform=fig.transFigure, facecolor=style.VI['card'],
                             edgecolor='none', zorder=-10)
        fig.add_artist(card)
        ax.set_facecolor('none')
        ax.plot([0, 1, 2], [12, 18, 20])
        fig.subplots_adjust(left=.13, right=.94, top=.79, bottom=.18)
        return fig, ax, card

    def assert_contained(self, fig, card, header):
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        bounds = card.get_window_extent(renderer)
        texts = [text.get_window_extent(renderer) for text in header if text is not None]
        for box in texts:
            self.assertGreaterEqual(box.x0, bounds.x0 + 10 * fig.dpi / 72)
            self.assertLessEqual(box.x1, bounds.x1 - 10 * fig.dpi / 72)
            self.assertGreaterEqual(box.y0, bounds.y0)
            self.assertLessEqual(box.y1, bounds.y1 - 10 * fig.dpi / 72)
        if len(texts) > 1:
            self.assertGreater(texts[0].y0, texts[1].y1)
        for ax in fig.axes:
            self.assertGreaterEqual(min(box.y0 for box in texts) - ax.get_tightbbox(renderer).y1,
                                    10 * fig.dpi / 72)

    def test_multiline_header_stays_inside_at_multiple_sizes_and_dpi(self):
        for size, dpi in (((8, 3.1), 100), ((4.8, 2.8), 180)):
            with self.subTest(size=size, dpi=dpi):
                fig, ax, card = self.scene(size, dpi)
                initial_plot_height = ax.get_position().height * fig.bbox.height
                header = style.layout_card_header(
                    fig, ax, card, 'Repeated measurements across visits\nSignal distribution in the demonstration cohort',
                    subtitle='Synthetic observations; available participants at each visit')
                self.assert_contained(fig, card, header)
                self.assertGreaterEqual(ax.bbox.height, initial_plot_height - .1)
                for fmt in ('png', 'svg'):
                    fig.savefig(io.BytesIO(), format=fmt, bbox_inches='tight', dpi=dpi)
                    self.assert_contained(fig, card, header)

    def test_long_unspaced_header_wraps_without_losing_text(self):
        fig, ax, card = self.scene((4.8, 4.2))
        original = 'UnspacedMeasurementIdentifier' * 4
        header = style.layout_card_header(fig, ax, card, original)
        self.assertIn('\n', header[0].get_text())
        self.assertEqual(header[0].get_text().replace('\n', ''), original)
        self.assert_contained(fig, card, header)

    def test_heatmap_header_reserves_colorbar_decorations(self):
        fig, ax, card = self.scene((6.5, 3.4))
        im = ax.imshow([[1, 2], [3, 4]], aspect='auto')
        bar = fig.colorbar(im, ax=ax)
        bar.set_label('Mean absolute error (μm)')
        header = style.layout_card_header(fig, ax, card,
                                         'Errors across methods\nAnd datasets',
                                         subtitle='Synthetic values', plot_axes=fig.axes)
        self.assert_contained(fig, card, header)
        self.assertAlmostEqual(ax.get_position().y0, bar.ax.get_position().y0)
        self.assertAlmostEqual(ax.get_position().y1, bar.ax.get_position().y1)

    def test_relayout_after_resize_replaces_header_and_preserves_font(self):
        fig, ax, card = self.scene()
        title = 'Signal distribution in the demonstration cohort across repeated visits'
        first = style.layout_card_header(fig, ax, card, title)
        size = first[0].get_fontsize()
        fig.set_size_inches(4.8, 3)
        second = style.layout_card_header(fig, ax, card, title)
        self.assertNotIn(first[0], fig.texts)
        self.assertEqual(second[0].get_fontsize(), size)
        self.assert_contained(fig, card, second)

    def test_fixed_small_canvas_reports_insufficient_space(self):
        fig, ax, card = self.scene((5, 2))
        with self.assertRaisesRegex(ValueError, 'increase figure height'):
            style.layout_card_header(fig, ax, card, 'First line\nSecond line\nThird line', grow_height=False)

    def test_active_layout_engine_cannot_silently_move_axes_later(self):
        fig, ax, card = self.scene()
        fig.set_layout_engine('constrained')
        with self.assertRaisesRegex(ValueError, 'disable its engine'):
            style.layout_card_header(fig, ax, card, 'Title')
        fig.canvas.draw()
        fig.set_layout_engine('none')
        header = style.layout_card_header(fig, ax, card, 'Title')
        self.assert_contained(fig, card, header)


if __name__ == '__main__':
    unittest.main()

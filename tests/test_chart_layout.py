"""Physical geometry regressions for scientific figure headers and colorbars."""
import importlib.util
import io
import os
from pathlib import Path
import unittest

os.environ.setdefault('MPLBACKEND', 'Agg')
import matplotlib.pyplot as plt

SCRIPT = Path(__file__).resolve().parents[1]/'skills/scientific-chart-style/scripts/matplotlib_example.py'
spec = importlib.util.spec_from_file_location('scientific_style', SCRIPT)
style = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style)

class PublicationLayoutTests(unittest.TestCase):
    def scene(self, width=89, height=65, dpi=100):
        style.configure_typography(dpi)
        fig, ax = plt.subplots(figsize=(width/25.4,height/25.4),dpi=dpi)
        self.addCleanup(plt.close,fig)
        ax.plot([0,1,2],[12,18,20])
        style.style_axes(ax)
        fig.subplots_adjust(left=.2,right=.9,top=.78,bottom=.2)
        return fig,ax

    def assert_contained(self, fig, header):
        fig.canvas.draw()
        renderer=fig.canvas.get_renderer()
        boxes=[t.get_window_extent(renderer) for t in header if t is not None]
        for b in boxes:
            self.assertGreaterEqual(b.x0,0)
            self.assertLessEqual(b.x1,fig.bbox.width)
            self.assertGreaterEqual(b.y0,0)
            self.assertLessEqual(b.y1,fig.bbox.height)
        if len(boxes)>1:
            self.assertGreater(boxes[0].y0,boxes[1].y1)
        for ax in fig.axes:
            self.assertGreaterEqual(min(b.y0 for b in boxes)-ax.get_tightbbox(renderer).y1,
                                    3.5*fig.dpi/72)

    def test_header_survives_single_double_column_and_export(self):
        for width,dpi in [(89,100),(180,300)]:
            fig,ax=self.scene(width=width,dpi=dpi)
            initial_height=ax.bbox.height*72/dpi
            h=style.layout_figure_header(fig,ax,'Repeated measurements across visits\nA long synthetic scientific title',
                                        subtitle='Synthetic observations; available samples at each time')
            self.assert_contained(fig,h)
            self.assertGreaterEqual(ax.bbox.height*72/dpi,initial_height-.1)
            self.assertEqual(fig.get_figwidth(),width/25.4)
            self.assertEqual(h[0].get_fontsize(),7)
            for fmt in ['png','svg','pdf']:
                fig.savefig(io.BytesIO(),format=fmt,dpi=dpi)
                self.assert_contained(fig,h)

    def test_long_unspaced_header_keeps_content(self):
        fig,ax=self.scene()
        title='UnspacedMeasurementIdentifier'*4
        h=style.layout_figure_header(fig,ax,title)
        self.assertEqual(h[0].get_text().replace('\n',''),title)
        self.assertIn('\n',h[0].get_text())
        self.assert_contained(fig,h)

    def test_colorbar_is_aligned_and_reserved(self):
        fig,ax=self.scene(width=120)
        im=ax.imshow([[1,2],[3,4]],aspect='auto')
        bar=fig.colorbar(im,ax=ax)
        bar.set_label('Mean absolute error (a.u.)')
        h=style.layout_figure_header(fig,ax,'Errors across methods\nAnd datasets',
                                    subtitle='Synthetic values',plot_axes=fig.axes)
        self.assert_contained(fig,h)
        self.assertAlmostEqual(ax.get_position().y0,bar.ax.get_position().y0)
        self.assertAlmostEqual(ax.get_position().y1,bar.ax.get_position().y1)

    def test_resize_replaces_header_without_shrinking_font(self):
        fig,ax=self.scene(width=180)
        title='Signal distribution across repeated observations and long condition names'
        first=style.layout_figure_header(fig,ax,title)
        fig.set_size_inches(89/25.4,65/25.4)
        second=style.layout_figure_header(fig,ax,title)
        self.assertNotIn(first[0],fig.texts)
        self.assertEqual(second[0].get_fontsize(),first[0].get_fontsize())
        self.assert_contained(fig,second)

    def test_fixed_canvas_reports_insufficient_space(self):
        fig,ax=self.scene(height=25)
        with self.assertRaisesRegex(ValueError,'increase figure height'):
            style.layout_figure_header(fig,ax,'First line\nSecond line\nThird line\nFourth line',grow_height=False)

    def test_conflicting_layout_engine_must_be_resolved(self):
        fig,ax=self.scene()
        fig.set_layout_engine('constrained')
        with self.assertRaisesRegex(ValueError,'disable its engine'):
            style.layout_figure_header(fig,ax,'Title')
        fig.canvas.draw()
        fig.set_layout_engine('none')
        h=style.layout_figure_header(fig,ax,'Title')
        self.assert_contained(fig,h)

if __name__=='__main__':
    unittest.main()

"""Scientific invariants and real exports for the optional chart gallery."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

os.environ.setdefault('MPLBACKEND', 'Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/clinical-data-chart-style/scripts/scientific_chart_gallery.py'
spec = importlib.util.spec_from_file_location('scientific_gallery', SCRIPT)
gallery = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(SCRIPT.parent))
try:
    spec.loader.exec_module(gallery)
finally:
    sys.path.pop(0)


class ScientificGalleryTests(unittest.TestCase):
    def test_synthetic_fixture_preserves_missingness_and_boolean_type(self):
        data = gallery.fixture_data()
        self.assertIs(data['synthetic'], True)
        self.assertEqual(data, gallery.fixture_data())
        self.assertTrue(all(row['values'][2] is None for row in data['longitudinal']['subjects']))
        self.assertIsNone(data['heatmap']['values'][1][2])
        json.dumps(data, allow_nan=False)

    def test_box_whiskers_do_not_discard_outliers(self):
        data = gallery.fixture_data(); data['groups']['A'] = [0,1,2,3,4,100]
        stats = gallery.summarize(data); a = stats['groups']['A']
        self.assertEqual((a['q1'],a['median'],a['q3']), (1.25,2.5,3.75))
        self.assertEqual((a['whisker_low'],a['whisker_high']), (0,4))
        fig, ax = plt.subplots()
        try:
            gallery.draw('boxplot', ax, data, stats)
            plotted = np.concatenate([c.get_offsets()[:,1] for c in ax.collections])
            self.assertEqual(len(plotted), 6+len(data['groups']['B']))
            self.assertIn(100, plotted)
        finally:
            plt.close(fig)

    def test_ecdf_combines_ties_and_reaches_one(self):
        data = gallery.fixture_data(); data['groups']['A'] = [1,2,2,4]
        row = gallery.summarize(data)['ecdf']['A']
        self.assertEqual(row['x'], [1,2,4])
        self.assertEqual(row['cumulative'], [.25,.75,1])

    def test_time_gap_and_sample_sd_are_preserved_in_data_and_plot(self):
        data = gallery.fixture_data()
        data['longitudinal'] = {'weeks':[0,2,7], 'subjects':[{'id':'A','values':[1,None,4]},{'id':'B','values':[3,None,8]}]}
        stats = gallery.summarize(data)
        self.assertAlmostEqual(stats['line'][0]['sd'], 2**.5)
        self.assertEqual(stats['line'][1], {'week':2,'n':0,'mean':None,'sd':None})
        fig, ax = plt.subplots()
        try:
            gallery.draw('line', ax, data, stats)
            line = ax.lines[0]
            self.assertEqual(list(line.get_xdata()), [0,2,7])
            self.assertTrue(np.isnan(line.get_ydata()[1]))
        finally:
            plt.close(fig)

    def test_paired_differences_exclude_only_incomplete_pairs(self):
        data = gallery.fixture_data()
        data['paired'] = [{'id':'A','before':10,'after':8},{'id':'B','before':11,'after':None},{'id':'C','before':20,'after':17}]
        row = gallery.summarize(data)['paired']
        self.assertEqual(row, {'enrolled':3,'complete':2,'excluded':1,'mean_change':-2.5,'median_change':-2.5})

    def test_histogram_counts_conserve_all_observations(self):
        data = gallery.fixture_data(); hist = gallery.summarize(data)['histogram']
        pooled = sum(data['groups'].values(), [])
        self.assertEqual(sum(hist['counts']), len(pooled))
        for i, (lo, hi, count) in enumerate(zip(hist['edges'][:-1],hist['edges'][1:],hist['counts'])):
            self.assertEqual(count, sum(lo<=x and (x<=hi if i==len(hist['counts'])-1 else x<hi) for x in pooled))

    def test_heatmap_keeps_missing_mask_and_shared_scale(self):
        data = gallery.fixture_data(); stats = gallery.summarize(data)
        fig, ax = plt.subplots()
        try:
            gallery.draw('heatmap', ax, data, stats)
            artist = ax.images[0]
            self.assertTrue(artist.get_array().mask[1,2])
            self.assertEqual(artist.get_clim(), (0,5))
            self.assertEqual(artist.get_array()[0,0], 3.4)
        finally:
            plt.close(fig)

    def test_all_nine_charts_export_with_raw_and_derived_data(self):
        with tempfile.TemporaryDirectory(prefix='scientific-gallery-test-') as temp:
            root = Path(temp)
            data, stats = gallery.generate(root)
            self.assertEqual(json.loads((root/'data.json').read_text()), data)
            self.assertEqual(json.loads((root/'statistics.json').read_text()), stats)
            self.assertEqual({p.stem for p in (root/'figures').glob('*.svg')}, set(gallery.KINDS))
            self.assertEqual({p.stem for p in (root/'figures').glob('*.png')}, set(gallery.KINDS))
            for kind in gallery.KINDS:
                self.assertTrue(ET.parse(root/f'figures/{kind}.svg').getroot().tag.endswith('svg'))
                with Image.open(root/f'figures/{kind}.png') as image:
                    image.verify()
            self.assertTrue((root/'overview.png').is_file())
            self.assertTrue((root/'gallery.md').is_file())


if __name__ == '__main__':
    unittest.main()

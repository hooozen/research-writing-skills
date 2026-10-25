"""Numerical definitions and actual exported artifacts for scientific examples."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

os.environ.setdefault('MPLBACKEND','Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

SCRIPT=Path(__file__).resolve().parents[1]/'skills/scientific-chart-style/scripts/advanced_chart_gallery.py'
spec=importlib.util.spec_from_file_location('advanced_gallery',SCRIPT)
gallery=importlib.util.module_from_spec(spec)
sys.path.insert(0,str(SCRIPT.parent))
try:
    spec.loader.exec_module(gallery)
finally:
    sys.path.pop(0)


class AdvancedGalleryTests(unittest.TestCase):
    def test_tied_scores_enter_together_and_ap_is_not_trapezoidal_area(self):
        row=gallery.binary_curves([0,1,0,1],[.5,.5,.5,.5])
        self.assertEqual(row['thresholds'],[None,.5])
        self.assertEqual(row['fpr'],[0,1])
        self.assertEqual(row['tpr'],[0,1])
        self.assertAlmostEqual(row['roc_auc'],.5)
        self.assertAlmostEqual(row['average_precision'],.5)
        self.assertAlmostEqual(row['trapezoidal_pr_auc'],.75)

    def test_perfect_and_reversed_rankings_have_expected_auc_and_ap(self):
        perfect=gallery.binary_curves([0,0,1,1],[.1,.2,.8,.9])
        reverse=gallery.binary_curves([0,0,1,1],[.9,.8,.2,.1])
        self.assertEqual(perfect['roc_auc'],1)
        self.assertEqual(perfect['average_precision'],1)
        self.assertEqual(reverse['roc_auc'],0)
        self.assertAlmostEqual(reverse['average_precision'],(1/3+2/4)/2)
        with self.assertRaises(ValueError):
            gallery.binary_curves([1,1],[.2,.8])

    def test_calibration_bins_keep_zero_one_edges_and_empty_bins(self):
        row=gallery.calibration_bins([0,1,1],[0,.2,1],[0,.2,.4,.6,.8,1])
        self.assertEqual([r['n'] for r in row['bins']],[1,1,0,0,1])
        self.assertIsNone(row['bins'][2]['mean_probability'])
        self.assertEqual(row['bins'][-1]['mean_probability'],1)
        self.assertAlmostEqual(row['ece'],.8/3)
        with self.assertRaises(ValueError):
            gallery.calibration_bins([0,1],[0,1.2])

    def test_confusion_matrix_has_true_rows_predicted_columns_and_undefined_rows(self):
        row=gallery.confusion_summary([0,0,1,1],[.1,.7,.5,.3],.5)
        self.assertEqual(row['counts'],[[1,1],[1,1]])
        self.assertEqual(row['row_fraction'],[[.5,.5],[.5,.5]])
        row=gallery.confusion_summary([0,0],[.1,.2],.5)
        self.assertEqual(row['row_fraction'][1],[None,None])

    def test_agreement_limits_use_paired_difference_and_sample_sd(self):
        row=gallery.agreement_summary([10,20,30],[11,22,33])
        self.assertEqual(row['pair_mean'],[10.5,21,31.5])
        self.assertEqual(row['difference'],[1,2,3])
        self.assertEqual(row['bias'],2)
        self.assertEqual(row['sample_sd'],1)
        self.assertAlmostEqual(row['loa_low'],.04)
        self.assertAlmostEqual(row['loa_high'],3.96)

    def test_survival_ties_use_risk_before_events_and_censoring(self):
        row=gallery.kaplan_meier([2,2,4,5],[1,0,1,0],[0,2,3,5,6])
        self.assertEqual(row['n_at_risk'],[4,4,2,1,0])
        self.assertEqual(row['table'][0],dict(time=2.,at_risk=4,events=1,censored=1,survival=.75))
        self.assertEqual(row['step_survival'],[1,.75,.375,.375])
        self.assertEqual(row['censor_times'],[2,5])
        self.assertEqual(row['censor_survival'],[.75,.375])
        self.assertEqual(row['step_time'][-1],5)

    def test_risk_counts_are_horizontally_aligned_with_their_time_ticks(self):
        data=gallery.fixture_data();stats=gallery.summarize(data)
        fig,ax=plt.subplots()
        try:
            gallery.draw('survival',ax,data,stats)
            fig.canvas.draw()
            risk=[t for t in ax.texts if (t.get_gid() or '').startswith('km-risk-')]
            self.assertEqual(len(risk),len(stats['survival'])*len(data['survival']['risk_times']))
            for text in risk:
                time=float(text.get_gid().rsplit('-',1)[-1])
                actual_x=text.get_window_extent(fig.canvas.get_renderer()).x0+text.get_window_extent(fig.canvas.get_renderer()).width/2
                expected_x=ax.transData.transform((time,0))[0]
                self.assertAlmostEqual(actual_x,expected_x)
        finally:
            plt.close(fig)

    def test_bh_adjustment_restores_input_order_and_monotonic_sorted_values(self):
        actual=gallery.benjamini_hochberg([.04,.001,.03,.2])
        np.testing.assert_allclose(actual,[.05333333333333334,.004,.05333333333333334,.2])
        p=np.array([.3,.01,.01,.02,1,0])
        adjusted=gallery.benjamini_hochberg(p)
        self.assertTrue(np.all(np.diff(adjusted[np.argsort(p)])>=0))
        self.assertEqual(adjusted[1],adjusted[2])
        self.assertTrue(np.all((adjusted>=p)&(adjusted<=1)))

    def test_pca_variance_and_scores_reconstruct_the_standardized_matrix(self):
        x=np.array([[1,2,6],[2,1,5],[3,5,2],[5,4,1]],dtype=float)
        row=gallery.pca_summary(x)
        z=(x-x.mean(axis=0))/x.std(axis=0,ddof=1)
        scores,components=np.asarray(row['scores']),np.asarray(row['components'])
        np.testing.assert_allclose(scores@components,z,atol=1e-12)
        np.testing.assert_allclose(np.var(scores,axis=0,ddof=1),row['explained_variance'],atol=1e-12)
        self.assertAlmostEqual(sum(row['explained_variance_ratio']),1)
        self.assertAlmostEqual(sum(row['explained_variance']),3)
        with self.assertRaises(ValueError):
            gallery.pca_summary([[1,2],[1,3]])

    def test_raincloud_shows_every_observation_including_outlier(self):
        data=gallery.fixture_data();stats=gallery.summarize(data)
        fig,ax=plt.subplots()
        try:
            gallery.draw('raincloud',ax,data,stats)
            observed=[c.get_offsets() for c in ax.collections if len(c.get_offsets())>1]
            y=np.concatenate([p[:,1] for p in observed])
            self.assertEqual(len(y),sum(map(len,data['raincloud'].values())))
            self.assertIn(8.8,y)
        finally:
            plt.close(fig)

    def test_layout_validation_detects_outside_text_and_note_collision(self):
        fig,ax=plt.subplots()
        try:
            ax.plot([0,1],[0,1])
            outside=fig.text(1.05,.5,'Outside')
            with self.assertRaisesRegex(ValueError,'leaves final canvas'):
                gallery.validate_figure(fig)
            outside.remove()
            fig.text(.5,.5,'Note over data')
            with self.assertRaisesRegex(ValueError,'overlaps plot decorations'):
                gallery.validate_figure(fig)
        finally:
            plt.close(fig)

    def test_all_nine_charts_export_vectors_previews_and_exact_json(self):
        with tempfile.TemporaryDirectory(prefix='advanced-gallery-test-') as temp:
            root=Path(temp)
            data,stats=gallery.generate(root,mode='grayscale')
            self.assertIs(data['synthetic'],True)
            self.assertEqual(json.loads((root/'data.json').read_text()),data)
            self.assertEqual(json.loads((root/'statistics.json').read_text()),stats)
            manifest=json.loads((root/'manifest.json').read_text())
            self.assertEqual(manifest['mode'],'grayscale')
            self.assertEqual(manifest['figure_dimensions_mm']['roc']['width'],89)
            self.assertEqual(manifest['figure_dimensions_mm']['survival']['width'],180)
            self.assertEqual({p.stem for p in (root/'figures').glob('*.pdf')},set(gallery.KINDS))
            for kind in gallery.KINDS:
                tree=ET.parse(root/f'figures/{kind}.svg')
                self.assertTrue(tree.getroot().tag.endswith('svg'))
                self.assertIn('Synthetic data',' '.join(tree.getroot().itertext()))
                self.assertTrue((root/f'figures/{kind}.pdf').read_bytes().startswith(b'%PDF'))
                with Image.open(root/f'figures/{kind}.png') as image:
                    image.verify()
            self.assertTrue((root/'overview.png').is_file())
            self.assertTrue((root/'gallery.md').is_file())


if __name__=='__main__':
    unittest.main()

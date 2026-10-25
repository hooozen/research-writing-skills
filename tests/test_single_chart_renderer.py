"""Single-chart contracts, data isolation and executable reference paths."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

os.environ.setdefault('MPLBACKEND','Agg')
SCRIPT=Path(__file__).resolve().parents[1]/'skills/scientific-chart-style/scripts/render_chart.py'
spec=importlib.util.spec_from_file_location('single_chart_renderer',SCRIPT)
renderer=importlib.util.module_from_spec(spec)
sys.path.insert(0,str(SCRIPT.parent))
spec.loader.exec_module(renderer)


class SingleChartRendererTests(unittest.TestCase):
    def test_cli_requires_explicit_input_or_example_without_creating_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'uncreated'
            result=subprocess.run([sys.executable,str(SCRIPT),'--chart','roc','--output-dir',str(output)],text=True,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('explicitly choose --example',result.stderr)
            self.assertFalse(output.exists())

    def test_roc_renders_only_requested_chart_and_preserves_custom_raw_input(self):
        data={'labels':[0,1,0,1],'scores':[.1,.9,.4,.7]}
        source=json.loads(json.dumps(data))
        with tempfile.TemporaryDirectory() as temp:
            result=renderer.render_chart('roc',data,temp)
            root=Path(temp)
            self.assertEqual({p.name for p in root.iterdir()}, {'roc.svg','roc.png','data.json','statistics.json','manifest.json'})
            self.assertEqual(data,source)
            self.assertEqual(json.loads((root/'data.json').read_text()),source)
            stats=json.loads((root/'statistics.json').read_text())
            self.assertEqual(set(stats),{'ranking'})
            self.assertEqual(stats['ranking']['roc_auc'],1)
            self.assertFalse(result['metadata']['synthetic'])
            self.assertNotIn('Synthetic data',' '.join(ET.parse(root/'roc.svg').getroot().itertext()))
            self.assertEqual(result['metadata']['width_mm'],89)

    def test_color_and_print_have_identical_statistics_and_editable_svg(self):
        data={'synthetic':True,'groups':{'Control':[1,2,3,4],'Treated':[3,4,5,6]},'value_label':'Mass (g)'}
        with tempfile.TemporaryDirectory() as temp:
            paths=[]
            for mode in ['color','grayscale']:
                root=Path(temp)/mode
                renderer.render_chart('ecdf',data,root,mode=mode,formats=('svg',))
                tree=ET.parse(root/'ecdf.svg').getroot()
                self.assertTrue(any(n.tag.endswith('text') for n in tree.iter()))
                self.assertIn('Mass (g)',' '.join(tree.itertext()))
                paths.append(root)
            self.assertEqual((paths[0]/'statistics.json').read_bytes(),(paths[1]/'statistics.json').read_bytes())
            self.assertEqual((paths[0]/'data.json').read_bytes(),(paths[1]/'data.json').read_bytes())
            self.assertNotEqual((paths[0]/'ecdf.svg').read_bytes(),(paths[1]/'ecdf.svg').read_bytes())

    def test_three_arbitrarily_named_groups_are_not_silently_dropped(self):
        data={'groups':{'North':[1,2,3],'South':[4,5,6],'West':[7,8,9]},'value_label':'Length (cm)'}
        with tempfile.TemporaryDirectory() as temp:
            renderer.render_chart('boxplot',data,temp,formats=('svg',))
            text=' '.join(ET.parse(Path(temp)/'boxplot.svg').getroot().itertext())
            for name in data['groups']: self.assertIn(name,text)
            stats=json.loads((Path(temp)/'statistics.json').read_text())
            self.assertEqual(set(stats['groups']),set(data['groups']))

    def test_missing_paired_endpoint_is_retained_without_a_fake_pair(self):
        data={'pairs':[{'id':'A','before':2,'after':1},{'id':'B','before':3,'after':None}], 'value_label':'Response (a.u.)'}
        prepared,stats=renderer.prepare_chart('paired',data)
        self.assertEqual(stats['paired']['complete'],1)
        self.assertEqual(stats['paired']['baseline_n'],2)
        self.assertEqual(stats['paired']['followup_n'],1)
        self.assertEqual(prepared['paired'][1]['after'],None)
        with tempfile.TemporaryDirectory() as temp:
            renderer.render_chart('paired',data,temp,formats=('svg',))
            self.assertIn('1 complete pairs',' '.join(ET.parse(Path(temp)/'paired.svg').getroot().itertext()))

    def test_histogram_edges_include_every_supplied_observation(self):
        data={'groups':{'Batch':[100,100,102,110]},'value_label':'Frequency (Hz)'}
        _,stats=renderer.prepare_chart('histogram',data)
        self.assertEqual(sum(stats['histogram']['counts']),4)
        self.assertGreaterEqual(stats['histogram']['edges'][-1],110)
        bad=dict(data,bin_edges=[0,1,2])
        with self.assertRaisesRegex(ValueError,'contain every observation'):
            renderer.prepare_chart('histogram',bad)

    def test_count_relationships_do_not_normalize_overlapping_counts(self):
        data={'categories':['Flag A','Flag B'],'counts':[70,55],'denominator':100,'relationship':'overlapping','unit':'records'}
        _,stats=renderer.prepare_chart('count_share',data)
        self.assertEqual(stats['count_share']['shares'],[.7,.55])
        with self.assertRaisesRegex(ValueError,'reconcile'):
            renderer.prepare_chart('count_share',dict(data,relationship='exclusive_exhaustive'))
        _,stats=renderer.prepare_chart('count_share',dict(data,denominator=None))
        self.assertEqual(stats['count_share']['shares'],[None,None])

    def test_invalid_contracts_fail_before_creating_artifacts(self):
        cases=[
            ('boxplot',{'groups':{'A':[]},'value_label':'x'}),
            ('violin',{'groups':{'A':[2,2]},'value_label':'x'}),
            ('line',{'times':[2,0],'subjects':[{'id':'A','values':[1,2]}],'time_label':'h','value_label':'x'}),
            ('interval',{'estimates':[{'label':'A','estimate':3,'low':4,'high':5}],'reference':0,'value_label':'x','interval_label':'CI'}),
            ('heatmap',{'values':[[0,10]],'row_labels':['A'],'column_labels':['B','C'],'limits':[0,5],'value_label':'x'}),
            ('roc',{'labels':[1,1],'scores':[.2,.8]}),
            ('calibration',{'labels':[0,1],'probabilities':[0,1.2],'bin_edges':[0,.5,1]}),
            ('pca',{'values':[[1,2],[1,3]],'groups':['A','B'],'feature_names':['a','b'],'preprocessing':'standardize'}),
        ]
        with tempfile.TemporaryDirectory() as temp:
            for i,(kind,data) in enumerate(cases):
                root=Path(temp)/str(i)
                with self.subTest(kind=kind):
                    with self.assertRaises(ValueError): renderer.render_chart(kind,data,root)
                    self.assertFalse(root.exists())

    def test_constant_scatter_has_undefined_correlation_instead_of_fabricated_r(self):
        data={'observations':[{'x':1,'y':2},{'x':1,'y':3}],'x_label':'Constant x','y_label':'y'}
        with tempfile.TemporaryDirectory() as temp:
            renderer.render_chart('scatter',data,temp,formats=('svg',))
            stats=json.loads((Path(temp)/'statistics.json').read_text())
            self.assertIsNone(stats['scatter']['pearson_r'])

    def test_chinese_count_export_localizes_structure_and_preserves_supplied_unit(self):
        from matplotlib import font_manager
        fonts={f.name for f in font_manager.fontManager.ttflist}
        if not fonts.intersection({'Noto Sans CJK SC','PingFang SC','Microsoft YaHei','Arial Unicode MS','Heiti SC'}):
            self.skipTest('No installed CJK font for this rendered language check.')
        data={'synthetic':True,'categories':['标记A'],'counts':[0],'denominator':None,
              'relationship':'overlapping','unit':'custom unit'}
        with tempfile.TemporaryDirectory() as temp:
            renderer.render_chart('count_share',data,temp,language='zh',formats=('svg',))
            text=' '.join(ET.parse(Path(temp)/'count_share.svg').getroot().itertext())
            self.assertIn('custom unit',text)
            self.assertIn('标记A',text)
            self.assertIn('占比不可用',text)
            self.assertNotIn('Denominator:',text)
            self.assertNotIn('share unavailable',text)
            stats=json.loads((Path(temp)/'statistics.json').read_text())
            self.assertEqual(stats['count_share']['shares'],[None])

    def test_cli_example_routes_a_single_fixture_and_list_is_stdlib_only(self):
        registry=renderer.SKILL_ROOT/'references/chart-index.json'
        self.assertTrue(registry.is_file(), 'The single-chart registry is required.')
        result=subprocess.run([sys.executable,str(SCRIPT),'--list'],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual({r['id'] for r in json.loads(result.stdout)['charts']},set(renderer.CHART_IDS))
        # A dedicated interpreter import probe shows routing does not import plotting libraries.
        probe=(f'import runpy,sys\nsys.argv=[{str(SCRIPT)!r},"--list"]\n'
               f'try: runpy.run_path({str(SCRIPT)!r},run_name="__main__")\n'
               'except SystemExit as error: assert error.code == 0\n'
               'assert "matplotlib" not in sys.modules\nassert "numpy" not in sys.modules\n')
        result=subprocess.run([sys.executable,'-c',probe],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        with tempfile.TemporaryDirectory() as temp:
            result=subprocess.run([sys.executable,str(SCRIPT),'--chart','roc','--example','--output-dir',temp,'--formats','svg'],text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual({p.suffix for p in Path(temp).iterdir()},{'.svg','.json'})
            self.assertTrue(json.loads((Path(temp)/'manifest.json').read_text())['synthetic'])


if __name__=='__main__':
    unittest.main()

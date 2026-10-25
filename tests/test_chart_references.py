"""Reference lookup/integrity checks without re-rendering on CI font stacks."""
from __future__ import annotations

import base64
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'skills/scientific-chart-style'
SCRIPT = SKILL/'scripts/build_chart_references.py'
spec = importlib.util.spec_from_file_location('chart_reference_builder', SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="252pt" height="180pt"><text x="4" y="12">Synthetic chart</text><path d="M1 2L3 4"/></svg>'
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jR6kAAAAASUVORK5CYII=')


class ReferenceBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='chart-reference-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for relative in builder.SOURCE_PATHS:
            path = self.root/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('source fixture: '+relative+'\n')
        self.charts = []
        for name in sorted(builder.CHART_IDS):
            item = dict(id=name, name=name.replace('_', ' '), question='What changed?',
                        required_inputs=['observations', 'units'], family='basic',
                        guide=f'references/charts/{name}.md',
                        input=f'references/examples/{name}.json',
                        svg=f'references/examples/{name}.svg',
                        png=f'references/examples/{name}.png')
            self.charts.append(item)
            path = self.root/item['guide']; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Scientific definition and one example for '+name+'\n')
            path = self.root/item['input']; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({'synthetic': True, 'values': [1, 2, 4]}))
        self.write_registry()
        self.calls = []

    def write_registry(self):
        (self.root/builder.REGISTRY).write_text(json.dumps({'schema_version': 1, 'charts': self.charts}))

    def fake_renderer(self, chart_id, data, output, *, mode, formats):
        self.calls.append((chart_id, data, mode, formats))
        (output/(chart_id+'.svg')).write_text(SVG)
        (output/(chart_id+'.png')).write_bytes(PNG)
        return {'chart': chart_id, 'metadata': {'synthetic': True}}

    def build(self):
        return builder.build_references(self.root, renderer=self.fake_renderer)

    def snapshot(self):
        return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob('*') if p.is_file()}

    def test_complete_build_maps_every_chart_and_check_is_read_only(self):
        manifest = self.build()
        self.assertEqual(set(manifest['charts']), builder.CHART_IDS)
        self.assertEqual({call[0] for call in self.calls}, builder.CHART_IDS)
        self.assertEqual(len(self.calls), 19)
        self.assertTrue(all(call[2:] == ('color', ('svg', 'png')) for call in self.calls))
        before = self.snapshot()
        self.assertEqual(builder.check_references(self.root), [])
        self.assertEqual(self.snapshot(), before)
        index = (self.root/builder.INDEX).read_text()
        for item in self.charts:
            self.assertIn('(charts/'+item['id']+'.md)', index)
            self.assertIn('(examples/'+item['id']+'.svg)', index)
            self.assertIn('(examples/'+item['id']+'.png)', index)
        self.assertNotIn('![', index, 'The mandatory text index must not eagerly embed previews.')
        one = manifest['charts']['roc']
        self.assertAlmostEqual(one['svg_dimensions_mm']['width'], 88.9)
        self.assertEqual(one['png_pixels'], {'width': 1, 'height': 1})

    def test_missing_preview_is_detected(self):
        self.build()
        (self.root/'references/examples/roc.svg').unlink()
        self.assertTrue(any('missing svg' in error for error in builder.check_references(self.root)))

    def test_changed_input_source_and_image_each_fail_freshness(self):
        self.build()
        targets = [self.root/'references/examples/roc.json',
                   self.root/'scripts/render_chart.py',
                   self.root/'references/style-guide.md',
                   self.root/'references/examples/roc.svg']
        for path in targets:
            with self.subTest(path=path.name):
                original = path.read_bytes()
                path.write_bytes(original+b'\n')
                self.assertTrue(builder.check_references(self.root))
                path.write_bytes(original)
                self.assertEqual(builder.check_references(self.root), [])

    def test_broken_registry_mapping_duplicate_and_missing_ids_are_rejected(self):
        original = list(self.charts)
        self.charts[0] = dict(self.charts[0], svg='references/examples/roc.svg')
        self.write_registry()
        with self.assertRaisesRegex(ValueError, 'must map'):
            builder.load_registry(self.root)
        self.charts = original+[original[0]]; self.write_registry()
        with self.assertRaisesRegex(ValueError, 'unique'):
            builder.load_registry(self.root)
        self.charts = original[:-1]; self.write_registry()
        with self.assertRaisesRegex(ValueError, '19 supported'):
            builder.load_registry(self.root)

    def test_paths_cannot_escape_skill_or_use_external_urls(self):
        for path in ('../other.json', '/tmp/other.json', 'https://example.org/a.svg', 'references\\other.svg'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                builder.resource(self.root, path)
        outside = self.root.parent/(self.root.name+'-outside')
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        (self.root/'escape').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            builder.resource(self.root, 'escape/example.svg')

    def test_svg_requires_editable_text_and_vector_marks(self):
        svg, png = self.root/'reference.svg', self.root/'reference.png'
        png.write_bytes(PNG)
        for content in ['<svg width="20pt" height="20pt"><path/></svg>',
                        '<svg width="20pt" height="20pt"><text>Chart</text><image/></svg>']:
            svg.write_text(content)
            with self.assertRaisesRegex(ValueError, 'editable text and vector'):
                builder.preview_properties(svg, png)

    def test_failed_render_does_not_replace_existing_references(self):
        self.build()
        before = self.snapshot()
        count = 0
        def fail_on_second(*args, **kwargs):
            nonlocal count
            count += 1
            if count == 2:
                raise ValueError('A reference failed to render.')
            return self.fake_renderer(*args, **kwargs)
        with self.assertRaisesRegex(ValueError, 'failed to render'):
            builder.build_references(self.root, renderer=fail_on_second)
        self.assertEqual(self.snapshot(), before)

    def test_inputs_modified_during_render_are_not_recorded_as_fresh(self):
        def change_input(*args, **kwargs):
            result = self.fake_renderer(*args, **kwargs)
            if args[0] == self.charts[0]['id']:
                target = self.root/self.charts[-1]['input']
                target.write_text(json.dumps({'synthetic': True, 'values': [9, 9]}))
            return result
        with self.assertRaisesRegex(ValueError, 'changed during the build'):
            builder.build_references(self.root, renderer=change_input)
        self.assertFalse((self.root/builder.MANIFEST).exists())
        self.assertFalse((self.root/'references/examples/roc.svg').exists())

    def test_changed_index_and_unlabeled_input_are_not_accepted(self):
        self.build()
        index = self.root/builder.INDEX
        index.write_text(index.read_text().replace('charts/roc.md', 'charts/pr.md'))
        self.assertTrue(any('index is stale' in error for error in builder.check_references(self.root)))
        input_path = self.root/'references/examples/roc.json'
        input_path.write_text(json.dumps({'values': [1, 2, 3]}))
        self.assertTrue(any('synthetic' in error for error in builder.check_references(self.root)))

    def test_read_only_cli_does_not_require_plotting_imports(self):
        self.build()
        before = self.snapshot()
        # Importing the check implementation itself must not import Matplotlib.
        code = ('import importlib.util,sys; '
                f's=importlib.util.spec_from_file_location("refcheck",{str(SCRIPT)!r}); '
                'm=importlib.util.module_from_spec(s);s.loader.exec_module(m); '
                f'assert not m.check_references(m.Path({str(self.root)!r})); '
                'assert "matplotlib" not in sys.modules')
        result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_repository_has_all_19_fresh_readable_references(self):
        self.assertEqual(builder.check_references(SKILL), [])


if __name__ == '__main__':
    unittest.main()

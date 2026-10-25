"""Execute the actual short chart-card examples against their recorded inputs."""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest

os.environ.setdefault('MPLBACKEND', 'Agg')
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'skills/scientific-chart-style'


class ChartCardExampleTests(unittest.TestCase):
    def test_every_card_code_runs_one_chart_with_its_exact_recorded_input(self):
        registry = json.loads((SKILL/'references/chart-index.json').read_text())
        old_cwd, old_path = Path.cwd(), list(sys.path)
        with tempfile.TemporaryDirectory(prefix='chart-card-examples-') as temporary:
            try:
                os.chdir(SKILL)
                for entry in registry['charts']:
                    with self.subTest(chart=entry['id']):
                        card = (SKILL/entry['guide']).read_text()
                        blocks = re.findall(r'```python\n(.*?)\n```', card, re.DOTALL)
                        self.assertEqual(len(blocks), 1, 'Provide one unambiguous minimal runnable example.')
                        tree = ast.parse(blocks[0], filename=entry['guide'])
                        inputs = [node.value for node in tree.body if isinstance(node, ast.Assign)
                                  and any(isinstance(target, ast.Name) and target.id == 'data' for target in node.targets)]
                        self.assertEqual(len(inputs), 1)
                        expected = json.loads((SKILL/entry['input']).read_text())
                        self.assertEqual(ast.literal_eval(inputs[0]), expected)
                        calls = [node.value for node in tree.body if isinstance(node, ast.Expr)
                                 and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
                                 and node.value.func.id == 'render_chart']
                        self.assertEqual(len(calls), 1)
                        self.assertEqual(ast.literal_eval(calls[0].args[0]), entry['id'])
                        output = Path(temporary)/entry['id']
                        # The published demo path is replaced only for test isolation.
                        calls[0].args[2] = ast.Constant(str(output))
                        ast.fix_missing_locations(tree)
                        exec(compile(tree, entry['guide'], 'exec'), {})
                        self.assertEqual(json.loads((output/'data.json').read_text()), expected)
                        self.assertEqual({p.stem for p in output.glob('*.svg')}, {entry['id']})
                        self.assertEqual({p.stem for p in output.glob('*.png')}, {entry['id']})
                        self.assertFalse((output/'overview.png').exists())
                        self.assertEqual(json.loads((output/'manifest.json').read_text())['chart'], entry['id'])
                        sys.path[:] = old_path
            finally:
                os.chdir(old_cwd)
                sys.path[:] = old_path


if __name__ == '__main__':
    unittest.main()

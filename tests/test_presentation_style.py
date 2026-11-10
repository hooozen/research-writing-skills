"""Data/statistics regressions for the optional presentation adapter."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PresentationStyleTests(unittest.TestCase):
    def test_palette_matches_the_scientific_chart_source(self):
        spec = importlib.util.spec_from_file_location("presentation_chart_style", ROOT / "skills/scientific-chart-style/scripts/matplotlib_example.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        tokens = json.loads((ROOT / "skills/scientific-presentation-style/assets/design-tokens.json").read_text())
        for mode in ("color", "grayscale"):
            actual = tokens["colors"] | (tokens["grayscale"] if mode == "grayscale" else {})
            expected = module.get_style(mode)
            for key in ("primary", "secondary", "third", "light", "neutral", "text", "muted"):
                with self.subTest(mode=mode, key=key):
                    self.assertEqual(actual[key], expected[key])
            self.assertEqual(actual["axis"], expected["baseline"])
            self.assertEqual(actual["background"], expected["canvas"])

    def test_native_adapter_data_and_statistics(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js 20+ is required for presentation adapter regression checks")
        result = subprocess.run([node, "--test", str(ROOT / "tests/presentation_adapter.test.mjs")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

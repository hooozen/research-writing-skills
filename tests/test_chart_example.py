"""Check denominator semantics and both supported export formats."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

os.environ.setdefault("MPLBACKEND", "Agg")
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chart_example", ROOT / "skills/clinical-data-chart-style/scripts/matplotlib_example.py")
chart = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chart)


class ChartExampleTests(unittest.TestCase):
    def test_exact_count_and_share_labels(self):
        self.assertEqual(chart.count_share_label(14325, 28552), "14,325 · 50.2%")
        self.assertEqual(chart.count_share_label(0, 100), "0 · 0.0%")

    def test_zero_and_unknown_population_have_no_percentage(self):
        self.assertEqual(chart.count_share_label(0, 0), "0 · share unavailable")
        self.assertEqual(chart.count_share_label(12, None), "12 · share unavailable")

    def test_invalid_counts_fail_before_rendering(self):
        for value, total in ((-1, 10), (1, 0), (11, 10), (1.5, 10), (True, 10), (1, -2), (1, 2.0)):
            with self.subTest(value=value, total=total):
                with self.assertRaises(ValueError):
                    chart.count_share_label(value, total)

    def test_png_and_svg_export_include_correct_synthetic_values(self):
        with tempfile.TemporaryDirectory(prefix="chart-export-test-") as tmp:
            svg, png = Path(tmp) / "chart.svg", Path(tmp) / "chart.png"
            chart.build_example(svg)
            chart.build_example(png)
            text = " ".join(ET.parse(svg).getroot().itertext())
            for expected in ("14,325 · 50.2%", "12,194 · 42.7%", "2,033 · 7.1%", "Synthetic", "28,552 scans"):
                self.assertIn(expected, text)
            self.assertEqual(png.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()

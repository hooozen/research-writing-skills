# Calibration diagram (`calibration`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use calibration for probability predictions on an identified evaluation population. Raw arbitrary scores are insufficient. Calibration and ranking answer different questions; a good ROC curve does not establish calibrated probabilities.

## Minimal inputs

`labels` contains 0/1 outcomes; `probabilities` has matching finite values in [0,1]. Supply increasing `bin_edges` from 0 to 1. Record how probabilities/calibration were fitted, and where evaluation occurred.

## Encoding and calculation

Bins are left-closed/right-open, with 1 included in the final bin. Each nonempty bin plots actual mean probability against observed positive fraction and reports n; empty bins remain missing, not zero. ECE is the n-weighted absolute bin gap and depends on binning. The identity line is a reference.

## Interpretation limits

Do not interpolate across empty bins, fabricate bin confidence intervals or fit a calibrator on the final test data without disclosing reuse. Brier score also reflects factors beyond calibration. This fixture deliberately includes empty bins.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart calibration --example --output-dir /tmp/calibration-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'labels': [0, 0, 1, 0, 1, 1, 1, 1],
 'probabilities': [0, 0.05, 0.15, 0.65, 0.72, 0.85, 0.95, 1],
 'bin_edges': [0, 0.2, 0.4, 0.6, 0.8, 1]}
render_chart("calibration", data, "/tmp/calibration-example")
```

**References:** [exact input](../examples/calibration.json) · [editable SVG](../examples/calibration.svg) · [PNG visual fallback](../examples/calibration.png). All example values are synthetic.

**Definition source:** [Official calibration guide](https://scikit-learn.org/stable/modules/calibration.html).

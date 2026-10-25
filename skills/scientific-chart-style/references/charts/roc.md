# ROC curve (`roc`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use ROC for binary ranking evaluation from per-case labels and scores on an identified evaluation population. A confusion matrix at one threshold cannot reconstruct this curve. ROC does not assess probability calibration.

## Minimal inputs

`labels` is a 0/1 vector with both classes; `scores` is a same-length finite vector, larger meaning more positive. Define positive class 1, the evaluation population, weighting and repeated-unit structure. Scores need not be calibrated probabilities.

## Encoding and calculation

At each threshold, include all tied scores together with score ≥ threshold. Plot FPR = FP/(FP+TN) against TPR = TP/(TP+FN), spanning 0–1. This reference reports trapezoidal ROC AUC over empirical threshold points and a restrained chance diagonal.

## Interpretation limits

One-class data cannot support this binary ROC. AUC does not specify sensitivity at an operational threshold, calibration, causation or statistical superiority. Show operating points or uncertainty only from a stated valid protocol; never choose a threshold on final test data silently.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart roc --example --output-dir /tmp/roc-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'labels': [0, 1, 0, 1, 0, 1, 1, 0],
 'scores': [0.1, 0.8, 0.4, 0.8, 0.2, 0.6, 0.45, 0.45]}
render_chart("roc", data, "/tmp/roc-example")
```

**References:** [exact input](../examples/roc.json) · [editable SVG](../examples/roc.svg) · [PNG visual fallback](../examples/roc.png). All example values are synthetic.

**Definition source:** [Official ROC definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html).

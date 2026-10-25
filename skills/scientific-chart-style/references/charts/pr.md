# Precision–recall curve (`pr`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use precision–recall to expose positive prediction quality, particularly when negatives dominate. Compare models on the same evaluation population; positive-class prevalence affects this view. A single confusion matrix cannot supply the curve.

## Minimal inputs

`labels` is a 0/1 vector with positive and negative cases; `scores` is a same-length finite vector with larger values more positive. Define positive class 1 and evaluation population; preserve tied scores as a group.

## Encoding and calculation

Plot precision = TP/(TP+FP) versus recall = TP/(TP+FN). The empirical reference step uses the precision after each recall increase. AP = sum(Δrecall × precision), without interpolation; trapezoidal PR area is separately named and not substituted for AP. Show prevalence as its identified reference.

## Interpretation limits

No positives makes recall-based evaluation undefined. Do not smooth the curve, compare unmatched prevalences as if identical, or interpret a curve summary as a threshold-specific operating point or calibration result.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart pr --example --output-dir /tmp/pr-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'labels': [0, 1, 0, 1, 0, 1, 1, 0],
 'scores': [0.1, 0.8, 0.4, 0.8, 0.2, 0.6, 0.45, 0.45]}
render_chart("pr", data, "/tmp/pr-example")
```

**References:** [exact input](../examples/pr.json) · [editable SVG](../examples/pr.svg) · [PNG visual fallback](../examples/pr.png). All example values are synthetic.

**Definition source:** [Official AP definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html).

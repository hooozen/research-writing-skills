# Confusion matrix (`confusion`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use a confusion matrix for classification outcomes at a fixed, stated rule. This runnable reference is binary, with positive class 1. Scores across thresholds or probabilities are needed for ROC/PR or calibration, respectively.

## Minimal inputs

`labels` is a 0/1 vector; `scores` is a matching finite vector; numeric `threshold` defines score ≥ threshold as positive. Supply the same class order and evaluation population for comparisons. A multiclass/count-matrix extension needs its own explicit adapter.

## Encoding and calculation

Rows are true classes and columns predicted classes. Cell counts are exact; color represents within-true-class fractions on one shared 0–1 scale. Show count and row percentage together. A row with zero support has undefined fractions, not zero performance.

## Interpretation limits

Always label true/predicted axes and normalization. Do not derive ranking curves or calibrated probabilities from the matrix, compare different normalizations silently, or tune a threshold on final test data and claim untouched evaluation.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart confusion --example --output-dir /tmp/confusion-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'labels': [0, 0, 0, 0, 1, 1, 1, 1],
 'scores': [0.1, 0.2, 0.55, 0.3, 0.5, 0.8, 0.4, 0.9],
 'threshold': 0.5}
render_chart("confusion", data, "/tmp/confusion-example")
```

**References:** [exact input](../examples/confusion.json) · [editable SVG](../examples/confusion.svg) · [PNG visual fallback](../examples/confusion.png). All example values are synthetic.

**Definition source:** [Official confusion-matrix conventions](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html).

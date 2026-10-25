# Time series / longitudinal summary (`line`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use lines for a meaningful ordered predictor, especially actual time. For unordered conditions, use points or grouped distributions. Shared participants across visits do not become independent observations at every time.

## Minimal inputs

`times` contains increasing finite coordinates. Each `subjects` record has a stable `id` and a matching-length `values` array; missing observations are `null`. Supply `time_label` and `value_label` with units.

## Encoding and calculation

At each time, summarize available values with a mean and sample SD (`ddof=1`) and report n. SD is absent with fewer than two observations. An entirely missing visit remains a gap in both line and band; uneven times retain uneven spacing.

## Interpretation limits

A mean ± SD band is not a confidence interval for the mean or individual prediction. Do not delete an unobserved visit and connect over it, treat missing as zero, or claim a longitudinal treatment effect from the picture.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart line --example --output-dir /tmp/line-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'times': [0, 2, 4, 7],
 'subjects': [{'id': 'S1', 'values': [10, None, 12, 14]},
              {'id': 'S2', 'values': [12, None, 14, 15]},
              {'id': 'S3', 'values': [11, None, 13, None]}],
 'time_label': 'Time (h)',
 'value_label': 'Response (a.u.)'}
render_chart("line", data, "/tmp/line-example")
```

**References:** [exact input](../examples/line.json) · [editable SVG](../examples/line.svg) · [PNG visual fallback](../examples/line.png). All example values are synthetic.

**Definition source:** [Matplotlib missing-value behavior](https://matplotlib.org/stable/gallery/lines_bars_and_markers/masked_demo.html).

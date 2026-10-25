# Violin plot with observations (`violin`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use a violin when a smooth density adds information to continuous observations. Prefer points, a box or an ECDF for very small, discrete or strongly bounded samples that a smooth cloud could misrepresent.

## Minimal inputs

`groups` maps group names to finite raw measurements with nonzero variation; `value_label` gives quantity and unit. A mean/SD/n summary is insufficient. Keep group sample sizes and the observation unit explicit.

The optional runner accepts one to three groups; use facets or an explicitly extended implementation for more groups.

## Encoding and calculation

The reference uses Gaussian KDE with Scott bandwidth, trimmed to the observed range, plus raw observations and a thin median mark. Equal maximum widths do not encode group n. Show the actual points in front of the light density fill.

## Interpretation limits

A KDE is an estimate, not additional observations or evidence of multimodality. State bandwidth and support; do not infer significance or an effect from silhouette shape. Do not synthesize values to fill a requested violin.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart violin --example --output-dir /tmp/violin-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'groups': {'A': [3.8, 4.1, 4.4, 4.7, 4.9, 5.0, 5.2, 5.4, 5.5, 5.8, 6.0, 6.4],
            'B': [4.3, 4.7, 5.0, 5.2, 5.5, 5.8, 6.0, 6.1, 6.4, 6.8, 7.1, 7.5]},
 'value_label': 'Measurement (a.u.)'}
render_chart("violin", data, "/tmp/violin-example")
```

**References:** [exact input](../examples/violin.json) · [editable SVG](../examples/violin.svg) · [PNG visual fallback](../examples/violin.png). All example values are synthetic.

**Definition source:** [Matplotlib violin parameters](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.violinplot.html).

# Scatter plot (`scatter`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use one point per supplied x/y pair to inspect association, range and outliers. A scatter plot describes the observed relationship; it does not establish causation or prediction performance.

## Minimal inputs

`observations` is a list of `{x, y}` pairs measured on the same unit. Supply `x_label` and `y_label` with units. Repeated observations need their actual sample/cluster identifiers in the source and a suitable interpretation.

## Encoding and calculation

Plot the actual coordinates. A descriptive Pearson correlation, if reported, uses those same complete pairs and is undefined for a constant coordinate. Add no fitted model or interval unless supplied or justified. Use transparency or a stated density/count encoding for crowding.

## Interpretation limits

Do not pair independently sorted x and y arrays, label every dense point, infer a causal effect, or invent a fitted trend. Any downsampling affects displayed marks only and must not silently replace full-data statistics.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart scatter --example --output-dir /tmp/scatter-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'observations': [{'x': 1, 'y': 2.2},
                  {'x': 2, 'y': 2.7},
                  {'x': 3, 'y': 2.4},
                  {'x': 4, 'y': 3.7},
                  {'x': 5, 'y': 3.9},
                  {'x': 6, 'y': 4.2}],
 'x_label': 'Input measurement (a.u.)',
 'y_label': 'Output measurement (a.u.)'}
render_chart("scatter", data, "/tmp/scatter-example")
```

**References:** [exact input](../examples/scatter.json) · [editable SVG](../examples/scatter.svg) · [PNG visual fallback](../examples/scatter.png). All example values are synthetic.

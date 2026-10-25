# Empirical cumulative distribution (`ecdf`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use an ECDF to compare entire numerical distributions without choosing a KDE bandwidth or histogram bins. It remains useful for small samples and tied values. It does not replace an effect estimate when effect magnitude is the question.

## Minimal inputs

`groups` maps each named group to finite raw observations. `value_label` defines the measured quantity and unit. Each group uses its own sample count as the denominator; record n and dependence structure.

The optional runner accepts one to three groups; use facets or an explicitly extended implementation for more groups.

## Encoding and calculation

For each group, F(x) = count(values ≤ x) / n. Sort unique values, combine ties into their actual cumulative jump and draw a right-continuous staircase. Retain zero and one endpoint plateaus; distinguish groups by line style as well as color.

## Interpretation limits

Do not smooth the staircase or normalize all groups by a common pooled n. Vertical separation is descriptive and does not establish a statistical test, causal shift or independence of repeated records.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart ecdf --example --output-dir /tmp/ecdf-example
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
render_chart("ecdf", data, "/tmp/ecdf-example")
```

**References:** [exact input](../examples/ecdf.json) · [editable SVG](../examples/ecdf.svg) · [PNG visual fallback](../examples/ecdf.png). All example values are synthetic.

# Effect estimates and intervals (`interval`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use points and horizontal intervals for estimates with supported uncertainty. This is suitable for a compact coefficient/forest-style view without implying a meta-analysis. Raw distributions answer a different question.

## Minimal inputs

`estimates` contains `label`, `estimate`, `low`, `high`; bounds bracket the estimate and retain signed units. Supply numeric `reference`, `value_label`, and a truthful `interval_label` identifying the provided interval type and provenance.

## Encoding and calculation

A point marks the supplied estimate; its segment spans the actual lower and upper bounds. For differences, the usual null is zero. Ratios generally need one and may require a log axis; explicitly adapt both axis and interpretation for that protocol.

## Interpretation limits

The renderer does not infer CI, SD, SE, n or p-values from endpoints. Crossing a reference does not prove absence of an effect. Do not add a pooled diamond or call this meta-analysis without an actual synthesis design.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart interval --example --output-dir /tmp/interval-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'estimates': [{'label': 'Method A', 'estimate': -0.8, 'low': -1.3, 'high': -0.2},
               {'label': 'Method B', 'estimate': 0.3, 'low': 0.1, 'high': 0.7}],
 'reference': 0,
 'value_label': 'Difference from reference (a.u.)',
 'interval_label': '95% CI (supplied)'}
render_chart("interval", data, "/tmp/interval-example")
```

**References:** [exact input](../examples/interval.json) · [editable SVG](../examples/interval.svg) · [PNG visual fallback](../examples/interval.png). All example values are synthetic.

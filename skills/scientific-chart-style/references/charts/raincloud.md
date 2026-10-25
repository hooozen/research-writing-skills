# Raincloud (`raincloud`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use a raincloud to combine a light half-density, a defined summary and actual observations in separate lanes. Prefer a simpler point/box/ECDF view when the density adds little or data are discrete, bounded or too sparse.

## Minimal inputs

`groups` maps group names to finite raw measurements with nonzero variation; `value_label` includes units. Group n and the independence/repetition unit belong in the caption. Mean/SD/n cannot reconstruct a cloud.

The optional runner accepts one to three groups; use facets or an explicitly extended implementation for more groups.

## Encoding and calculation

The reference uses a Gaussian Scott-bandwidth KDE trimmed to the observed range, a Q1–Q3/median box with 1.5-IQR observed whiskers, and every point once. Equal maximum density widths do not encode group sample size. Jitter is perpendicular to the measurement axis.

## Interpretation limits

Keep clouds, points and summary marks separated. A smoothed density is not new evidence of subgroups; the example makes no effect or significance claim. A separate estimation view needs an actually computed or supplied effect and interval.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart raincloud --example --output-dir /tmp/raincloud-example
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
render_chart("raincloud", data, "/tmp/raincloud-example")
```

**References:** [exact input](../examples/raincloud.json) · [editable SVG](../examples/raincloud.svg) · [PNG visual fallback](../examples/raincloud.png). All example values are synthetic.

**Definition source:** [Allen et al., raincloud paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6480976/).

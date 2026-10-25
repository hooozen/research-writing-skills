# Histogram (`histogram`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use bins for the distribution of numerical observations. An ECDF avoids bin selection; a dot view can be more honest for a very small dataset. Do not use unordered category names as numerical bins.

## Minimal inputs

`groups` supplies finite raw measurements; the reference pools the supplied groups for one count histogram. `value_label` includes units. Record which groups are pooled and total n; do not imply that pooled data retain group differences.

The optional runner accepts one to three groups; use facets or an explicitly extended implementation for more groups.

## Encoding and calculation

Count each observation once using explicit bin edges or a recorded binning rule. Preserve the chosen boundaries in the numerical companion. Count height, proportion and probability density are different encodings; density divides by both total count and bin width.

## Interpretation limits

Do not change edges between comparable panels without explanation, omit observations outside the displayed bins silently, or infer stable modes from one arbitrary width. Any log transform or clipping belongs in the caption and axis labels.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart histogram --example --output-dir /tmp/histogram-example
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
render_chart("histogram", data, "/tmp/histogram-example")
```

**References:** [exact input](../examples/histogram.json) · [editable SVG](../examples/histogram.svg) · [PNG visual fallback](../examples/histogram.png). All example values are synthetic.

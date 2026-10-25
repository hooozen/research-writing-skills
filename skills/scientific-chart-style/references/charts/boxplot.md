# Box plot with observations (`boxplot`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use a box plus individual observations for continuous group distributions. It exposes sample size and unusual values while summarizing location and spread. Mean, SD and n cannot reconstruct quartiles or hidden observations.

## Minimal inputs

`groups` maps each group name to finite raw measurements; `value_label` names the quantity and unit. Record independence, repeated units and exclusions in the caption. The reference uses small independent synthetic groups.

The optional runner accepts one to three groups; use facets or an explicitly extended implementation for more groups.

## Encoding and calculation

The box spans linearly interpolated Q1–Q3, with a thin median stroke. Whiskers reach the most extreme observed values within Q1 − 1.5 IQR and Q3 + 1.5 IQR. Overlay every observation, including outliers; suppress duplicate automatic flier marks only.

## Interpretation limits

Whiskers are not generally min/max, SD or confidence limits. The horizontal jitter is a display offset, never a changed measurement. Quartile conventions can matter for small samples; preserve the actual method.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart boxplot --example --output-dir /tmp/boxplot-example
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
render_chart("boxplot", data, "/tmp/boxplot-example")
```

**References:** [exact input](../examples/boxplot.json) · [editable SVG](../examples/boxplot.svg) · [PNG visual fallback](../examples/boxplot.png). All example values are synthetic.

**Definition source:** [Matplotlib box-plot definition](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html).

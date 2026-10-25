# Kaplan–Meier survival (`survival`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use Kaplan–Meier with observed durations and right-censor indicators from a common time origin. Aggregate event percentages cannot reconstruct it. Delayed entry, competing risks or informative censoring require a suitable different/extended analysis.

## Minimal inputs

`groups` maps names to matching finite nonnegative `duration` and binary `event` vectors (1=event, 0=censor). Supply `risk_times` and `time_unit`. State eligibility, origin and censoring assumptions; this reference has no delayed entry.

The optional runner supports up to three group identities; extend or facet deliberately when more are needed.

## Encoding and calculation

At event times, S(t) = product(1−d/n), using n at risk immediately before the event. Tied events are counted before removing same-time censored units. Curves are steps, censor marks use post-event survival, and aligned risk counts use duration ≥ displayed time. Stop each curve at its last observation.

## Interpretation limits

A median not reached stays not reached. Do not smooth or extrapolate a sparse tail, invent confidence bands, or interpret curve separation as a hazard ratio, causal effect or competing-risk incidence.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart survival --example --output-dir /tmp/survival-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'groups': {'A': {'duration': [1, 2, 2, 4, 5, 6], 'event': [1, 0, 1, 1, 0, 1]},
            'B': {'duration': [2, 3, 4, 4, 6, 7], 'event': [1, 0, 1, 0, 1, 0]}},
 'risk_times': [0, 2, 4, 6],
 'time_unit': 'months'}
render_chart("survival", data, "/tmp/survival-example")
```

**References:** [exact input](../examples/survival.json) · [editable SVG](../examples/survival.svg) · [PNG visual fallback](../examples/survival.png). All example values are synthetic.

**Definition source:** [Official survival-estimation documentation](https://www.statsmodels.org/stable/duration.html).

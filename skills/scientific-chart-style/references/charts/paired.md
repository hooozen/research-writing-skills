# Paired observations (`paired`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use connecting segments only for repeated measurements on the same units. Independent before/after groups require an unpaired comparison. The direction and dispersion of observed individual changes should remain visible.

## Minimal inputs

`pairs` is a list of stable `id`, `before`, `after` records. Measurements may be `null`; `value_label` gives units. Report enrolled, observed and complete-pair counts, and which missing records are omitted from paired summaries.

## Encoding and calculation

Match records by ID, not rank. Connect actual complete pairs and preserve every measured y value. Any paired mean/median change uses the same complete pairs. A missing follow-up can be identified as a baseline-only mark if retained; it cannot create a segment.

## Interpretation limits

Do not invent zero follow-up, pair independently sorted values, or turn individual trajectories into confidence intervals or a significance claim. Perpendicular display offsets must not alter the measured coordinate.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart paired --example --output-dir /tmp/paired-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'pairs': [{'id': 'S1', 'before': 10, 'after': 8},
           {'id': 'S2', 'before': 11, 'after': 10},
           {'id': 'S3', 'before': 9, 'after': 10},
           {'id': 'S4', 'before': 12, 'after': 9},
           {'id': 'S5', 'before': 10, 'after': None},
           {'id': 'S6', 'before': 8, 'after': 7}],
 'value_label': 'Measurement (a.u.)'}
render_chart("paired", data, "/tmp/paired-example")
```

**References:** [exact input](../examples/paired.json) · [editable SVG](../examples/paired.svg) · [PNG visual fallback](../examples/paired.png). All example values are synthetic.

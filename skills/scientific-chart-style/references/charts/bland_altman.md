# Bland–Altman agreement (`bland_altman`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use matched measurements to inspect agreement rather than only association. High correlation does not establish interchangeability. Compare limits with supplied scientific tolerances; a figure alone cannot decide acceptable agreement.

## Minimal inputs

`method_a` and `method_b` are equal-length finite complete paired vectors, at least two pairs for a sample SD. `value_unit` applies to both. State matching, independent unit and any repeated measurements; this simple reference does not adjust repeated pairs.

## Encoding and calculation

For each pair, x = (A+B)/2 and y = B−A. Bias is the mean difference; descriptive limits of agreement are bias ± 1.96 × sample SD (`ddof=1`) under an appropriate approximately normal, constant-spread difference model.

## Interpretation limits

These limits are not confidence limits for bias. Inspect trends and changing spread; transformations or repeated-measures limits need a justified analysis. Do not fabricate uncertainty bands or infer acceptable agreement from small bias alone.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart bland_altman --example --output-dir /tmp/bland_altman-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'method_a': [10, 12, 14, 16, 18, 20, 22, 24],
 'method_b': [10.2, 12.7, 14.1, 16.9, 18.3, 20.6, 22.2, 24.8],
 'value_unit': 'a.u.'}
render_chart("bland_altman", data, "/tmp/bland_altman-example")
```

**References:** [exact input](../examples/bland_altman.json) · [editable SVG](../examples/bland_altman.svg) · [PNG visual fallback](../examples/bland_altman.png). All example values are synthetic.

**Definition source:** [Bland and Altman, original paper](https://www-users.york.ac.uk/~mb55/meas/ba.htm).

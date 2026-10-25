# Count/share bars (`count_share`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use aligned bars for category counts, rates or shares. A horizontal layout accommodates longer names. For continuous distributions or effects, use observations or an estimate/interval instead of a mean-only bar.

## Minimal inputs

`categories` and nonnegative integer `counts` have equal lengths. Supply `denominator` as a nonnegative population count or `null`, `unit`, and `relationship`: `exclusive_exhaustive`, `overlapping` or `subset`. Counts and denominator use the same unit.

## Encoding and calculation

Bar length starts at zero. With a known positive denominator, share = count / denominator; a direct count · share label is useful when readable. Exclusive/exhaustive counts reconcile with the population. Subsets retain the full denominator; overlapping categories use separate bars and may total more than 100%.

## Interpretation limits

Unknown or zero population has no defined numerical share. Missing counts are not zero. Do not renormalize a displayed subset or stack overlapping flags as a composition. Retain neutral gray for a residual category.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart count_share --example --output-dir /tmp/count_share-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'categories': ['Category A', 'Category B', 'Other / unknown'],
 'counts': [50, 35, 15],
 'denominator': 100,
 'relationship': 'exclusive_exhaustive',
 'unit': 'records'}
render_chart("count_share", data, "/tmp/count_share-example")
```

**References:** [exact input](../examples/count_share.json) · [editable SVG](../examples/count_share.svg) · [PNG visual fallback](../examples/count_share.png). All example values are synthetic.

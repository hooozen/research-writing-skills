# Heatmap with missing cells (`heatmap`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use a heatmap for a supplied numerical matrix with meaningful row/column identities. A direct table may be clearer for very few values. Use a common color scale when comparing several panels.

## Minimal inputs

`values` is a rectangular matrix, with `null` for missing cells. Supply matching `row_labels`, `column_labels`, `value_label` and finite increasing `limits` for the color scale. Record normalization and aggregation provenance separately.

## Encoding and calculation

Map magnitudes to an ordered sequential scale and show a labeled colorbar. Preserve missing cells as distinct NA marks rather than zero. Annotate values when readable, choosing foreground text from actual background contrast. Small matrices remain editable vector cells.

## Interpretation limits

Do not rescale each row/panel silently, invent cell n, reorder by an undocumented clustering, or use a diverging map without a meaningful center. For signed effects, choose and document an appropriate centered diverging implementation.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart heatmap --example --output-dir /tmp/heatmap-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'values': [[0.58, 0.64, 0.71], [0.65, None, 0.77], [0.72, 0.79, 0.84]],
 'row_labels': ['Method A', 'Method B', 'Method C'],
 'column_labels': ['Set 1', 'Set 2', 'Set 3'],
 'value_label': 'Score (a.u.)',
 'limits': [0, 1]}
render_chart("heatmap", data, "/tmp/heatmap-example")
```

**References:** [exact input](../examples/heatmap.json) · [editable SVG](../examples/heatmap.svg) · [PNG visual fallback](../examples/heatmap.png). All example values are synthetic.

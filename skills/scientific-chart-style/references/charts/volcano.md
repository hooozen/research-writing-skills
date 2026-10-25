# Volcano plot (`volcano`)

[All chart types](../chart-index.md) · [Shared B/D style](../style-guide.md)

## Use and avoid

Use a volcano view for supplied per-feature effects and statistical evidence. It does not perform the underlying experimental test or prove a feature is biologically important. The plotted family and contrast must be identified.

## Minimal inputs

Supply matching `ids`, signed `log2_fold_change` and raw positive `pvalues`, plus explicit `adjusted_p_threshold` and `absolute_log2_effect_threshold`. The example inputs are synthetic estimates, not p-values inferred from invented expression observations.

## Encoding and calculation

The reference applies Benjamini–Hochberg over all supplied hypotheses, restores input order, and plots −log10(adjusted p) against log2 effect. Highlight only the stated joint effect/evidence criteria; use direction markers in print mode. The example thresholds are explicitly demonstrative.

## Interpretation limits

Do not feed already-adjusted q-values as raw p-values, silently change the tested family, or introduce default scientific thresholds. Zero/underflow values need an explicit plotting-floor policy; this minimal example uses strictly positive p-values.

## Run just this chart

Run from the skill directory; choose a task-workspace output directory. The temporary path below is a demonstration location.

```sh
python scripts/render_chart.py --chart volcano --example --output-dir /tmp/volcano-example
```

For real observations use `--input /path/to/task-data.json`; `--mode grayscale` selects D. Missing required data must not become synthetic evidence.

```python
import sys
sys.path.insert(0, "scripts")  # run from the skill directory
from render_chart import render_chart

data = {'synthetic': True,
 'ids': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
 'log2_fold_change': [0.1, 0.6, -1.6, 1.2, -0.2, 1.8, 0.4, -2.1],
 'pvalues': [0.8, 0.04, 0.001, 0.02, 0.6, 0.003, 0.25, 0.0004],
 'adjusted_p_threshold': 0.05,
 'absolute_log2_effect_threshold': 1}
render_chart("volcano", data, "/tmp/volcano-example")
```

**References:** [exact input](../examples/volcano.json) · [editable SVG](../examples/volcano.svg) · [PNG visual fallback](../examples/volcano.png). All example values are synthetic.

**Definition source:** [Bioconductor EnhancedVolcano reference](https://bioconductor.org/packages/release/bioc/manuals/EnhancedVolcano/man/EnhancedVolcano.pdf).

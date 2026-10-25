---
name: scientific-chart-style
description: "Create or restyle publication-oriented scientific charts across disciplines. Locate one of 19 chart references, read only its input/definition/example, and render a selected chart with editable exports. Use muted teal/terracotta by default and a designed grayscale print mode."
---

# Scientific Chart Style

Use the approved **B muted teal/terracotta** palette by default and **D grayscale** for black-and-white print. Preserve source evidence and target-journal requirements. This skill supports scientific charts across disciplines.

## Start with the requested chart

Open the [19-chart index](references/chart-index.md) and select the row matching the scientific question and available data. Each row links directly to a short chart card, minimal JSON input, individual SVG and PNG. The [JSON index](references/chart-index.json) exposes the same mapping for programmatic lookup; reading both indexes is unnecessary.

1. Read **only the selected chart card** for when to use it, required fields, statistical definition, limitations and a short runnable example. Follow its linked methodological source only when needed. Do not read both long galleries or every chart card to make one plot.
2. Read the [shared style guide](references/style-guide.md) when creating or restyling the figure. It owns palette, physical-point typography, spacing and export settings. Read [publication references](references/publication-references.md) only when adapting to a named publication or checking a submission requirement. Target-journal instructions override visual defaults.
3. Use the individual SVG for editable geometry/style and the individual PNG for convenient visual inspection. A renderer may not display SVG directly; do not assume that reading SVG XML provides a visual inspection or a statistical definition. The nine-panel contact sheets are optional browsing aids, not required context.
4. Use supplied observations or supported summaries. Identify units, grouping/pairing, missingness and the comparison/reference. If a required field is absent, obtain it or use an appropriate simpler encoding. Never reconstruct individual data, quartiles, densities, pairing, intervals or censoring from insufficient aggregates.

## Render one chart

The optional [single-chart runner](scripts/render_chart.py) accepts the minimal input described by each card. Set `SKILL_DIR` to this installed skill's actual directory and `TASK_DIR` to the task workspace; write outputs in the task workspace, not inside the installed skill.

```sh
# List available chart IDs without generating figures.
python "$SKILL_DIR/scripts/render_chart.py" --list

# Plot supplied data; only the chosen chart is generated.
python "$SKILL_DIR/scripts/render_chart.py" --chart roc \
  --input "$TASK_DIR/data.json" --output-dir "$TASK_DIR/figures/roc"

# Explicitly requested synthetic demonstration; never a fallback for missing data.
python "$SKILL_DIR/scripts/render_chart.py" --chart roc --example \
  --output-dir "$TASK_DIR/figures/roc-example"
```

Use `--mode grayscale` for D and `--formats svg,png,pdf` when PDF is needed; individual cards also show short Python calls. Without `--input` or explicit `--example`, the runner must not generate sample data. Keep synthetic flags and limitations in the output. The data/statistics/export records belong to the selected chart, not an unrelated atlas.

The runner is a reference implementation, not a requirement to use Python or a general statistical analysis service. Use the user's existing R, JavaScript or other capable tool when appropriate, translating the selected card's meaning and shared visual rules. Use task-specific implementation when the runner's documented input subset does not cover the design; do not force incompatible data into an example schema. Reuse shared style/statistical helpers rather than copying a full gallery or nineteen separate style implementations.

## Scientific and visual checks

- Match the encoding to the question: observations/distributions for spread, effects and justified intervals for comparisons, counts/rates for bars. Retain a zero origin for bar lengths, actual time spacing, actual pair IDs, explicit denominators and missing values.
- Define what a point represents, n and the dependence unit. State whether uncertainty is SD, SE, confidence/prediction interval or limits of agreement. Do not add unsupported intervals, significance stars, causal claims or conclusions of module contribution.
- Keep group identities stable across related figures. D needs marker, line or hatch distinctions in addition to tonal differences. For quantitative matrices use an appropriate shared sequential/diverging scale and explicit missing cells.
- Set final physical size before composing. Fonts are points, not pixels scaled by export DPI; reflow a single-column figure rather than shrinking a double-column figure's labels. Use white backgrounds, readable labels and measured spacing without decorative cards.
- Retain editable vector text/geometry when suitable, embed PDF fonts and provide a PNG for visual QA when needed. Inspect the actual final render, including legends, colorbars, neighboring panels and glyphs; a valid SVG or a passing numerical test is not proof of visual readability.
- Captions identify measure, population, units, n/denominator, reference, uncertainty method and source. Keep long interpretation outside the data rectangle. Save report figures in `figures/` with meaningful alt text and relative links, and keep exact data/derived values traceable.

## Optional background and maintenance

The [basic background](references/scientific-chart-examples.md) and [advanced background](references/advanced-chart-guide.md) contain broader comparisons and methodological sources. The old [basic gallery](scripts/scientific_chart_gallery.py) and [advanced gallery](scripts/advanced_chart_gallery.py) remain reproducible atlas examples; a single chart uses the direct runner above.

When maintaining this skill, use [scripts/build_chart_references.py](scripts/build_chart_references.py) to rebuild the index and individual reference figures from their recorded inputs, then run it with `--check`. The manifest ties reference inputs and SVG/PNG files to generator sources. Do not rebuild or load all nineteen references during an ordinary plotting task. HTML or contact sheets may be generated for human browsing; the Agent's primary route remains the text index and selected chart card.

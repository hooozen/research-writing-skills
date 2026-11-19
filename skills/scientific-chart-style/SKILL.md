---
name: scientific-chart-style
description: "Create or restyle publication-quality scientific charts in any discipline. Pick one of 19 chart types from an index, read only that chart's card (inputs, statistical definition, example), and render it with editable SVG/PDF and PNG exports. Saturated blue palette by default, with a purpose-built grayscale mode for print."
---

# Scientific Chart Style

Default look: white background, saturated blue `#1464D2` as the first series, dark orange and purple for the next two, physical-point typography. Use `--mode grayscale` for black-and-white print; it's a designed mode with distinct markers and line styles, not a desaturated screenshot. A target journal's instructions always override these defaults.

## 1. Find the chart

Open the [chart index](references/chart-index.md) and pick the row whose question matches the user's question and data. Each row links to a short card, a minimal JSON input, and an SVG/PNG preview. [chart-index.json](references/chart-index.json) has the same mapping for scripts; you don't need both.

1. Read **only the chosen card**: when to use it, required fields, how it's calculated, what it can't show, and a runnable example. Don't read every card or the long background guides to make one plot.
2. Read the [style guide](references/style-guide.md) when creating or restyling a figure. It owns colors, type sizes, spacing and export. Read [publication-references.md](references/publication-references.md) only for a named journal.
3. Look at the card's PNG to see the intended result. Reading SVG source is not a visual check.
4. Work from the user's observations or valid summaries. Know the units, grouping, pairing, missing values and the reference being compared against. If a required field is missing, ask for it or use a simpler chart the data do support. Never reconstruct raw points, quartiles, densities, pairs, intervals or censoring from summaries.

## 2. Render it

[scripts/render_chart.py](scripts/render_chart.py) draws one chart from the card's input format. Set `SKILL_DIR` to this skill's installed directory and `TASK_DIR` to the user's workspace; write output to the workspace, never into the skill.

```sh
# List chart IDs.
python "$SKILL_DIR/scripts/render_chart.py" --list

# Plot the user's data.
python "$SKILL_DIR/scripts/render_chart.py" --chart roc \
  --input "$TASK_DIR/data.json" --output-dir "$TASK_DIR/figures/roc"

# Synthetic demo, only when the user asks for one.
python "$SKILL_DIR/scripts/render_chart.py" --chart roc --example \
  --output-dir "$TASK_DIR/figures/roc-example"
```

Add `--mode grayscale` for print and `--formats svg,png,pdf` when PDF is needed. Without `--input` or `--example` the runner refuses to plot, so missing data never turns into demo data. Synthetic outputs stay labeled as synthetic.

The runner is a reference implementation, not a requirement. If the user works in R, JavaScript or another tool, apply the card's definitions and the style guide there. If the design goes beyond the runner's input format, write task-specific code that reuses the shared helpers rather than forcing the data into the example schema.

## 3. Check the result

- **Right chart for the question.** Observations and distributions for spread; estimates with justified intervals for comparisons; bars for counts and rates. Bars start at zero, time keeps its real spacing, pairs keep their real IDs, denominators and missing values stay visible.
- **Honest statistics.** Say what a point is, the n, and the unit of independence. Say whether error bars are SD, SE, a confidence or prediction interval, or limits of agreement. No unsupported intervals, significance stars or causal claims.
- **Consistent identities.** A group keeps its color across related figures. Grayscale needs marker, line or hatch differences, not just tone. Matrices use one shared sequential or diverging scale and mark missing cells explicitly.
- **Final size first.** Set the physical size before laying out. Fonts are points, not pixels scaled by DPI. For a single column, reflow rather than shrinking a double-column figure.
- **Look at the render.** Inspect the actual PNG or PDF at final size, including legends, colorbars, neighboring panels and CJK glyphs. A valid SVG or a passing test isn't proof it reads well.
- **Complete caption.** Measure, population, unit, n or denominator, reference, uncertainty method and source. Long interpretation goes in the caption or text, not inside the plot. Report figures live in `figures/` with alt text and relative links.

## Background and maintenance

[scientific-chart-examples.md](references/scientific-chart-examples.md) and [advanced-chart-guide.md](references/advanced-chart-guide.md) compare related chart types and cite methodological sources; read them only when choosing between methods. The gallery scripts ([basic](scripts/scientific_chart_gallery.py), [advanced](scripts/advanced_chart_gallery.py)) reproduce the overview sheets; single charts use the runner above.

Maintainers rebuild the index and previews with [scripts/build_chart_references.py](scripts/build_chart_references.py) and verify with `--check`. An ordinary plotting task never rebuilds them.

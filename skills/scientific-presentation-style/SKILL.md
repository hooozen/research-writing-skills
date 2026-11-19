---
name: scientific-presentation-style
description: "Build scientific PowerPoint slides in the scientific-chart-style look: white canvas, saturated blue/orange/purple, projection-size type, and editable native charts, tables and plot geometry that keep their statistical meaning. Use for research presentations and chart- or table-focused PPT requests; not for journal figure sizing or unrelated slide branding."
---

# Scientific Presentation Style

Slides use the same visual system as the publication charts (white canvas, blue `#1464D2`, dark orange `#B64B00`, purple `#7A3DB8`, dark text, restrained axes), with type sized for a projector. Never paste a 7 pt journal figure onto a slide. An existing deck or a requested template always takes priority over these defaults.

## 1. Pick the workflow

- **New deck:** 16:9. Use [assets/design-tokens.json](assets/design-tokens.json) and read [references/presentation-design.md](references/presentation-design.md) for colors, type sizes, layout and editability.
- **Destination:** use the presentation tool and destination the environment provides. In an Artifact Session, edit the bound `presentation` and keep its artifact reference; a saved Spaces deck can be downloaded as `.pptx`. Don't create a separate file or cloud deck to get around the destination.
- **Editing one chart in an existing deck:** restyle that chart only. Keep the surrounding theme, text and positions unless asked.
- **Editability:** default to native, editable evidence. Know which kind you're delivering: a data-bound native chart, editable shapes that must be regenerated when data change, or a static picture. A picture is never an editable dataset.

## 2. Pick and preserve the chart

Read only the relevant row of [references/chart-mapping.md](references/chart-mapping.md), which maps all 19 chart types to a PowerPoint representation and the data each needs. If `scientific-chart-style` is installed, its chart card gives the statistical definition; it's optional.

Don't invent observations, intervals, quartiles, densities, pairs, censoring or test results to fill a layout. [assets/example-data.json](assets/example-data.json) is for an explicitly requested demo only, and its slides stay visibly labeled synthetic.

Keep units, n, denominators, signs, real time spacing, missing values, reference lines, category order and uncertainty definitions. Bars start at zero. Missing cells look different from low values. Step curves keep their steps; don't smooth them or put real times on an evenly spaced category axis.

## 3. Write the slides

For a full research talk, settle the question, approach, evidence and conclusion before laying out slides, and follow the user's outline. A tour of chart types is a template, not a talk.

- **Title states the point.** "Quality filtering raised validation accuracy from 75% to 80%" beats "Results". Keep it to one or two lines.
- **One message per slide.** One main plot, or two that genuinely belong together, plus one caption with the evidence details. The plot is the largest thing on the slide.
- **Plain words.** Same terminology as the report, new concepts introduced by what they do. No slogans or buzzwords (see the research-progress-report writing guide if it's installed).
- **Native elements.** Use the chart's own title, axes, legend and labels instead of overlaid text boxes. For custom plots, draw native paths, lines, markers and text through one coordinate transform. Put full source data in the notes or a companion file.
- **Tables for exact values.** Read [references/tables.md](references/tables.md). Labels left, numbers right, units in headers, consistent precision, missing values explained, highlights explained. A heatmap doesn't replace a requested table.

[scripts/slide-builders.mjs](scripts/slide-builders.mjs) is an optional Artifact Tool adapter that builds count bars, time-series lines, scatter, two-group box plots, paired plots, intervals, heatmaps, ROC/PR, native tables, a style page, a grayscale example and an empty plot layout. Read [references/authoring-adapter.md](references/authoring-adapter.md) only when using it. Any capable PowerPoint tool can follow the same rules.

What updates by itself and what doesn't: native bar and XY charts keep their data. Count/share labels are text, so refresh them when counts or denominators change. Box plots, paired plots, intervals and heatmaps are drawn shapes with data in the notes; editing a shape recalculates nothing, so rebuild them from new data.

## 4. Check the deck

- Render every slide at presentation size. Check CJK glyphs, labels, axes, legends, captions, contrast and overlaps. Reflow a crowded slide before shrinking type.
- Compare native chart series, x values, category order and number formats with the source. Drawn plots keep their real coordinates, all observations and interval endpoints.
- Check every table cell against the source: denominators, totals, percent vs. percentage points, precision, units, missing-value meanings, highlighted rows. Table cells don't recalculate.
- State honestly what's editable: native chart, editable shapes or picture. A preview doesn't prove PowerPoint behavior.
- If exporting PPTX is part of the workflow, validate chart data, native objects, fonts and slide size there. Test in PowerPoint only if it's available, and say so if it wasn't.
- Template examples stay labeled synthetic. In a real deck, replace all example data and captions and delete unused layouts.

---
name: clinical-data-chart-style
description: "Create or restyle static clinical, medical-imaging, OCT/OCTA, and healthcare data charts with consistent blue/gray evidence panels. Use for counts, distributions, relationships, repeated measurements, and statistical comparisons; preserve units, denominators, uncertainty, and source data."
---

# Clinical Data Chart Style

Apply one implementation-neutral visual system to clinical-data charts, especially figures embedded in Markdown reports.

## Workflow

1. Preserve the source data. Create a derived table with categories, values, units, and explicit denominators where shares are shown. Identify whether categories are exclusive, overlapping, or a displayed subset; do not assume their sum is the population.
2. Read [references/style-guide.md](references/style-guide.md) completely before creating, restyling, or reviewing charts.
3. Choose the plotting language and library from the user's environment and existing project. Do not require Matplotlib, Python, or any other specific implementation.
4. Translate the style guide's tokens and composition rules into the selected tool without changing their visual meaning.
5. Choose the encoding from the analytical question. For categorical bars with short readable labels, start with a vertical layout. Use horizontal bars when long labels, crowded categories or ranked values are easier to read that way; decide from the actual labels and available space, not a fixed category-count cutoff. Preserve meaningful clinical, anatomical, or temporal order.
6. Prefer SVG for Markdown, with high-resolution PNG as a compatibility fallback. Save figures in a `figures/` directory beside the report and use relative links.
7. Verify every plotted value, denominator, percentage, label, title, source note, and rendered figure before finishing.

## Implementation choice

The VI specification is authoritative; implementation examples are not. Apply it with Matplotlib, Plotly, Altair, Vega-Lite, R/ggplot2, JavaScript, native office charts, or another capable renderer.

If Matplotlib is already appropriate, use [scripts/matplotlib_example.py](scripts/matplotlib_example.py) as a translation example. Copy its style decisions into task-specific plotting code; do not force its sample data or chart type onto the task.

Embed report figures with meaningful alt text:

```markdown
![Distribution of image modalities, with counts and shares](figures/modality.svg)
```

## Rules

- Maintain clear spacing between chart elements and prevent inappropriate overlap, occlusion, or clipping; apply the spacing and rendered-output checks in [references/style-guide.md](references/style-guide.md). Intentional layering is acceptable only when it preserves readability and data meaning.
- For count-and-share bars, show `count · share` directly on each bar using one decimal place for shares and thousands separators for counts. State the denominator and its unit; when it is unknown or zero, show the count with “share unavailable”, never a made-up percentage.
- For means, rates, changes, or intervals, label the actual metric and unit, and specify uncertainty when supplied. Do not convert continuous outcomes or signed changes to counts or percentages. A single series needs no legend.
- Treat `Other`, `Unknown`, `Missing`, and similar residual categories as neutral gray.
- Do not use 3D, decorative gradients, shadows, decorative icons, or rainbow palettes. Continuous color scales in heatmaps and restrained gridlines that support quantitative reading are valid data encodings.
- Do not use pie or donut charts when bars make comparison clearer.
- Write a conclusion-led title when the figure stands alone; use a descriptive metric title inside a multi-figure report section.
- Reserve a title region before sizing the plot. The entire title and subtitle must sit inside the card with padding, or wholly above it with a clear gap; no text may straddle the gray/white boundary. Follow the title-layout and export checks in the style guide.
- Keep a vector artifact when supported. Also provide PNG when the user requests it or the target renderer needs it.
- Use synthetic values only for an explicitly requested demonstration, and label them on the figure. Otherwise missing values require a specification or an incomplete table, not fabricated observations.

## Additional chart types

For box/violin plots, scatter plots, time series, histograms, ECDFs, paired observations, intervals, or heatmaps, read the relevant section of [references/scientific-chart-examples.md](references/scientific-chart-examples.md). It explains which data and statistical definitions each encoding needs and shows one compact visual overview.

Use axes and a few meaningful labels for dense observations; do not force the count/share labeling pattern onto them. Identify the observation unit, missing-data handling, and any uncertainty encoding. Preserve pairing and actual time spacing. Do not invent clinical interpretation or statistical significance.

When an executable example would help and Matplotlib fits the environment, use [scripts/scientific_chart_gallery.py](scripts/scientific_chart_gallery.py). It generates synthetic figures and exact data in an explicit output directory. Load or run only what the task needs; the gallery does not make Python a requirement for this skill.

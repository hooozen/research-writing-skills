---
name: clinical-data-chart-style
description: "Create or restyle static clinical, medical-imaging, OCT/OCTA, and healthcare data charts with consistent blue/gray evidence panels. Use for counts, distributions, trends, and statistical comparisons in reports; preserve the metric, denominator, uncertainty, and source data."
---

# Clinical Data Chart Style

Apply one implementation-neutral visual system to clinical-data charts, especially figures embedded in Markdown reports.

## Workflow

1. Preserve the source data. Create a derived table with categories, values, units, and explicit denominators where shares are shown. Identify whether categories are exclusive, overlapping, or a displayed subset; do not assume their sum is the population.
2. Read [references/style-guide.md](references/style-guide.md) completely before creating, restyling, or reviewing charts.
3. Choose the plotting language and library from the user's environment and existing project. Do not require Matplotlib, Python, or any other specific implementation.
4. Translate the style guide's tokens and composition rules into the selected tool without changing their visual meaning.
5. Choose the encoding from the analytical question. For categorical bars, use horizontal bars for long labels or more than four categories; vertical bars suit two to four short labels. Preserve meaningful clinical, anatomical, or temporal order.
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

- For count-and-share bars, show `count · share` directly on each bar using one decimal place for shares and thousands separators for counts. State the denominator and its unit; when it is unknown or zero, show the count with “share unavailable”, never a made-up percentage.
- For means, rates, changes, or intervals, label the actual metric and unit, and specify uncertainty when supplied. Do not convert continuous outcomes or signed changes to counts or percentages. A single series needs no legend.
- Treat `Other`, `Unknown`, `Missing`, and similar residual categories as neutral gray.
- Do not use 3D, gradients, shadows, decorative icons, dense gridlines, or rainbow palettes.
- Do not use pie or donut charts when bars make comparison clearer.
- Write a conclusion-led title when the figure stands alone; use a descriptive metric title inside a multi-figure report section.
- Keep a vector artifact when supported. Also provide PNG when the user requests it or the target renderer needs it.
- Use synthetic values only for an explicitly requested demonstration, and label them on the figure. Otherwise missing values require a specification or an incomplete table, not fabricated observations.

## Additional chart types

For time series, paired comparisons, or statistical intervals, reproduce the design tokens and hierarchy in the style guide using an appropriate implementation. Keep direct labeling and restrained blue/gray encoding. Do not invent clinical interpretation or statistical significance.

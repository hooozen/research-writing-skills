---
name: clinical-data-chart-style
description: "Specify, create, and restyle consistent clinical, medical-imaging, OCT, OCTA, and healthcare data charts for Markdown reports and other static deliverables, independently of programming language or visualization library. Use when an agent needs distribution charts, count-and-share graphics, modality/layer/scan-size summaries, report figures, implementation guidance, or visual QA that should follow the Clinical Imaging Data Brief visual system: white canvas, light-gray evidence cards, black typography, muted-gray annotations, blue data accents, and direct count-plus-percentage labels."
---

# Clinical Data Chart Style

Apply one implementation-neutral visual system to clinical-data charts, especially figures embedded in Markdown reports.

## Workflow

1. Preserve the source data. Create a small derived table for each figure with categories, values, and an explicit denominator where shares are shown.
2. Read `references/style-guide.md` completely before creating, restyling, or reviewing charts.
3. Choose the plotting language and library from the user's environment and existing project. Do not require Matplotlib, Python, or any other specific implementation.
4. Translate the style guide's tokens and composition rules into the selected tool without changing their visual meaning.
5. Use horizontal bars for long labels or more than four categories. Use vertical bars for two to six short categories.
6. Prefer SVG for Markdown, with high-resolution PNG as a compatibility fallback. Save figures in a `figures/` directory beside the report and use relative links.
7. Verify every plotted value, denominator, percentage, label, title, source note, and rendered figure before finishing.

## Implementation choice

The VI specification is authoritative; implementation examples are not. Apply it with Matplotlib, Plotly, Altair, Vega-Lite, R/ggplot2, JavaScript, native office charts, or another capable renderer.

If Matplotlib is already appropriate, use `scripts/matplotlib_example.py` as a translation example. Copy its style decisions into task-specific plotting code; do not force its sample data or chart type onto the task.

Embed report figures with meaningful alt text:

```markdown
![Distribution of image modalities, with counts and shares](figures/modality.svg)
```

## Rules

- Show `count · share` directly on every bar; do not require a legend for a single series.
- Use one decimal place for shares and thousands separators for counts.
- Treat `Other`, `Unknown`, `Missing`, and similar residual categories as neutral gray.
- Do not use 3D, gradients, shadows, decorative icons, dense gridlines, or rainbow palettes.
- Do not use pie or donut charts when bars make comparison clearer.
- Write a conclusion-led title when the figure stands alone; use a descriptive metric title inside a multi-figure report section.
- Keep a vector artifact when supported. Provide PNG only when the target Markdown renderer cannot display SVG.

## Additional chart types

For time series, paired comparisons, or statistical intervals, reproduce the design tokens and hierarchy in `references/style-guide.md` using an appropriate implementation. Keep direct labeling and restrained blue/gray encoding. Do not invent clinical interpretation or statistical significance.

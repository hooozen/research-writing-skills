---
name: scientific-chart-style
description: "Create or restyle publication-oriented scientific charts across disciplines. Use muted teal/terracotta by default and a designed grayscale print mode; specify statistical encodings, final-size typography, uncertainty, and editable exports. Covers distributions, comparisons, relationships, model evaluation, agreement, survival, and high-dimensional data."
---

# Scientific Chart Style

Create clear scientific figures for papers, supplements and research reports across disciplines. Preserve evidence and use the user's approved visual system: **B, muted teal/terracotta, by default; D, designed grayscale, for black-and-white print.** This skill replaces `clinical-data-chart-style`; its scope includes clinical work without being limited to it.

## Workflow

1. Identify the question, observation/independence unit, available raw data or summaries, grouping/pairing, units and intended comparison. Preserve source data and missingness. Use already supplied settings; do not repeat intake. Synthetic values are permitted only for an explicitly requested demonstration and must be labeled on the figure and in its data.
2. Read [references/style-guide.md](references/style-guide.md) for visual tokens, final physical size, color and grayscale modes, typography, spacing and export requirements. A specified target journal overrides these default design parameters; use [references/publication-references.md](references/publication-references.md) to locate primary guidance. Do not describe one palette or font size as a universal journal requirement.
3. Choose an encoding from the scientific question and data. Read the relevant sections of [references/scientific-chart-examples.md](references/scientific-chart-examples.md) for distributions, associations, repeated observations, intervals and matrices. Read [references/advanced-chart-guide.md](references/advanced-chart-guide.md) for raincloud/estimation plots, ROC/PR, calibration, confusion matrices, Bland–Altman, survival, volcano and PCA. Load only the needed sections.
4. Make a traceable derived table with the plotted observations/aggregates, units, sample counts, denominators, transformations, statistical definitions and any exclusions. Do not manufacture quartiles, densities, paired records, intervals, p-values, censoring or individual outcomes from insufficient summaries.
5. Use the plotting language/library appropriate to the user's project. The specification is authoritative; Python examples are optional translations, not a runtime requirement. Preserve the same visual meaning in R/ggplot2, Matplotlib, Plotly, Vega-Lite or other capable tools.
6. Compose at the intended physical size. Align panels and consistent axis/legend roles, retain readable text and distinguish series with shape/line style as well as color. Move long prose to captions. Use statistical definitions and detail that let another reader interpret the figure correctly.
7. Export vector PDF/SVG when suitable, plus a PNG preview when needed. Retain editable text and embed PDF fonts. Render and inspect the final exports at intended size; compare both default and print modes when both are requested. Verify values, labels, intervals, denominators, links and clipping before delivery.

## Core decisions

- Use **color** unless the user requests grayscale or black-and-white printing. For grayscale, apply D's explicit tones plus marker/line/hatch distinctions; a desaturated screenshot is insufficient. Keep group identities consistent across related figures.
- For continuous group comparisons, show observations or distributions and estimates/intervals when supported. A bar of a mean alone conceals spread. Use bars for counts, rates or meaningful aggregated quantities, with a zero origin for bar lengths. Choose orientation from label readability and meaningful order, not an arbitrary category-count rule.
- Preserve actual time spacing and actual pairing; identify repeated observations and independent units. Do not connect unordered categories or independently sampled people as trajectories. Label interpolation, smoothing, fitted models and their uncertainty explicitly.
- Define error bars and bands: SD, SE, confidence interval, prediction interval and limits of agreement answer different questions. State n, analysis unit, interval method and dependence structure where relevant. Do not derive statistical significance or module contribution from visual appearance.
- Name the reference and direction for differences; distinguish relative percentages from percentage-point changes. Use a zero reference for additive effects and a reference of one, often on a log axis, for ratios.
- For counts/shares, show direct count/share labels when readable, specify the denominator and its unit, and preserve exclusive/overlapping/subset relationships. Unknown or zero denominators have no defined share; missing is not zero. Never force count/share labels onto continuous outcomes.
- Use neutral gray for residual/missing categories. Sequential and diverging color scales must reflect the quantity and a shared meaningful range. Mark missing cells separately, keep annotations legible and show a colorbar; do not silently normalize each row or panel.
- Avoid decorative cards, shadows, gradients unrelated to data, 3D, rainbow scales and unnecessary chart furniture. Do not use pie/donut charts where aligned bars reveal the comparison more clearly. A quantitative heatmap or density scale is a valid use of a gradient.
- Do not add significance stars, causal wording, extrapolated survival tails or machine-learning performance claims unsupported by the supplied analysis. Preserve negative and uncertain results.

## Reference implementations and examples

When Matplotlib is appropriate, use these optional scripts or adapt their decisions:

- [scripts/matplotlib_example.py](scripts/matplotlib_example.py): shared B/D tokens, physical-point typography, white figure/header layout and a count/share example. Supports SVG, PNG and PDF.
- [scripts/scientific_chart_gallery.py](scripts/scientific_chart_gallery.py): nine basic scientific encodings, raw/derived data and color/print examples.
- [scripts/advanced_chart_gallery.py](scripts/advanced_chart_gallery.py): nine further examples with explicit computational definitions and statistical limits.

The galleries produce labeled synthetic examples, exact data/statistics and export manifests. Run only the relevant example or gallery for the task; an ordinary chart does not require generating an entire atlas. The [basic reference preview](references/scientific-chart-preview.png) and [advanced reference preview](references/advanced-chart-preview.png) illustrate the system; they are not a source of real research results.

## Figure delivery

Keep a figure's question, metric, population, units, n/denominator, uncertainty meaning and source clear in its caption or adjacent report text. Use short descriptive panel titles when needed, lower-case panel letters for multi-panel figures, and a separate manuscript caption for long interpretation. A standalone report figure may have a concise conclusion-led title when the evidence supports it.

Save figures in `figures/` beside a report with meaningful alt text and relative links. Retain raw/derived data and an analysis/export record when practical. Check actual exported artwork after changing font, size, labels or backend; automatic layout and a valid file do not establish readability. Deliver only supported conclusions and identify missing inputs or unverified rendering honestly.

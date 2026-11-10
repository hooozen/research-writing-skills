---
name: scientific-presentation-style
description: "Create scientific PowerPoint or slide templates and figures with the high-contrast scientific-chart-style visual system. Adapt typography for projection, preserve statistical meaning, and use editable native charts or slide geometry. Use for research presentations and chart-focused PPT requests, not journal-figure sizing or unrelated slide branding."
---

# Scientific Presentation Style

Translate the scientific chart system into readable presentation slides: white canvas, saturated blue, dark orange and purple, dark text, restrained axes, direct units and honest evidence. Keep the user's existing deck or requested template authoritative. A scientific chart on a slide needs presentation-size typography; do not paste a publication figure with unreadable 7 pt labels.

## Choose the workflow

- For a new deck, default to a 16:9 canvas. Use [assets/design-tokens.json](assets/design-tokens.json) and read [references/presentation-design.md](references/presentation-design.md) for colors, physical-point sizes, spacing, plot frames and editability rules.
- Use the installed presentation-authoring workflow and its requested destination. In an Artifact Session, author the existing bound `presentation` and preserve its exact artifact reference. A saved Spaces presentation can be exported to PowerPoint by the user. Do not create a separate file or unrelated cloud deck to bypass the destination's rules.
- For a focused chart edit, preserve the surrounding theme, text and geometry unless their change is requested. Apply local chart styling rather than replacing the entire deck theme.
- Identify whether the user needs data-bound native charts, editable vector geometry, or a static supplied figure. Default to native editable evidence. State when a geometric chart requires regeneration after data changes; a picture or SVG image is not an editable chart dataset.

## Select and preserve the chart

Read only the relevant row of [references/chart-mapping.md](references/chart-mapping.md). It maps the 19 scientific chart types to suitable PowerPoint representations and the data each needs.

Use `scientific-chart-style` when available for the selected chart's statistical definition, data requirements and original figure conventions. It is a companion, not a mandatory dependency: the mapping and design rules here remain usable independently. Do not invent observations, intervals, quartiles, density, pairing, censoring or test results to fill a template. Use [assets/example-data.json](assets/example-data.json) only for an explicitly requested demonstration/template example and retain the visible synthetic disclosure.

Preserve observation units, n, denominators, signs, actual time spacing, missingness, reference values, category order and uncertainty definitions. Retain a zero origin for bars. Keep missing cells distinct from low values. Lines that represent steps must retain the step coordinates; a smoothed curve or equally spaced category axis can change scientific meaning.

## Build slides with editable evidence

For a full research deck, establish the question, overall approach, available evidence and conclusion before expanding details. Follow a supplied outline. A gallery of chart types is a template, not the narrative of a real report. Use stable terminology, explain a new concept through its role, and keep titles and explanations in plain language.

Use a clear title, one main plot or a genuinely related pair, and one evidence caption. Keep the plot larger than its surrounding explanation. Use native chart titles, axes, legends and labels rather than overlaying duplicate text boxes. For custom scientific plots, use native paths, lines, markers and text with a shared coordinate transform. Keep complete source data in notes or a companion data file.

The optional [scripts/slide-builders.mjs](scripts/slide-builders.mjs) is an Artifact Tool adapter. It creates counts, numeric-time lines, scatter, two-group box plots, paired observations, intervals, heatmaps and ROC/PR panels, plus a style page, grayscale example and empty plot layout. Read [references/authoring-adapter.md](references/authoring-adapter.md) only when using this implementation. Other capable PowerPoint tools can apply the same specification.

Native bar and XY charts retain their series/category values. The count/share labels are custom text: regenerate those labels when counts or denominators change, even if the bars update from edited data. Boxes, paired plots, intervals and heatmaps in this adapter are editable slide geometry with source data in notes; editing a shape does not recalculate its statistics. Rebuild those plots from updated data. For unsupported chart designs, use the mapping and the selected chart's definition rather than forcing the data into a sample layout.

## Verify the presentation

- Render and inspect every slide at presentation size. Check CJK glyphs, labels, axes, legends, captions, contrast and unintended overlap. Reflow a crowded plot before reducing its fonts.
- Inspect native chart series, x coordinates, category order and number formats against source data. Confirm geometric plots retain their actual coordinates, complete observations and interval endpoints.
- Check the actual editability class: a native chart, editable shapes, and an embedded image are different deliverables. Do not claim that geometry is data-bound or that a preview proves PowerPoint editing behavior.
- When exporting a PPTX is part of the authoring route, validate chart data/workbook references, native objects, fonts and slide size using that workflow. Test in PowerPoint only when available, and report unavailable application checks accurately.
- Keep any template example marked synthetic. For real reports, replace example data and captions with the user's evidence, preserve the distinction between observations and interpretations, and remove unused layouts.

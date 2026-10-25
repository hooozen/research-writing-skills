# Scientific Chart Style Guide

This implementation-neutral system uses the approved **B color palette** by default and **D grayscale** for black-and-white print. Apply it across scientific disciplines, preserving the question, statistical meaning and source data. A user's target-journal instructions take priority over these design defaults. See [publication-references.md](publication-references.md) for primary guidance and its scope.

## Color and print tokens

| Role | B: default color | D: grayscale print | Meaning |
|---|---|---|---|
| Canvas and plot background | `#FFFFFF` | `#FFFFFF` | White, no rounded card, border or shadow |
| First series / focal series | `#547F7E` | `#34383C` | Muted teal / dark graphite |
| Second series | `#AE766A` | `#70767B` | Muted terracotta / medium graphite |
| Third series | `#9B895B` | `#92989E` | Muted ochre / lighter graphite |
| Other, unknown or missing | `#8B9197` | `#B7BCC0` | Neutral residual; missing remains distinct from zero |
| Main text | `#24282C` | `#24282C` | High-contrast labels and numerical text |
| Secondary notes | `#626B73` | `#626B73` | Captions/notes that remain legible |
| Axis lines | `#34383C` | `#34383C` | Thin reference geometry |

Assign colors by meaning and retain assignments across a figure series. One series often needs just one color. For more than three groups, first consider small multiples or direct labels; if extra hues are necessary, extend the muted palette deliberately and check distinctness at final size. Do not silently recycle three colors for six different identities. Never imply that red/green or warm/cool conveys risk, significance or direction without defining it.

Pair group identity with redundant channels: circle/square/triangle, solid/dashed/dotted lines, direct labels, and sparse hatching when useful for bars. D uses these deliberately; do not merely convert B to grayscale. Use adequate point/line contrast against white, and retain outlines for pale fills. Thin gray lines must still survive normal printing. Low saturation does not justify low contrast.

For ordered values, use a perceptually ordered light-to-dark sequential scale; a light neutral to the teal endpoint is the default example. Use a teal–light neutral–terracotta diverging scale only for a meaningful midpoint, with explicit centered limits when scientifically appropriate. Keep the range common across comparable panels. A change in color should reflect a change in value; avoid rainbow, cyclic or categorical scales for ordinary continuous magnitudes. A low-density background is not missing data. Select annotation text from the actual cell/background contrast rather than a fixed numeric threshold.

[B color examples](scientific-chart-preview.png) · [D print examples](scientific-chart-print-preview.png). These are labeled synthetic references.

## Physical size and typography

Set the intended final width before plotting. About **89 mm** for a single column and **180–183 mm** for a double column are useful design starting points, not universal journal dimensions. Use the specified journal's dimensions when known. A double-column figure reduced to half width also halves its text; reflow it for a single column rather than relying on a high DPI to repair tiny labels.

| Element | Preview/default starting point at final size |
|---|---|
| Font | Arial, Helvetica or a suitable installed sans-serif; Noto Sans/DejaVu Sans are portable alternatives |
| Axis labels and ordinary annotations | 7 pt, regular |
| Tick labels / compact legends | 6.5–7 pt, adjusted to the actual target and readability |
| Panel letters | 8 pt, bold, lower-case (`a`, `b`, `c`) |
| Small descriptive panel title | About 7 pt; avoid a large report-style heading inside the plot |
| Axes / tick strokes | About 0.6 pt |
| Data lines / interval strokes | About 0.8–1.1 pt, stronger only when needed |
| Markers | Roughly 2.5–4 pt; density and output size determine the actual choice |

These are physical points, **not pixels divided by output DPI**. Raising PNG DPI changes sampling, not the intended printed font size. Use normal letter spacing and consistent sentence case; do not stretch text, outline every label, or use bold for every number. Mathematical symbols, Greek letters, subscripts and units need an installed font that covers them. For Chinese, use a CJK font such as Noto Sans CJK SC/PingFang SC where available and inspect actual glyphs; record a material fallback instead of silently changing the hierarchy.

Use one coherent hierarchy across panels. Keep comparable axes, labels, legend roles and numerical precision consistent. Units belong in labels, commonly in parentheses; define arbitrary/normalized units and transformations. Report sensible precision supported by the data. Put long definitions and interpretations in the figure caption, without removing the definitions needed to read the figure.

## Layout, spacing and panel alignment

Use a white canvas with compact, purposeful whitespace. Align panel edges and shared axes; allocate gutters for labels, legends and colorbars rather than squeezing them into a fixed small square. Share axes only when units and ranges are truly comparable. Keep panel letters outside the data region, aligned consistently. Do not use an axis break or truncated bar origin to exaggerate effects; a zoomed coordinate plot should make its limits explicit.

Leave visible separation between title/letter, data area, tick labels, axis labels, legends, annotations and captions. Useful initial gaps are about 3–5 pt between ticks and labels and 4–8 pt between a heading and plot decorations; final rendered measurements govern, not these approximate numbers. Long labels should wrap, rotate modestly or prompt a horizontal plot. Increase figure height, adjust gutters or split panels before shrinking text below a readable final size.

For a manuscript figure, keep the long caption outside the artwork. If a standalone example/report needs a header, reserve a separate white header row, wrap it to the available width, and measure its actual bounds. Include legends, scientific-notation offset text, top ticks and colorbar decorations when measuring the plot's top. Re-render after resizing. The optional [Matplotlib example](../scripts/matplotlib_example.py) provides `layout_figure_header()`; use one final layout owner and do not run another layout engine after manual positions without recalculating them.

Avoid grids by default. A few subtle grid/reference lines may be retained when they help precise reading. Remove unnecessary top/right frames, redundant legends and duplicate labels, while keeping numeric axes needed for scatter, distributions, time series and effects. Grid removal is not permission to remove a reference that makes the quantitative claim interpretable.

## Statistical encodings and captions

Choose an observation-level or distribution view for continuous samples; use estimates and intervals to answer effect/comparison questions. A violin is a density estimate, not measured individual values; a box is quartiles, not a mean confidence interval. For dense samples, use transparent points or a justified density/binning method. Any downsampling must be disclosed and must not replace full-data statistics. Do not use jitter on a measured coordinate in a way that changes its apparent value.

Define what each point represents, biological/technical replication or repeated units, exclusions and effective n. State whether uncertainty is SD, SE, confidence/prediction interval, bootstrap interval or limits of agreement, and give its method. Respect pairing, clustering and censoring; resampling individual images from repeated subjects is not automatically a valid uncertainty estimate. A p-value does not describe effect magnitude, and overlapping intervals alone are not a significance test. Use exact supported p-values and named corrections when appropriate; do not add stars to untested comparisons.

For count/share labels, `14,325 · 50.2%` is a useful compact pattern when space permits. Define the population denominator and observation unit. Exclusive/exhaustive categories reconcile with the population; subsets keep the stated full denominator; overlapping flags may sum over 100% and require separate bars rather than a composition stack. Show a count without a fabricated share when the denominator is unknown or zero. Missing observations are not zeros. Continuous/signed effects retain their actual units rather than adopting count/share labels.

Use the relevant [basic](scientific-chart-examples.md) or [advanced](advanced-chart-guide.md) guidance for KDE, bins, fits, thresholds, calibration, risk tables, normalization and dimensionality reduction. Explanatory method detail must match the actual computation, including edge cases, not just the familiar name of a plot.

## Export and rendered verification

- Prefer editable vector PDF/SVG for lines, text and ordinary-size points/matrices. Preserve text as text in SVG and embed fonts in PDF; follow the target journal if it requests another format. Retain an editable source even when a final submission needs outlined text.
- Supply a PNG preview at the final aspect ratio, commonly 300 dpi for screen/print inspection. Raster or mixed artwork may need different resolutions; use the actual target's rule. DPI does not apply to vector geometry as a quality setting.
- Very large point clouds or image layers can be rasterized at a suitable final resolution while axes/text remain vector. This should be a deliberate export decision. Small heatmaps can use vector cells and colorbars; avoid thin white seams from renderer antialiasing without hiding real boundaries.
- Keep final physical dimensions; tight cropping can change the nominal page width. If cropping is used, record the resulting size and verify its placement. Preserve meaningful transparency against a known background, and use the requested color space/profile rather than blindly assuming CMYK or RGB.
- Inspect the final PNG and vector/PDF rendering at actual size. Check glyphs, line weight, marker visibility, text bounds, neighboring panels, colorbar labels and contrast. Check the grayscale export itself, including legends and overlapping bands. A syntactically valid file or a passing numerical test does not establish visual quality.
- Cross-check plotted values with raw/derived tables, aggregation, intervals, denominators, coordinate transformations, rounding, legend assignments and caption definitions. Keep links relative inside reports/portable skills. Preserve source and extraction/run metadata where available.

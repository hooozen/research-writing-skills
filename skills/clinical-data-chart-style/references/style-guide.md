# Clinical Data Chart Style Guide

This specification is implementation-neutral. Preserve the visual result whether the chart is produced with Python, R, JavaScript, an office suite, or another system.

## Visual character

Use a calm, evidence-first clinical reporting style: spacious, precise, minimal, and legible. The chart should feel like a compact evidence panel, not a dashboard widget.

## Design tokens

| Role | Value | Use |
|---|---|---|
| Report canvas | `#FFFFFF` | Page or report background |
| Evidence card | `#F2F2F2` | Chart background with 16 px rounded corners |
| Primary blue | `#3D8DFF` | Leading or highlighted category |
| Secondary blue | `#6DCBF4` | Supporting category |
| Light blue | `#BFE8FA` | Additional category |
| Neutral gray | `#A8AFB8` | Other, unknown, missing, residual |
| Baseline gray | `#D4D4D4` | Minimal axis baseline |
| Primary text | `#000000` | Titles and direct data labels |
| Muted text | `#5F6670` | Category labels, subtitles, notes |

Use colors semantically and consistently. Translate these exact hex values into the selected renderer. Do not assign red or green unless the source explicitly defines risk/status semantics and the report explains them.

## Typography

- Font stack: `Helvetica Neue`, Helvetica, Arial, `Noto Sans`, sans-serif. Use the first installed option that covers the output language without changing the hierarchy. For Chinese or mixed-script labels, use an installed CJK fallback such as Noto Sans CJK SC or PingFang SC; check the rendered glyphs. Convert px to the renderer’s units rather than treating px as points.
- Chart title: 26 px, bold, black.
- Subtitle: 14 px, regular, muted gray.
- Category labels: 15 px, regular, muted gray.
- Direct values: 15 px, bold, black.
- Source note: 12 px, regular, muted gray.
- Use sentence case. Avoid all caps.

## Composition

- Place the chart on a light-gray card without border or shadow.
- Maintain generous padding: about 40 px on all sides.
- For count/share bars, a single baseline and direct labels often suffice. For scatter plots, distributions and time series, retain the numeric axes needed to read coordinates; use restrained gridlines only when they improve quantitative reading.
- Put horizontal-bar labels immediately beyond bar ends.
- Put vertical-bar labels immediately above bars.
- Keep category order descending by value unless clinical, anatomical, temporal, or acquisition order is meaningful.
- Limit a figure to one message. Split unrelated metrics into separate figures.
- Keep box-plot and violin-plot median strokes thin and legible, without dominating the observations or distribution outline. The examples use 0.8 pt; adjust to the final display size when needed.
- Omit heatmap colorbar outlines by default. Keep ticks and labels restrained; if a boundary is needed, use a thin baseline-gray edge rather than a solid black frame.

## Spacing and overlap

- Leave clear separation between titles, subtitles, plot areas, axis ticks and labels, direct values, legends, annotations, and source notes, including between adjacent panels. Scale spacing to the font size and final display size.
- Prevent unintended overlap, occlusion, and clipping that obscure text, data marks, or their relationships. Intentional layering, such as intersecting series or confidence bands, is acceptable when the data remain interpretable and labels stay legible.
- Resolve collisions by adjusting margins, axis limits, label positions, wrapping, panel spacing, or figure size; simplify or split a crowded figure when needed. Do not hide required information or shrink text until it becomes hard to read.
- Inspect the actual rendered export at its intended display size, including long labels and edge elements. Fix collisions and render again before delivery; automatic layout alone is not sufficient verification.

## Title placement and panel boundaries

Choose one layout per panel before positioning its contents:

- **Title inside the card (default for a standalone card):** the gray background contains a header region for the complete title and optional subtitle, followed by a separate plot region. Align the title with the plot's left edge and reserve top/side padding. Measure the header height before assigning the plot's top edge.
- **Title above the panel:** the entire title/subtitle sits on white, with a clear gap before the gray panel begins. This suits compact multi-panel figures. Keep the same arrangement across comparable panels.

The gray/white boundary must never pass through any title or subtitle glyph. Check the full rendered text rectangle, not its anchor point or baseline. As a starting point, leave about 24–40 px from an inside title to the card edge and 12–20 px from the header to plot decorations; scale these gaps to the actual typography and final display size.

Long or multiline titles need more header height. Wrap at the available text width using the final font, then move the plot down or increase figure height. Do not keep a fixed header height while adding lines, move the title onto the card edge, or shrink text until it becomes hard to read. Include top ticks, scientific-notation offsets, legends and colorbar labels when checking the gap below the header.

**Matplotlib translation.** A figure-coordinate `FancyBboxPatch` and an axes title positioned by `ax.set_title()` have different layout owners: changing axes geometry can move the title without moving the card. A fixed `y`, `top` or `pad` is not a containment guarantee. For a full card, use a figure-level title with top alignment, measure its bounding box after drawing, and reserve the plot area below it. The optional `layout_card_header()` in [the Matplotlib example](../scripts/matplotlib_example.py) demonstrates measured wrapping, title/subtitle placement and height growth; pass the colorbar axes too when present. It handles plain-text headers; give mathematical titles appropriate explicit breaks in task-specific code.

Use one final layout owner. Finish automatic axes layout before positioning a manual card header, then disable that layout engine; do not call `tight_layout()` or enable constrained layout afterwards without recomputing the card/header geometry. `bbox_inches="tight"` crops the outer export; it does not repair an internal gray/white boundary. Changing fonts, size, DPI or export backend requires another render check. [Title coordinates](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_title.html), [text bounding boxes](https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text.get_window_extent), [automatic layout scope](https://matplotlib.org/stable/users/explain/axes/tight_layout_guide.html).

Apply the same ownership in other tools: for example, put a heading and plot in separate rows of one gray container, with padding on the container; avoid absolutely centering the heading on its top border.

## Data labels

For a count-and-share chart with a known positive denominator, use this pattern:

```text
14,325 · 50.2%
```

Compute the percentage with the correct population denominator, naming its unit (patients, eyes, images, or scans). Do not treat these units as interchangeable.

- Exclusive and exhaustive categories reconcile with the population; rounding alone may prevent a displayed sum of exactly 100.0%.
- For subsets, retain the full-population denominator and identify omitted categories. Do not silently normalize the displayed subset to 100%.
- For overlapping categories, count each category against the stated population; explain that one unit may occur in multiple categories and shares can sum above 100%. Use separate bars, not a composition stack.
- If denominators vary by category, show each denominator and make the comparison basis explicit. Choose a rate or percentage axis when rates are the intended comparison rather than using count lengths to imply rate differences.
- For an unknown or zero denominator, show counts without numeric shares and explain why the share is unavailable. Zero is a valid count; missing data are not zero.
- For continuous outcomes, signed changes, or intervals, use the metric's unit and supplied uncertainty. Do not apply the count-and-share pattern or infer error bars from unsupported assumptions.

## Chart selection

- Vertical bars: a natural starting point for categorical comparisons with short readable labels; keep meaningful left-to-right order such as dose or acquisition size.
- Horizontal bars: useful when long category names, many crowded labels, or a ranking read more clearly top-to-bottom. Leave room for labels and values without excessive axis-label rotation.
- Select orientation from the actual label lengths, order, audience convention and available aspect ratio. Category count alone is not a rule, and neither orientation is inherently more scientific. Follow the user's chosen orientation when supplied.
- Lines: ordered time; use primary blue for the focal series and gray for comparison. For other continuous ordered predictors, use an appropriate scatter/line encoding with explicitly defined axes rather than connecting unordered categories.
- Stacked bars: mutually exclusive composition across a small number of cohorts; label totals and explain the denominator.
- Means, effects, and uncertainty: use points and intervals when appropriate; keep signed values, units, and a meaningful reference such as zero. Bar lengths encode from zero; do not truncate a bar axis to exaggerate differences.
- Avoid pie/donut charts unless the user explicitly requests them.

For distributions, associations, paired data, uncertainty and heatmaps, consult the relevant example in [scientific-chart-examples.md](scientific-chart-examples.md). Its statistical conventions complement these shared style tokens.

## Markdown integration

Store figures beside the report:

```text
report.md
figures/
  modality.svg
  layer.svg
  scan-size.svg
```

Use meaningful alt text that states the measure and population. Add the data source and extraction date in prose below the figure when traceability matters.

## Quality checks

- Values and labels match the source table.
- Percentages use the correct denominator.
- Spacing is clear at the intended display size; no inappropriate overlap, occlusion, or clipping affects text or data marks (see Spacing and overlap).
- At the final export size, the title/subtitle rectangles are wholly inside the card with padding, or wholly above it with a gap. Check both PNG and SVG when delivering both; automatic layout or a valid file alone does not verify this.
- Residual categories use neutral gray.
- The title accurately states the metric or conclusion.
- The SVG link is relative and resolves from the Markdown file.
- The chart remains readable at approximately 800–1000 px width.

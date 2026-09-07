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
- No labels are clipped or overlapping.
- Residual categories use neutral gray.
- The title accurately states the metric or conclusion.
- The SVG link is relative and resolves from the Markdown file.
- The chart remains readable at approximately 800–1000 px width.

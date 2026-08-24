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

- Font stack: `Helvetica Neue`, Helvetica, Arial, `Noto Sans`, sans-serif. Use the first installed option without changing the hierarchy.
- Chart title: 26 px, bold, black.
- Subtitle: 14 px, regular, muted gray.
- Category labels: 15 px, regular, muted gray.
- Direct values: 15 px, bold, black.
- Source note: 12 px, regular, muted gray.
- Use sentence case. Avoid all caps.

## Composition

- Place the chart on a light-gray card without border or shadow.
- Maintain generous padding: about 40 px on all sides.
- Use a single baseline and remove gridlines when direct labels carry the values.
- Put horizontal-bar labels immediately beyond bar ends.
- Put vertical-bar labels immediately above bars.
- Keep category order descending by value unless clinical, anatomical, temporal, or acquisition order is meaningful.
- Limit a figure to one message. Split unrelated metrics into separate figures.

## Data labels

Use this exact pattern:

```text
14,325 · 50.2%
```

Compute the percentage with an explicit denominator. Confirm that category shares reconcile with the intended total; rounding may cause displayed shares not to sum to exactly 100.0%.

## Chart selection

- Horizontal bars: modality, layer/type, diagnosis, device, long category labels, or more than four categories.
- Vertical bars: scan sizes or two to six short categories.
- Lines: ordered time only; use primary blue for the focal series and gray for comparison.
- Stacked bars: composition across a small number of cohorts; label totals and explain the denominator.
- Avoid pie/donut charts unless the user explicitly requests them.

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

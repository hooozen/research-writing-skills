# Scientific tables in PowerPoint

Use a table for exact values, several metrics per method, population composition or settings with their meaning. Use a chart when the relationship or distribution is the main evidence. Keep a requested table as a native table with editable cells, not a heatmap, screenshot or grid assembled from separate text boxes.

## Shared style

- Keep the existing 16:9 white canvas, slide-title position and evidence-caption band. The reference table starts at x=80, y=196 and spans 1120 px.
- Use the same CJK/sans-serif family as the deck. Start headers and body at 18 pt; the caption remains 15 pt. Split a dense table instead of shrinking the text.
- Use a saturated blue `#1464D2` header with white bold text; keep body cells white and dark text. In grayscale, use the palette's dark primary. Avoid a heavy full grid; a header rule and bottom rule are sufficient, with a rule above a total when needed.
- Left-align text and right-align numbers, with consistent decimal places within each metric. Put units, percentage notation and meaningful preference arrows in headers. Explain arrows in the caption. Give long descriptions more column width.
- Use a pale blue row only for a declared focal method or selection. Explain its meaning. Highlighting is not evidence of statistical significance or of being best on every metric.

## Table layouts

| Layout | Columns and meaning | Required checks |
|---|---|---|
| Results comparison | Method plus a small set of metrics | Same evaluation population/protocol, positive class as relevant, metric units, available uncertainty, missing evaluations; no unsupported rank/significance |
| Sample composition | Category, count, share and an appropriate total | Actual denominator and observation unit; totals only for mutually exclusive exhaustive categories; overlapping flags may exceed 100% |
| Methods and parameters | Setting, value and role/definition | Exact supplied configuration; distinguish unprovided information from an explicitly disabled feature |

Keep necessary interval definitions and sample information in the caption or linked methods. Do not fill a missing interval from a mean/SD unless the required assumptions and inputs support that calculation. Keep `0`, missing, unmeasured and not applicable distinct; explain any symbol used. A single missing symbol is adequate only when it has one clearly stated meaning in that table.

Calculate from unrounded source values. Use percentages consistently and distinguish a change in percentage points from relative change. Preserve exact source data and definitions in notes or a companion file. Native PowerPoint table cells are literal text/values, not a spreadsheet with formulas: update totals, shares, differences and intervals together when the source changes.

## Optional adapter

Use `kind: 'table'` with `data.columns` and `data.rows`. Each column declares `label`, `kind` (`text`, `integer`, `number`, `percent`), optional `digits` and positive relative `weight`. Percentage inputs are proportions in [0,1], displayed in the header's percentage unit; `0.85` becomes `85.0` at one decimal. Integers retain whole-count formatting. Explicit `null` becomes `missing_label` (default `—`); numbers never silently become missing values.

`highlight_rows` and `total_row` are zero-based body-row indexes. The adapter supports 2–6 columns and 1–5 body rows in this layout; larger tables require splitting/reflow. It does not infer a total, denominator, interval or best result. The composition demonstration derives shares from its explicitly supplied count population; it does not normalize overlapping flags.

The synthetic fixtures in [example-data.json](../assets/example-data.json) demonstrate results and parameters. `tableSpecifications(examples)` also builds a sample-composition table from the same count data as the existing bar chart. Keep the synthetic caption in a template; replace all evidence and captions when adapting it to real work.

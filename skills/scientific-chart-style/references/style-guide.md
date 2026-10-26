# Shared Scientific Chart Style

Use **high-contrast blue by default**, **D for black-and-white print**, and white backgrounds. A named journal's current specifications take priority. Read only the sections relevant to the current figure. Scientific definitions and minimal inputs belong to the selected [chart card](chart-index.md), not a contact sheet.

## Color and print tokens

| Role | High-contrast color | D print |
|---|---|---|
| Canvas / plot background | `#FFFFFF` | `#FFFFFF` |
| First / focal series | `#1464D2` (saturated blue) | `#34383C` |
| Second series | `#B64B00` (dark orange) | `#70767B` |
| Third series | `#7A3DB8` (purple) | `#92989E` |
| Light background fill / sequential midpoint | `#BFD5F4` | `#E0E3E5` |
| Other / unknown / missing | `#586575` | `#B7BCC0` |
| Main text | `#24282C` | `#24282C` |
| Secondary notes | `#626B73` | `#626B73` |
| Axes / ticks | `#34383C` | `#34383C` |

Keep group identity consistent across figures. One series often needs only one color. For more than three groups, consider facets/direct labels or deliberately extend the contrasting palette; do not silently recycle hues. Color must not imply risk, significance or direction unless defined.

Use circle/square/triangle and solid/dashed/dotted lines as redundant identities, with sparse bar hatching when useful. Apply D deliberately, rather than desaturating a color screenshot. Pale fills are background layers; use the stronger series colors for essential outlines, points and lines. Check the final composited color when transparency is present. Essential graphical cues should reach at least 3:1 against their adjacent background; this does not require pale support fills or every sequential-scale cell to reach 3:1 when other visible cues retain the meaning. See [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

For ordered magnitudes, use an ordered light-to-dark blue sequential scale with a visible light-blue midpoint. Use blue–neutral–orange divergence only for a meaningful midpoint, with explicitly centered limits when appropriate. Keep comparable panels on a common scale; mark missing cells separately from low values. Choose dark or white annotation ink from actual background contrast. Avoid rainbow scales and decorative gradients. Color changes do not alter the physical typography, line widths, markers, layout, spacing or export rules below; the D print design remains unchanged.

## Physical size and typography

Compose at final width. About **89 mm** single-column and **180–183 mm** double-column are useful starting points; the destination's dimensions override them. Reflow narrow figures rather than shrinking a wide figure's labels. Higher raster DPI cannot repair tiny printed type.

| Element | Starting point at final size |
|---|---|
| Font | Arial / Helvetica / suitable installed sans-serif; Noto Sans or DejaVu Sans are portable alternatives |
| Axis labels / ordinary annotations | 7 pt, regular |
| Ticks / compact legends | 6.5–7 pt |
| Panel letters | 8 pt, bold, lower-case |
| Short panel title | About 7 pt; long caption outside artwork |
| Axis / tick strokes | About 0.6 pt |
| Data / interval lines | About 0.8–1.1 pt |
| Markers | Roughly 2.5–4 pt; adjust to density |

These are physical points, not pixels divided by export DPI. Use normal letter spacing and sentence case, with one hierarchy across panels. Preserve readable math, subscripts, units and supported numerical precision. For Chinese/mixed glyphs choose an installed CJK font (for example Noto Sans CJK SC or PingFang SC), inspect actual glyphs and record material font substitution.

## Layout and spacing

Use compact purposeful whitespace, aligned panels and numeric axes needed to interpret coordinates. Share axes only for comparable units/ranges. Put panel letters consistently outside data. Retain a zero origin for bar lengths; show meaningful references for differences or ratios. Wrap long categories or choose horizontal orientation before reducing type size.

Reserve space for legends, colorbars, ticks, offset notation and annotations. Approximate starting gaps are 3–5 pt for tick labels and 4–8 pt below a heading; rendered geometry governs. Increase height/gutters or split crowded panels before shrinking text. Avoid decorative cards, rounded containers, shadows and unnecessary top/right frames. Retain restrained grid/reference lines only when they aid quantitative reading.

If a standalone example needs a header, allocate a measured white row above the plot. [The shared helper](../scripts/matplotlib_example.py) provides `layout_figure_header()`. Finish automatic layout before manually assigning final positions and remeasure after font, size or backend changes. Keep long manuscript captions outside the artwork.

## Data marks and captions

The selected card defines the encoding, missingness, aggregation and statistical assumptions. Identify observation/independence unit, n, exclusions, units, reference direction and uncertainty meaning. Distinguish SD/SE/CI/prediction interval/limits of agreement. Jitter is permitted perpendicular to a measurement, without altering its apparent value. Unsupported p-values, intervals, paired records and raw observations must remain unavailable. Exact results should remain traceable to source/derived tables.

For readable count/share bars, `14,325 · 50.2%` is a compact pattern; specify population and unit. Exclusive/exhaustive, subset and overlapping categories have different denominators. Zero or unknown denominators have no numeric share; missing values are not zero. Continuous and signed outcomes retain their own units.

## Export and final verification

- Preserve editable vector SVG/PDF for ordinary plots; keep SVG text as text and embed PDF fonts. Follow destination requirements if it needs another submission format, and retain an editable master.
- A PNG preview commonly uses 300 dpi at final aspect ratio. Raster/mixed images may need other resolutions; check the named journal. Increasing metadata DPI does not recover image detail. Dense point clouds may be selectively rasterized while axes/text remain vector.
- Small heatmaps/colorbars can use vector cells; remove renderer seams without obscuring real boundaries. Use the requested color space/profile and known background for transparency.
- Keep actual physical dimensions. Tight cropping can alter nominal page width, so inspect and record the final result if used.
- Inspect final rendered text, glyphs, lines, marker contrast, legends, colorbar labels and neighboring panels at actual size. Inspect D itself when requested. Passing code/numerical checks does not establish visual readability.
- Check values, limits, transformations, intervals, denominators, legend identities, rounding and caption definitions against the source. Keep relative report links and relevant source/run metadata.

For a named submission, consult [publication-references.md](publication-references.md). Optional broad comparisons remain in the [basic](scientific-chart-examples.md) and [advanced](advanced-chart-guide.md) backgrounds; they are not mandatory reading for one chart.

# Scientific chart system for presentations

## Visual system and point sizes

Use a white 16:9 canvas with a flat composition, dark text and no decorative cards, shadows or 3D marks. Match a supplied deck's size and layout when editing it. The retained color system is:

| Role | Color | Grayscale D |
|---|---|---|
| First/focal group | `#1464D2` | `#34383C` |
| Second group | `#B64B00` | `#70767B` |
| Third group | `#7A3DB8` | `#92989E` |
| Light sequential midpoint | `#BFD5F4` | `#E0E3E5` |
| Other/unknown/missing | `#586575` | `#B7BCC0` |
| Main text | `#24282C` | Same |
| Notes | `#626B73` | Same |
| Axes/ticks | `#34383C` | Same |

Keep group identity stable across the deck. Use point shapes or line styles as well as color where groups overlap or grayscale is requested. Use one color for one series. Count/share labels retain the correct population, and continuous outcomes keep their actual units. A light fill supports a visible outline or foreground mark; it does not replace one.

Projection typography is intentionally larger than publication typography:

| Element | Presentation starting point | 96-DPI API pixels |
|---|---:|---:|
| Cover | 42 pt | 56 px |
| Slide title | 33 pt | 44 px |
| Body | 20 pt | 26.67 px |
| Chart axis/legend/direct labels | 16.5 pt | 22 px |
| Table header/body | 18 pt | 24 px |
| Two related panels, if necessary | 15 pt | 20 px |
| Caption/source | 15 pt | 20 px |

Use Arial/Helvetica or another suitable sans-serif. For Chinese, use an installed matching CJK family such as Microsoft YaHei, Noto Sans CJK SC or PingFang SC and inspect the rendered glyphs. The included demonstration uses Arial Unicode MS for CJK coverage. Record a required substitution and check the target machine; do not claim fonts are embedded or available without checking. The equation is `pixels = points × 96 / 72`; higher export DPI does not change these point sizes.

## Layouts

The reference frame is 1280 × 720 px. Keep roughly 64 px outer margins, a title near y=42, the main chart beginning near y=168, and the evidence caption near y=624. These are template starting points, not permission to clip content. Reserve space for axis titles, long category labels and colorbars before fixing the plot size.

- **Single plot:** one large chart with title and one caption. The adapter uses a native chart frame about 1080 × 420 px. Keep its axes and legend inside the chart object.
- **Editable scientific geometry:** use a shared numeric-to-slide transform for axes, marks and labels. Leave a dedicated band for axis units. Keep interval caps, individual points and uncertainty definitions visible.
- **Two related plots:** share grouping and scales when meaningful. Use two readable panels only when the relationship warrants them; otherwise use two slides. Keep panel labels and legends inside their reserved space.
- **Matrix:** use consistent native cells, a shared sequential/diverging scale and explicit missing cells. Choose black or white cell text using the actual fill contrast. Keep the colorbar readable and editable.
- **Empty plot layout:** retain a plot placeholder and a caption placeholder without fabricated experimental values.
- **Native table:** blue header, dark text on white body cells, numerical columns right-aligned, minimal horizontal rules and explicitly explained emphasis. Read [tables.md](tables.md) when building result, composition or parameter tables.

Use short, direct titles. Captions identify the observation unit, n/denominator, metric/unit, reference, uncertainty and source as applicable. A template guide may explain how to replace a chart; a real research slide should show the research content rather than authoring instructions.

## Editability

| Representation | What the user can edit | What changes require |
|---|---|---|
| Native chart | Data series, categories, axes, labels and appearance | Update the native dataset/workbook and rerender |
| Native table | Individual cells, row/column sizes, text and formatting | Refresh derived values explicitly; cells do not recalculate spreadsheet formulas |
| Native vector geometry | Individual marks, lines, cells, labels and positions | Recompute/rebuild from source when data change |
| Supplied image/SVG image | Placement and size, sometimes conversion in a target app | Original plotting source to update data |

The adapter uses native charts for bars, numeric-time lines, scatter and ROC/PR. It uses native geometry for boxes/raw points, paired observations, supplied intervals and heatmaps. It preserves source data and definitions in notes. Neither class requires a full-slide screenshot. Do not imply that every advanced scientific plot is an Excel-native chart or that moving a geometric point updates an underlying workbook.

Custom count/share labels do not recalculate from a native data edit. Refresh their count and denominator together. ROC/PR native series contain derived coordinates; recompute them when the underlying labels/scores change. Editing the plotted coordinates alone does not rerun model evaluation.

For real datasets, retain exact data and relevant calculations beside the deck. For a figure supplied only as an image, obtain its data before claiming to reconstruct an editable dataset. A template's demonstration figures are not evidence for the user's project.

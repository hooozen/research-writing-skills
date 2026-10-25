# Publication Guidance and Sources

Use these primary sources to adapt a figure to its destination. The approved B palette is this skill's default and D is its grayscale alternative. Low saturation is a user preference; journals generally require legibility, adequate contrast and accessible encoding, not one universal palette. The shared style tokens are working defaults, while the target journal's current instructions determine submission dimensions, type sizes, accepted formats and resolution. Recheck linked specifications when preparing an actual submission; this reference was checked on 2026-10-25.

## Examples of journal-specific requirements

| Source | Verified guidance and scope |
|---|---|
| [Nature: preparing figures](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/) | Standard sans-serif fonts such as Arial/Helvetica, editable text and embedded fonts. Ordinary text is 5–7 pt; multi-panel letters are 8 pt bold upright lowercase. Include axes, ticks and units; avoid overlapping text and unnecessary decoration. These numbers belong to this guide, not every Nature Portfolio journal. |
| [Nature: building/exporting panels](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/) | Build at publication size; the guide specifies 89 mm single-column and 183 mm double-column widths. Arrange panels compactly and retain editable vector content where possible. Its export instructions are destination-specific. |
| [Journal of Cell Biology: figure guidelines](https://rupress.org/jcb/pages/fig-vid-guidelines) | Most text 8 pt and strokes 0.5–1 pt. RGB color; at least 300 dpi, with 600 dpi recommended for photographs combined with text/line art, and 1,000 dpi for black-and-white line art without gray. This journal is published by Rockefeller University Press, not Cell Press. |
| [Elsevier: artwork sizing](https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing) | Plan the final printed dimensions and lettering together. Approximately 7 pt ordinary text and at least 6 pt sub/superscripts are presented as practical guidance rather than one binding rule for every journal. Consult the specific journal's author guide. |
| [Elsevier: accessible color](https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions) | Maintain sufficient contrast and test color-vision accessibility. Shapes, positions and line types can communicate distinctions alongside color. Muting a palette must not erase the distinctions needed to interpret the result. |

## Translate principles into an export

Set figure width and height in physical units before choosing type sizes. Reflow a multi-panel layout for a narrower column rather than shrinking its text with the whole image. At the final size, check axis labels, legends, superscripts, panel letters, error bars, markers and the separation between adjacent panels. Keep mathematical meaning, units and exact values intact when shortening labels.

Preserve an editable vector master for plots and annotations; embed fonts when the format permits. Raster content needs adequate native resolution at its placed size. Increasing a DPI metadata value or enlarging a small raster does not recover missing detail. Retain vector axes/text when selectively rasterizing dense marks, and state the chosen output dimensions and resolution in the export record.

Check the actual rendered PDF/SVG and a grayscale print preview. Use black/dark text with colored keys, marker shapes and line patterns rather than relying on colored text. Distinguish a mean±SD band, confidence interval, prediction interval and limits of agreement in the caption; styling cannot resolve an undefined statistic. Journal-specific rules can override a default visual convention, such as whether an in-figure title or pattern is acceptable.

For statistical definitions and examples, use [scientific-chart-examples.md](scientific-chart-examples.md) and [advanced-chart-guide.md](advanced-chart-guide.md). They link to original methodological papers and official implementation documentation. Those links are references, not requirements to install the corresponding software or copy the source figures.

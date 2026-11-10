# The 19 chart types in PowerPoint

Choose the row for the requested question. Use the statistical definition from an available `scientific-chart-style` chart card when needed; do not load the whole reference atlas to make one slide. Native XY means a numeric scatter chart, including connected or repeated coordinates when the scientific curve requires them.

| Chart | Preferred editable representation | Preserve/check |
|---|---|---|
| Count/share bars | Native bar/column, with direct labels | Zero origin, actual counts, correct denominators, exclusive/overlap/subset relationship, neutral residuals |
| Box plot | Native boxes/whiskers/raw points; a native boxWhisker chart only with matching definitions | Raw observations, linear/inclusive versus other quartiles, 1.5×IQR or stated whiskers, all outliers, n |
| Violin | Native freeform density outline and raw points | Real observations, density method/bandwidth, normalization, group identity; requires regeneration from data |
| Scatter | Native XY markers | True x/y values, units, actual observation unit, grouping; no invented regression or causality |
| Longitudinal line | Native XY with numeric time; use native geometry for unsupported uncertainty bands | Actual spacing, missing gaps, pairing/repeated measures and stated uncertainty; do not silently omit a supplied band |
| Histogram | Native columns for equal-width bins; native numeric rectangles for unequal bins | Explicit boundaries, bin counts/density, closure convention, total observations and true bin widths |
| ECDF | Native XY with repeated step coordinates | Ties, exact cumulative counts/proportions and step direction; no smoothing |
| Paired observations | Native lines and endpoint markers keyed by ID | Real pairs, incomplete endpoints retained/disclosed, no invented pairing or zero filling |
| Estimates and intervals | Native points, interval lines and caps | Supplied/calculated justified endpoints, interval meaning, signed units, reference line and group order |
| Heatmap | Native cell shapes, editable values and scale | Common limits, ordered scale, units, missing cells and readable label ink |
| Raincloud | Native half-density freeform, raw points and box components | Same source observations, density and quartile definitions; no reconstructed distributions from means |
| ROC | Native XY line/steps and reference line | Binary labels/scores, tie handling, threshold order, axis [0,1], supported AUC/interval method |
| PR | Native XY step coordinates | Positive-class prevalence, tie handling, precision/recall, AP definition; no trapezoidal AP substitution |
| Calibration | Native XY points/line; native interval marks when justified | Defined bins, empty bins, within-bin n, mean predicted probability, observed frequency and any ECE definition |
| Confusion matrix | Native cells and counts/normalized labels | True/predicted axis direction, class order, explicit normalization denominator, undefined rows |
| Bland–Altman | Native XY plus horizontal reference lines | Paired measurements, sign of difference, mean bias and stated limits of agreement; not a correlation substitute |
| Survival | Native XY step curve, censor marks and native risk table | Actual times, censoring, tie convention, step positions and aligned risk counts; no invented events |
| Volcano | Native XY groups, threshold reference lines | Effect scale, raw/adjusted p definition, log transform, multiplicity, zero/missing handling and threshold direction |
| PCA | Native XY grouped observations | Actual scores, preprocessing, explained-variance labels, loading interpretation only when supported |

The included adapter demonstrates a subset of these implementations. The other rows describe the required faithful representation, not an implemented one-command renderer. If the author's tool cannot preserve a necessary chart component as native objects, use a capable authoring route or agree on a clearly disclosed static figure; never claim full data editability for an embedded picture.

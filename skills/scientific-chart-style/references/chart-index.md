# Chart Index: 19 Scientific Encodings

Start with the question and available inputs. Choose one chart ID, read only its card, and inspect its individual SVG or PNG only when visual detail is needed. The card specifies the statistical definition, input format, limitations and a short runnable example.

The linked inputs and previews are **synthetic reference examples**, not research findings. B teal/terracotta is the default; generate D print mode with `--mode grayscale`. Keep the shared [style guide](style-guide.md) authoritative for appearance.

| ID / chart card | Use when | Required inputs | Example data | Individual preview |
|---|---|---|---|---|
| [`count_share`: Count/share bars](charts/count_share.md) | How many records belong to each category, and what is the denominator? | categories, counts, denominator, relationship, unit | [JSON](examples/count_share.json) | [SVG](examples/count_share.svg) · [PNG](examples/count_share.png) |
| [`boxplot`: Box plot with observations](charts/boxplot.md) | How do groups differ in location and spread? | groups, value_label | [JSON](examples/boxplot.json) | [SVG](examples/boxplot.svg) · [PNG](examples/boxplot.png) |
| [`violin`: Violin plot with observations](charts/violin.md) | What distribution shape is supported by the observations? | groups, value_label | [JSON](examples/violin.json) | [SVG](examples/violin.svg) · [PNG](examples/violin.png) |
| [`scatter`: Scatter plot](charts/scatter.md) | Are two measured quantities associated? | observations, x_label, y_label | [JSON](examples/scatter.json) | [SVG](examples/scatter.svg) · [PNG](examples/scatter.png) |
| [`line`: Time series / longitudinal summary](charts/line.md) | How does the observed quantity change over actual ordered times? | times, subjects, time_label, value_label | [JSON](examples/line.json) | [SVG](examples/line.svg) · [PNG](examples/line.png) |
| [`histogram`: Histogram](charts/histogram.md) | How many observations fall in each numerical range? | groups, value_label | [JSON](examples/histogram.json) | [SVG](examples/histogram.svg) · [PNG](examples/histogram.png) |
| [`ecdf`: Empirical cumulative distribution](charts/ecdf.md) | What fraction of each group is at or below a value? | groups, value_label | [JSON](examples/ecdf.json) | [SVG](examples/ecdf.svg) · [PNG](examples/ecdf.png) |
| [`paired`: Paired observations](charts/paired.md) | How did the same identified units change? | pairs, value_label | [JSON](examples/paired.json) | [SVG](examples/paired.svg) · [PNG](examples/paired.png) |
| [`interval`: Effect estimates and intervals](charts/interval.md) | What is the estimated effect relative to a common reference? | estimates, reference, value_label, interval_label | [JSON](examples/interval.json) | [SVG](examples/interval.svg) · [PNG](examples/interval.png) |
| [`heatmap`: Heatmap with missing cells](charts/heatmap.md) | How does a numerical quantity vary across rows and columns? | values, row_labels, column_labels, value_label, limits | [JSON](examples/heatmap.json) | [SVG](examples/heatmap.svg) · [PNG](examples/heatmap.png) |
| [`raincloud`: Raincloud](charts/raincloud.md) | What do raw observations, distribution shape and summary show together? | groups, value_label | [JSON](examples/raincloud.json) | [SVG](examples/raincloud.svg) · [PNG](examples/raincloud.png) |
| [`roc`: ROC curve](charts/roc.md) | How well do continuous scores rank positives above negatives? | labels, scores | [JSON](examples/roc.json) | [SVG](examples/roc.svg) · [PNG](examples/roc.png) |
| [`pr`: Precision–recall curve](charts/pr.md) | How precise are positive predictions as recall increases? | labels, scores | [JSON](examples/pr.json) | [SVG](examples/pr.svg) · [PNG](examples/pr.png) |
| [`calibration`: Calibration diagram](charts/calibration.md) | Do predicted probabilities match observed positive frequencies? | labels, probabilities, bin_edges | [JSON](examples/calibration.json) | [SVG](examples/calibration.svg) · [PNG](examples/calibration.png) |
| [`confusion`: Confusion matrix](charts/confusion.md) | Which binary classes are confused at a stated threshold? | labels, scores, threshold | [JSON](examples/confusion.json) | [SVG](examples/confusion.svg) · [PNG](examples/confusion.png) |
| [`bland_altman`: Bland–Altman agreement](charts/bland_altman.md) | Do two measurement methods agree on the same units? | method_a, method_b, value_unit | [JSON](examples/bland_altman.json) | [SVG](examples/bland_altman.svg) · [PNG](examples/bland_altman.png) |
| [`survival`: Kaplan–Meier survival](charts/survival.md) | How does event-free probability change under right censoring? | groups, risk_times, time_unit | [JSON](examples/survival.json) | [SVG](examples/survival.svg) · [PNG](examples/survival.png) |
| [`volcano`: Volcano plot](charts/volcano.md) | Which features combine signed effects with adjusted statistical evidence? | ids, log2_fold_change, pvalues, adjusted_p_threshold, absolute_log2_effect_threshold | [JSON](examples/volcano.json) | [SVG](examples/volcano.svg) · [PNG](examples/volcano.png) |
| [`pca`: PCA scores](charts/pca.md) | Which multivariate variation appears in the first principal components? | values, groups, feature_names, preprocessing | [JSON](examples/pca.json) | [SVG](examples/pca.svg) · [PNG](examples/pca.png) |


## Run one example

From the skill directory, use an output directory in the task workspace. The following creates only the ROC example and its numerical/export companions:

```sh
python scripts/render_chart.py --chart roc --example --output-dir /tmp/roc-reference
```

For actual supplied data, replace `--example` with `--input /path/to/task/roc.json`. `--input` and `--example` are mutually exclusive; no data is silently synthesized. Use `--formats svg,png,pdf` when all three exports are needed. [Renderer](../scripts/render_chart.py) · [machine-readable index](chart-index.json).


## Maintenance and optional browsing

The [preview manifest](examples/manifest.json) records fixture, source and output hashes. `python scripts/build_chart_references.py --check` verifies this mapping without rendering. Refreshing all shipped reference images is a maintainer action, not a prerequisite for drawing one chart. The older [basic](scientific-chart-examples.md) and [advanced](advanced-chart-guide.md) guides remain optional background; their contact sheets are not required Agent input.

# Additional Scientific Charts — optional background

Start with the [19-chart index](chart-index.md), then read one selected chart card and use its single-chart command. This longer guide is optional background for comparing related methods. The B/D tokens in [style-guide.md](style-guide.md) control appearance, not the analysis; overview images are optional browsing aids.

## Choose from the evidence

| Question | Chart | Minimum useful inputs |
|---|---|---|
| What do individual values and their distribution look like? | Raincloud | Raw observations, group and independence unit |
| How large is a difference? | Estimation plot | Observations or an estimate with justified interval; pairing if applicable |
| How do scores rank positives and negatives? | ROC and precision–recall | Per-case labels and continuous scores; positive class |
| Do predicted probabilities match observed frequencies? | Calibration | Per-case outcomes and probabilities; evaluation population |
| Which classes are confused at a decision rule? | Confusion matrix | Labels and predictions, or a complete count matrix |
| Do two methods agree on the same units? | Bland–Altman | Matched measurements, units and difference direction |
| How does event-free probability change over time? | Kaplan–Meier | Duration, event/censor indicator and group; entry time when applicable |
| Which features combine large effects with statistical evidence? | Volcano | Feature identifiers, signed effects and stated raw/adjusted p-values |
| What variation is visible in a multivariate dataset? | PCA scores | Sample-by-feature data and an explicit preprocessing/fitting protocol |

Every caption should identify the observation unit, independent n, missing/excluded records, estimate or transformation, and uncertainty definition when present. Keep exact source values and computed summaries alongside figures. “Modern” means readable evidence, appropriate encodings and reproducible definitions, not extra ornament or automatic significance symbols.

## Distributions and differences

### Raincloud and estimation plots

A raincloud combines a half-density, individual observations and a defined summary. Use separate lanes so points, density and median/interval do not obscure one another. Report kernel/bandwidth, support and density-width normalization; width should not silently imply group sample size. Use stable jitter only perpendicular to the measurement axis. Preserve outliers and group n. For small, discrete or highly bounded datasets, show points, a box or an ECDF when a smooth cloud suggests unsupported shape. Raw observations are required: mean, SD and n cannot reconstruct them. [Allen et al., raincloud paper, version 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC6480976/).

An estimation plot places observations beside the effect and its interval rather than replacing values with mean bars and stars. Name the estimand, reference, signed direction and interval method. For paired changes, connect actual pair IDs and resample independent pairs/subjects; independent groups require their own design. Display bootstrap distributions only when actually computed, with method, iterations and seed recorded. Use zero for differences and one for ratios, with a log scale when appropriate. The existing point/interval example supplies the effect view; its fixture interval is not evidence from a new analysis. [Ho et al., estimation-graphics preprint](https://www.biorxiv.org/content/10.1101/377978v2).

## Prediction: ranking, calibration and decisions

Use held-out or appropriately generated out-of-fold predictions. Identify score direction, positive class, test population and weighting. Do not fit a calibrator or choose a decision threshold on the final test set and then describe that same set as independent final evaluation. Report the actual protocol, including any such limitation.

### ROC

Plot false-positive rate against true-positive rate on axes spanning 0–1:

$$
\mathrm{FPR}=\frac{FP}{FP+TN},\qquad
\mathrm{TPR}=\frac{TP}{TP+FN}.
$$

Compute threshold points from continuous scores, treating tied scores together. Use the empirical curve without decorative smoothing, a restrained chance diagonal, and a legend that identifies model and ROC AUC. Mark an operating point only when its threshold rule is stated. AUC alone does not define sensitivity at a desired specificity or calibration. One-class evaluation data cannot support an ordinary binary ROC. For multiclass comparisons, specify one-vs-rest/one-vs-one and averaging; do not overlay incomparable definitions. [Official ROC definition and thresholds](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html).

### Precision–recall

Show precision $TP/(TP+FP)$ versus recall $TP/(TP+FN)$, with the positive-class prevalence as an explicitly identified reference. This view makes positive prediction quality visible when negatives dominate. Keep model comparisons on the same evaluation population. Specify the curve/integration definition: non-interpolated average precision uses

$$
\mathrm{AP}=\sum_k (R_k-R_{k-1})P_k,
$$

where $P_k$ and $R_k$ are precision and recall at successive thresholds in increasing recall order. AP is not interchangeable with trapezoidal PR area. Retain the implementation's endpoint conventions; do not insert fabricated precision values at unsupported thresholds. No positives means recall-based evaluation is undefined. [Official AP definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html).

### Calibration

Use mean predicted probability on x and observed positive fraction on y; add the identity line. Specify equal-width or quantile bins, boundaries, per-bin counts and handling of empty bins. Empty bins are absent observations, not zero event rates; gaps should remain apparent. A small aligned probability histogram or count panel helps readers assess sparse regions. An interval around bin frequencies needs an actual method and dependence unit. If reporting a binned calibration error, define the weighting, such as $\sum_b(n_b/N)|\bar p_b-\bar y_b|$; it depends on binning. Brier score and log loss also reflect aspects beyond calibration. Do not interpret a raw classifier score as a probability without justification. [Official calibration guide](https://scikit-learn.org/stable/modules/calibration.html).

### Confusion matrix

Label true and predicted axes explicitly and retain the same class order across models. With rows=true and columns=predicted, $C_{ij}$ counts true class $i$ assigned to class $j$. State whether cells are counts, row-normalized, column-normalized or normalized by all observations; show support counts when normalized. Unknown/absent classes and zero denominators require explicit handling. Use a sequential scale, readable numeric labels and sufficient foreground contrast. A count matrix cannot recover ROC/PR curves or calibration, because it describes one decision rule. For many classes, enlarge or split the figure rather than shrinking all labels; add a ranked error summary only when it answers a distinct question. [Official matrix conventions](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html).

## Method agreement and time-to-event evidence

### Bland–Altman

For two measurements $A_i,B_i$ on the same unit, plot their difference $d_i=B_i-A_i$ against their mean $m_i=(A_i+B_i)/2$. Label the subtraction direction and physical units. Show mean bias $\bar d$ and, for a justified approximately normal constant-spread difference model, limits $\bar d\pm1.96s_d$. These are limits for differences, not a confidence interval for the bias and not proof of acceptable interchangeability. Compare them with supplied domain tolerances. High correlation alone does not establish agreement. [Bland and Altman, original paper](https://www-users.york.ac.uk/~mb55/meas/ba.htm).

Inspect changing spread and trends over measurement magnitude. Repeated measurements within units need an appropriate repeated-measures analysis; do not pool them as independent pairs. If confidence bands for bias or limits are shown, distinguish each and state their calculation. Transformations or nonparametric limits require an explicit rationale and back-transformed interpretation. A simple mean-difference plot is preferable to unsupported normal limits. [NIST implementation and interval assumptions](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/blandalt.htm).

### Kaplan–Meier

Define time origin, event and censor codes, follow-up unit, eligibility and delayed entry where applicable. Draw a step function, not a smoothed line. At event time $t_j$, with $n_j$ at risk just before the event and $d_j$ events,

$$
\widehat S(t)=\prod_{t_j\le t}\left(1-\frac{d_j}{n_j}\right).
$$

Show censor marks and an aligned at-risk table at meaningful times. State the convention for event/censor ties and the risk-table timing. A confidence band needs a named estimator/transform; do not invent it from aggregate survival percentages. Sparse tails should be identifiable, and curves should not imply follow-up beyond available observations. Censoring assumptions matter. A median not reached remains not reached. Curve separation is not itself a hazard ratio or causal benefit; competing-risk incidence may require a different estimator. Ordinary event proportions without durations and censoring cannot reconstruct KM curves. [Official survival-estimation documentation](https://www.statsmodels.org/stable/duration.html).

## Many features and multivariate structure

### Volcano

Put a signed effect, often $\log_2$ fold change, on x and $-\log_{10}$ of the stated evidence measure on y. State the contrast direction, whether p-values are raw or adjusted, the correction method and the tested family. The displayed y value and the quantity used for highlighting may differ only when this is explained. Draw thresholds supplied by the analysis; do not make an arbitrary threshold into a scientific conclusion. Keep non-highlighted points neutral and use a small number of meaningful classes with shapes in grayscale. Label a declared subset of features with restrained leaders, avoiding collisions. Zero/underflow p-values need a disclosed plotting floor; missing values stay distinct. Effect size, uncertainty and biological or physical interpretation remain necessary. [Bioconductor's EnhancedVolcano reference manual](https://bioconductor.org/packages/release/bioc/manuals/EnhancedVolcano/man/EnhancedVolcano.pdf).

### PCA scores

State the analysis matrix, feature units, exclusions, transformations, centering and whether features were scaled. PCA centering does not automatically imply unit-variance scaling. Fit the transformation on the permitted development data when evaluating a predictive workflow, then project held-out observations with that fixed transform. Use one point per identified sample/unit, modest markers and group labels or shapes that remain readable in grayscale. Label axes with the actual explained-variance percentages. Keep a shared transformation for comparable panels; independently fitted PC axes are not directly interchangeable. Loading arrows require a stated scaling convention. Ellipses must identify whether they show data spread or an estimated region and how they were computed; omit them when unsupported. A 2D projection can hide important dimensions and does not prove clustering, classification performance or causation. [Official PCA definition](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).

## Reference examples and final checks

The optional [advanced gallery](../scripts/advanced_chart_gallery.py) illustrates the nine added chart types with clearly labeled synthetic fixtures; the [basic gallery](scientific-chart-examples.md) covers the original nine. Treat examples as drawing and definition references, not analysis defaults. Keep computed curve points, bins, matrices, exclusions, estimates and preprocessing settings traceable to their inputs. Use existing analysis outputs instead of recomputing inferential quantities when the task is only restyling.

Inspect both color and grayscale exports at the intended physical size. Verify units, sign/reference lines, uncertainty meanings, colorbar bounds, observation counts, thresholds and text contrast. Simplify labels or split panels before reducing text below a legible size. A valid SVG/PDF or passing numeric check does not establish visual readability. Use [publication-references.md](publication-references.md) when adapting a figure for a specific journal.

## Optional browsing overviews

These contact sheets are for a quick visual survey, not required Agent context. For a selected figure, use its card, exact input and single SVG/PNG from the [index](chart-index.md).

[Color overview](advanced-chart-preview.png) · [Designed print overview](advanced-chart-print-preview.png).

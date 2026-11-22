# Reporting a Model

Read this whenever a report introduces, evaluates or materially changes a model. Everything below belongs in the reader-facing report or a linked appendix, not only in your notes. These are coverage requirements, not mandatory headings: fit them into the user's outline and language. When several models share a protocol, describe the shared part once and spell out the differences.

## Start from what was actually run

Use the supplied code, configs, split manifests, logs and predictions as the evidence. Note the config version or run ID and checkpoint when available. A paper's default architecture or a library's default settings tell you nothing about this run. Keep planned, implemented, trained and evaluated components distinct. If two sources disagree, resolve it before stating a value; otherwise name the conflicting field and why it matters.

For a model that's proposed but not trained, describe the design that's supported and mark training and evaluation as pending. In a requested draft, mark gaps precisely, e.g. `[待补充：每设备 batch size、梯度累积次数及实际优化器更新步数]`. In a finished report, get the missing evidence or state the specific limitation. Never fill a gap with a typical value, a standard loss you assume, or a synthetic result.

## Data and splits

Introduce each dataset before the split table. Connect its original purpose, population, measurements and labels to what this run actually reads and predicts. Distinguish the complete release from the eligible and analyzed subsets, and trace labels from the source table to the model's target. For time-to-event data, name the event, the time origin, the observation unit, follow-up coverage and censoring. Cite the original release or data dictionary and use the experiment's manifest or outputs for the analyzed counts.

Give a compact table per split: source and version, purpose, observation unit, number of independent subjects or groups, number of images or records, and share of the total with an explicit denominator. Add class or target distribution when relevant. Explain inclusion and exclusion, missing labels, preprocessing, and how subsets relate to their parent dataset. Keep planned split sizes separate from final usable counts.

Say how the split was made (random, stratified, grouped, temporal, by site, or a supplied fixed list) and give the seed or manifest ID. Name the unit of independence: repeated scans, both eyes, video frames, patches or augmentations of one subject must not end up on both sides of a split by accident. Describe the actual overlap controls and any remaining leakage risk instead of asserting independence.

Give each set an explicit role:

- **Training** fits model parameters and any learned preprocessing statistics.
- **Validation / development** tunes hyperparameters, stopping, calibration or thresholds and selects checkpoints, as the actual protocol says.
- **Test** estimates performance after all of those choices are fixed. External or temporal test sets need their own source and eligibility description.

Don't infer roles from file names. Spell out calibration sets, nested subsets and shared use. Say where normalization, imputation, feature selection, resampling and augmentation are fit and applied: anything fit on held-out data leaks. For cross-validation, give folds, grouping or stratification, inner vs. outer selection, repeats and seeds, retraining, and how out-of-fold results are aggregated. Say whether an independent final test set exists.

## Architecture and data flow

Draw an overall network diagram, plus an internal diagram for every custom, unfamiliar or materially modified module. [network-diagram-references.md](network-diagram-references.md) lists classic figures worth borrowing conventions from; draw the actual network, not the reference. If the user asks for text only, keep the full trace in prose and mention outside the report that the diagram was omitted.

The overall diagram shows inputs and modalities, where preprocessing ends, backbone stages, task heads, outputs, and where each loss attaches. Mark repeat counts and key tensor shapes in a stated layout such as $B\times C\times H\times W$ or $B\times L\times D$. Draw addition, concatenation and multiplication differently. Show projections, resizing, cropping, reshapes, pooling or broadcasting where a connection needs them. Separate training-only branches, frozen vs. trainable parts, and inference behavior when they differ. Don't draw unknown dimensions as facts.

For every module, say what it's for in this task, what goes in, what it does, what comes out and what consumes it. Standard modules can be brief: name the variant and the settings that matter. For custom or unfamiliar modules, also give:

- The problem it addresses and why this design; keep motivation separate from demonstrated benefit.
- The internal operations in order, with equations, shape changes and key parameters (kernel and stride, projection widths, attention heads, gating functions).
- Every branch and how branches merge; where weights, masks or attention scores come from and how they're normalized or broadcast.
- Which parameters are learned or frozen, how gradients reach the module, any initialization or external reference input, and training vs. inference differences.
- How it differs from the cited standard module. Report ablations if supplied; novelty or added complexity alone doesn't show an improvement.

Then trace one sample or symbolic batch through the network in connected prose. A symbolic trace shows shapes and operations, not observed predictions. Cross-check shapes at every merge, module names, figure labels and formulas against the code. Captions explain symbols, arrow styles, modifications and which paper figure inspired the drawing. Missing code means the design is unresolved, not that you get to invent it.

## Loss

Write the objective that's actually optimized, every term and its weight. For a verified multi-term objective, a convenient notation is

$$
\mathcal{L}_{\mathrm{total}}=\sum_{k=1}^{K}\lambda_k\mathcal{L}_k,
$$

where $K$ is the number of loss terms and $\lambda_k$ their configured weights. This is notation, not an assumed objective. Give each term's formula; "cross-entropy + Dice" isn't enough. Match the implementation on logits vs. probabilities, hard vs. soft targets, class weights, smoothing, masks, ignored labels, reduction denominators and numerical stabilizers. Decoupled weight decay in the optimizer is not an $L_2$ term in the loss.

Define predictions, targets, indices, the sets summed over, weights and normalization next to the formula. Say what error each term penalizes, why it's there and which output it supervises. Include auxiliary or self-supervised targets and their schedules. Keep three things apart: the differentiable training loss, the thresholded evaluation metric, and the validation quantity used for selection. If the exact variant is unknown, say so instead of picking a familiar formula. Follow [math-formatting.md](math-formatting.md).

## Training, stopping and the final checkpoint

Use a compact settings table, split by stage if training has phases. Report actual values, confirmed absences, or the specific missing field:

| Setting | What to report |
|---|---|
| Input and initialization | Input size and modalities, preprocessing and normalization, training augmentation vs. evaluation transforms; pretrained weights and source, frozen vs. trainable modules, phase changes. |
| Batch size | Per-device batch, device count, gradient accumulation, and the effective batch when different. For ordinary equal-size data parallelism, effective batch = per-device batch × devices × accumulation steps; check before applying this elsewhere. |
| Optimizer and loss | Optimizer and its key parameters, initial learning rate, schedule and warmup, weight decay or other regularization, loss terms and weights linked to their formulas. |
| Duration | Planned maximum and actual epochs and optimizer updates, validation interval, any resumed or interrupted run. Minibatches and optimizer updates differ under accumulation; don't derive step counts without the sampler, batching and stopping details. |
| Early stopping | Whether it's on; the monitored quantity and direction, validation cadence, patience and its unit, minimum improvement, warmup, where and why it stopped, whether best weights were restored. If off, say so; a maximum epoch budget isn't early stopping. |
| Final selection | Candidate runs or checkpoints, the selection criterion and direction, evaluation population and aggregation, tie rule, and the selected epoch, step or checkpoint. Say whether the final weights are best, last, EMA/SWA, an ensemble or a refit, and why. |
| Reproducibility | Seeds, framework and key library versions, precision, hardware and device count, determinism settings where they matter; name missing run, config or checkpoint records. Compute time only if supplied and relevant. |

A stopping rule and a checkpoint rule are different things. "Trained for 100 epochs" doesn't say which weights were evaluated. Report the selection rule that was actually used, even if it's imperfect; don't quietly substitute a better one. If test data were used for tuning, thresholds or selection, say so and limit claims of independent test performance.

## Metrics, results and interpretation

For each reported metric give its purpose, formula, symbols, population and denominator, aggregation, unit or range, and which direction is better. With many metrics, use a definitions table or a linked appendix. Explain why the primary metric fits this question (class imbalance, asymmetric error costs, clinically meaningful operating points); don't assume a familiar metric is adequate.

Spell out the details that change the number:

- **Classification:** positive class, decision threshold and where it was chosen, per-class vs. macro/micro/weighted averaging, undefined classes, multilabel handling. Accuracy alone can hide minority-class errors.
- **Segmentation / detection:** evaluation unit (pixel, image, subject, object), overlap or matching rule, empty masks, whether background counts, averaging, postprocessing.
- **Regression / reconstruction:** target scale and inverse transforms, reduction unit, normalization, physical units. RMSE and MSE have different units.
- **Curves and ranking:** the exact ROC/PR or ranking definition, interpolation and averaging (average precision is not trapezoidal PR area). A curve summary has no threshold-specific meaning.

Give formulas for the definitions you actually used, not a generic catalog. If ordinary binary sensitivity and specificity are reported:

$$
\mathrm{Sensitivity}=\frac{TP}{TP+FN},\qquad
\mathrm{Specificity}=\frac{TN}{TN+FP}.
$$

Define $TP$, $TN$, $FP$, $FN$ under the project's positive class and threshold, and say in words that sensitivity measures how many positives are caught and specificity how many negatives are correctly cleared. State how a zero denominator is handled.

Tie each result to the checkpoint, split, sample counts and inference protocol (calibration, thresholds, test-time augmentation, ensembling). Put exact values in a table or figure with a traceable source. Compare baselines only under matched splits and evaluation settings, and flag mismatches instead of presenting them as controlled improvements. Keep percentage points and relative change apart, and keep the unit of uncertainty explicit. Compute intervals or tests only from suitable data with a justified dependence structure; never fabricate significance, uncertainty or per-sample outcomes from summary scores.

Then say what the results mean: the main pattern, its practical meaning, failure cases and subgroups, and what is and isn't supported relative to the objective and baseline. Use ablations to talk about module contributions; don't credit a whole-system gain to a component that wasn't isolated. Validation gains don't prove external generalization or clinical value. If nothing has been evaluated yet, say which evaluation is pending and why it matters; no empty results tables, and an interface demo is not a performance result.

## Final check

A reader should be able to answer: Which data fit the model, which selected it, which tested it? How does an input move through every module that matters? Which objective produced the gradients? What were the actual training budget, stopping rule and chosen weights? What does each score measure, how is it computed, and what follows from it?

Cross-check dataset totals and units, diagram shapes and connections, loss weights and reductions, batch and step definitions, the monitored criterion, the selected checkpoint and the evaluation outputs. Keep the core mechanism and the selection rationale in the main text, with links to full configs or derivations. For a short continuation, link the earlier methods version and describe what changed. For a one-paragraph edit, edit only that paragraph. State each piece of missing evidence once, where it matters.

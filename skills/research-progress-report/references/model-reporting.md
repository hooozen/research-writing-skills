# Model Methods and Performance

Use this reference whenever a progress report introduces, evaluates or materially changes a model. The required detail belongs in the reader-facing report or its explicitly linked appendix, not only in internal notes. Preserve the user's outline and language; these are coverage requirements, not mandatory headings. Apply them to each model or shared protocol, describing shared settings once and differences explicitly.

## Establish what was actually done

Use the supplied implementation, configuration, split manifests, logs and predictions as evidence. Record the model/configuration version or run identifier and checkpoint when available. A paper's default architecture and a library's default settings are not proof of this run's behavior. Distinguish planned, implemented, trained and evaluated components. If sources disagree, resolve the difference before reporting a definite value; otherwise identify the conflicting field and its consequence.

For a proposed or untrained model, explain the supported design and mark training or evaluation as pending. In a requested incomplete draft, use localized markers such as `[待补充：每设备 batch size、梯度累积次数及实际优化器更新步数]`. In a completed report, obtain essential missing evidence or describe its absence as a specific limitation. Do not fill gaps with typical values, assumed standard losses or synthetic outcomes.

## Dataset composition, splits and leakage

Use a compact table for each split's source/version, purpose, observation unit, number of independent subjects/groups, number of images/records and proportion with an explicit denominator. Include class/target distribution where relevant. Explain inclusion/exclusion, missing labels, preprocessing and the relationship between parent datasets and subsets. Separate planned split sizes from final usable counts.

State the split procedure: random, stratified, grouped, temporal, site-based or a supplied fixed split; include the split seed or manifest identifier when available. Identify the independence unit. Repeated scans, both eyes, video frames, patches or augmentations from one subject must not silently become independent train/test samples. Describe actual overlap controls and residual leakage risks rather than asserting independence without evidence.

Give each dataset an explicit role:

- Training fits model parameters and any learned preprocessing statistics.
- Validation/development data tune hyperparameters, stopping, calibration or thresholds, and select checkpoints, according to the actual protocol.
- Final test data estimate performance after those choices are fixed. External or temporal test sets need their own source and eligibility description.

Do not infer roles solely from filenames. Explain calibration sets, nested subsets and shared data use explicitly. State where normalization, imputation, feature selection, resampling and augmentation are fit or applied; transformations fit on held-out data can leak information. For cross-validation, give folds, grouping/stratification, inner versus outer selection, repetition/seeds, retraining procedure and out-of-fold/aggregate reporting as applicable. Say whether an independent final test set exists.

## Architecture, module explanations and data flow

Provide an overall network diagram and detailed internal diagrams for custom, unfamiliar or materially modified modules. Consult [network-diagram-references.md](network-diagram-references.md) for classic-paper conventions. Draw the actual network; a reference image does not substitute for the project's architecture. When the user explicitly requests text only, preserve the trace in prose and state any omitted diagram outside the artifact if it affects completeness.

The overall diagram should locate inputs/modalities, preprocessing boundaries, backbone/stages, task heads, outputs and supervised loss attachment points. Mark repeat counts and key tensor shapes with a defined layout, such as $B\times C\times H\times W$ or $B\times L\times D$. Label addition, concatenation and multiplication distinctly. Show projection, resizing, cropping, reshape, pooling or broadcast when needed to explain a connection. Separate training-only branches, frozen/trainable parts and inference-time behavior when they differ. Do not draw unknown dimensions as facts.

For every module, explain its purpose in this task, input, transformation, output and downstream consumer. Standard modules can be concise with the actual variant and consequential settings. For unfamiliar/custom modules, provide:

- The problem it addresses and the rationale for this design; distinguish motivation from demonstrated benefit.
- Internal operations in execution order, relevant equations, tensor shape changes and key parameters, such as kernels/strides, projection widths, attention heads or gating functions.
- Every branch and how outputs merge; specify where weights, masks or attention scores come from and how they are normalized or broadcast.
- Which parameters are learned or frozen, how gradients/losses reach the module, any initialization or external reference input, and training/inference differences.
- What differs from the cited standard module. Report supplied ablations when available; do not claim that novelty or added complexity itself establishes an improvement.

Trace one actual sample or symbolic batch through the network in connected prose. A symbolic trace illustrates shapes and operations, not observed predictions. Cross-check shapes at merges, module names, figure labels and formulas against the implementation. Captions should explain symbols, arrow conventions, modifications and the cited paper/figure used as visual inspiration. Missing code is a reason to mark a design as unresolved, not to invent its internals.

## Loss functions and optimization targets

Write the objective actually optimized, including each component and its coefficient. For a verified multi-term objective, a useful notation is

$$
\mathcal{L}_{\mathrm{total}}=\sum_{k=1}^{K}\lambda_k\mathcal{L}_k.
$$

Here $K$ is the number of actual loss terms and $\lambda_k$ their configured weights. This is a notation example, not an assumed project objective. Give each component's formula; naming “cross-entropy + Dice” is insufficient. Match logits versus probabilities, hard versus soft targets, class weights, smoothing, masks, ignored labels, reduction denominators and numerical stabilizers to the actual implementation. Explain regularization accurately: decoupled optimizer weight decay must not automatically become an added $L_2$ loss term.

Define predictions, ground truth, indices, sample/pixel/class sets, weights and normalization near the formula. Explain what error each term penalizes, why it is used, and which output it supervises. Include auxiliary/self-supervised targets and schedules when used. Distinguish a differentiable training surrogate from a thresholded evaluation metric and from the validation quantity used for selection. If the exact loss variant is unknown, identify the unresolved definition instead of choosing a familiar formula. Follow [math-formatting.md](math-formatting.md) for rendering.

## Training settings, stopping and final checkpoint

Use a compact settings table, with stage-specific differences when training has multiple phases. Report actual values, confirmed absences or specific missing fields:

| Setting | Required account |
|---|---|
| Input and initialization | Input size/modalities, preprocessing/normalization, training augmentation versus evaluation transforms; pretrained weights/source, trainable/frozen modules and phase transitions. |
| Batch size | Per-device batch size, device count and gradient accumulation; effective batch size when different, including incomplete/variable batches if consequential. For ordinary equal-sized data-parallel batches, effective batch = per-device batch × devices × accumulation steps; do not apply this blindly to a different setup. |
| Optimizer and loss | Optimizer and material parameters, initial learning rate, scheduler/warmup, weight decay or other regularization, objective/components/weights linked to their formulas. |
| Duration | Planned maximum and actually completed epochs and optimizer update steps, validation interval, and any resume or interrupted run. Distinguish minibatch iterations from optimizer updates under accumulation; do not derive a step count without the sampler, batching and stopping details. |
| Early stopping | Whether enabled; monitored validation quantity and minimize/maximize direction, validation cadence, patience unit, minimum improvement, warmup/burn-in when present, actual stopping point/reason and whether best weights were restored. If disabled, say so; a maximum epoch budget alone is not early stopping. |
| Final model selection | Candidate runs/checkpoints, selected validation criterion and direction, evaluation population/aggregation, tie rule if relevant, and selected epoch/step/checkpoint. State whether final weights are best, last, EMA/SWA, an ensemble or a subsequent refit, with the actual procedure and rationale. |
| Reproducibility | Seed(s), framework/relevant library versions, precision, hardware/device count and deterministic settings where material; identify missing run/config/checkpoint records. Include compute/time only when supplied and relevant. |

A best-checkpoint rule and a stopping rule are distinct. “Train for 100 epochs” does not establish which weights were evaluated. Report the actual selection rule even if it is imperfect; do not silently substitute a better protocol. If test performance was used for tuning, thresholding or model selection, disclose that use and limit claims of independent test performance. Separate validation-selected model comparison, final testing and any later retraining.

## Metrics, results and interpretation

For each reported metric, include its purpose, formula, symbol definitions, population/denominator, aggregation, units/range and better/worse direction. Prefer a metric-definition table or a linked mathematical appendix when there are many metrics. Explain why the primary metric answers this task's question, including class imbalance, asymmetric errors or clinically meaningful operating points when relevant; do not infer that a familiar metric is adequate without context.

Specify the details that can change the value:

- Classification: positive class, decision threshold and where it was chosen, per-class versus macro/micro/weighted averaging, missing/undefined classes and how multilabel predictions are handled. Accuracy alone can conceal minority-class errors.
- Segmentation/detection: evaluation unit (pixel, image, subject, object), overlap or matching rule, empty-mask cases, background inclusion, averaging and any postprocessing.
- Regression/reconstruction: target scale and inverse transforms, reduction unit, reference range or normalization and relevant physical units. RMSE and MSE have different units.
- Ranking/curve metrics: the actual ROC/PR or ranking definition, integration/interpolation and averaging convention, such as average precision versus trapezoidal PR area. Do not attach a threshold-specific interpretation to a curve summary.

Give formulas for the actual definitions, not a generic metric catalog. For example, if ordinary binary sensitivity and specificity are reported, define

$$
\mathrm{Sensitivity}=\frac{TP}{TP+FN},\qquad
\mathrm{Specificity}=\frac{TN}{TN+FP}.
$$

Define $TP$, $TN$, $FP$ and $FN$ under the project's positive class and threshold. Explain that sensitivity measures detection of positives and specificity measures exclusion of negatives. A zero denominator needs an explicit undefined-value convention. This example does not prescribe metrics for unrelated tasks.

Tie each result to the model/checkpoint, split, sample counts and inference protocol, including calibration, thresholding, test-time augmentation or ensembling if used. Present the exact values in a table or figure with traceable sources. Compare baselines under matched splits and evaluation settings; identify mismatches instead of presenting them as controlled improvements. Distinguish percentage-point changes from relative changes and keep uncertainty/repetition units explicit. Compute intervals or statistical tests only with suitable data and a justified dependence structure; never fabricate significance, uncertainty or per-sample outcomes from summary scores.

Summarize the main pattern, its practical meaning, failure cases/subgroups and limits. Explain what is supported relative to the stated objective and baseline. Use available ablations to assess module contributions, without attributing a whole-system gain to an unisolated component. Validation gains do not establish external generalization or clinical utility. If no evaluation exists, say which evaluation is pending and why it matters; do not produce an empty performance table or substitute interface demonstrations for model results.

## Final reader and consistency check

A reader should be able to answer: What data fitted the model, what selected it, and what tested it? How does an input move through every consequential module? Which objective produced gradients? What were the actual training budget, stopping rule and selected weights? What does each reported score measure, how is it calculated, and what conclusion follows?

Cross-check dataset totals and units, diagram shapes/connections, loss coefficients/reductions, batch/step definitions, monitored criterion, selected checkpoint and evaluation outputs. Keep crucial mechanism and selection rationale in the main narrative, with explicit links to full configurations or formulas in appendices. For a short continuation, link an accessible prior methods version and describe changes. For a local paragraph edit, revise only that scope; do not force a complete methods scaffold into it. Explain unreported evidence once at its relevant location and retain local qualifications only when they prevent a distinct misinterpretation.

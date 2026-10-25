---
name: research-progress-report
description: "Draft or revise self-contained scientific progress reports for public briefings or lab meetings, including 科研进展报告、阶段性研究总结、项目进度汇报. Explain the whole argument clearly; document model data splits, architecture, module data flow, losses, training, selection, and evaluation in detail. Use another workflow for journal manuscripts or grant proposals."
---

# Research Progress Report

Create audience-facing material in the researcher's voice. Readers should understand the problem, the overall approach, how its parts connect, and what the evidence changes. Preserve the user's language, outline, scope, and explicit instructions. Accuracy and understanding come first; concision removes redundancy, not the explanation needed to follow the argument. Charts and formulas support that explanation.

## Establish the reporting contract

Use settings already supplied in this conversation or in the report being revised. Do not restart intake on a follow-up.

- **Language and output:** use the request's language and Markdown unless specified otherwise; produce standalone HTML when requested.
- **Audience:** obtain an explicit audience description or permission to choose. The calibration profiles are `普遍高学历人群`, `大领域科研人群`, `小领域科研人群`, and `研究伙伴`; custom descriptions are equally valid. If no audience or delegation is available, ask one concise question before the first full draft. If the user explicitly says to decide, use a reasonable profile and state the assumption outside the artifact. Do not ask again when the request already describes the readers.
- **Context:** public report or lab meeting, using the request or existing artifact. If uncertain and consequential, include it in the audience question; otherwise state a reasonable assumption outside the report.
- **Outline:** follow supplied headings or the existing report. Offer the option to supply an outline when another intake question is needed; an optional outline must not create a separate waiting step. Without an outline, organize the report using the evidence. Instructions such as “draft directly” or “organize it” already delegate structure.
- **Scope:** identify the project, period, objective, evidence, methods, results, limitations, and intended next steps. Ask only about missing information that prevents a useful or accurate draft.

Read [references/audience-and-context.md](references/audience-and-context.md) to calibrate depth. For mixed audiences, follow the designated primary audience and layer specialist detail. Ask for a primary audience only if that choice materially affects the report and has not been delegated.

Missing facts are not permission to invent them. If the user wants an incomplete draft or template, use precise localized missing-information markers. For a completed report, either obtain essential missing evidence or describe its absence as a scientific limitation; do not label an unfinished template as final.

## Organize the whole report before writing details

Treat conversations, attachments, notebooks, and previous drafts as authoring sources the audience has not seen. Expertise does not imply knowledge of this project's samples, internal names, baselines, or previous decisions. Include a compact recap for continuation reports unless the user confirms the shared prior material.

Before drafting, identify the report's central question and the answer or current state the evidence supports. Arrange the material into a coherent route: what the reader must understand first, which question each section answers, what evidence belongs there, and how it leads to the next section. Resolve contradictions or missing premises before polishing sentences. Do not organize a report by pasting source fragments or listing components in the order they were encountered.

When describing a module or experiment, place it within the whole project before expanding it: its purpose, inputs, outputs, and connection to other steps. Distinguish training, calibration, ordinary use, and later feedback when they have different roles. Explain how a local dataset or substep relates to its parent; similarly named sets or stages are not automatically the same. Do not invent relationships absent from the sources.

Open with a short, substantive overview that connects the problem, overall approach or flow, and main progress, conclusion, or unresolved question. Let readers see how the parts fit before meeting their details. A list of headings or “this report has five sections” is not an overview. An opening finding must carry enough context to make its meaning clear; do not front-load unexplained abbreviations. For a brief update, integrate the overview into its opening sentences rather than adding a separate section.

Follow a supplied outline's hierarchy, order, and emphasis. Integrate necessary context and connections into it; explain a consequential conflict before materially reordering it unless restructuring is authorized. With delegated structure, organize by the research question, causal or process relationships, and decisions; use chronology when it explains the work. Keep the planning map internal unless requested. This workflow does not require a separate outline-approval turn.

## Expand the overview into connected explanations

Build each section around one clear question. Start with its purpose or main point, then supply the necessary mechanism, design, evidence, and interpretation. Important actions need reasons, comparisons need explicit baselines, and conclusions must answer the question. Explain consequential transitions: which unresolved issue makes the next step necessary? Follow the relevant parts of `question → reason and setup → evidence → interpretation → next decision`; these are reasoning checks, not mandatory headings.

Introduce an unfamiliar concept where the reader needs it: explain the problem it addresses, what it means in ordinary language, and its role or connection here; then give the technical name, abbreviation, or formula when useful. Expanding an English acronym is not an explanation. Familiar disciplinary concepts need no textbook recap, but project-specific roles still need explanation. Remove concepts that do no work in the argument.

For an abstract mechanism or interface, use a supplied case to show input, processing or decision, output, and consequence when this clarifies the explanation. Do not fabricate an observed case. State which parts are implemented, tested, proposed, or undecided. Present the current approach clearly and keep alternatives subordinate unless the report's purpose is to compare them; do not add architecture, parameters, or future branches merely to make the report look complete.

Read [references/writing-and-explanation.md](references/writing-and-explanation.md) when drafting or substantially restructuring a report, or repairing complaints about unclear logic, terminology, or dense language. It provides worked examples and a reader check. Follow [references/output-formats.md](references/output-formats.md) for Markdown or HTML; its headings are examples.

## Make model methods and evaluation explicit

When a report describes a model, read [references/model-reporting.md](references/model-reporting.md). Model detail is required scientific content, not an optional expansion for specialist audiences. A reader must be able to trace how data become predictions, how parameters are learned, which checkpoint is selected, and how performance is measured. Ground the account in supplied code, configuration, dataset manifests, logs, and evaluation outputs; resolve disagreements or identify them explicitly.

Cover all applicable items in the report or an explicitly linked appendix:

- **Dataset splits:** sources, inclusion/exclusion, sample units, counts and proportions, train/validation/test roles, split method and seed or fixed manifest, grouping to prevent leakage, and any cross-validation or external test design. Explain which data fit preprocessing, tune settings or thresholds, select checkpoints, and measure final performance.
- **Architecture and module data flow:** provide an overall network diagram and internal expansion diagrams for unfamiliar, custom, or materially modified modules. Follow a sample or batch from input to output, showing key tensor shapes, branches, fusion operations, repeated blocks, and differences between training and inference. Explain each module's purpose, actual operations, inputs, outputs, and connection to the next module. A backbone name or a sequence of unexplained boxes is insufficient. Read [references/network-diagram-references.md](references/network-diagram-references.md) for verified classic-paper examples; borrow their visual conventions and draw the actual implementation.
- **Loss functions:** give the actual optimized objective as a formula, including component terms, weights, reductions, masks and regularization where applicable. Define symbols and targets, explain each term's purpose and where it attaches to the network, and distinguish the training loss from selection and evaluation metrics.
- **Training and final model selection:** report batch size and effective batch size when different, optimizer, learning rate and schedule, training loss, planned and completed epochs/optimizer steps, validation cadence, early stopping settings or its explicit absence, and the exact checkpoint selection rule. Include preprocessing, augmentation, initialization, frozen/trainable modules, seeds, runtime and numerical settings when they affect reproducibility. Distinguish best-validation, last, averaged, or ensemble weights; explain the actual choice without using final-test performance to tune or select it.
- **Results and performance, when available:** identify the evaluated checkpoint, split, sample size and inference protocol. For every reported metric, explain why it addresses the research question, provide its calculation formula and symbol definitions, and specify aggregation, thresholds, units and direction. Present supported values and comparisons, then summarize what worked, what failed, and what the evidence does and does not establish. Do not turn an implemented interface into measured predictive performance.

Audience and brevity change the presentation and placement of detail, not its accuracy or completeness. Keep the central architecture, custom mechanism, selection rationale and main result understandable in the main narrative; place long configurations, derivations and secondary results in a linked appendix. A brief continuation may link to an accessible, identified prior methods version and specify changes. An explicit local-edit, text-only or no-formula request limits that deliverable; honor it without silently claiming that a full model account is complete.

Missing facts must remain missing. In an incomplete draft, mark the exact unreported field; in a completed report, obtain essential evidence or state the concrete limitation. Use “not used” only when confirmed and “not yet evaluated” when appropriate. Do not invent architecture, split ratios, hyperparameters, stopping rules, metric formulas for unknown implementations, or performance to fill this contract.

## Keep terminology stable and language direct

- Choose a canonical name for each important entity, concept, dataset, and symbol before drafting. At first relevant use, explain a necessary alias or abbreviation and its relationship; then use the canonical name consistently across prose, headings, figures, tables, and formulas. Retain exact code identifiers where needed, with a readable explanation. Do not invent synonyms for variety or merge distinct concepts because their names sound similar. Keep this name map internal unless a glossary would help the reader.
- Use concrete subjects and verbs: who or what takes which input, performs which action, and produces which result? Replace abstract noun chains, invented labels, ornate academic phrasing, and empty transitions with that relationship. A professional tone comes from precise meaning, not terminology density. Replace “as discussed”, “the previous method”, and vague pronouns with clear referents.
- Give each paragraph one purpose. Remove repeated background, inflated significance, and sentences that add no explanation, evidence, or decision. Keep essential introductions, reasons, and bridges even when they cost a few words. An overview establishes relationships; later sections substantiate them, so this useful layering is not redundant repetition. Scale length to the task rather than enforcing a word count.
- Give each detailed fact or shared limitation one main location. Do not recite a full data table in surrounding prose or repeat the same implementation status in an overview, status table, section endings, and conclusion. State shared missing evidence clearly once; repeat a boundary locally only when it prevents a distinct misinterpretation. Prefer “已接通接口，尚未评估分类效果” to repeated abstract statements about what the evidence can support.

## Use charts and formulas to clarify the argument

Plan the representation with the section's question. Prefer a chart for a comparison, pattern, distribution, or uncertainty; a compact table for exact values or mapped roles; a flow or hierarchy diagram for relationships; and a formula for a quantitative definition or calculation. Give them priority when they make the explanation clearer and more precise. Explain why the reader needs to see the representation and what follows from it; a diagram of jargon or an unexplained equation does not repair an unclear argument.

Keep decisive evidence near its claim. Let the chart reveal the pattern, the formula define the relationship, and prose explain its meaning and limit without reciting every label. Move full tables, derivations, protocols, and secondary diagnostics to explicitly linked appendices when they interrupt the narrative. Respect text-only requests and use prose alone for a simple or qualitative update when visuals add no clarity. Do not impose visual quotas or decorative notation.

For model methods and performance, the diagrams and formulas in the model-reporting contract are required representations. Treat the general preference for fewer visuals as a presentation choice within that contract, subject to explicit user restrictions.

## Preserve scientific integrity

- Do not strengthen a claim beyond its evidence. Distinguish correlation from causation, exploratory from confirmatory results, and absence of evidence from evidence of no effect. Include negative or inconclusive results that change the research logic.
- Retain material units, denominators, sample sizes, biological versus technical replicates, time range, statistical methods, and definitions of uncertainty. Repeated images or measurements are not automatically independent subjects.
- Identify each comparison's reference value. Distinguish percentage-point changes from relative percentage changes; do not derive significance or confidence intervals from aggregate counts without an appropriate design and justified assumptions.
- State specific limitations, plausible alternatives, confounders, and data-quality issues in proportion to their impact. Keep proposed explanations and next experiments distinct from completed work. Do not invent owners, deadlines, thresholds, or commitments.
- Preserve supplied citations and source identifiers. Mark missing citations for completion rather than manufacturing bibliographic details.
- Use synthetic data only when the user requests a demonstration or simulation, and label the resulting report, tables, and figures clearly. Missing real evidence must never silently become synthetic results.

## Mathematics

Introduce the quantity and why it matters before its formula. Define symbols, units, reference values, and material assumptions near first use, then explain the implication needed by the audience. Use only supported relationships; notation must not imply an untested model, causal mechanism, or unavailable uncertainty estimate. Keep derivations only when they help assess the claim or are requested.

When formulas appear, read [references/math-formatting.md](references/math-formatting.md). Use `$...$` inline and `$$...$$` on separate lines for display math in Markdown and retained TeX source. Use portable KaTeX constructs, define symbols, and preserve mathematical meaning. Avoid equation numbering, labels, cross-references, custom macros, and document/package commands.

Standalone HTML must actually display formulas when rendered mathematics is requested. Use a local rendering route or semantic MathML as described in the reference; raw dollar-delimited TeX alone is not rendered mathematics. If conversion is uncertain, resolve the expression before claiming a finished mathematical report.

## Figures and exact values

Create the planned figures when the data and output format support them. Give each a specific question or message; combine panels only for a useful shared comparison. Distinguish observed flows from proposed designs and hypotheses. Keep exact values in an adjacent compact table or explicitly linked appendix. Follow a user-named style first.

For clinical, medical-imaging, or healthcare figures, use `clinical-data-chart-style` when available. It is an optional companion: if absent, continue with legible encodings, units, explicit denominators, accessible direct labels, and restrained styling; do not require installation or claim to have applied an unavailable skill. This skill controls the evidence narrative, while the companion controls the visual system.

Choose the encoding from the analytical question. Show uncertainty and individual observations only when supported by the data. Caption the metric, population, unit, denominator where relevant, uncertainty encoding, and source or extraction date when available. Save static figures in `figures/` beside the report with relative links; prefer SVG and provide PNG when compatibility requires it. For a requested single-file HTML, embed figures as described in the output guide.

If essential plot data are missing, supply a specification or table schema in an incomplete draft; do not fabricate a rendered result. Verify the plotted values against the source table.

## Authorial voice and audience boundary

Use established first-person voice when supplied; otherwise prefer neutral research prose such as “本研究” or “本项目”. Keep writing advice, generation commentary, and configuration outside the report. Do not include “根据您的要求”, “I have prepared”, instructions addressed to “你/您/you”, or headings such as `组会汇报口径`, `可以直接说`, `表达建议`, or “what to say”.

Write scientific boundaries as content: “These results do not establish causality,” rather than coaching the speaker. Keep audience/context labels and internal checks hidden unless requested as metadata. Provide speaker notes, coaching, or talk scripts only when requested, as a separate artifact.

Deliver the report first, with any necessary assumption or missing-input note kept concise and outside it.

## Verify before delivery

- Read only the opening and section openings: can a reader retell the problem, overall approach, how the parts connect, and current state? Repair missing links before sentence polishing. A supplied outline remains recognizable.
- Read in order as someone without the authoring context: concepts are introduced before they are needed, important actions have reasons, and inputs, outputs, stages, data relationships, and baselines have clear referents. Names, aliases, and symbols remain consistent across the artifact.
- Opening claims have supporting evidence; experiments have reasons; conclusions and next decisions follow from the data. Training or evaluation descriptions support the role claimed for the method in actual use.
- For model content, check the split, architecture/module data flow, loss formulas, training settings, stopping and checkpoint selection, and available metric formulas/results against [references/model-reporting.md](references/model-reporting.md). Trace one forward pass and each loss to the implementation. Verify that diagrams, tensor shapes, configuration, logs, checkpoint and reported results agree; disclose unavailable details instead of silently omitting them.
- Prose uses concrete actions and readable sentences. Charts and formulas clarify rather than conceal the explanation; overviews, details, and captions each have a distinct purpose. Do not mistake compact terminology for understandable reasoning.
- Numbers, units, denominators, formulas, tables, charts, captions, and sources agree, including derived values and rounding. Compression has not removed essential sample sizes, uncertainty, baselines, or limitations. Observations, interpretations, and plans remain distinguishable.
- Every visible section is scientific content the researcher could show the audience, without drafting instructions or invented evidence.
- Formulas preserve meaning and use the selected output's rendering route. Inspect a rendered preview when available; report any inability to verify rendering rather than claiming it passed.
- Local links resolve; HTML has semantic structure and accessible figures/tables, and works with the agreed offline or single-file constraints.
- Remove resolved placeholders and unused scaffold sections. Describe outstanding gaps honestly when delivering an incomplete draft.

---
name: research-progress-report
description: "Draft or revise concise, self-contained scientific progress reports for public briefings or lab meetings, including 科研进展报告、阶段性研究总结、项目进度汇报. Use clear reasoning, informative charts, and precise formulas in audience-appropriate Markdown or HTML; use another workflow for journal manuscripts or grant proposals."
---

# Research Progress Report

Create audience-facing material in the researcher's voice. Make clear what changed, what supports that conclusion, what remains uncertain, and which decision or experiment follows. Preserve the user's language, outline, scope, and explicit instructions.

## Establish the reporting contract

Use settings already supplied in this conversation or in the report being revised. Do not restart intake on a follow-up.

- **Language and output:** use the request's language and Markdown unless specified otherwise; produce standalone HTML when requested.
- **Audience:** obtain an explicit audience description or permission to choose. The calibration profiles are `普遍高学历人群`, `大领域科研人群`, `小领域科研人群`, and `研究伙伴`; custom descriptions are equally valid. If no audience or delegation is available, ask one concise question before the first full draft. If the user explicitly says to decide, use a reasonable profile and state the assumption outside the artifact. Do not ask again when the request already describes the readers.
- **Context:** public report or lab meeting, using the request or existing artifact. If uncertain and consequential, include it in the audience question; otherwise state a reasonable assumption outside the report.
- **Outline:** follow supplied headings or the existing report. Offer the option to supply an outline when another intake question is needed; an optional outline must not create a separate waiting step. Without an outline, organize the report using the evidence. Instructions such as “draft directly” or “organize it” already delegate structure.
- **Scope:** identify the project, period, objective, evidence, methods, results, limitations, and intended next steps. Ask only about missing information that prevents a useful or accurate draft.

Read [references/audience-and-context.md](references/audience-and-context.md) to calibrate depth. For mixed audiences, follow the designated primary audience and layer specialist detail. Ask for a primary audience only if that choice materially affects the report and has not been delegated.

Missing facts are not permission to invent them. If the user wants an incomplete draft or template, use precise localized missing-information markers. For a completed report, either obtain essential missing evidence or describe its absence as a scientific limitation; do not label an unfinished template as final.

## Build a self-contained argument

Treat conversations, attachments, notebooks, and previous drafts as authoring sources the audience has not seen. Expertise does not imply knowledge of this project's samples, internal names, baselines, or previous decisions. Include a compact recap for continuation reports unless the user confirms the shared prior material.

Before drafting, map the research problem, relevant prior state, unresolved gap, objective, experimental setup, and current change. Supply the minimum background needed to understand each claim; avoid unrelated textbook review. Define project-specific terms, cohorts, metrics, abbreviations, and comparison baselines before first substantive use. Replace “as discussed”, “the previous method”, and similarly vague references with their actual referents.

Inventory the evidence and preserve its identifiers. Separate observation, interpretation, decision, plan, and open question. Build each substantive result around the relevant parts of:

`question → essential rationale and setup → evidence → supported interpretation → next decision`

This is a reasoning check, not a required list of headings. Make each comparison's premise and baseline explicit, and ensure the conclusion answers the question. Organize by research question or decision rather than narrating every activity in chronological order, unless chronology is itself explanatory or the user requests it.

- Follow a supplied outline's hierarchy, order, and emphasis. Integrate missing context or limitations in the nearest suitable section. Explain a consequential conflict before materially reordering it unless the user authorized restructuring.
- With delegated structure, open with the important progress and problems, develop the evidence by research question or decision, and close with unresolved issues and concrete next steps. Scale the structure to the task; a short update does not need an exhaustive section scaffold or repetitive final summary.
- Include enough methods to judge the claim at the selected audience's depth. Do not turn a progress report into a full protocol or literature review unless requested.
- Follow [references/output-formats.md](references/output-formats.md) for Markdown or HTML. Its headings are examples, not requirements.

## Write concisely and prioritize charts and formulas

- State the main finding early. Give each paragraph one inferential purpose, use short direct sentences and concrete terms, and remove repeated background, empty transitions, vague praise, and summaries that merely repeat earlier conclusions. Scale length to the requested scope; do not impose a word count or remove necessary scientific context to appear brief.
- Choose how to express the evidence before writing explanatory prose. Prefer a chart for comparisons, trends, distributions, composition, relationships, or uncertainty; a compact table for exact values or decision matrices; and a formula for metric definitions, transformations, model relationships, or quantitative decision rules. Give charts and formulas priority when they communicate the same information more briefly and accurately than prose.
- Let each representation do its work: a chart reveals a pattern, a table retains exact values, a formula defines a relationship, and prose explains its scientific meaning, limitation, or consequence. Replace redundant prose rather than adding a visual to an unchanged explanation. Do not narrate every plotted value or restate a formula step by step when a short interpretation suffices.
- Keep decisive evidence near its claim; move full tables, derivations, protocols, and secondary diagnostics to explicitly linked appendices when they interrupt the argument. Use a process or concept diagram only when it clarifies actual structure or relationships, and distinguish a hypothesized mechanism from an observed result.
- Use prose alone for a simple fact or qualitative update when a chart or formula adds no clarity. Respect explicit requests for text-only output. Do not add decorative figures, unnecessary notation, or unsupported calculations to meet a visual quota.

## Preserve scientific integrity

- Do not strengthen a claim beyond its evidence. Distinguish correlation from causation, exploratory from confirmatory results, and absence of evidence from evidence of no effect. Include negative or inconclusive results that change the research logic.
- Retain material units, denominators, sample sizes, biological versus technical replicates, time range, statistical methods, and definitions of uncertainty. Repeated images or measurements are not automatically independent subjects.
- Identify each comparison's reference value. Distinguish percentage-point changes from relative percentage changes; do not derive significance or confidence intervals from aggregate counts without an appropriate design and justified assumptions.
- State specific limitations, plausible alternatives, confounders, and data-quality issues in proportion to their impact. Keep proposed explanations and next experiments distinct from completed work. Do not invent owners, deadlines, thresholds, or commitments.
- Preserve supplied citations and source identifiers. Mark missing citations for completion rather than manufacturing bibliographic details.
- Use synthetic data only when the user requests a demonstration or simulation, and label the resulting report, tables, and figures clearly. Missing real evidence must never silently become synthetic results.

## Mathematics

Prefer a concise formula over a long verbal description when defining a quantitative metric, normalization, model, objective, or decision threshold. State its purpose, define symbols, units, reference values, and material assumptions near first use, and explain only the implication needed by the selected audience. Use only supported relationships; notation must not imply an untested model, causal mechanism, or unavailable uncertainty estimate. Keep derivations only when they help assess the claim or are requested.

When formulas appear, read [references/math-formatting.md](references/math-formatting.md). Use `$...$` inline and `$$...$$` on separate lines for display math in Markdown and retained TeX source. Use portable KaTeX constructs, define symbols, and preserve mathematical meaning. Avoid equation numbering, labels, cross-references, custom macros, and document/package commands.

Standalone HTML must actually display formulas when rendered mathematics is requested. Use a local rendering route or semantic MathML as described in the reference; raw dollar-delimited TeX alone is not rendered mathematics. If conversion is uncertain, resolve the expression before claiming a finished mathematical report.

## Figures and exact values

Plan the decisive figures alongside the argument and create them when the available data and output format support a clearer, shorter presentation. Give each figure a specific question or message; combine related panels only when they share a useful comparison, and avoid repeating the same result across multiple charts. Keep exact values in an adjacent compact table or explicitly linked appendix rather than crowding the main narrative. Follow a user-named style first.

For clinical, medical-imaging, or healthcare figures, use `clinical-data-chart-style` when available. It is an optional companion: if absent, continue with legible encodings, units, explicit denominators, accessible direct labels, and restrained styling; do not require installation or claim to have applied an unavailable skill. This skill controls the evidence narrative, while the companion controls the visual system.

Choose the encoding from the analytical question. Show uncertainty and individual observations only when supported by the data. Caption the metric, population, unit, denominator where relevant, uncertainty encoding, and source or extraction date when available. Save static figures in `figures/` beside the report with relative links; prefer SVG and provide PNG when compatibility requires it. For a requested single-file HTML, embed figures as described in the output guide.

If essential plot data are missing, supply a specification or table schema in an incomplete draft; do not fabricate a rendered result. Verify the plotted values against the source table.

## Authorial voice and audience boundary

Use established first-person voice when supplied; otherwise prefer neutral research prose such as “本研究” or “本项目”. Keep writing advice, generation commentary, and configuration outside the report. Do not include “根据您的要求”, “I have prepared”, instructions addressed to “你/您/you”, or headings such as `组会汇报口径`, `可以直接说`, `表达建议`, or “what to say”.

Write scientific boundaries as content: “These results do not establish causality,” rather than coaching the speaker. Keep audience/context labels and internal checks hidden unless requested as metadata. Provide speaker notes, coaching, or talk scripts only when requested, as a separate artifact.

Deliver the report first, with any necessary assumption or missing-input note kept concise and outside it.

## Verify before delivery

- Opening claims have supporting evidence; experiments have reasons; conclusions and next decisions follow from the data.
- Prose is direct and logically ordered. Charts and formulas replace avoidable exposition where useful; paragraphs, captions, and summaries do not repeat the same information without a distinct purpose.
- Numbers, units, denominators, formulas, tables, charts, captions, and sources agree, including derived values and rounding. Compression has not removed essential sample sizes, uncertainty, baselines, or limitations. Observations, interpretations, and plans remain distinguishable.
- A reader from the chosen audience can understand the problem, setup, baselines, and reasoning without the authoring context. A supplied outline remains recognizable.
- Every visible section is scientific content the researcher could show the audience, without drafting instructions or invented evidence.
- Formulas preserve meaning and use the selected output's rendering route. Inspect a rendered preview when available; report any inability to verify rendering rather than claiming it passed.
- Local links resolve; HTML has semantic structure and accessible figures/tables, and works with the agreed offline or single-file constraints.
- Remove resolved placeholders and unused scaffold sections. Describe outstanding gaps honestly when delivering an incomplete draft.

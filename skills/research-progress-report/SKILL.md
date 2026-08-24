---
name: research-progress-report
description: "Draft, restructure, or revise researcher-authored scientific progress reports for public briefings or lab meetings. Use for 科研进展报告、阶段性研究总结、项目进度汇报, especially when language, audience depth, evidence, charts, and Markdown or HTML output must be coordinated; do not route journal-manuscript or grant-proposal requests here unless the requested artifact is explicitly a progress report."
---

# Research Progress Report

Create a report that reads as the researcher's own public or lab-meeting material. Lead with the important progress, conclusions, and problems; develop them through traceable evidence and experimental reasoning; close with unresolved issues, responses, next decisions, and outlook.

## Establish the reporting contract

Determine these settings from the request and supplied material:

- **Language:** `中文`, `English`, or a user-specified language. If unspecified, use the language of the user's request. Keep the report consistently in that language except for established names, symbols, or quotations.
- **Output:** Markdown by default; standalone semantic HTML when requested.
- **Audience:** `普遍高学历人群`, `大领域科研人群`, `小领域科研人群`, or `研究伙伴`. Read [references/audience-and-context.md](references/audience-and-context.md) when selecting background depth, terminology, methods detail, and emphasis.
- **Context:** public report or lab meeting. This affects disclosure, explanation, and operational detail; it does not change the evidence standard.
- **Scope:** project and reporting period, objectives or hypotheses, material progress, methods or interventions, results, source data, citations, problems, and intended next steps.

**Audience is a required user decision.** Before drafting any report body, verify that the user has explicitly selected one of the four audience profiles or described a custom audience for this artifact. If not, stop and ask the user to choose; present the four options with brief distinctions and wait for the answer. Do not infer the audience from the field, terminology, source complexity, intended venue, or presumed expertise. If the audience is mixed, ask which group is primary and use layered detail for the rest. When context is also missing, ask for public report or lab meeting in the same clarification; context never substitutes for audience.

Ask further clarification only when another missing choice would materially change the artifact and cannot be inferred safely. Otherwise proceed with the stated settings. If factual inputs are insufficient, produce a useful structure with localized missing-information markers such as `[待补充：样本量与统计方法]` or `[TO SUPPLY: sample size and statistical method]`; never invent data, citations, experiments, causes, or outcomes.

## Build the report

1. Inventory the supplied claims and evidence. Distinguish observation, interpretation, decision, plan, and open question. Preserve source identifiers so every number and citation remains traceable.
2. Decide the report's central message: what changed during this period, what the strongest evidence supports, what remains blocked or uncertain, and what decision or action follows.
3. Use a flexible **summary–detail–summary** structure:
   - Open with the most important progress, conclusions, problems, and any decision required.
   - Organize the body by research question, hypothesis, work package, or decision—not merely by chronology. Present the evidence behind each opening claim.
   - Close by restating the supported conclusions, naming unresolved problems and proposed responses, and specifying next steps and outlook.
4. For each substantive result, preserve the reasoning chain as applicable:

   `objective or question → prior evidence or rationale → action or experimental choice and why → design and controls → observation or data → analysis → supported interpretation → implication or next decision`

   This is a completeness principle, not a mandatory list of headings. Adapt the visible structure to the project and audience. Every non-obvious action needs a reason; every conclusion needs evidence; every result should connect back to the objective or decision it informs.
5. Calibrate detail using the audience reference. Define only the concepts the audience is unlikely to know. Retain enough methodological detail to evaluate the claim, without turning a progress report into a protocol or literature review unless requested.
6. Use [references/output-formats.md](references/output-formats.md) for the selected output. The examples are adaptable scaffolds, not compulsory headings.

## Maintain scientific integrity

- Do not strengthen the user's claim beyond the evidence. Separate correlation from causation, exploratory findings from confirmatory results, and absence of evidence from evidence of no effect.
- Report negative, inconclusive, or failed results when they affect the research logic. Explain what they rule out, fail to rule out, or motivate next.
- For quantitative claims, retain the relevant units, denominator, sample size, biological and technical replicate distinction, time range, uncertainty or error definition, and statistical method when supplied and material.
- State limitations, alternative explanations, confounders, and data-quality issues in proportion to their impact. Do not use generic limitation boilerplate.
- Preserve citation details exactly. If a source is missing, mark it for completion instead of fabricating a title, DOI, author, or URL.
- Keep plans and proposed solutions distinct from completed work and demonstrated results.

## Visualize key data without losing detail

Use a chart when comparison, trend, distribution, composition, relationship, or uncertainty is materially easier to understand visually. Keep the corresponding numerical table adjacent to the figure or in a clearly linked appendix so readers can locate exact values.

- If the user names a local chart-style skill, load and follow it before creating or restyling figures.
- For clinical, medical-imaging, or healthcare data, load the installed `clinical-data-chart-style` skill and follow its required style guide. That skill controls the figure's visual system; this skill controls the report logic and evidence narrative.
- Outside those domains, use another user-specified or domain-appropriate local chart skill when available. Do not claim that a style skill was used when none matched. Retain the same evidence-first principles: legible encodings, direct units, explicit denominators, accessible labels, restrained decoration, and exact agreement with the data table.
- Choose chart type from the analytical question, not decoration. Show uncertainty and individual observations where scientifically important and supported by the data.
- Give each figure a caption that identifies the message or metric, population or sample, units, denominator where relevant, uncertainty encoding, and data source or extraction date when available.
- Store generated figures in a `figures/` directory beside the report and link them relatively. Prefer SVG for text-heavy static charts and high-resolution PNG when compatibility requires it.
- When source data are missing or incomplete, supply a chart specification and table schema with missing markers; do not fabricate a rendered result.

## Use an authorial, report-ready voice

Write as material the researcher can present or publish, not as an AI explaining its answer. Do not place phrases such as “根据您的要求”, “以下是为您生成的报告”, “I have prepared”, or commentary about prompting inside the report. Use the project's established first-person voice if provided; otherwise prefer neutral constructions such as “本研究”, “本项目”, or the equivalent in the selected language. Avoid synthetic transitions, inflated significance, repetitive summaries, and promotional adjectives.

Deliver the finished report first. Keep any necessary assumptions or missing-input notes outside the report and concise so they do not contaminate the artifact's authorial voice.

## Enforce the speaker–audience boundary

The report is an audience-facing artifact. By default, include only material that the researcher could directly show, publish, or say to the selected audience. Keep planning logic, writing advice, safety coaching, and instructions to the researcher outside the report.

- Do not create headings or passages such as `组会汇报口径`, `可以直接说`, `可以说与不能说`, `表达建议`, `写作说明`, `演讲提示`, “what to say”, “what not to say”, or “suggested wording”. These describe the drafting process rather than the research.
- Do not address the researcher as “你/您/you” inside the report or tell them how to present a claim.
- Express scientific boundaries as audience-facing content. Write “These results do not establish causality,” not “Do not say that the results prove causality.”
- Treat audience profile, context selection, internal quality checks, and content-generation instructions as hidden configuration. Do not expose them as report sections or metadata unless the user explicitly requests that information in the artifact.
- Add speaker notes, delivery coaching, anticipated questions, or a talk script only when the user explicitly requests them. Return them as a separate artifact after the report, never interleaved with the report body. Even there, prefer direct spoken text or concise stage cues over “can say/cannot say” coaching.

Apply a projection test to every visible section: if showing it to the audience would reveal the drafting process, instruct the speaker, or sound absurd as part of a scientific report, remove it or rewrite it as scientific content.

## Verify before delivery

Confirm that:

- the opening claims reappear with supporting evidence in the body;
- measures and experimental choices have reasons, and conclusions have evidence;
- numbers, units, tables, charts, captions, and cited sources agree;
- the depth and terminology fit the selected audience and context;
- problems lead to concrete responses, decision criteria, or next experiments rather than vague promises;
- completed work, interpretation, uncertainty, and future plans remain distinguishable;
- every heading names scientific content rather than writing, speaking, or generation advice;
- every visible paragraph passes the projection test and respects the speaker–audience boundary;
- Markdown links resolve, or the HTML is valid, semantic, accessible, and free of unnecessary remote dependencies;
- no AI-facing preamble, invented evidence, or unfilled scaffold instruction remains in the report.

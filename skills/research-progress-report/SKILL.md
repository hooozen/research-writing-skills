---
name: research-progress-report
description: "Draft or revise self-contained scientific progress reports for public briefings or lab meetings, including 科研进展报告、阶段性研究总结、项目进度汇报. Explains the evidence in plain language and documents dataset backgrounds, model data splits, architecture, losses, training, checkpoint selection and evaluation in full. Not for journal manuscripts or grant proposals."
---

# Research Progress Report

Write a report the researcher can hand to their audience as is. A reader who has never seen the chat, the notebooks or earlier drafts should come away knowing what problem the project tackles, how the approach works, what the evidence shows, and what happens next.

Keep the user's language, outline, scope and explicit instructions. Accuracy comes first, then clarity, then brevity: cut repetition, never the explanation a reader needs to follow the argument.

## 1. Settle the basics, then stop asking

Reuse whatever the conversation or the existing report already settles. Don't restart intake on a follow-up.

| Setting | Default | Ask only if… |
|---|---|---|
| Language and format | The request's language; Markdown. HTML when asked. | — |
| Audience | None. You need a description or permission to choose. | Nobody has described the readers or said "you decide". |
| Context | Public briefing or lab meeting, whichever the material suggests. | Getting it wrong would change the report. |
| Outline | The user's outline or the existing report's structure; otherwise organize it yourself. | You're already asking something else. Offer it in the same message; never as a separate wait. |

If you must ask, ask once, in one short message. Calibration profiles for the audience are `普遍高学历人群`, `大领域科研人群`, `小领域科研人群` and `研究伙伴` (see [references/audience-and-context.md](references/audience-and-context.md)); a free-form description works just as well. When the user says "you decide", pick a profile and mention the assumption outside the report. "直接写" or "你来组织" already hands you the structure.

Missing facts are never an invitation to invent them. In a draft or template, mark each gap precisely (`[待补充：对照组 n 与标准差]`). In a finished report, either get the evidence or state its absence as a limitation.

## 2. Plan the whole report before writing any section

Treat everything you were given (chat, attachments, notebooks, drafts) as material the reader has not seen. Expert readers still don't know this project's samples, internal names, baselines or earlier decisions, so a continuation report needs a short recap unless the user confirms the audience already has it.

Before drafting, answer privately:

1. What is the one question this report answers, and what is the current answer?
2. What does the reader need to understand first, second, third?
3. Which evidence supports each step, and why does each step lead to the next?

Fix contradictions and missing premises now; polishing sentences won't repair a broken route. Don't assemble the report from source fragments in the order you happened to read them.

Open with a real overview: the problem, the overall approach, how the parts connect, and where things stand. "本报告分为五部分" is a table of contents, not an overview. For a short update, the first two sentences do this job; no separate section.

With a supplied outline, keep its hierarchy and emphasis and fill in the missing connections. Explain before reordering anything substantial. With no outline, organize around the research question and the cause-and-effect or process order; use chronology only when the timeline is the point.

When asked to revise an existing report, put the requested explanations in that report. Give readers the definitions, methods and evidence they need to understand the result there. Use source links for attribution and verification and internal links for supporting details.

## 3. Write sections that each answer one question

Open every section with its question or main point, then give the mechanism, design, evidence and interpretation it needs. Actions need reasons. Comparisons need an explicit baseline. Conclusions must answer the question asked. At a big transition, say what is still unresolved and why the next step addresses it.

Introduce an unfamiliar concept where it is first needed: the problem it solves, what it is in plain words, its role here, and only then its technical name or formula. Spelling out an acronym is not an explanation.

Introduce each dataset used in the reported work, including external evaluation and auxiliary training data. Describe who released it, who or what it covers, what one record contains, the usable fields and timeline, and which records the experiment used. For longitudinal or survival data, give the time origin and the observed duration or follow-up coverage where available. A short, labeled example can make an unfamiliar record understandable. Verify public dataset details and version against primary sources such as the release, dictionary or dataset paper. Verify experiment counts and local availability against the actual run artifacts.

Pick one name for each important thing and keep it everywhere: prose, headings, figures, tables, formulas. If the sources use an alias, mention it once. Don't vary names for style, and don't merge two things because their names sound alike.

Say who does what to what, with what result. Not "构建协同治理闭环", but what actually runs, on which input, producing which output. A professional tone comes from precise meaning, not from dense terminology.

[references/writing-and-explanation.md](references/writing-and-explanation.md) has worked examples, a style guide for Chinese and English prose, and a reader test. Read it when drafting, restructuring, or fixing a report someone called unclear.

## 4. Models: explain them completely

When the report describes a model, read [references/model-reporting.md](references/model-reporting.md). This detail is required for every audience; the audience only changes where it lives (main text or a linked appendix). A reader must be able to trace:

- **Data splits.** Source, unit, counts, train/validation/test roles, how the split was made, and what prevents leakage.
- **Architecture and data flow.** An overall network diagram, plus an internal diagram for any custom or modified module. Follow one sample from input to output with tensor shapes. See [references/network-diagram-references.md](references/network-diagram-references.md) for classic diagrams worth borrowing conventions from.
- **Loss.** The actual objective as a formula, every term defined, kept separate from evaluation metrics.
- **Training and checkpoint choice.** Batch size, optimizer, learning-rate schedule, planned vs. actual duration, early stopping (or its absence), and the exact rule that picked the final weights.
- **Results, if any.** Which checkpoint, split and protocol; each metric's purpose and formula; what the numbers do and don't show.

Ground every value in supplied code, configs, manifests, logs and outputs. Unknown stays unknown: never fill a split ratio, hyperparameter, loss or score with a "typical" value. An explicit text-only, no-formula or one-paragraph request limits the deliverable; respect it, and don't pretend the model account is complete.

## 5. Figures, tables and formulas

Choose the representation from the section's question: a chart for comparisons, patterns, distributions and uncertainty; a compact table for exact values; a diagram for structure and flow; a formula for a definition or calculation. Before a figure or formula, say why the reader needs it; after it, say what follows from it. Don't add visuals to fill a quota, and respect text-only requests.

- Keep decisive evidence next to its claim and move long tables, derivations and secondary diagnostics to a linked appendix.
- Number figures and tables separately in reading order and give each a descriptive title and a stable destination link. Link references such as “Figure 1” or “Table 2” to the item. Add a compact linked index when the document is long enough to benefit. Preserve existing anchors when editing and update displayed references if numbering changes. Captions name the metric, population, unit, denominator, uncertainty and source where applicable.
- Save figures in `figures/` next to the report with relative links. Prefer SVG, add PNG if needed.
- Draw figures only from real data. If plot data are missing, give a table schema in a draft, not a fake chart.
- For chart styling, use `scientific-chart-style` if it's installed (saturated blue/orange/purple, plus a grayscale print mode). It's optional: without it, keep clear encodings, units, denominators and direct labels, and don't claim to have used it.
- For formulas, read [references/math-formatting.md](references/math-formatting.md). Write the editable equation in the report as LaTeX math and render it as selectable, structured mathematics in the intended reading view. Use `$...$` inline and `$$...$$` on their own lines in Markdown. Use native MathML or a text-and-MathML LaTeX renderer in HTML, and retain the TeX source.

For output layout, follow [references/output-formats.md](references/output-formats.md). For HTML, start from [assets/report-template.html](assets/report-template.html) and follow [references/html-report.md](references/html-report.md).

## 6. Scientific integrity

- Claims never outrun evidence. Keep correlation vs. causation, exploratory vs. confirmatory, and "no evidence" vs. "evidence of no effect" distinct. Keep negative and inconclusive results that matter.
- Keep units, denominators, sample sizes, replicate types, time ranges, statistical methods and uncertainty definitions. Repeated images of one subject are not independent subjects.
- Name the reference for every comparison. Percentage points and relative percent are different numbers. Don't derive significance or intervals from aggregate counts.
- State limitations and confounders in proportion to their impact. Keep plans separate from completed work. Never invent owners, deadlines or thresholds.
- Keep supplied citations; mark missing ones instead of fabricating them.
- Use synthetic data only when the user asks for a demonstration, and label it visibly in the report, tables and figures.

## 7. Keep yourself out of the report

The report is in the researcher's voice. Use the voice the user established; otherwise neutral research prose ("本研究", "本项目", "we"). The report must not contain "根据您的要求", "I have prepared", instructions to the reader, or sections such as `组会汇报口径`, `可以直接说`, `表达建议`. Write limits as science ("这些结果不能说明因果关系"), not as speaker coaching. Audience labels and internal checks stay hidden unless requested. Speaker notes or a talk script are a separate deliverable, only on request.

Deliver the report first. Put any assumption or missing-input note briefly after it, outside the artifact.

## 8. Check before delivering

- **Skim test.** Read only the opening and each section's first lines. Can you retell the problem, approach, how parts connect, and current status? If not, fix the structure before the sentences.
- **Newcomer test.** Read in order as someone who never saw the sources. Every concept appears before it's needed, every action has a reason, every "it", "the previous method" or "this set" has a clear referent, and names stay consistent.
- **Evidence test.** Each opening claim has support; each conclusion and next step follows from the data.
- **Model test.** Trace one forward pass and each loss term to the implementation; diagrams, shapes, configs, logs, checkpoint and results agree. Disclose what's unavailable.
- **Numbers test.** Values, units, denominators, rounding, tables, charts and captions agree. Compression hasn't dropped sample sizes, uncertainty, baselines or limitations.
- **Rendering test.** Open the intended reading view. Check representative inline and display equations for correct layout and selectable math, and follow links to the numbered figures and tables. Validate the HTML layout when relevant. State which render checks could not be performed.
- **Cleanup.** No leftover placeholders in a final report, no unused scaffold sections, no drafting notes.

# Output Formats

The user's outline wins over everything below. Use this scaffold only when you're organizing the report yourself, and drop sections a short report doesn't need. Section names are examples: adapt them to the language, project and evidence.

Audience and context settings shape the writing; they aren't report content. Add an event, venue or audience line only when the user supplies it and it belongs on the page. Never add writing advice, speaking tips or "what to say" sections.

For model content, [model-reporting.md](model-reporting.md) applies in every format: splits, diagrams, data flow, loss formulas, training and checkpoint selection, metric definitions and results. A short or qualitative scaffold doesn't waive it; explicit text-only, no-formula or local-edit requests do limit it.

## Markdown

Use GitHub-flavored Markdown unless the target platform needs another dialect. Formulas follow [math-formatting.md](math-formatting.md).

A scaffold for a substantial report:

```markdown
# [Title that names the project and the period]

> 报告期：[...] · 汇报人：[...]

## 概述

[Problem → overall approach → how the parts fit → what is now supported or still open. Connected prose, not a list of section names. Add a flow diagram if it makes module roles or data relationships clearer.]

## 背景与目标

[Only what's needed to read the evidence: the problem, the prior baseline, the gap, essential terms, the success criterion.]

## [A heading that states the finding or the question]

[The section's question, why it follows from the approach, and the design or controls. Introduce new concepts by the problem they solve.]

[Formula, if it replaces a longer explanation; symbols defined right below.]

![Alt text that says what the figure shows](figures/example.svg)

*图 1. [Metric; population; unit; uncertainty; source.]*

[Compact table of exact values, or a link to the appendix table.]

[What the evidence supports, its main limit, and the decision that follows.]

## 待解决问题与下一步

[Prioritized open questions and the test or action each one motivates.]

## 参考文献

[Keep the supplied citation style and identifiers.]

## 附录：完整数值与补充细节

[Full tables, derivations, diagnostics, linked from the main text.]
```

Notes on using it:

- Drop empty metadata and irrelevant sections, never the premises needed to read the evidence. "Background" can merge into the overview or first section when that stays clear.
- Continuation reports keep a short recap unless the user confirms the audience already shares it.
- Keep the exact-value table next to its chart when practical; otherwise link to the appendix table.
- A simple qualitative update can be prose only.
- Add a closing summary only if it contributes a decision or a cross-result insight the opening didn't.
- Keep names, aliases and symbols consistent and run the reader test in [writing-and-explanation.md](writing-and-explanation.md).

## HTML

When the user asks for HTML, follow [html-report.md](html-report.md) and start from its template: a complete, offline, single reading-column document with an automatic contents rail, a figure viewer, print styles and native MathML formulas. Don't hand-roll a new page design for each report.

## Missing inputs

Localize placeholders to the report language and make them specific enough to be actionable:

- Good: `[待补充：对照组 n、均值、标准差及统计检验]`
- Good: `[TO SUPPLY: extraction date and denominator for the cohort percentage]`
- Avoid: `[补充内容]`, `TBD`, fabricated examples that resemble real results, or prose implying the missing claim is already established.

Placeholders are acceptable in a requested template or incomplete draft. Remove all resolved placeholders before presenting a report as final.

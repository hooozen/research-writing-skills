# Output Formats

Adapt section names to the selected language, project, audience, and available evidence. Start with a substantive overview: the problem, overall approach or flow, how the parts connect, and main progress or unresolved question. Then develop the details in the order needed to understand them. An opening conclusion still needs enough context to be intelligible. Prefer informative charts and precise formulas when they clarify the explanation, retaining the plain-language purpose and interpretation needed by the reader.

Audience and context choices configure the writing but are not automatic report content. Include an event, venue, or audience label only when the user supplies it and it naturally belongs in the published or projected artifact. Never add internal writing guidance, speaking advice, or “what to say” sections to either format.

A user-supplied outline takes precedence over the scaffold below. Preserve its recognizable hierarchy and emphasis while completing the scientific logic. Use this scaffold when structure is delegated or no outline is supplied; omit redundant sections in short reports.

For model content, follow [model-reporting.md](model-reporting.md) in either format. Integrate dataset composition/splits, overall and custom-module architecture diagrams, module explanations and data flow, actual loss formulas, training/stopping/checkpoint selection settings, and available performance with metric purposes/formulas and interpretation into the supplied structure. Use explicitly linked appendices for extensive details, with the central mechanism and selection rationale still clear in the main text. A qualitative scaffold or brevity preference does not waive these requirements. Respect explicit text-only/no-formula requests and local-edit scope, and distinguish those limited deliverables from a complete model report.

## Markdown

Use ordinary GitHub-flavored Markdown unless the target platform imposes another dialect.

When formulas appear, follow [math-formatting.md](math-formatting.md): use `$...$` for inline math and `$$...$$` for display math, and keep all commands KaTeX-compatible.

For a substantial report without a supplied outline, a useful scaffold is:

```markdown
# [Project or progress-report title]

> Reporting period: [...] \
> Presenter or team: [...]

## Overall approach and current progress

[The problem, the overall route to address it, how the main parts fit, and what is now supported or unresolved; use connected prose rather than a directory of section titles]

[A flow or hierarchy diagram when it clarifies module roles, data movement, or parent–child relationships; explain names before relying on them]

## Background and objective

[Only the research problem, prior baseline, unresolved gap, essential terms, and success criteria needed to understand the evidence]

## [Research question or work package]

[The section's question or point, why it follows from the overall approach, and necessary design or controls. Introduce an unfamiliar concept through the problem it addresses and its role here before technical detail.]

[Metric definition or quantitative relationship as a formula when it replaces a longer explanation; define symbols, units, and assumptions nearby]

![Meaningful alt text](figures/example.svg)

*Figure 1. [Message or metric; sample/population; units; uncertainty; source.]*

[Compact exact-value table here, or an explicit link to the full table in an appendix]

[Short interpretation: what the evidence supports, its material limitation, and which decision follows. Use a supplied input–processing–output example if a mechanism would otherwise remain abstract.]

## Open questions and next steps

[Prioritized uncertainties and the actions or discriminating tests they motivate; use a compact table if it makes the mapping clearer]

## References

[Preserve supplied citation style and identifiers]

## Appendix: exact values and supporting detail

[Full tables, derivations, or diagnostics that are explicitly linked from the main report, when needed]
```

Omit empty metadata and irrelevant sections, but do not omit premises required to understand the evidence. The background heading is optional only when its content is integrated clearly into the opening or first relevant section. For a continuation report, retain a compact recap unless the user explicitly confirms that the audience shares the specific prior material. Use appendices for detailed protocols, full tables, supplementary diagnostics, or specialist material that would interrupt the main narrative. Keep the exact-value table adjacent to its chart when practical; otherwise link explicitly to the appendix table. Use prose alone for simple or qualitative updates that do not require the model diagrams and formulas specified above, or when the user explicitly restricts the format. Add a closing synthesis only when it contributes a decision or cross-result insight beyond the opening. Keep names, aliases, and symbols consistent in both formats, and apply the reader check in [writing-and-explanation.md](writing-and-explanation.md).

## HTML

Produce a complete HTML document when HTML is requested:

- Include `<!doctype html>`, an accurate `<html lang="...">`, UTF-8 charset, viewport metadata, and a meaningful `<title>`.
- Use semantic landmarks such as `<header>`, `<main>`, `<section>`, `<figure>`, `<figcaption>`, and `<footer>`.
- Use one `<h1>` and a correctly nested heading hierarchy.
- Put tabular data in `<table>` with `<caption>`, `<thead>`, `<tbody>`, and scoped header cells. Preserve units in headers and exact values in cells.
- Give every informative image meaningful `alt` text. Do not duplicate the full visible caption in the alt text.
- Embed restrained print-friendly CSS in `<style>` unless the user supplies a stylesheet. Use no remote dependencies by default. A requested rendered-math output permits the minimal local rendering assets it needs; use static rendering or semantic MathML when practical.
- Keep figures in a sibling `figures/` directory and use relative paths. For an explicitly requested single-file artifact, embed figures as inline SVG or image data, including accessible descriptions. The request already authorizes embedding; ask about size only if an actual delivery limit is at risk.
- Ensure the reading order and meaning remain intact without color and when printed.
- For formulas, follow [math-formatting.md](math-formatting.md). Check that a host renderer recognizes the chosen delimiters; a standalone file must contain a working offline rendering route when displayed mathematics is requested.

Use responsive tables or wrappers where needed, but do not hide columns or exact values on small screens.

## Missing inputs

Localize placeholders to the report language and make them specific enough to be actionable:

- Good: `[待补充：对照组 n、均值、标准差及统计检验]`
- Good: `[TO SUPPLY: extraction date and denominator for the cohort percentage]`
- Avoid: `[补充内容]`, `TBD`, fabricated examples that resemble real results, or prose implying the missing claim is already established.

Placeholders are acceptable in a requested template or incomplete draft. Remove all resolved placeholders before presenting a report as final.

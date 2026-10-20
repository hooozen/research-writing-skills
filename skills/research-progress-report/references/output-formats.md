# Output Formats

Adapt section names to the selected language, project, audience, and available evidence. Lead with the material progress and provide its evidence and next implications; scale the structure to the requested length. Prefer informative charts and precise formulas over lengthy exposition when they improve clarity and accuracy. Use brief prose to connect evidence to conclusions and decisions, without repeating all values, definitions, or captions.

Audience and context choices configure the writing but are not automatic report content. Include an event, venue, or audience label only when the user supplies it and it naturally belongs in the published or projected artifact. Never add internal writing guidance, speaking advice, or “what to say” sections to either format.

A user-supplied outline takes precedence over the scaffold below. Preserve its recognizable hierarchy and emphasis while completing the scientific logic. Use this scaffold when structure is delegated or no outline is supplied; omit redundant sections in short reports.

## Markdown

Use ordinary GitHub-flavored Markdown unless the target platform imposes another dialect.

When formulas appear, follow [math-formatting.md](math-formatting.md): use `$...$` for inline math and `$$...$$` for display math, and keep all commands KaTeX-compatible.

For a substantial report without a supplied outline, a useful scaffold is:

```markdown
# [Project or progress-report title]

> Reporting period: [...] \
> Presenter or team: [...]

## Main finding and current decision

[Most important supported advance or limitation, enough context to understand its significance, and the decision it changes]

## Background and objective

[Only the research problem, prior baseline, unresolved gap, essential terms, and success criteria needed to understand the evidence]

## [Research question or work package]

[Brief rationale, action, and consequential design or controls]

[Metric definition or quantitative relationship as a formula when it replaces a longer explanation; define symbols, units, and assumptions nearby]

![Meaningful alt text](figures/example.svg)

*Figure 1. [Message or metric; sample/population; units; uncertainty; source.]*

[Compact exact-value table here, or an explicit link to the full table in an appendix]

[Short interpretation: what the evidence supports, its material limitation, and which decision follows]

## Open questions and next steps

[Prioritized uncertainties and the actions or discriminating tests they motivate; use a compact table if it makes the mapping clearer]

## References

[Preserve supplied citation style and identifiers]

## Appendix: exact values and supporting detail

[Full tables, derivations, or diagnostics that are explicitly linked from the main report, when needed]
```

Omit empty metadata and irrelevant sections, but do not omit premises required to understand the evidence. The background heading is optional only when its content is integrated clearly into the opening or first relevant section. For a continuation report, retain a compact recap unless the user explicitly confirms that the audience shares the specific prior material. Use appendices for detailed protocols, full tables, supplementary diagnostics, or specialist material that would interrupt the main narrative. Keep the exact-value table adjacent to its chart when practical; otherwise link explicitly to the appendix table. Use prose alone when a simple or qualitative update does not benefit from a chart or formula. Add a closing synthesis only when it contributes a decision or cross-result insight beyond the opening.

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

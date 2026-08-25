# Output Formats

Adapt section names to the selected language, project, audience, and available evidence. Preserve the summary–detail–summary logic even when the visible headings differ.

Audience and context choices configure the writing but are not automatic report content. Include an event, venue, or audience label only when the user supplies it and it naturally belongs in the published or projected artifact. Never add internal writing guidance, speaking advice, or “what to say” sections to either format.

A user-supplied outline takes precedence over the scaffold below. Preserve its recognizable hierarchy and emphasis while completing the scientific logic. Use this scaffold only when the user asks the agent to organize the report, or to fill a genuine gap that cannot be integrated clearly into the supplied outline.

## Markdown

Use ordinary GitHub-flavored Markdown unless the target platform imposes another dialect. When no outline is supplied, a useful scaffold is:

When formulas appear, follow [math-formatting.md](math-formatting.md): use `$...$` for inline math and `$$...$$` for display math, and keep all commands KaTeX-compatible.

```markdown
# [Project or progress-report title]

> Reporting period: [...] \
> Presenter or team: [...]

## Key progress and conclusions

- [Most important supported advance, with enough problem context to understand why it matters]
- [Second advance, limitation, or changed conclusion]
- [Main unresolved problem or decision required]

## Background and research gap

[Research object and larger problem; relevant prior state or baseline; unresolved gap; essential project-specific terms. Calibrate depth to the selected audience.]

## Objective and success criteria

[The question or hypothesis, current scope, and criteria used to judge progress]

## [Research question or work package]

### Rationale and action

[What was done or changed, and why this action was chosen]

### Results and evidence

![Meaningful alt text](figures/example.svg)

*Figure 1. [Message or metric; sample/population; units; uncertainty; source.]*

| Condition | n | Metric (unit) | Uncertainty | Notes |
|---|---:|---:|---:|---|
| [...] | [...] | [...] | [...] | [...] |

### Interpretation and implications

[What the evidence supports, what it does not establish, and which decision follows]

## Problems, risks, and responses

| Problem or uncertainty | Evidence / impact | Current explanation | Response or discriminating test | Decision criterion |
|---|---|---|---|---|
| [...] | [...] | [...] | [...] | [...] |

## Next steps and outlook

[Prioritized actions, their rationale, dependencies, and expected decision value]

## Final summary

[Supported conclusions, unresolved issues, proposed responses, and near-term outlook]

## References

[Preserve supplied citation style and identifiers]
```

Omit empty metadata and irrelevant sections, but do not omit premises required to understand the evidence. The background heading is optional only when its content is integrated clearly into the opening or first relevant section. For a continuation report, retain a compact recap unless the user explicitly confirms that the audience shares the specific prior material. Use appendices for detailed protocols, full tables, supplementary diagnostics, or specialist material that would interrupt the main narrative. Keep the exact-value table adjacent to its chart when practical; otherwise link explicitly to the appendix table.

## HTML

Produce a complete HTML document when HTML is requested:

- Include `<!doctype html>`, an accurate `<html lang="...">`, UTF-8 charset, viewport metadata, and a meaningful `<title>`.
- Use semantic landmarks such as `<header>`, `<main>`, `<section>`, `<figure>`, `<figcaption>`, and `<footer>`.
- Use one `<h1>` and a correctly nested heading hierarchy.
- Put tabular data in `<table>` with `<caption>`, `<thead>`, `<tbody>`, and scoped header cells. Preserve units in headers and exact values in cells.
- Give every informative image meaningful `alt` text. Do not duplicate the full visible caption in the alt text.
- Embed restrained print-friendly CSS in `<style>` unless the user supplies a stylesheet. Do not use JavaScript or remote fonts, libraries, trackers, or CDNs unless requested.
- Keep figures in a sibling `figures/` directory and use relative paths. If the user explicitly requires a single-file artifact, confirm whether images should be embedded before expanding file size.
- Ensure the reading order and meaning remain intact without color and when printed.
- When the target page already loads KaTeX auto-render, keep formulas in `$...$` and `$$...$$` form. Otherwise follow the standalone-HTML rule in [math-formatting.md](math-formatting.md) and do not introduce an undeclared remote dependency.

Use responsive tables or wrappers where needed, but do not hide columns or exact values on small screens.

## Missing inputs

Localize placeholders to the report language and make them specific enough to be actionable:

- Good: `[待补充：对照组 n、均值、标准差及统计检验]`
- Good: `[TO SUPPLY: extraction date and denominator for the cohort percentage]`
- Avoid: `[补充内容]`, `TBD`, fabricated examples that resemble real results, or prose implying the missing claim is already established.

Placeholders are acceptable in a requested template or incomplete draft. Remove all resolved placeholders before presenting a report as final.

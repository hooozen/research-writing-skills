# HTML Reports

An HTML report is a document people read, scroll and sometimes print or project. Design it like a well-set paper, not a dashboard: one comfortable reading column, quiet chrome, figures and tables that are easy to inspect.

## Start from the template

Copy [../assets/report-template.html](../assets/report-template.html) and replace its content. Keep its `<style>` and `<script>` unless the user supplies their own stylesheet or the destination imposes one. The template's example content is synthetic; none of it may survive into a real report.

What the template already does:

| Feature | How it works | What you need to do |
|---|---|---|
| Reading column | About 40 Chinese characters or 75 Latin characters per line, 17 px text, 1.75 line height | Nothing. Don't widen the column for wide figures; export the figure at the right size instead. |
| Contents | Built automatically from each `<section>`'s `<h2>` and the appendix `<summary>`. Sticky rail with the current section highlighted on wide screens; a collapsed "目录" block on phones. Hidden when there are fewer than three sections. | Give each top-level section an `id` and an `<h2>`. Don't hand-write a contents list. Localize the "目录" label for non-Chinese reports. |
| Figure viewer | Click or press Enter on any figure image or inline SVG to open it larger; Esc or "关闭" closes it. | Use `<figure>` with an `id`, an `<img>` or inline `<svg>` and a `<figcaption>`. Localize "关闭". |
| Tables | Horizontal rules only, numbers right-aligned in tabular figures; on narrow screens the table scrolls sideways with an edge shadow instead of squashing columns. | Wrap each table in `<div class="table-wrap">` and use a table `id`, a `<caption>`, `class="num"` on numeric cells and headers, and units in headers. |
| Notices | `.notice` for the one thing a reader must not miss, such as "all data are synthetic". `.todo` marks a missing input in a draft. | Use at most one notice near the top. Remove every `.todo` before calling a report final. |
| Appendix | `<details class="appendix">` collapses long supporting material; it opens automatically when printed or linked from the contents. | Put full tables, derivations and diagnostics here, linked from the main text. |
| Print | A4 margins, contents and viewer hidden, figures and tables kept whole, appendices expanded. | Check the print preview once. |
| Accessibility | Semantic landmarks, visible keyboard focus, reduced-motion respected, works without JavaScript. | Keep one `<h1>`, nested headings, `alt` text or `<title>` on figures, `scope` on header cells. |

## Design rules

Keep the visual system tied to the charts: white paper, dark ink `#24282C`, muted text `#626B73`, hairline rules, and the chart blue `#1464D2` as the only accent (links, the active contents item). Orange `#B64B00` is reserved for the synthetic-data or missing-input notice. There is no dark mode on purpose: scientific figures are white-background artwork and look pasted-on against a dark page.

Don't add:

- Cards, drop shadows, rounded panels or gradient backgrounds around sections. Spacing and headings already separate them.
- "Key metrics" tiles or big-number banners at the top. The overview paragraph states the main result in a sentence with its context.
- Icons, emoji, badges, all-caps labels or decorative dividers.
- Animated entrances, parallax, auto-playing anything. The only motion is a short highlight on the element a link jumps to.
- Web fonts, CDNs or external scripts. The file must open offline and look the same.

Headings should say something. "筛选后验证准确率从 75% 升到 80%" tells the reader the finding; "实验结果" doesn't. The contents rail then doubles as a summary of the report.

## Structure

```html
<div class="layout">
  <header class="report-header">
    <h1>…</h1>
    <dl class="meta"><div><dt>报告期</dt><dd>…</dd></div></dl>
  </header>
  <nav class="toc" aria-label="目录" hidden><details open><summary>目录</summary><ol></ol></details></nav>
  <main>
    <div class="notice" role="note"><p>…synthetic-data notice, only if needed…</p></div>
    <section id="overview"><h2>概述</h2><p class="lede">…</p></section>
    <section id="…"><h2>…</h2> … </section>
    <details class="appendix" id="appendix"><summary>附录：…</summary> … </details>
  </main>
</div>
```

Only the overview paragraph gets `class="lede"`. Leave out metadata the user didn't supply; don't invent a presenter or date.

## Figures and formulas

- Link figures from a sibling `figures/` directory with relative paths. For a single-file report, inline the SVG (keep its text as text) or embed a PNG as a data URI. A single-file request already authorizes embedding.
- Start figure and table captions with their own number (`图 N.` or `表 N.`) and a descriptive title. Include metric, population, unit, uncertainty and source where relevant. Give `<img>` useful alt text and inline SVG a `<title>`.
- For offline reports render formulas as native MathML and preserve the TeX in `<annotation encoding="application/x-tex">` inside `<semantics>`, as the template does. A served page can use its local KaTeX renderer in HTML-and-MathML mode. See [math-formatting.md](math-formatting.md).
- Refer to each figure and table by an anchor link, for example `<a href="#fig-accuracy">图 1</a>` or `<a href="#tab-accuracy">表 1</a>`. The target briefly highlights when reached.

## Check before delivering

Open the file in a browser and look at it; don't just validate the markup.

1. Wide window (≥ 1100 px): contents rail visible, the active item follows scrolling, no horizontal page scroll.
2. Phone width (375 px): contents collapsed at the top, text readable, tables scroll inside their frame, figures fit.
3. Click a figure: the viewer opens larger and closes with Esc.
4. Print preview: appendices expanded, nothing cut across pages that shouldn't be, no contents rail.
5. Disconnect from the network or check the source: no external requests.
6. Inline and display formulas render as selectable mathematics in the actual view, with accessible TeX source. Figure and table links jump to their captioned items. Every link resolves and the final report is free of `.todo` placeholders.

If you can't open a browser, say which of these checks you couldn't run.

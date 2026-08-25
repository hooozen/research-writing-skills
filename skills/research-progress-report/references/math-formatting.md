# KaTeX-Compatible Mathematics

Use this guide whenever a report contains mathematical notation. The source must render in common VS Code Markdown math support and KaTeX without relying on a full LaTeX installation or optional extensions.

## Delimiters

- Inline math: `$E = mc^2$`
- Display math: put `$$` on separate lines:

  ```markdown
  $$
  \bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
  $$
  ```

- Do not use `\(...\)`, `\[...\]`, or bare TeX without delimiters.
- Keep each inline expression within one paragraph. Do not span an inline formula across line breaks.
- Escape a literal currency dollar sign outside mathematics as `\$` when it could be mistaken for a delimiter.

## Use portable KaTeX constructs

Prefer basic, widely supported notation:

- superscripts and subscripts: `x_i^2`;
- fractions and roots: `\frac{a}{b}`, `\sqrt{x}`;
- Greek letters and common relations: `\alpha`, `\Delta`, `\le`, `\approx`;
- sums, products, limits, and integrals: `\sum`, `\prod`, `\lim`, `\int`;
- delimiters: `\left(`, `\right)`, `\lvert`, `\rvert`, `\lVert`, `\rVert`;
- text and operators: `\text{}`, `\mathrm{}`, `\mathbf{}`, `\operatorname{}`;
- standard matrix environments such as `matrix`, `pmatrix`, and `bmatrix` inside display math;
- `aligned` inside `$$...$$` for a small multi-line derivation:

  ```markdown
  $$
  \begin{aligned}
  L &= L_{\mathrm{data}} + \lambda L_{\mathrm{reg}}, \\
  L_{\mathrm{data}} &= \frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2.
  \end{aligned}
  $$
  ```

Define every nonstandard symbol near first use. Keep units in prose when possible; otherwise use upright text such as `$5\,\mathrm{mm}$`.

## Avoid non-portable LaTeX

Do not use:

- `\label`, `\ref`, `\eqref`, `\tag`, or automatic equation numbering;
- `\newcommand`, `\renewcommand`, `\def`, `\let`, or other custom macro definitions;
- `\documentclass`, `\usepackage`, `\begin{document}`, `\input`, or `\include`;
- top-level `equation`, `equation*`, `align`, `align*`, `gather`, or other document environments;
- commands that require optional extensions or packages, such as chemistry notation, unless the user confirms the target renderer loads that extension;
- styling or link commands whose support varies across renderers when plain mathematical notation can express the same meaning.

If uncertain whether a command is portable, rewrite it using simpler primitives. Do not preserve a specialized macro merely because it works in a full LaTeX editor.

## Markdown and HTML interactions

- Avoid display math inside Markdown tables. Put the equation before or after the table and refer to it by symbol or descriptive name.
- Inside a Markdown table, avoid raw vertical bars in formulas because they can split cells. Use `\mid`, `\lvert...\rvert`, or `\lVert...\rVert` as appropriate.
- Do not place formulas in code spans or fenced code blocks in the finished report; code fences in this guide show source syntax only.
- Keep sentence punctuation outside an inline delimiter unless it is mathematically meaningful.
- For HTML intended for a page that already loads KaTeX auto-render, retain `$...$` and `$$...$$` in text content. Do not place TeX in HTML attributes.
- For standalone HTML without a math renderer, do not claim the formulas are rendered. Use user-approved local KaTeX assets when available, or state the rendering requirement outside the report; never add an undeclared remote CDN dependency.

## Verification

Before delivery:

- confirm every opening `$` or `$$` has the matching closing delimiter;
- confirm no prose was accidentally enclosed as mathematics;
- confirm every symbol and comparison baseline is defined;
- scan for forbidden labels, references, custom macros, and document environments;
- render-check the Markdown in a KaTeX-capable preview when available;
- preserve the user's mathematical meaning, including indices, grouping, units, and operator precedence.

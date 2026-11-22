# LaTeX source and rendered formulas

Read this whenever a report contains math. Keep the LaTeX source editable and make the published equation selectable as mathematics. Use KaTeX-compatible LaTeX in Markdown. In HTML use native MathML with retained TeX, or a renderer such as KaTeX in HTML-and-MathML mode. Readers should never need a TeX installation.

## When a formula earns its place

Use a formula when it states a metric, transformation, model or decision rule more briefly and precisely than prose. Show the defining relationship once, define the symbols right after it, then say what it means for the result. Keep short expressions inline; give a central or complex one its own line. Derivations go to an appendix unless the reader needs the steps to judge the result.

Keep units, denominators, baselines and assumptions. With accuracy $a = n_{\mathrm{correct}}/N$, say what population $N$ counts. For a nonzero baseline $a_0$, the percentage-point change $100(a_1-a_0)$ and the relative change $100(a_1-a_0)/a_0$ are different numbers. A ratio with a zero denominator is undefined; say so rather than printing a number. Don't write notation that implies a relationship nobody tested.

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

## Markdown and HTML delivery

- Avoid display math inside Markdown tables. Put the equation before or after the table and refer to it by symbol or descriptive name.
- Inside a Markdown table, avoid raw vertical bars in formulas because they can split cells. Use `\mid`, `\lvert...\rvert`, or `\lVert...\rVert` as appropriate.
- Do not place formulas in code spans or fenced code blocks in the finished report; code fences in this guide show source syntax only.
- Keep sentence punctuation outside an inline delimiter unless it is mathematically meaningful.
- For a report published from Markdown, check the published view as well as the source. Confirm the renderer recognizes both math delimiters. If using client-side LaTeX rendering, keep TeX in text content and retain it in the rendered math's annotation or source document.
- For offline standalone HTML, use native MathML or bundle the local KaTeX assets, styles and fonts. For single-file delivery, embed assets or use MathML without runtime dependencies. Preserve the exact TeX in `<annotation encoding="application/x-tex">` inside `<semantics>`. Native `<math>` holds the equivalent structure, including fractions and scripts.
- Use document math for every required formula. Equation screenshots, PNG exports, SVG paths, and other image substitutes do not pass this requirement. Supporting scientific figures may still use normal image formats.
- If the requested destination has no workable math renderer, keep the editable TeX in the source and state the specific rendering limitation. When an alternate view is in scope, provide the equivalent rendered document there.

## Verification

Before delivery:

- confirm every opening `$` or `$$` has the matching closing delimiter;
- confirm no prose was accidentally enclosed as mathematics;
- confirm every symbol and comparison baseline is defined;
- scan for forbidden labels, references, custom macros, and document environments;
- open the delivered view and check at least an inline equation and a display equation with a fraction or subscript for actual typesetting, layout and selection;
- verify the rendered equation is part of the document's math/text structure and that the TeX remains available in the source or a math annotation;
- preserve the user's mathematical meaning, including indices, grouping, units, and operator precedence.

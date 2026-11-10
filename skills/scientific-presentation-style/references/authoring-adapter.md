# Optional Artifact Tool adapter

The adapter accepts a live or standalone presentation facade; it does not create cloud documents, publish, export or install anything. Follow the active presentation workflow for destination, session setup, rendering and delivery. The core design is portable to other capable PowerPoint authoring tools.

Load these files from this skill's actual directory:

- [Design tokens](../assets/design-tokens.json)
- [Explicit synthetic examples](../assets/example-data.json), only for a requested template/demo
- [Slide builders](../scripts/slide-builders.mjs)

The module exports `configureScientificTheme(presentation, tokens)`, `makeScientificSlide(presentation, specification, tokens)`, `templateSpecifications(examples)`, `tableSpecifications(examples)`, `palette(tokens, mode)`, `px(points)`, and the statistical helpers used in its geometric plots. Do not retain live presentation/slide handles outside a session callback.

For an Artifact Session, import the module in the authoring runtime, load the two JSON files, and pass plain inputs to the active callback:

```javascript
const builders = await import(`${SKILL_DIR}/scripts/slide-builders.mjs`);
// tokens, specification and artifactRef come from the actual task/session.
const result = await artifactSession.run(async ({presentation, input}) => {
  // Set the theme only for a new template or explicitly authorized restyling.
  builders.configureScientificTheme(presentation, input.tokens);
  return builders.makeScientificSlide(presentation, input.specification, input.tokens);
}, {artifactRef, input: {tokens, specification}});
```

Every specification requires `kind`, `title`, `caption`, and the appropriate `data`. Set `synthetic: true` for explicit examples; the slide receives a visible disclosure. No example dataset is silently inserted. `kind` supports `counts`, `line`, `scatter`, `boxplot`, `paired`, `interval`, `heatmap`, `performance`, `table`, `style`, `grayscale`, and `empty`. For the table schema and missing/derived-value rules, read [tables.md](tables.md).

Count bars use one blue series unless an aligned `data.roles` array explicitly assigns `primary`, `secondary`, `third` or `neutral` to categories. Use neutral for an actual residual/unknown category, not automatically for the third group.

The [example data](../assets/example-data.json) demonstrates each supported data object. Counts require an explicit `relationship` and known nonnegative denominator or `null`; unavailable shares remain unavailable. Numeric-time lines accept explicit `null` gaps and one to three series. Scatter supports one to three groups. The box layout supports two groups of raw observations; the interval layout supports one to four supplied estimates. Larger designs require reflow, not font shrinking. Heatmap values must fit the declared common limits. The classification layout derives ROC/PR from aligned binary labels/scores and aggregates ties at one threshold.

`makeScientificSlide` adds a slide. `reuseIndex` may refer only to a completely empty existing slide, such as a newly created destination's initial blank slide. It never clears or overwrites a populated slide. Rendering errors can leave an incomplete slide in some authoring environments; inspect and repair that slide before retrying an append operation.

Use `templateSpecifications(examples)` to obtain fourteen content layouts, including three tables. Add a simple cover using the presentation workflow, then build small batches. For new cloud decks, inspect whether the destination already has an empty slide and reuse it when appropriate. A complete demonstration has fifteen slides including its cover. Use `tableSpecifications(examples)` to obtain only the three table examples for an existing template.

Bars and XY plots are native charts. Boxes, paired plots, intervals and heatmaps are native geometry with source data in notes. Geometric figures need regeneration to follow data changes. The adapter uses one coordinate transform per geometric plot and preserves a zero bar origin, numerical time, incomplete pairs, actual interval endpoints and a distinct missing-cell fill.

Tables are native editable cells with literal display values. Preserve the raw values in notes and refresh derived cells when the source changes; editing a count does not automatically recalculate another cell's percentage.

After a native count edit, refresh custom count/share label text from the new counts and denominator. ROC/PR plot data are derived coordinates; recompute them from changed labels/scores rather than treating a chart-data edit as a rerun of evaluation.

Render and inspect every slide, then inspect chart series and shape geometry. For native PowerPoint export, follow the active export workflow's checks for chart workbook values, fonts, slide size and native elements. The module alone does not establish that a particular viewer or PowerPoint version supports every exported object.

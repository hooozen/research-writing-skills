# Changelog

All notable changes to this repository are documented here.

## [Unreleased]

## [1.0.0] - 2026-10-25

### Changed

- Make a 19-chart text/JSON index and per-chart cards the Agent's primary reference route. Each card has a minimal input, scientific definition, short runnable example and individual editable SVG/PNG; large contact sheets are optional.
- Add a direct single-chart renderer for supplied input or explicitly requested synthetic examples, keeping shared B/D styles and tested statistical calculations. It rejects absent/invalid required data instead of falling back to a whole synthetic gallery.
- Add source/input/image freshness records, reference consistency checks, and bounded Agent retrieval/single-chart/incomplete-input evaluations alongside numerical, layout and export regressions.
- Publish the new skill directory and reference layout as a major release relative to v0.2.1; migrate old installed names and preserve recoverable backups outside discovery roots.
- Rename `clinical-data-chart-style` to `scientific-chart-style`, broaden it to scientific figures across disciplines, and update discovery metadata, report integration and executable/test paths. Retire the old installed name rather than exposing duplicate skills.
- Adopt the selected muted B teal/terracotta palette as the default and a deliberately encoded D grayscale mode for print; replace gray rounded cards and pixel-scaled typography with white publication figures, physical-point fonts and aligned panels.
- Expand guidance on observation-level views, estimates/uncertainty, model evaluation, agreement, survival and high-dimensional data. Add primary publication/technical references and nine advanced reproducible examples alongside the existing nine basic examples and count/share figure.
- Export editable SVG/PDF and high-resolution PNG, preserve meaningful statistical definitions, support both color modes, and verify rendered physical-size layout, masks, ties, censoring, normalization and transformations.

- Require explicit model-report coverage: dataset splits and leakage boundaries, overall/custom-module architecture diagrams and data flow, actual loss formulas, training settings, early stopping and final checkpoint selection, and available performance with metric purposes, formulas and interpretation.
- Add a detailed model-reporting reference and verified original-paper diagram examples from ResNet, U-Net, Transformer and Squeeze-and-Excitation; reconcile audience/conciseness guidance with required methods detail, missing evidence and scoped edits.
- Add bounded behavior cases for complete model methods, metric calculations, custom modules and incomplete training/evaluation evidence.
- Make whole-report organization and a substantive reader-facing overview precede detailed exposition; connect module roles, stages, data relationships, evidence, and decisions instead of assembling source fragments.
- Require consistent canonical names and explained aliases, introduce unfamiliar concepts through their purpose and role, and replace abstract terminology with concrete actions. Preserve necessary explanations when shortening text or using figures and formulas.
- Add worked writing examples and behavior cases for concept introduction, terminology consistency, and a report's overall explanatory flow.
- Make concise language and explicit question–evidence–conclusion logic the default for progress reports; remove repeated exposition while preserving essential scientific context and limitations.
- Prioritize informative charts and precise formulas when they communicate evidence more briefly and accurately than prose; keep exact values traceable, define quantitative assumptions, and avoid redundant visuals or forced notation.
- Simplify the report scaffold and add bounded evaluation cases for visual compression, mathematical accuracy, and text-only updates.

## [0.2.1] - 2026-09-08

### Fixed

- Reserve measured title/subtitle space inside chart cards, wrap long headers and grow short figures when necessary; keep colorbar axes aligned and prevent title text from crossing gray/white panel boundaries.
- Define inside-card versus above-panel title ownership and require a final boundary check after font, size or export changes; preserve the existing spacing, overlap and clipping guidance.

## [0.2.0] - 2026-09-07

### Changed

- Use lighter box/violin median strokes and a borderless heatmap colorbar; choose bar orientation from label readability, ordering and layout instead of a category-count cutoff.

### Added

- Nine reproducible scientific chart examples: box, violin, scatter, longitudinal line, histogram, ECDF, paired observations, estimates with intervals, and heatmap; export raw/derived data and English or Chinese labels.
- A compact visual reference and chart-specific guidance on statistical definitions, pairing, missingness, axes and quantitative color scales, loaded only when relevant.

## [0.1.5] - 2026-09-07

### Fixed

- Reject unsafe installation names, deduplicate selections, honor `--`, protect source directories and dangling destination symlinks, stage copies before replacement, and restore the previous installation when its final move fails.
- Validate malformed catalog entries and actual YAML without tracebacks; check links in supporting references, portability boundaries, optional adapters, and nested script syntax without writing skill bytecode.
- Reuse supplied or delegated report settings, remove the separate optional-outline wait, and align mixed-audience guidance around the chosen primary audience.
- Provide an explicit offline/single-file HTML math route and make the chart-style companion optional for portable report use.
- Scope count/share labels to counts, preserve overlapping/subset denominators and continuous metrics, and handle missing or zero populations without invented percentages.
- Use exclusive scan-size categories and explicit synthetic/population labels in the plotting example; convert pixel typography tokens to renderer points.

### Added

- Installer, validator, and chart regression tests; Python maintenance dependencies; Linux/macOS CI coverage; and bounded behavioral evaluation cases.

## [0.1.4] - 2026-08-25

### Added

- Require `$...$` for inline mathematics and `$$...$$` for display mathematics.
- Add a KaTeX/VS Code compatibility guide covering supported constructs, Markdown interactions, HTML behavior, and verification.
- Prohibit equation labels, cross-references, custom macros, document-level LaTeX commands, package-dependent extensions, and unsupported environments.

## [0.1.3] - 2026-08-24

### Added

- Give the user an explicit pre-draft opportunity to provide an optional outline or delegate report organization to the agent.
- Combine missing audience, context, and outline choices into one concise intake message.
- Preserve the hierarchy and emphasis of a supplied outline while integrating essential scientific context and evidence.

## [0.1.2] - 2026-08-24

### Fixed

- Make reports self-contained by default instead of assuming the audience has access to the author–agent conversation, attachments, prior drafts, or source bundle.
- Require the report to reconstruct the relevant problem, prior state, research gap, project setup, baselines, and reasons needed to understand each result.
- Add standalone-reader and reference-resolution checks for unexplained terms, cohorts, comparisons, and context-dependent phrases.
- Add an explicit background-and-gap layer to the adaptable report scaffold.

## [0.1.1] - 2026-08-24

### Fixed

- Require an explicit target-audience choice before drafting a progress report; audience may no longer be inferred from the material.
- Prevent speaker coaching, “what to say”, and other author-facing meta-content from appearing in the audience-facing report.
- Keep audience and context settings hidden unless the user explicitly requests them as report metadata.

## [0.1.0] - 2026-08-24

### Added

- `research-progress-report` for audience-aware, evidence-led research progress reports.
- `clinical-data-chart-style` for consistent clinical and medical-imaging data charts.
- Agent-neutral discovery, installation, validation, and contribution workflows.

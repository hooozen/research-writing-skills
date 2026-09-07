# Changelog

All notable changes to this repository are documented here.

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

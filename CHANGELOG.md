# Changelog

All notable changes to this repository are documented here.

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

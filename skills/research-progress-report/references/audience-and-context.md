# Audience and Context Calibration

Use the selected audience to decide what must be explained, what can be assumed, and which evidence details belong in the main narrative. Scientific accuracy and traceability do not change across audiences.

The audience must come from an explicit user choice; these profiles are not inference targets. Treat the selected profile and public/lab context as internal configuration. Do not print labels such as `小领域科研人群` or `研究伙伴` in the report unless the user explicitly asks for audience metadata.

## Audience profiles

| Audience | Assume | Explain in the report | Evidence and methods emphasis | Avoid |
|---|---|---|---|---|
| 普遍高学历人群 | General scientific literacy, quantitative reasoning, and scientific skepticism; no field-specific background | The research problem, why it matters, essential domain concepts, and how the evidence answers the question | Intuitive scales and comparisons, transparent study design, key controls, uncertainty in plain language, and a small number of decisive results | Unexplained acronyms, protocol parameters, field-internal debates without context, and oversimplified certainty |
| 大领域科研人群 | Foundational and common knowledge of the broad discipline; limited knowledge of this specific subfield and its current frontier | The subfield landscape, the precise gap, why the chosen approach is credible, and how it differs from common alternatives | Design choices, major controls, benchmark or baseline, interpretable effect sizes, and enough methods detail to assess validity | Re-teaching broad disciplinary basics or assuming familiarity with niche methods and recent disputes |
| 小领域科研人群 | Current questions, major methods, benchmarks, and recognized bottlenecks in the research direction | Only project-specific concepts, nonstandard choices, changed assumptions, and evidence that alters the state of the problem | Exact experimental conditions that affect interpretation, controls, ablations, uncertainty, failure modes, comparison to state of the art, and unresolved technical risks | Introductory background, vague claims such as “significantly improved” without a defined baseline, or hiding null and failed results |
| 研究伙伴 | Shared project goals, history, terminology, datasets, equipment, and most prior decisions | What changed since the last update, why a deviation was made, what the newest evidence means, and what input or decision is needed | Reproducible parameters, versions and sample identifiers when material, raw and processed results, anomalies, blockers, owners, dependencies, and immediate next experiments | General background, polished narrative at the expense of operational facts, or burying blockers and decisions |

These profiles are calibration anchors, not rigid personas. If the actual audience spans levels, write the main narrative for the least specialized intended reader and place specialist detail in expandable sections, appendices, footnotes, or linked tables.

## Public report

- Make the central finding and its significance understandable before presenting technical detail.
- Define specialized terms at first use and use figures that can stand with their captions.
- Include enough methods and uncertainty to prevent the report from becoming publicity copy.
- Respect any provided confidentiality, consent, embargo, de-identification, or disclosure constraints. If public release conflicts with an explicit constraint, flag the issue outside the report instead of silently publishing or silently altering the evidence.
- Keep internal logistics, tentative blame, credentials, and operational identifiers out unless the user explicitly wants them public.

## Lab meeting

- Prioritize what changed, the evidence, failed or ambiguous results, technical causes under consideration, and decisions needed from the group.
- Include consequential protocol changes, controls, sample exclusions, quality checks, and analysis versions.
- Make next experiments testable: connect each to the uncertainty it addresses, expected discriminating outcomes, dependencies, and decision criteria.
- Use owners and dates only when supplied or explicitly requested. Do not invent commitments.

## Depth test

For every paragraph, ask whether it enables this audience to understand a conclusion, evaluate evidence, follow a decision, or act on the next step. Compress or relocate content that does none of these.

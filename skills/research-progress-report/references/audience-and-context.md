# Audience and Context

The audience decides what you explain, what you can assume, and which details sit in the main text versus an appendix. It never changes accuracy or traceability.

Three rules hold for every audience:

- **Nobody has seen your sources.** Readers don't have the chat, the attachments or earlier drafts. Expertise tells you which textbook concepts to skip, not what this project's samples, baselines, decisions or internal names are. Skip project background only when the user confirms the audience already shares it.
- **Expertise doesn't excuse jargon.** Specialists still need a coherent overview, explained project-specific names and visible reasoning.
- **Model detail doesn't shrink.** [model-reporting.md](model-reporting.md) applies to every audience; for a general audience, keep the central mechanism in the main text and move specialist detail to a linked appendix.

Use the audience the user described, or choose one when they explicitly delegate. Otherwise ask once before the first full draft. The profile and the public/lab context are internal settings: don't print labels such as `小领域科研人群` in the report unless the user asks for that metadata.

## Profiles

These are calibration anchors, not personas you must pick from.

| Audience | Assume they know | Explain | Emphasize | Avoid |
|---|---|---|---|---|
| 普遍高学历人群 (educated non-specialists) | Scientific literacy and healthy skepticism; no field background | The problem and why it matters, essential domain concepts, how the evidence answers the question | Intuitive scales and comparisons, the study design, key controls, uncertainty in plain words, a few decisive results; full model methods in an appendix | Unexplained acronyms, protocol detail that breaks the narrative, insider debates, false certainty |
| 大领域科研人群 (same broad field) | Fundamentals of the discipline; little about this subfield's frontier | The subfield landscape, the precise gap, why this approach is credible and how it differs from common alternatives | Design choices, main controls, baselines, interpretable effect sizes, enough method to judge validity | Re-teaching basics; assuming niche methods or recent disputes are known |
| 小领域科研人群 (same subfield) | Current questions, main methods, benchmarks and bottlenecks | Only what's project-specific: nonstandard choices, changed assumptions, evidence that moves the field | Conditions that affect interpretation, controls, ablations, uncertainty, failure modes, comparison with the state of the art, open risks | Introductory background, "significantly improved" with no baseline, hiding null or failed results |
| 研究伙伴 (collaborators) | Domain expertise; project history only if confirmed as shared | A short recap of the last state, what changed, why, what the new evidence means, what input or decision is needed | Reproducible parameters, versions and sample IDs when they matter, raw and processed results, anomalies, blockers, dependencies, next experiments | General background, assuming they read the chat, polish at the expense of operational facts, burying blockers |

For a mixed audience, write the main text for the primary audience the user named and layer extra detail for the others. If the choice was delegated, write for the least specialized intended reader and put specialist detail in appendices or linked tables.

## Public briefing

- Make the central finding and why it matters clear before the technical detail.
- Define specialist terms at first use; figures should stand on their own with their captions.
- Keep enough method and uncertainty that the report doesn't turn into publicity.
- Respect confidentiality, consent, embargo and de-identification constraints. If publishing conflicts with one, flag it outside the report; don't silently publish or silently edit the evidence.
- Leave out internal logistics, tentative blame, credentials and operational identifiers unless the user wants them public.

## Lab meeting

- Lead with what changed, the evidence, failed or ambiguous results, suspected technical causes, and decisions the group needs to make.
- Include protocol changes, controls, exclusions, quality checks and analysis versions that matter.
- Make next experiments testable: which uncertainty each one addresses, what result would discriminate, dependencies, decision criteria.
- Add owners and dates only if supplied or requested.

## Depth test

For each paragraph, ask whether it helps this audience understand a conclusion, judge evidence, follow a decision or act on a next step. Shorten or move anything that does none of those, but check the overall route first: the opening and section openings must still let a reader explain the problem, approach, how parts connect and current status.

Then hand the report, mentally, to a typical reader with no access to the prompt, attachments, earlier drafts or chat. They should still be able to identify the problem, the prior state, the objective, what each comparison means, why each major action was taken and what each conclusion rests on.

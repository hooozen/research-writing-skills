---
name: infohub-maintenance
description: "Maintain an existing InfoHub research workspace: project datasets, previews, annotations, local snapshots and exports, report delivery, and the unified Web/MCP services. Optional integration for people who already run InfoHub; ordinary research never needs warehouse publication, and the writing and chart skills don't need InfoHub."
---

# InfoHub Maintenance

Use this only when the task is about an existing InfoHub installation, or the user explicitly asks to change its services. Writing a report or preparing data doesn't by itself mean deploying InfoHub, registering data, publishing a report or archiving to the warehouse.

## Find the installation first

Locate the authorized checkout from the task, the project's instructions or `INFOHUB_ROOT`. Read its `AGENTS.md`, `README.md`, the relevant code and the current configuration. Service names, data roots, LAN and private-network addresses and API contracts come from there, never from memory or another user's setup.

If there's no InfoHub, carry on with the writing, figures or local files and say the integration isn't available. Don't provision a server, create credentials or publish somewhere else to make this skill apply. Installing InfoHub is a separate, explicitly scoped request.

## Where to go

| The task | Read |
|---|---|
| Create a project; register or revise data; annotate; freeze experiment input; export locally | [references/project-data.md](references/project-data.md) |
| Change a source adapter, viewer, page, API, gateway or MCP endpoint | [references/web-services.md](references/web-services.md) |
| Write or revise a report or chart | The writing or chart skill, on its own. Come back here only for an InfoHub step the user asked for. |
| Deliver a report through InfoHub | The installation's report publisher. Publishing is its own requested action. |
| Publish project results to the warehouse | Freeze a complete project snapshot, then follow the installation's warehouse runbook. |
| Update skills or documentation | Stay in that scope. No snapshots, exports, imports or deployments on the side. |

## Rules that protect research data

- **Working data is usable now.** Project data can be previewed, annotated, revised, used in experiments and exported locally without ever reaching the warehouse.
- **Layers stay separate.** Source records, model outputs, human revisions, review decisions, membership and existing experiment splits are kept apart. Inheritance and refresh bind explicit revisions; upstream changes never silently replace project results.
- **Unknown is not negative.** Keep unknown values, original option order, partially known QA and provenance. Don't infer patient identity or labels from file names. Apply mask or QA conventions only where that project defines them.
- **Assets by reference, retained by hash.** Reference stable original images in place. Keep project-needed assets from disposable mirrors or embedded containers as separate copies with content hashes. A local manifest is not automatically a portable copy.
- **One writer, checked revisions.** Use the unified write path with expected-revision checks. Keep undo history and old masks. Test writes against isolated databases and synthetic fixtures, never live annotations.
- **No side effects from UI work.** A UI or catalog change never recomputes QA, redraws splits, changes members or publishes. Those happen only when the task asks, as a new traceable revision.
- **Report the real stage.** Validated, activated and fully accepted are different states. A version can be active while export or backup acceptance still needs recovery.

## Delivering and sharing

Reuse the installation's navigation, UI components, asset service and gateway paths. Reports live in the report center; dataset tools live in the viewing and annotation systems. Keep legacy URLs working and keep a single annotation writer.

When sharing a resource, give both the LAN and the private-network link if both exist, with the same path, query and fragment. Say which links you actually opened. Never substitute `localhost` or an internal backend port, invent a hostname, or claim a second device was tested when it wasn't.

Authorization already given in the conversation covers routine steps; don't re-ask. Data publication, external transfers and access changes stay within what was requested. Never put credentials, database dumps, raw research data or private deployment configuration into a report or a skill package.

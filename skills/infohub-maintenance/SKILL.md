---
name: infohub-maintenance
description: "Maintain an existing InfoHub research workspace: project datasets, previews, annotations, local snapshots and exports, report delivery, and unified Web/MCP services. Optional integration for installations using InfoHub; ordinary research does not require warehouse publication. Not a prerequisite for writing reports or figures."
---

# InfoHub Maintenance

Use this optional integration when the task concerns an existing InfoHub workspace or an explicitly requested change to its services. Writing a report or preparing research data alone does not imply deploying InfoHub, registering data, publishing a report, or archiving to a warehouse.

## Establish the installation

Locate the authorized InfoHub checkout from the task, project instructions, or configured `INFOHUB_ROOT`. Read its `AGENTS.md`, `README.md`, relevant source and current configuration. Discover service names, allowed data roots, LAN/Tailnet addresses and API contracts there; do not assume another user's paths, hostnames, credentials or ports.

If InfoHub is absent, continue independent writing, figures or local artifact preparation. Explain that the integration is unavailable; do not provision a server, create credentials or publish elsewhere merely to satisfy this skill. An explicit installation request requires its own concrete deployment scope.

## Route the task

| Intent | Route |
| --- | --- |
| Create a project, register or repeatedly revise data, annotate, freeze experiment input, export locally | Read [project data workflows](references/project-data.md) |
| Extend a source adapter, viewer, page, API, gateway or MCP endpoint | Read [Web services and delivery](references/web-services.md) |
| Draft or revise a progress report or scientific chart | Use the applicable writing/chart skill independently; return here only for requested InfoHub integration |
| Deliver a report through InfoHub | Follow the deployment's report publisher and delivery instructions; publication is a separate requested action |
| Publish project results to a warehouse | Freeze a complete project snapshot and follow the installation's warehouse skill/runbook and publication task |
| Inspect, plan, or update skills/documentation | Stay within that scope; do not create snapshots, exports, imports or deployments incidentally |

The writing skills in this collection do not require this skill or a running InfoHub installation. Platform-specific metadata under `agents/` is optional.

## Preserve the research workflow

- Project working data is usable immediately for preview, annotation, repeated changes, experiments and local export. Warehouse publication is an optional destination, not a condition for using a dataset or completing a project.
- Preserve source records, model outputs, human revisions, review decisions, membership and existing experiment splits separately. Project inheritance and refresh bind explicit revisions; upstream changes do not silently replace project results.
- Preserve unknown values, original option order, partial-known QA and provenance. Do not infer patient identity or labels from filenames. Apply medical mask/QA conventions only when established by that project's standards.
- Reuse original images by reference when stable. Retain project-needed assets from disposable mirrors or embedded data independently, with immutable content hashes. A local manifest is not automatically a portable copy of every image.
- Use the unified write boundary and expected-revision checks. Preserve undo events and historical masks. Use isolated databases and synthetic fixtures for write tests; do not use live research annotations as smoke-test input.
- Do not recompute QA, redraw experiment splits, change members or publish because of a UI or catalog update. Perform such changes only within the actual task, with a new traceable revision.
- Distinguish validation, activation and completed acceptance. A version may be active while export or backup acceptance still needs recovery; report the real stage and preserve checkpoints.

## Delivery and scope

Reuse the installation's shared navigation, UI components, asset service and gateway paths. Keep report content in the report center and dataset tools in the viewing/annotation systems. Respect existing legacy URL compatibility and keep one annotation writer.

When sharing a configured InfoHub resource, provide both LAN and private-network links when those access modes exist. Keep the path, query and fragment identical; report which endpoints were actually verified. Do not substitute localhost or an internal backend port, invent a private hostname, or claim a second device was tested without evidence.

Existing conversation authorization governs the work; do not ask again for routine steps already authorized. Data publication, external transfer and access changes must remain within the requested scope. Never bundle credentials, database dumps, raw research data or private deployment configuration in a report or skill package.

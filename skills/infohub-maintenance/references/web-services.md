# Web services and research delivery

## Discover before editing

Read the checkout's deployment docs, route and module registry, actual configuration and the relevant code first. Service names, ports, file roots and user identities mentioned below are roles to look up, not defaults. Don't print `.env`, tokens, credential files or private patient paths while inspecting configuration.

The existing implementation separates React/TypeScript/Vite UI, a modular FastAPI API, an independent PostgreSQL work database, persistent jobs, shared assets and a reverse-proxy gateway. Reuse these boundaries rather than creating another ad hoc viewer/backend for the same data.

| Concern | Change and preserve |
| --- | --- |
| Navigation/pages | Shared components, theme variables, system titles/icons, tables, filters, error states and narrow layouts; see [Interface and interaction quality](#interface-and-interaction-quality) |
| Source adapters | Immutable source revision/provenance, native fields, assets, unknown values and established splits |
| Local data operations | Working revisions, expected-revision saves, independent snapshots, Python reads and local exports |
| Assets | Registered sample/role access, original bytes where requested, dimensions/hashes, no arbitrary filesystem traversal |
| Annotation canvas | Original coordinates, mask encoding, continuous strokes, undo/redo, zoom/pan and history |
| Volume viewing | Versioned slice manifest, dimensions/orientation, content hashes, independent bounded cache and honest calibration metadata |
| Standards | Version/fingerprint, source and validation links, explicit project bindings |
| Publication | Trusted server-side bridge, persistent stages, dataset locks, idempotency and recoverable acceptance |
| Gateway | Public-facing paths, LAN/private-network access, legacy links, streaming/compression and metadata headers |

Treat the deployment's legacy databases and migration scripts as historical evidence unless the task is an explicit migration/recovery. Ordinary maintenance does not repeat a cutover or start retired writers. Never run both old and new annotation writers as an expedient rollback.

## Interface and interaction quality

Research tools are used for hours at a time by people inspecting images and labels. Every UI change should make that work faster and less error-prone, not just look new. Reuse the installation's shared components and theme variables; if a needed pattern is missing, add it to the shared layer rather than styling one page by hand.

**Copy.** Name things the way researchers talk about them: "项目", "数据集", "标注", "快照", not table names, internal IDs or API terms. Buttons say exactly what they do ("保存标注", "导出到本地", "发布到数据仓库"), and the confirmation uses the same verb ("已保存", "已导出"). Errors say what happened and what to do next ("另一位标注者刚保存了新版本。重新加载后再保存。"), never just "操作失败" or a raw status code. Empty states say what belongs there and offer the action that fills it.

**Layout.** The data is the main thing on the screen: give the image, table or viewer the space, and keep controls compact around it. Lists of samples are dense tables with sortable columns, a sticky header, right-aligned numbers and a visible count ("显示 50 / 1,284"), not grids of cards. Keep filters, sort and selection in the URL so a view can be shared and survives reload.

**Interaction.**

- Every action that takes time shows progress right where it was triggered and disables the trigger while it runs; long jobs show their stage and can be left and resumed.
- Saving is never ambiguous: show unsaved changes, warn before leaving with them, and show "已保存" with the revision once the server confirms.
- Destructive or publishing actions say what will change and how much ("将从项目移除 12 个样本") before confirming. Prefer undo over a confirmation dialog for reversible edits.
- Annotation canvases support keyboard shortcuts for frequent actions (next/previous sample, undo/redo, brush size, toggle mask), show them on hover, and keep zoom and pan when moving between samples of the same size.
- Optimistic updates roll back visibly on a 409 or other failure; a conflict is shown as a choice to reload, never silently overwritten.

**Visuals.** Neutral surfaces, one accent color for primary actions and selection, and status colors used only for status (and always paired with text or an icon). Mask overlays need adjustable opacity and colors that stay distinguishable for color-blind users. No decorative gradients, shadows on every panel or animations that delay work. Text stays at least 14 px in tables and 16 px in reading views.

**Check it in a browser.** At desktop width and a narrow window: keyboard-only navigation with visible focus, loading, empty and error states (force them with a synthetic fixture), a conflicting save, and a long list. Screenshots of the changed pages belong in the change report.

## Unified routes and delivery

The usual UI routes are `/projects/`, `/datasets/`, `/annotations/`, `/reports/`, `/standards/`, `/warehouse/` and `/mcp/`, with versioned APIs under `/api/v1/`. Discover the installed contract before adding or changing routes.

Dataset preview, annotation and research tools belong in their corresponding systems. The report center contains reports and their static figures/downloads, not independently deployed dataset applications. A report update keeps its slug and original URLs; it does not overwrite the platform navigation.

For requested report authoring, use the appropriate writing/chart skill. For requested publication, locate the actual report publisher and preserve its static-extension boundary, hooks and atomic catalog update. When the installation provides `local-report-server`, read it as the deployment-specific companion; its absence does not block independent drafting or figure generation. A drafting request alone is not a publication request.

Preserve existing project associations. If a deployment organizes reports by an external project identity, use the actual ID and its documented registration mechanism, not a title/slug guess. Do not confuse that identity with InfoHub's dataset working-project model.

Keep raw data, database dumps, secrets and configuration archives outside public report directories. Check nested index pages, relative figures, old anchors and downloads. Scope link/browser checks to affected reports unless catalog-serving behavior changed.

## Assets and volumes during synchronization

Original images normally remain referenced in place. On joining a project, independently retain the requested assets if a mirror may prune them or they are embedded in another container format. Verify the fixed manifest hash while reading/copying, keep immutable assets shared across projects, and reject mismatches rather than caching partial results.

Do not make project reads wait indefinitely for a mirror's global synchronization lock. A committed-version manifest and verified open-file read/copy can preserve object identity during mirror renames. Reuse the implementation's tested retention mechanism; do not remove synchronization safeguards without an equivalent integrity check.

For supported OCT BMP stacks, use the versioned manifest and native filename order, verify dimensions and bottom-up/padding interpretation, and preserve orthogonal/projection axes. Keep caches outside source assets. Do not restore a dependency on deleted ZIPs or invent calibrated axial millimeters. A cached volume does not justify claiming missing source scans exist.

## MCP and gateway compatibility

`/mcp/` is normally documentation/control UI; `/mcp/warehouse` is the protocol endpoint. Confirm the exact configured route. Preserve existing tool behavior and original-image export defaults; complete annotation export is an explicit supported package mode, not an assumption about every warehouse version.

Keep Bearer and precise Host/Origin checks. Tokens may differ across unified, LAN and legacy endpoints: discover their configured locations without displaying contents. Browser test tokens stay in page memory, not URLs, localStorage, sessionStorage or built assets.

Default connection testing performs initialization, initialized notification, tool discovery and read-only metadata/count queries. A successful 202/204 notification may have no JSON body. Do not create export plans or start/cancel exports as routine health probes. Preserve streamed bodies, compression and necessary volume metadata headers through the gateway.

Retain authorized LAN and private-network access and legacy paths. Redirect legacy pages with their query parameters; delegate old write APIs to the unified writer instead of redirecting POSTs. New internal backends bind privately behind the gateway. Do not enable public tunneling or change account sharing to solve a private-network task.

## Verify and deploy only the requested change

Inspect the actual scripts and their side effects before running them. Documentation or skill edits do not trigger data discovery, a snapshot, publication, restore drill or service restart. Use isolated databases/synthetic assets for write tests, and do not report unperformed checks as passed.

For the existing Python/Node checkout, typical checks are:

```sh
cd "$INFOHUB_ROOT"
.venv/bin/python -m pytest -q
npm run build
```

Select browser/asset/protocol tests for the change: desktop and narrow layouts; raw versus thumbnail bytes; mask dimensions/history/conflicts; local workflows without warehouse; real volume axes/gzip; same-resource LAN/private links; and legacy writes reaching only the current database. Fresh experiments and old snapshots must remain independent of later edits.

Report files usually need no restart. Rebuild changed UI, restart only changed backend roles, and validate a changed proxy configuration before applying it. Preserve Compose overrides containing the supported image/schema/MCP extension when using explicit `-f` arguments. Do not reinitialize credentials or application databases to fix an address change.

User-mode private networking may not install host DNS/routes. Diagnose with the deployment's existing tools rather than modifying global DNS or declaring the private endpoint unavailable from one failed resolver call. When returning resource links, label configured LAN and private-network addresses and retain the same resource path/query/fragment; explain verification limits accurately.

## Backup and completion

Use the installation's backup/recovery runbook. Cover the work database, retained assets, snapshots and publication checkpoints consistently. Check backup coverage when adding a new persistent data type. Rebuildable caches/payloads and externally referenced original research directories may need distinct treatment.

Restore into a disposable database and verify counts, hashes, relationships and the actual migration revision. Do not overwrite the live database to test recovery. A backup file or schema listing alone is not a completed restore drill; a local drill does not automatically authorize an external upload.

Deliver the concrete change, affected paths, actual verification and remaining limits. Distinguish deployed behavior from a template or prepared patch, active versions from fully accepted publications, and local verification from testing another device.

# Project data workflows

## Discover current records

Read the project's own data standards and the installation's actual API before writing. Typical InfoHub metadata routes are `/api/v1/projects`, `/datasets`, `/projects/{project}/sources` and sample detail. Use real source IDs, sample IDs and revisions, not guessed version suffixes or historical acceptance counts. Cached catalog rows are not necessarily the full source population.

The routes and commands below describe the project-workspace implementation. Check its current OpenAPI/source contract first; adapt to an installed version rather than inventing unsupported fields. Existing experiment inputs remain valid even when newer working data exists.

## Prepare and register a local package

Create a separate package/output revision instead of overwriting original images, masks or old experiment inputs. A supported local package contains:

| File | Preserve |
| --- | --- |
| `manifest.json` | Dataset identity, version/provenance and `image_path_base` |
| `images.json` | Array of stable `id`, image reference, content hash and native fields |
| `qa.json` | Array associated by image ID; original options/order, answers, unknown/partial-known states and audit |
| Optional asset/split metadata | Mask roles, paths, source semantics and existing `memberships` |

Relative path bases resolve against the package directory, then each image reference resolves against that base. Do not silently rebase paths. IDs must be unique within the registered source; keep conflicting native IDs in separate sources or use the installed adapter's documented identity mapping. Do not merge patients or source identities because bytes match.

Use an empty QA array when the source has no QA. Do not fabricate answers or discard unsupported fields to fit an example. Unknown does not mean negative. For project-defined Retinal-style masks, for example, 255-positive and 127-excluded pixels must retain their distinct meanings; this is not a universal mask encoding for unrelated datasets.

Confirm permitted data roots and task capabilities in the installation. Generic package registration may produce a read-only source: it does not by itself enable grading, lesion editing, QA editing or three-dimensional annotation. Extend and test the adapter/capabilities when requested; do not flip database flags to pretend support exists.

Typical registration, using an already located checkout:

```sh
cd "$INFOHUB_ROOT"
.venv/bin/infohub register /absolute/authorized/package
```

The corresponding API is typically `POST /api/v1/datasets/register` with a package `path`. Registration writes the local catalog; it does not publish to a warehouse or automatically join a project. A source version should bind the manifest/images/QA contents. Replacing an image in place without a new reference/hash does not reliably version experiments.

## Create, join and explicitly refresh

Typical API contracts:

- `POST /api/v1/projects`: project `title`, `description`, optional `parent_id`. Parent inheritance freezes its selected working revision; it does not follow future edits.
- `POST /api/v1/projects/{project}/datasets`: `source_id`, optional explicit `sample_ids`. For dynamic warehouse, embedded-image or volume sources, select the actual samples/page rather than implicitly importing everything.
- `POST /api/v1/projects/{project}/refresh`: `old_source_id` and `new_source_id`, after registering the updated source.

Typical command for an explicit refresh:

```sh
cd "$INFOHUB_ROOT"
.venv/bin/infohub refresh-project PROJECT_ID \
  --from-source OLD_SOURCE_ID --to-source NEW_SOURCE_ID
```

Check the old/new dataset identity, members, provenance and affected revisions first. Refresh preserves manual history and old snapshots; it does not automatically add or withdraw members or redraw splits. If the new source lacks existing members, resolve the discrepancy instead of bypassing the check. Add genuinely new members separately; adding an entire new source after refresh may bind duplicate versions of the same images.

Use the installation's same-origin write header, permission extension point and expected revision. For example, the current implementation uses `X-InfoHub-Request: 1`. A 409 requires rereading and reconciling, not unconditional overwrite. Do not write the retired SQLite database or bypass the service with direct table edits.

## Annotations, review and experiments

Preserve source/model/manual/review layers. In the existing eye/disc workflow, manual disc masks use original-image dimensions and opaque binary PNG; resetting creates another revision rather than deleting history. Review binds the annotation revision and source fingerprint. Review approval does not relabel a model prediction as human annotation.

Do not assume a mask edit recomputes all derived QA or lesion statistics. When rederivation is requested, output a new package/revision and audit the actual algorithm, labels and unknown states. Preserve established patient/group leakage boundaries and all QA belonging to each image.

The Python reader can freeze experiment input without warehouse publication:

```python
from infohub.reader import open_dataset, open_package

data = open_dataset("PROJECT_ID")
fixed = open_dataset(snapshot=data.snapshot_id)
package_path = data.export()
images = open_package(package_path)
# For supported volume packages: open_package(package_path, volumes=True)
```

`open_dataset(project)` creates or reuses a snapshot; it is not a pure status check. Use metadata reads for inspections that must not freeze research data. The returned read manifest must not absorb later web edits. If multiple source versions of an image are present, select `source` explicitly rather than mixing labels.

Local packages may reference absolute paths with `/` as their base. Preserve the declared basis and validate actual availability; do not advertise an export as portable until its required assets have been included and checked. Retain needed disposable-mirror, embedded-image and volume assets by content hash; copying every dataset is not the default.

## Optional warehouse publication

Only an actual publication/archival request enters this boundary. Locate the warehouse runbook/skill in that deployment and prefer its persistent publication task:

`complete frozen snapshot → strict validation → object and semantic diff → authorized confirmation → copy/verify → activate → version-scoped query, export and backup acceptance`

A changed baseline requires a fresh comparison. Withdrawals require an explicit decision; equal file counts do not prove unchanged labels, provenance or unknown states. New working edits remain outside the in-flight snapshot.

Separate active-version state from acceptance success, preserve idempotency keys/checkpoints and resume the same task after reconciliation. A legacy warehouse version without annotation relationships cannot be advertised as a complete annotation package. External exports, full-database uploads and sharing must stay within the request; a local backup check does not imply those transfers.

# Research Writing Skills

Reusable, agent-neutral skills for turning research evidence into self-contained progress reports and publication-oriented scientific figures.

Each skill is a self-contained directory built around `SKILL.md`. Supporting references, scripts, assets, and optional agent adapters stay inside the same directory, so a skill can be installed by copying one folder.

## Skills

| Skill | Purpose |
|---|---|
| [`research-progress-report`](skills/research-progress-report/) | Explain research from overview to evidence in plain language. Model reports require dataset splits, actual architecture and module data flow, loss formulas, training/stopping/model selection, and available results with metric purposes, formulas and interpretation. Follow the user's audience and outline in Markdown or HTML; retain detailed methods in the report or linked appendices. |
| [`scientific-chart-style`](skills/scientific-chart-style/) | Publication-oriented scientific charts across disciplines. A direct index of 19 chart cards with minimal inputs, runnable single-chart examples, individual SVG/PNG references, B color and D print modes, and statistical/export guidance. |

Machine-readable discovery metadata is available in [`catalog.json`](catalog.json).

## Install

Clone the repository, choose your agent's skills directory, and install one or all skills:

```sh
git clone https://github.com/hooozen/research-writing-skills.git
cd research-writing-skills

SKILLS_DIR=/path/to/your-agent/skills

# Install one skill
./scripts/install.sh --target "$SKILLS_DIR" research-progress-report

# Or install every skill
./scripts/install.sh --target "$SKILLS_DIR" --all
```

The installer never overwrites an existing skill by default. To upgrade intentionally, add `--force`; all selected copies are staged first, and each previous installation is moved to a unique timestamped backup before replacement. Repeating a skill name installs it once. Invalid selections are rejected before any skill is installed, and source directories cannot be used as their own destinations. If replacement fails, the installer attempts to restore that skill; a multi-skill install is not one atomic transaction.

Manual installation is equally simple:

```sh
SKILLS_DIR=/path/to/your-agent/skills
mkdir -p "$SKILLS_DIR"
cp -R skills/research-progress-report "$SKILLS_DIR/"
```

An agent can install automatically with this prompt:

```text
Install the relevant skills from https://github.com/hooozen/research-writing-skills.
Follow AGENTS.md, inspect catalog.json before selecting skills, copy complete skill
directories, and do not overwrite an existing installation without confirmation.
```

Agents that support `SKILL.md` directories can load the installed skill directly. Other agents can read the selected `SKILL.md` as task instructions and resolve its linked resources relative to the skill directory. Files under `agents/` are optional platform adapters, not runtime requirements.

## Upgrade from the former chart skill

`scientific-chart-style` replaces `clinical-data-chart-style`. Install the complete new directory, update any explicitly named invocations, and archive the old installation **outside all skill discovery roots**. Do the same for backup folders that still contain a discoverable `SKILL.md`; keep recoverable backups without exposing duplicate old skills. The installer does not infer or remove prior names. The report skill now names the new companion.

The color default is the selected B palette (teal `#547F7E`, terracotta `#AE766A`, ochre `#9B895B`); `--mode grayscale` uses the selected D design and redundant shapes/line styles. The [style guide](skills/scientific-chart-style/references/style-guide.md) defines physical-point typography and export rules; journal-specific instructions override the defaults.

## Agent reference entry

Start at the [19-chart index](skills/scientific-chart-style/references/chart-index.md), then read only the relevant chart card and the shared style guide. Each card links its minimal JSON, individual SVG/PNG and a runnable command. The [machine-readable index](skills/scientific-chart-style/references/chart-index.json) has the same chart IDs and paths. Nine-panel previews and the two longer background guides are optional browsing material.

The single-chart runner reads supplied data with `--input`, or a labeled synthetic fixture only with explicit `--example`:

```sh
python skills/scientific-chart-style/scripts/render_chart.py --list
python skills/scientific-chart-style/scripts/render_chart.py --chart roc --example --output-dir /tmp/roc-example
python skills/scientific-chart-style/scripts/render_chart.py --chart paired --input /path/to/task/pairs.json --mode grayscale --output-dir /path/to/task/figures
```

Commands create only the selected figure and its data/statistics/export record. Use `--formats svg,png,pdf` when all formats are required. The runner is an optional Matplotlib reference, while the input and scientific guidance remain portable to other plotting tools. Missing required data must not silently become demonstration observations.

Maintainers rebuild the installed reference set with `python skills/scientific-chart-style/scripts/build_chart_references.py`; `--check` verifies the registry, input/source hashes and saved individual SVG/PNG without rendering all charts. An ordinary Agent task does not rebuild the atlas.

## Version 1 migration

This release replaces the old `clinical-data-chart-style` directory with `scientific-chart-style`, and its primary reference entry is now the chart index. Update explicitly named invocations and keep old versions/backups outside discovery roots. The existing B/D visual decisions and scientific definitions remain intact. Repository versioning treats the changed installed skill path since v0.2.1 as a major release.

## Maintain

Use Python 3.10+ and install maintenance dependencies before validating changes:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 skills/scientific-chart-style/scripts/build_chart_references.py --check
MPLBACKEND=Agg python3 -m unittest discover -s tests -v
```

These dependencies are for maintainers, not installation requirements. Installed skill instructions remain agent-neutral; Matplotlib is needed only for its optional example. Validation parses YAML, checks catalog consistency and relative Markdown resources throughout each skill, validates optional UI metadata, and checks script syntax without executing skill scripts or creating bytecode in their folders. It does not verify remote URLs, Markdown anchor IDs, raw HTML links, or scientific reasoning.

Use [evals/cases.md](evals/cases.md) for bounded report and chart behavior checks. Review generated artifacts as well as source data; a passing structural check does not establish scientific or visual correctness.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for scope and contribution rules. Releases use semantic version tags; changes are recorded in [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE)

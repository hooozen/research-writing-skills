# Research Writing Skills

Reusable, agent-neutral skills for turning research evidence into self-contained progress reports and precise clinical-data figures.

Each skill is a self-contained directory built around `SKILL.md`. Supporting references, scripts, assets, and optional agent adapters stay inside the same directory, so a skill can be installed by copying one folder.

## Skills

| Skill | Purpose |
|---|---|
| [`research-progress-report`](skills/research-progress-report/) | Draft or revise self-contained, evidence-led progress reports for different languages, audiences, and public or lab-meeting contexts. Accepts an optional user outline, outputs Markdown or HTML with KaTeX-compatible mathematics, and keeps charts paired with exact-value tables. |
| [`clinical-data-chart-style`](skills/clinical-data-chart-style/) | Create consistent clinical, medical-imaging, OCT/OCTA, and healthcare charts with an implementation-neutral visual system. |

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

## Maintain

Use Python 3.10+ and install maintenance dependencies before validating changes:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
MPLBACKEND=Agg python3 -m unittest discover -s tests -v
```

These dependencies are for maintainers, not installation requirements. Installed skill instructions remain agent-neutral; Matplotlib is needed only for its optional example. Validation parses YAML, checks catalog consistency and relative Markdown resources throughout each skill, validates optional UI metadata, and checks script syntax without executing skill scripts or creating bytecode in their folders. It does not verify remote URLs, Markdown anchor IDs, raw HTML links, or scientific reasoning.

Use [evals/cases.md](evals/cases.md) for bounded report and chart behavior checks. Review generated artifacts as well as source data; a passing structural check does not establish scientific or visual correctness.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for scope and contribution rules. Releases use semantic version tags; changes are recorded in [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE)

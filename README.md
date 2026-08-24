# Research Writing Skills

Reusable, agent-neutral skills for turning research evidence into clear reports, figures, manuscripts, reviews, and presentations.

Each skill is a self-contained directory built around `SKILL.md`. Supporting references, scripts, assets, and optional agent adapters stay inside the same directory, so a skill can be installed by copying one folder.

## Skills

| Skill | Purpose |
|---|---|
| [`research-progress-report`](skills/research-progress-report/) | Draft or revise self-contained, evidence-led progress reports for different languages, audiences, and public or lab-meeting contexts. Outputs Markdown or HTML and keeps charts paired with exact-value tables. |
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

The installer never overwrites an existing skill by default. To upgrade intentionally, add `--force`; the previous directory is moved to a timestamped backup before the new version is copied.

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

Validate the repository before publishing changes:

```sh
python3 scripts/validate.py
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for scope and contribution rules. Releases use semantic version tags; changes are recorded in [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE)

# Research Writing Skills

Agent skills for turning research evidence into progress reports, publication figures and scientific slides. They work with any agent that can read a `SKILL.md` folder (Claude Code, Codex and others).

| Skill | What it does |
|---|---|
| [`research-progress-report`](skills/research-progress-report/) | Writes self-contained progress reports (科研进展报告) that go from an overview down to the evidence in plain language. Model reports cover data splits, architecture, loss, training, checkpoint choice and metrics in full. Markdown, or HTML from a ready-made reading template. |
| [`scientific-chart-style`](skills/scientific-chart-style/) | 19 scientific chart types, each with a one-page card (inputs, calculation, limits) and a one-command renderer. Editable SVG/PDF plus PNG, saturated blue by default, designed grayscale for print. |
| [`scientific-presentation-style`](skills/scientific-presentation-style/) | The same look for PowerPoint: projector-size type, titles that state the point, and native editable charts and tables. |
| [`infohub-maintenance`](skills/infohub-maintenance/) | Optional. Maintains an existing InfoHub research workspace (project data, annotations, snapshots, report delivery, Web/MCP services). Nothing else depends on it. |

[`catalog.json`](catalog.json) lists the same skills for agents.

## Install

```sh
git clone https://github.com/hooozen/research-writing-skills.git
cd research-writing-skills
SKILLS_DIR=/path/to/your-agent/skills
```

Install one skill:

```sh
./scripts/install.sh --target "$SKILLS_DIR" research-progress-report
```

Or all of them (including the optional InfoHub skill):

```sh
./scripts/install.sh --target "$SKILLS_DIR" --all
```

The installer won't overwrite an existing skill. Add `--force` to upgrade; the old copy is moved to a timestamped backup first. Copying a folder by hand (`cp -R skills/<name> "$SKILLS_DIR/"`) works too.

Or ask your agent:

```text
Install the relevant skills from https://github.com/hooozen/research-writing-skills.
Follow AGENTS.md, check catalog.json first, copy whole skill folders,
and don't overwrite an existing installation without asking me.
```

Files under `agents/` are optional metadata for specific clients; the skills don't need them.

## Use

Just describe the task; the agent picks the skill. Some examples:

```text
帮我把这些实验记录整理成一份组会进展报告，听众是本领域的研究生，输出 HTML。
```

```text
Plot these labels and scores as a ROC curve for an 89 mm single column, color and grayscale versions.
```

```text
用这些结果做三页科研汇报 PPT，图表要能在 PowerPoint 里改数据。
```

To render a chart directly:

```sh
python skills/scientific-chart-style/scripts/render_chart.py --list
python skills/scientific-chart-style/scripts/render_chart.py --chart paired \
  --input path/to/pairs.json --mode grayscale --output-dir path/to/figures
```

`--example` draws a labeled synthetic demo instead of your data. Without `--input` or `--example` the renderer refuses to run, so missing data never turns into demo data.

## Upgrading from `clinical-data-chart-style`

`scientific-chart-style` replaced `clinical-data-chart-style` in v1.0.0. Install the new folder, update any prompts that name the old skill, and move the old folder (and any backups containing a `SKILL.md`) out of your agent's skills directory so it isn't loaded twice. The installer doesn't remove old names for you.

## Maintain

Python 3.10+; Node.js 20+ for the presentation adapter tests.

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 skills/scientific-chart-style/scripts/build_chart_references.py --check
MPLBACKEND=Agg python3 -m unittest discover -s tests -v
node --test tests/presentation_adapter.test.mjs
```

`validate.py` checks the catalog, YAML, relative links and script syntax. It doesn't check remote URLs, anchors, or whether the science or the visuals are right: for that, run the relevant [evaluation cases](evals/cases.md) and look at the actual output.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules and [CHANGELOG.md](CHANGELOG.md) for history. Releases use semantic version tags.

## License

[MIT](LICENSE)

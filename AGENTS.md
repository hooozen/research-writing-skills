# Agent Installation Instructions

This repository is a catalog of portable skills. Each installable skill lives at `skills/<name>/` and has a required `SKILL.md` entrypoint.

## Discover

1. Read `catalog.json` first. Do not load every skill body into context.
2. Match the user's task against each catalog description.
3. Read the selected skill's complete `SKILL.md` before installing or using it.
4. Read linked references only when the selected `SKILL.md` routes the current task to them.

## Install

1. Resolve the destination from the agent's documented or configured skills directory. Do not guess a privileged system path.
2. Inspect `scripts/install.sh` before executing it, then use:

   ```sh
   SKILL_NAME=research-progress-report
   ./scripts/install.sh --target "$SKILLS_DIR" "$SKILL_NAME"
   ```

3. Copy the entire skill directory. Do not flatten, rename, or omit `references/`, `scripts/`, `assets/`, or optional `agents/` content.
4. Do not overwrite an existing skill unless the user explicitly approves an upgrade. `--force` creates a timestamped backup.
5. After installation, confirm that `SKILL.md` exists and that its relative resource links resolve.

If shell execution is unavailable, perform the same operation with the agent's file tools. If the destination cannot be determined safely, report the selected skill and ask the user for the target directory.

## Use

Treat `SKILL.md` as the authoritative cross-agent instructions. Platform-specific files under `agents/` may improve one client experience but must not be required for the core workflow. Do not execute bundled scripts merely to inspect a skill; run them only when the selected skill and user task require them.

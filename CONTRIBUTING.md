# Contributing

Contributions should improve reusable research writing, reporting, evidence presentation, figures, review, or publication workflows.

## Add or update a skill

1. Use a lowercase hyphenated name and create `skills/<name>/SKILL.md`.
2. Keep the core instructions agent-neutral. Put optional platform metadata in `agents/` and never make it a runtime dependency.
3. Keep the entrypoint concise. Place conditional detail in linked `references/`, repeatable automation in `scripts/`, and output resources in `assets/`.
4. Do not invent evidence, citations, or permissions. Preserve the user's choices and the skill's stated scope.
5. Add or update the skill entry in `catalog.json` and document user-visible changes in `CHANGELOG.md`.
6. Run `python3 scripts/validate.py` and test any changed executable script before opening a pull request.

Pull requests should explain the use case, important behavior changes, validation performed, and any compatibility considerations. Keep unrelated changes separate.

## Releases

The repository uses semantic version tags:

- Patch: corrections that preserve intended behavior.
- Minor: new skills or backward-compatible capabilities.
- Major: incompatible skill layout or behavioral contract changes.

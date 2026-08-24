#!/usr/bin/env python3
"""Validate the repository catalog and portable skill structure."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_PATTERN = re.compile(r"```.*?```", re.DOTALL)


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")

    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as error:
        raise ValueError("missing closing YAML frontmatter delimiter") from error

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def validate_links(skill_file: Path, errors: list[str]) -> None:
    text = skill_file.read_text(encoding="utf-8")
    text = FENCED_CODE_PATTERN.sub("", text)
    for target in MARKDOWN_LINK_PATTERN.findall(text):
        if target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        relative_target = target.split("#", 1)[0]
        if relative_target and not (skill_file.parent / relative_target).exists():
            errors.append(f"{skill_file}: unresolved relative link {target!r}")


def main() -> int:
    errors: list[str] = []
    catalog_path = ROOT / "catalog.json"

    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"catalog.json: {error}", file=sys.stderr)
        return 1

    entries = catalog.get("skills")
    if not isinstance(entries, list):
        print("catalog.json: 'skills' must be a list", file=sys.stderr)
        return 1

    catalog_by_name = {entry.get("name"): entry for entry in entries if isinstance(entry, dict)}
    if len(catalog_by_name) != len(entries):
        errors.append("catalog.json: every entry needs a unique name")

    skill_directories = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    discovered_names = {path.name for path in skill_directories}
    if discovered_names != set(catalog_by_name):
        errors.append(
            "catalog.json names do not match skills directories: "
            f"catalog={sorted(catalog_by_name)}, directories={sorted(discovered_names)}"
        )

    for skill_directory in skill_directories:
        name = skill_directory.name
        skill_file = skill_directory / "SKILL.md"
        if not NAME_PATTERN.fullmatch(name):
            errors.append(f"{name}: directory name must be lowercase and hyphenated")
        if not skill_file.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue

        try:
            frontmatter = parse_frontmatter(skill_file)
        except ValueError as error:
            errors.append(f"{skill_file}: {error}")
            continue

        if frontmatter.get("name") != name:
            errors.append(f"{skill_file}: frontmatter name must match directory name")
        description = frontmatter.get("description", "").strip()
        if not description:
            errors.append(f"{skill_file}: description is required")
        if any(marker in skill_file.read_text(encoding="utf-8") for marker in ("[TODO", "TODO:")):
            errors.append(f"{skill_file}: unfinished TODO marker")

        entry = catalog_by_name.get(name, {})
        if entry.get("path") != f"skills/{name}":
            errors.append(f"catalog.json: invalid path for {name}")
        if entry.get("description") != description:
            errors.append(f"catalog.json: description differs from {skill_file}")
        validate_links(skill_file, errors)

        for script in (skill_directory / "scripts").glob("*.py") if (skill_directory / "scripts").is_dir() else ():
            try:
                py_compile.compile(str(script), doraise=True)
            except py_compile.PyCompileError as error:
                errors.append(f"{script}: {error.msg}")

    for error in errors:
        print(error, file=sys.stderr)

    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_directories)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

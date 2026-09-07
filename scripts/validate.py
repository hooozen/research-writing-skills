#!/usr/bin/env python3
"""Validate catalog metadata, YAML, portable resource links and script syntax.

Install maintenance dependencies from requirements-dev.txt. This check neither
executes bundled skill scripts nor creates bytecode inside installable skills.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from markdown_it import MarkdownIt
except ImportError:
    raise SystemExit("Install validation dependencies: python3 -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parent.parent
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN = MarkdownIt("commonmark")


class UniqueKeyLoader(yaml.SafeLoader):
    """Do not silently accept duplicate YAML keys."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def parse_yaml(text: str) -> dict:
    value = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError("YAML must be a mapping")
    return value


def split_frontmatter(path: Path) -> tuple[dict, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("missing closing YAML frontmatter delimiter")
    return parse_yaml("\n".join(lines[1:end])), "\n".join(lines[end + 1:])


def parse_frontmatter(path: Path) -> dict:
    return split_frontmatter(path)[0]


def valid_name(name) -> bool:
    return isinstance(name, str) and len(name) < 64 and bool(NAME_PATTERN.fullmatch(name))


def validate_target(document: Path, target: str, boundary: Path, errors: list[str]) -> None:
    try:
        url = urlsplit(target)
        if url.scheme and url.scheme != "file":
            return
        if url.netloc:
            return
        if not url.path:
            return
        path = Path(unquote(url.path))
        if url.scheme == "file" or path.is_absolute():
            raise ValueError(f"non-portable local link {target!r}")
        resolved = (document.parent / path).resolve()
        if not resolved.is_relative_to(boundary.resolve()):
            raise ValueError(f"resource link leaves its portable directory: {target!r}")
        if not resolved.exists():
            raise ValueError(f"unresolved relative link {target!r}")
    except (OSError, RuntimeError, ValueError) as error:
        errors.append(f"{document}: {error}")


def validate_links(document: Path, boundary: Path, errors: list[str]) -> None:
    text = document.read_text(encoding="utf-8")
    if document.name == "SKILL.md":
        _, text = split_frontmatter(document)
    # Markdown parsing handles reference links, images, escaped paths and code fences.
    for token in MARKDOWN.parse(text):
        for child in token.children or ():
            target = child.attrGet("href") if child.type == "link_open" else child.attrGet("src") if child.type == "image" else None
            if target is not None:
                validate_target(document, target, boundary, errors)


def validate(root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    try:
        catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"catalog.json: {error}"], 0
    if not isinstance(catalog, dict):
        return ["catalog.json must be an object"], 0
    if type(catalog.get("schema_version")) is not int or catalog["schema_version"] != 1:
        errors.append("catalog.json: schema_version must be 1")
    if not isinstance(catalog.get("release"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", catalog["release"]):
        errors.append("catalog.json: release must use major.minor.patch")
    entries = catalog.get("skills")
    if not isinstance(entries, list):
        return errors + ["catalog.json: 'skills' must be a list"], 0
    catalog_by_name: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not valid_name(entry.get("name")):
            errors.append(f"catalog.json: entry {index} needs a valid skill name")
            continue
        name = entry["name"]
        if name in catalog_by_name:
            errors.append(f"catalog.json: duplicate skill name {name!r}")
        catalog_by_name[name] = entry
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return errors + ["missing skills directory"], 0
    directories = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    discovered = {path.name for path in directories}
    if discovered != set(catalog_by_name):
        errors.append(f"catalog.json names do not match skills directories: catalog={sorted(catalog_by_name)}, directories={sorted(discovered)}")
    for entry in catalog_by_name.values():
        related = entry.get("related_skills", [])
        if not isinstance(related, list) or any(not isinstance(name, str) or name not in catalog_by_name for name in related):
            errors.append(f"catalog.json: invalid related_skills for {entry['name']}")
    for directory in directories:
        name = directory.name
        if directory.is_symlink():
            errors.append(f"{directory}: skill directory must not be a symlink")
            continue
        if not valid_name(name):
            errors.append(f"{name}: use a lowercase hyphenated name shorter than 64 characters")
        skill_file = directory / "SKILL.md"
        try:
            frontmatter, body = split_frontmatter(skill_file)
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{skill_file}: {error}")
            continue
        if frontmatter.get("name") != name:
            errors.append(f"{skill_file}: frontmatter name must match directory name")
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{skill_file}: nonempty string description is required")
        if isinstance(description, str) and ("[TODO" in description or "TODO:" in description):
            errors.append(f"{skill_file}: unfinished description placeholder")
        if "[TODO" in body or "TODO:" in body:
            errors.append(f"{skill_file}: unfinished TODO marker")
        entry = catalog_by_name.get(name, {})
        if entry.get("path") != f"skills/{name}":
            errors.append(f"catalog.json: invalid path for {name}")
        if entry.get("description") != description:
            errors.append(f"catalog.json: description differs from {skill_file}")
        for resource in directory.rglob("*"):
            if resource.is_symlink():
                try:
                    if not resource.resolve().is_relative_to(directory.resolve()):
                        errors.append(f"{resource}: symlink leaves the portable skill")
                    elif not resource.exists():
                        errors.append(f"{resource}: broken resource symlink")
                except (OSError, RuntimeError, ValueError) as error:
                    errors.append(f"{resource}: cannot resolve resource symlink: {error}")
        adapter = directory / "agents/openai.yaml"
        if adapter.exists():
            try:
                metadata = parse_yaml(adapter.read_text(encoding="utf-8"))
                interface = metadata.get("interface", {})
                if not isinstance(interface, dict):
                    raise ValueError("interface must be a mapping")
                for field in ("display_name", "short_description", "default_prompt"):
                    if field in interface and (not isinstance(interface[field], str) or not interface[field].strip()):
                        raise ValueError(f"interface.{field} must be a nonempty string")
                if "default_prompt" in interface and f"${name}" not in interface["default_prompt"]:
                    raise ValueError("default_prompt must mention the skill as $skill-name")
                for field in ("icon_small", "icon_large"):
                    if field in interface:
                        if not isinstance(interface[field], str):
                            raise ValueError(f"{field} must be a path string")
                        validate_target(directory / "SKILL.md", interface[field], directory, errors)
            except (OSError, ValueError, yaml.YAMLError) as error:
                errors.append(f"{adapter}: {error}")
    # Check reference documents as well as entrypoints; do not follow other skills' resources.
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts or document.is_symlink():
            continue
        relative = document.relative_to(root)
        boundary = skills_dir / relative.parts[1] if len(relative.parts) >= 3 and relative.parts[0] == "skills" else root
        try:
            validate_links(document, boundary, errors)
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{document}: {error}")
    for script in sorted(root.rglob("*.py")):
        if ".git" in script.parts or script.is_symlink():
            continue
        try:
            compile(script.read_bytes(), str(script), "exec")
        except (OSError, SyntaxError, ValueError) as error:
            errors.append(f"{script}: {error}")
    for script in sorted((root / "scripts").glob("*.sh")):
        result = subprocess.run(["sh", "-n", str(script)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f"{script}: {result.stderr.strip()}")
    return errors, len(directories)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository to validate (default: this repository)")
    errors, count = validate(parser.parse_args().root.resolve())
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated {count} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

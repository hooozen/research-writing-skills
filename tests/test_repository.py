"""Behavioral regressions for portable installation and repository validation."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_validator", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-install-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "repo"
        shutil.copytree(ROOT / "scripts", self.repo / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("alpha", "beta"):
            skill = self.repo / "skills" / name
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"fixture {name}")
            (skill / "references/details.md").write_text("nested resource")
        self.target = self.base / "target with spaces"

    def run_install(self, *args, env=None):
        return subprocess.run(["sh", str(self.repo / "scripts/install.sh"), "--target", str(self.target), *args], env=env, text=True, capture_output=True)

    def test_complete_copy_and_double_dash(self):
        result = self.run_install("--", "alpha")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / "alpha/references/details.md").read_text(), "nested resource")

    def test_duplicate_names_install_once(self):
        result = self.run_install("alpha", "alpha")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Installed:"), 1)
        self.assertFalse(list(self.target.glob("*.backup-*")))

    def test_all_installs_available_skills(self):
        result = self.run_install("--all")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({p.name for p in self.target.iterdir()}, {"alpha", "beta"})

    def test_list_has_no_destination_side_effect(self):
        result = self.run_install("--list")
        self.assertEqual(result.stdout.splitlines(), ["alpha", "beta"])
        self.assertFalse(self.target.exists())

    def test_path_traversal_rejected(self):
        (self.repo / "scripts/SKILL.md").write_text("outside source fixture")
        result = self.run_install("../scripts")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.base / "scripts").exists())
        self.assertFalse(self.target.exists())

    def test_invalid_names_are_not_split_or_expanded(self):
        for name in ("alpha beta", "*", "", "/alpha", "alpha--beta", "alpha/../beta", "x" * 64):
            with self.subTest(name=name):
                self.assertNotEqual(self.run_install("--", name).returncode, 0)
                self.assertFalse(self.target.exists())

    def test_unknown_selection_prevents_partial_install(self):
        self.assertNotEqual(self.run_install("alpha", "unknown").returncode, 0)
        self.assertFalse(self.target.exists())

    def test_existing_install_is_unchanged_without_force(self):
        self.assertEqual(self.run_install("alpha").returncode, 0)
        sentinel = self.target / "alpha/local.txt"
        sentinel.write_text("keep this")
        self.assertNotEqual(self.run_install("beta", "alpha").returncode, 0)
        self.assertEqual(sentinel.read_text(), "keep this")
        self.assertFalse((self.target / "beta").exists())

    def test_force_preserves_distinct_backups(self):
        self.assertEqual(self.run_install("alpha").returncode, 0)
        for text in ("first local version", "second local version"):
            (self.target / "alpha/local.txt").write_text(text)
            result = self.run_install("--force", "alpha", "alpha")
            self.assertEqual(result.returncode, 0, result.stderr)
        backups = list(self.target.glob("alpha.backup-*/local.txt"))
        self.assertEqual({p.read_text() for p in backups}, {"first local version", "second local version"})

    def test_broken_destination_symlink_counts_as_existing(self):
        self.target.mkdir()
        link = self.target / "alpha"
        link.symlink_to(self.base / "missing")
        self.assertNotEqual(self.run_install("alpha").returncode, 0)
        self.assertTrue(link.is_symlink())
        self.assertEqual(self.run_install("--force", "alpha").returncode, 0)
        backups = list(self.target.glob("alpha.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertTrue(backups[0].is_symlink())
        self.assertTrue((self.target / "alpha/SKILL.md").is_file())

    def test_source_symlink_rejected(self):
        (self.repo / "skills/gamma").symlink_to(self.repo / "skills/alpha", target_is_directory=True)
        self.assertNotEqual(self.run_install("gamma").returncode, 0)

    def test_self_install_cannot_move_source(self):
        self.target = self.repo / "skills"
        before = (self.target / "alpha/SKILL.md").read_bytes()
        self.assertNotEqual(self.run_install("--force", "alpha").returncode, 0)
        self.assertEqual((self.target / "alpha/SKILL.md").read_bytes(), before)
        self.assertFalse(list(self.target.glob("*.backup-*")))

    def test_failed_copy_keeps_existing_install(self):
        self.assertEqual(self.run_install("alpha").returncode, 0)
        (self.target / "alpha/local.txt").write_text("preserve me")
        fake_bin = self.base / "fake-bin"
        fake_bin.mkdir()
        fake_cp = fake_bin / "cp"
        fake_cp.write_text("#!/bin/sh\nexit 1\n")
        fake_cp.chmod(0o755)
        env = dict(os.environ, PATH=str(fake_bin) + os.pathsep + os.environ["PATH"])
        result = self.run_install("--force", "alpha", env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.target / "alpha/local.txt").read_text(), "preserve me")
        self.assertFalse(list(self.target.glob("*.backup-*")))
        self.assertFalse(list(self.target.glob(".skills-install.*")))


    def test_failed_final_move_restores_previous_install(self):
        self.assertEqual(self.run_install("alpha").returncode, 0)
        (self.target / "alpha/local.txt").write_text("restore me")
        fake_bin = self.base / "fake-mv-bin"
        fake_bin.mkdir()
        fake_mv = fake_bin / "mv"
        real_mv = shutil.which("mv")
        fake_mv.write_text('#!/bin/sh\nif [ "$1" = "--" ]; then shift; fi\ncase "$1" in */.skills-install.*/*) exit 1 ;; esac\nexec "' + real_mv + '" "$@"\n')
        fake_mv.chmod(0o755)
        env = dict(os.environ, PATH=str(fake_bin) + os.pathsep + os.environ["PATH"])
        result = self.run_install("--force", "alpha", env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.target / "alpha/local.txt").read_text(), "restore me")
        self.assertTrue((self.target / "alpha/references/details.md").is_file())
        self.assertFalse(list(self.target.glob(".skills-install.*")))


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-validation-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skill = self.root / "skills/alpha"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text('---\nname: alpha\ndescription: "Alpha skill"\n---\n[Guide](references/guide.md)\n')
        (self.skill / "references/guide.md").write_text("A guide.\n")
        self.catalog = {"schema_version": 1, "release": "0.1.0", "skills": [{"name": "alpha", "path": "skills/alpha", "description": "Alpha skill"}]}
        self.write_catalog()

    def write_catalog(self):
        (self.root / "catalog.json").write_text(json.dumps(self.catalog))

    def errors(self):
        return validator.validate(self.root)[0]

    def test_valid_repository_does_not_write_bytecode(self):
        (self.skill / "scripts").mkdir()
        (self.skill / "scripts/example.py").write_text('print("example")\n')
        self.assertEqual(self.errors(), [])
        self.assertFalse(list(self.root.rglob("__pycache__")))

    def test_broken_link_in_reference_is_detected(self):
        (self.skill / "references/guide.md").write_text('[Read more][details]\n\n[details]: absent.md "Title"\n')
        self.assertTrue(any("absent.md" in error for error in self.errors()))

    def test_link_titles_encoded_paths_and_code_fences(self):
        (self.skill / "references/a file.md").write_text("Content")
        (self.skill / "references/guide.md").write_text('[link](a%20file.md "Title")\n~~~md\n[Example only](missing.md)\n~~~\n')
        self.assertEqual(self.errors(), [])

    def test_resource_cannot_depend_on_sibling_skill(self):
        (self.root / "shared.md").write_text("nonportable")
        (self.skill / "references/guide.md").write_text('[outside](../../../shared.md)')
        self.assertTrue(any("leaves" in error for error in self.errors()))

    def test_frontmatter_accepts_valid_folded_yaml(self):
        (self.skill / "SKILL.md").write_text('---\nname: alpha\ndescription: >-\n  Alpha\n  skill\nmetadata:\n  short-description: "Example"\n---\n')
        self.assertEqual(self.errors(), [])

    def test_frontmatter_rejects_malformed_or_duplicate_yaml(self):
        for body in ('name: alpha\ndescription: [', 'name: alpha\nname: beta\ndescription: Alpha skill'):
            with self.subTest(body=body):
                (self.skill / "SKILL.md").write_text(f"---\n{body}\n---\n")
                self.assertTrue(self.errors())

    def test_malformed_catalogs_report_errors_without_exceptions(self):
        for catalog in ([], None, {"skills": [{}]}, {"skills": [{"name": []}]}, {"skills": None}):
            with self.subTest(catalog=catalog):
                self.catalog = catalog
                self.write_catalog()
                self.assertTrue(self.errors())

    def test_duplicate_names_and_unknown_related_skill(self):
        self.catalog['skills'][0]['related_skills'] = ['absent']
        self.catalog['skills'].append(dict(self.catalog['skills'][0]))
        self.write_catalog()
        errors = self.errors()
        self.assertTrue(any("duplicate" in error for error in errors))
        self.assertTrue(any("related_skills" in error for error in errors))

    def test_invalid_optional_adapter_is_detected(self):
        (self.skill / "agents").mkdir()
        (self.skill / "agents/openai.yaml").write_text("interface: [broken\n")
        self.assertTrue(any("openai.yaml" in error for error in self.errors()))

    def test_nested_python_syntax_is_checked(self):
        nested = self.skill / "scripts/nested"
        nested.mkdir(parents=True)
        (nested / "broken.py").write_text("def broken(:\n")
        self.assertTrue(any("broken.py" in error for error in self.errors()))

    def test_description_placeholder_is_not_a_valid_description(self):
        self.catalog['skills'][0]['description'] = '[TODO: describe capability]'
        self.write_catalog()
        (self.skill / "SKILL.md").write_text('---\nname: alpha\ndescription: "[TODO: describe capability]"\n---\n')
        self.assertTrue(any("description placeholder" in error for error in self.errors()))

    def test_symlink_cycle_is_reported_without_crashing(self):
        (self.skill / "references/loop").symlink_to("loop")
        self.assertTrue(any("symlink" in error for error in self.errors()))

    def test_missing_skills_directory_is_reported(self):
        shutil.rmtree(self.root / "skills")
        self.assertTrue(any("missing skills directory" in error for error in self.errors()))


if __name__ == "__main__":
    unittest.main()

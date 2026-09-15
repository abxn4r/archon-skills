"""
Tests for Archon cross-agent export adapters.
Verifies file generation for Cursor, Claude Code, Windsurf, Copilot, Cline, Aider, Antigravity.
"""

import tempfile
import unittest
from pathlib import Path

from adapters import run_export, ADAPTER_MAP


class TestAdapters(unittest.TestCase):

    def setUp(self):
        self.skills_dir = Path(__file__).resolve().parent.parent / "skills"
        self.temp_dir = tempfile.TemporaryDirectory()
        self.out_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cursor_export(self):
        """Verify Cursor .cursor/rules/*.mdc generation with alwaysApply: false."""
        files = run_export("cursor", self.skills_dir, self.out_dir)
        self.assertGreaterEqual(len(files), 6)
        saltzer_mdc = self.out_dir / ".cursor" / "rules" / "saltzer.mdc"
        self.assertTrue(saltzer_mdc.exists())
        content = saltzer_mdc.read_text(encoding="utf-8")
        self.assertIn("alwaysApply: false", content)
        self.assertIn("globs:", content)

    def test_claude_code_export(self):
        """Verify Claude Code .claude/skills/ and plugin.json generation."""
        files = run_export("claude_code", self.skills_dir, self.out_dir)
        self.assertGreaterEqual(len(files), 6)
        plugin_file = self.out_dir / ".claude-plugin" / "plugin.json"
        self.assertTrue(plugin_file.exists())
        skill_file = self.out_dir / ".claude" / "skills" / "dijkstra" / "SKILL.md"
        self.assertTrue(skill_file.exists())

    def test_windsurf_export(self):
        """Verify Windsurf .windsurfrules and workflow generation."""
        files = run_export("windsurf", self.skills_dir, self.out_dir)
        rules_file = self.out_dir / ".windsurfrules"
        self.assertTrue(rules_file.exists())
        content = rules_file.read_text(encoding="utf-8")
        self.assertIn("MICRO-ROUTER", content)

    def test_copilot_export(self):
        """Verify GitHub Copilot compact instructions."""
        files = run_export("copilot", self.skills_dir, self.out_dir)
        copilot_file = self.out_dir / ".github" / "copilot-instructions.md"
        self.assertTrue(copilot_file.exists())
        content = copilot_file.read_text(encoding="utf-8")
        self.assertLess(len(content.split()), 400)

    def test_cline_export(self):
        """Verify Cline .clinerules and .roomodes generation."""
        files = run_export("cline", self.skills_dir, self.out_dir)
        self.assertTrue((self.out_dir / ".clinerules").exists())
        self.assertTrue((self.out_dir / ".roomodes").exists())

    def test_aider_export(self):
        """Verify Aider CONVENTIONS.md and .aider.conf.yml generation."""
        files = run_export("aider", self.skills_dir, self.out_dir)
        self.assertTrue((self.out_dir / "CONVENTIONS.md").exists())
        self.assertTrue((self.out_dir / ".aider.conf.yml").exists())

    def test_antigravity_export(self):
        """Verify Antigravity .agents/skills/ export."""
        files = run_export("antigravity", self.skills_dir, self.out_dir)
        self.assertTrue((self.out_dir / ".agents" / "skills" / "ARCHON_ROUTER.md").exists())

    def test_export_all(self):
        """Verify full export targeting all agents."""
        files = run_export("all", self.skills_dir, self.out_dir)
        self.assertGreater(len(files), 25)


if __name__ == "__main__":
    unittest.main()

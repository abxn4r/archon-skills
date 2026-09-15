"""
Tests for Archon universal CLI commands.
Verifies command dispatch, argument parsing, and return codes.
"""

import os
import tempfile
import unittest
from pathlib import Path
from io import StringIO
import contextlib

from archon.cli import main


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.temp_global = tempfile.TemporaryDirectory()
        self.temp_repo = tempfile.TemporaryDirectory()
        os.environ["ARCHON_GLOBAL_ROOT"] = self.temp_global.name
        self.repo_dir = Path(self.temp_repo.name)
        (self.repo_dir / ".archon").mkdir()

    def tearDown(self):
        del os.environ["ARCHON_GLOBAL_ROOT"]
        self.temp_global.cleanup()
        self.temp_repo.cleanup()

    def run_cli(self, args):
        """Helper to invoke CLI with captured stdout."""
        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = main(args)
        return exit_code, stdout.getvalue()

    def test_cli_record_and_query(self):
        """Test recording and querying via CLI."""
        code, out = self.run_cli([
            "record",
            "--advisor", "seneca",
            "--type", "decision",
            "--data", "Decided to ship CLI first",
            "--tags", "cli,strategy",
        ])
        self.assertEqual(code, 0)
        self.assertIn("SUCCESS", out)

        code_q, out_q = self.run_cli(["query", "ship"])
        self.assertEqual(code_q, 0)
        self.assertIn("SENECA", out_q)

    def test_cli_stats_and_debt(self):
        """Test stats and debt subcommands."""
        code_s, out_s = self.run_cli(["stats"])
        self.assertEqual(code_s, 0)
        self.assertIn("ARCHON INSTITUTIONAL MEMORY METRICS", out_s)

        code_d, out_d = self.run_cli(["debt"])
        self.assertEqual(code_d, 0)
        self.assertIn("SALTZER SECURITY DEBT", out_d)

    def test_cli_council(self):
        """Test council deliberation via CLI."""
        code, out = self.run_cli(["council", "Adopt Rust for performance critical modules", "--no-record"])
        self.assertEqual(code, 0)
        self.assertIn("ARCHON EXECUTIVE BOARD CONSENSUS COUNCIL", out)

    def test_cli_detect(self):
        """Test detect subcommand."""
        code, out = self.run_cli(["detect"])
        self.assertEqual(code, 0)
        self.assertIn("DETECTED AI CODING AGENTS", out)

    def test_cli_dashboard_snapshot(self):
        """Test dashboard in non-interactive snapshot mode."""
        code, out = self.run_cli(["dashboard", "--snapshot"])
        self.assertEqual(code, 0)
        self.assertIn("ARCHON EXPERT ADVISOR SUITE", out)


if __name__ == "__main__":
    unittest.main()

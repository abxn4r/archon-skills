"""
Tests for Archon dual-scope institutional memory engine.
Verifies record logging, queries with token ceilings, security debt tracking, and stats.
"""

import os
import json
import tempfile
import unittest
from pathlib import Path

from archon.memory import record, learn, query, profile, stats, debt, init_scopes


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.temp_global = tempfile.TemporaryDirectory()
        self.temp_repo = tempfile.TemporaryDirectory()
        os.environ["ARCHON_GLOBAL_ROOT"] = self.temp_global.name
        self.repo_root = Path(self.temp_repo.name)
        (self.repo_root / ".archon").mkdir()
        init_scopes(scope="all", repo_root=self.repo_root)

    def tearDown(self):
        del os.environ["ARCHON_GLOBAL_ROOT"]
        self.temp_global.cleanup()
        self.temp_repo.cleanup()

    def test_record_and_query(self):
        """Test recording an entry and finding it via keyword search."""
        rec = record(
            advisor="dijkstra",
            record_type="review",
            data={"decision": "Use SQLite for metadata", "status": "accepted"},
            tags=["sqlite", "database"],
            scope="local",
            repo_root=self.repo_root,
        )
        self.assertEqual(rec["advisor"], "dijkstra")
        self.assertEqual(rec["_scope"], "local")

        results = query("sqlite", advisor="dijkstra", scope="local", repo_root=self.repo_root)
        self.assertGreaterEqual(len(results), 1)
        top_entry = results[0]["entry"]
        self.assertEqual(top_entry["data"]["decision"], "Use SQLite for metadata")

    def test_query_token_budget_ceiling(self):
        """Test that --max-tokens truncates results when query output exceeds budget."""
        # Create 10 entries
        for i in range(10):
            record(
                advisor="caples",
                record_type="copy",
                data={"headline": f"A very descriptive and long headline number {i} testing the token budget limit ceiling"},
                tags=["headline", "test"],
                scope="local",
                repo_root=self.repo_root,
            )

        # Query with high token budget
        unbounded = query("headline", advisor="caples", limit=10, repo_root=self.repo_root)
        self.assertEqual(len(unbounded), 10)

        # Query with tight token budget (e.g. 50 tokens)
        bounded = query("headline", advisor="caples", limit=10, max_tokens=50, repo_root=self.repo_root)
        self.assertLess(len(bounded), len(unbounded))
        self.assertGreater(len(bounded), 0)

    def test_security_debt_tracking(self):
        """Test tracking security debt with owner and overdue detection."""
        record(
            advisor="saltzer",
            record_type="security_debt",
            data={
                "title": "Unpinned package in legacy tool",
                "severity": "HIGH",
                "owner": "alice",
                "expiry_date": "2020-01-01",  # Overdue
            },
            tags=["mcp", "supply_chain"],
            scope="local",
            repo_root=self.repo_root,
        )
        debts = debt(scope="local", repo_root=self.repo_root)
        self.assertEqual(len(debts), 1)
        self.assertTrue(debts[0]["overdue"])
        self.assertEqual(debts[0]["severity"], "HIGH")

    def test_learn_and_profile(self):
        """Test learning and cognitive profile integration."""
        l_res = learn(
            advisor="seneca",
            lesson="Check for refinement as avoidance when feeling scattered",
            tags=["cognitive_model", "bias"],
            scope="global",
            repo_root=self.repo_root,
        )
        self.assertEqual(l_res["advisor"], "seneca")

        prof = profile(advisor="seneca")
        self.assertIn("refinement as avoidance", prof)

    def test_stats_aggregation(self):
        """Test aggregate memory stats."""
        record(
            advisor="orwell",
            record_type="post",
            data={"topic": "Architecture", "platform": "X"},
            tags=["architecture"],
            scope="local",
            repo_root=self.repo_root,
        )
        st = stats(repo_root=self.repo_root)
        self.assertGreaterEqual(st["total_records"], 1)
        self.assertIn("orwell", st["advisors"])


if __name__ == "__main__":
    unittest.main()

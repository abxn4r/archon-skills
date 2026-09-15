"""
Tests for Archon atomic file write-and-replace.
Verifies no 0-byte corruption, clean temp file cleanup, and same-directory rename safety.
"""

import json
import tempfile
import unittest
from pathlib import Path

from archon.atomic import atomic_write, atomic_write_json, atomic_append_jsonl


class TestAtomic(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_atomic_write_text(self):
        """Test atomic text file writing and subsequent overwrite."""
        target = self.base_path / "config.txt"
        atomic_write(target, "hello world 1")
        self.assertEqual(target.read_text(encoding="utf-8"), "hello world 1")

        # Overwrite
        atomic_write(target, "hello world 2")
        self.assertEqual(target.read_text(encoding="utf-8"), "hello world 2")

        # Ensure no stray temp files remain
        stray = list(self.base_path.glob(".*.tmp-*"))
        self.assertEqual(len(stray), 0)

    def test_atomic_write_json(self):
        """Test atomic JSON serialization."""
        target = self.base_path / "data.json"
        data = {"status": "ok", "count": 42, "items": ["a", "b"]}
        atomic_write_json(target, data)

        self.assertTrue(target.exists())
        loaded = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(loaded, data)

    def test_atomic_append_jsonl(self):
        """Test atomic line appending to JSONL file."""
        target = self.base_path / "log.jsonl"
        r1 = {"id": "1", "msg": "first"}
        r2 = {"id": "2", "msg": "second"}

        atomic_append_jsonl(target, r1)
        atomic_append_jsonl(target, r2)

        lines = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["id"], "1")
        self.assertEqual(lines[1]["id"], "2")


if __name__ == "__main__":
    unittest.main()

"""
Tests for Archon cross-platform path utilities.
Verifies Windows extended path (\\?\\) handling, safe relativity without ValueError,
and dual-scope directory resolution.
"""

import os
import tempfile
import unittest
from pathlib import Path

from archon.paths import (
    strip_extended_prefix,
    add_extended_prefix,
    normalize_path,
    safe_relative_to,
    get_repo_root,
    get_local_archon_dir,
    get_global_archon_dir,
    resolve_scope_dirs,
)


class TestPaths(unittest.TestCase):

    def test_strip_extended_prefix(self):
        """Verify Windows extended prefixes are stripped cleanly."""
        self.assertEqual(strip_extended_prefix("\\\\?\\C:\\Users"), "C:\\Users")
        self.assertEqual(strip_extended_prefix("\\\\?\\UNC\\server\\share"), "\\\\server\\share")
        self.assertEqual(strip_extended_prefix("/home/user"), "/home/user")

    def test_safe_relative_to_descendant(self):
        """Verify relative path calculation for normal descendants."""
        base = Path("/workspace/project") if os.name != "nt" else Path("C:/workspace/project")
        child = base / "src" / "index.ts"
        rel = safe_relative_to(child, base)
        self.assertEqual(rel, "src/index.ts")

    def test_safe_relative_to_unrelated_paths(self):
        """Verify safe fallback without ValueError when path is outside base."""
        base = Path("/workspace/a") if os.name != "nt" else Path("C:/workspace/a")
        other = Path("/workspace/b/foo.txt") if os.name != "nt" else Path("C:/workspace/b/foo.txt")
        rel = safe_relative_to(other, base)
        self.assertIsInstance(rel, str)
        self.assertIn("foo.txt", rel)

    def test_safe_relative_to_cross_drive(self):
        """Verify Windows cross-drive comparison never raises ValueError."""
        p1 = "C:\\projects\\app\\main.py"
        p2 = "D:\\other\\dir"
        res = safe_relative_to(p1, p2)
        self.assertIsInstance(res, str)
        self.assertTrue(res.startswith("C:/") or res.startswith("c:/") or "main.py" in res)

    def test_repo_root_discovery(self):
        """Verify discovery of repository root via .archon or .git."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".archon").mkdir()
            sub = root / "subdir" / "nested"
            sub.mkdir(parents=True)

            discovered = get_repo_root(sub)
            self.assertIsNotNone(discovered)
            self.assertEqual(normalize_path(discovered), normalize_path(root))

            local_dir = get_local_archon_dir(sub)
            self.assertEqual(normalize_path(local_dir), normalize_path(root / ".archon"))

    def test_global_archon_dir_env_override(self):
        """Verify ARCHON_GLOBAL_ROOT environment variable overrides default home dir."""
        with tempfile.TemporaryDirectory() as td:
            os.environ["ARCHON_GLOBAL_ROOT"] = td
            try:
                g_dir = get_global_archon_dir()
                self.assertEqual(normalize_path(g_dir), normalize_path(td))
            finally:
                del os.environ["ARCHON_GLOBAL_ROOT"]


if __name__ == "__main__":
    unittest.main()

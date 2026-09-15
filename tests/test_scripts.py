"""
Unit tests for the 4 zero-dependency empirical verification scripts:
- verify_evidence_quotes.py (Dijkstra)
- audit_mcp_config.py (Saltzer)
- check_contrast.py (Aperture)
- analyze_copy.py (Caples)
"""

import unittest
from pathlib import Path

# Import scripts dynamically or directly
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from skills.dijkstra.scripts.verify_evidence_quotes import extract_quotes, search_in_source
from skills.saltzer.scripts.audit_mcp_config import audit_config
from skills.aperture.scripts.check_contrast import parse_color, wcag_contrast_ratio, apca_contrast
from skills.caples.scripts.analyze_copy import analyze


class TestEmpiricalScripts(unittest.TestCase):

    def test_verify_evidence_quotes(self):
        """Test substring citation extraction and matching."""
        doc = 'The spec claimed "extracted 24 artifacts" and cited `authenticate_user` function.'
        quotes = extract_quotes(doc)
        self.assertIn("extracted 24 artifacts", quotes)
        self.assertIn("authenticate_user", quotes)

        # Search within this test file
        matches = search_in_source("The spec claimed", Path(__file__).resolve())
        self.assertGreaterEqual(len(matches), 1)

    def test_audit_mcp_config(self):
        """Test detection of MCP security risks."""
        unsafe_config = {
            "mcpServers": {
                "danger_shell": {"command": "powershell.exe", "args": ["-Command", "ls"]},
                "unpinned_pkg": {"command": "npx", "args": ["-y", "super-tool"]},
                "root_fs": {"command": "node", "args": ["app.js", "/"]},
                "exposed_secret": {"command": "node", "args": ["app.js"], "env": {"OPENAI_API_KEY": "sk-12345"}},
                "clean_server": {"command": "node", "args": ["server.js", "src/dir"], "env": {"PORT": "8080"}},
            }
        }
        res = audit_config(unsafe_config)
        self.assertEqual(res["finding_count"], 4)
        severities = [f["severity"] for f in res["findings"]]
        self.assertIn("CRITICAL", severities)
        self.assertIn("HIGH", severities)

    def test_check_contrast(self):
        """Test WCAG ratio and APCA calculation."""
        # Pure black (#000000) on pure white (#FFFFFF)
        fg = parse_color("#FFFFFF")
        bg = parse_color("#000000")
        ratio = wcag_contrast_ratio(fg, bg)
        self.assertAlmostEqual(ratio, 21.0, places=1)

        # Linear dark theme (#EDEDED on #0D0E11)
        fg_lin = parse_color("#EDEDED")
        bg_lin = parse_color("#0D0E11")
        ratio_lin = wcag_contrast_ratio(fg_lin, bg_lin)
        self.assertGreater(ratio_lin, 15.0)

        # APCA check
        apca_val = abs(apca_contrast(fg_lin, bg_lin))
        self.assertGreater(apca_val, 80.0)

    def test_analyze_copy(self):
        """Test readability and AI cliché detection."""
        cliche_text = "We delve into this game-changer platform to seamlessly elevate your workflow in the realm of AI."
        res = analyze(cliche_text)
        self.assertGreaterEqual(len(res["cliches"]), 3)
        matches = [c["match"].lower() for c in res["cliches"]]
        self.assertIn("delve", matches)
        self.assertIn("game-changer", matches)
        self.assertIn("seamlessly", matches)

        clean_text = "Archon is fast and simple. It runs with zero extra packages. You can start in seconds."
        res_clean = analyze(clean_text)
        self.assertEqual(len(res_clean["cliches"]), 0)
        self.assertGreater(res_clean["flesch_reading_ease"], 60.0)


if __name__ == "__main__":
    unittest.main()

"""
Tests for Archon agent auto-detector.
"""

import unittest
from archon.detector import detect_installed_agents, AGENT_DEFINITIONS


class TestDetector(unittest.TestCase):

    def test_detector_execution(self):
        """Verify detector runs without error and returns structured agent list."""
        detected = detect_installed_agents()
        self.assertIsInstance(detected, list)
        for a in detected:
            self.assertIn("id", a)
            self.assertIn("name", a)
            self.assertIn("adapter", a)
            self.assertIn("target_desc", a)
            self.assertIn("evidence", a)

    def test_agent_definitions_integrity(self):
        """Verify all registered agent definitions have valid schemas."""
        for k, v in AGENT_DEFINITIONS.items():
            self.assertIn("name", v)
            self.assertIn("adapter", v)
            self.assertIn("target_desc", v)


if __name__ == "__main__":
    unittest.main()

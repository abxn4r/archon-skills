"""
Tests for Archon agentskills.io schema validator and 500-line budget enforcer.
"""

import tempfile
import unittest
from pathlib import Path

from archon.validator import validate_skill, validate_all_skills, MAX_SKILL_LINES


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.skills_dir = Path(__file__).resolve().parent.parent / "skills"

    def test_canonical_skills_pass_validation(self):
        """Verify all canonical skills in the repo pass validation and stay under 500 lines."""
        report = validate_all_skills(self.skills_dir)
        self.assertTrue(report["all_passed"], f"Validation failed: {report['skills']}")
        self.assertGreaterEqual(report["total"], 7)  # 6 advisors + council

        for s in report["skills"]:
            self.assertTrue(s["valid"], f"Skill {s['name']} failed validation: {s['errors']}")
            self.assertLessEqual(
                s["line_count"],
                MAX_SKILL_LINES,
                f"Skill {s['name']} exceeds {MAX_SKILL_LINES} line budget: {s['line_count']} lines",
            )

    def test_budget_exceeded_fails_validation(self):
        """Verify that an oversized skill file triggers a validation error."""
        with tempfile.TemporaryDirectory() as td:
            skill_dir = Path(td) / "bloated_skill"
            skill_dir.mkdir()
            skill_file = skill_dir / "SKILL.md"

            oversized_content = (
                "---\n"
                "name: bloated\n"
                "description: A bloated test skill\n"
                "---\n"
                "# BLOATED SKILL\n"
                "Evidence: Observed, Inference, Hypothesis, Unknown.\n"
                + "\n".join(f"Line {i}" for i in range(600))
            )
            skill_file.write_text(oversized_content, encoding="utf-8")

            res = validate_skill(skill_dir)
            self.assertFalse(res["valid"])
            self.assertTrue(any("500-line" in e for e in res["errors"]))


if __name__ == "__main__":
    unittest.main()

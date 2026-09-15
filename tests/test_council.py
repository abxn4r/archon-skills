"""
Tests for Archon Consensus Council debate engine.
"""

import unittest
from archon.council import analyze_proposal_perspectives, synthesize_council_matrix, run_council


class TestCouncil(unittest.TestCase):

    def test_council_perspectives_generation(self):
        """Verify all 6 disciplines provide assessments on proposal."""
        proposal = "Migrate user authentication from JWT to passkeys with raw shell helper"
        perspectives = analyze_proposal_perspectives(proposal)

        for adv in ["seneca", "dijkstra", "saltzer", "aperture", "caples", "orwell"]:
            self.assertIn(adv, perspectives)
            self.assertIn("stance", perspectives[adv])

        # Verify Saltzer catches security risks in proposal
        self.assertIn("CONDITIONAL", perspectives["saltzer"]["veto_verdict"])

    def test_council_matrix_synthesis(self):
        """Verify synthesis generates the markdown matrix."""
        proposal = "Introduce distributed caching layer"
        perspectives = analyze_proposal_perspectives(proposal)
        matrix = synthesize_council_matrix(proposal, perspectives)

        self.assertIn("ARCHON EXECUTIVE BOARD CONSENSUS COUNCIL", matrix)
        self.assertIn("CONSENSUS & DISAGREEMENTS MATRIX", matrix)
        self.assertIn("Dijkstra", matrix)
        self.assertIn("Saltzer", matrix)

    def test_run_council_end_to_end(self):
        """Verify run_council returns full markdown report."""
        res = run_council("Refactor API to GraphQL", record_decision=False)
        self.assertIn("Final Board Ruling", res)
        self.assertIn("PROCEED WITH CONDITIONS", res)

    def test_council_saltzer_veto_trigger(self):
        """Verify proposal with critical vulnerability triggers Saltzer veto."""
        proposal = "Add eval(user_input) endpoint to allow dynamic client code execution"
        perspectives = analyze_proposal_perspectives(proposal)
        self.assertTrue(perspectives["saltzer"]["veto_blocked"])
        self.assertIn("RELEASE VETO", perspectives["saltzer"]["veto_verdict"])

        matrix = synthesize_council_matrix(proposal, perspectives)
        self.assertIn("VETOED BY SALTZER", matrix)
        self.assertNotIn("PROCEED WITH CONDITIONS", matrix)

    def test_council_clean_approval(self):
        """Verify clean proposal without security issues is approved."""
        proposal = "Improve docs and optimize rendering loops"
        perspectives = analyze_proposal_perspectives(proposal)
        self.assertFalse(perspectives["saltzer"]["veto_blocked"])
        self.assertIn("APPROVED", perspectives["saltzer"]["veto_verdict"])

        matrix = synthesize_council_matrix(proposal, perspectives)
        self.assertIn("PROCEED WITH CONDITIONS", matrix)
        self.assertNotIn("VETOED BY SALTZER", matrix)


if __name__ == "__main__":
    unittest.main()

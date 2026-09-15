"""
GitHub Copilot Adapter
Exports a ultra-compact (<400 tokens) instruction file to .github/copilot-instructions.md.
"""

from pathlib import Path
from typing import List

from adapters.base import BaseAdapter
from archon.atomic import atomic_write


class CopilotAdapter(BaseAdapter):
    """Exports skills to GitHub Copilot .github/copilot-instructions.md format."""

    def export(self) -> List[Path]:
        github_dir = self.output_dir / ".github"
        github_dir.mkdir(parents=True, exist_ok=True)

        copilot_content = (
            "# Archon Expert Rules for Copilot\n\n"
            "## Epistemic Evidence Tiers\n"
            "Label non-trivial statements: **Observed** (fact in code), **Inference** (deduction), "
            "**Hypothesis** (unconfirmed theory), **Unknown** (missing info). Never state inference as fact.\n\n"
            "## Micro-Router Table\n"
            "- **Seneca** (Strategy): Irreversible Type 1 vs Type 2 choices; call out avoidance-as-refinement.\n"
            "- **Dijkstra** (Architecture): Simplicity first; verify citations exist verbatim (`python skills/dijkstra/scripts/verify_evidence_quotes.py`).\n"
            "- **Saltzer** (Security): Critical finding = DO NOT SHIP veto. Least privilege, secure defaults.\n"
            "- **Aperture** (UX/UI): Linear craft standard; 4px grid; check contrast (`python skills/aperture/scripts/check_contrast.py`).\n"
            "- **Caples** (Copy): Specificity beats hype; headline first; scan cliches (`python skills/caples/scripts/analyze_copy.py`).\n"
            "- **Orwell** (Growth): Long-term developer reputation; technical case studies over vanity virality.\n"
            "- **Council**: High-stakes debate (`python -m archon.cli council \"<proposal>\"`).\n\n"
            "## Memory Protocol\n"
            "- Query: `python -m archon.cli query \"<topic>\" --max-tokens 250`\n"
            "- Record: `python -m archon.cli record --advisor <name> --type <type> --data \"<data>\"`\n"
        )

        target_file = github_dir / "copilot-instructions.md"
        atomic_write(target_file, copilot_content)
        return [target_file]

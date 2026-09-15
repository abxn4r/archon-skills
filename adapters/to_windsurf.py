"""
Windsurf Adapter
Exports Archon skill router to .windsurfrules and Cascade workflow configurations.
"""

from pathlib import Path
from typing import List

from adapters.base import BaseAdapter
from archon.atomic import atomic_write


class WindsurfAdapter(BaseAdapter):
    """Exports skills to Windsurf .windsurfrules and Cascade workflows."""

    def export(self) -> List[Path]:
        generated = []

        # 1. Generate .windsurfrules
        rules_content = (
            "# ARCHON SKILL SUITE -- WINDSURF RULES\n\n"
            "## EPISTEMOLOGICAL EVIDENCE TIERS\n"
            "Distinguish strictly in all evaluations:\n"
            "- **Observed / Fact**: Directly visible in code, configuration, or verifiable output.\n"
            "- **Inference**: Reasonably drawn from visible facts; state the basis.\n"
            "- **Hypothesis**: Plausible interpretation or risk requiring confirmation.\n"
            "- **Unknown**: Critical context not available; state the gap explicitly.\n\n"
            "## EXPERT ADVISOR MICRO-ROUTER TABLE\n"
            "| Situation / Domain | Advisor | Key Directive |\n"
            "|---|---|---|\n"
            "| Strategy, leverage, irreversible choices | **Seneca** | Type 1 vs Type 2 doors; no refinement-as-avoidance |\n"
            "| Architecture, tech debt, PR reviews | **Dijkstra** | Simplicity first; verify evidence quotes on disk |\n"
            "| Security, auth, MCP tools, release audit | **Saltzer** | Critical finding = RELEASE VETO (DO NOT SHIP) |\n"
            "| UI, UX, design systems, craft | **Aperture** | Linear/Stripe craft standard; 4px grid; WCAG/APCA contrast |\n"
            "| Copy, messaging, positioning, landing pages | **Caples** | Specificity over hype; headline gatekeeper; no AI cliches |\n"
            "| Growth, developer reputation, open source | **Orwell** | Compounding credibility; technical blueprints over virality |\n"
            "| High-stakes dilemma or multi-discipline choice | **Council** | Multi-advisor debate & Consensus Matrix |\n\n"
            "## LOCAL TOOLS & MEMORY\n"
            "- Query Institutional Memory: `python -m archon.cli query \"<topic>\"`\n"
            "- Record Architectural Review: `python -m archon.cli record --advisor dijkstra --type review --data \"<json>\"`\n"
            "- Log Security Debt: `python -m archon.cli record --advisor saltzer --type security_debt --data \"<json>\"`\n"
            "- Log Learning: `python -m archon.cli learn --advisor <name> --lesson \"<lesson>\"`\n"
        )
        rules_file = self.output_dir / ".windsurfrules"
        atomic_write(rules_file, rules_content)
        generated.append(rules_file)

        # 2. Generate Cascade Workflows
        wf_dir = self.output_dir / ".windsurf" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)

        council_wf = (
            "# Cascade Workflow: Archon Consensus Council\n"
            "When facing an architectural dilemma or high-stakes technology choice:\n"
            "1. Run: `python -m archon.cli council \"<proposal>\"`\n"
            "2. Review the resulting Consensus & Disagreements Matrix.\n"
            "3. Ensure Saltzer has not triggered a Security Veto.\n"
        )
        cwf_file = wf_dir / "archon-council.md"
        atomic_write(cwf_file, council_wf)
        generated.append(cwf_file)

        return generated

"""
Cline & Roo Code Adapter
Exports instructions to .clinerules and custom role modes to .roomodes.
"""

from pathlib import Path
from typing import List

from adapters.base import BaseAdapter
from archon.atomic import atomic_write, atomic_write_json


class ClineAdapter(BaseAdapter):
    """Exports skills to Cline .clinerules and Roo Code .roomodes."""

    def export(self) -> List[Path]:
        generated = []

        # 1. .clinerules
        cline_content = (
            "# Archon Expert Rules for Cline\n\n"
            "## Epistemic Evidence Framework\n"
            "Always classify factual assessments before recommending changes:\n"
            "- **Observed**: Explicitly visible in the workspace files or CLI command execution.\n"
            "- **Inference**: Logically deduced from observed code; state the connecting premise.\n"
            "- **Hypothesis**: Plausible interpretation requiring confirmation.\n"
            "- **Unknown**: Context or code that was not inspected.\n\n"
            "## Specialist Advisor Activation\n"
            "- **Dijkstra** (Architecture): Challenge unnecessary abstractions. Verify quotes verbatim in codebase.\n"
            "- **Saltzer** (Security): RELEASE VETO: If any Critical vulnerability is found, halt release.\n"
            "- **Seneca** (Strategy): Focus on reversibility and leverage. Avoid refinement as avoidance.\n"
            "- **Aperture** (Design): Linear 4px spatial grid, WCAG AA & APCA contrast compliance.\n"
            "- **Caples** (Copy): Remove AI buzzwords (delve, leverage, seamless). Emphasize specificity.\n"
            "- **Orwell** (Growth): Technical blueprints and open-source credibility.\n"
            "- **Council**: High-stakes consensus debate (`python -m archon.cli council \"<topic>\"`).\n\n"
            "## Institutional Memory CLI\n"
            "- Query context: `python -m archon.cli query \"<query>\" --max-tokens 250`\n"
            "- Save ADR: `python -m archon.cli record --advisor dijkstra --type review --data \"<json>\"`\n"
            "- Track Security Debt: `python -m archon.cli record --advisor saltzer --type security_debt --data \"<json>\"`\n"
        )
        clinerules_file = self.output_dir / ".clinerules"
        atomic_write(clinerules_file, cline_content)
        generated.append(clinerules_file)

        # 2. .roomodes
        roomodes = {
            "customModes": [
                {
                    "slug": "archon-architect",
                    "name": "Dijkstra (Architecture)",
                    "roleDefinition": "You are Dijkstra, Principal Software Architect. You prioritize simplicity, maintainability, and empirical proof.",
                    "groups": ["read", "edit", "command"],
                },
                {
                    "slug": "archon-security",
                    "name": "Saltzer (Security)",
                    "roleDefinition": "You are Saltzer, Principal Application Security Engineer. You possess Release Veto authority.",
                    "groups": ["read", "command"],
                },
                {
                    "slug": "archon-strategy",
                    "name": "Seneca (Strategy)",
                    "roleDefinition": "You are Seneca, Strategic Advisor and Second Brain. You evaluate reversibility and opportunity cost.",
                    "groups": ["read"],
                },
                {
                    "slug": "archon-design",
                    "name": "Aperture (UI/UX)",
                    "roleDefinition": "You are Aperture, Design & UX Director. You enforce Linear/Stripe craft standards.",
                    "groups": ["read", "edit"],
                },
            ]
        }
        roomodes_file = self.output_dir / ".roomodes"
        atomic_write_json(roomodes_file, roomodes)
        generated.append(roomodes_file)

        return generated

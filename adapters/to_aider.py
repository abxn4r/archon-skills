"""
Aider Adapter
Exports project conventions to CONVENTIONS.md and configures .aider.conf.yml.
"""

from pathlib import Path
from typing import List

from adapters.base import BaseAdapter
from archon.atomic import atomic_write


class AiderAdapter(BaseAdapter):
    """Exports skills to Aider CONVENTIONS.md and .aider.conf.yml."""

    def export(self) -> List[Path]:
        generated = []

        conventions_content = (
            "# Archon Engineering & Architecture Conventions\n\n"
            "## Epistemic Rigor\n"
            "- Distinguish between Observed facts, Inferences, Hypotheses, and Unknowns.\n"
            "- Never state an assumption or inference as a verified fact.\n\n"
            "## Core Invariants\n"
            "- **Simplicity**: Every layer of abstraction must justify its existence. Prefer standard library.\n"
            "- **Security Gate (Saltzer)**: Never introduce unvalidated inputs, shell execution, or plaintext secrets.\n"
            "- **Atomic Persistence**: Always use atomic write-and-replace to prevent file corruption.\n"
            "- **Evidence Verification**: Before citing benchmarks or numbers, verify the artifact exists on disk.\n\n"
            "## Verification Tools\n"
            "- Quote Verifier: `python skills/dijkstra/scripts/verify_evidence_quotes.py`\n"
            "- MCP Security: `python skills/saltzer/scripts/audit_mcp_config.py`\n"
            "- Contrast Checker: `python skills/aperture/scripts/check_contrast.py`\n"
            "- Copy Linter: `python skills/caples/scripts/analyze_copy.py`\n"
        )
        conventions_file = self.output_dir / "CONVENTIONS.md"
        atomic_write(conventions_file, conventions_content)
        generated.append(conventions_file)

        aider_conf = (
            "# Aider configuration for Archon\n"
            "read:\n"
            "  - CONVENTIONS.md\n"
        )
        conf_file = self.output_dir / ".aider.conf.yml"
        atomic_write(conf_file, aider_conf)
        generated.append(conf_file)

        return generated

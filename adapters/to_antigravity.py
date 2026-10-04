"""
Antigravity Adapter
Exports canonical skills to Google Antigravity format:
- .agents/skills/<name>/SKILL.md
- Referenced scripts and checklists
- Archon Micro-Router rule table
"""

import shutil
from pathlib import Path
from typing import List

from adapters.base import BaseAdapter
from archon.atomic import atomic_write


class AntigravityAdapter(BaseAdapter):
    """Exports skills to Google Antigravity .agents/skills/ directory."""

    def export(self) -> List[Path]:
        generated = []
        target_root = self.output_dir / ".agents" / "skills"
        target_root.mkdir(parents=True, exist_ok=True)

        skills = self.load_skills()
        for skill in skills:
            skill_dest_dir = target_root / skill.name
            skill_dest_dir.mkdir(parents=True, exist_ok=True)

            # Copy SKILL.md
            dest_skill_file = skill_dest_dir / "SKILL.md"
            atomic_write(dest_skill_file, skill.raw_content)
            generated.append(dest_skill_file)

            # Copy subdirectories (references, scripts, assets)
            for sub in ["references", "scripts", "assets"]:
                src_sub = skill.directory / sub
                if src_sub.exists() and src_sub.is_dir():
                    dest_sub = skill_dest_dir / sub
                    dest_sub.mkdir(parents=True, exist_ok=True)
                    for item in src_sub.iterdir():
                        if item.is_file():
                            d_file = dest_sub / item.name
                            shutil.copy2(item, d_file)
                            generated.append(d_file)

        # Write router table reference
        router_file = target_root / "ARCHON_ROUTER.md"
        router_content = (
            "# ARCHON MICRO-ROUTER FOR ANTIGRAVITY\n\n"
            "| Situation / Domain | Advisor | Skill Path | Mode / Directive |\n"
            "|---|---|---|---|\n"
            "| Strategic dilemma, high-stakes choice, accountability | Seneca | `.agents/skills/seneca/SKILL.md` | Type 1 vs Type 2 choices |\n"
            "| Codebase review, architecture, refactoring, PR | Dijkstra | `.agents/skills/dijkstra/SKILL.md` | Structural simplicity & fitness |\n"
            "| Security review, auth, API security, release gate | Saltzer | `.agents/skills/saltzer/SKILL.md` | Advisory Mode (Release Veto) |\n"
            "| Full comprehensive audit, pen-test, repo vulnerability hunt | Saltzer | `.agents/skills/saltzer/SKILL.md` | Full Audit Harness Mode (6-Phase) |\n"
            "| UI/UX design, visual hierarchy, contrast, design systems | Aperture | `.agents/skills/aperture/SKILL.md` | Linear/Stripe craft standard |\n"
            "| Landing page copy, headlines, messaging, positioning | Caples | `.agents/skills/caples/SKILL.md` | Specificity over hype |\n"
            "| Growth, developer reputation, technical articles, posts | Orwell | `.agents/skills/orwell/SKILL.md` | Compounding developer credibility |\n"
            "| SEO, GEO, AEO, dual-retrieval blog posts, Pastebase | Berners | `.agents/skills/berners/SKILL.md` | Sound human, look machine-parsable |\n"
            "| Autonomous debate across all 6 disciplines | Council | `.agents/skills/council/SKILL.md` | Consensus & Disagreements Matrix |\n"
        )
        atomic_write(router_file, router_content)
        generated.append(router_file)

        return generated

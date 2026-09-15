"""
Claude Code Adapter
Exports canonical skills to Claude Code format:
- .claude/skills/<name>/SKILL.md
- .claude-plugin/plugin.json
"""

import shutil
from pathlib import Path
from typing import List

from adapters.base import BaseAdapter
from archon.atomic import atomic_write, atomic_write_json


class ClaudeCodeAdapter(BaseAdapter):
    """Exports skills to Claude Code .claude/skills/ and plugin manifests."""

    def export(self) -> List[Path]:
        generated = []
        claude_skills_dir = self.output_dir / ".claude" / "skills"
        claude_skills_dir.mkdir(parents=True, exist_ok=True)
        plugin_dir = self.output_dir / ".claude-plugin"
        plugin_dir.mkdir(parents=True, exist_ok=True)

        skills = self.load_skills()
        skill_manifests = []

        for skill in skills:
            target_skill_dir = claude_skills_dir / skill.name
            target_skill_dir.mkdir(parents=True, exist_ok=True)

            # Copy or write SKILL.md
            dest_skill_file = target_skill_dir / "SKILL.md"
            atomic_write(dest_skill_file, skill.raw_content)
            generated.append(dest_skill_file)

            # Copy references, scripts, and assets if present
            for sub in ["references", "scripts", "assets"]:
                src_sub = skill.directory / sub
                if src_sub.exists() and src_sub.is_dir():
                    dest_sub = target_skill_dir / sub
                    dest_sub.mkdir(parents=True, exist_ok=True)
                    for item in src_sub.iterdir():
                        if item.is_file():
                            d_file = dest_sub / item.name
                            shutil.copy2(item, d_file)
                            generated.append(d_file)

            skill_manifests.append({
                "name": skill.name,
                "description": skill.description,
                "path": f".claude/skills/{skill.name}/SKILL.md",
            })

        # Generate plugin.json
        plugin_manifest = {
            "name": "archon-skills",
            "version": "0.1.0",
            "description": "Archon Universal Expert Skill Suite & Epistemic Memory Engine",
            "skills": skill_manifests,
        }
        plugin_file = plugin_dir / "plugin.json"
        atomic_write_json(plugin_file, plugin_manifest)
        generated.append(plugin_file)

        return generated

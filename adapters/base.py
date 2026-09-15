"""
Archon Base Adapter
Defines the standard interface and common file loading/parsing utilities
for exporting skills to specific AI coding assistants.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional

from archon.paths import normalize_path
from archon.validator import parse_frontmatter


class SkillPackage:
    """Represents a canonical skill directory with SKILL.md, references, and scripts."""

    def __init__(self, directory: Path):
        self.directory = normalize_path(directory)
        self.skill_file = self.directory / "SKILL.md"
        self.raw_content = ""
        self.frontmatter: Dict[str, str] = {}
        self.body: str = ""
        self.name: str = self.directory.name
        self.description: str = ""

        if self.skill_file.exists():
            self.raw_content = self.skill_file.read_text(encoding="utf-8", errors="ignore")
            fm = parse_frontmatter(self.raw_content)
            if fm:
                self.frontmatter = fm
                self.name = fm.get("name", self.name)
                self.description = fm.get("description", "")
                # Extract body after frontmatter
                parts = self.raw_content.split("---", 2)
                if len(parts) >= 3:
                    self.body = parts[2].strip()
                else:
                    self.body = self.raw_content
            else:
                self.body = self.raw_content


class BaseAdapter(ABC):
    """Abstract base class for all AI coding agent adapters."""

    def __init__(self, skills_dir: Path, output_dir: Path):
        self.skills_dir = normalize_path(skills_dir)
        self.output_dir = normalize_path(output_dir)

    def load_skills(self) -> List[SkillPackage]:
        """Load all skills found in the skills directory."""
        packages = []
        if not self.skills_dir.exists():
            return packages

        for child in sorted(self.skills_dir.iterdir()):
            if child.is_dir() and (child / "SKILL.md").exists():
                packages.append(SkillPackage(child))
        return packages

    @abstractmethod
    def export(self) -> List[Path]:
        """
        Generate agent-specific configuration and skill files.
        Returns list of generated file paths.
        """
        pass

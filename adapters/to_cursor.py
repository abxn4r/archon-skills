"""
Cursor Rules Adapter
Exports canonical skills to Cursor rules (.cursor/rules/*.mdc).
Configures strictly scoped file globs and 'alwaysApply: false' to ensure zero idle token overhead.
"""

from pathlib import Path
from typing import List

from adapters.base import BaseAdapter
from archon.atomic import atomic_write


CURSOR_GLOBS = {
    "aperture": "**/*.{tsx,jsx,css,scss,html,vue,svelte,svg}",
    "saltzer": "**/auth/**, **/*.env*, **/*.config.*, **/security/**, **/api/**",
    "dijkstra": "**/*.{py,ts,js,go,rs,java,c,cpp,cs,rb,php}",
    "caples": "**/*.{md,mdx,html,txt,json}",
    "orwell": "**/*.{md,mdx,txt}",
    "seneca": "**/*",
    "council": "**/*",
}


class CursorAdapter(BaseAdapter):
    """Exports skills to Cursor .cursor/rules/*.mdc format."""

    def export(self) -> List[Path]:
        generated = []
        rules_dir = self.output_dir / ".cursor" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)

        skills = self.load_skills()
        for skill in skills:
            name = skill.name
            globs = CURSOR_GLOBS.get(name, "**/*")
            desc = skill.description or f"Archon {name.capitalize()} expert skill"

            mdc_content = (
                f"---\n"
                f"description: \"{desc}\"\n"
                f"globs: \"{globs}\"\n"
                f"alwaysApply: false\n"
                f"---\n\n"
                f"{skill.body}\n"
            )

            target_file = rules_dir / f"{name}.mdc"
            atomic_write(target_file, mdc_content)
            generated.append(target_file)

        return generated

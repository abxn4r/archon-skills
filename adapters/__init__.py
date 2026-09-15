"""
Archon Cross-Agent Adapters
Exports canonical Archon skills to Cursor, Claude Code, Windsurf, GitHub Copilot,
Cline, Roo Code, Aider, and Google Antigravity.
"""

from pathlib import Path
from typing import Dict, List, Type

from archon.paths import normalize_path
from adapters.base import BaseAdapter
from adapters.to_cursor import CursorAdapter
from adapters.to_claude_code import ClaudeCodeAdapter
from adapters.to_windsurf import WindsurfAdapter
from adapters.to_copilot import CopilotAdapter
from adapters.to_cline import ClineAdapter
from adapters.to_aider import AiderAdapter
from adapters.to_antigravity import AntigravityAdapter


ADAPTER_MAP: Dict[str, Type[BaseAdapter]] = {
    "cursor": CursorAdapter,
    "claude_code": ClaudeCodeAdapter,
    "claude": ClaudeCodeAdapter,
    "windsurf": WindsurfAdapter,
    "copilot": CopilotAdapter,
    "cline": ClineAdapter,
    "roo_code": ClineAdapter,
    "aider": AiderAdapter,
    "antigravity": AntigravityAdapter,
}


def run_export(
    target: str = "all",
    skills_dir: Path = Path("./skills"),
    output_dir: Path = Path("."),
) -> List[Path]:
    """
    Run the export process for target adapter(s).
    target can be an agent name or 'all'.
    """
    s_dir = normalize_path(skills_dir)
    o_dir = normalize_path(output_dir)

    target_key = (target or "all").lower().strip()
    generated_files: List[Path] = []

    if target_key == "all":
        adapters_to_run = [
            CursorAdapter,
            ClaudeCodeAdapter,
            WindsurfAdapter,
            CopilotAdapter,
            ClineAdapter,
            AiderAdapter,
            AntigravityAdapter,
        ]
        for adapter_cls in adapters_to_run:
            adapter = adapter_cls(skills_dir=s_dir, output_dir=o_dir)
            files = adapter.export()
            generated_files.extend(files)
    else:
        adapter_cls = ADAPTER_MAP.get(target_key)
        if not adapter_cls:
            raise ValueError(
                f"Unknown export target '{target}'. Available targets: {', '.join(sorted(ADAPTER_MAP.keys()))}, all"
            )
        adapter = adapter_cls(skills_dir=s_dir, output_dir=o_dir)
        files = adapter.export()
        generated_files.extend(files)

    return generated_files


__all__ = [
    "BaseAdapter",
    "CursorAdapter",
    "ClaudeCodeAdapter",
    "WindsurfAdapter",
    "CopilotAdapter",
    "ClineAdapter",
    "AiderAdapter",
    "AntigravityAdapter",
    "run_export",
    "ADAPTER_MAP",
]

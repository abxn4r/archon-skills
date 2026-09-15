"""
Archon Agent Auto-Detector
Discovers installed AI coding assistants and environments on the host machine
(Cursor, Claude Code, Windsurf, GitHub Copilot, Cline, Roo Code, Aider, Antigravity).
Enables zero-friction, one-command configuration.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Any


AGENT_DEFINITIONS = {
    "cursor": {
        "name": "Cursor",
        "binary": "cursor",
        "home_dirs": [".cursor"],
        "appdata_subdirs": ["Cursor", "cursor"],
        "target_desc": ".cursor/rules/*.mdc",
        "adapter": "cursor",
    },
    "claude_code": {
        "name": "Claude Code",
        "binary": "claude",
        "home_dirs": [".claude", ".claude-plugin"],
        "appdata_subdirs": [],
        "target_desc": ".claude/skills/ & .claude-plugin/",
        "adapter": "claude_code",
    },
    "windsurf": {
        "name": "Windsurf",
        "binary": "windsurf",
        "home_dirs": [".windsurf", ".codeium"],
        "appdata_subdirs": ["Windsurf", "windsurf"],
        "target_desc": ".windsurfrules & Cascade workflows",
        "adapter": "windsurf",
    },
    "copilot": {
        "name": "GitHub Copilot",
        "binary": "gh",
        "home_dirs": [".copilot"],
        "appdata_subdirs": ["github-copilot"],
        "target_desc": ".github/copilot-instructions.md",
        "adapter": "copilot",
    },
    "cline": {
        "name": "Cline",
        "binary": "",
        "home_dirs": [".cline"],
        "appdata_subdirs": ["Code/User/globalStorage/saoudrizwan.claude-dev"],
        "target_desc": ".clinerules",
        "adapter": "cline",
    },
    "roo_code": {
        "name": "Roo Code",
        "binary": "",
        "home_dirs": [".roo-code"],
        "appdata_subdirs": ["Code/User/globalStorage/rooveterinaryinc.roo-cline"],
        "target_desc": ".roomodes & .clinerules",
        "adapter": "cline",
    },
    "aider": {
        "name": "Aider",
        "binary": "aider",
        "home_dirs": [".aider.conf.yml"],
        "appdata_subdirs": [],
        "target_desc": ".aider.conf.yml & CONVENTIONS.md",
        "adapter": "aider",
    },
    "antigravity": {
        "name": "Antigravity",
        "binary": "antigravity",
        "home_dirs": [".gemini/antigravity", ".gemini/config/skills"],
        "appdata_subdirs": [],
        "target_desc": ".agents/skills/",
        "adapter": "antigravity",
    },
}


def detect_installed_agents() -> List[Dict[str, Any]]:
    """
    Inspect the local system to identify which AI coding assistants are present.
    Returns a list of dicts describing installed agents.
    """
    home = Path.home()
    appdata = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
    localappdata = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))

    detected = []

    for agent_id, meta in AGENT_DEFINITIONS.items():
        found = False
        evidence = []

        # 1. Check binary on PATH
        binary = meta.get("binary")
        if binary and shutil.which(binary):
            found = True
            evidence.append(f"Executable '{binary}' found on system PATH")

        # 2. Check home directory markers
        for h_sub in meta.get("home_dirs", []):
            target = home / h_sub
            if target.exists():
                found = True
                evidence.append(f"Directory or config found at ~/{h_sub}")
                break

        # 3. Check AppData markers on Windows
        if sys.platform == "win32":
            for app_sub in meta.get("appdata_subdirs", []):
                p1 = appdata / app_sub
                p2 = localappdata / app_sub
                if p1.exists() or p2.exists():
                    found = True
                    evidence.append(f"AppData configuration found for {meta['name']}")
                    break

        # Special check: If repository already contains config files for this agent
        cwd = Path.cwd()
        if agent_id == "cursor" and (cwd / ".cursor").exists():
            found = True
            evidence.append("Local .cursor directory exists in repository")
        elif agent_id == "claude_code" and (cwd / ".claude").exists():
            found = True
            evidence.append("Local .claude directory exists in repository")
        elif agent_id == "windsurf" and (cwd / ".windsurfrules").exists():
            found = True
            evidence.append("Local .windsurfrules exists in repository")
        elif agent_id == "copilot" and (cwd / ".github" / "copilot-instructions.md").exists():
            found = True
            evidence.append("Local copilot-instructions.md exists in repository")

        if found:
            detected.append({
                "id": agent_id,
                "name": meta["name"],
                "adapter": meta["adapter"],
                "target_desc": meta["target_desc"],
                "evidence": evidence,
            })

    return detected

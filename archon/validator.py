"""
Archon Skill Specification & Portability Validator
Validates skills against the open agentskills.io standard:
- YAML frontmatter presence (name, description)
- Strict 500-line portability budget per SKILL.md
- Epistemological evidence policy adherence (Observed, Inference, Hypothesis, Unknown)
- Reference and empirical script existence on disk
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from archon.paths import normalize_path


MAX_SKILL_LINES = 500
REQUIRED_EVIDENCE_TERMS = ["observed", "inference", "hypothesis", "unknown"]


def parse_frontmatter(content: str) -> Optional[Dict[str, str]]:
    """Extract simple YAML frontmatter between leading --- delimiters."""
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    front_text = parts[1]
    metadata = {}
    current_key = None
    current_val = []

    for line in front_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" in line and not line.startswith("-") and not line.startswith(">"):
            if current_key:
                metadata[current_key] = " ".join(current_val).strip()
            k, v = line.split(":", 1)
            current_key = k.strip()
            v_clean = v.strip().lstrip(">-").strip()
            current_val = [v_clean] if v_clean else []
        elif current_key:
            current_val.append(line)

    if current_key:
        metadata[current_key] = " ".join(current_val).strip()

    return metadata


def validate_skill(skill_dir: Union[str, Path]) -> Dict[str, Any]:
    """
    Validate a single skill directory containing SKILL.md.
    """
    dir_path = normalize_path(skill_dir)
    skill_file = dir_path / "SKILL.md"

    errors = []
    warnings = []

    if not skill_file.exists():
        return {
            "name": dir_path.name,
            "path": str(dir_path),
            "valid": False,
            "line_count": 0,
            "errors": [f"Missing SKILL.md in {dir_path}"],
            "warnings": [],
        }

    try:
        content = skill_file.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {
            "name": dir_path.name,
            "path": str(dir_path),
            "valid": False,
            "line_count": 0,
            "errors": [f"Failed to read SKILL.md: {e}"],
            "warnings": [],
        }

    lines = content.splitlines()
    line_count = len(lines)

    # 1. 500-line budget check
    if line_count > MAX_SKILL_LINES:
        errors.append(
            f"SKILL.md exceeds 500-line portability budget ({line_count} lines > {MAX_SKILL_LINES} lines max). "
            f"Modularize detailed checklists into references/ directory."
        )

    # 2. Frontmatter check
    fm = parse_frontmatter(content)
    if not fm:
        errors.append("Missing or malformed YAML frontmatter (must start with '---').")
    else:
        if not fm.get("name"):
            errors.append("Frontmatter missing required 'name' attribute.")
        elif not re.match(r"^[a-zA-Z0-9_-]+$", fm["name"]):
            warnings.append(f"Frontmatter name '{fm['name']}' contains non-standard characters.")

        if not fm.get("description"):
            errors.append("Frontmatter missing required 'description' attribute.")
        elif len(fm["description"]) < 20:
            warnings.append("Description is very brief; should clearly specify when to invoke the skill.")

    # 3. Evidence policy check
    content_lower = content.lower()
    missing_evidence = [term for term in REQUIRED_EVIDENCE_TERMS if term not in content_lower]
    if missing_evidence:
        # Check if "fact" is used instead of "observed"
        if "observed" in missing_evidence and "fact" in content_lower:
            missing_evidence.remove("observed")
        if missing_evidence:
            warnings.append(
                f"Evidence policy missing standard epistemic tiers: {', '.join(missing_evidence)}"
            )

    # 4. Check referenced files exist
    for match in re.finditer(r"(?:references|scripts|assets)/[a-zA-Z0-9_.-]+", content):
        ref_rel = match.group(0)
        ref_full = dir_path / ref_rel
        if not ref_full.exists():
            warnings.append(f"Referenced asset does not exist on disk: {ref_rel}")

    is_valid = len(errors) == 0

    return {
        "name": fm.get("name", dir_path.name) if fm else dir_path.name,
        "path": str(dir_path),
        "valid": is_valid,
        "line_count": line_count,
        "errors": errors,
        "warnings": warnings,
    }


def validate_all_skills(skills_root: Union[str, Path]) -> Dict[str, Any]:
    """
    Validate all skills in a parent directory.
    """
    root = normalize_path(skills_root)
    results = []
    total_valid = 0
    total_skills = 0

    if root.is_file() and root.name == "SKILL.md":
        res = validate_skill(root.parent)
        results.append(res)
        return {
            "total": 1,
            "valid_count": 1 if res["valid"] else 0,
            "skills": results,
        }

    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "SKILL.md").exists():
            total_skills += 1
            res = validate_skill(child)
            if res["valid"]:
                total_valid += 1
            results.append(res)

    return {
        "total": total_skills,
        "valid_count": total_valid,
        "all_passed": total_valid == total_skills and total_skills > 0,
        "skills": results,
    }

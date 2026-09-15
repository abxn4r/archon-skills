"""
Archon Dual-Scope Institutional Memory Engine
Zero-dependency Python standard library implementation with cross-platform
file locking (msvcrt / fcntl) and atomic persistence.

Scopes:
- Local Scope: Repository-level (.archon/) committed into Git for team alignment
  (MADR reviews, tracked security debt, copy experiments).
- Global Scope: User-level (~/.archon/) private to developer
  (Founder profile, cognitive tendencies, cross-project learnings).
"""

import os
import sys
import json
import re
import uuid
from pathlib import Path
from datetime import datetime, timezone, date
from collections import Counter
from typing import Any, Dict, List, Optional, Union, Tuple

from archon.paths import (
    normalize_path,
    safe_relative_to,
    get_repo_root,
    get_local_archon_dir,
    get_global_archon_dir,
    resolve_scope_dirs,
)
from archon.lock import file_lock
from archon.atomic import atomic_write, atomic_write_json, atomic_append_jsonl

VALID_ADVISORS = ("seneca", "dijkstra", "saltzer", "aperture", "caples", "orwell", "council", "global")


def parse_tags(tags_input: Optional[Union[str, List[str]]]) -> List[str]:
    """Normalize tags input to a sorted unique list of clean strings."""
    if not tags_input:
        return []
    if isinstance(tags_input, list):
        raw_list = tags_input
    else:
        raw_list = str(tags_input).split(",")

    tags = []
    for t in raw_list:
        clean = str(t).strip().strip("[]\"'")
        if clean:
            tags.append(clean.lower())
    return sorted(list(set(tags)))


def estimate_tokens(text: str) -> int:
    """
    Standard fast token estimation:
    Roughly 1 token per 3.8 characters or 0.75 words.
    """
    if not text:
        return 0
    words = len(text.split())
    chars = len(text)
    return max(1, int(round((words * 1.3 + chars / 3.8) / 2)))


def ensure_scope_structure(scope_dir: Path) -> None:
    """Create directory structure for all advisors within the scope directory."""
    for adv in VALID_ADVISORS:
        (scope_dir / adv).mkdir(parents=True, exist_ok=True)


def init_scopes(
    scope: str = "all",
    repo_root: Optional[Union[str, Path]] = None,
) -> Dict[str, Path]:
    """
    Initialize directory structure for local, global, or all scopes.
    Returns map of {scope_name: scope_dir_path}.
    """
    result = {}
    scope_lower = (scope or "all").lower()

    if scope_lower in ("global", "all"):
        g_dir = get_global_archon_dir()
        ensure_scope_structure(g_dir)
        # Create default profile template if missing
        prof_file = g_dir / "seneca" / "user_profile.md"
        if not prof_file.exists():
            default_profile = (
                "# FOUNDER COGNITIVE PROFILE & SECOND BRAIN\n"
                "*Maintained by Seneca Advisor*\n\n"
                "## 1. COGNITIVE PATTERNS\n"
                "- Bias towards action; check for refinement as avoidance.\n"
                "- High leverage focus: avoid premature optimization.\n\n"
                "## 2. REVERSIBILITY PROTOCOL\n"
                "- Fast velocity on Type 2 decisions (two-way doors).\n"
                "- Deliberate cool-off on Type 1 decisions (one-way doors).\n\n"
                "## 3. EVOLUTION & OBSERVATION LOG\n"
            )
            atomic_write(prof_file, default_profile)
        result["global"] = g_dir

    if scope_lower in ("local", "all"):
        l_dir = get_local_archon_dir(repo_root)
        if l_dir is not None:
            ensure_scope_structure(l_dir)
            result["local"] = l_dir

    return result


def determine_target_file(
    advisor: str,
    record_type: str,
    scope: str = "auto",
    repo_root: Optional[Union[str, Path]] = None,
) -> Tuple[Path, str]:
    """
    Resolve target file path and effective scope name ('local' or 'global').
    """
    adv = advisor.strip().lower()
    rec_type = record_type.strip().lower()
    local_dir = get_local_archon_dir(repo_root)
    global_dir = get_global_archon_dir()

    # Determine desired scope
    effective_scope = "global"
    if scope == "local":
        if local_dir is None:
            raise ValueError(
                "Local scope explicitly requested, but no repository root found."
            )
        effective_scope = "local"
    elif scope == "global":
        effective_scope = "global"
    else:
        # Auto-routing based on record type
        if rec_type in ("learning", "profile") or adv == "global":
            effective_scope = "global"
        elif local_dir is not None:
            effective_scope = "local"
        else:
            effective_scope = "global"

    base_dir = local_dir if (effective_scope == "local" and local_dir is not None) else global_dir
    ensure_scope_structure(base_dir)

    # Filename mappings (all append-only .jsonl for consistency & concurrency)
    if adv == "seneca" and rec_type == "decision":
        target = base_dir / "seneca" / "decisions.jsonl"
    elif adv == "dijkstra" and rec_type == "review":
        target = base_dir / "dijkstra" / "reviews.jsonl"
    elif adv == "saltzer" and rec_type in ("security_debt", "debt", "risk"):
        target = base_dir / "saltzer" / "security_debt.jsonl"
    elif adv == "caples" and rec_type in ("copy", "copy_experiment", "experiment"):
        target = base_dir / "caples" / "copy_experiments.jsonl"
    elif adv == "orwell" and rec_type in ("post", "playbook"):
        target = base_dir / "orwell" / "playbook.jsonl"
    elif rec_type == "learning" or adv == "global":
        filename = "local_learnings.jsonl" if effective_scope == "local" else "global_learnings.jsonl"
        target = base_dir / filename
    else:
        target = base_dir / adv / f"{rec_type}s.jsonl"

    return target, effective_scope


def record(
    advisor: str,
    record_type: str,
    data: Union[str, Dict[str, Any], List[Any]],
    tags: Optional[Union[str, List[str]]] = None,
    scope: str = "auto",
    repo_root: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """
    Record an entry into persistent memory with atomic file locking.
    """
    adv = advisor.strip().lower()
    rec_type = record_type.strip().lower()
    tag_list = parse_tags(tags)

    parsed_data: Any
    if isinstance(data, (dict, list)):
        parsed_data = data
    else:
        raw_str = str(data).strip()
        try:
            parsed_data = json.loads(raw_str)
        except Exception:
            parsed_data = {"content": raw_str}

    rec_id = f"{adv[:3]}_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    entry = {
        "id": rec_id,
        "timestamp": now_iso,
        "advisor": adv,
        "type": rec_type,
        "tags": tag_list,
        "data": parsed_data,
    }

    target_file, eff_scope = determine_target_file(adv, rec_type, scope=scope, repo_root=repo_root)
    atomic_append_jsonl(target_file, entry)

    entry["_target_file"] = str(target_file)
    entry["_scope"] = eff_scope
    return entry


def learn(
    advisor: str,
    lesson: str,
    tags: Optional[Union[str, List[str]]] = None,
    scope: str = "auto",
    repo_root: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """
    Log a validated insight, cognitive observation, or user preference.
    """
    res = record(
        advisor=advisor,
        record_type="learning",
        data={"lesson": lesson.strip()},
        tags=tags,
        scope=scope,
        repo_root=repo_root,
    )

    adv = advisor.strip().lower()
    tag_list = parse_tags(tags)
    # If Seneca logs an insight with cognitive/profile tag, append to global user_profile.md
    if adv == "seneca" and any(t in ("cognitive_model", "profile", "founder", "bias") for t in tag_list):
        try:
            profile_file = get_global_archon_dir() / "seneca" / "user_profile.md"
            if profile_file.exists():
                today_str = date.today().isoformat()
                entry_line = f"- **{today_str}** [{res['id']}]: {lesson.strip()}\n"
                with file_lock(profile_file):
                    current_content = profile_file.read_text(encoding="utf-8")
                    if "## 3. EVOLUTION & OBSERVATION LOG" in current_content:
                        profile_file.write_text(current_content.rstrip() + f"\n{entry_line}", encoding="utf-8")
        except Exception:
            pass

    return res


def profile(advisor: str = "seneca") -> str:
    """Read and return the user cognitive profile / second brain text."""
    global_root = get_global_archon_dir()
    adv = advisor.strip().lower()
    target = global_root / adv / "user_profile.md"
    if not target.exists():
        fallback = global_root / "seneca" / "user_profile.md"
        if fallback.exists():
            target = fallback
        else:
            return f"No user profile found for advisor '{adv}' at {target}."
    return target.read_text(encoding="utf-8")


def _extract_text(obj: Any) -> str:
    """Recursively stringify JSON objects for full-text search."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        parts = []
        for k, v in obj.items():
            parts.append(str(k))
            parts.append(_extract_text(v))
        return " ".join(parts)
    if isinstance(obj, (list, tuple, set)):
        return " ".join(_extract_text(v) for v in obj)
    return str(obj)


def query(
    text: str,
    advisor: Optional[str] = None,
    scope: str = "all",
    limit: int = 10,
    max_tokens: Optional[int] = None,
    repo_root: Optional[Union[str, Path]] = None,
    after_date: Optional[str] = None,
    before_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search dual-scope memory with relevance scoring and token budget ceiling.
    """
    scopes = resolve_scope_dirs(scope=scope, repo_root=repo_root)
    tokens = [t.lower() for t in re.findall(r"\w+", text) if len(t) > 1]
    query_lower = text.lower().strip()
    target_adv = advisor.strip().lower() if advisor else None
    is_wildcard = query_lower in ("", "*")

    results: List[Dict[str, Any]] = []

    for scope_name, scope_dir in scopes:
        if not scope_dir.exists():
            continue

        for file_path in scope_dir.glob("**/*"):
            if (
                file_path.is_dir()
                or file_path.name.endswith(".py")
                or file_path.name.endswith(".pyc")
                or file_path.name.endswith(".lock")
                or file_path.name.startswith(".")
                or "__pycache__" in file_path.parts
            ):
                continue

            # Process JSONL files
            if file_path.suffix == ".jsonl":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line_no, line in enumerate(f, 1):
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                item = json.loads(line)
                            except Exception:
                                continue
                            if not isinstance(item, dict):
                                continue

                            # Date range filter
                            ts = item.get("timestamp", "")
                            if after_date and ts and ts[:10] < after_date:
                                continue
                            if before_date and ts and ts[:10] > before_date:
                                continue

                            item_adv = str(item.get("advisor", "")).lower()
                            if target_adv and item_adv and item_adv != target_adv and item_adv != "global":
                                continue

                            searchable = _extract_text(item).lower()
                            score = 0
                            matched = False

                            if is_wildcard:
                                score = 1
                                matched = True
                            else:
                                if query_lower and query_lower in searchable:
                                    score += 10
                                    matched = True
                                for tok in tokens:
                                    cnt = searchable.count(tok)
                                    if cnt > 0:
                                        score += 2 + min(cnt, 5)
                                        matched = True

                                item_tags = [str(t).lower() for t in item.get("tags", [])]
                                for tok in tokens:
                                    if tok in item_tags or any(tok in t for t in item_tags):
                                        score += 4
                                        matched = True

                            if matched:
                                if target_adv and item_adv == target_adv:
                                    score += 3
                                results.append({
                                    "score": score,
                                    "scope": scope_name,
                                    "source": safe_relative_to(file_path, scope_dir),
                                    "line": line_no,
                                    "entry": item,
                                })
                except Exception:
                    continue

            # Process JSON files
            elif file_path.suffix == ".json":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        items = data if isinstance(data, list) else [data]
                        for idx, item in enumerate(items):
                            if not isinstance(item, dict):
                                continue

                            item_adv = str(item.get("advisor", "")).lower()
                            if target_adv and item_adv and item_adv != target_adv and item_adv != "global":
                                continue

                            searchable = _extract_text(item).lower()
                            score = 0
                            matched = False

                            if is_wildcard:
                                score = 1
                                matched = True
                            else:
                                if query_lower and query_lower in searchable:
                                    score += 10
                                    matched = True
                                for tok in tokens:
                                    cnt = searchable.count(tok)
                                    if cnt > 0:
                                        score += 2 + min(cnt, 5)
                                        matched = True

                            if matched:
                                if target_adv and item_adv == target_adv:
                                    score += 3
                                results.append({
                                    "score": score,
                                    "scope": scope_name,
                                    "source": f"{safe_relative_to(file_path, scope_dir)}[{idx}]",
                                    "line": idx + 1,
                                    "entry": item,
                                })
                except Exception:
                    continue

    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:limit]

    # Apply token budget ceiling if max_tokens is provided
    if max_tokens is not None and max_tokens > 0:
        budget_results = []
        accumulated_tokens = 0
        for r in results:
            entry_str = json.dumps(r["entry"], ensure_ascii=False)
            t_count = estimate_tokens(entry_str)
            if accumulated_tokens + t_count > max_tokens and budget_results:
                break
            budget_results.append(r)
            accumulated_tokens += t_count
        return budget_results

    return results


def debt(
    scope: str = "all",
    repo_root: Optional[Union[str, Path]] = None,
    include_resolved: bool = False,
) -> List[Dict[str, Any]]:
    """
    List tracked security debt entries from Saltzer with expiry & status.
    """
    scopes = resolve_scope_dirs(scope=scope, repo_root=repo_root)
    today_str = date.today().isoformat()
    debts = []

    for scope_name, scope_dir in scopes:
        debt_file = scope_dir / "saltzer" / "security_debt.jsonl"
        legacy_debt_file = scope_dir / "saltzer" / "security_debt.json"

        entries = []
        if debt_file.exists():
            try:
                with open(debt_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            entries.append(json.loads(line))
            except Exception:
                pass
        elif legacy_debt_file.exists():
            try:
                with open(legacy_debt_file, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    entries = d if isinstance(d, list) else [d]
            except Exception:
                pass

        for item in entries:
            if not isinstance(item, dict):
                continue
            data_obj = item.get("data", {})
            if not isinstance(data_obj, dict):
                data_obj = {"description": str(data_obj)}

            is_resolved = bool(data_obj.get("resolved") or item.get("resolved"))
            if is_resolved and not include_resolved:
                continue

            expiry = str(data_obj.get("expiry_date") or data_obj.get("review_date") or item.get("expiry_date") or "")
            is_overdue = bool(expiry and expiry[:10] < today_str)

            debts.append({
                "id": item.get("id"),
                "scope": scope_name,
                "title": data_obj.get("title") or data_obj.get("risk") or str(data_obj.get("description", ""))[:80],
                "severity": data_obj.get("severity", "MEDIUM").upper(),
                "owner": data_obj.get("owner", "unassigned"),
                "expiry": expiry,
                "overdue": is_overdue,
                "resolved": is_resolved,
                "tags": item.get("tags", []),
                "data": data_obj,
            })

    debts.sort(key=lambda x: (x["overdue"], x["severity"] == "CRITICAL", x["expiry"]), reverse=True)
    return debts


def stats(repo_root: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Aggregate statistics across local repository scope and global user scope.
    """
    today_str = date.today().isoformat()
    all_scopes = resolve_scope_dirs(scope="all", repo_root=repo_root)

    total_records = 0
    scope_records = {}
    advisor_counts = Counter()
    type_counts = Counter()
    tag_counts = Counter()

    decisions_total = 0
    decisions_due = []
    decisions_upcoming = []

    for scope_name, scope_dir in all_scopes:
        count_for_scope = 0
        if not scope_dir.exists():
            continue

        for file_path in scope_dir.glob("**/*"):
            if (
                file_path.is_dir()
                or file_path.name.endswith(".py")
                or file_path.name.endswith(".pyc")
                or file_path.name.endswith(".lock")
                or file_path.name.startswith(".")
                or "__pycache__" in file_path.parts
            ):
                continue

            if file_path.suffix == ".jsonl":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if not line.strip():
                                continue
                            count_for_scope += 1
                            try:
                                item = json.loads(line)
                                if not isinstance(item, dict):
                                    continue
                                adv = item.get("advisor", "unassigned")
                                r_type = item.get("type", "unknown")
                                advisor_counts[adv] += 1
                                type_counts[r_type] += 1
                                for t in item.get("tags", []):
                                    tag_counts[t] += 1

                                if r_type == "decision" or "decisions" in file_path.name:
                                    decisions_total += 1
                                    d_obj = item.get("data", {})
                                    rev_date = (
                                        d_obj.get("review_date")
                                        if isinstance(d_obj, dict)
                                        else item.get("review_date")
                                    )
                                    d_desc = (
                                        (d_obj.get("decision") or d_obj.get("title") or str(d_obj)[:80])
                                        if isinstance(d_obj, dict)
                                        else str(d_obj)[:80]
                                    )
                                    if rev_date:
                                        d_info = {
                                            "id": item.get("id"),
                                            "scope": scope_name,
                                            "review_date": str(rev_date),
                                            "decision": d_desc,
                                        }
                                        if str(rev_date)[:10] <= today_str:
                                            decisions_due.append(d_info)
                                        else:
                                            decisions_upcoming.append(d_info)
                            except Exception:
                                pass
                except Exception:
                    pass

        scope_records[scope_name] = count_for_scope
        total_records += count_for_scope

    active_debts = debt(scope="all", repo_root=repo_root)

    return {
        "total_records": total_records,
        "scope_records": scope_records,
        "advisors": dict(advisor_counts),
        "types": dict(type_counts),
        "top_tags": tag_counts.most_common(12),
        "decisions": {
            "total": decisions_total,
            "due_count": len(decisions_due),
            "due": decisions_due,
            "upcoming_count": len(decisions_upcoming),
            "upcoming": decisions_upcoming,
        },
        "security_debt": {
            "total_active": len(active_debts),
            "overdue_count": sum(1 for d in active_debts if d["overdue"]),
            "critical_count": sum(1 for d in active_debts if d["severity"] == "CRITICAL"),
        },
    }

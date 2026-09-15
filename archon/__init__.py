"""
Archon: Universal Expert Skill Suite, Epistemic Rigor & Dual-Scope Memory Engine.
Zero external dependencies. Runs across all major AI coding agents.
"""

__version__ = "0.1.0"
__author__ = "Archon Contributors"
__license__ = "Apache-2.0"

from archon.paths import (
    normalize_path,
    safe_relative_to,
    get_repo_root,
    get_local_archon_dir,
    get_global_archon_dir,
)
from archon.lock import FileLock, file_lock
from archon.atomic import atomic_write, atomic_write_json
from archon.memory import record, learn, query, profile, stats, debt
from archon.council import run_council
from archon.detector import detect_installed_agents

__all__ = [
    "__version__",
    "normalize_path",
    "safe_relative_to",
    "get_repo_root",
    "get_local_archon_dir",
    "get_global_archon_dir",
    "FileLock",
    "file_lock",
    "atomic_write",
    "atomic_write_json",
    "record",
    "learn",
    "query",
    "profile",
    "stats",
    "debt",
    "run_council",
    "detect_installed_agents",
]

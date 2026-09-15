"""
Archon Path Utilities
Safe cross-platform path manipulation, Windows extended-length prefix (\\?\\) handling,
safe relativity resolution without ValueError, and dual-scope institutional memory resolution.
Zero external runtime dependencies.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Union, List, Tuple


def strip_extended_prefix(path_str: str) -> str:
    """Strip Windows \\?\\ and \\?\\UNC\\ prefixes for normal comparisons."""
    if not isinstance(path_str, str):
        path_str = str(path_str)
    if path_str.startswith("\\\\?\\UNC\\"):
        return "\\\\" + path_str[8:]
    if path_str.startswith("\\\\?\\"):
        return path_str[4:]
    return path_str


def add_extended_prefix(path_str: str) -> str:
    """Add Windows extended-length prefix (\\\\?\\) on Win32 if path is absolute and long."""
    if sys.platform != "win32":
        return path_str
    if path_str.startswith("\\\\?\\"):
        return path_str
    abs_path = os.path.abspath(path_str)
    if abs_path.startswith("\\\\"):
        return "\\\\?\\UNC\\" + abs_path[2:]
    return "\\\\?\\" + abs_path


def normalize_path(path: Union[str, Path]) -> Path:
    """
    Resolve path to an absolute, normalized Path object.
    Handles symlinks and normalizes casing where supported.
    """
    if isinstance(path, str):
        clean_str = strip_extended_prefix(path)
        p = Path(clean_str)
    else:
        p = Path(strip_extended_prefix(str(path)))

    try:
        resolved = p.resolve()
    except (OSError, RuntimeError):
        resolved = p.absolute()
    return resolved


def safe_relative_to(path: Union[str, Path], base: Union[str, Path]) -> str:
    """
    Calculate a safe relative path string using forward slashes.
    Never raises ValueError if on different drives or outside base tree;
    falls back cleanly to the normalized string.
    """
    path_norm = normalize_path(path)
    base_norm = normalize_path(base)

    p_str = strip_extended_prefix(str(path_norm))
    b_str = strip_extended_prefix(str(base_norm))

    # Check drive mismatch on Windows (e.g. C: vs D:)
    p_drive = os.path.splitdrive(p_str)[0].lower()
    b_drive = os.path.splitdrive(b_str)[0].lower()
    if p_drive != b_drive:
        return p_str.replace("\\", "/")

    try:
        rel = Path(p_str).relative_to(Path(b_str))
        return str(rel).replace("\\", "/")
    except ValueError:
        try:
            rel = os.path.relpath(p_str, b_str)
            return rel.replace("\\", "/")
        except (ValueError, OSError):
            return p_str.replace("\\", "/")


def get_repo_root(start_dir: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """
    Search upwards from start_dir for repository indicators:
    .git directory, .archon directory, pyproject.toml, or package.json.
    Returns Path or None if outside any repository.
    """
    if start_dir is None:
        current = Path.cwd()
    else:
        current = normalize_path(start_dir)
        if current.is_file():
            current = current.parent

    # Traverse upward to filesystem root
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists() or (parent / ".archon").exists():
            return parent
        if (parent / "pyproject.toml").exists() or (parent / "package.json").exists():
            return parent
    return None


def get_local_archon_dir(repo_root: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """
    Return the repository-local .archon directory path if within a repository.
    Does not automatically create it unless requested by caller.
    """
    root = get_repo_root(repo_root)
    if root is not None:
        return root / ".archon"
    return None


def get_global_archon_dir() -> Path:
    """
    Return the private user-global ~/.archon directory path.
    Can be overridden via ARCHON_GLOBAL_ROOT environment variable.
    Ensures directory exists.
    """
    env_root = os.environ.get("ARCHON_GLOBAL_ROOT")
    if env_root:
        global_path = normalize_path(env_root)
    else:
        global_path = Path.home() / ".archon"

    try:
        global_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return global_path


def resolve_scope_dirs(
    scope: str = "auto",
    repo_root: Optional[Union[str, Path]] = None
) -> List[Tuple[str, Path]]:
    """
    Resolve active directory scopes.
    Returns list of (scope_name, directory_path).
    scope can be 'local', 'global', 'all', or 'auto'.
    """
    scope = (scope or "auto").strip().lower()
    local_dir = get_local_archon_dir(repo_root)
    global_dir = get_global_archon_dir()

    if scope == "local":
        if local_dir is None:
            raise ValueError(
                "Local repository scope requested, but no repository root (.git or .archon) was found. "
                "Run 'archon init' to initialize repository scope."
            )
        return [("local", local_dir)]

    if scope == "global":
        return [("global", global_dir)]

    if scope == "all":
        scopes = []
        if local_dir is not None:
            scopes.append(("local", local_dir))
        scopes.append(("global", global_dir))
        return scopes

    # 'auto': prioritize local repo if available, otherwise global
    if local_dir is not None and local_dir.exists():
        return [("local", local_dir), ("global", global_dir)]
    elif local_dir is not None:
        return [("local", local_dir)]
    return [("global", global_dir)]

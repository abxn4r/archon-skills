"""
Archon Atomic File Replacement
Ensures zero file corruption or zero-byte reads during crashes or concurrent interrupts.
Writes to a temporary file in the identical parent directory, executes flush and fsync,
and swaps atomically via os.replace.
"""

import os
import json
import tempfile
from pathlib import Path
from typing import Any, Union

from archon.paths import normalize_path
from archon.lock import file_lock


def atomic_write(
    target_path: Union[str, Path],
    content: Union[str, bytes],
    mode: str = "w",
    encoding: str = "utf-8",
) -> Path:
    """
    Write content to target_path atomically.
    Creates a temporary file in the same directory, flushes, fsyncs,
    and replaces the destination file via os.replace.
    """
    target = normalize_path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    is_binary = "b" in mode
    actual_mode = "wb" if is_binary else "w"
    actual_encoding = None if is_binary else encoding

    # Create temporary file in the exact same directory for same-device atomic rename
    prefix = f".{target.name}.tmp-"
    tmp_file = None
    tmp_path = None

    try:
        tmp_file = tempfile.NamedTemporaryFile(
            mode=actual_mode,
            encoding=actual_encoding,
            dir=str(target.parent),
            prefix=prefix,
            delete=False,
        )
        tmp_path = Path(tmp_file.name)

        tmp_file.write(content)
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
        tmp_file.close()
        tmp_file = None

        # Atomic filesystem swap
        os.replace(str(tmp_path), str(target))
        tmp_path = None
        return target
    finally:
        if tmp_file is not None:
            try:
                tmp_file.close()
            except OSError:
                pass
        if tmp_path is not None and tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def atomic_write_json(
    target_path: Union[str, Path],
    data: Any,
    indent: int = 2,
    ensure_ascii: bool = False,
    encoding: str = "utf-8",
) -> Path:
    """Serialize data to JSON and write atomically to target_path."""
    json_str = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii) + "\n"
    return atomic_write(target_path, json_str, mode="w", encoding=encoding)


def atomic_append_jsonl(
    target_path: Union[str, Path],
    record_dict: dict,
    encoding: str = "utf-8",
) -> Path:
    """
    Safely append a single JSON entry as a line into target_path with a file lock
    and durable flush/fsync.
    """
    target = normalize_path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    line = json.dumps(record_dict, ensure_ascii=False) + "\n"

    with file_lock(target):
        with open(target, "a", encoding=encoding) as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
    return target

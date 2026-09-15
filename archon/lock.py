"""
Archon Cross-Platform File Lock
Cross-platform atomic file lock using Python standard library:
- msvcrt on Windows (LK_NBLCK with seek-zero anchoring)
- fcntl on POSIX (LOCK_EX | LOCK_NB)
Exponential backoff with jitter prevents lock convoys under concurrent agent executions.
"""

import os
import sys
import time
import random
import contextlib
from pathlib import Path
from typing import Optional, Union

from archon.paths import normalize_path


class LockTimeoutError(TimeoutError):
    """Raised when lock acquisition exceeds the timeout threshold."""
    pass


class FileLock:
    """
    Cross-platform re-entrant or isolated file lock context manager.
    Protects target files from concurrent read/write race conditions.
    """

    def __init__(
        self,
        target_path: Union[str, Path],
        timeout: float = 10.0,
        poll_interval: float = 0.02,
        lock_file_path: Optional[Union[str, Path]] = None,
    ):
        self.target_path = normalize_path(target_path)
        self.timeout = float(timeout)
        self.poll_interval = float(poll_interval)
        if lock_file_path is not None:
            self.lock_file = normalize_path(lock_file_path)
        else:
            self.lock_file = self.target_path.parent / f".{self.target_path.name}.lock"
        self._fd: Optional[int] = None

    def acquire(self) -> "FileLock":
        """Acquire the file lock within the configured timeout."""
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        start_time = time.time()
        curr_interval = self.poll_interval

        # Open lock file descriptor with read/write & create flags
        fd = os.open(str(self.lock_file), os.O_RDWR | os.O_CREAT)
        try:
            while True:
                try:
                    # Seek to byte zero before locking
                    os.lseek(fd, 0, os.SEEK_SET)

                    if sys.platform == "win32":
                        import msvcrt
                        # Lock 1 byte non-blocking
                        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        # Exclusive non-blocking lock
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

                    # Acquired successfully
                    self._fd = fd
                    return self
                except (IOError, OSError):
                    elapsed = time.time() - start_time
                    if elapsed >= self.timeout:
                        raise LockTimeoutError(
                            f"Failed to acquire lock on {self.lock_file} after {elapsed:.2f}s "
                            f"(timeout was {self.timeout}s)"
                        )

                    # Exponential backoff with jitter to reduce contention
                    jitter = random.uniform(0.5, 1.5)
                    sleep_time = min(curr_interval * jitter, 0.25)
                    time.sleep(sleep_time)
                    curr_interval = min(curr_interval * 1.5, 0.2)
        except Exception:
            try:
                os.close(fd)
            except OSError:
                pass
            raise

    def release(self) -> None:
        """Release the file lock and close the file descriptor."""
        fd = self._fd
        if fd is not None:
            self._fd = None
            try:
                os.lseek(fd, 0, os.SEEK_SET)
                if sys.platform == "win32":
                    import msvcrt
                    try:
                        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                    except OSError:
                        pass
                else:
                    import fcntl
                    try:
                        fcntl.flock(fd, fcntl.LOCK_UN)
                    except OSError:
                        pass
            finally:
                try:
                    os.close(fd)
                except OSError:
                    pass

    def __enter__(self) -> "FileLock":
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()


@contextlib.contextmanager
def file_lock(
    target_path: Union[str, Path],
    timeout: float = 10.0,
    poll_interval: float = 0.02,
    lock_file_path: Optional[Union[str, Path]] = None,
):
    """Context manager functional wrapper for FileLock."""
    lock = FileLock(
        target_path=target_path,
        timeout=timeout,
        poll_interval=poll_interval,
        lock_file_path=lock_file_path,
    )
    with lock:
        yield lock

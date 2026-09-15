"""
Tests for Archon cross-platform file locking (msvcrt / fcntl).
Verifies lock acquisition, mutual exclusion, contention handling, and timeouts.
"""

import os
import sys
import time
import tempfile
import unittest
import threading
from pathlib import Path

from archon.lock import FileLock, file_lock, LockTimeoutError


class TestFileLock(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.target_file = Path(self.temp_dir.name) / "test_data.jsonl"
        self.target_file.touch()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_basic_acquire_and_release(self):
        """Test basic lock acquire and release within context manager."""
        lock = FileLock(self.target_file, timeout=2.0)
        with lock:
            self.assertTrue(lock.lock_file.exists())
            # Verify file can be written to while lock is held
            with open(self.target_file, "a") as f:
                f.write("test_line\n")

        self.assertTrue(self.target_file.exists())

    def test_reentrant_or_sequential_locks(self):
        """Test acquiring lock sequentially multiple times."""
        for _ in range(3):
            with file_lock(self.target_file, timeout=2.0):
                with open(self.target_file, "a") as f:
                    f.write("line\n")

        lines = self.target_file.read_text().splitlines()
        self.assertEqual(len(lines), 3)

    def test_threaded_contention(self):
        """Test multiple concurrent threads incrementing a shared counter under lock."""
        counter_file = Path(self.temp_dir.name) / "counter.txt"
        counter_file.write_text("0")

        def worker():
            for _ in range(10):
                with file_lock(counter_file, timeout=5.0):
                    val = int(counter_file.read_text().strip())
                    time.sleep(0.005)  # induce contention
                    counter_file.write_text(str(val + 1))

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        final_val = int(counter_file.read_text().strip())
        self.assertEqual(final_val, 40)

    def test_lock_timeout_error(self):
        """Test that a second lock times out when the first is held past timeout."""
        lock1 = FileLock(self.target_file, timeout=1.0)
        lock2 = FileLock(self.target_file, timeout=0.2)

        lock1.acquire()
        try:
            with self.assertRaises(LockTimeoutError):
                lock2.acquire()
        finally:
            lock1.release()


if __name__ == "__main__":
    unittest.main()

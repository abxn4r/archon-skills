# Archon Dual-Scope Institutional Memory Engine

Archon solves AI agent amnesia while preventing private founder reflections, stress signatures, or personal habits from leaking into team Git repositories.

---

## 1. Dual-Scope Institutional Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARCHON DUAL-SCOPE MEMORY SYSTEM                          │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. Local Repository Scope (.archon/) │ 2. User Global Scope (~/.archon/)    │
│    - Committed to Git                │    - Completely private to user      │
│    - Shared across team & agents     │    - Never committed to Git          │
│    - Architectural Decisions (MADRs) │    - Founder cognitive profile       │
│    - Tracked Security Debt (Saltzer) │    - Personal stress signatures      │
│    - Tested Copy Experiments         │    - Cross-project learnings         │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### Routing Invariants:
- **Seneca User Profile / Cognitive Model**: ALWAYS writes to global private scope `~/.archon/seneca/user_profile.md`.
- **Architectural Decision Records (MADRs)**: Default to repository scope `.archon/dijkstra/reviews.jsonl`.
- **Tracked Security Debt**: Default to repository scope `.archon/saltzer/security_debt.jsonl`.
- **Copy Experiments**: Default to repository scope `.archon/caples/copy_experiments.jsonl`.
- **Validated Learnings**: Automatically routed to local or global scope based on context or `--scope` flag.

---

## 2. Concurrency & Cross-Platform File Locking

Multi-agent swarms and concurrent processes frequently collide when writing to disk. Archon implements a robust, zero-dependency file lock:
- **Windows**: `msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)` with seek-zero anchoring.
- **macOS / Linux**: `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)`.
- **Contention Prevention**: Exponential backoff with randomized jitter prevents thundering herd lock convoys.
- **Timeout Safety**: Clean lock release via context manager (`with FileLock(path):`).

---

## 3. Atomic File Replacement (Zero-Corruption)

To eliminate corrupted files or zero-byte reads caused by process interruption or power loss:
1. Data is written to a temporary file in the **same directory** as the target.
2. The file is flushed and committed to disk with `os.fsync(f.fileno())`.
3. The file is swapped atomically using `os.replace()`, guaranteeing an atomic POSIX / Win32 rename on the same volume.

---

## 4. Append-Only JSONL Storage

All advisor records are stored as append-only `.jsonl` lines:
- **O(1) Appends**: Fast writes without loading or rewriting large JSON arrays.
- **Crash Recovery**: If an append is cut short, existing lines remain intact.
- **Git Friendly**: Each new record is a single line diff, eliminating merge conflicts.

---

## 5. CLI Usage Guide

```bash
# Query memory across all scopes with token ceiling
python -m archon.cli query "authentication" --max-tokens 250 --format tsv

# Record an architectural decision
python -m archon.cli record --advisor dijkstra --type review --data '{"decision": "Use SQLite", "status": "accepted"}'

# Log tracked security debt
python -m archon.cli record --advisor saltzer --type security_debt --data '{"title": "Weak JWT expiration", "severity": "HIGH", "owner": "sec-team", "expiry_date": "2026-10-01"}'

# View active security debts
python -m archon.cli debt

# Inspect memory statistics
python -m archon.cli stats
```

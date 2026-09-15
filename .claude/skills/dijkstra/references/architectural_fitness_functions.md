# ARCHITECTURAL FITNESS FUNCTIONS
*Automated Verification of System Design Invariants*

---

## 1. WHAT IS AN ARCHITECTURAL FITNESS FUNCTION?
*Concept introduced by Neal Ford, Rebecca Parsons, and Patrick Kua.*

An architectural fitness function provides an objective, automated metric to assess how close an architecture is to achieving certain architectural goals (security, modularity, performance, maintainability).

Unlike functional tests that verify *what* software does, fitness functions verify *how* the system behaves structurally over hundreds of commits.

---

## 2. CORE FITNESS FUNCTION CATEGORIES

### 1. Structural & Dependency Invariants
- **Layering Rule**: Inner domain entities must never import outer infrastructure (e.g. database, HTTP client, or UI drivers).
- **Cyclic Dependency Checker**: Automated detection that alerts when Package A imports Package B which imports Package A.
- **Dependency Scope**: Ensure assistant helper scripts strictly import Python Standard Library modules (no accidental `pip` dependencies).

### 2. Evidence Verification & Artifact Proof
- **Artifact-Before-Doc Rule**: No documentation or status report may cite numbers or benchmark results unless the corresponding JSON/log artifact exists on disk.
- **Substring Verifier**: Use `verify_evidence_quotes.py` to confirm quoted citations exist verbatim in source repositories.

### 3. Performance & Resource Budgets
- **CLI Startup Budget**: Local CLI tools must execute and return `--help` in < 250ms.
- **Payload Size Budget**: Configuration payloads must not exceed predefined size ceilings.

---

## 3. IMPLEMENTATION PROTOCOL
1. Define the invariant explicitly in markdown / MADR.
2. Implement a zero-dependency automated script in `scripts/`.
3. Wire into local commit or pre-push checks.

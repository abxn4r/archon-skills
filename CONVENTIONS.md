# Archon Engineering & Architecture Conventions

## Epistemic Rigor
- Distinguish between Observed facts, Inferences, Hypotheses, and Unknowns.
- Never state an assumption or inference as a verified fact.

## Core Invariants
- **Simplicity**: Every layer of abstraction must justify its existence. Prefer standard library.
- **Security Gate (Saltzer)**: Never introduce unvalidated inputs, shell execution, or plaintext secrets.
- **Atomic Persistence**: Always use atomic write-and-replace to prevent file corruption.
- **Evidence Verification**: Before citing benchmarks or numbers, verify the artifact exists on disk.

## Verification Tools
- Quote Verifier: `python skills/dijkstra/scripts/verify_evidence_quotes.py`
- MCP Security: `python skills/saltzer/scripts/audit_mcp_config.py`
- Contrast Checker: `python skills/aperture/scripts/check_contrast.py`
- Copy Linter: `python skills/caples/scripts/analyze_copy.py`

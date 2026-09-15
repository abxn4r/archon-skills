# Archon Autonomous Consensus Council

The **Archon Consensus Council** is an autonomous multi-advisor deliberation engine designed to evaluate high-stakes technology choices, architectural migrations, and irreversible decisions.

---

## 1. Why Council Mode?

In complex software projects, single-discipline reviews often create blind spots:
- An **Architect** (Dijkstra) might recommend an elegant pattern that significantly expands the **Attack Surface** (Saltzer).
- A **Security Engineer** (Saltzer) might propose restrictions that create severe **User Friction** (Aperture).
- A **Founder** (Seneca) might pursue a technical migration that represents **Refinement as Avoidance** instead of strategic leverage.

The Council breaks these silos by convening an independent inquest across all six disciplines simultaneously and producing a unified **Consensus & Disagreements Matrix** before code is committed.

---

## 2. Deliberation Protocol

When convened on a proposal (e.g., `archon council "Migrate from SQLite to PostgreSQL"`):

1. **Reversibility Classification**:
   - **Type 1 (One-Way Door)**: Irreversible or highly destructive to unwind. Requires unanimous consensus and strict pre-mortems.
   - **Type 2 (Two-Way Door)**: Reversible with low friction. Prioritizes execution velocity.

2. **The 6 Discipline Inquests**:
   - **Seneca**: Strategic leverage, opportunity cost, and pre-mortem failure mode.
   - **Dijkstra**: Simplicity test, cognitive load, and operational liability.
   - **Saltzer**: Attack surface delta, trust boundaries, and release veto evaluation.
   - **Aperture**: User friction, latency budget (<200ms), and craft consistency.
   - **Caples**: Value clarity, positioning differentiation, and elimination of marketing jargon.
   - **Orwell**: Developer community perception and open-source credibility.

3. **Consensus & Disagreements Matrix**:
   - Resolves cross-disciplinary tensions.
   - Declares binding invariants for implementation.

4. **Saltzer Release Veto Gate**:
   - If Saltzer detects a **Critical** security vulnerability in the proposal, the proposal is **VETOED — DO NOT SHIP**, overriding all other approvals.

---

## 3. CLI Execution

```bash
# Convene the Council on an architectural dilemma
python -m archon.cli council "Migrate storage from SQLite to PostgreSQL"

# Run debate without persisting to institutional memory
python -m archon.cli council "Evaluate GraphQL vs REST" --no-record
```

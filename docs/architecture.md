# Archon System Architecture & Epistemic Foundations

Archon is a zero-dependency, open-source expert skill suite and compounding institutional memory engine designed to operate natively across all major AI coding agents.

---

## 1. Zero-Dependency Standard Library Invariant

A core architectural invariant of Archon is **100% Python Standard Library implementation**. 

### Why Zero Runtime Dependencies?
- **Zero Supply-Chain Attack Surface**: Agent toolchains frequently handle sensitive source code, environment credentials, and system command interfaces. Third-party packages introduce dependency confusion, typosquatting, and unpinned upstream vulnerabilities.
- **Instant Execution Velocity**: Archon CLI executes in < 20ms without package resolution overhead or virtual environment activation requirements.
- **Cross-Platform Portability**: Runs identically on Windows (Win32 API via `msvcrt`), macOS, and Linux (POSIX via `fcntl`).
- **Zero Bitrot**: Standard library APIs are stable across decades of Python releases (Python 3.8 through 3.13+).

---

## 2. Epistemological Evidence Framework

Every Archon advisor adheres to a rigorous four-tier epistemic taxonomy:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        EPISTEMIC EVIDENCE TIERS                        │
├─────────────────┬──────────────────────────────────────────────────────┤
│ Observed / Fact │ Directly visible in code, configuration, or data.    │
├─────────────────┼──────────────────────────────────────────────────────┤
│ Inference       │ Logical deduction derived strictly from observations.│
├─────────────────┼──────────────────────────────────────────────────────┤
│ Hypothesis      │ Plausible interpretation or risk requiring validation│
├─────────────────┼──────────────────────────────────────────────────────┤
│ Unknown         │ Critical context that is missing or unverified.      │
└─────────────────┴──────────────────────────────────────────────────────┘
```

### Invariants:
1. **Never Present Inference as Fact**: An advisor must state the connecting premise of every deduction.
2. **Never Invent Absence**: If an artifact or code file is not found, verify at the exact path before claiming non-existence.
3. **Absence of Evidence ≠ Evidence of Security**: A system is not safe simply because an exploit is not immediately visible.

---

## 3. The 6 Specialist Disciplines & Council

Archon models six distinct engineering and executive disciplines that operate with full autonomy:

```
                            ┌───────────────────────────────────┐
                            │    ARCHON CONSENSUS COUNCIL       │
                            │ Multi-Discipline Debate & Matrix  │
                            └─────────────────┬─────────────────┘
                                              │
         ┌───────────────┬────────────────────┼───────────────────┬───────────────┐
         │               │                    │                   │               │
         ▼               ▼                    ▼                   ▼               ▼
┌─────────────────┐ ┌───────────────┐ ┌───────────────┐ ┌────────────────┐ ┌──────────────┐
│     Seneca      │ │   Dijkstra    │ │    Saltzer    │ │    Aperture    │ │    Caples    │
│    Strategy     │ │ Architecture  │ │Security (VETO)│ │   Design/UX    │ │Copy/Messaging│
└─────────────────┘ └───────────────┘ └───────────────┘ └────────────────┘ └──────────────┘
                                              │
                                              ▼
                                     ┌────────────────┐
                                     │     Orwell     │
                                     │Growth & Playbook│
                                     └────────────────┘
```

- **Seneca (Strategy & Second Brain)**: Reversibility (Type 1 vs Type 2), opportunity cost, cognitive bias detection (refinement as avoidance).
- **Dijkstra (Engineering Architect)**: Simplicity tests, structural layering, empirical claims reconciliation, fitness functions.
- **Saltzer (Security Engineer)**: Threat modeling, attack chains, least privilege, and binding **Release Veto Authority** (Critical = DO NOT SHIP).
- **Aperture (Design & UX Director)**: 4px/8px spatial grid, typography scale, monochromatic discipline, WCAG/APCA contrast math.
- **Caples (Copy & Messaging Director)**: Customer awareness calibration, positioning framework, headline gatekeeper, 16 AI cliché detectors.
- **Orwell (Growth & Content Director)**: 2026 platform algorithms (X, LinkedIn, Reddit, HN), compounding reputation, 8-node relational playbook.
- **Consensus Council**: Autonomous multi-advisor debate mode producing a structured Consensus & Disagreements Matrix for high-stakes proposals.

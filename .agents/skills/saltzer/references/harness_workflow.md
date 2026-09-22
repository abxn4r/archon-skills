# SALTZER FULL AUDIT HARNESS WORKFLOW
*Autonomous Multi-Agent Repository Vulnerability Discovery Engine*

---

## 1. WHEN TO ACTIVATE THE HARNESS

Saltzer operates in **Advisory Mode** by default. Activate the **Full Audit Harness** ONLY when:
- The user explicitly requests a codebase audit or penetration test (*"audit this codebase"*, *"find all vulnerabilities in ./src"*, *"do a comprehensive security review"*).
- The user requests formal audit artifacts (`findings.json`, `coverage-ledger.json`, `REPORT.md`).

For ordinary code reviews, PR reviews, architectural questions, or Council meetings, stay in **Advisory Mode**.

---

## 2. UNIVERSAL EXECUTION SAFETY & OS SANDBOXING

Source inspection is strictly read-only. Bounded local execution (running unit tests, minimal function harnesses, local fixtures, or sanitizers) is permitted ONLY inside an OS-enforced sandbox that enforces:
1. **Zero External Network**: Isolated loopback only when local server/client traffic is strictly required.
2. **Empty Allowlisted Environment**: No ambient host environment variables, inherited credentials, or authentication tokens.
3. **Read-Only Target & Toolchain**: Target files are mounted read-only.
4. **Scratch Write Isolation**: Agents write only to their designated `agents/<agent-id>/scratch/` directory.
5. **Strict Resource Bounds**: Low CPU, memory, process count, file size, and wall-clock limits.

### Artifact Promotion Discipline
Target-controlled processes must never write directly to shared report paths or retained artifacts. Only trusted parent-side code may promote allowlisted regular files from `scratch/` to `artifacts/` using race-safe, non-symlink traversal. If sandboxing is unavailable on the host, target execution is blocked and leads must remain `needs_validation`.

---

## 3. THE 6-PHASE AUDIT PIPELINE

```
Phase 1: RECONNAISSANCE ───► architecture.md + coverage-ledger.json
                                     │
Phase 2: HUNTING WAVES ◄─────────────┤
   │                                 │
   └──► Coverage Critic Review ──────┘ (Loop until clean pass or budget exhausted)
                                     │
Phase 3: ADVERSARIAL VALIDATION ─────┘ (Fresh verifier tries to REFUTE each candidate)
                                     │
Phase 4: STRUCTURED OUTPUT ──────────► findings.json + Schema Validation (.cjs)
                                     │
Phase 5: FINAL RECORD VERIFICATION ──► Fresh independent check of claims & severity
                                     │
Phase 6: REPORTING & PERSISTENCE ────► REPORT.md + Archon Security Debt Tracking
```

---

### PHASE 1: RECONNAISSANCE & COVERAGE LEDGER SETUP

Launch parallel `research` sub-agents (read-only):
- **Agent 1a (Stack & Operations)**: Map product type, tech stack, dependencies, build definitions, and offline test paths.
- **Agent 1b (Authority & Controls)**: Map principals, authentication at entry surfaces, tenant authorization, and privilege boundaries.
- **Agent 1c (Surfaces & Sinks)**: Inventory all untrusted input surfaces (HTTP, RPC, CLI, files, webhooks, model context) and dangerous sinks.
- **Agent 1d (Execution Visibility)**: Identify offline test harnesses and runtime controls.

**Outputs**:
- `architecture.md`: Max 1,000 words summarizing system trust boundaries.
- `coverage-ledger.json`: Deterministic coverage matrix composed of `(surface, boundary, subsystem, attack_class)`. Validate using:
  ```powershell
  node skills/saltzer/scripts/validate-coverage-ledger.cjs coverage-ledger.json
  ```

---

### PHASE 2: COVERAGE-LED HUNTING WAVES & COVERAGE CRITICS

1. **Assign Units**: Assign planned coverage units to isolated `general` hunter sub-agents.
2. **Hunter Prompt Structure**:
   - Give the hunter its assigned coverage units, `architecture.md`, and relevant attack class reference guides.
   - Instruct the hunter to follow inputs from entrypoint to sink, search for invariant failures, and attempt the smallest local sandboxed reproduction.
   - Return structured JSON results (`covered`, `candidate`, `blocked`, or `uncovered`).
3. **Coverage Critic Wave**:
   - After each hunter wave, launch a fresh `research` **Coverage Critic** sub-agent.
   - The critic inspects `coverage-ledger.json` against current source to detect blind spots, unmapped routes, uninspected lifecycle transitions, or unjustified closures.
   - Loop back to assign discovered units until the critic reports a clean pass.

---

### PHASE 3: INDEPENDENT ADVERSARIAL CANDIDATE VALIDATION

> [!IMPORTANT]
> **Adversarial Discipline**: The agent that validates a candidate is **never** the agent that found it.

For every proposed `confirmed` or `needs_validation` candidate, launch a fresh `general` verifier sub-agent with this core instruction:
```text
You did not write this candidate. Try to refute it from repository source and bounded local evidence.
1. Check every line, file, and scope in the claimed trace.
2. Identify the strongest source-visible control or preventing layer on the path. If an earlier layer prevents the exploit, REFUTE the finding.
3. Verify that the impact crosses a real security boundary with demonstrable harm.
4. If a required runtime or deployment fact is missing, demote to needs_validation (zero severity).
5. Return: {"decision": "confirmed|needs_validation|rejected", "record": { ... }}
```

---

### PHASE 4: STRUCTURED OUTPUT & VALIDATION

The parent orchestrator writes all finalized records to `findings.json` adhering strictly to [report-schema.json](file:///c:/Users/Abeer/Desktop/Repos/Skills/.agents/skills/saltzer/scripts/report-schema.json):
- `confirmed`: Complete verified trace, bounded local execution evidence, conditions, remediation, and severity.
- `needs_validation`: Source-grounded hypothesis blocked by missing deployment/runtime facts. **MUST NOT HAVE SEVERITY**. Includes exact blockers and a validation plan.
- `rejected`: Refuted candidate retained for audit transparency.

Validate immediately using:
```powershell
node skills/saltzer/scripts/validate-findings.cjs findings.json
```

---

### PHASE 5: INDEPENDENT FINAL RECORD VERIFICATION

Launch one fresh `research` verifier per `confirmed` and `needs_validation` finding to verify:
1. Overall severity matches demonstrated impact (Likelihood &times; Demonstrated Impact).
2. Remediation enforces the invariant at the last trusted decision point without merely shifting trust.
3. Path and line references are accurate.

---

### PHASE 6: REPORTING & ARCHON INTEGRATION

1. **Generate Human-Readable Reports**:
   - `REPORT.md`: Executive posture summary, confirmed findings table, needs-validation table, hardening opportunities, and coverage summary.
   - `FINDINGS-DETAIL.md`: In-depth reproduction steps, payloads, and smallest source fixes for confirmed findings.
   - `NEEDS-VALIDATION.md`: Exact blockers and owner-observable checks for unconfirmed leads.
2. **Institutional Security Debt Integration**:
   - Every accepted risk or unresolved security finding is recorded into Archon persistent memory:
     ```powershell
     python -m archon.cli record --advisor saltzer --type security_debt --data "<finding_json>"
     ```
   - If any `confirmed` finding is rated **Critical**, enforce the binding **Release Veto Gate**:
     ```
     RELEASE RECOMMENDATION: DO NOT SHIP
     ```

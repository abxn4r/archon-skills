<div align="center">

# ARCHON
### The Universal Expert Skill Suite & Dual-Scope Memory Engine for AI Coding Agents

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0%20(Standard%20Library)-success)](pyproject.toml)
[![Token Reduction](https://img.shields.io/badge/Token%20Reduction-88%25%20to%2094%25-brightgreen)](#the-5-layer-token-reduction-architecture)
[![Specification](https://img.shields.io/badge/Standard-agentskills.io-purple)](https://agentskills.io)

**Archon** productizes expert engineering, architecture, and executive judgment into a **zero-external-dependency, production-ready system** that runs natively across all major AI coding agents: **Cursor**, **Claude Code**, **Windsurf**, **GitHub Copilot**, **Cline / Roo Code**, **Aider**, **Google Antigravity**, and the open **`skills.sh`** registry.

</div>

---

## Why Archon?

Modern AI coding agents suffer from three catastrophic problems:
1. **AI Amnesia & Drift**: Models forget past architectural decisions, re-introduce previously rejected patterns, and repeat mistakes across sessions.
2. **Context Window Bloat**: Monolithic skill prompts consume **~35,000 tokens per turn** ($21+/day in LLM inference), degrading reasoning and crowding out actual code.
3. **Unchecked Sycophancy & Hallucinated Advice**: Models agree with unsound architectural choices, cite non-existent benchmark numbers, and lack the discipline to veto insecure code.

**Archon cures these structural flaws:**
- **Dual-Scope Memory**: Institutional memory committed into git (`.archon/`) for team alignment, paired with private user memory (`~/.archon/`) that never leaves your machine.
- **5-Layer Token Reduction**: Cuts active agent token consumption by **88% to 94.5%** via micro-router tables, on-demand activation, and token-capped queries.
- **Epistemic Rigor**: Strict classification of every assessment into *Observed Fact*, *Inference*, *Hypothesis*, or *Unknown*.
- **Autonomous Consensus Council**: Six specialist disciplines debate high-stakes technology migrations before code is committed.
- **Release Veto Authority**: If security detects a Critical vulnerability, merge is blocked: **DO NOT SHIP**.
- **Zero Runtime Dependencies**: 100% Python Standard Library. Zero pip packages. Zero supply-chain attack surface. Sub-20ms CLI execution.

---

## Quickstart (One Command)

### macOS / Linux
```bash
git clone https://github.com/archon-ai/archon-skills.git
cd archon-skills
./install.sh
```

### Windows (PowerShell)
```powershell
git clone https://github.com/archon-ai/archon-skills.git
cd archon-skills
.\install.ps1
```

### Via `skills.sh` Registry
```bash
npx skills add archon-ai/archon-skills --global
```

The installer auto-detects installed coding assistants on your machine (Cursor, Claude Code, Windsurf, Copilot, Cline, Aider, Antigravity) and configures them automatically without user friction.

---

## The 6 Specialist Advisors & Council

Archon packages six autonomous disciplines adhering to uncompromising standards:

| Specialist | Domain & Authority | Key Directive |
|---|---|---|
| **Seneca** | Strategic Advisor & Second Brain | Reversibility (Type 1 vs Type 2 doors); calls out refinement-as-avoidance. |
| **Dijkstra** | Engineering Architect | Simplicity first; verifies evidence citations exist verbatim in source code. |
| **Saltzer** | Principal Security Engineer | **RELEASE VETO GATE**: Any Critical finding blocks deployment (**DO NOT SHIP**). |
| **Aperture** | Design & UX Director | Linear/Stripe/Vercel craft standard; 4px grid; WCAG AA & APCA contrast math. |
| **Caples** | Copy & Messaging Director | Customer awareness stages; April Dunford positioning; eliminates AI clichés. |
| **Orwell** | Growth & Developer Reputation | 2026 platform distribution; technical blueprints over vanity metrics. |
| **Council** | Autonomous Consensus Council | Orchestrates multi-advisor debate producing a Consensus & Disagreements Matrix. |

---

## The 5-Layer Token Reduction Architecture

Archon slashes token consumption by over 90% using progressive disclosure:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Zero-Idle Micro-Router Table (~120 tokens total)                         │
│    Only ~120 tokens injected into idle context (vs ~35,000 for monolithic)  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. 500-Line Modular Portability Pruning                                     │
│    Core SKILL.md trimmed to 150–350 lines; deep checklists in references/   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Deterministic Script Delegation (Zero LLM Tokens)                        │
│    Mathematical & regex tasks offloaded to local standard-library tools     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Token-Budgeted Memory Retrieval (--max-tokens 250)                       │
│    Dynamic token ceiling on queries; returns compact, high-density TSV/JSONL│
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. Prompt-Cache Boundary Design                                             │
│    Immutable epistemic rules anchored at the top for 90% cache hits         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Benchmark Comparison

| Mode | Idle Context | Active Turn | Cost / 100 Turns (Claude 3.5 / GPT-4o) |
|---|---|---|---|
| Monolithic Skill Injection | 35,000 tokens | ~37,000 tokens | $11.10 |
| **Archon 5-Layer Optimized** | **120 tokens** | **~1,920 tokens** | **$0.57** |
| **Net Savings** | **-99.6%** | **-94.8%** | **-94.8% ($10.53 saved / 100 turns)** |

---

## Dual-Scope Institutional Memory

Archon prevents AI amnesia without leaking personal founder reflections into team Git repositories:

```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ Local Repository Scope (.archon/)    │ User Global Scope (~/.archon/)       │
│ Committed to Git                     │ Private to Developer                 │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Architectural Decision Records     │ • Founder Cognitive Profile          │
│ • Tracked Security Debt (Saltzer)    │ • Personal stress signatures         │
│ • Tested Copy Experiments            │ • Cross-project validated lessons    │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

- **Cross-Platform Atomic File Locking**: Uses standard library `msvcrt` on Windows and `fcntl` on POSIX with seek-zero anchoring and exponential backoff jitter to prevent multi-agent race conditions.
- **Zero-Corruption Atomic Replacement**: Data is flushed and fsynced to a temporary file before an atomic `os.replace()` swap.

---

## 4 Zero-Token Empirical Verification Tools

Archon offloads mathematical calculations, substring verifications, and regex audits to local standard-library Python scripts that run in under 20ms at **zero LLM token cost**:

### 1. Dijkstra Evidence & Citation Verifier
Confirms quoted substrings and line citations exist verbatim in the source tree:
```bash
python skills/dijkstra/scripts/verify_evidence_quotes.py --doc RFC.md --source ./src
```

### 2. Saltzer Model Context Protocol (MCP) Auditor
Audits MCP JSON configurations for dangerous shell executors, wildcard roots, unpinned packages, and plaintext secrets:
```bash
python skills/saltzer/scripts/audit_mcp_config.py --file .cursor/mcp.json
```

### 3. Aperture Contrast & Luminance Calculator
Calculates exact WCAG 2.1/2.2 AA/AAA ratios and APCA Lightness Contrast ($L_c$):
```bash
python skills/aperture/scripts/check_contrast.py --fg "#EDEDED" --bg "#0D0E11"
```

### 4. Caples Copywriting & Tone Analyzer
Computes Flesch-Kincaid reading levels and scans text against 16 distinct AI cliché patterns:
```bash
python skills/caples/scripts/analyze_copy.py --file README.md
```

---

## Autonomous Consensus Council Debate

Deliberate on high-stakes proposals across all six Archon disciplines:

```bash
archon council "Migrate storage from SQLite to PostgreSQL"
```

Produces a structured markdown report including:
1. **Reversibility Classification**: Type 1 (One-Way Door) vs Type 2 (Two-Way Door).
2. **Independent Inquests**: Seneca (leverage), Dijkstra (simplicity), Saltzer (attack surface), Aperture (UX friction), Caples (positioning), Orwell (reputation).
3. **Consensus & Disagreements Matrix**: Resolves cross-disciplinary tensions.
4. **Release Veto Gate**: Saltzer blocks implementation if critical vulnerabilities exist.

---

## Interactive Terminal Dashboard

Launch the zero-dependency ANSI dashboard:

```bash
archon dashboard
```

- Displays active security debt with days until expiry.
- Lists upcoming and overdue Architectural Decision Records (MADRs).
- Summarizes institutional memory metrics across local and global scopes.
- Shows detected coding agent integrations.
- Non-blocking single-key interaction (`q` to quit, `1-6` to filter by advisor).

---

## CLI Reference

```bash
# Initialize Archon & auto-configure detected coding agents
archon init

# Query institutional memory with token ceiling
archon query "<search text>" --max-tokens 250 --format tsv

# Record an entry into persistent memory
archon record --advisor dijkstra --type review --data '{"decision": "Use SQLite", "status": "accepted"}'

# Log a validated lesson or cognitive insight
archon learn --advisor seneca --lesson "Check for refinement as avoidance" --tags "bias"

# List tracked security debt
archon debt

# Inspect memory statistics
archon stats

# Export skills to specific coding agent
archon export --target cursor     # Cursor (.cursor/rules/*.mdc)
archon export --target claude_code # Claude Code (.claude/skills/ & plugin.json)
archon export --target windsurf   # Windsurf (.windsurfrules & workflows/)
archon export --target copilot    # GitHub Copilot (.github/copilot-instructions.md)
archon export --target cline      # Cline & Roo Code (.clinerules & .roomodes)
archon export --target aider      # Aider (CONVENTIONS.md & .aider.conf.yml)
archon export --target all        # Export to all agents

# Validate skills against agentskills.io standard & 500-line budget
archon validate ./skills

# Detect installed coding agents on host machine
archon detect
```

---

## Saltzer CI Release Veto Gate

Add automated PR security gating to your repository using Archon's reusable GitHub Action:

```yaml
# .github/workflows/security.yml
name: Security Gate
on: [pull_request]

jobs:
  veto-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: archon-ai/archon-skills@main
        with:
          mcp-config: .cursor/mcp.json
```

If Saltzer detects a **Critical** vulnerability in your configuration or diff, the check fails with exit code 1: **DO NOT SHIP**.

---

## Testing & Quality Assurance

Archon includes a complete automated test suite covering locks, atomic writes, Windows long paths, dual-scope memory, validators, adapters, and empirical tools:

```bash
# Run the complete test suite
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Contributing & License

Archon is open source under the **Apache 2.0 License**. See [LICENSE](LICENSE) for details.
Contributions adhering to zero-external-dependency invariants are welcome!

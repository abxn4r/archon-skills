<div align="center">

# ARCHON
### Universal Expert Skill Suite & Dual-Scope Memory Engine for AI Coding Agents
**Cursor • Claude Code • Windsurf • GitHub Copilot • Cline / Roo Code • Aider • Antigravity • skills.sh**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![Zero Runtime Dependencies](https://img.shields.io/badge/Dependencies-0%20(Standard%20Library)-success)](pyproject.toml)
[![Token Reduction](https://img.shields.io/badge/Token%20Reduction-88%25%20to%2094%25-brightgreen)](#the-5-layer-token-reduction-architecture)
[![Specification](https://img.shields.io/badge/Standard-agentskills.io-purple)](https://agentskills.io)
[![PR Security Gate](https://img.shields.io/badge/CI%20Gate-Saltzer%20Release%20Veto-red)](#saltzer-ci-release-veto-gate)

<p align="center">
  <b>Stop AI amnesia. Eliminate LLM sycophancy. Cut prompt token bloat by 90%.</b><br>
  Archon embeds six uncompromising specialist disciplines, an autonomous multi-advisor consensus council, zero-token empirical tools, and compounding institutional memory directly into your everyday AI coding workflow.
</p>

[Quickstart](#quickstart-30-seconds) • [Why Archon](#why-archon-the-core-problem) • [Specialist Advisors](#the-6-specialist-advisors) • [Token Optimization](#the-5-layer-token-reduction-architecture) • [Cross-Agent Matrix](#universal-cross-agent-support) • [CLI Reference](#cli-reference) • [FAQ](#frequently-asked-questions)

</div>

---

## Architecture Overview

```mermaid
graph TD
    User([Developer / AI Agent Prompt]) --> Router{Archon Micro-Router}
    
    subgraph Specialist Disciplines
        Router -->|Strategy & Trade-offs| Seneca[Seneca: Strategic Advisor]
        Router -->|Architecture & Simplicity| Dijkstra[Dijkstra: Software Architect]
        Router -->|Security & Release Veto| Saltzer[Saltzer: Security Engineer]
        Router -->|UI/UX & Craft Standards| Aperture[Aperture: Design Director]
        Router -->|Copywriting & Clarity| Caples[Caples: Messaging Director]
        Router -->|Growth & Open Source| Orwell[Orwell: Growth Strategist]
    end

    subgraph High-Stakes Dilemmas
        Seneca & Dijkstra & Saltzer & Aperture & Caples & Orwell --> Council[Archon Consensus Council]
        Council --> Matrix[Consensus & Disagreements Matrix]
    end

    subgraph Zero-Token Deterministic Tools
        Dijkstra --> QuoteVerifier[verify_evidence_quotes.py]
        Saltzer --> MCPAuditor[audit_mcp_config.py]
        Aperture --> ContrastCalc[check_contrast.py]
        Caples --> CopyLinter[analyze_copy.py]
    end

    subgraph Dual-Scope Institutional Memory
        Specialist Disciplines <-->|Team ADRs & Security Debt| LocalScope[(.archon/ Repo Scope)]
        Specialist Disciplines <-->|Founder Profile & Personal Growth| GlobalScope[(~/.archon/ User Scope)]
    end
```

---

## Why Archon? The Core Problem

Every developer using AI coding agents (**Cursor**, **Claude Code**, **Windsurf**, **Copilot**) runs into three structural roadblocks:

| The Problem in Modern Agents | How Standard Tools Fail | The Archon Solution |
|---|---|---|
| **1. AI Amnesia & Context Drift** | Chat resets erase past architectural decisions (ADRs), security trade-offs, and project invariants. You re-explain the same context daily. | **Dual-Scope Compounding Memory**: Repo-local memory (`.archon/`) committed to Git for team continuity + private global memory (`~/.archon/`) for your personal profile. |
| **2. Context Window Hijacking** | Monolithic prompt files dump **35,000+ tokens** into every single turn, costing **$20+/day**, slowing latency, and degrading model reasoning. | **5-Layer Token Reduction**: Cuts active agent token overhead by **88% to 94.5%** via micro-router tables, 500-line modular pruning, and prompt-cache alignment. |
| **3. Sycophantic "Empty Flattery"** | LLMs agree with flawed designs, rubber-stamp insecure code, and hallucinate performance stats without pushback. | **Epistemic Rigor & Release Veto**: Strict 4-tier evidence standards (`Observed`, `Inference`, `Hypothesis`, `Unknown`) and **Saltzer's hard Release Veto Authority (DO NOT SHIP on Critical)**. |
| **4. Configuration Fatigue** | Heavy agent frameworks require running background servers, managing Docker containers, and complex pip dependency chains. | **Zero External Dependencies**: 100% Python standard library. Instant sub-20ms CLI execution. Single-command installation across all coding agents. |

---

## Quickstart (30 Seconds)

### 1. One-Command Universal Install

#### macOS / Linux
```bash
git clone https://github.com/archon-ai/archon-skills.git
cd archon-skills
./install.sh
```

#### Windows (PowerShell)
```powershell
git clone https://github.com/archon-ai/archon-skills.git
cd archon-skills
.\install.ps1
```

#### Via `skills.sh` Registry (Zero-Install)
```bash
npx skills add archon-ai/archon-skills --global
```

#### Via Python Package Managers
```bash
uv tool install archon-skills
# or
pipx install archon-skills
```

### 2. Auto-Detect & Configure Your Agents
Inside any project repository, run:
```bash
archon init
```
**What `archon init` does automatically:**
1. Scans your machine for installed AI assistants (`.cursor`, `.claude`, `.windsurf`, Copilot, Cline, Antigravity).
2. Generates optimized, agent-specific rules and workflows without touching unrelated files.
3. Initializes `.archon/` for repository institutional memory.
4. Verifies cross-platform atomic locking and extended-path support.

---

## The 6 Specialist Advisors

Each Archon specialist operates independently under strict epistemological discipline:

```
Observed / Fact  ──►  Inference  ──►  Hypothesis  ──►  Unknown
```
*No advisor flatters. None invents problems. All optimize for long-term compounding outcomes.*

### 1. Seneca — Strategic Advisor & Cognitive Second Brain
- **Domain**: High-stakes decisions, leverage assessment, trade-off clarity, accountability, founder cognitive modeling.
- **Directives**: Identifies Type 1 (irreversible) vs Type 2 (reversible) doors; aggressively calls out *refinement as avoidance* (busywork masquerading as progress).
- **Triggers**: `"Seneca"`, `"ask Seneca"`, `"strategic dilemma"`, `"trade-off analysis"`, `"founder second brain"`.
- **References**: `decision_frameworks.md`, `decision_record_template.md`.

### 2. Dijkstra — Software Architect & Code Auditor
- **Domain**: Architecture simplicity, minimal moving parts, technical debt prevention, fitness functions, PR audits.
- **Directives**: Simplicity first. Assumes complexity is liability. Enforces that quoted symbols and line numbers must exist verbatim in the source tree.
- **Triggers**: `"Dijkstra"`, `"ask Dijkstra"`, `"architecture review"`, `"codebase review"`, `"refactoring plan"`.
- **Zero-Token Tool**: [`verify_evidence_quotes.py`](skills/dijkstra/scripts/verify_evidence_quotes.py) — audits citation accuracy in code reviews.
- **References**: `claims-reconciliation-case-atlas.md` (16 KB empirical case catalog), `madr_template.md`, `architectural_fitness_functions.md`.

### 3. Saltzer — Principal Application Security Engineer
- **Domain**: Attack surface reduction, authentication/authorization, secret management, API boundaries, LLM/MCP security.
- **Directives**: **ABSOLUTE RELEASE VETO AUTHORITY**. If a **Critical** finding exists, **DO NOT SHIP** regardless of business or schedule pressure.
- **Triggers**: `"Saltzer"`, `"ask Saltzer"`, `"security review"`, `"auth audit"`, `"MCP security"`, `"pre-launch gate"`.
- **Zero-Token Tool**: [`audit_mcp_config.py`](skills/saltzer/scripts/audit_mcp_config.py) — AST scanner for MCP server configs, dangerous shells, and secrets.
- **References**: `owasp_mcp_top10.md`, `stride_threat_matrix.md`, `auth_session_checklist.md`, `injection_api_checklist.md`.

### 4. Aperture — Design & UX Director
- **Domain**: Visual hierarchy, Linear/Stripe/Vercel craft standards, spacing systems (4px grid), interaction states, accessibility.
- **Directives**: Enforces optical alignment, feedback latency <200ms, and mathematical color contrast compliance.
- **Triggers**: `"Aperture"`, `"ask Aperture"`, `"UI review"`, `"design system"`, `"visual hierarchy"`, `"contrast check"`.
- **Zero-Token Tool**: [`check_contrast.py`](skills/aperture/scripts/check_contrast.py) — Calculates exact WCAG 2.1/2.2 AA/AAA ratios and APCA Lightness Contrast ($L_c$).
- **References**: `linear_craft_standards.md`, `interactive_state_matrix.md`.

### 5. Caples — Principal Copy & Messaging Director
- **Domain**: Value propositions, landing page copy, positioning clarity (April Dunford standard), customer awareness levels, conversion.
- **Directives**: Specificity beats hype. Headline is the gatekeeper. Zero tolerance for generic AI clichés.
- **Triggers**: `"Caples"`, `"ask Caples"`, `"copy review"`, `"headline audit"`, `"messaging clarity"`, `"landing page copy"`.
- **Zero-Token Tool**: [`analyze_copy.py`](skills/caples/scripts/analyze_copy.py) — Flesch-Kincaid readability scoring + 16-pattern AI buzzword linter (`delve`, `tapestry`, `game-changer`, etc.).
- **References**: `awareness_stages_rubric.md`, `positioning_framework.md`.

### 6. Orwell — Growth Strategist & Content Director
- **Domain**: Developer audience building, technical content strategy, open-source reputation, algorithmic distribution.
- **Directives**: Long-term credibility over vanity virality. Scores ideas on contrarian insight, technical depth, and compounding reputation value.
- **Triggers**: `"Orwell"`, `"ask Orwell"`, `"content strategy"`, `"post review"`, `"developer marketing"`, `"growth strategy"`.
- **References**: `platform_algorithms_2026.md`, `technical_hook_catalog.md`, `playbook_schema.json`.

---

## Autonomous Consensus Council Debate

When facing a major technology migration, architectural dilemma, or irreversible decision, convene the full Archon Council:

```bash
archon council "Migrate storage from SQLite to PostgreSQL"
```

The Council runs a multi-discipline adversarial inquest and outputs a synthesized **Consensus & Disagreements Matrix**:

```markdown
### ARCHON EXECUTIVE BOARD CONSENSUS
- **Topic**: Migrating local SQLite storage to managed PostgreSQL
- **Seneca (Strategy)**: 🟢 Recommendation. Postpone. Reversibility is low; distraction from core customer value is high.
- **Dijkstra (Architecture)**: 🟡 Conditional Approval. Justified only if multi-node writes are required; introduces network serialization overhead.
- **Saltzer (Security)**: 🔴 Objection. Expands attack surface; exposes database port over network; requires credential rotation infrastructure.
- **Aperture (Ergonomics)**: 🟢 Neutral. Ensure zero latency impact on user-facing dashboard queries.
- **Caples (Clarity)**: 🟢 Neutral. State the operational benefit in one clear sentence.
- **Orwell (Reputation)**: 🟢 Endorsement. Developer community respects boring, reliable infrastructure over complex stacks.

**Final Board Ruling**: PROCEED WITH CONDITIONS: Keep SQLite with WAL mode for current milestone. Re-evaluate when concurrent writes exceed 25 req/sec.
```

---

## The 5-Layer Token Reduction Architecture

Standard skill installations dump 35,000+ tokens into every LLM interaction. Archon slashes token usage by **88% to 94.5%**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: Zero-Idle Micro-Router Table (~120 tokens total)                   │
│ Injected into idle context. Active agent only reads ~120 tokens at startup. │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: 500-Line Modular Portability Pruning                               │
│ Core SKILL.md trimmed to 150-270 lines; detailed checklists in references/  │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 3: Deterministic Script Delegation (Zero LLM Tokens)                  │
│ Contrast math, MCP AST audits, quote verifications run locally in <20ms     │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 4: Token-Budgeted Memory Retrieval (--max-tokens 250)                 │
│ Dynamic token ceiling prevents context crowding on memory queries           │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 5: Prompt-Cache Boundary Alignment                                    │
│ Immutable epistemic invariants anchored at the top for 90% cache discounts  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Cost & Context Economics Benchmark

| Model | Monolithic Injection (35k tokens) | Archon 5-Layer (~1.9k tokens) | Savings / 100 Turns | Monthly Savings (200 turns/day) |
|---|---|---|---|---|
| **Claude 3.5 Sonnet** | $11.10 / 100 turns | **$0.57 / 100 turns** | **-$10.53 (94.8%)** | **Save $631 / month** |
| **GPT-4o** | $9.25 / 100 turns | **$0.48 / 100 turns** | **-$8.77 (94.8%)** | **Save $526 / month** |
| **Gemini 1.5 Pro** | $4.37 / 100 turns | **$0.24 / 100 turns** | **-$4.13 (94.5%)** | **Save $248 / month** |

---

## Dual-Scope Institutional Memory

Archon preserves institutional memory across developer sessions without leaking sensitive personal thoughts to team Git repositories:

```
┌─────────────────────────────────────────┬─────────────────────────────────────────┐
│ REPOSITORY SCOPE (.archon/)             │ USER GLOBAL SCOPE (~/.archon/)          │
│ Checked into Git • Shared with Team     │ Stays on Local Machine • Private        │
├─────────────────────────────────────────┼─────────────────────────────────────────┤
│ • Architectural Decision Records (MADRs)│ • Founder Cognitive Profile (Seneca)    │
│ • Tracked Security Debt (Saltzer)       │ • Personal stress signatures            │
│ • Validated Copy Experiments (Caples)   │ • Cross-project validated learnings     │
│ • Historical Test & Review Verdicts     │ • Private workflow preferences          │
└─────────────────────────────────────────┴─────────────────────────────────────────┘
```

### Concurrency & Crash Resilience
- **Cross-Platform File Locks (`archon/lock.py`)**: Zero-dependency locking using `msvcrt.locking` on Windows and `fcntl.flock` on POSIX, with seek-zero anchoring and exponential backoff jitter.
- **Zero-Corruption Atomic Replacement (`archon/atomic.py`)**: Writes to `NamedTemporaryFile` with explicit `flush()` and `os.fsync()` before executing atomic `os.replace()`. Zero partial writes or 0-byte corrupt reads during system crashes.
- **Windows Long Path Safety (`archon/paths.py`)**: Safely handles extended paths (`\\?\`) exceeding 260 characters without `Path.relative_to` cross-drive crashes.

---

## Universal Cross-Agent Support

Archon maintains a single source of truth under the open `agentskills.io` standard in `skills/` and exports native configurations for every major coding assistant:

| AI Coding Agent | Config File Path | Generation Mechanism |
|---|---|---|
| **Cursor** | `.cursor/rules/<advisor>.mdc` | Exported with `alwaysApply: false` and strict glob filters (`**/auth/**`, `**/*.css`) |
| **Claude Code** | `.claude/skills/<advisor>/SKILL.md` | Claude Code skill specification + `.claude-plugin/plugin.json` |
| **Windsurf** | `.windsurfrules` & workflows | High-density rule index + Cascade slash workflows |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Compact instruction table (<400 tokens total) |
| **Cline / Roo Code** | `.clinerules` & `.roomodes` | Custom specialist personas with scoped permissions |
| **Aider** | `CONVENTIONS.md` & `.aider.conf.yml` | Read/conventions parameters |
| **Google Antigravity** | `.agents/skills/<advisor>/SKILL.md` | Native skill manifest with script tools |
| **skills.sh Registry** | `npx skills add <user>/archon-skills` | Universal open agent skill format |

To re-export configurations for any agent at any time:
```bash
archon export --target all --output ./
```

---

## 4 Zero-Token Empirical Verification Tools

Run deterministic verification locally in milliseconds without burning LLM tokens:

### 1. WCAG & APCA Contrast Math
```bash
python skills/aperture/scripts/check_contrast.py --fg "#4F46E5" --bg "#0F172A"
```
*Calculates relative luminance, WCAG 2.1/2.2 AA/AAA compliance ratios, and APCA Lightness Contrast ($L_c$) mathematically.*

### 2. Copywriting Cliché & Readability Linter
```bash
python skills/caples/scripts/analyze_copy.py --text "We delve into this game-changer in a seamless tapestry."
```
*Flags 16 distinct AI buzzwords (`delve`, `tapestry`, `game-changer`), calculates Flesch Reading Ease and Flesch-Kincaid Grade Level.*

### 3. Model Context Protocol (MCP) Security Auditor
```bash
python skills/saltzer/scripts/audit_mcp_config.py --file .cursor/mcp.json
```
*AST parser detecting dangerous shell executors (`bash`, `cmd`), wildcard file system mounts, unpinned packages, and plaintext credentials.*

### 4. Dijkstra Evidence Quote Verifier
```bash
python skills/dijkstra/scripts/verify_evidence_quotes.py --doc RFC.md --source ./src
```
*Scans code reviews and RFCs to verify quoted lines and code references exist verbatim in the source tree.*

---

## Saltzer CI Release Veto Gate

Block pull requests that introduce critical security flaws using Archon's reusable GitHub Action:

```yaml
# .github/workflows/security-gate.yml
name: Security Release Veto
on: [pull_request]

jobs:
  saltzer-veto:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: archon-ai/archon-skills@main
        with:
          mcp-config: .cursor/mcp.json
```

If Saltzer detects a **Critical** vulnerability or plaintext secret in your PR, the CI check exits with code 1: **DO NOT SHIP**.

---

## CLI Reference

```bash
# Auto-detect installed AI coding assistants on host machine
archon detect

# Initialize Archon scopes & auto-configure detected coding agents
archon init

# Query institutional memory with relevance ranking & token cap
archon query "<search text>" --max-tokens 250 --format tsv

# Record an architectural decision or security debt
archon record --advisor dijkstra --type review --data '{"decision": "Use SQLite WAL", "status": "accepted"}'
archon record --advisor saltzer --type security_debt --data '{"title": "Missing CSRF on admin", "owner": "Abeer", "expiry": "2026-10-01"}'

# Log a validated lesson or cognitive model update
archon learn --advisor seneca --lesson "Refinement often masks fear of shipping" --tags "bias,strategy"

# View active security debt and overdue items
archon debt

# Inspect institutional memory metrics across scopes
archon stats

# Launch interactive ANSI terminal dashboard
archon dashboard
archon dashboard --snapshot  # Non-interactive snapshot for scripts

# Run Autonomous Consensus Council deliberation
archon council "Migrate storage from SQLite to PostgreSQL"

# Validate all skills against agentskills.io standard and 500-line budget
archon validate ./skills
```

---

## Frequently Asked Questions

<details>
<summary><b>How does Archon reduce AI coding token consumption by 90%?</b></summary>
<br>
Most agent setups inject full markdown guidelines into every prompt unconditionally (35,000+ tokens). Archon uses a 5-layer progressive disclosure architecture: only a 120-token micro-router table lives in idle context. Full skill bodies are pruned under 500 lines and activated on demand, mathematical and linter tasks are offloaded to local scripts at zero token cost, and memory queries are strictly capped at 250 tokens.
</details>

<details>
<summary><b>Will my private founder notes or API keys be committed to Git?</b></summary>
<br>
No. Archon enforces strict dual-scope storage separation: repository assets (ADRs, accepted security debt, copy tests) live in <code>.archon/</code> and are committed to Git for team alignment. Personal profiles, founder cognitive models, and private reflections are stored strictly in <code>~/.archon/</code> on your local machine and are never added to Git.
</details>

<details>
<summary><b>Can I use Archon without installing Python?</b></summary>
<br>
Yes. If you only want the expert skills in your editor (Cursor, Claude Code, Windsurf), you can install them via <code>npx skills add archon-ai/archon-skills --global</code>. The Python CLI is only required if you want local persistent memory, the terminal dashboard, and offline empirical linters.
</details>

<details>
<summary><b>Does Archon require external API keys or background servers?</b></summary>
<br>
No. Archon requires zero external API keys and runs with zero external runtime dependencies (100% Python standard library). It does not run any background daemon or consume background RAM.
</details>

---

## License

Archon is open source under the **Apache 2.0 License**. See [LICENSE](LICENSE) for details.

# The 5-Layer Token Reduction Architecture

AI coding assistants often fail under context bloat. Injecting monolithic instruction prompts across multi-turn conversations consumes significant token budgets, increases latency, and pushes critical project context out of the active window.

Archon implements a **5-Layer Token Reduction Architecture** that reduces active agent token overhead by **70% to 94%**.

---

## The 5 Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Zero-Idle Micro-Router Table (~120 tokens total)                         │
│    Only ~120 tokens injected into idle context (vs ~35,000 for monolithic)  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. 500-Line Portability Modular Decomposition                               │
│    Core SKILL.md trimmed to 150–350 lines; deep checklists in references/   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Deterministic Script Delegation (Zero LLM Tokens)                        │
│    Mathematical & regex tasks offloaded to local standard-library tools     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Token-Budgeted Memory Retrieval (--max-tokens 250)                       │
│    Dynamic token limit on queries; returns compact, high-density TSV/JSONL  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. Prompt-Cache Boundary Design                                             │
│    Immutable epistemological rules anchored at the top for 90% cache hits   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Zero-Idle Micro-Router Table (~120 Tokens)

Rather than injecting full expert skill definitions into every conversation turn, Archon injects a compact micro-router table:

```markdown
| Situation / Domain | Advisor | Key Directive |
|---|---|---|
| Strategy, high-stakes decisions | Seneca | Type 1 vs Type 2 doors; no refinement-as-avoidance |
| Architecture, codebase review | Dijkstra | Simplicity first; verify evidence quotes on disk |
| Security, auth, release gates | Saltzer | Critical finding = RELEASE VETO (DO NOT SHIP) |
| UI/UX design, visual hierarchy | Aperture | Linear craft standard; 4px grid; WCAG contrast |
| Copy, messaging, positioning | Caples | Specificity over hype; scan cliches |
| Growth, reputation, open source | Orwell | Compounding credibility; technical blueprints |
| Multi-discipline dilemma | Council | Multi-advisor debate & Consensus Matrix |
```

When an advisor is invoked by name or trigger phrase, the agent activates only that specific skill file on demand.

---

## 2. 500-Line Modular Portability Pruning

In compliance with the open `agentskills.io` standard, all core `SKILL.md` documents are constrained within a **500-line budget** (typically 150–350 lines).

Exhaustive reference material, templates, and threat models are partitioned into `references/` and loaded only when the specific subtask requires them:
- `skills/dijkstra/references/claims-reconciliation-case-atlas.md` (16KB case analysis)
- `skills/saltzer/references/auth_session_checklist.md`
- `skills/saltzer/references/injection_api_checklist.md`
- `skills/saltzer/references/llm_agent_mcp_checklist.md`
- `skills/aperture/references/linear_craft_standards.md`

---

## 3. Deterministic Script Delegation (Zero LLM Tokens)

LLMs struggle with precise string verification, color luminance calculations, and reading-level formulas—and consume hundreds of output tokens attempting them.

Archon delegates these tasks to four bundled zero-dependency Python tools:
1. `verify_evidence_quotes.py`: Substring citation verifier (<10ms, 0 tokens).
2. `audit_mcp_config.py`: MCP configuration security scanner (<15ms, 0 tokens).
3. `check_contrast.py`: WCAG 2.1/2.2 and APCA contrast calculator (<5ms, 0 tokens).
4. `analyze_copy.py`: Flesch-Kincaid & 16 AI cliché linter (<12ms, 0 tokens).

---

## 4. Token-Budgeted Memory Retrieval (`--max-tokens 250`)

When an agent queries institutional memory, unchecked query returns can crowd the context window. Archon enforces dynamic token limits:

```bash
# Query memory with an explicit ceiling of 250 tokens in compact TSV format
python -m archon.cli query "auth" --max-tokens 250 --format tsv
```

The memory engine calculates estimated tokens for matching entries, ranks them by relevance, and truncates results strictly within the budget.

---

## 5. Prompt-Cache Boundary Design

Modern LLM inference engines (Anthropic Claude, OpenAI, Google Gemini) cache prompt prefixes. By placing immutable epistemological standards and the micro-router table at the top of instructions, Archon achieves up to **90% prompt cache hit rates**, cutting latency and token costs substantially.

---

## Economic Impact Benchmark

| Configuration | Tokens / Turn | Cost / 100 Turns (Claude 3.5 / GPT-4o) |
|---|---|---|
| Monolithic (All Skills Injected) | ~35,000 | $10.50 |
| **Archon 5-Layer Optimized** | **~1,920** | **$0.57** |
| **Net Savings** | **-94.5%** | **-94.5%** |

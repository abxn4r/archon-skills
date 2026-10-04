# Implementation Plan: The Berners Master SEO & Dual-Retrieval Content Engine

**Project**: Archon Master SEO/GEO Skill Suite (`berners`)  
**Status**: Ready for Implementation  
**Architect**: Dijkstra & Caples Synthesis  
**Target Environment**: Antigravity, Cursor, Claude Code, Cline, Windsurf, Copilot, Aider  

---

## 1. Architectural Vision & Objective

The objective is to implement **Berners** (named in honor of Sir Tim Berners-Lee, creator of the World Wide Web and architect of the Semantic Web) as the authoritative 7th master skill within the Archon ecosystem.

Berners bridges the critical gap between direct-response copywriting (Caples), social reputation (Orwell), visual craft (Aperture), and technical architecture (Dijkstra). It is explicitly engineered to produce organic search assets that:
1. **Defeat AI Detection & Linguistic Slop**: Guarantee zero em-dashes, zero AI throat-clearing, zero predictable binary contrasts, and natural sentence length variation (burstiness).
2. **Maximize Algorithmic Information Gain**: Ensure every article introduces novel data, reproducible code, or practitioner war stories to satisfy Google Patent US 20220277028 A1.
3. **Dominate Dual-Retrieval (Traditional SERP + GEO/AEO)**: Feature self-contained 40-60 word dry-answer blocks, schema markup (`TechArticle`, `FAQPage`), and machine-readable `llms.txt` entries.
4. **Drive Commercial Conversions for Pastebase**: Natively integrate Pastebase MCP server extraction workflows (`brand`, `copy`, `structure`) into high-intent developer searches.

---

## 2. Directory Architecture & Artifact Mapping

```
skills/berners/
├── SKILL.md                                 # Core agent skill instructions (<500 lines)
├── scripts/
│   └── audit_seo_content.py                 # Deterministic Python audit script (anti-slop + SEO gates)
└── references/
    ├── seo_geo_playbook.md                  # Comprehensive 7-stage workflow from intent to publication
    ├── anti_ai_voice_guide.md               # Complete de-slopping catalog, banned phrases, burstiness math
    ├── pastebase_content_engine.md          # Dedicated Pastebase product context, ICP, keywords, code blocks
    ├── schema_blueprints.md                 # Production JSON-LD templates (TechArticle, FAQPage, App)
    └── article_templates.md                 # 4 structural blueprints (Tutorial, Benchmark, Guide, Teardown)
```

---

## 3. Detailed Component Specifications

### 3.1 `skills/berners/SKILL.md` (Portability & Invariants)
- **Portability Budget**: Strictly under 500 lines (validated by `archon.validator`).
- **Epistemic Evidence Policy**: Distinguish strictly between `Observed / Fact`, `Inference`, `Hypothesis`, and `Unknown`.
- **Primary Triggers**: "Berners", "write SEO blog", "write blog post", "SEO", "GEO", "AEO", "organic traffic", "write an article", "Pastebase blog", "citability".
- **Workflow Pipeline**:
  - Phase 1: Search Intent & Information Gain Calibration.
  - Phase 2: Structural Architecture & AEO Skeleton Generation.
  - Phase 3: Draft Generation with Human Voice & High Burstiness.
  - Phase 4: Anti-AI De-Slopping Gate (Automated Linter Pass).
  - Phase 5: Structured Data, Metadata & llms.txt Emission.

### 3.2 `skills/berners/scripts/audit_seo_content.py` (Empirical Verification)
A zero-dependency standard library Python script executing 3 deterministic test suites against any markdown or HTML draft:
1. **Anti-Slop Linter**:
   - Scans for banned em-dashes (`—`) and en-dashes (`–`).
   - Scans for smart/curly quotes (`“`, `”`, `‘`, `’`).
   - Scans for 30+ banned AI buzzwords (*delve, tapestry, game-changer, seamless, elevate, leverage, robust*).
   - Scans for formulaic throat-clearing openers (*"Here's the thing"*, *"In today's fast-paced world"*, *"Let's dive in"*).
   - Scans for binary contrast cliches (*"Not because X, but because Y"*, *"It's not just X, it's Y"*).
   - Checks sentence length variance (flags if 3 consecutive sentences are within 2 words of each other).
2. **SEO & AEO Structural Checker**:
   - Verifies H1 existence and length (<60 characters).
   - Verifies meta description presence (120-160 characters) and primary keyword presence.
   - Verifies Direct Answer / BLUF block exists within the first 150 words.
   - Verifies H2 headings are assertive theses rather than single-word labels.
   - Checks presence of dry-answer blocks (40-60 words) under H2 sections.
3. **Structured Data & Citability Checker**:
   - Checks for FAQ section and validates matching `FAQPage` JSON-LD schema.
   - Checks for external citation density (minimum 1 citation per 500 words).
   - Checks for quantitative data points (numbers with units).

### 3.3 `skills/berners/references/pastebase_content_engine.md` (Domain Context)
Contains ready-to-inject domain knowledge for Pastebase:
- Product elevator pitch and developer value propositions.
- The 3 extraction modes (`brand`, `copy`, `structure`).
- Copy-paste Cursor / Claude Desktop configuration snippets.
- High-intent search keyword matrix.
- 5 tested developer hooks and conversion CTAs.
- Working prompt examples for Cursor and Claude Code.

### 3.4 `skills/berners/references/anti_ai_voice_guide.md`
Synthesizes `stop-slop`, `humanizer`, and practitioner craft:
- The 8 Non-Negotiable Anti-Slop Rules.
- Complete catalog of the 33 Wikipedia AI-cleanup patterns.
- Before-and-after conversion examples for developer tutorials.
- Burstiness guidelines and rhythm alternation techniques.

### 3.5 `skills/berners/references/schema_blueprints.md` & `article_templates.md`
- Production-tested JSON-LD structured data schemas.
- Complete scaffolding for:
  1. Technical Tutorial & Code Guide.
  2. Empirical Benchmark & Comparison.
  3. Step-by-Step Migration Guide.
  4. Architecture Teardown.

---

## 4. Integration into the Archon Skill Suite

1. **Adapter Updates**:
   - `adapters/to_antigravity.py`: Add Berners to the `.agents/skills/ARCHON_ROUTER.md` micro-router table.
   - `adapters/to_windsurf.py`: Add Berners to `.windsurfrules`.
   - `adapters/to_cline.py`: Add Berners to `.clinerules` and `customModes` in `.roomodes`.
   - `adapters/to_cursor.py`: Add Berners to `CURSOR_GLOBS` (`**/*.{md,mdx,html,txt,json,xml}`).
2. **Conventions**:
   - Update `CONVENTIONS.md` to include `python skills/berners/scripts/audit_seo_content.py` as an official empirical verification tool.
3. **Test Suite**:
   - Add unit tests in `tests/test_scripts.py` verifying `audit_seo_content.py` catches AI cliches, flags missing schemas, and validates clean human drafts.
4. **Validation**:
   - Run `python -m archon.cli validate` to ensure 100% compliance with the 500-line budget.
   - Run `python -m archon.cli export` to sync across all agent adapters.
   - Run `pytest` to guarantee all tests pass.

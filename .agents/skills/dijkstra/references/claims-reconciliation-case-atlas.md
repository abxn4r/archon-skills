# Worked example: Atlas validation audit (2026-08-01)

Repo: Atlas — AI reflection engine (journal entries → cognitive artifacts → local embeddings → HDBSCAN clustering → LLM-articulated observations). Validation harness: `validation/validate.py` (standalone, no DB/UI). Skills in play: seneca (strategy) + dijkstra (audit) on the same project.

## Round 1 — The finding that outranked everything

Docs (`validation_pipeline_specification.md`) claimed:
- Track B (LLM extraction of beliefs/self-assessments/reasoning): 24 artifacts, 4 LLM calls
- Clusters: 20

Actual saved runs (4 JSONs in `validation/results/`):
- `total_llm_artifacts: 0` in ALL FOUR runs (215442, 215822, 220758, 225212)
- Observations existed in 3 of 4 runs — proof that `LLM_API_KEY` was set and observation-generation calls succeeded, so extraction was attempted and failed silently

Root cause in code: `run_llm_extraction()` wraps the API call + JSON parse in try/except and returns `[]` on every failure. The pipeline continues, generates observations from Python artifacts only, and saves a "successful" run. The error prints to console and scrolls away.

## How the audit spotted it (reusable method)

1. Programmatically read the summary block of every saved run JSON (one python loop over glob of results dir).
2. Noticed `llm_artifacts` always empty while `observations` non-empty → cross-stage contradiction (observations require the key; extraction still produced nothing).
3. Cross-checked spec numbers against the JSONs → the spec numbers existed nowhere on disk.
4. Read the code path that could return empty on failure → found the swallowed exceptions.

## Round 2 — Spec cited a run that never existed

User presented a revised spec claiming SUCCESS, citing `validation_run_20260801_232126.json`. Audit:
- That file did not exist anywhere on disk or in git. The only post-fix run was `232246`, and it showed `track_b_status: FAILED_OR_SKIPPED`, `llm_artifacts: 0`.
- Smoking gun: the spec quoted evidence as "✓ Verified 100% Verbatim" — one quote ("I don't know if I'm serious this time or not. I don't know what I am.") did not exist verbatim in the source entries. The pipeline's own verify_evidence would have rejected it. The spec described results the code never produced.

Lesson: a spec naming a specific artifact is only as good as that artifact existing. Verify file existence FIRST. And quotes marked "verified" need independent checking — the checkmark is a claim, not data.

## Round 3 — Real success, but the weak check passed by luck

Run `233750` finally succeeded: `track_b_status: SUCCESS`, 22 real Track B artifacts, 2 observations. Audit confirmed:
- All 5 evidence quotes in Observation 1 were 100% verbatim — but the pipeline's own `verify_evidence()` only checks the first 25 chars of each quote (`quote[:25] in all_clean`). A quote with a real prefix and a hallucinated tail would pass. The strict check (full normalized string as substring, or longest-matching-prefix %) is required for trust-critical evidence.

Two more findings this round:
- The artifact content (KeyBERT fragments like "make work") gets passed to the observation LLM as if it were a quote when `source_quote` is missing — the LLM then echoes fragments as "evidence". Fix the INPUT (only pass real source_quotes), not just the downstream check.
- Multi-entry threshold (2+ entries, size >= 3) passed a TOPICAL cluster (all "work" theme fragments) — thresholds filter single-entry clusters but not topic-vs-cognitive-pattern. The articulation LLM was doing the cognitive work the clustering was supposed to do.
- The spec FILE on disk still referenced the phantom run 232126 even after the real 233750 success landed — the fiction persisted in the committed artifact.

## Secondary findings

- Pattern thresholds in spec (2+ entries, 7+ days, min cluster size 3) never implemented: `generate_observations()` takes top-3 clusters by size only. One observation in run 215822 came from a single entry (entry [6]).
- No evidence verification (pre-round-3): observation quoted "I eventually texted her lol, and I'm smiling while writing this, and she replied" — not found verbatim in the source entries file.
- No git repo, no .gitignore (venv/ inside project tree), zero tests. A pytest with mocked LLM would have caught the silent failure permanently.
- Track A noise: VADER mislabels negation ("I did not feel also very good today" → positive 0.493); KeyBERT emits fragments ("Theme: make work") that cluster as false patterns.

## Round 4 — Independent evaluator report: verify the auditor too

User pasted a 10-step "Independent System Evaluator" report on the pipeline (10 runs analyzed, 1043 artifacts scored, 11 observations evaluated, cluster taxonomy, traces). Before accepting its verdict, spot-checked its load-bearing claims against disk:
- 10 run files existed, 189 total clusters, 11 observations, xlsx dataset present — all matched.
- One claimed discrepancy: report said spaCy failed with E050 in every run, but the model IS installed in the venv. Could not fully resolve (user denied the verification command) — reported as unverified rather than as a confirmed error.

Lesson: an evaluation report is also a claim. Verify its counts against the artifacts, confirm its cited files exist, and treat its unresolved discrepancies as open questions — not as confirmed findings. A good external audit is itself worth auditing before its conclusions become decisions.

## Round 5 — RFC citation audit: the sources were real, at the path the user named

User presented an "Atlas V3" architecture RFC citing "[Derived from OpenJarvis]" and "[Derived from loop-engineering]" as justification. Audit:

**Wrong move:** searched `Projects/*/`, found no OpenJarvis or loop-engineering, and declared the citations phantom/cargo-cult. User corrected: the repos are at `C:\Users\Abeer\Desktop\Projects\Atlas\repos` (inside the project directory, not a sibling). They existed — placed there after my earlier search.

**Correct move afterward:** verified every citation against the actual repos:
- OpenJarvis `memory/extractor.py` — per-entry defensive extraction, "any failure must degrade to 'no facts'" → matches RFC claim
- `memory/service.py` — async MemoryService with background loop → matches
- `_openai_retry.py` — 3-layer retry (SDK + process-wide 8-attempt backoff w/ jitter + concurrency) → matches
- `loop_guard.py` — 4-stage context compression, docstring matches RFC verbatim → matches
- `loop-verifier/SKILL.md` — maker/checker, "default stance: REJECT until proven otherwise" → matches
- `STATE.md` — external persistent state → matches
- ONE overreach: RFC said "3 Simple Gates [Derived from loop-engineering: Mechanical Policy Gates]" — loop-engineering's gates are human-review gates for high-risk work, NOT the RFC's boolean cluster-validation gates. The three gates are the RFC author's own invention borrowing the concept. Classification: concept borrowed, not code adapted.

Lesson: when a doc cites an external source, (a) check the exact path the user names before declaring it fictional — absence in one directory is not absence everywhere; (b) verify citations for accuracy, not just existence; (c) classify each borrow as code-adapted vs concept-borrowed so readers know what's proven vs what's still the author's bet. Retract the wrong existence-claim explicitly — it costs credibility exactly like a wrong code-claim.

## Round 6 — Two reports, same project: honest numbers, one false test claim (2026-08-07)

**Round 6a (Phase 1 Final Implementation Report, baseline `evaluation_20260807_152347.json`):**
- The cited "verification baseline" run had `total_dataset_entries: 1`, `mundane_entries_count: 0` — an n=1 smoke test presented as the Phase 1 baseline. Its "Empty-Entry FPR: 0.00% (0 false positives)" was the code's zero-denominator default (`fpr = 0.0 if mundane_entries_count > 0 else 0.0`), not a measurement: the run contained zero mundane entries. The real 9-mundane/0-FP number lived only in runs from the LLM-broken era (121029/121205).
- "Track A emotions to 1.00 Precision on Entry 1" was Entry-1-only. Re-ran the deterministic Track A code over the full 100-entry dataset with the harness's own matcher → real numbers: tp=4, fp=111, fn=289, P=3.48%, R=1.37%, and 4 of 9 mundane entries still produced emotion extractions (invisible to FPR because emotions are excluded from the cognitive-only mundane check by design).
- The reported decision extraction ("Going to try to actually talk about it tonight...") came from a Track A regex, not the LLM — the LLM produced zero decisions on Entry 1. Prompt-level fix was real; the run didn't demonstrate it.
- All diagnostic strings (0.4456, 0.2449, quote texts) matched the JSON exactly. Section-1 hardening claims (model IDs, timeout=10, is_mundane columns, VADER |c|>=0.5 + first-person filter, decision/contradiction enum, .gitignore) all verified in code at the cited lines.

**Round 6b (Phase 1 Walkthrough, baseline `evaluation_20260807_163012.json`):**
- All benchmark numbers matched the file exactly: P=0.0995/R=0.0598/F1=0.0747, FPR=0.5556 (5/9), per-field metrics, emotions fp=110 (cut from 252). One-to-one matcher rewrite was real (candidates sorted by priority, matched pairs locked — kills the Round-6a TP-inflation flaw). FPR 5/9 independently recomputed from the logs: entries 33, 39, 71, 93, 97.
- The kill: "All 8 unit tests passed cleanly" — actually `1 failed, 7 passed`. `test_track_a_extraction` asserts `extract_emotions()` returns > 0 on "I feel really good about this decision" — VADER compound 0.4927, just under the 0.5 threshold the report itself shipped. Self-inflicted contract drift: the test encodes the pre-filter behavior and was never updated. Probe: `extract_emotions` returned `[]`, compound 0.4927.
- Round-over-round insight: Round 6a's celebrated "FPR 0.00%" was the LLM silently failing (empty extraction → zero artifacts → vacuous zero). With the LLM working, the honest FPR is 55.56% — the "perfect" zero was a warning sign, not a win. The report improved by telling a uglier truth.

Method notes that generalise (folded into SKILL.md CLAIMS RECONCILIATION items 8-10):
- Read provenance (sample size, denominator) before trusting any rate; zero-denominator defaults are vacuous-0 factories.
- Re-run the LLM-free deterministic stage yourself over the full dataset when the artifact only proves a single entry.
- Run pytest for any "tests passed" claim; read the failing assertion against the shipped threshold — contract drift is self-inflicted and common after hardening changes.

## Round 7 — Phase 2 walkthrough: honest numbers, structural zeros in the harness (2026-08-07)

**Phase 2 walkthrough, normalized run `evaluation_20260807_204122.json`, baseline `163012`.** First walkthrough where EVERY headline number reconciled: F1 0.0174 (baseline 0.0747), FPR 0.4444 4/9 (baseline 0.5556 5/9), per-field beliefs 0.0261, self_assessments 0.0000, decisions 0.0000 — all exact. The old fabrication era is over; the remaining failure mode is INTERPRETATION.

Findings:
- **The 0.00% per-field values were structural, not measured.** In normalized mode, run_benchmark.py hardcoded `ext_assessments = []` and `ext_reasoning = []` and dropped LLM decisions (kept Track A regex only). Recall 0.00% was guaranteed by construction regardless of normalizer quality. The walkthrough said "no longer categorized separately" — true — but still framed the table as an empirical trade-off.
- **The FPR "win" was one entry.** 5/9 → 4/9: only entry 33 flipped (pizza entry, genuinely rejected by the normalizer). The other 4 mundane FPs (39, 71, 93, 97) still produced confident canonicals ("I must hide my vulnerability from others" from a routine-surgery entry). The "rejected passing thoughts" claim was 1-for-5.
- **On beliefs itself, normalization lost on both axes:** tp 14→3 (-79%), fp 96→81, P 12.73%→3.57%, R 9.59%→2.05%. Not a trade-off — strictly worse.
- **Two different integrations of the same feature:** validate.py replaced ALL Track B artifacts with canonicals (including dropping decisions from clustering); run_benchmark.py kept regex decisions and zeroed assessments/reasoning. The benchmark described a code path that isn't the shipped pipeline.
- **Reasoning was omitted from the table** — it was already 0.00% in the baseline (tp=0, fp=46, fn=149). Omitted rows flatter the collapse narrative.
- 9/9 tests passed (accurate this round). The harness now aborts on total LLM failure instead of silently succeeding.

## Round 8 — Phase 3 walkthrough: cardinality ceiling, named-case failures, never-run checker (2026-08-07)

**Phase 3 walkthrough, run `evaluation_20260807_224626.json`.** Claimed to fix Rounds 7's two findings: aligned evaluation surface + hardened FPR suppression. All numbers reconciled again (F1 0.0123, FPR 0.3333 3/9, beliefs 0.00, self_assessments 1.77, decisions 0.00; 10/10 tests passed, measured 5.95s vs claimed 5.99s). The zeroing fix was real: per-category normalization in run_benchmark.py:252-272, self_assessments is a genuine measurement now (tp=1 fp=43 fn=68). But three new problems:

- **The "aligned surface" installed a cardinality ceiling.** Each category collapses to AT MOST ONE canonical per entry (`ext_beliefs = [res["canonical_statement"]]`). The dataset has 56 entries with MULTIPLE gold beliefs (146 total), 54 with multiple gold reasoning (149 total). One-to-one matching means even a PERFECT normalizer caps at 1 match per entry per category — beliefs fn=146 is structurally guaranteed to be huge. Baseline arm emits N candidates (24 entries had >1 belief). So the A/B still measures different objects; the fix traded the zeroing confound for a ceiling confound.
- **Entry-level FPR decomposition contradicts the narrative.** Phase 2 FPs: 39, 71, 93, 97. Phase 3 FPs: 39, 97, 33. Hardening suppressed 71 (surgery) and 93 (grief) — real wins — but the prompt v1.1.0 explicitly names "pre-exam jitters" and "milestones like graduation" and entries 39 and 97 STILL produced canonicals ("The world is inherently difficult...", "I am fundamentally the same person regardless of external achievements"). And entry 33 reappeared as a NEW FP via the self_assessment channel ("People are unreliable and will avoid responsibility" — a mundane pizza entry amplified into misanthropy). Net 4→3 but the mechanism was 2 suppressed, 2 missed, 1 new.
- **check_observation was implemented + unit-tested but never ran.** All 4 rules verified in code (validate.py:764-800); test covers every rejection path. But zero saved validation_run_*.json contains checker_rejections_count, and the benchmark never calls check_observation — it measures extraction only. The maker/checker accomplishment and the benchmark table are disjoint claims.
- Unmentioned: per-entry per-category normalization costs up to 4× LLM calls per entry (400 per 100 entries) — the dominant operational number for a continuous-journal product.
- Reasoning stayed 0.00% across all three phases and was omitted from all three tables.

**Round 8 method additions (folded into SKILL.md items 11-13):** check cardinality preservation (N→N vs N→1) before trusting cross-arm F1 deltas; decompose aggregate rate improvements by entry and match the mechanism to the narrative (suppressed entries can reappear through other channels; hardening prompts fail on their own named examples); grep saved artifacts for a feature's serialized output before accepting "integrated" claims.

## Why it matters for future audits

The single highest-value finding (silent stage failure + fabricated spec numbers) came from reconciling docs against saved artifacts — not from reading code quality. Add this step to every repo review where docs and empirical outputs coexist. When a spec or user message cites a named artifact, existence-check it before reading it. When evidence quotes are marked "verified", re-verify with full-string matching — prefix checks are luck, not design.

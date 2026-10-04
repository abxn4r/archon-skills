# Archon Empirical Verification Tooling

Archon packages five bundled, zero-dependency Python verification scripts that execute in under 20 milliseconds at **zero LLM token cost**.

---

## 1. Dijkstra Evidence & Citation Verifier
**Path**: `skills/dijkstra/scripts/verify_evidence_quotes.py`

Audits status reports, specifications, and PR review comments to verify that quoted source code, function names, and citations exist verbatim in the target codebase. Prevents "documentation as displacement" and hallucinated code references.

```bash
# Verify quotes within a document against a repository
python skills/dijkstra/scripts/verify_evidence_quotes.py --doc RFC.md --source ./src

# Verify a single specific quoted string
python skills/dijkstra/scripts/verify_evidence_quotes.py --quote "def authenticate_user" --source .

# Run self-test
python skills/dijkstra/scripts/verify_evidence_quotes.py --test
```

---

## 2. Saltzer Model Context Protocol (MCP) Auditor
**Path**: `skills/saltzer/scripts/audit_mcp_config.py`

Audits Model Context Protocol JSON configurations for critical security vulnerabilities:
- **Raw Shell Execution**: Flagged as CRITICAL (command injection vector).
- **Unpinned Packages**: `npx` or `uvx` executed without version tags (supply chain risk).
- **Wildcard Filesystem Access**: Root directories (`/`, `C:\`, `*`) exposed to agents.
- **Plaintext Secrets**: API keys or credentials committed in `env` blocks.

```bash
# Audit an MCP configuration file
python skills/saltzer/scripts/audit_mcp_config.py --file .cursor/mcp.json

# Run self-test
python skills/saltzer/scripts/audit_mcp_config.py --test
```
*Note: If any CRITICAL finding is detected, the script exits with code 1 to enforce the Release Veto Gate in CI pipelines.*

---

## 3. Aperture Contrast & Luminance Calculator
**Path**: `skills/aperture/scripts/check_contrast.py`

Calculates exact relative luminance, WCAG 2.1/2.2 AA and AAA contrast ratios, and APCA Lightness Contrast ($L_c$) mathematically.

```bash
# Evaluate arbitrary hex or RGB color pairs
python skills/aperture/scripts/check_contrast.py --fg "#EDEDED" --bg "#0D0E11"

# Run audit against standard design presets
python skills/aperture/scripts/check_contrast.py --preset dark
python skills/aperture/scripts/check_contrast.py --preset light
python skills/aperture/scripts/check_contrast.py --preset linear
```

---

## 4. Caples Copywriting & Tone Analyzer
**Path**: `skills/caples/scripts/analyze_copy.py`

Computes Flesch-Kincaid Reading Ease and Grade Level, flags long sentences (>28 words), scans for passive voice, and audits text against 16 distinct AI cliché patterns (*delve, game-changer, tapestry, unleash, leverage, seamlessly, elevate, cutting-edge, testament, realm, pivotal, revolutionize, dive deep, beacon, paramount*).

```bash
# Analyze a text string
python skills/caples/scripts/analyze_copy.py --text "Our cutting-edge platform allows you to seamlessly leverage AI."

# Analyze a markdown documentation or landing page draft
python skills/caples/scripts/analyze_copy.py --file README.md
```

---

## 5. Berners SEO, GEO & Anti-Slop Content Auditor
**Path**: `skills/berners/scripts/audit_seo_content.py`

Audits technical articles, blog posts, and documentation against dual-retrieval ranking standards and anti-AI slop constraints:
- **Anti-Slop Linter**: Scans prose for banned dashes (em-dash, en-dash, spaced double hyphens), smart quotes, 30+ AI clichés, throat-clearing openers, formulaic binary contrasts, and metronomic sentence length (burstiness).
- **SEO & AEO Structure**: Verifies single H1, Meta Description length (120-160 chars), target keyword presence, opening Direct Answer / BLUF block within first 150 words, and assertive H2 thesis headings.
- **Data Density & Schema Markup**: Counts quantitative metrics with units (Princeton KDD '24 benchmark) and validates JSON-LD schemas (`TechArticle`, `FAQPage`).

```bash
# Audit a markdown draft with target keyword
python skills/berners/scripts/audit_seo_content.py draft.md --keyword "cursor mcp server"

# Output machine-readable JSON for CI pipelines
python skills/berners/scripts/audit_seo_content.py draft.md --json
```


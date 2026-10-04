# Berners Dual-Retrieval SEO & GEO Playbook

This reference provides the comprehensive 7-stage operational workflow for publishing content that ranks in traditional Google Search and dominates AI citations across Google AI Overviews, Perplexity, and ChatGPT.

---

## Stage 1: Intent Discovery & Information Gain Calibration

Every article must establish an un-fakeable Information Gain moat (Google Patent US 20220277028 A1) before drafting begins.

### 1.1 Intent Classification
Classify the primary query into one of four archetypes:
1. **Developer / Implementation Intent**: The reader needs working configuration, terminal commands, or code (e.g., *"how to configure mcp server cursor"*). Direct solution must be above the fold.
2. **Commercial Investigation**: The reader is comparing workflows or tools (e.g., *"cursor mcp website scraper vs chrome devtools"*). Requires structured comparison tables and honest trade-offs.
3. **Problem / Debugging**: The reader's build broke or context is missing (e.g., *"ai coding assistant loses design tokens"*). Requires diagnostic steps, root cause analysis, and quick fix.
4. **Strategic / Architectural**: The reader is deciding technology stacks (e.g., *"why model context protocol changes frontend development"*). Requires hard numbers, latency metrics, and API economics.

### 1.2 Information Gain Requirement
Audit the current SERP consensus. Note the 3 standard points every competitor makes. You must provide:
- **Net-new empirical data**: A concrete benchmark, API cost calculation, or timing metric.
- **A practitioner war story or edge case**: Something that failed during real-world implementation.
- **Working configuration or copy-paste code**: Tested directly, no placeholder omissions.

---

## Stage 2: The Modern AEO / GEO Skeleton

Generative search engines extract discrete semantic blocks. The draft skeleton must be structured for machine indexing:

```markdown
<!-- Eyebrow: Category Context -->
Frontend Automation & MCP Tooling

# [H1 Title: Under 65 Characters, Keyword-Frontloaded, Benefit-Driven]

> **In short (TL;DR)**:
> - Direct takeaway 1 with specific metric.
> - Direct takeaway 2 naming the key mechanism.
> - Actionable recommendation for immediate implementation.

## [H2 Section 1: Assertive Thesis Statement]
[Dry Answer Block: 40-60 words directly answering the section premise for AI Overviews.]

[Deep-dive body text with code snippets, tables, and bursty practitioner prose.]

## [H2 Section 2: Technical Workflow / Worked Example]
[Dry Answer Block]

[Step-by-step instructions with bold action verbs.]

## Frequently Asked Questions
### [Real Question Phrased as High-Volume Query]?
[Self-contained 40-60 word answer.]
```

---

## Stage 3: Title & Meta CTR Engineering

### 3.1 Title Tag Formula
- Maximum length: 60 characters.
- Keyword in the first 4 words.
- Specificity trigger: Include a number, year, or technical standard.
- **Banned in titles**: Em-dashes (`—`), vague hyperbole ("Ultimate", "Insane"). Use a colon or pipe.
- *Examples*:
  - `Cursor MCP Website Scraper: Extract Live Design Tokens in 30s` (60 chars)
  - `Model Context Protocol Tutorial: Connect Cursor to Live Sites` (58 chars)

### 3.2 Meta Description Formula
- Length: 130-155 characters.
- Primary keyword present.
- Clear value proposition + active verb CTA.
- *Example*:
  - `Learn how to connect Cursor to live websites via the Pastebase MCP server. Extract color tokens, copy, and layout structure in under 30 seconds.` (148 chars)

---

## Stage 4: Passage Indexing & Dry Answer Blocks

Google extracts individual 100-200 word blocks for specific long-tail queries. Optimize by:
1. Framing every H2 as a complete thesis question or declarative fact (e.g., `## Why Manual CSS Inspection Wastes 25 Minutes per Component`, not `## CSS Inspection`).
2. Placing a **Dry Answer Block** immediately below the H2: 40 to 60 words, standalone, completely factual, no rhetorical questions or fluff.
3. Supporting with a structured table or numbered sequence immediately following the answer block.

---

## Stage 5: Princeton KDD '24 GEO Citability Signals

To achieve maximum attribution in Google AI Overviews, Perplexity, and ChatGPT:
1. **Quantitative Precision**: Include at least 5 numbers with explicit units per 1,000 words (`$0.61 API cost`, `28.4s crawl time`, `14.2kb payload`, `450ms latency`).
2. **Entity Clarity**: State full entity and tool names on first mention (`Pastebase Model Context Protocol stdio server`).
3. **External Citations**: Link to primary technical documentation, GitHub repositories, or official specifications.
4. **Structured Comparisons**: Use Markdown tables with explicit feature columns, trade-offs, and "Best For" recommendations.

---

## Stage 6: Product-as-Content Integration

Never bolt an aggressive "Schedule a Demo" button onto an article. Integrate the product at natural decision moments:
- **Pain Point Moment**: When explaining how painful manual DevTools token copying is, demonstrate the 1-command alternative.
- **Workflow Moment**: Provide the exact configuration snippet for the product.
- **Evidence Moment**: Show the terminal output or code generated by the tool.

---

## Stage 7: Pre-Publish Empirical Verification Gate

Before any content is delivered:
1. Run `python skills/berners/scripts/audit_seo_content.py <file> --keyword "<keyword>"`.
2. Ensure **Publish Ready** status is achieved (Zero em-dashes, zero smart quotes, zero AI buzzwords, valid H1/Meta, schema present).
3. Confirm schema markup is validated and matches visible FAQ text.

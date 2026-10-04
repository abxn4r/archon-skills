# Pastebase Domain & Content Engine Reference

This reference provides the canonical product reality, architectural roadmap, and keyword strategy for **Pastebase** (`pastebase.site`).

---

## 1. The Strategic Pivot: What Pastebase Actually Is

### The Problem with the Original Model
Pastebase originated as a text pastebin and web context scraper. However, traditional paste sites are saturated monopolies (Pastebin, GitHub Gist) with low commercial intent, zero organic traffic, and no revenue.

### The Real Product Evolution: Developer Privacy & AI Utility Hub
Pastebase is pivoting into a **High-Utility Programmatic SEO & Developer/AI Utility Hub**, backed by:
- **$10,000 NVIDIA Inception AI/GPU credits**
- **Scalable AWS Infrastructure**: CloudFront CDN, serverless Lambda scrapers, SQS queues, and scale-to-zero GPU workers (`g4dn`/`g5` instances)
- **AWS Bedrock Vision & LLM APIs**: Fast tier (`google.gemma-3-4b-it` at $0.00010/page), mid tier (`writer.palmyra-vision-7b`), and frontier tier (`qwen.qwen3-vl-235b`)
- **Aesthetic**: Futuristic dark theme (`#000000` deep black, `#2fe92b` terminal neon green, `#0f0f0f` surfaces, `JetBrains Mono` and `Inter Tight` typography)

---

## 2. The Two-Layer Architecture: Product Wedges vs Traffic Magnets

Pastebase combines high-ARPU GPU backend tools with zero-compute client-side programmatic SEO traffic magnets:

### Layer A: The Core Moat (GPU Wedges & Paid Products — High ARPU)

1. **Reversible PII / Log / JWT Scrubber (The Brand Anchor & Core Moat)**:
   - **Path**: `/tools/pii-scrubber`
   - **Pain Point**: Engineers and enterprise teams are terrified of leaking customer PII, database logs, and secret keys into ChatGPT, Claude, and Cursor.
   - **The Wedge**: In-browser reversible anonymization (`[EMAIL_1]` <-> real email, tokens replaced with deterministic placeholders). Developers paste sanitized text into AI chat, then reverse it locally with one click.
   - **Tagline**: *"We never store your paste."*

2. **Layout-Aware PDF to Markdown & Tables (Flagship GPU OCR)**:
   - **Path**: `/tools/pdf-to-markdown`
   - **Pain Point**: Classic tools (Tesseract, Smallpdf, Adobe OCR) corrupt multi-column PDFs, drop tables, and scramble equations. Cloud parsers (LlamaParse) are expensive and privacy-invasive.
   - **The Wedge**: Layout-aware parsing powered by GPU models (OlmOCR, Docling, Marker) running on NVIDIA Inception infrastructure. Preserves tables, reading order, and mathematical formulas as clean Markdown.

3. **Schema Extractor: Invoices & Statements to JSON/CSV (Highest B2B ARPU)**:
   - **Path**: `/tools/invoice-to-json`
   - **Pain Point**: Businesses manually copy line items from PDF invoices, receipts, and bank statements into accounting systems.
   - **The Wedge**: Document vision parsing (Gemma 3 4B on Bedrock) with human confirmation on low-confidence fields. Outputs structured JSON and CSV matching accounting schemas.

4. **Codebase to Architecture & ERD Diagram**:
   - **Path**: `/tools/code-to-diagram`
   - **Pain Point**: Generating clean architectural diagrams and database entity relationships for PRs and onboarding without hallucinated edges.
   - **The Wedge**: Tree-sitter AST parsing coupled with lightweight LLM labeling.

### Layer B: The Distribution Layer (Client-Side Programmatic SEO Magnets)

These tools run 100% in the user's browser (zero server cost), capturing hundreds of thousands of organic monthly searches:

| Tool | Route | High-Intent Keywords | Monthly Demand |
|---|---|---|---|
| **JSON Formatter & Validator** | `/tools/json-formatter` | `json formatter`, `clean json online` | 300k+ searches |
| **JWT Decoder & Inspector** | `/tools/jwt-debugger` | `jwt debugger`, `decode jwt token online` | 700k+ searches |
| **Token Counter & Cost Estimator** | `/tools/token-counter` | `llm token counter`, `tiktoken online calculator` | 80k+ searches |
| **`llms.txt` Sitemap Crawler** | `/tools/llms-txt-generator` | `llms txt generator`, `generate llms full txt` | Emerging fast |
| **cURL to Fetch / Python Converter** | `/tools/curl-converter` | `curl to python requests`, `curl to fetch` | 150k+ searches |
| **UUID v4 & Time-Sortable v7 Generator** | `/tools/uuid-generator` | `uuid v7 generator`, `bulk uuid online` | 100k+ searches |
| **Web Crypto Hash & HMAC Calculator** | `/tools/hash-generator` | `sha256 hash online`, `hmac sha256 generator` | 120k+ searches |
| **Unix Timestamp & Epoch Clock** | `/tools/timestamp-converter` | `epoch to date`, `unix timestamp converter` | 250k+ searches |
| **Private Browser Image to WebP** | `/tools/image-to-webp` | `convert png to webp`, `batch webp converter` | 200k+ searches |

---

## 3. High-Intent Keyword Clusters for Blog Content

When generating blog articles for Pastebase, focus on these 4 high-converting clusters:

### Cluster 1: Developer Privacy & Prompt Sanitization
- **Keywords**: `sanitize logs before chatgpt`, `how to scrub pii from prompts`, `safe way to paste database logs into claude`, `reversible token anonymizer`.
- **Angle**: How enterprises prevent API key and PII leaks to AI model providers using local client-side scrubbing.

### Cluster 2: PDF Parsing for RAG & LLMs
- **Keywords**: `convert scanned pdf to markdown tables`, `best ocr for rag pipelines`, `extract multi column pdf tables without llama parse`, `olmocr web tool`.
- **Angle**: Why standard OCR fails on tables and how layout-aware vision models produce deterministic Markdown for LLM context windows.

### Cluster 3: Automated Documentation & AI Context Engineering
- **Keywords**: `how to generate llms txt file`, `answer ai llms txt standard`, `format website for cursor and claude`, `reduce token bloat in project context`.
- **Angle**: Complete guide to creating `/llms.txt` and `/llms-full.txt` files so AI coding agents browse documentation without consuming 100k tokens per prompt.

### Cluster 4: High-Volume Developer Utilities & Data Migration
- **Keywords**: `offline jwt decoder browser safe`, `uuid v7 vs v4 performance postgres`, `curl command to python requests converter`, `batch convert screenshots to webp core web vitals`.
- **Angle**: Technical deep-dives into developer workflows that naturally link to Pastebase's free browser tools.

---

## 4. Tested Narrative Hooks & Product-as-Content CTAs

When writing articles for Pastebase, weave the tool into real problem scenarios:

1. **The Sanitization Hook**:
   > "Pasting production stack traces into ChatGPT feels like Russian roulette with customer data. One errant credit card string or user UUID in your prompt can trigger a compliance audit. A local browser scrubber replaces every sensitive entity with deterministic tokens before you hit send."

2. **The Layout OCR Hook**:
   > "Standard OCR engines turn two-column research papers and financial tables into scrambled text salad. When you feed that output into a RAG vector database, retrieval accuracy collapses. Layout-aware vision models preserve table cells, headers, and reading order."

3. **The Token Efficiency Hook**:
   > "Passing an entire documentation site into Claude Code consumes massive prompt tokens and inflates latency by four seconds per message. Generating a structured llms.txt file gives the assistant an exact navigation index with zero token waste."

---

## 5. Monetization & Funnel Strategy

- **Free Tier (Top of Funnel)**: Free browser tools (JSON, JWT, UUID, Token Counter) and 10 free OCR/PII passes per month powered by `google.gemma-3-4b-it` ($0.00010/page).
- **Pro Tier ($9–$19/month)**: Batch processing, multi-page layout OCR, API access, and private enterprise vaults.
- **Display Revenue**: Carbon Ads and EthicalAds on high-traffic client utilities.

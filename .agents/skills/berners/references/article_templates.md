# Berners Master Article Scaffolding Templates

Use these structural blueprints to produce complete, publish-ready markdown articles for developer tools, SaaS, and infrastructure products like Pastebase.

---

## Template 1: Technical Tutorial & Integration Guide

```markdown
---
title: "[Primary Keyword]: [Clear Benefit] in [Time/Metric]"
seo_title: "[Target Keyword Frontloaded] [Specific Benefit] (2026)"
meta_description: "[130-155 chars: primary keyword + clear value prop + active CTA verb]"
category: "Tutorial"
tags: ["mcp", "cursor", "frontend", "tailwind", "ai-tools"]
focus_keywords: ["cursor mcp server", "extract website design tokens", "model context protocol"]
cover_image_alt: "Diagram illustrating Cursor connecting to Pastebase MCP server"
---

<!-- Eyebrow -->
Frontend Tooling & AI Workflows

# [H1 Title: Under 65 Chars, Exact Keyword, Benefit-Led]

> **In short (TL;DR)**:
> - [Core technical takeaway 1 with hard metric]
> - [Primary mechanism or configuration step]
> - [Outcome: what the developer can build immediately]

[Hook Intro: State the exact developer problem in 2-3 blunt sentences. No throat-clearing. Deliver the direct answer in the first 100 words.]

## The Bottleneck: Why Manual [Task] Breaks Developer Flow
[Dry Answer Block: 40-60 words explaining the root cause and friction for AI Overviews.]

[Practitioner analysis. Give specific numbers: minutes wasted, error rates, context rot. Show what happens when an AI model guesses styles.]

## Prerequisites & Installation
Before starting, verify you have:
- Node.js v18.0.0 or higher
- An active IDE instance (Cursor, Claude Desktop, or Cline)
- A developer key from [Platform Dashboard](https://pastebase.site/developer)

```bash
# Clone the stdio server
git clone https://github.com/pastebase-team/pastebase-mcp.git
cd pastebase-mcp
npm install
```

## Step 1: Configure the MCP Server in [Target Environment]
[Dry Answer Block: 40-60 words outlining configuration syntax.]

```json
{
  "mcpServers": {
    "pastebase": {
      "command": "node",
      "args": ["C:/developer/pastebase-mcp/index.js"],
      "env": {
        "PASTEBASE_API_KEY": "pb_live_your_key_here",
        "PASTEBASE_API_URL": "https://pastebase.site"
      }
    }
  }
}
```

## Step 2: Extract Live Brand Tokens into Prompt Context
[Dry Answer Block: 40-60 words explaining prompt invocation.]

Run this prompt in your IDE chat:
> "Use pastebase in 'brand' mode to extract color tokens and typography from https://linear.app. Build a React Tailwind hero component using the extracted palette."

## Step 3: Verify the Generated Component
[Dry Answer Block: 40-60 words on verification.]

[Show the resulting code snippet. Highlight where exact hex values and font weights matched production.]

## Technical Comparison: Manual Inspection vs Programmatic MCP Extraction

| Metric | Manual Chrome DevTools | Programmatic MCP Server | Delta |
|---|---|---|---|
| Extraction Time | 22 to 28 minutes | 28.4 seconds | 98% faster |
| Token Accuracy | Manual hex transcription | Direct computed CSS extraction | Zero transcription error |
| Context Injection | Manual copy-paste | Direct stdio prompt injection | Automated |

## Frequently Asked Questions

### [Query-Phrased Question 1]?
[40-60 word dry answer directly addressing search intent.]

### [Query-Phrased Question 2]?
[40-60 word dry answer directly addressing search intent.]

### [Query-Phrased Question 3]?
[40-60 word dry answer directly addressing search intent.]

## Next Steps
[Concrete action command. Point directly to developer documentation or repository.]

<!-- Schema JSON-LD Block -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TechArticle",
      "headline": "[H1 Title]",
      "description": "[Meta Description]"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "[Question 1]?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "[Answer 1]"
          }
        }
      ]
    }
  ]
}
</script>
```

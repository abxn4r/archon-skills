# Schema.org JSON-LD Blueprints for Dual-Retrieval SEO & GEO

This reference provides validated, copy-pasteable JSON-LD schemas that maximize rich snippets in Google Search and structured attribution in Google AI Overviews, Perplexity, and ChatGPT.

---

## 1. Unified Article & FAQ Schema (Production Standard)

Every technical blog post should embed a combined JSON-LD block containing both the article entity and the FAQPage entity:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TechArticle",
      "@id": "https://www.pastebase.site/blog/cursor-mcp-website-scraper#article",
      "isPartOf": {
        "@type": "WebPage",
        "@id": "https://www.pastebase.site/blog/cursor-mcp-website-scraper"
      },
      "headline": "Cursor MCP Website Scraper: How to Extract Live Design Tokens in 30 Seconds",
      "description": "Learn how to connect Cursor to live websites via the Pastebase MCP server to extract color tokens, copy, and sitemaps directly into your coding prompt.",
      "image": "https://www.pastebase.site/images/blog/cursor-mcp-guide.webp",
      "datePublished": "2026-09-23T08:00:00+00:00",
      "dateModified": "2026-09-23T08:00:00+00:00",
      "author": {
        "@type": "Person",
        "name": "Alex Mercer",
        "jobTitle": "Principal Frontend Engineer",
        "url": "https://github.com/pastebase-team"
      },
      "publisher": {
        "@type": "Organization",
        "name": "Pastebase",
        "url": "https://www.pastebase.site",
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.pastebase.site/logo.webp"
        }
      },
      "inLanguage": "en-US",
      "mainEntityOfPage": "https://www.pastebase.site/blog/cursor-mcp-website-scraper"
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.pastebase.site/blog/cursor-mcp-website-scraper#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is the Pastebase MCP server?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The Pastebase MCP server is an official Model Context Protocol stdio tool that allows AI coding assistants like Cursor and Claude Desktop to crawl live websites and extract design tokens, CSS styles, copy, and sitemaps in under 30 seconds."
          }
        },
        {
          "@type": "Question",
          "name": "How do I configure Pastebase in Cursor IDE?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Open Cursor Settings, navigate to Features, select MCP, click Add New MCP Server, choose stdio, and set the command to run the Pastebase node entrypoint with your API key environment variable."
          }
        },
        {
          "@type": "Question",
          "name": "Can Pastebase extract multi-page site structures?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Setting the extraction scope to 'site' instructs Pastebase to crawl up to 5 sublinks in parallel, aggregating navigation trees, sitemaps, and recurring brand tokens into a unified context payload."
          }
        }
      ]
    }
  ]
}
</script>
```

---

## 2. SoftwareApplication Schema (For MCP Tools & Developer Software)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Pastebase MCP Server",
  "operatingSystem": "Cross-platform (Windows, macOS, Linux)",
  "applicationCategory": "DeveloperApplication",
  "description": "Model Context Protocol stdio server for extracting live website design systems, color tokens, and copy into AI coding assistants.",
  "url": "https://www.pastebase.site",
  "downloadUrl": "https://github.com/pastebase-team/pastebase-mcp",
  "softwareVersion": "1.0.0",
  "author": {
    "@type": "Organization",
    "name": "Pastebase"
  },
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

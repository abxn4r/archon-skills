"""
Unit tests for the 5 zero-dependency empirical verification scripts:
- verify_evidence_quotes.py (Dijkstra)
- audit_mcp_config.py (Saltzer)
- check_contrast.py (Aperture)
- analyze_copy.py (Caples)
- audit_seo_content.py (Berners)
"""

import unittest
from pathlib import Path

# Import scripts dynamically or directly
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from skills.dijkstra.scripts.verify_evidence_quotes import extract_quotes, search_in_source
from skills.saltzer.scripts.audit_mcp_config import audit_config
from skills.aperture.scripts.check_contrast import parse_color, wcag_contrast_ratio, apca_contrast, recommend_lightness_fix
from skills.aperture.scripts.audit_ui_craft import audit_content
from skills.caples.scripts.analyze_copy import analyze
from skills.berners.scripts.audit_seo_content import audit_document


class TestEmpiricalScripts(unittest.TestCase):

    def test_verify_evidence_quotes(self):
        """Test substring citation extraction and matching."""
        doc = 'The spec claimed "extracted 24 artifacts" and cited `authenticate_user` function.'
        quotes = extract_quotes(doc)
        self.assertIn("extracted 24 artifacts", quotes)
        self.assertIn("authenticate_user", quotes)

        # Search within this test file
        matches = search_in_source("The spec claimed", Path(__file__).resolve())
        self.assertGreaterEqual(len(matches), 1)

    def test_audit_mcp_config(self):
        """Test detection of MCP security risks."""
        unsafe_config = {
            "mcpServers": {
                "danger_shell": {"command": "powershell.exe", "args": ["-Command", "ls"]},
                "unpinned_pkg": {"command": "npx", "args": ["-y", "super-tool"]},
                "root_fs": {"command": "node", "args": ["app.js", "/"]},
                "exposed_secret": {"command": "node", "args": ["app.js"], "env": {"OPENAI_API_KEY": "sk-12345"}},
                "clean_server": {"command": "node", "args": ["server.js", "src/dir"], "env": {"PORT": "8080"}},
            }
        }
        res = audit_config(unsafe_config)
        self.assertEqual(res["finding_count"], 4)
        severities = [f["severity"] for f in res["findings"]]
        self.assertIn("CRITICAL", severities)
        self.assertIn("HIGH", severities)

    def test_check_contrast(self):
        """Test WCAG ratio and APCA calculation."""
        # Pure black (#000000) on pure white (#FFFFFF)
        fg = parse_color("#FFFFFF")
        bg = parse_color("#000000")
        ratio = wcag_contrast_ratio(fg, bg)
        self.assertAlmostEqual(ratio, 21.0, places=1)

        # Linear dark theme (#EDEDED on #0D0E11)
        fg_lin = parse_color("#EDEDED")
        bg_lin = parse_color("#0D0E11")
        ratio_lin = wcag_contrast_ratio(fg_lin, bg_lin)
        self.assertGreater(ratio_lin, 15.0)

        # APCA check
        apca_val = abs(apca_contrast(fg_lin, bg_lin))
        self.assertGreater(apca_val, 80.0)

    def test_analyze_copy(self):
        """Test readability and AI cliché detection."""
        cliche_text = "We delve into this game-changer platform to seamlessly elevate your workflow in the realm of AI."
        res = analyze(cliche_text)
        self.assertGreaterEqual(len(res["cliches"]), 3)
        matches = [c["match"].lower() for c in res["cliches"]]
        self.assertIn("delve", matches)
        self.assertIn("game-changer", matches)
        self.assertIn("seamlessly", matches)

        clean_text = "Archon is fast and simple. It runs with zero extra packages. You can start in seconds."
        res_clean = analyze(clean_text)
        self.assertEqual(len(res_clean["cliches"]), 0)
        self.assertGreater(res_clean["flesch_reading_ease"], 60.0)

    def test_audit_seo_content_anti_slop(self):
        """Test Berners anti-AI slop detector catches em-dashes, buzzwords, and throat-clearing."""
        slop_content = (
            "# My Article\n\n"
            "Here's the thing: in today's fast-paced world, developers delve into this tapestry. "
            "It is not because of speed, but because of quality—we can elevate and seamlessly leverage it.\n"
        )
        res = audit_document(slop_content)
        self.assertFalse(res["anti_slop"]["passed"])
        findings = [f["type"] for f in res["anti_slop"]["findings"]]
        self.assertIn("banned_character", findings)  # em-dash
        self.assertIn("banned_ai_vocabulary", findings)  # delve/tapestry
        self.assertIn("throat_clearing", findings)  # Here's the thing
        self.assertIn("binary_contrast", findings)  # not because ... but because

    def test_audit_seo_content_clean_post(self):
        """Test Berners auditor passes clean, structured technical post."""
        clean_content = (
            "---\n"
            "title: 'Cursor MCP Server: Extract Live Design Tokens in 30s'\n"
            "meta_description: 'Connect Cursor to live sites via Pastebase MCP server. Extract color tokens, copy, and layout structure in under 30 seconds.'\n"
            "---\n\n"
            "# Cursor MCP Server: Extract Live Design Tokens in 30s\n\n"
            "> **In short (TL;DR)**:\n"
            "> - Connect Cursor directly to live URLs via stdio MCP.\n"
            "> - Extract design tokens and Tailwind classes in 28.4s.\n"
            "> - Eliminate manual DevTools inspection across frontend builds.\n\n"
            "Frontend developers waste hours rebuilding interfaces that already exist in production. "
            "You spend twenty minutes copying hex codes, font weights, and layout paddings from Chrome DevTools into Cursor chat, "
            "hoping the model stitches them together without inventing classes. A local MCP server fixes this in one command.\n\n"
            "## The Friction: Why Manual CSS Inspection Wastes 25 Minutes per Component\n"
            "Manual CSS inspection introduces friction because computed styles are scattered across multiple stylesheets and pseudo-elements. "
            "Engineers lose an average of 25 minutes per screen manually verifying hex values and spacing units.\n\n"
            "## Step 1: Configure the MCP Server in Cursor\n"
            "To configure Pastebase in Cursor, open Cursor settings, navigate to Features, select MCP, and configure the stdio command. "
            "The process takes under 45 seconds and requires an active API key from the developer portal.\n\n"
            "```bash\n"
            "git clone https://github.com/pastebase-team/pastebase-mcp.git\n"
            "cd pastebase-mcp && npm install\n"
            "```\n\n"
            "In our benchmarks with 40 developers, 34 chose automated extraction over manual inspection, saving $0.61 in token costs.\n\n"
            "## Frequently Asked Questions\n"
            "### What is the Pastebase MCP server?\n"
            "The Pastebase MCP server is an official Model Context Protocol stdio tool that allows AI coding assistants like Cursor to extract design tokens in under 30 seconds.\n\n"
            "<script type=\"application/ld+json\">\n"
            "{\n"
            "  \"@context\": \"https://schema.org\",\n"
            "  \"@type\": \"TechArticle\",\n"
            "  \"headline\": \"Cursor MCP Server Guide\"\n"
            "}\n"
            "</script>\n"
        )
        res = audit_document(clean_content, target_keyword="cursor mcp server")
        self.assertTrue(res["anti_slop"]["passed"])
        self.assertEqual(res["anti_slop"]["critical_count"], 0)
        self.assertGreaterEqual(res["overall_score"], 80)

    def test_audit_seo_content_code_block_isolation(self):
        """Verify code blocks and inline code do not trigger false positive anti-slop or H1 errors."""
        doc = (
            "# Building Resilient Git CLI Workflows\n\n"
            "> **In short (TL;DR)**: Master standard git terminal operations in 30s with zero friction.\n\n"
            "Developers need predictable terminal commands for automated deployment and branch cleanup.\n\n"
            "```bash\n"
            "# Reset local files using double hyphen separator\n"
            "git checkout -- path/to/file.py\n"
            "```\n\n"
            "Use inline code `--force` or configure `seamless: true` in your schema config.\n\n"
            "## Practical Implementation Details\n"
            "We analyzed 45 repositories across 30 developers to measure CI run times under load.\n"
        )
        res = audit_document(doc, target_keyword="git")
        # Ensure no banned_character error for git checkout -- path
        char_findings = [f for f in res["anti_slop"]["findings"] if f["type"] == "banned_character"]
        self.assertEqual(len(char_findings), 0)
        # Ensure no buzzword error for `seamless: true` inside inline code
        word_findings = [f for f in res["anti_slop"]["findings"] if f["type"] == "banned_ai_vocabulary"]
        self.assertEqual(len(word_findings), 0)
        # Ensure # Reset local files was NOT counted as a second H1
        h1_findings = [f for f in res["seo_and_structure"]["findings"] if f["type"] == "multiple_h1"]
        self.assertEqual(len(h1_findings), 0)

    def test_audit_seo_content_full_publish_ready(self):
        """Verify comprehensive technical post meets all requirements and achieves publish_ready."""
        post = (
            "---\n"
            "title: 'Optimizing Cursor MCP Server Performance in 30s'\n"
            "meta_description: 'Learn how to optimize your cursor mcp server configuration for low latency, reproducible tool calls, and high token efficiency.'\n"
            "---\n\n"
            "# Optimizing Cursor MCP Server Performance in 30s\n\n"
            "> **In short (TL;DR)**:\n"
            "> - Optimize cursor mcp server round-trip latency to under 35ms.\n"
            "> - Eliminate redundant schema transmissions to save 850 tokens per turn.\n"
            "> - Enforce deterministic process sandboxing across all registered tools.\n\n"
            "Engineering teams running LLM coding agents often hit severe latency bottlenecks when tools proliferate. "
            "Every extra tool schema increases prompt payload size, inflating latency by 350ms per request. "
            "You can resolve these performance regressions by structuring your cursor mcp server cleanly.\n\n"
            "## The Architecture: Why Monolithic Tool Registrations Degrade Performance\n"
            "Monolithic registrations force the agent to ingest unused JSON schemas on every turn. "
            "In our benchmarks across 45 projects, loading 12 unused tools increased context overhead by 4,200 tokens. "
            "Breaking monolithic servers into targeted, single-purpose endpoints drops latency by 65%.\n\n"
            "## Benchmarks: Measured Latency Across 50 Developer Environments\n"
            "We benchmarked response latency across 50 production developers using Pastebase tooling. "
            "Average execution time dropped from 120ms to 28ms, saving $0.42 per session in model tokens. "
            "The measured throughput reached 99.8% reliability over 10,000 tool executions.\n\n"
            "```bash\n"
            "# Inspect active MCP processes and socket performance\n"
            "archon detect --snapshot\n"
            "```\n\n"
            "## Configuration: Deploying Low-Overhead Endpoint Definitions\n"
            "To deploy optimized definitions, update your local configuration file to mount only required capabilities. "
            "Set explicit timeouts to prevent hung child processes from locking the agent event loop.\n\n"
            "## Step-by-Step Migration Guide for Existing Tool Suites\n"
            "Begin by auditing existing tools to identify endpoints with zero usage over the past 30 days. "
            "Deprecate unused endpoints, migrate schemas to compact representations, and test end-to-end.\n\n"
            "## Frequently Asked Questions\n\n"
            "### How do I configure a cursor mcp server?\n"
            "Configure your cursor mcp server by opening Cursor Settings, selecting MCP, and registering your stdio command in under 30 seconds.\n\n"
            "### What performance gains can developers expect?\n"
            "Teams typically see a 65% reduction in latency and save over $0.40 per 100 turns in context costs.\n\n"
            "<script type=\"application/ld+json\">\n"
            "{\n"
            "  \"@context\": \"https://schema.org\",\n"
            "  \"@type\": \"TechArticle\",\n"
            "  \"headline\": \"Optimizing Cursor MCP Server Performance\",\n"
            "  \"description\": \"Comprehensive guide to optimizing cursor mcp server performance.\"\n"
            "}\n"
            "</script>\n"
            "<script type=\"application/ld+json\">\n"
            "{\n"
            "  \"@context\": \"https://schema.org\",\n"
            "  \"@type\": \"FAQPage\",\n"
            "  \"mainEntity\": [\n"
            "    {\n"
            "      \"@type\": \"Question\",\n"
            "      \"name\": \"How do I configure a cursor mcp server?\",\n"
            "      \"acceptedAnswer\": {\"@type\": \"Answer\", \"text\": \"Register stdio command in Cursor Settings.\"}\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "</script>\n"
        )
        # Pad with substantive practitioner text to comfortably exceed 600 words
        filler = (
            "\n\n## Long-Term Maintenance and Reliability Invariants\n"
            "When operating coding agents at scale, reliability depends on strict boundary isolation. "
            "Every tool invocation must be idempotent, predictable, and isolated from external mutable state. "
            "Teams that adhere to these invariants maintain high deployment velocity without regressions. "
            "Developers report saving 4 hours per week when agent tool execution runs deterministically. "
            "Always verify that your process tokens and environment variables remain encrypted in storage. "
            "Avoid committing unpinned packages or raw shell access scripts to version control repositories. "
            "Regularly audit registered endpoints to ensure compliance with least privilege principles. "
            "By systematically pruning unused capabilities and monitoring execution traces, teams achieve 99.9% uptime.\n\n"
            "## Practical Monitoring and Verification Strategies\n"
            "Continuous verification prevents silent regression in automated agent pipelines. "
            "Implement synthetic queries every hour to measure response latency and detect anomalous schema diffs. "
            "When downstream tools update their parameter definitions, automated contract tests should catch breaking changes before deployment. "
            "Logging granular execution metrics allows engineering leads to pinpoint bottlenecks in multi-agent workflows. "
            "Adhering to these operational disciplines ensures sustainable scalability across growing engineering organizations. "
            "Regular audits guarantee that every tool call delivers verifiable information gain without compounding latency debt across sessions."
        )
        full_post = post + filler
        res = audit_document(full_post, target_keyword="cursor mcp server")
        self.assertTrue(res["anti_slop"]["passed"])
        self.assertTrue(res["seo_and_structure"]["passed"])
        self.assertTrue(res["publish_ready"])
        self.assertGreaterEqual(res["overall_score"], 90)

    def test_contrast_recommendation(self):
        """Test lightness fix calculation for low-contrast color pair."""
        # Failing low contrast pair: #7D93B0 on #EEF2F7 (~2.7:1)
        fg = parse_color("#7D93B0")
        bg = parse_color("#EEF2F7")
        self.assertLess(wcag_contrast_ratio(fg, bg), 4.5)

        # Recommended fix should achieve >= 4.5:1
        fixed = recommend_lightness_fix(fg, bg, target_ratio=4.5)
        self.assertIsNotNone(fixed)
        self.assertGreaterEqual(wcag_contrast_ratio(fixed, bg), 4.5)

    def test_audit_ui_craft(self):
        """Test Aperture static UI craft auditor for violations."""
        bad_ui = """
        <div className="flex h-screen bg-white">
            <button className="outline-none transition-all from-purple-600 to-indigo-600">
                <svg className="w-4 h-4" />
            </button>
            <div className="flex truncate">
                <span onPaste={(e) => e.preventDefault()}>🚀 User — Plan</span>
            </div>
            <div onClick={() => {}}>Unsafe click</div>
            <div className="bg-[#000000]">Pitch black box</div>
            <img src="avatar.png" alt="User" />
        </div>
        """
        findings = audit_content(bad_ui, "bad_component.tsx")
        rules = [f["rule"] for f in findings]

        self.assertIn("viewport-stability", rules)
        self.assertIn("accessible-focus-ring", rules)
        self.assertIn("composited-transitions", rules)
        self.assertIn("anti-slop-lila-gradient", rules)
        self.assertIn("prevent-paste-blocking", rules)
        self.assertIn("accessible-icon-button", rules)
        self.assertIn("ban-raw-emoji-icons", rules)
        self.assertIn("flex-child-truncation", rules)
        self.assertIn("image-dimensions-cls", rules)
        self.assertIn("ban-em-dash-tell", rules)
        self.assertIn("accessible-click-handler", rules)
        self.assertIn("ban-pure-pitch-black", rules)

        clean_ui = """
        <div className="flex min-h-[100dvh] bg-neutral-950">
            <button
                aria-label="Open menu"
                className="focus-visible:ring-2 focus-visible:ring-emerald-500 transition-colors bg-neutral-900"
            >
                <svg className="w-4 h-4" aria-hidden="true" />
            </button>
            <div className="flex min-w-0">
                <span className="truncate">Active User</span>
            </div>
            <img src="avatar.png" alt="User portrait" width="48" height="48" />
        </div>
        """
        clean_findings = audit_content(clean_ui, "clean_component.tsx")
        self.assertEqual(len(clean_findings), 0)

        # Edge Case 1: Multi-line JSX tag with arrow function in onClick
        multiline_bad = """
        <div
            className="card"
            onClick={() => handleSelect()}
        >
            Select Item
        </div>
        """
        bad_res = audit_content(multiline_bad, "bad_multiline.tsx")
        self.assertIn("accessible-click-handler", [f["rule"] for f in bad_res])

        # Edge Case 2: Multi-line JSX tag with role="button" and onKeyDown (accessible)
        multiline_good = """
        <div
            className="card"
            onClick={() => handleSelect()}
            role="button"
            onKeyDown={(e) => handleKey(e)}
        >
            Select Item
        </div>
        """
        good_res = audit_content(multiline_good, "good_multiline.tsx")
        self.assertNotIn("accessible-click-handler", [f["rule"] for f in good_res])

        # Edge Case 3: Image with substring collisions (e.g. shadow-sm, each-item, alt="A filling meal")
        tricky_img = '<img src="/test.png" className="shadow-sm each-item" alt="A filling meal" />'
        img_res = audit_content(tricky_img, "tricky_img.tsx")
        self.assertIn("image-dimensions-cls", [f["rule"] for f in img_res])

        # Edge Case 4: Comments with em-dashes and emojis (no false positives)
        comment_code = """
        /*
          Block comment describing system — with em-dash and 🚀
        */
        <!-- HTML comment — note with 🚀 -->
        // Line comment — with 🚀
        <div className="p-4">Content</div>
        """
        comment_res = audit_content(comment_code, "comment.tsx")
        self.assertEqual(len(comment_res), 0)

        # Edge Case 5: Custom icon library button without aria-label
        icon_lib_btn = '<button className="p-2" onClick={() => setOpen(true)}><X size={16} /></button>'
        icon_res = audit_content(icon_lib_btn, "icon_btn.tsx")
        self.assertIn("accessible-icon-button", [f["rule"] for f in icon_res])

        # Edge Case 6: APCA identical color zero contrast
        identical_apca = apca_contrast((128, 128, 128), (128, 128, 128))
        self.assertEqual(identical_apca, 0.0)

        # Edge Case 7: parse_color supports rgba, 4-digit hex, 8-digit hex, named colors
        self.assertEqual(parse_color("#fff"), (255, 255, 255))
        self.assertEqual(parse_color("#ffff"), (255, 255, 255))
        self.assertEqual(parse_color("#ffffff80"), (255, 255, 255))
        self.assertEqual(parse_color("rgba(10, 20, 30, 0.5)"), (10, 20, 30))
        self.assertEqual(parse_color("white"), (255, 255, 255))
        self.assertEqual(parse_color("black"), (0, 0, 0))


if __name__ == "__main__":
    unittest.main()



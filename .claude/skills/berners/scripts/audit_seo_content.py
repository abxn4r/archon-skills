#!/usr/bin/env python3
"""
Berners Deterministic SEO, GEO & Anti-AI Content Auditor
Zero external dependencies. Enforces Stop-Slop de-slopping rules,
Google Information Gain metrics, and AEO/GEO passage indexing standards.

Usage:
    python audit_seo_content.py draft.md --keyword "cursor mcp server"
    python audit_seo_content.py draft.md --json
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple


BANNED_DASHES = [
    ("\u2014", "Em-dash (—) detected. Replace with a period, comma, colon, or parentheses."),
    ("\u2013", "En-dash (–) detected. Replace with a standard ASCII hyphen or restructure."),
    (" -- ", "Spaced double hyphen (' -- ') detected. Use clean punctuation."),
]

SMART_QUOTES = [
    ("\u201c", "Smart opening double quote (“) detected. Use straight quote (\")."),
    ("\u201d", "Smart closing double quote (”) detected. Use straight quote (\")."),
    ("\u2018", "Smart opening single quote (‘) detected. Use straight quote (')."),
    ("\u2019", "Smart closing single quote (’) detected. Use straight quote (')."),
]

BANNED_AI_WORDS = [
    "delve", "tapestry", "game-changer", "seamless", "seamlessly",
    "elevate", "leverage", "robust", "testament", "pivotal", "vibrant",
    "myriad", "plethora", "foster", "facilitate", "harness", "beacon",
    "revolutionize", "crucial", "furthermore", "moreover", "at its core",
    "deep dive", "transformative", "ever-evolving", "rich tapestry",
    "nestled in", "serves as a reminder", "stands as a testament"
]

THROAT_CLEARING_PATTERNS = [
    r"\bhere'?s the thing\b",
    r"\bin today'?s (?:fast-paced|digital|modern) world\b",
    r"\blet'?s dive in\b",
    r"\blet'?s break this down\b",
    r"\bit turns out\b",
    r"\bthe truth is\b",
    r"\bwithout further ado\b",
    r"\bit is (?:important|worth) (?:to note|noting)\b",
    r"\bin a world where\b",
    r"\bat the end of the day\b",
    r"\bmake no mistake\b",
    r"\blet that sink in\b",
    r"\bwhether you'?re a .* or a .*\b",
]

BINARY_CONTRAST_PATTERNS = [
    r"\bnot because\b.*?\bbut because\b",
    r"\bnot just\b.*?\bbut (?:also)?\b",
    r"\bisn'?t the problem\b.*?\bis\b",
    r"\bit'?s not (?:about|just)\b.*?\bit'?s\b",
    r"\bnot an? .*?, not an? .*?, a \b",
]

EMPTY_ADVERBS = [
    "literally", "genuinely", "honestly", "actually",
    "simply", "fundamentally", "inherently", "inevitably"
]


def extract_metadata_and_body(content: str) -> Tuple[Dict[str, str], str]:
    """Parse frontmatter or top markdown metadata if present."""
    metadata = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip().lower()] = v.strip().strip('"\'')

    # Also search for standard metadata fields in body
    meta_desc_match = re.search(r"(?:meta description|description):\s*([^\n]+)", content, re.IGNORECASE)
    if meta_desc_match and "meta_description" not in metadata:
        metadata["meta_description"] = meta_desc_match.group(1).strip().strip('"\'')

    seo_title_match = re.search(r"(?:seo title|title):\s*([^\n]+)", content, re.IGNORECASE)
    if seo_title_match and "seo_title" not in metadata:
        metadata["seo_title"] = seo_title_match.group(1).strip().strip('"\'')

    return metadata, body


def strip_fenced_code(text: str) -> str:
    """Remove triple-backtick fenced code blocks, replacing with newlines to preserve line structure."""
    return re.sub(r"```[\s\S]*?```", "\n", text)


def strip_code_and_markup(text: str) -> str:
    """
    Strip fenced code blocks, HTML script/style tags, inline code,
    and HTML tags for prose anti-slop and readability evaluation.
    """
    # 1. Strip fenced code blocks
    cleaned = re.sub(r"```[\s\S]*?```", "\n", text)
    # 2. Strip HTML scripts and styles (e.g. JSON-LD schemas)
    cleaned = re.sub(r"<script[\s\S]*?</script>", "\n", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<style[\s\S]*?</style>", "\n", cleaned, flags=re.IGNORECASE)
    # 3. Strip HTML comments
    cleaned = re.sub(r"<!--[\s\S]*?-->", " ", cleaned)
    # 4. Strip inline code `...`
    cleaned = re.sub(r"`[^`\n]+`", " ", cleaned)
    # 5. Strip remaining HTML tags
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return cleaned


def audit_anti_slop(text: str) -> Dict[str, Any]:
    """Check text against all anti-AI stop-slop rules."""
    findings = []
    # Strip code blocks, inline code, and markup so only human prose is analyzed
    prose = strip_code_and_markup(text)
    prose_lower = prose.lower()

    # 1. Banned Dashes
    for char, msg in BANNED_DASHES:
        count = prose.count(char)
        if count > 0:
            findings.append({
                "type": "banned_character",
                "severity": "CRITICAL",
                "message": f"{msg} (Found {count} occurrences)",
                "count": count,
            })

    # 2. Smart Quotes
    for char, msg in SMART_QUOTES:
        count = prose.count(char)
        if count > 0:
            findings.append({
                "type": "smart_quotes",
                "severity": "WARNING",
                "message": f"{msg} (Found {count} occurrences)",
                "count": count,
            })

    # 3. Banned AI Words
    found_banned_words = []
    for word in BANNED_AI_WORDS:
        pattern = r"\b" + re.escape(word) + r"\b"
        matches = re.findall(pattern, prose_lower)
        if matches:
            found_banned_words.append((word, len(matches)))
            findings.append({
                "type": "banned_ai_vocabulary",
                "severity": "HIGH",
                "word": word,
                "count": len(matches),
                "message": f"Banned AI vocabulary '{word}' found {len(matches)} time(s). Replace with plain, concrete language.",
            })

    # 4. Throat-Clearing Openers
    for pattern in THROAT_CLEARING_PATTERNS:
        matches = re.findall(pattern, prose_lower)
        if matches:
            findings.append({
                "type": "throat_clearing",
                "severity": "HIGH",
                "count": len(matches),
                "message": f"Throat-clearing opener detected: '{matches[0]}'. State the point directly.",
            })

    # 5. Binary Contrasts
    for pattern in BINARY_CONTRAST_PATTERNS:
        matches = re.findall(pattern, prose_lower)
        if matches:
            findings.append({
                "type": "binary_contrast",
                "severity": "HIGH",
                "count": len(matches),
                "message": f"Formulaic binary contrast detected: '{matches[0]}'. State the assertion directly without theatrical negation.",
            })

    # 6. Empty Adverbs
    for adv in EMPTY_ADVERBS:
        pattern = r"\b" + re.escape(adv) + r"\b"
        matches = re.findall(pattern, prose_lower)
        if len(matches) > 1:  # Allow 1 rare occurrence, flag repetition
            findings.append({
                "type": "empty_adverb",
                "severity": "WARNING",
                "count": len(matches),
                "message": f"Overused empty adverb/hedge '{adv}' found {len(matches)} times. Remove.",
            })

    # 7. Burstiness & Metronomic Cadence Check
    # Extract plain sentences from prose
    cleaned = re.sub(r"#+.*", "", prose)
    sentences = [s.strip() for s in re.split(r"[.!?]+", cleaned) if len(s.strip()) > 5]
    sentence_lengths = [len(s.split()) for s in sentences if len(s.split()) > 2]

    metronomic_runs = 0
    if len(sentence_lengths) >= 3:
        for i in range(len(sentence_lengths) - 2):
            l1, l2, l3 = sentence_lengths[i], sentence_lengths[i+1], sentence_lengths[i+2]
            if abs(l1 - l2) <= 2 and abs(l2 - l3) <= 2 and 12 <= l1 <= 24:
                metronomic_runs += 1

    if metronomic_runs > 2:
        findings.append({
            "type": "metronomic_cadence",
            "severity": "WARNING",
            "count": metronomic_runs,
            "message": f"Detected {metronomic_runs} sequences of 3+ consecutive sentences with identical length (12-24 words). Inject short 3-5 word sentences to increase burstiness.",
        })

    # Score calculation
    crit_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in findings if f["severity"] == "HIGH")
    warn_count = sum(1 for f in findings if f["severity"] == "WARNING")

    score = max(0, 100 - (crit_count * 30 + high_count * 12 + warn_count * 4))

    return {
        "score": score,
        "passed": crit_count == 0 and high_count == 0,
        "critical_count": crit_count,
        "high_count": high_count,
        "warning_count": warn_count,
        "findings": findings,
    }


def audit_seo_and_structure(text: str, metadata: Dict[str, str], target_keyword: str = "") -> Dict[str, Any]:
    """Check SEO, AEO, and passage indexing structure."""
    findings = []
    text_lower = text.lower()
    kw_lower = target_keyword.lower().strip() if target_keyword else ""

    # Strip fenced code blocks before heading extraction and structural checks
    no_code_text = strip_fenced_code(text)

    # 1. H1 Check
    h1_matches = re.findall(r"^#\s+([^\n]+)", no_code_text, re.MULTILINE)
    if not h1_matches:
        # Check metadata for title
        if "title" in metadata:
            h1_title = metadata["title"]
        else:
            h1_title = None
            findings.append({
                "type": "missing_h1",
                "severity": "CRITICAL",
                "message": "Missing H1 title tag in markdown (# Title).",
            })
    else:
        h1_title = h1_matches[0]
        if len(h1_matches) > 1:
            findings.append({
                "type": "multiple_h1",
                "severity": "HIGH",
                "message": f"Found {len(h1_matches)} H1 headings. A page must have exactly one H1.",
            })

    if h1_title:
        if len(h1_title) > 70:
            findings.append({
                "type": "overlong_h1",
                "severity": "WARNING",
                "message": f"H1 title is {len(h1_title)} characters long (target: 45-65 characters).",
            })
        if kw_lower and kw_lower not in h1_title.lower():
            findings.append({
                "type": "keyword_missing_h1",
                "severity": "HIGH",
                "message": f"Target keyword '{target_keyword}' is missing from H1 title.",
            })

    # 2. Meta Description
    meta_desc = metadata.get("meta_description") or metadata.get("description")
    if not meta_desc:
        findings.append({
            "type": "missing_meta_description",
            "severity": "HIGH",
            "message": "Missing Meta Description. Provide 120-160 character description.",
        })
    else:
        desc_len = len(meta_desc)
        if desc_len < 110 or desc_len > 165:
            findings.append({
                "type": "meta_description_length",
                "severity": "WARNING",
                "message": f"Meta Description length is {desc_len} chars (target: 120-160 characters).",
            })
        if kw_lower and kw_lower not in meta_desc.lower():
            findings.append({
                "type": "keyword_missing_meta",
                "severity": "HIGH",
                "message": f"Target keyword '{target_keyword}' missing from Meta Description.",
            })

    # 3. Direct Answer / BLUF Block
    first_300_words = " ".join(no_code_text.split()[:300]).lower()
    has_bluf = any(indicator in first_300_words for indicator in [
        "tl;dr", "in short", "summary", "key takeaway", "bottom line", "quick answer"
    ]) or (h1_title and len(text.split()) > 150 and any(
        kw in " ".join(text.split()[:120]).lower() for kw in ([kw_lower] if kw_lower else ["is", "allows", "enables"])
    ))

    if not has_bluf:
        findings.append({
            "type": "missing_direct_answer",
            "severity": "HIGH",
            "message": "No clear direct answer, TL;DR, or summary block in the opening 150 words (AEO requirement).",
        })

    # 4. H2 Heading Structure & Assertiveness
    h2_matches = re.findall(r"^##\s+([^\n]+)", no_code_text, re.MULTILINE)
    if len(h2_matches) < 2:
        findings.append({
            "type": "insufficient_h2",
            "severity": "HIGH",
            "message": f"Found only {len(h2_matches)} H2 heading(s). Long-form content requires structured H2 sections.",
        })
    else:
        # Check for vague 1-word headings
        for h2 in h2_matches:
            words = h2.split()
            if len(words) <= 1 and words[0].lower() not in ["conclusion", "faq", "faqs"]:
                findings.append({
                    "type": "vague_h2",
                    "severity": "WARNING",
                    "heading": h2,
                    "message": f"H2 heading '{h2}' is a vague label. Use assertive thesis headings that state a complete proposition.",
                })

    # 5. Information Gain & Quantitative Metrics
    # Count numbers with units (e.g., 30s, $0.61, 47%, 12ms, 5 pages)
    metric_matches = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|ms|s|sec|seconds?|minutes?|hours?|kb|mb|gb|px|rem|\$|usd|users?|clients?|pages?|tokens?)\b", text_lower)
    if len(metric_matches) < 3:
        findings.append({
            "type": "low_data_density",
            "severity": "WARNING",
            "count": len(metric_matches),
            "message": f"Found only {len(metric_matches)} quantitative metrics with units. Princeton KDD '24 benchmark shows adding specific statistics yields +41% AI visibility.",
        })

    # 6. Structured Schema Markup (JSON-LD)
    has_schema = "application/ld+json" in text or '"@context": "https://schema.org"' in text
    has_faq_schema = "faqpage" in text_lower or '"@type": "faqpage"' in text_lower
    if not has_schema:
        findings.append({
            "type": "missing_jsonld_schema",
            "severity": "HIGH",
            "message": "Missing JSON-LD structured data schema (TechArticle/BlogPosting and FAQPage).",
        })
    elif not has_faq_schema and any(q in text_lower for q in ["faq", "frequently asked questions"]):
        findings.append({
            "type": "missing_faq_schema",
            "severity": "WARNING",
            "message": "Content includes FAQ text but is missing matching FAQPage JSON-LD schema.",
        })

    # 7. Word Count
    total_words = len(text.split())
    if total_words < 600:
        findings.append({
            "type": "thin_content",
            "severity": "HIGH",
            "count": total_words,
            "message": f"Total word count ({total_words} words) is below comprehensive topical coverage floor (600+ words).",
        })

    # Score calculation
    crit_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in findings if f["severity"] == "HIGH")
    warn_count = sum(1 for f in findings if f["severity"] == "WARNING")

    score = max(0, 100 - (crit_count * 30 + high_count * 15 + warn_count * 5))

    return {
        "score": score,
        "word_count": total_words,
        "h1_title": h1_title,
        "h2_count": len(h2_matches),
        "metrics_found": len(metric_matches),
        "has_schema": has_schema,
        "passed": crit_count == 0 and high_count == 0,
        "findings": findings,
    }


def audit_document(content: str, target_keyword: str = "") -> Dict[str, Any]:
    """Execute complete Berners content audit suite."""
    metadata, body = extract_metadata_and_body(content)
    anti_slop = audit_anti_slop(body)
    seo_struct = audit_seo_and_structure(content, metadata, target_keyword)

    overall_score = round((anti_slop["score"] * 0.5) + (seo_struct["score"] * 0.5))
    is_publish_ready = anti_slop["passed"] and seo_struct["passed"] and overall_score >= 80

    return {
        "overall_score": overall_score,
        "publish_ready": is_publish_ready,
        "anti_slop": anti_slop,
        "seo_and_structure": seo_struct,
        "metadata_detected": metadata,
    }


def main():
    parser = argparse.ArgumentParser(description="Berners SEO & Anti-AI Content Auditor")
    parser.add_argument("file", help="Path to markdown or text file to audit")
    parser.add_argument("--keyword", "-k", default="", help="Target keyword to check")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    results = audit_document(content, args.keyword)

    if args.json:
        print(json.dumps(results, indent=2))
        sys.exit(0 if results["publish_ready"] else 1)

    print("=" * 65)
    print(f"       BERNERS DUAL-RETRIEVAL SEO & ANTI-SLOP AUDIT       ")
    print("=" * 65)
    print(f"File Tested         : {file_path.name}")
    print(f"Word Count          : {results['seo_and_structure']['word_count']}")
    print(f"Overall Quality     : {results['overall_score']}/100")
    print(f"Anti-AI Slop Score  : {results['anti_slop']['score']}/100")
    print(f"SEO & AEO Structure : {results['seo_and_structure']['score']}/100")
    status_str = "READY TO PUBLISH" if results["publish_ready"] else "REVISIONS REQUIRED"
    print(f"Verdict             : {status_str}")
    print("=" * 65)

    all_findings = results["anti_slop"]["findings"] + results["seo_and_structure"]["findings"]
    if not all_findings:
        print("\n[+] Perfect score! Zero AI tells, clean cadence, valid SEO/AEO structure.")
    else:
        print(f"\nDiscovered {len(all_findings)} finding(s):")
        for f in all_findings:
            sev = f.get("severity", "INFO")
            msg = f.get("message", "")
            print(f"  [{sev}] {msg}")

    print("=" * 65)
    sys.exit(0 if results["publish_ready"] else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Dijkstra Evidence & Substring Quote Verifier
Zero-dependency Python standard library implementation.

Audits review comments, status specs, and RFC documents to verify that
every quoted substring or code citation actually exists in the source codebase.
Directly combats "documentation as displacement".

Usage:
  python verify_evidence_quotes.py --quote "exact substring" --source ./src
  python verify_evidence_quotes.py --doc review.md --source ./repo
  python verify_evidence_quotes.py --test
"""

import sys
import os
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

QUOTE_PATTERN = re.compile(r'["\']([^"\'\n]{6,120})["\']|`([^`\n]{4,80})`')


def extract_quotes(text: str) -> List[str]:
    quotes = []
    for m in QUOTE_PATTERN.finditer(text):
        q = m.group(1) or m.group(2)
        if q and len(q.strip()) >= 6:
            q_clean = q.strip()
            if not q_clean.startswith("http"):
                quotes.append(q_clean)
    return list(dict.fromkeys(quotes))


def search_in_source(quote: str, source_path: Path) -> List[Tuple[str, int, str]]:
    matches = []
    if source_path.is_file():
        files = [source_path]
    else:
        files = [
            p
            for p in source_path.glob("**/*")
            if p.is_file()
            and not any(
                part in (".git", ".svn", "__pycache__", "node_modules", "vendor")
                for part in p.parts
            )
        ]

    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if quote in content:
                for line_no, line in enumerate(content.splitlines(), 1):
                    if quote in line:
                        matches.append((str(f), line_no, line.strip()))
        except Exception:
            continue
    return matches


def run_verification(doc_text: str, source_path: Path, explicit_quote: Optional[str] = None) -> int:
    if explicit_quote:
        quotes = [explicit_quote.strip()]
    else:
        quotes = extract_quotes(doc_text)

    print("=" * 70)
    print("          DIJKSTRA EVIDENCE & SUBSTRING QUOTATION VERIFIER          ")
    print("=" * 70)
    print(f"Source Target        : {source_path}")
    print(f"Extracted Quotations : {len(quotes)}")
    print()

    if not quotes:
        print("[INFO] No quoted phrases or citations found in target.")
        return 0

    verified_count = 0
    discrepancy_count = 0

    for idx, q in enumerate(quotes, 1):
        found = search_in_source(q, source_path)
        if found:
            verified_count += 1
            src_file, lno, snippet = found[0]
            print(f'[{idx}] [VERIFIED] "{q}"')
            print(f"    Found in: {src_file}:{lno}")
            print(f"    Line    : {snippet[:90]}")
        else:
            discrepancy_count += 1
            print(f'[{idx}] [DISCREPANCY] "{q}"')
            print("    [!] Quote NOT found in target source files. Check for citation drift.")
        print()

    print("=" * 70)
    print(f"SUMMARY: {verified_count} Verified | {discrepancy_count} Discrepancies")
    if discrepancy_count > 0:
        print("[WARNING] Unverified citations detected. Verify artifacts on disk.")
        return 1
    print("[SUCCESS] All evidence citations verified verbatim.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Dijkstra Evidence & Substring Quote Verifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--source", default=".", help="Root directory of codebase to search within (default: .)")
    parser.add_argument("--doc", default=None, help="Markdown document containing citations/quotes to audit")
    parser.add_argument("--quote", default=None, help="Specific quote to verify")
    parser.add_argument("--test", action="store_true", help="Run self-test on current script")

    args = parser.parse_args()

    if args.test:
        print("[TEST] Running self-test on verify_evidence_quotes.py...")
        self_path = Path(__file__).resolve()
        test_quote = "Dijkstra Evidence & Substring Quote Verifier"
        found = search_in_source(test_quote, self_path)
        if found:
            print(f"[TEST PASS] Successfully verified self-quote at line {found[0][1]}.")
            return 0
        else:
            print("[TEST FAIL] Failed to find self-quote.")
            return 1

    source_path = Path(args.source).resolve()
    if not source_path.exists():
        print(f"[ERROR] Source path does not exist: {source_path}", file=sys.stderr)
        return 1

    doc_text = ""
    if args.doc:
        doc_path = Path(args.doc).resolve()
        if not doc_path.exists():
            print(f"[ERROR] Document does not exist: {doc_path}", file=sys.stderr)
            return 1
        doc_text = doc_path.read_text(encoding="utf-8", errors="ignore")

    return run_verification(doc_text, source_path, explicit_quote=args.quote)


if __name__ == "__main__":
    sys.exit(main())

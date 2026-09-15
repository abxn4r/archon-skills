#!/usr/bin/env python3
"""
Caples Copywriting & Tone Analyzer
Flesch-Kincaid Readability + AI Cliché / Buzzword Linter
Zero-dependency Python standard library implementation.

Usage:
  python analyze_copy.py --text "Our cutting-edge platform allows you to seamlessly leverage AI."
  python analyze_copy.py --file README.md
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CLICHE_PATTERNS = [
    (r"\bdelve\b", "AI Cliché: 'delve' -- replace with direct action verb"),
    (r"\bgame-?changer\b", "Buzzword: 'game-changer' -- state concrete improvement instead"),
    (r"\btapestry\b", "AI Cliché: 'tapestry' -- inflated symbolism"),
    (r"\bunleash\b", "AI Cliché: 'unleash' -- hyperbolic framing"),
    (r"\bleverage\b", "Corporate Buzzword: 'leverage' -- replace with use/apply/harness"),
    (r"\bseamless(ly)?\b", "Vague Cliché: 'seamless' -- explain how it actually integrates"),
    (r"\belevate\b", "AI Cliché: 'elevate' -- vague promotional verb"),
    (r"\bcutting-?edge\b", "Empty Buzzword: 'cutting-edge' -- state exact technical spec"),
    (r"\btestament\b", "AI Cliché: 'testament to' -- wordy abstraction"),
    (r"\brealm\b", "AI Cliché: 'in the realm of' -- replace with 'in' or specify domain"),
    (r"\bpivotal\b", "Overused Cliché: 'pivotal'"),
    (r"\bin today'?s (fast-paced|digital) world\b", "Trite Opener: delete entire phrase"),
    (r"\brevolutionize\b", "Hyperbole: 'revolutionize' -- show actual benchmark change"),
    (r"\bdive deep\b", "Cliché: 'dive deep' -- replace with examine/audit/analyze"),
    (r"\bbeacon\b", "AI Cliché: 'beacon of'"),
    (r"\bparamount\b", "Stiff formality: 'paramount' -- replace with critical or essential"),
]

PASSIVE_REGEX = re.compile(r"\b(is|are|was|were|been|be|being)\s+([a-z]+ed)\b", re.I)


def count_syllables(word: str) -> int:
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    matches = re.findall(r'[aeiouy]{1,2}', word)
    return max(1, len(matches))


def analyze(text: str) -> Dict[str, Any]:
    # Sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = max(1, len(sentences))

    # Words
    words = re.findall(r"\b[a-zA-Z0-9'-]+\b", text)
    word_count = max(1, len(words))

    # Syllables
    syllables = sum(count_syllables(w) for w in words)

    # Readability formulas
    asl = word_count / sentence_count
    asw = syllables / word_count

    flesch_ease = 206.835 - (1.015 * asl) - (84.6 * asw)
    fk_grade = (0.39 * asl) + (11.8 * asw) - 15.59

    # Cliché matches
    cliche_findings = []
    for pattern, note in CLICHE_PATTERNS:
        for m in re.finditer(pattern, text, re.I):
            cliche_findings.append({"match": m.group(0), "note": note, "span": m.span()})

    # Long sentences (> 28 words)
    long_sentences = [s for s in sentences if len(s.split()) > 28]

    # Passive voice matches
    passive_matches = [m.group(0) for m in PASSIVE_REGEX.finditer(text)]

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_len": asl,
        "flesch_reading_ease": flesch_ease,
        "flesch_kincaid_grade": fk_grade,
        "cliches": cliche_findings,
        "long_sentences": long_sentences,
        "passive_instances": passive_matches,
    }


def print_report(res: Dict[str, Any]):
    print("=" * 65)
    print("              CAPLES COPYWRITING & CLICHE AUDIT              ")
    print("=" * 65)
    print(f"Total Words Analyzed        : {res['word_count']}")
    print(f"Total Sentences             : {res['sentence_count']}")
    print(f"Average Sentence Length     : {res['avg_sentence_len']:.1f} words")
    print(f"Flesch Reading Ease (0-100) : {res['flesch_reading_ease']:.1f} (Target: >60)")
    print(f"Flesch-Kincaid Grade Level  : {res['flesch_kincaid_grade']:.1f} (Target: 7-9 for B2B)")
    print()

    print("--- Cliché & Buzzword Detections ---")
    if res["cliches"]:
        for c in res["cliches"]:
            print(f"  [!] Match: '{c['match']}' -> {c['note']}")
    else:
        print("  [✓] Zero flagged AI clichés detected.")
    print()

    print("--- Long Sentences (>28 words) ---")
    if res["long_sentences"]:
        for s in res["long_sentences"][:3]:
            print(f"  [!] {s[:90]}... ({len(s.split())} words)")
    else:
        print("  [✓] All sentences within readable length bounds.")
    print()

    print("--- Passive Voice Instances ---")
    if res["passive_instances"]:
        print(f"  [-] {len(res['passive_instances'])} passive constructions found: {', '.join(res['passive_instances'][:5])}")
    else:
        print("  [✓] Active voice maintained.")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(
        description="Caples Copywriting & AI Cliché Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", help="Text string to analyze")
    parser.add_argument("--file", help="Path to text or markdown file to analyze")

    args = parser.parse_args()

    content = ""
    if args.text:
        content = args.text
    elif args.file:
        p = Path(args.file).resolve()
        if not p.exists():
            print(f"[ERROR] File not found: {p}", file=sys.stderr)
            return 1
        content = p.read_text(encoding="utf-8", errors="ignore")
    else:
        parser.print_help()
        return 1

    res = analyze(content)
    print_report(res)
    return 1 if res["cliches"] else 0


if __name__ == "__main__":
    sys.exit(main())

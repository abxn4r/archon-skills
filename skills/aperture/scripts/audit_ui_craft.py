#!/usr/bin/env python3
"""
Aperture UI Craft & Anti-Slop Static Auditor
Zero-dependency Python standard library implementation.

Audits UI files (HTML, JSX, TSX, Vue, Svelte, CSS) against:
- Anti-AI Slop Rules (purple gradients, scale(0), h-screen)
- WCAG 2.2 & A11y Invariants (icon button aria-labels, outline:none without focus)
- Layout Stability (min-w-0 on flex truncation, explicit img dimensions)
- Compositor Performance (transition: all, non-composited animations)
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Comprehensive emoji detection regex range
EMOJI_PATTERN = re.compile(
    r"[\U0001F1E0-\U0001F1FF"  # flags
    r"\U0001F300-\U0001F5FF"  # symbols & pictographs
    r"\U0001F600-\U0001F64F"  # emoticons
    r"\U0001F680-\U0001F6FF"  # transport & map
    r"\U0001F700-\U0001F77F"  # alchemical symbols
    r"\U0001F780-\U0001F7FF"  # geometric shapes
    r"\U0001F800-\U0001F8FF"  # arrows
    r"\U0001F900-\U0001F9FF"  # supplemental symbols
    r"\U0001FA00-\U0001FA6F"  # chess, symbols
    r"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
    r"\U00002702-\U000027B0"  # dingbats
    r"\U000024C2-\U0001F251"
    r"]+",
    flags=re.UNICODE,
)


def mask_comments(content: str) -> str:
    """Mask block, html, and line comments with whitespace preserving line and column offsets."""
    def replacer(match):
        s = match.group(0)
        return "".join("\n" if c == "\n" else " " for c in s)

    # 1. Block comments /* ... */
    res = re.sub(r"/\*.*?\*/", replacer, content, flags=re.DOTALL)
    # 2. HTML comments <!-- ... -->
    res = re.sub(r"<!--.*?-->", replacer, res, flags=re.DOTALL)
    # 3. Line comments // ...
    res = re.sub(r"//[^\n]*", replacer, res)
    return res


def find_jsx_tags(content: str, target_tags: set) -> List[Tuple[str, str, int, int]]:
    """Extract opening JSX/HTML tags and their full attributes preserving brace/quote boundaries."""
    i = 0
    n = len(content)
    results = []

    while i < n:
        if content[i] == '<':
            start = i
            i += 1
            if i < n and content[i] in ('/', '!', '?'):
                i += 1
                continue
            name_start = i
            while i < n and (content[i].isalnum() or content[i] in "-_"):
                i += 1
            tag_name = content[name_start:i]

            if tag_name.lower() in target_tags:
                attrs_start = i
                brace_depth = 0
                in_quote = None
                while i < n:
                    ch = content[i]
                    if in_quote:
                        if ch == '\\' and i + 1 < n:
                            i += 2
                            continue
                        elif ch == in_quote:
                            in_quote = None
                    else:
                        if ch in ('"', "'", '`'):
                            in_quote = ch
                        elif ch == '{':
                            brace_depth += 1
                        elif ch == '}':
                            brace_depth = max(0, brace_depth - 1)
                        elif ch == '>' and brace_depth == 0:
                            break
                    i += 1
                attrs = content[attrs_start:i]
                results.append((tag_name, attrs, start, i))
        i += 1
    return results


def audit_content(content: str, filename: str = "<stdin>") -> List[Dict[str, Any]]:
    """Scan string content for UI craft violations and anti-patterns."""
    findings = []
    lines = content.splitlines()
    masked_content = mask_comments(content)
    masked_lines = masked_content.splitlines()

    for idx, line in enumerate(lines, 1):
        # 1. Viewport Stability: h-screen creates layout jumps on mobile Safari
        if "h-screen" in line and not "min-h-[100dvh]" in line:
            findings.append({
                "rule": "viewport-stability",
                "severity": "HIGH",
                "file": filename,
                "line": idx,
                "message": "Use of 'h-screen' causes mobile browser layout jumping. Replace with 'min-h-[100dvh]' or 'h-[100dvh]'.",
                "snippet": line.strip(),
            })

        # 2. Outline None without Focus-Visible replacement
        if re.search(r"\boutline-none\b", line) or re.search(r"outline\s*:\s*none", line):
            if "focus-visible" not in line and ":focus-visible" not in line and "ring-" not in line:
                findings.append({
                    "rule": "accessible-focus-ring",
                    "severity": "CRITICAL",
                    "file": filename,
                    "line": idx,
                    "message": "Removing outline without an explicit ':focus-visible' replacement breaks keyboard navigation.",
                    "snippet": line.strip(),
                })

        # 3. Compositor Performance: transition: all animates layout properties off-GPU
        if re.search(r"\btransition-all\b", line) or re.search(r"transition\s*:\s*all\b", line):
            findings.append({
                "rule": "composited-transitions",
                "severity": "MEDIUM",
                "file": filename,
                "line": idx,
                "message": "'transition: all' triggers expensive style recalculations and layout recalculations. Animate transform and opacity explicitly.",
                "snippet": line.strip(),
            })

        # 4. Physicality & Origin: scale(0) is physically unnatural
        if re.search(r"\bscale\(0\)", line) or re.search(r"\bscale-0\b", line):
            findings.append({
                "rule": "unnatural-scale-origin",
                "severity": "MEDIUM",
                "file": filename,
                "line": idx,
                "message": "Scale from 0 is physically unnatural. Animate entrance from scale(0.95) with opacity: 0 instead.",
                "snippet": line.strip(),
            })

        # 5. Anti-AI Slop: The Lila Ban (generic AI purple/blue gradient buttons)
        if re.search(r"from-purple-\d+.*to-(?:indigo|blue|pink)-\d+", line) or re.search(r"from-violet-\d+.*to-fuchsia-\d+", line):
            findings.append({
                "rule": "anti-slop-lila-gradient",
                "severity": "MEDIUM",
                "file": filename,
                "line": idx,
                "message": "Generic AI purple/violet gradient detected. Use neutral surface with a single purposeful accent.",
                "snippet": line.strip(),
            })

        # 6. Paste blocking: prevents users and password managers from pasting
        if "onPaste" in line and "preventDefault" in line:
            findings.append({
                "rule": "prevent-paste-blocking",
                "severity": "CRITICAL",
                "file": filename,
                "line": idx,
                "message": "Blocking paste in form fields harms accessibility and password manager integration (WCAG 2.2 3.3.8).",
                "snippet": line.strip(),
            })

        # 7. Unsafe Flex Truncation: truncate on flex child without min-w-0
        if ("truncate" in line or "text-ellipsis" in line) and "flex" in line and "min-w-0" not in line:
            findings.append({
                "rule": "flex-child-truncation",
                "severity": "HIGH",
                "file": filename,
                "line": idx,
                "message": "Flex child with truncation requires 'min-w-0' to prevent horizontal overflow blowout.",
                "snippet": line.strip(),
            })

        # 8. Raw Emoji in UI code / markup (evaluated on comment-masked line)
        m_line = masked_lines[idx - 1] if idx - 1 < len(masked_lines) else line
        if EMOJI_PATTERN.search(m_line):
            findings.append({
                "rule": "ban-raw-emoji-icons",
                "severity": "LOW",
                "file": filename,
                "line": idx,
                "message": "Raw emoji used in UI. Replace with high-quality SVG icon primitives (e.g. Radix, Phosphor, Lucide).",
                "snippet": line.strip(),
            })

        # 9. Em-dash and En-dash Tell in UI Copy (evaluated on comment-masked line)
        if "—" in m_line or "–" in m_line:
            findings.append({
                "rule": "ban-em-dash-tell",
                "severity": "MEDIUM",
                "file": filename,
                "line": idx,
                "message": "Em-dash (—) or en-dash (–) detected in UI copy. Use standard hyphen (-) or restructure sentence to eliminate AI crutch.",
                "snippet": line.strip(),
            })

        # 10. Pure Pitch Black Background
        if re.search(r"\b(?:bg-\[#000(?:000)?\]|background(?:-color)?\s*:\s*#000(?:000)?\b)", line):
            findings.append({
                "rule": "ban-pure-pitch-black",
                "severity": "LOW",
                "file": filename,
                "line": idx,
                "message": "Pure pitch black (#000000) background detected. Use tinted dark neutrals (e.g. #0D0E11, #09090B, zinc-950) for depth.",
                "snippet": line.strip(),
            })

    # Multi-line checks

    # 11. Click handler on non-interactive element (<div onClick> / <span onClick>) across multiple lines
    for tag_name, attrs, start_pos, end_pos in find_jsx_tags(content, {"div", "span"}):
        if re.search(r"\bonClick\b", attrs):
            has_role = bool(re.search(r'\brole\s*=\s*["\']?(?:button|link|menuitem|tab|switch|checkbox)\b', attrs, re.I))
            has_keyboard = bool(re.search(r'\b(?:onKeyDown|onKeyUp|onKeyPress)\b', attrs))
            if not has_role and not has_keyboard:
                line_num = content[:start_pos].count("\n") + 1
                findings.append({
                    "rule": "accessible-click-handler",
                    "severity": "CRITICAL",
                    "file": filename,
                    "line": line_num,
                    "message": f"Non-interactive element (<{tag_name}>) has onClick without keyboard handler or accessible role='button'. Use native <button>.",
                    "snippet": content[start_pos:end_pos + 1].splitlines()[0].strip()[:80],
                })

    # 12. Icon-only or empty button without aria-label
    for tag_name, attrs, start_pos, end_pos in find_jsx_tags(content, {"button"}):
        close_m = re.search(r"</button\s*>", content[end_pos + 1:], re.IGNORECASE)
        inner = content[end_pos + 1 : end_pos + 1 + close_m.start()].strip() if close_m else ""
        visible_text = re.sub(r"<[^>]+>", "", inner).strip()
        has_aria = bool(re.search(r'\b(?:aria-label|aria-labelledby|title)\s*=', attrs))

        if not visible_text and not has_aria:
            line_num = content[:start_pos].count("\n") + 1
            snippet_end = min(len(content), start_pos + 80)
            findings.append({
                "rule": "accessible-icon-button",
                "severity": "CRITICAL",
                "file": filename,
                "line": line_num,
                "message": "Button has no visible text or accessible name. Add 'aria-label' or visually hidden text.",
                "snippet": content[start_pos:snippet_end].replace("\n", " ") + "...",
            })

    # 13. Missing width/height on img tags (CLS risk)
    for tag_name, attrs, start_pos, end_pos in find_jsx_tags(content, {"img"}):
        has_w = bool(re.search(r'\bwidth\s*=|width\s*:|\bw-(?:\d+|\[|px|full|screen|auto)\b', attrs))
        has_h = bool(re.search(r'\bheight\s*=|height\s*:|\bh-(?:\d+|\[|px|full|screen|auto)\b', attrs))
        has_aspect = bool(re.search(r'\baspect-(?:square|video|auto|\[)|\baspect-ratio\b', attrs))
        has_fill = bool(re.search(r'(?<![-_a-zA-Z0-9])fill(?:\s*=\s*\{?\s*true|\s*(?![-_:=a-zA-Z0-9]))', attrs))
        if not ((has_w and has_h) or has_aspect or has_fill):
            line_num = content[:start_pos].count("\n") + 1
            findings.append({
                "rule": "image-dimensions-cls",
                "severity": "MEDIUM",
                "file": filename,
                "line": line_num,
                "message": "Image element lacks explicit width/height or aspect-ratio, risking Cumulative Layout Shift (CLS).",
                "snippet": content[start_pos:end_pos + 1].replace("\n", " ")[:80],
            })

    return findings


def audit_file(file_path: Path) -> List[Dict[str, Any]]:
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        return audit_content(content, str(file_path))
    except Exception as e:
        return [{
            "rule": "read-error",
            "severity": "CRITICAL",
            "file": str(file_path),
            "line": 1,
            "message": f"Could not read file: {e}",
            "snippet": "",
        }]


def main():
    parser = argparse.ArgumentParser(
        description="Aperture UI Craft & Anti-Slop Static Auditor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("targets", nargs="+", help="Files or directories to audit")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--fail-on-high", action="store_true", help="Exit with code 1 if CRITICAL or HIGH findings exist")

    args = parser.parse_args()

    all_findings = []
    extensions = {".html", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".scss"}

    for target_str in args.targets:
        target_path = Path(target_str)
        if target_path.is_file():
            all_findings.extend(audit_file(target_path))
        elif target_path.is_dir():
            for root, _, files in os.walk(target_path):
                for f in files:
                    fp = Path(root) / f
                    if fp.suffix.lower() in extensions:
                        all_findings.extend(audit_file(fp))
        else:
            print(f"[WARN] Target not found: {target_str}", file=sys.stderr)

    if args.json:
        print(json.dumps({"findings": all_findings, "total": len(all_findings)}, indent=2))
        has_blocker = any(f["severity"] in ("CRITICAL", "HIGH") for f in all_findings)
        return 1 if (args.fail_on_high and has_blocker) else 0

    print("=" * 70)
    print("  APERTURE UI CRAFT & ANTI-SLOP AUDIT REPORT")
    print("=" * 70)
    if not all_findings:
        print("  [PASS] No UI craft or accessibility violations detected.")
        print()
        return 0

    print(f"  Total findings: {len(all_findings)}\n")
    for f in all_findings:
        sev_tag = f"[{f['severity']}]"
        print(f"  {sev_tag:<10} {f['file']}:{f['line']}")
        print(f"             Rule   : {f['rule']}")
        print(f"             Issue  : {f['message']}")
        if f["snippet"]:
            print(f"             Context: {f['snippet']}")
        print()

    has_blocker = any(f["severity"] in ("CRITICAL", "HIGH") for f in all_findings)
    return 1 if (args.fail_on_high and has_blocker) else 0


if __name__ == "__main__":
    sys.exit(main())

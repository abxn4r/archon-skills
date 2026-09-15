#!/usr/bin/env python3
"""
Aperture Contrast Checker
WCAG 2.1/2.2 Relative Luminance + APCA Lightness Contrast (Lc)
Zero-dependency Python standard library implementation.

Usage:
  python check_contrast.py --fg "#EDEDED" --bg "#0D0E11"
  python check_contrast.py --preset dark
"""

import sys
import re
import argparse
from typing import Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_color(color_str: str) -> Tuple[int, int, int]:
    color_str = color_str.strip()
    if color_str.startswith("#"):
        hex_val = color_str.lstrip("#")
        if len(hex_val) == 3:
            hex_val = "".join(c * 2 for c in hex_val)
        if len(hex_val) == 6:
            try:
                return (int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16))
            except ValueError:
                raise ValueError(f"Invalid hex digits in color: {color_str}")
    match = re.match(r"^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$", color_str, re.I)
    if match:
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if all(0 <= c <= 255 for c in (r, g, b)):
            return (r, g, b)
        raise ValueError(f"RGB values must be in range 0-255: {color_str}")
    raise ValueError(f"Unsupported color format: {color_str}")


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    def srgb_to_lin(c: int) -> float:
        v = c / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = [srgb_to_lin(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag_contrast_ratio(fg_rgb: Tuple[int, int, int], bg_rgb: Tuple[int, int, int]) -> float:
    l1 = relative_luminance(fg_rgb)
    l2 = relative_luminance(bg_rgb)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def apca_contrast(txt_rgb: Tuple[int, int, int], bg_rgb: Tuple[int, int, int]) -> float:
    y_txt = relative_luminance(txt_rgb)
    y_bg = relative_luminance(bg_rgb)
    if y_bg > y_txt:
        c = (y_bg ** 0.56 - y_txt ** 0.57) * 1.14
        return c * 100.0
    else:
        c = (y_bg ** 0.65 - y_txt ** 0.62) * 1.14
        return -c * 100.0


def evaluate_pair(fg_str: str, bg_str: str, label: str = "") -> int:
    fg = parse_color(fg_str)
    bg = parse_color(bg_str)
    ratio = wcag_contrast_ratio(fg, bg)
    apca = abs(apca_contrast(fg, bg))

    aa_normal = ratio >= 4.5
    aa_large = ratio >= 3.0
    aaa_normal = ratio >= 7.0
    aaa_large = ratio >= 4.5

    header = f"Evaluating [{label}]: FG={fg_str} on BG={bg_str}" if label else f"FG={fg_str} on BG={bg_str}"
    print("=" * 60)
    print(f"  {header}")
    print("=" * 60)
    print(f"  * WCAG 2.1/2.2 Contrast Ratio : {ratio:.2f}:1")
    print(f"    - AA Normal Text (>=4.5:1)   : {'[PASS]' if aa_normal else '[FAIL]'}")
    print(f"    - AA Large Text (>=3.0:1)    : {'[PASS]' if aa_large else '[FAIL]'}")
    print(f"    - AAA Normal Text (>=7.0:1)  : {'[PASS]' if aaa_normal else '[FAIL]'}")
    print(f"    - AAA Large Text (>=4.5:1)   : {'[PASS]' if aaa_large else '[FAIL]'}")
    print(f"  * APCA Lightness Contrast (Lc) : {apca:.1f}")
    if apca >= 75:
        apca_grade = "[PASS] Preferred for Body Copy (Lc >= 75)"
    elif apca >= 60:
        apca_grade = "[PASS] Minimum for Content (Lc >= 60)"
    elif apca >= 45:
        apca_grade = "[WARN] Headlines / Large Only (Lc >= 45)"
    else:
        apca_grade = "[FAIL] Non-text elements only (Lc < 45)"
    print(f"    - Assessment                 : {apca_grade}")
    print()
    return 0 if aa_normal else 1


def main():
    parser = argparse.ArgumentParser(
        description="Aperture WCAG 2.1/2.2 & APCA Contrast Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--fg", help="Foreground color (e.g. #EDEDED, 'rgb(237,237,237)')")
    parser.add_argument("--bg", help="Background color (e.g. #0D0E11, 'rgb(13,14,17)')")
    parser.add_argument("--preset", choices=["dark", "light", "linear"], help="Audit standard color preset")

    args = parser.parse_args()

    if args.preset == "dark" or args.preset == "linear":
        evaluate_pair("#EDEDED", "#0D0E11", "Linear Dark Base / Primary Text")
        evaluate_pair("#8A8F98", "#0D0E11", "Linear Dark Base / Muted Secondary Text")
        evaluate_pair("#5E6AD2", "#0D0E11", "Linear Accent Indigo / Dark Base")
        return 0
    elif args.preset == "light":
        evaluate_pair("#111827", "#FFFFFF", "Clean Light Base / Primary Text")
        evaluate_pair("#6B7280", "#FFFFFF", "Clean Light Base / Secondary Text")
        evaluate_pair("#4F46E5", "#FFFFFF", "Primary Accent / Light Base")
        return 0

    if not args.fg or not args.bg:
        parser.print_help()
        return 1

    return evaluate_pair(args.fg, args.bg)


if __name__ == "__main__":
    sys.exit(main())

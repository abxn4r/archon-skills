#!/usr/bin/env python3
"""
Aperture Contrast Checker
WCAG 2.1/2.2 Relative Luminance + APCA Lightness Contrast (Lc)
Zero-dependency Python standard library implementation.

Usage:
  python check_contrast.py --fg "#EDEDED" --bg "#0D0E11"
  python check_contrast.py --fg "#7D93B0" --bg "#EEF2F7" --recommend
  python check_contrast.py --preset linear
"""

import sys
import re
import argparse
from typing import Tuple, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_color(color_str: str) -> Tuple[int, int, int]:
    color_str = color_str.strip()
    # Named colors
    named_colors = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "transparent": (0, 0, 0),
    }
    if color_str.lower() in named_colors:
        return named_colors[color_str.lower()]

    if color_str.startswith("#"):
        hex_val = color_str.lstrip("#")
        # #RGB -> #RRGGBB
        if len(hex_val) == 3:
            hex_val = "".join(c * 2 for c in hex_val)
        # #RGBA -> #RRGGBB (strip alpha for solid evaluation)
        elif len(hex_val) == 4:
            hex_val = "".join(c * 2 for c in hex_val[:3])
        # #RRGGBBAA -> #RRGGBB
        elif len(hex_val) == 8:
            hex_val = hex_val[:6]
        if len(hex_val) == 6:
            try:
                return (int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16))
            except ValueError:
                raise ValueError(f"Invalid hex digits in color: {color_str}")

    match_rgb = re.match(r"^rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*[\d.]+%?)?\s*\)$", color_str, re.I)
    if match_rgb:
        r, g, b = int(match_rgb.group(1)), int(match_rgb.group(2)), int(match_rgb.group(3))
        if all(0 <= c <= 255 for c in (r, g, b)):
            return (r, g, b)
        raise ValueError(f"RGB values must be in range 0-255: {color_str}")

    match_hsl = re.match(r"^hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?(?:\s*,\s*[\d.]+%?)?\s*\)$", color_str, re.I)
    if match_hsl:
        h, s, l = float(match_hsl.group(1)), float(match_hsl.group(2)) / 100.0, float(match_hsl.group(3)) / 100.0
        return hsl_to_rgb((h, s, l))

    raise ValueError(f"Unsupported color format: {color_str}")


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


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
    if abs(y_bg - y_txt) < 1e-5:
        return 0.0
    if y_bg > y_txt:
        c = (y_bg ** 0.56 - y_txt ** 0.57) * 1.14
        return c * 100.0
    else:
        c = (y_bg ** 0.65 - y_txt ** 0.62) * 1.14
        return -c * 100.0


def rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin
    l = (cmax + cmin) / 2.0

    if delta == 0:
        h = 0.0
        s = 0.0
    else:
        s = delta / (1.0 - abs(2.0 * l - 1.0))
        if cmax == r:
            h = ((g - b) / delta) % 6.0
        elif cmax == g:
            h = ((b - r) / delta) + 2.0
        else:
            h = ((r - g) / delta) + 4.0
        h *= 60.0
        if h < 0:
            h += 360.0
    return (h, s, l)


def hsl_to_rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
    h, s, l = hsl
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    x = c * (1.0 - abs(((h / 60.0) % 2.0) - 1.0))
    m = l - c / 2.0

    if 0 <= h < 60:
        r_p, g_p, b_p = c, x, 0
    elif 60 <= h < 120:
        r_p, g_p, b_p = x, c, 0
    elif 120 <= h < 180:
        r_p, g_p, b_p = 0, c, x
    elif 180 <= h < 240:
        r_p, g_p, b_p = 0, x, c
    elif 240 <= h < 300:
        r_p, g_p, b_p = x, 0, c
    else:
        r_p, g_p, b_p = c, 0, x

    r = round((r_p + m) * 255)
    g = round((g_p + m) * 255)
    b = round((b_p + m) * 255)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def recommend_lightness_fix(fg_rgb: Tuple[int, int, int], bg_rgb: Tuple[int, int, int], target_ratio: float = 4.5) -> Optional[Tuple[int, int, int]]:
    """Holding hue and saturation fixed, adjust lightness to achieve target WCAG ratio."""
    h, s, l = rgb_to_hsl(fg_rgb)
    bg_lum = relative_luminance(bg_rgb)
    direction = -1 if bg_lum > 0.18 else 1

    best_rgb = None
    step = 0.01

    for d in (direction, -direction):
        cur_l = l
        while True:
            cur_l += d * step
            if cur_l < 0.0:
                cur_l = 0.0
            elif cur_l > 1.0:
                cur_l = 1.0
            cand_rgb = hsl_to_rgb((h, s, cur_l))
            if wcag_contrast_ratio(cand_rgb, bg_rgb) >= target_ratio:
                best_rgb = cand_rgb
                break
            if cur_l == 0.0 or cur_l == 1.0:
                break
        if best_rgb is not None:
            break

    return best_rgb


def evaluate_pair(fg_str: str, bg_str: str, label: str = "", recommend: bool = False) -> int:
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

    if (not aa_normal or recommend):
        fix_rgb = recommend_lightness_fix(fg, bg, target_ratio=4.5)
        if fix_rgb:
            fix_hex = rgb_to_hex(fix_rgb)
            fix_ratio = wcag_contrast_ratio(fix_rgb, bg)
            fix_apca = abs(apca_contrast(fix_rgb, bg))
            print(f"  * Recommended Fix (Holding Hue/Sat):")
            print(f"    - Suggested FG               : {fix_hex}")
            print(f"    - Adjusted WCAG Ratio        : {fix_ratio:.2f}:1 [PASS AA]")
            print(f"    - Adjusted APCA (Lc)         : {fix_apca:.1f}")

    print()
    return 0 if aa_normal else 1


def main():
    parser = argparse.ArgumentParser(
        description="Aperture WCAG 2.1/2.2 & APCA Contrast Calculator with Fix Recommendations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--fg", help="Foreground color (e.g. #EDEDED, 'rgb(237,237,237)')")
    parser.add_argument("--bg", help="Background color (e.g. #0D0E11, 'rgb(13,14,17)')")
    parser.add_argument("--preset", choices=["dark", "light", "linear", "slate", "zinc"], help="Audit standard color preset")
    parser.add_argument("--recommend", action="store_true", help="Calculate recommended lightness adjustment to pass AA")

    args = parser.parse_args()

    if args.preset == "dark" or args.preset == "linear":
        evaluate_pair("#EDEDED", "#0D0E11", "Linear Dark Base / Primary Text", args.recommend)
        evaluate_pair("#8A8F98", "#0D0E11", "Linear Dark Base / Muted Secondary Text", args.recommend)
        evaluate_pair("#5E6AD2", "#0D0E11", "Linear Accent Indigo / Dark Base", args.recommend)
        return 0
    elif args.preset == "light":
        evaluate_pair("#111827", "#FFFFFF", "Clean Light Base / Primary Text", args.recommend)
        evaluate_pair("#6B7280", "#FFFFFF", "Clean Light Base / Secondary Text", args.recommend)
        evaluate_pair("#4F46E5", "#FFFFFF", "Primary Accent / Light Base", args.recommend)
        return 0
    elif args.preset == "slate":
        evaluate_pair("#F8FAFC", "#0F172A", "Slate-900 Base / Slate-50 Text", args.recommend)
        evaluate_pair("#94A3B8", "#0F172A", "Slate-900 Base / Slate-400 Muted", args.recommend)
        evaluate_pair("#38BDF8", "#0F172A", "Slate-900 Base / Sky-400 Accent", args.recommend)
        return 0
    elif args.preset == "zinc":
        evaluate_pair("#FAFAFA", "#09090B", "Zinc-950 Base / Zinc-50 Text", args.recommend)
        evaluate_pair("#A1A1AA", "#09090B", "Zinc-950 Base / Zinc-400 Muted", args.recommend)
        evaluate_pair("#10B981", "#09090B", "Zinc-950 Base / Emerald-500 Accent", args.recommend)
        return 0

    if not args.fg or not args.bg:
        parser.print_help()
        return 1

    return evaluate_pair(args.fg, args.bg, recommend=args.recommend)


if __name__ == "__main__":
    sys.exit(main())

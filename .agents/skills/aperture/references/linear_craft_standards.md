# LINEAR CRAFT STANDARDS & INTERACTION DESIGN
*Archon Design & UX Direction -- Aperture Advisor*

---

## 1. 4PX / 8PX SPATIAL SYSTEM
- **Grid Increment**: All padding, margins, gaps, and dimensions strictly adhere to 4px multiples: 4, 8, 12, 16, 20, 24, 32, 48, 64px.
- **Component Heights**:
  - Small / Dense (tables, badges): 24px - 28px
  - Medium (buttons, input fields): 32px - 36px
  - Large (hero CTAs, prominent inputs): 40px - 44px
- **Negative Space Directive**: Whitespace is structural hierarchy, not emptiness. Prefer generous component separation (32-48px) paired with dense internal component packing (8-12px).

---

## 2. TYPOGRAPHIC CRAFT & OPTICAL SCALE
- **Scale**: 11px (micro), 12px (caption/meta), 13px/14px (body compact/default), 16px (subhead), 20px (section header), 28px+ (page title).
- **Line Heights**:
  - Body copy: 1.5x - 1.6x for relaxed scanning.
  - Headings: 1.15x - 1.25x to prevent awkward vertical separation.
- **Letter Spacing**:
  - Tighten display headers: `-0.02em` to `-0.03em`.
  - Loosen small uppercase meta text: `+0.05em` to `+0.08em`.

---

## 3. COLOR ARCHITECTURE & MONOCHROMATIC DISCIPLINE
- **Dark Mode Palette**:
  - Background Base: `#0D0E11` / `#090A0C` (avoid pure pitch `#000000` except for high-contrast OLED blackouts).
  - Card / Surface: `#16181D` (subtle elevation).
  - Border Neutral: `rgba(255, 255, 255, 0.08)` -- razor-thin, never harsh.
  - Primary Text: `#EDEDED` (92% luminance).
  - Secondary / Muted Text: `#8A8F98` (60% luminance).
- **Deliberate Accent**: A single saturated accent (e.g. Linear Indigo `#5E6AD2`, Electric Blue, or Amber). Never scatter rainbow accents across a utility interface.

---

## 4. MOTION & MICRO-INTERACTIONS
- **Duration**: 150ms - 220ms. Never exceed 300ms for utility interactions.
- **Easing**: `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out spring / snappy deceleration).
- **Hover Transitions**: Background color, border opacity, and subtle scale (`scale(1.015)`).

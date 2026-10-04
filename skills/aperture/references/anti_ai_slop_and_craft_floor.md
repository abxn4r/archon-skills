# ANTI-AI SLOP GATES & THE CRAFT FLOOR
*Aperture Design & UX Direction — Universal Quality Floor (75 Non-Negotiable Invariants)*

---

## 1. THE 75 CRAFT FLOOR GATES

AI coding assistants naturally gravitate toward clichés, safe templates, and statistical averages. The following 75 gates enforce an uncompromising quality floor across all interfaces designed, audited, or generated under Aperture.

---

### PART 1: VISUAL & MATERIALITY GATES

1. **The Lila / AI Purple Gradient Ban**: Strictly ban purple/violet gradient hero buttons, glowing purple card borders, and neon gradient text fills. Use crisp neutral bases with a single purposeful, high-contrast accent.
2. **The Premium-Consumer Palette Ban**: For luxury, wellness, artisan, DTC, or culinary briefs, the LLM default is warm beige/cream (`#f5f1ea`, `#f7f5f1`) + brass/clay (`#b08947`, `#b6553a`) + espresso text (`#1a1714`). This palette is BANNED as an unprompted default. Rotate across 7 distinctive palettes:
   - *Cold Luxury*: silver-grey + chrome + smoke (Tesla / Apple Watch aesthetic)
   - *Forest*: deep pine green + bone neutral + amber accent
   - *Black and Tan*: true off-black + warm tan, sharp contrast, zero beige
   - *Cobalt + Cream*: saturated blue against a single crisp neutral
   - *Terracotta + Slate*: warm rust against cool technical grey
   - *Olive + Brick + Paper*: muted olive with brick-red accent
   - *Monochrome + High-Voltage Pop*: off-white + off-black + single electric accent (emerald, hot pink, cobalt)
3. **Elevation Singularity**: Declare elevation once — either a 1px border OR a soft diffused shadow (`shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`). Never combine a 1px border with a wide dark shadow ("the ghost card").
4. **No Zero-Offset Colored Halos**: Outer glows with 0px blur and bright saturation are banned. Shadows must carry vertical offset (`Y > 0`) and soft diffusion tinted to the ambient background.
5. **No Neobrutalist Block Shadows by Accident**: Hard offset shadows (`box-shadow: 4px 4px 0 #000`) belong strictly to authentic neobrutalism. Never use them as an unprompted default.
6. **No Pure Pitch Black**: Never use `#000000` for backgrounds unless targeting high-contrast OLED blackouts. Use `#0D0E11`, `#090A0C`, Zinc-950 (`#09090B`), or Slate-950 (`#020617`).
7. **Desaturated Accent Palette & Single Accent Lock**: Accent colors must not exceed 80% saturation. Once an accent is chosen, lock it across the entire page — never mix teal badges, blue CTAs, and purple highlights in the same screen.
8. **No Re-Drawn UI Chrome**: Never hand-build fake browser address bars (URL pill + traffic light dots), fake smartphone bezels, or mock terminal windows wrapping code unless explicitly requested as mockup art. Real content speaks for itself.
9. **No Monospace as Costume**: Monospace fonts belong to code, data tables, metrics, and technical measurements. Never set normal headings, subtitles, or body copy in monospace just to make the app "look technical."
10. **No Sketchy SVG Doodles**: Hand-drawn vector squiggles, `feTurbulence` grain classes, and cartoon arrows look amateurish. Use clean geometric primitives and hairline rules.
11. **Never Animate an Image Directly on Hover**: Never apply `scale()` or `translate()` directly to an `<img>` element on hover. Apply tactile feedback to the outer card/container instead.
12. **Concentric Border Radius Mathematics**: When nesting rounded containers, calculate outer radius using:
    $$\text{outerRadius} = \text{innerRadius} + \text{padding} \quad (\text{when padding} \le 24\text{px})$$
    Example: `rounded-2xl` (16px) with `p-2` (8px padding) contains an inner `rounded-lg` (8px). Mismatched radii create severe optical tension.
13. **Optical Alignment for Action Buttons**: When an icon accompanies text inside a button, geometric centering looks unbalanced. Apply optical compensation:
    $$\text{icon-side padding} = \text{text-side padding} - 2\text{px}$$
    Example: `ps-4 pe-3.5 flex items-center gap-2`.
14. **Play Button Triangle Optical Offset**: Play icon triangles have an asymmetrical visual weight. Offset the SVG horizontally: `transform: translateX(2px)`.
15. **Shadows as Borders (3-Layer Light / 1-Ring Dark)**:
    - *Light Mode*:
      ```css
      box-shadow: 0 0 0 1px oklch(0 0 0 / 0.06), 0 1px 2px -1px oklch(0 0 0 / 0.06), 0 2px 4px 0 oklch(0 0 0 / 0.04);
      ```
    - *Dark Mode*:
      ```css
      box-shadow: 0 0 0 1px oklch(1 0 0 / 0.08);
      ```
16. **Neutral Image Outlines**: Apply a 1px inner outline to images for crisp edge separation:
    ```css
    img { outline: 1px solid oklch(0 0 0 / 0.1); outline-offset: -1px; }
    /* Dark mode */
    img { outline: 1px solid oklch(1 0 0 / 0.1); outline-offset: -1px; }
    ```
    Never tint the outline to the project palette or accent hue.
17. **Shape Consistency Lock**: Establish ONE corner-radius scale for the entire surface (all-sharp, all-soft 12-16px, or all-pill). Mixed corner styles without a documented rule are broken.
18. **Page Theme Lock**: A page has ONE theme. Never sandwich a light-mode warm-paper section inside a dark-mode page without explicit user authorization for a deliberate theme-switch scroll device.

---

### PART 2: LAYOUT & STRUCTURAL GATES

19. **Anti-Center Bias**: When `DESIGN_VARIANCE > 4`, centered H1 + subtitle + button hero blocks are banned. Force split-screen (50/50), left-aligned copy with right-aligned asset, or deliberate asymmetric whitespace.
20. **Hero Fits Initial Viewport**:
    - Headline: maximum 2 lines on desktop.
    - Subtext: maximum **20 words** AND maximum 3-4 lines.
    - CTAs: visible immediately without scrolling.
21. **Hero Top Padding Cap**: Maximum `pt-24` (≈6rem) on desktop. Larger padding pushes content halfway down the fold, reading as a layout bug.
22. **Hero Stack Discipline (Max 4 Text Elements)**: Allowed text elements in hero:
    1. Eyebrow OR brand strip (pick zero or one)
    2. Headline (max 2 lines)
    3. Subtext (max 20 words)
    4. CTAs (1 primary + max 1 secondary)
    Banned inside hero: trust logo strips, version stamps, pricing teasers, bullet lists.
23. **Trust Logo Wall Under Hero**: Logo walls ("Trusted by", "Customers") belong directly UNDER the hero section, never inside the hero flex container.
24. **Eyebrow Restraint (#1 Violated AI Tell)**:
    - Maximum 1 eyebrow per 3 sections (e.g., a 9-section page may have at most 3 eyebrows total).
    - If Section A has an eyebrow, Sections B and C cannot have one.
    - Never prepend tiny uppercase tracked labels (`OVERVIEW`, `FEATURES`, `WHY US`) above every heading. Let headings stand on their own weight.
25. **Split-Header Ban**: The pattern "left big headline + right small explainer paragraph floating in top-right" is banned as default. Use clean vertical stacking or genuine 2-column content.
26. **Section Layout Repetition Ban**: Once a layout family is used (e.g. 3-column cards, split media, full-width quote), it may appear at most ONCE on the page. A page with 8 sections needs at least 4 distinct layout families.
27. **Zigzag Alternation Cap**: Alternating left-image/right-text then left-text/right-image is capped at maximum 2 consecutive sections. The 3rd section must break the pattern.
28. **Bento Cell Count Rule**: A bento grid has EXACTLY as many cells as there is real content. 3 items = 3 cells (1+2 split). Never generate an empty or placeholder cell at the end of a grid.
29. **Bento Background Diversity**: A multi-cell bento grid cannot be uniform cards. At least 2-3 cells must have real visual contrast: photography, subtle gradient, pattern, or tinted background.
30. **Single CTA Intent Across Page**: Never use multiple synonyms for the same action on one page (e.g. mixing "Get in touch" + "Contact us" + "Let's talk"). Pick ONE label and use it consistently.
31. **CTA Button Wrap Ban**: Primary CTA button text MUST fit on a single line at desktop. Wrapping CTA text ("GET STARTED<br>TODAY") is an immediate failure.
32. **Desktop Single-Line Navigation**: Desktop navigation must fit on a single row at ≥1024px. Height cap: 64px–80px.
33. **Anti-Card Overuse (Dashboard Hardening)**: When `VISUAL_DENSITY > 7`, generic card containers are banned. Group metrics using structural borders (`border-t`, `divide-y`) or whitespace hierarchy.
34. **No 3-Column Equal Card Rows**: The generic 3 identical cards horizontally layout is banned. Diversify using 2-column zig-zag, asymmetric bento grids (70/30 split), or horizontal scrolling galleries.
35. **Viewport Stability**: Never use `h-screen` on mobile-accessible hero sections. Always use `min-h-[100dvh]` to prevent Safari dynamic URL bar jumping.
36. **CSS Grid Over Flex Math**: Never calculate column layouts with percentage math (`w-[calc(33%-1rem)]`). Use standard CSS Grid (`grid-cols-1 md:grid-cols-3 gap-6`).
37. **Unsafe Flex Truncation**: Every flex child containing text truncation (`truncate`, `overflow-hidden`, `text-ellipsis`) must declare `min-w-0` to avoid layout blowout.
38. **Root Horizontal Overflow Protection**: Set `overflow-x: clip` on `html` and `body` (never `overflow-x: hidden`, which can break sticky positioning).

---

### PART 3: TYPOGRAPHY & COPY GATES

39. **No Inter by Default for Creative / Premium Vibes**: Do not default to `Inter` when a premium, distinct personality is needed. Prefer `Geist`, `Satoshi`, `Cabinet Grotesk`, `Outfit`, or `Plus Jakarta Sans`.
40. **Serif Discipline**: Serif typefaces are strictly reserved for authentic editorial, luxury, or literary surfaces. Utility, SaaS, and productivity dashboards must use high-craft sans-serif pairings.
41. **Italic Descender Clearance**: When italic display type contains descenders (`y`, `g`, `j`, `p`, `q`), `leading-none` clips the bottom. Use `leading-[1.1]` minimum and add `pb-1` reserve padding.
42. **Optical Text Compensation on Dark Surfaces**: Light text on dark backgrounds optically expands and appears tighter. Compensate on three perceptual axes:
    - Slightly more line height (+0.05x)
    - Slightly more tracking (+0.01em)
    - One weight step lighter (Medium 500 instead of SemiBold 600)
43. **Heading Line Balancing**: Apply `text-wrap: balance` or `text-pretty` to all headings to eliminate lonely orphan words.
44. **Tabular Numerals**: Apply `font-variant-numeric: tabular-nums` (or `tabular-nums` class) to all numbers in data tables, tickers, counters, timers, and metric grids.
45. **Body Measure Limits**: Restrict running body text to `max-w-[65ch]` or `max-w-[75ch]` to preserve reading comfort.
46. **ABSOLUTE EM-DASH BAN (#1 Visual Tell)**: Em-dash (`—`) and en-dash (`–`) are strictly BANNED in visible UI text, headlines, buttons, eyebrows, and captions. Use standard hyphens (`-`), periods, or restructure the sentence into two clauses.
47. **Middle-Dot Rationed**: The middle-dot (`·`) is rationed to maximum 1 per line in metadata strips. Never use it as a universal list separator (`foo · bar · baz · qux`).
48. **Zero Decorative Status Dots**: A colored dot before nav items or list rows without actual server status meaning is banned.
49. **No Generic Step Labels**: Banned: `Stage 1 / Stage 2`, `Step 01 / Step 02`, `Phase 1 / Phase 2`. Name the step by its concrete action: "Install", "Configure", "Ship".
50. **No Startup-Slop Brand Names & Jane Doe**: Never invent fake metrics ("+47% conversion") or cliché names ("Acme Corp", "John Doe"). Use authentic data, honest placeholders (`--` or `N/A`), or realistic messy numbers (`47.2%`, `+$14,280`).
51. **No AI Throat-Clearing Copy**: Ban words like "Elevate", "Seamless", "Unleash", "Next-Gen", "Tapestry", "Delve", "Testament". Use concrete, active verbs.
52. **Quote & Testimonial Line Cap**: Testimonials on landing pages are capped at **maximum 3 lines**. Long paragraphs belong in case studies.

---

### PART 4: INTERACTION & ACCESSIBILITY GATES

53. **No Outline Removal without Focus Replacement**: Never use `outline: none` or `outline-none` without providing an immediate, high-contrast `:focus-visible` replacement (`ring-2 ring-offset-2`).
54. **Icon Buttons Need Accessible Names**: Every icon-only button must include `aria-label` or visually hidden text. Decorative icons inside buttons must declare `aria-hidden="true"`.
55. **Never Block Paste**: Never intercept paste events (`onPaste={(e) => e.preventDefault()}`) on input or password fields.
56. **Touch Target Minimums**: Mobile interactive targets must meet a minimum bounding box of 44×44px (with at least 8px spacing). Desktop targets must never fall below 24×24px.
57. **Focus Not Obscured**: Sticky headers, footers, and floating banners must not obscure focused elements (`scroll-margin-top: 80px`).
58. **Form Error Association**: Form field errors must be linked to inputs via `aria-describedby` and flagged with `aria-invalid="true"`.
59. **No Color Alone for Status**: State, validation, or errors must never be communicated by color alone — always accompany with an icon, badge, or explicit text.
60. **Accessible Click Handlers**: Never use `<div onClick>` or `<span onClick>`. Use semantic `<button>`. If a custom element is required, declare `role="button"`, `tabIndex={0}`, and `onKeyDown` handlers for Enter/Space.
61. **Frequency-Based Motion (100+/Day = 0ms)**: Keyboard shortcuts, command palettes, and primary navigation must execute in **0ms** with zero animation (the Raycast model).
62. **Never Animate from `scale(0)`**: Scale entrances must start from `scale(0.95)` with `opacity: 0`.
63. **Origin-Aware Popovers**: Popovers and dropdowns animate outward from their trigger (`transform-origin: var(--transform-origin)`). Modals stay centered.
64. **Tooltips Skip Delay**: Once a tooltip opens, hovering adjacent tooltips must open them instantly with 0ms transition (`[data-instant] { transition-duration: 0ms }`).
65. **Tactile Feedback on `:active`**: Buttons must compress physically on click: `transform: scale(0.97)` with `transition: transform 160ms ease-out`.
66. **Composited Transitions Only**: Animate strictly `transform` and `opacity`. Never use `transition: all`.
67. **Modern CSS `@starting-style`**: Use `@starting-style` for zero-JS CSS entrance animations.
68. **Browser Surfaces AI Forgets**: Theme native browser surfaces from the project palette:
    - Text selection (`::selection`)
    - Input caret (`caret-color`)
    - Scrollbar stability (`scrollbar-gutter: stable;`)
    - Underline offset (`text-underline-offset: 4px;`)
    - Tabular digits (`tabular-nums`)
69. **Floating Pill / Recessed Navigation**: For marketing, showcases, and landing pages, ban full-width, edge-to-edge sticky navbars with heavy solid backgrounds. Prefer floating pill navbars (`max-w-fit mx-auto rounded-full backdrop-blur-md border border-white/10 px-5 py-2.5`) or integrated recessed headers that feel native to the page surface.
70. **Double-Bezel Card Architecture**: For high-elevation and showcase components, use double-bezel containment: an outer hairline border paired with an inner inset highlight ring (`border border-zinc-200/80 dark:border-white/10 ring-1 ring-inset ring-black/5 dark:ring-white/5`) to create authentic physical depth.
71. **Ultra-Light Iconography & Stroke Weight Discipline**: Defaulting to heavy 2px–2.5px icon strokes makes interfaces look clumsy. Use ultra-light 1.0px or 1.5px stroke weights (Phosphor Light, Radix, Lucide thin). Lock stroke width globally across all icons on the page.
72. **Atmospheric Noise & Subtle Texture**: When designing dark-mode or immersive hero sections, ban sterile flat digital blacks. Introduce subtle SVG noise overlays (`mix-blend-mode: overlay`, opacity `0.02 - 0.04`) to give surfaces photographic grain and physical warmth.
73. **The Entry Sequence & Preloading Discipline**: High-end interactive experiences must never flash unstyled layout shifts or blank screens while fonts or assets resolve. Implement lightweight preloading sequences (smooth opacity fade or split reveal) with `@media (prefers-reduced-motion: reduce)` fallbacks.
74. **Responsive Degradation & Fine Pointer Bounds**: Complex hover interactions, magnetic buttons, and custom tracking cursors must be strictly wrapped inside `@media (hover: hover) and (pointer: fine)`. Mobile touch devices must receive direct, low-latency touch response with zero mouse-interpolation overhead.
75. **Curated Production Stack Standard**: Build upon battle-tested UI primitives rather than hand-rolling fragile custom DOM widgets:
    - Toasts: **Sonner**
    - Dialogs, Popovers, Dropdowns: **Radix UI** / **Base UI**
    - Command Menus: **Cmdk**
    - Drawers / Bottom Sheets: **Vaul**
    - Smooth Scrolling: **Lenis** (`@studio-freight/lenis`)
    - Data Tables: **TanStack Table**

---

## 2. THE BROWSER SURFACES CODE RECIPES

```css
/* 1. Text Selection */
::selection {
  background-color: var(--accent-subtle, rgba(94, 106, 210, 0.25));
  color: var(--fg-primary, #EDEDED);
}

/* 2. Caret Color */
input, textarea {
  caret-color: var(--accent, #5E6AD2);
}

/* 3. Scrollbar Gutter Stability & Minimalist Scrollbars */
html {
  scrollbar-gutter: stable;
}
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 9999px;
}

/* 4. Underline Offset */
a.underline-link {
  text-decoration: underline;
  text-underline-offset: 4px;
  text-decoration-thickness: 1px;
  text-decoration-color: rgba(255, 255, 255, 0.3);
}
```

---

## 3. PRE-EMIT CRITIQUE SCORING (SIX AXES)

Score every artifact before delivery (1 to 5):
- **Philosophy (P)**: Solves a real problem, not aesthetic vanity.
- **Hierarchy (H)**: Immediate eye-path to primary action/metric.
- **Execution (E)**: Mathematical precision on 4px grid, concentric radii, token grammar.
- **Specificity (S)**: Unique product voice, zero boilerplate placeholder copy.
- **Restraint (R)**: Pruned unnecessary cards, glows, and decorations.
- **Variety (V)**: Avoids predictable AI layouts and templates.

**Quality Gate**: Any score `< 3` requires an immediate revision pass.
Stamp final verdict:
`/* Aperture · Pre-emit Critique: P5 H5 E5 S5 R4 V5 */`

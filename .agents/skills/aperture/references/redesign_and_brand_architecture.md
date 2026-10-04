# REDESIGN & BRAND ARCHITECTURE
*Aperture Design & UX Direction — Greenfield vs. Redesign Protocols & System Mapping*

---

## 1. THE THREE WORKFLOW MODES

Misclassifying a redesign mode is the single most common failure in AI frontend engineering:

### 1.1 Greenfield
- **Condition**: New product, new feature surface, or explicit mandate to start from scratch.
- **Protocol**: Calibrate dials (`DESIGN_VARIANCE: 8`, `MOTION_INTENSITY: 6`, `VISUAL_DENSITY: 4`), establish two-tier token system, and construct fresh layout.

### 1.2 Redesign — Preserve
- **Condition**: Modernizing an existing production product without breaking brand equity, muscle memory, or SEO.
- **Protocol**: Audit before touching. Extract incumbent brand colors, typography, and spacing. Modernize sub-pixel craft, improve accessibility, and upgrade motion while keeping visual DNA identical.

### 1.3 Redesign — Overhaul
- **Condition**: Complete visual redesign on top of existing functional architecture.
- **Protocol**: Retain information architecture (routes, URLs, form fields, copy truth), but completely replace visual tokens, component implementations, and layout compositions.

---

## 2. AUDIT BEFORE TOUCHING (THE PRE-REDESIGN AUDIT)

Never edit a single file in a redesign until documenting current state:

1. **Brand Tokens**: Primary/accent colors, font stack, radii conventions, shadow depths.
2. **Information Architecture (IA)**: URL slugs, primary nav structure, breadcrumbs, conversion paths.
3. **SEO Baseline**: Existing ranking URLs, meta tags, H1 structure, structured data.
4. **Current Dial Reading**: Infer current `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY`.
5. **What Must Be Preserved**:
   - Signature user-recognized interactions.
   - Core copy claims and legal disclosures.
   - Form field names and analytics tracking IDs (`data-testid`, event hooks).
6. **What Must Be Retired**:
   - Outdated AI-slop tells (purple gradients, generic card rows, em-dash crutches).
   - Accessibility failures (missing focus rings, low contrast).
   - Viewport bugs (`h-screen`, layout blowouts).

---

## 3. THE 6 MODERNIZATION LEVERS (IN PRIORITY ORDER)

When improving an existing interface, execute strictly in order of ROI:

1. **Typography Refresh**: Biggest visual lift with lowest regression risk. Tighten display line heights (1.15x), establish 65ch body measure, apply `text-wrap: balance`.
2. **Spacing & Vertical Rhythm**: Enforce 4px/8px grid. Increase section whitespace and apply 2:1 heading margin ratio.
3. **Color Calibration**: Desaturate bright accents (<80%), tint dark neutrals, ensure all text achieves WCAG AA (4.5:1) / APCA Lc ≥ 75.
4. **Motion Layer**: Add sub-200ms `:active` tactile compression (`scale(0.97)`), origin-aware popovers, and smooth drawer curves.
5. **Hero & Layout Recomposition**: Replace generic centered heroes with asymmetric split layouts; enforce viewport fit (headline ≤ 2 lines, subtext ≤ 20 words).
6. **Full Block Replacement**: Rebuild components only when existing structure is completely unsalvageable.

---

## 4. BRIEF-TO-DESIGN-SYSTEM MAPPING

Do not hand-roll ad-hoc CSS for components when an official, battle-tested system exists:

### 4.1 When to Use Official Design System Packages
| Brief / Context | Target System | Why |
|---|---|---|
| Microsoft / Enterprise IT | `@fluentui/react-components` | Microsoft enterprise tokens, complete a11y |
| Google-style / Android SaaS | `@material/web` (Material 3) | Official dynamic color theming |
| Enterprise Analytics / IBM | `@carbon/react` | Industrial data density & complex data tables |
| E-commerce Admin / Merchant | `polaris.js` / `@shopify/polaris` | Native Shopify admin UX standard |
| Developer Tools / GitHub-style | `@primer/react` | Official GitHub design system |
| Modern Accessible React Foundation | `@radix-ui/themes` | Unstyled accessible primitives + theme layer |
| Modern High-Craft SaaS (Owned code) | `shadcn/ui` + Tailwind v4 | Maximum customization; full source code ownership |

### 4.2 When the Brief is an Aesthetic Direction (No Single Package)
| Aesthetic | Implementation Pattern | Guardrails |
|---|---|---|
| **Glassmorphism / Frosted Glass** | `backdrop-filter: blur()`, inner 1px border (`border-white/10`), inner highlight | Must provide solid fallback for `prefers-reduced-transparency`. |
| **Bento Grid 2.0** | Native CSS Grid, asymmetric row/col spans (e.g. 70/30 split) | Exactly as many cells as content; no empty placeholder tiles. |
| **Editorial Brutalism** | Monochromatic palettes, sharp edges (radius 0), hairline rules, raw type | Never use for dense productivity dashboards. |
| **Tactile Modern (Linear style)** | Off-black surfaces (`#0D0E11`), 1px translucent borders, spring physics | Sub-300ms motion budget; no gratuitous animation loops. |
| **Apple Liquid Glass** | *Approximation only*. Multi-layer backdrop blur + inner specular refraction | No official CSS package exists. Label code clearly as an approximation. |

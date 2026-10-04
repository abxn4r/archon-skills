# SPATIAL & TYPOGRAPHY SYSTEMS
*Aperture Design & UX Direction — Mathematics of Layout, Scale & Tokens*

---

## 1. 4PX / 8PX SPATIAL DISCIPLINE

Every margin, padding, gap, border-radius, and component dimension must strictly resolve to a multiple of 4px. Arbitrary values (e.g. `13px`, `19px`, `27px`) represent an immediate craft failure.

### Standard Spatial Scale
| Token | Dimension | Typical Usage |
|---|---|---|
| `space-1` | **4px** | Micro gaps between icon and label, inline badges |
| `space-2` | **8px** | Dense component internal padding, tightly grouped list items |
| `space-3` | **12px** | Standard form input horizontal padding, card internal spacing |
| `space-4` | **16px** | Standard container padding, modal body inset |
| `space-5` | **20px** | Section header separation |
| `space-6` | **24px** | Grid gaps, card separation in dashboards |
| `space-8` | **32px** | Major block separation, table section padding |
| `space-12` | **48px** | Page section vertical spacing (dense app) |
| `space-16` | **64px** | Landing page hero padding, major marketing transitions |

### Component Height Invariants
- **Dense Utility (Tables, Badges, Chips)**: `24px` to `28px`
- **Standard Control (Buttons, Inputs, Selects)**: `32px` to `36px`
- **Prominent / Large (Hero CTAs, Search Bars)**: `40px` to `44px`

### Vertical Rhythm & Gestalt Proximity (The 2:1 Ratio)
- **More Space Above than Below**: A section heading must always have more whitespace above it (separating it from previous content) than below it (binding it to the content it introduces). Target ratio: **2:1** (e.g. `margin-top: 32px; margin-bottom: 16px`).
- **Negative Space as Structural Framing**: Whitespace is not empty space; it is structural grouping. Before wrapping elements in another card border, test separating them with `32px` of pure whitespace.

---

## 2. OPTICAL ALIGNMENT & SURFACE GEOMETRY

### 2.1 Concentric Border Radius Mathematics
When nesting rounded containers, calculate the outer radius using:
$$\text{outerRadius} = \text{innerRadius} + \text{padding} \quad (\text{when padding} \le 24\text{px})$$

```css
/* Good: concentric radii */
.card {
  border-radius: 20px; /* 12px inner + 8px padding */
  padding: 8px;
}
.card-inner {
  border-radius: 12px;
}
```
*Tailwind Example*:
```tsx
<div className="rounded-2xl p-2">       {/* 16px radius, 8px padding */}
  <div className="rounded-lg">          {/* 8px radius (16 - 8 = 8) */}
    ...
  </div>
</div>
```

### 2.2 Optical Alignment for Action Buttons (Icon + Text)
Where an icon accompanies text inside a button, geometric centering looks unbalanced. Apply optical compensation:
$$\text{icon-side padding} = \text{text-side padding} - 2\text{px}$$

```css
.button-with-icon {
  padding-inline-start: 16px;
  padding-inline-end: 14px; /* trailing icon side = text side - 2px */
}
```
```tsx
<button className="ps-4 pe-3.5 flex items-center gap-2">
  <span>Continue</span>
  <ArrowRightIcon className="w-4 h-4" />
</button>
```

### 2.3 Play Button Triangle Optical Offset
Play icons are triangular and their geometric center is not their visual center. Shift horizontally:
```css
.play-button svg {
  transform: translateX(2px);
}
```

---

## 3. TWO-TIER DESIGN TOKEN ARCHITECTURE

To support effortless dark/light mode switching, whitelabeling, and high-contrast accessibility, design tokens are split into two strict tiers:

### Tier 1: Primitives (What it IS)
Named by appearance and step. Never referenced directly in components:
```css
:root {
  --blue-500: #3B82F6;
  --neutral-100: #F3F4F6;
  --neutral-900: #111827;
  --neutral-950: #09090B;
}
```

### Tier 2: Semantics (What JOB it does)
Named by role. This is what templates and UI components reference:
```css
:root {
  --color-bg-page: var(--neutral-100);
  --color-bg-surface: #FFFFFF;
  --color-text-primary: var(--neutral-900);
  --color-text-secondary: #6B7280;
  --color-border-subtle: #E5E7EB;
  --color-accent-solid: var(--blue-500);
  --color-accent-hover: #2563EB;
}

[data-theme="dark"] {
  --color-bg-page: var(--neutral-950);
  --color-bg-surface: #111215;
  --color-text-primary: #EDEDED;
  --color-text-secondary: #8A8F98;
  --color-border-subtle: rgba(255, 255, 255, 0.08);
  --color-accent-solid: #5E6AD2;
  --color-accent-hover: #4B55C4;
}
```

### Naming Grammar:
$$\text{--color-\{role\}-\{variant\}-\{state\}}$$
Examples:
- `--color-bg-surface-hover`
- `--color-text-secondary`
- `--color-border-strong`
- `--color-accent-solid-active`

---

## 4. OPTICAL TYPOGRAPHY & SCALE MATHEMATICS

### 4.1 Typography Hierarchy & Type Scales
| Role | Font Size | Line Height | Tracking | Weight | Recommended Sans Pairings |
|---|---|---|---|---|---|
| **Display Title** | 36px – 56px | 1.10x – 1.15x | `-0.03em` | Bold / Medium | `Cabinet Grotesk` or `Geist` |
| **Page H1** | 28px – 32px | 1.15x – 1.20x | `-0.02em` | SemiBold (600) | `Geist` or `Satoshi` |
| **Section H2** | 20px – 24px | 1.25x – 1.30x | `-0.015em` | SemiBold (600) | `Geist` or `Satoshi` |
| **Subhead H3** | 16px – 18px | 1.35x – 1.40x | `-0.01em` | Medium (500) | `Geist` or `Satoshi` |
| **Body Default** | 14px – 15px | 1.50x – 1.60x | `0em` | Regular (400) | `Geist` or `Inter` |
| **Caption / Meta** | 12px – 13px | 1.40x – 1.50x | `+0.01em` | Regular / Medium | `Geist` or `Inter` |
| **Micro Uppercase** | 10px – 11px | 1.20x | `+0.06em` to `+0.08em` | SemiBold (600) | `Geist Mono` or `JetBrains Mono` |

### 4.2 Optical Text Compensation on Dark Surfaces
Light text rendered on dark backgrounds optically bleeds and appears heavier and tighter. Always compensate:
1. **Increase Line Height**: Add +0.05x leading to dark mode body copy.
2. **Increase Tracking**: Add `+0.01em` tracking to prevent letterforms from merging.
3. **Reduce Font Weight**: Drop weight by one step (e.g. from SemiBold 600 to Medium 500) to match light-mode visual weight.

### 4.3 Typography Invariants
- **Headings MUST be tight**: Large display text with `leading-normal` (1.5x) looks detached. Headings require tight line heights (`1.10x – 1.25x`).
- **Body copy MUST breathe**: Dense body text requires `1.50x – 1.60x` line height.
- **Reading Measure**: Restrict running body text to `45ch`–`75ch` (`max-w-[65ch]`).
- **Heading Line Balancing**: Apply `text-wrap: balance` to eliminate lonely orphan words.
- **Tabular Numerals**: Apply `tabular-nums` (`font-variant-numeric: tabular-nums`) to all numbers in tables, metrics, counters, and timers.

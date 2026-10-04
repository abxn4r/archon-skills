# COMPONENT STATE MATRIX & REACT COMPOSITION PATTERNS
*Aperture Design & UX Direction — Architectural & State Craft*

---

## 1. THE 8-STATE COMPLETENESS MATRIX

Every interactive component evaluated, authored, or refactored under Aperture must explicitly account for all 8 lifecycle states. LLMs naturally produce "happy-path static" components; Aperture enforces state completeness:

| State | Visual Treatment & Behavior | CSS / Accessibility Trigger |
|---|---|---|
| **1. Default** | Resting elevation, border neutral (`rgba(255,255,255,0.08)` dark / `#E2E8F0` light), high-contrast text | Standard class definition |
| **2. Hover** | +6–10% surface luminance, subtle border brightening (`rgba(255,255,255,0.14)`). Bounded by pointer capability. | `:hover` inside `@media (hover: hover)` |
| **3. Active / Pressed** | Physical depression: `-translate-y-[1px]` or `scale-[0.98]`. Snappy 120ms spring compression. | `:active` |
| **4. Focus-Visible** | 2px solid accent ring with 2px offset (`outline: 2px solid var(--accent); outline-offset: 2px`). Never outline: none. | `:focus-visible` |
| **5. Disabled** | `opacity: 0.45`, `cursor: not-allowed`, `pointer-events: none`. Color contrast exempt but must remain discernible. | `:disabled`, `[aria-disabled="true"]` |
| **6. Loading / Skeleton** | Component preserves fixed width/height to eliminate layout shift (CLS). Text replaced by shimmer or spinner. | `[data-loading="true"]`, skeleton loader |
| **7. Error** | High-contrast error ring/border (`#F43F5E`), inline error message associated via `aria-describedby`, `aria-invalid="true"`. | `[aria-invalid="true"]` |
| **8. Success / Confirmed** | Subtle tactile confirmation (green checkmark icon or soft pulse). Auto-reverts to default after 2.5s. | `[data-state="success"]` |

---

## 2. REACT COMPOSITION PATTERNS (VERCEL STANDARDS)

Components scale through composition, not configuration. Avoid adding endless boolean props (`isPrimary`, `hasBadge`, `isCompact`, `withIcon`).

### 2.1 Rule 1: Compound Components over Boolean Props
```tsx
// ❌ Fragile: boolean prop proliferation
<Card 
  title="Analytics" 
  isCompact 
  hasHeaderBorder 
  showFilter 
  onFilterClick={fn} 
/>

// ✅ Resilient: compound component architecture
<Card size="compact">
  <Card.Header className="border-b">
    <Card.Title>Analytics</Card.Title>
    <Card.Actions>
      <Button variant="ghost" size="sm" onClick={fn}>Filter</Button>
    </Card.Actions>
  </Card.Header>
  <Card.Body>
    <MetricsGrid />
  </Card.Body>
</Card>
```

### 2.2 Rule 2: Children Over Render Props
Prefer standard `children` composition over `renderHeader` or `renderItem` props unless virtualization specifically requires a factory function.

### 2.3 Rule 3: Decouple State Logic into Provider Contexts
Keep presentation components purely functional. Move state orchestration into dedicated context providers so complex state machines can be tested independently of DOM markup.

### 2.4 Rule 4: Modern React 19 Patterns
- **No `forwardRef`**: In React 19, `ref` is a standard prop. Pass `ref` directly without wrapping components in `forwardRef()`.
- **`use()` Hook**: Use the `use(Context)` API instead of `useContext()` for dynamic context consumption.

---

## 3. BENTO 2.0 ARCHITECTURE & THE 5 CARD ARCHETYPES

Modern SaaS feature pages and dashboards thrive on asymmetric bento compositions with perpetual micro-physics.

### Architecture Specs
- **Grid Layout**: Asymmetric 12-column grid or 70/30 split rows.
- **Surface**: High-elevation card background (`#16181D` dark / `#FFFFFF` light) with 1px hairline border (`rgba(255,255,255,0.08)` / `border-slate-200/60`).
- **Diffusion Shadow**: Wide, soft ambient shadow (`shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`).
- **Isolated Re-renders**: Any looping micro-animation MUST be isolated in an independent Client Component leaf with `'use client'` to prevent parent re-renders.

### The 5 Card Archetypes
1. **The Intelligent List**: A vertical card stack with an infinite layout swap. Items smoothly glide between positions using Framer Motion `layoutId`, simulating autonomous AI prioritization.
2. **The Command Input**: A search/prompt bar featuring an automatic typewriter animation cycling through contextual prompts, accompanied by a blinking cursor and shimmer processing indicator.
3. **The Live Status**: A service monitor tile with a breathing green pulse dot and an overshoot notification pill that springs into view and auto-settles.
4. **The Wide Data Stream**: A horizontal infinite ticker of metrics or partner logos (`x: ["0%", "-100%"]`) that glides effortlessly across the viewport.
5. **The Contextual UI**: A mock document interface featuring a staggered text highlight sweep that summons a floating micro-toolbar with sub-pixel iconography.

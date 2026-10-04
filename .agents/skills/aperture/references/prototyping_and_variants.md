# PROTOTYPING & VARIANT EXPLORATION
*Aperture Design & UX Direction — Design Divergence & Evaluation*

---

## 1. THE PRINCIPLE OF GENUINE DIVERGENCE

When exploring UI variants or redesigning a component under Aperture, minor CSS color swaps are prohibited. Three tints of the same card waste the review: the team learns nothing. 

Every variant must diverge along a **named architectural axis**:
- **Layout Axis**: Centered split vs. Asymmetric rail vs. Stacked full-width
- **Density Axis**: Spacious editorial vs. Packed high-density cockpit
- **Materiality Axis**: Hairline borders with zero shadows vs. Diffused depth vs. Neomorphic inset
- **Interaction Axis**: In-place expansion vs. Floating drawer vs. Contextual dialog
- **Motion Axis**: Instant 0ms utility vs. Snappy spring deceleration

---

## 2. THE 5 CANONICAL VARIANT ARCHETYPES

When requested to prototype alternatives for an interface element (e.g. `aperture variant <component>`), generate 3 distinct options selected from these archetypes:

### 1. The Quiet Utility Archetype
- **Philosophy**: Pure functional efficiency for 100×/day tools. The interface recedes; data commands focus.
- **Styling**: Monochromatic slate/zinc palette, 1px border dividers instead of card boxes, 0ms–120ms transitions.
- **When it wins**: B2B SaaS, developer tools, financial trading, daily internal tools.
- **Trade-off**: Lowest visual memorability.

### 2. The High-Craft Editorial Archetype
- **Philosophy**: Premium brand presence and intellectual authority.
- **Styling**: Large optical typography scale, deliberate asymmetric whitespace, 65ch body measure, hairline dividers.
- **When it wins**: High-ticket SaaS, developer marketing, documentation, case studies.
- **Trade-off**: Consumes vertical screen real estate.

### 3. The Dense Cockpit Archetype
- **Philosophy**: Maximum information density for expert operators.
- **Styling**: 24px–28px control heights, monospaced tabular figures, zero card boxing, keyboard shortcuts visible on all actions.
- **When it wins**: Analytics consoles, server logs, operational dashboards, audio/video editors.
- **Trade-off**: Higher initial cognitive load for novice users.

### 4. The Tactile Modern Archetype (Linear / Stripe Standard)
- **Philosophy**: Physicality, responsiveness, and premium delight.
- **Styling**: Off-black surface (`#0D0E11`), 1px translucent borders (`rgba(255,255,255,0.08)`), single electric accent, spring physics on active click (`scale(0.98)`).
- **When it wins**: Modern productivity apps, collaboration tools, creator software.
- **Trade-off**: Requires tight CSS/motion performance discipline.

### 5. The Bento 2.0 Feature Archetype
- **Philosophy**: Visual storytelling and engaging product explanation.
- **Styling**: Asymmetric 70/30 grid cards, subtle diffused ambient shadows, perpetual micro-interactions.
- **When it wins**: Feature overview pages, onboarding tours, executive summaries.
- **Trade-off**: Rigid grid structures can be challenging on extreme narrow mobile screens.

---

## 3. THE AESTHETIC VARIANCE ENGINE (TASTE-SKILL)

To prevent AI coding assistants from converging on the same generic "SaaS template", Aperture employs the **Aesthetic Variance Engine**. When generating high-agency frontend code or divergent prototypes, draw intentional pairings from these vibe and layout archetypes:

### 3.1 The 5 Vibe Archetypes
1. **Ethereal Glass**:
   - Translucent frosted surfaces (`backdrop-blur-xl bg-white/5` dark, `bg-white/60` light).
   - Double-bezel containment (`border border-white/10 ring-1 ring-inset ring-white/5`).
   - Typographic pairing: `Geist` light/regular with tight tracking.
   - Ideal for: Web3, premium AI tools, creative studios, next-gen developer platforms.
2. **Editorial Luxury**:
   - High-contrast typography: oversized display headings (`PP Editorial New`, `Clash Display`, or `Cabinet Grotesk`) paired with crisp sans body (`Geist` / `Satoshi`).
   - Generous asymmetric whitespace with sharp geometric containers or pill accents.
   - Atmospheric SVG noise grain (`opacity 0.03`).
   - Ideal for: High-ticket consulting, design tools, luxury commerce, architectural portfolios.
3. **Soft Structuralism**:
   - Calibrated neutral bases (Zinc/Slate) with a single saturated accent (Emerald, Cobalt, or Crimson).
   - Structural dividers (`divide-y`, `border-t`) over card containers; 12px–16px corner radius.
   - Tactile interactive feedback (`scale(0.98)` on `:active`).
   - Ideal for: Linear-style project management, developer consoles, fintech workflows.
4. **Cyber Technical**:
   - Off-black canvas (`#090A0C`), monospaced metadata badges (`Geist Mono`, `JetBrains Mono`).
   - Tabular figures on all numerical data (`tabular-nums`).
   - Hairline borders (`rgba(255,255,255,0.08)`), rapid staggered reveals (50ms cascade).
   - Ideal for: Observability, security dashboards, CLI tooling, infrastructure consoles.
5. **Monochromatic Brutalism**:
   - Stark black-and-white contrast, zero gradients, zero shadows.
   - Raw grid architecture, oversized typography (`clamp(2.5rem, 6vw, 6rem)`), hairline black borders.
   - Pure structural clarity and deliberate typography.
   - Ideal for: Developer blogs, experimental labs, artistic platforms, design manifestos.

### 3.2 The 3 Layout Archetypes
1. **Asymmetrical Bento**:
   - 70/30 or 1+2 split grids that break standard 3-equal-card predictability.
   - Background diversity: at least one cell with photography/illustration, one with data UI, one with typographic punch.
2. **Z-Axis Cascade**:
   - Layered elevation with recessed canvases, floating pill navigation, and elevated interactive panels.
3. **Editorial Split**:
   - 50/50 split-screen layout with left-aligned narrative copy locked to the viewport and right-aligned interactive showcase scrolling naturally.

---

## 4. PROTOTYPE HARNESS & INTERACTIVE VARIANT PICKER

When presenting multiple variants to a user, provide a lightweight interactive switcher so they can immediately toggle between variants in a live environment:

```tsx
// VariantPicker.tsx — Lightweight interactive switcher for comparing prototypes
'use client';
import React, { useState } from 'react';

export function PrototypeHarness({ variants }: { variants: Record<string, React.ReactNode> }) {
  const keys = Object.keys(variants);
  const [active, setActive] = useState(keys[0]);

  return (
    <div className="flex flex-col gap-6 w-full max-w-5xl mx-auto p-6">
      {/* Floating Pill Switcher */}
      <div className="flex items-center gap-1.5 p-1.5 bg-neutral-900/80 backdrop-blur-md rounded-full border border-white/10 w-fit mx-auto">
        {keys.map((key) => (
          <button
            key={key}
            onClick={() => setActive(key)}
            className={`px-4 py-1.5 text-xs font-medium rounded-full transition-colors ${
              active === key 
                ? 'bg-white text-black shadow-sm' 
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            {key}
          </button>
        ))}
      </div>

      {/* Live Variant Canvas (100% full scale context) */}
      <div className="w-full min-h-[400px] rounded-2xl border border-white/5 bg-neutral-950 p-8 flex items-center justify-center">
        {variants[active]}
      </div>
    </div>
  );
}
```

### Evaluation Protocol
1. **Full-Size Context**: Always evaluate variants at 100% full scale within their realistic surrounding context (e.g. a button inside an actual form; a card flanked by sibling rows). Never judge micro-UI scaled down to thumbnail size.
2. **Instant Switching**: Flipping between variants must happen instantaneously with zero transition animations so the user's eye detects spatial differences without motion interference.
3. **Honest Trade-off Reporting**: Present variants with an objective trade-off matrix:
   ```markdown
   | # | Variant | Named Axis | When It Wins | Its Cost / Compromise |
   |---|---|---|---|---|
   | 1 | Quiet | Border Dividers | High-frequency daily usage | Least memorable |
   | 2 | Editorial | Asymmetric Type | High-trust brand conversion | Consumes vertical height |
   | 3 | Tactile | Micro-Physics | Modern developer software | Higher motion discipline |
   ```

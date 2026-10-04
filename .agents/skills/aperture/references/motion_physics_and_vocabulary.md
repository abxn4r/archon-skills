# MOTION PHYSICS, TOKENS & VOCABULARY
*Aperture Design & UX Direction — Animation & Interaction Physics*

---

## 1. THE ANIMATION DECISION FRAMEWORK

Before writing any animation code, evaluate these three questions in order:

### 1.1 Should this animate at all? (Frequency Table)
Animation speed directly determines perceived software performance. Frequency dictates allowance:

| Frequency | Target Interaction | Decision |
|---|---|---|
| **100+ times/day** | Keyboard shortcuts, command palettes (`⌘K`), power-user nav | **0ms (Instant). Never animate.** |
| **Tens of times/day** | Button clicks, table filtering, row expansion | **100ms – 160ms** (Micro-tactile) |
| **Occasional (1–5/day)** | Modals, sheets, drawers, toast alerts | **200ms – 320ms** (Standard spatial) |
| **Rare / First-Time** | Onboarding tours, celebratory milestones | **400ms – 600ms** (Delightful) |

> **The Raycast Principle**: Tools used hundreds of times a day must execute instantly. An open/close transition on a command palette makes the entire application feel sluggish and disconnected from user intent.

### 1.2 What is the purpose?
Valid purposes:
- **Spatial continuity**: An element enters and exits from the same vector, preserving spatial orientation.
- **State indication**: A toggle morphs between paused and running states.
- **Feedback**: A button compresses on `:active` to confirm the click was heard.
- **Preventing jarring cuts**: Modals appearing without transition feel like DOM rendering glitches.

*If the only purpose is "it looks cool" and the user encounters it repeatedly, do not animate.*

### 1.3 What easing curve should it use?
- Is the element entering or exiting? → **`ease-out`** (immediate movement, deceleration on arrival).
- Is it moving or morphing between on-screen positions? → **`ease-in-out`** (smooth acceleration and deceleration).
- Is it a hover or color transition? → **`ease`**.
- Is it continuous motion (marquee, spinner, progress stream)? → **`linear`**.

**THE EASE-IN BAN**: Never use `ease-in` on UI elements. An entrance using `ease-in` delays initial movement, making a 250ms dropdown feel like 500ms because the user's eye waits during the slowest initial phase.

---

## 2. CANONICAL EASING & DURATION TOKENS

Built-in CSS easings lack physical punch. Aperture standardizes on high-tension custom bezier curves:

```css
:root {
  /* Snappy UI interaction & dropdown entrance */
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);

  /* Extreme spring-like deceleration (Linear / Vercel standard) */
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);

  /* iOS-like sheet & drawer slide (Ionic standard) */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);

  /* Shared element transitions & on-screen layout movement */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
}
```

### Duration Budget (Sub-300ms Rule):
- **Tactile Active Feedback**: `100ms – 160ms`
- **Tooltips & Micro Popovers**: `125ms – 200ms`
- **Dropdowns, Selects & Menus**: `150ms – 250ms`
- **Modals, Drawers & Overlays**: `200ms – 320ms`
- **Focal Marketing Moments**: `500ms – 800ms` (authored once, not repeated)

---

## 3. PHYSICALITY & COMPONENT ERGONOMICS

### 3.1 Never Animate from `scale(0)`
Solid objects in the physical world do not materialize from a singularity. Animating from `scale(0)` looks cheap. Always enter from **`scale(0.95)`** to **`scale(0.97)`** paired with `opacity: 0`:

```css
/* ❌ Amateur singularity entrance */
.entering { transform: scale(0); }

/* ✅ Physical balloon entrance */
.entering {
  transform: scale(0.95);
  opacity: 0;
  transition: transform 180ms var(--ease-out), opacity 180ms ease;
}
```

### 3.2 Origin-Aware Popovers vs Centered Modals
- **Popovers, dropdowns, and tooltips** must scale outward from their trigger element:
  ```css
  .popover {
    transform-origin: var(--transform-origin, top left);
  }
  ```
- **Modals and global alert dialogs** remain centered: `transform-origin: center`.

### 3.3 Tactile Feedback on `:active`
Every clickable button and interactive row must confirm user touch:
```css
.button {
  transition: transform 160ms var(--ease-out);
}
.button:active {
  transform: scale(0.975) translateY(1px);
}
```

### 3.4 Tooltips: Skip Delay on Subsequent Hovers
The first tooltip should wait `300ms` to prevent accidental activation. Once open, adjacent tooltips in a toolbar must open **instantly** (`0ms`) with zero transition delay:
```css
.tooltip {
  transition: transform 125ms var(--ease-out), opacity 125ms ease;
  transform-origin: var(--transform-origin);
}
.tooltip[data-instant] {
  transition-duration: 0ms !important;
}
```

### 3.5 Blur Bridging for Crossfades
When two overlapping states crossfade, seeing two transparent objects swap feels awkward. Add subtle `filter: blur(2px)` during the transition to bridge the visual gap and simulate a single morphing entity:
```css
.content-transitioning {
  transition: filter 180ms ease, opacity 180ms ease;
  filter: blur(2px);
  opacity: 0.7;
}
```

### 3.6 Zero-JS Entrances with `@starting-style`
Modern browsers allow animating element entry directly in CSS without React `useEffect` mounting flags:
```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 300ms var(--ease-out), transform 300ms var(--ease-out);

  @starting-style {
    opacity: 0;
    transform: translateY(12px);
  }
}
```

---

## 4. COMPOSITOR PERFORMANCE & HARDWARE ACCELERATION

1. **Transform and Opacity Only**: Never animate `width`, `height`, `margin`, `padding`, `top`, or `left`. Those trigger layout re-calculation on every frame (60fps jank).
2. **Ban `transition: all`**: Always declare explicit properties (`transition: transform 180ms, opacity 180ms`).
3. **SVG Transforms**: Always wrap animated paths in `<g>` and declare:
   ```css
   svg g.animated-icon {
     transform-box: fill-box;
     transform-origin: center;
   }
   ```
4. **CSS Transitions Over Keyframes**: CSS transitions can be interrupted and retargeted mid-motion when user actions reverse. Keyframes reset to frame 0.
5. **Reduced Motion Graceful Fallback**:
   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       animation-iteration-count: 1 !important;
       transition-duration: 0.01ms !important;
     }
   }
   ```

---

## 5. REVERSE-LOOKUP ANIMATION VOCABULARY (EMIL KOWALSKI)

Use exact industry terminology when planning or critiquing motion:

- **Origin-Aware Animation**: An element scaling out from the button that triggered it instead of from screen center.
- **Shared Element Transition**: An element traveling and morphing between views (e.g. thumbnail expanding into modal card).
- **Layout Animation**: Siblings smoothly sliding into place when an item is inserted, deleted, or reordered (`layoutId`).
- **Rubber-Banding**: Springy resistance and snap-back when dragging past boundary edges (iOS overscroll).
- **Continuity Transition**: Keeping the user spatially oriented by transforming existing geometry rather than replacing it.
- **Stagger**: Sequencing a cascade of children with small delays (`delay: index * 0.04s`).
- **Pop In**: Element appears with a slight overshoot and settles into position.
- **FLIP (First, Last, Invert, Play)**: High-performance layout animation technique reading before/after bounding rects and animating via `transform`.

---

## 6. MOBILE, GESTURE & EXPO MOTION STANDARDS (ANIMATE-EXPO & APPLE DESIGN)

For React Native, Expo, and touch-first mobile interfaces, apply these native motion and gesture guidelines:

1. **UI Thread Execution (Worklets)**:
   - All gesture responses and physics must execute strictly on the native UI thread using **React Native Reanimated** (`useAnimatedStyle`, `withSpring`, `withTiming`).
   - Never update React state (`useState`) during high-frequency gesture drags or pan movements to prevent frame drops across the JS bridge.
2. **Direct Manipulation & Velocity Preservation (Apple Design)**:
   - Elements touched by the user must follow the finger with zero lag and 1:1 displacement.
   - When released, spring animations must absorb the gesture's release velocity (`velocity: gesture.velocityY`), maintaining physical momentum rather than snapping to a pre-canned easing curve.
3. **Tactile Haptic Feedback Ergonomics (`expo-haptics`)**:
   - Provide micro-haptic confirmation at tactile boundaries:
     - `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)` on button clicks and toggle switches.
     - `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)` on drawer snapping, card reordering, or threshold crossing.
     - `Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success)` on successful submissions.
4. **Sheet & Drawer Transitions (`Vaul` / `@gorhom/bottom-sheet`)**:
   - Drawers must support smooth drag-to-dismiss with velocity thresholds.
   - Background canvas scales down to `scale(0.96)` with a subtle `border-radius: 16px` to simulate depth layering (the iOS modal sheet pattern).

# INTERACTIVE STATE MATRIX & ACCESSIBILITY
*Archon UI Component States -- Aperture Advisor*

---

## 1. COMPONENT STATE MATRIX

| Component | Default | Hover | Active / Pressed | Focus-Visible | Disabled | Loading / Skeleton |
|---|---|---|---|---|---|---|
| **Primary Button** | Accent solid bg, pure white text | +8% brightness, subtle shadow | -5% scale/translateY(1px) | 2px accent focus ring with 2px offset | opacity: 0.45, cursor: not-allowed | Spinner replaces text, width locked |
| **Secondary Button** | Transparent bg, border-neutral | rgba(255,255,255,0.06) bg | rgba(255,255,255,0.10) bg | 2px focus ring, outline: none | opacity: 0.40, pointer-events: none | Skeleton pulse |
| **Input Field** | Subtle dark bg, 1px border-neutral | Border transitions to border-hover | Active cursor, text entry | Border becomes accent, 2px focus shadow | Grayed bg, no focus ring | Shimmer placeholder |
| **Data Table Row** | Transparent bg, 1px bottom border | rgba(255,255,255,0.03) bg | Highlight selected tint | Keyboard focus row outline | Opacity 50% for archived | Skeleton row animation |

---

## 2. ACCESSIBILITY & KEYBOARD FOCUS INVARIANTS
1. **Focus Ring Offset**: Always use `outline: 2px solid var(--accent); outline-offset: 2px;`. Never use `outline: none` without providing an explicit `:focus-visible` replacement.
2. **Touch Targets**: Mobile / touch surfaces must provide a minimum interactive bounding box of 44x44px. Desktop utility can scale down to 28x28px with 32x32px hit slop.
3. **Contrast**: Normal text must satisfy WCAG AA (4.5:1). UI boundary markers must satisfy minimum 3.0:1.

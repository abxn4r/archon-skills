# DESIGN ACTION PLAYBOOKS
*Aperture Design & UX Direction — Multi-Action Execution Directives*

---

## 1. POLISH PLAYBOOK (`aperture polish [target]`)

> **Refinement preserves; Redesign replaces.** Polish keeps the incumbent visual identity, behavior, content, and code structure intact while elevating sub-pixel craft and execution.

### The 5-Stage Polish Triage
Fix defects strictly in order of user impact:
1. **Broken or Blocked Tasks & Inaccessible Paths**: Missing focus rings, inaccessible icon buttons, paste-blocking inputs, broken tab order.
2. **Missing UI States**: Loading skeleton, empty data state, error banner, active press feedback, disabled contrast.
3. **Flow, Hierarchy & Design-System Drift**: Aligning ad-hoc hex colors to semantic tokens, fixing font sizes to established scale.
4. **Visual & Motion Inconsistencies**: Concentric border radii, optical icon alignment, shadow-as-border layers, easing tokens.
5. **Code & Asset Cleanup**: Removing dead CSS, unused imports, redundant wrapper divs, temporary logs.

### The Verification Walk
Walk the complete interaction path before declaring polish complete:
- [ ] Reflow test at 320px, 768px, and 1440px viewports.
- [ ] Complete keyboard-only traversal (Tab, Shift+Tab, Enter, Space, Escape).
- [ ] Screen contrast check against background on both light and dark themes.
- [ ] Source diff review: eliminate accidental whitespace churn and orphaned abstractions.

---

## 2. DISTILL PLAYBOOK (`aperture distill [target]`)

> **Simplicity is not about removing features; it is about removing obstacles between users and their goals.**

### Pruning Vectors
1. **The Card Cull**: Generic cards are the lazy container. Remove boxing around metrics, features, and settings. Group instead with subtle hairline dividers (`border-t`, `divide-y`) or pure whitespace.
2. **One Primary Action**: Every screen has ONE dominant action. Demote competing buttons to secondary ghost/outline or tertiary text links.
3. **Progressive Disclosure**: Move advanced filters, infrequent configurations, and secondary metadata into disclosures (`<details>`, drawers, or expandable rows).
4. **Copy Halving**: Cut every paragraph in half, then remove redundant intros. If the heading explains the section, delete the subhead.
5. **Flatten Component Trees**: Remove pointless intermediate nesting divs (`<div className="wrapper"><div className="container">...</div></div>`).

---

## 3. HARDEN PLAYBOOK (`aperture harden [target]`)

> **A design that only works with perfect data is a prototype, not software.**

### The 6 Stress-Testing Axes
1. **Narrow Viewport (320px Minimum)**: Zero horizontal scroll on mobile. Multi-column grids must declare explicit single-column fallbacks below 768px.
2. **Text Explosion & Unbreakable Strings**: Test inputs and displays with 60-character strings without spaces (`verylongemailaddress@subdomain.reallylongcompany.com`). Verify `truncate`, `min-w-0`, or `break-words`.
3. **Localization Expansion (+30%)**: German and French translations expand text by 25%–35%. Ensure buttons and badges do not wrap or overflow containers.
4. **Asynchronous Edge States**:
   - Loading: Skeletal loader matching exact final layout dimensions.
   - Empty: Clear explanation of what belongs here and an immediate CTA to create/populate data.
   - Error: Contextual message with specific recovery path and retry button.
5. **Keyboard Traps & Modal Bounds**: Verify that opening a dialog locks background scroll, traps focus, and closes on Escape.
6. **Network Latency & Double Submits**: Form submit buttons must disable or show loading spinners immediately upon submission to prevent duplicate charges or records.

---

## 4. BOLDER PLAYBOOK (`aperture bolder [target]`)

> **"Bolder" means raising one element to the conviction the rest of the brand already implies — not adding visual noise.**

### The Skeleton Test
Strip all copy out of the planned section and inspect the bare structure:
- Does the geometry, whitespace, and typographic contrast communicate what this section is and why it matters without reading words?
- If the design only works once text is inserted, the boldness is in the copy length, not the design craft.

### Amplification Directives
- **Amplify what the system already owns**: Turn up the existing display scale, increase negative space, or make layout asymmetry dramatic (e.g. 70/30 bento split).
- **Give it a scroll peak**: The bolder section should act as a visual rhythm change in the page flow.
- **Quiet everything around it**: If every element gets louder, the section gets flatter. Make the focal move decisive and quiet secondary elements.

---

## 5. QUIETER PLAYBOOK (`aperture quieter [target]`)

> **Quiet design is harder than bold design. Subtlety requires mathematical precision.**

### De-escalation Directives
1. **Desaturate Accents**: Pull vibrant 100% saturation down to 70%–80%.
2. **Neutral Dominance**: Let high-craft neutrals (Zinc/Slate) do 90% of the visual work; restrict color to interactive focus points.
3. **Gentler Visual Weight**: Reduce bold heading weights from 800/900 down to 600 (SemiBold) or 500 (Medium).
4. **Remove Unmotivated Motion**: Drop infinite floating animations, bouncing arrows, and unnecessary hover zooms. Keep motion strictly functional (sub-200ms).
5. **Tinted Grays Over Raw Grays**: Use warm or cool tinted neutrals rather than flat grayscale to maintain depth without shouting.

---

## 6. CLARIFY PLAYBOOK (`aperture clarify [target]`)

> **Interface copy is design material. Clarity outranks cleverness.**

### Actionable Error Formula (3-Part Architecture)
Every error message must answer three questions:
1. **What happened**: "Unable to connect to production database."
2. **Why (when known)**: "The authentication token expired."
3. **How to recover**: "Generate a new token in API Settings and retry."

### Functional UX Copy Rules
- **Buttons name actions**: Use "Save Changes", "Delete Workspace", "Export CSV" — never ambiguous labels like "OK", "Submit", or "Proceed".
- **Destructive clarity**: For destructive actions, name the target object and consequence: "Delete 'Project Apollo' and all 14 attached datasets."
- **Persistent form labels**: Never use placeholder text as a label. Placeholders disappear upon typing, destroying field context.
- **Loading honesty**: Use determinate progress bars when data is known; never invent artificial progress animations.

---

## 7. DELIGHT PLAYBOOK (`aperture delight [target]`)

> **Delight is not generic whimsy or cartoon confetti; it is product character revealed through an unexpectedly considered detail.**

### The Delight Thesis
State in one sentence what the user should feel and why that feeling belongs to this product.
- **Success Moments**: Tailor celebration to effort. Routine saves need quick certainty (a crisp checkmark); completing an annual tax filing earns an authored transition.
- **Waiting States**: Provide authentic system insight (e.g., displaying current optimization phase) rather than generic circular spinners.
- **Discovery**: Micro-shortcuts, keyboard nav hints, or tactile physics on buttons that reward mastery.

**Non-Negotiable Guardrails**:
- Delight must NEVER delay or block the primary user task.
- Must NEVER play unprompted sound without user consent.
- Must remain pleasant after the 100th repetition — never become irritating friction.

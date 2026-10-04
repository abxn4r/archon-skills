# CHANGE REVIEW & BLAST RADIUS METHODOLOGY
*Aperture Design & UX Direction — PR & Diff Analysis*

---

## 1. CHANGE REVIEW VS. SCREEN REVIEW

When evaluating pull requests, git commits, or uncommitted branches, the reviewer’s central question is: **"Did this change make the interface worse?"**

- **Stay quiet about untouched legacy code**: In a PR review, reporting 30 pre-existing issues in a file the author merely touched for a 2-line fix is unproductive noise. Report up to 3 pre-existing issues as a courtesy in their own section; focus 95% of analysis on what the change caused.
- **Diff is evidence, not the surface**: A changed React component is evidence; its **blast radius** is the set of user-facing views that render it.

---

## 2. BLAST RADIUS EXPANSION RULES

1. **Standard Components (1 Hop)**: When a UI component is modified, expand the review 1 hop to its direct consumers and parent pages.
2. **Tokens & Primitives (2 Hops)**: When modifying global design tokens, CSS variables, theme definitions, or base atoms (e.g. `Button`, `Input`, `Dialog`), expand 2 hops because a 1-line change touches the entire product.
3. **Consumer Bound**: Review at most **5 direct consumers** to maintain thoroughness without unbounded context dilution. Explicitly report how many additional consumers were left uninspected.

---

## 3. READING THE REMOVED LINES (`-` SIDE OF DIFF)

Visual regressions are often completely invisible if you only inspect the final post-change code. You must inspect the `-` side of git hunks for removed signals:

- **Removed Accessibility**: Did the change remove `aria-label`, `aria-describedby`, `<label>`, or `role`?
- **Removed Focus States**: Did the change drop `:focus-visible`, `outline-offset`, or keyboard keydown handlers?
- **Removed Motion Protection**: Did a refactor drop `@media (prefers-reduced-motion)` or `useReducedMotion()`?
- **Removed Truncation Safety**: Did replacement markup drop `min-w-0` from a flex child?
- **Removed Error Boundaries**: Did a component rewrite omit fallback or empty states?

If a removal is not replaced by an equivalent mechanism, status it as a `Regression`.

---

## 4. FINDING CLASSIFICATION

Every identified issue must be tagged with exactly one classification:

- `[Introduced]`: The change directly authored this flaw.
- `[Regression]`: The change weakened or removed something that was previously correct.
- `[Pre-existing]`: The issue existed in touched code prior to this change (does not block PR approval).

### The Cheaper Fix Hierarchy
When proposing fixes, always recommend the cheapest effective option:
1. **Delete**: Remove redundant divider borders, excessive animations, or obsolete wrapper divs.
2. **Use the Platform**: Use native `<button>`, `<dialog>`, or browser focus rings over custom JS reimplementations.
3. **Reuse Existing Tokens**: Apply an existing project color or spacing token before proposing a new one.
4. **Correct the Value**: Adjust the easing curve, padding multiple, or hex contrast pair.
5. **Add**: Introduce a new token, wrapper, or media query only when steps 1–4 cannot solve the problem.

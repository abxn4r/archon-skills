# ACCESSIBILITY & WCAG 2.2 SPECIFICATION MATRIX
*Aperture Design & UX Direction — Universal Accessibility & Web Interface Standards*

---

## 1. WCAG 2.2 LEVEL AA CRITICAL INVARIANTS

Aperture holds all web and mobile software to the strict requirements of WCAG 2.2 Level AA and modern web interface guidelines.

### 1.1 Focus Not Obscured (2.4.11 AA & 2.4.12 AAA)
When an element receives keyboard focus, it must not be hidden under sticky headers, floating navbars, cookie banners, or drawer overlays.
```css
:focus, :target, [id] {
  scroll-margin-top: 80px;    /* clears fixed top navbar */
  scroll-margin-bottom: 60px; /* clears floating bottom sheet */
}
```

### 1.2 Target Size Minimum (2.5.8 AA)
- **Desktop Minimum**: At least **24×24 CSS px** bounding box.
- **Mobile Touch Standard**: At least **44×44 CSS px** with at least **8px spacing** between adjacent targets to eliminate mis-taps.
```css
.touch-target {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

### 1.3 Dragging Movements (2.5.7 AA)
Any dragging interface (Kanban cards, reorderable lists, sliders) MUST provide a single-pointer tap/click or keyboard alternative (such as up/down reorder buttons or keyboard shortcuts).

### 1.4 Redundant Entry (3.3.7 AA)
Never force users to re-enter information already provided in the same session (e.g. shipping identical to billing). Provide auto-fill or a single-click checkbox.

### 1.5 Accessible Authentication (3.3.8 AA)
- Never rely on cognitive function tests (math puzzles, complex memorization).
- **Never Block Paste**: Never intercept paste events (`onPaste={(e) => e.preventDefault()}`) on password or input fields. Password managers must function unhindered.

---

## 2. PRODUCTION ACCESSIBILITY CODE PATTERNS (ADDY OSMANI STANDARD)

### 2.1 Modal Focus Trap Pattern
Trap keyboard focus inside active modals so Tab/Shift+Tab cannot escape into the background DOM, and Escape closes the dialog:
```javascript
function openModal(modalEl) {
  // Prefer native HTML5 <dialog> when possible
  if (typeof modalEl.showModal === 'function') {
    modalEl.showModal();
    return;
  }

  const focusable = modalEl.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstEl = focusable[0];
  const lastEl = focusable[focusable.length - 1];

  modalEl.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstEl) {
        e.preventDefault();
        lastEl.focus();
      } else if (!e.shiftKey && document.activeElement === lastEl) {
        e.preventDefault();
        firstEl.focus();
      }
    }
    if (e.key === 'Escape') {
      closeModal(modalEl);
    }
  });

  firstEl?.focus();
}
```

### 2.2 Skip Links for Keyboard Navigation
Allows keyboard users to bypass repetitive header navigation:
```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <header><!-- Navigation --></header>
  <main id="main-content" tabindex="-1">
    <!-- Primary page content -->
  </main>
</body>
```
```css
.skip-link {
  position: absolute;
  top: -48px;
  left: 16px;
  background: var(--bg-surface, #0D0E11);
  color: var(--fg-primary, #EDEDED);
  padding: 8px 16px;
  border-radius: 6px;
  z-index: 1000;
  transition: top 150ms ease-out;
}
.skip-link:focus-visible {
  top: 16px;
  outline: 2px solid var(--accent, #5E6AD2);
}
```

### 2.3 Form Error Association & Focus Recovery
```html
<form novalidate>
  <div class="field" aria-live="polite">
    <label for="email" class="block text-sm font-medium mb-1">Work Email</label>
    <input 
      id="email" 
      type="email" 
      name="email"
      autocomplete="email"
      spellCheck={false}
      aria-invalid="true"
      aria-describedby="email-error"
      class="border-rose-500 focus-visible:ring-rose-500"
    />
    <p id="email-error" class="text-rose-500 text-xs mt-1" role="alert">
      Please enter a valid work email address (e.g., name@company.com).
    </p>
  </div>
</form>
```
**Submit Validation Invariant**: On failed form submission, prevent submit and shift focus immediately to the first invalid field:
```javascript
form.addEventListener('submit', (e) => {
  const firstError = form.querySelector('[aria-invalid="true"]');
  if (firstError) {
    e.preventDefault();
    firstError.focus();
  }
});
```

---

## 3. VERCEL WEB INTERFACE GUIDELINES

1. **Disable Spellcheck on Technical Inputs**: Add `spellCheck={false}` to emails, usernames, code fields, URLs, and token inputs.
2. **Single Hit Target for Radios & Checkboxes**: Ensure the label and checkbox share a single unified clickable target with zero dead zones between them.
3. **Submit Button State Management**: Keep submit button enabled until the network request begins (avoid disabling on blur). Show a loading spinner during the active request.
4. **Unsaved Changes Guard**: Warn users before accidental tab navigation when a form has unsaved edits (`beforeunload` or router guard).
5. **Non-Auth Autocomplete**: Use `autocomplete="off"` on non-authentication fields to prevent browser password managers from erroneously popping up over search boxes or filters.
6. **Live Regions for Async Updates**: Announce notifications, toast messages, and background sync outcomes via `aria-live="polite"`.

---

## 4. CONTRAST STANDARDS: WCAG 2 VS APCA

Aperture computes both WCAG 2 luminance ratios and modern APCA (Accessible Perceptual Contrast Algorithm) ratings:

| Content Element | WCAG 2.2 AA | APCA Minimum (Lc) | APCA Preferred (Lc) |
|---|---|---|---|
| **Body Text (< 18px / 14pt bold)** | **4.5:1** | **Lc 75** | **Lc 90** |
| **Headings & Large Labels (≥ 18px / 14pt bold)** | **3.0:1** | **Lc 60** | **Lc 75** |
| **Display Titles (≥ 36px)** | **3.0:1** | **Lc 45** | **Lc 60** |
| **UI Boundaries & Active Controls** | **3.0:1** | **Lc 30** | **Lc 45** |
| **Placeholder & Disabled Text** | *Informative* | **Lc 30** | **Lc 45** |

### Lightness Fix Protocol (Hold Hue & Saturation)
When fixing a failing color pair:
1. Hold hue and saturation constant.
2. Adjust perceived lightness away from the background until WCAG ratio ≥ 4.5:1.
3. Use Aperture's CLI: `python skills/aperture/scripts/check_contrast.py --fg "#7D93B0" --bg "#EEF2F7" --recommend`.

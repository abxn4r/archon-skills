# SCENARIO BREAKING & STRESS-TESTING MATRIX
*Aperture Design & UX Direction — Edge Case & Resilience Audit*

---

## 1. THE 6 STRESS-TESTING AXES

Before certifying any UI component, screen, or dashboard as production-ready, Aperture tests it against the 6 stress-testing axes to discover edge-case fragility:

### Axis 1: Content Length Stress
- **Empty String**: Does the container collapse into an invisible 0px sliver? Do floating labels clip into borders?
- **Single Character / Word**: Do buttons or tags sized for long text collapse or misalign?
- **Multi-Line Paragraph**: Does a container that assumed a single line overlap adjacent controls or truncate abruptly?
- **Unbreakable String**: Test with a 90-character URL (`https://verylongdomain...`) or long unbroken string (`Donaudampfschiffahrtsgesellschaft`). Does it blow out the viewport or wrap safely via `overflow-wrap: anywhere; min-w-0`?

### Axis 2: Content Shape Stress
- **Emoji Ingestion**: Do emoji characters cause line-height jumping, break baseline alignment, or slice vertically?
- **RTL & BiDi Text**: When rendered in Arabic or Hebrew, do margins, paddings, and icons properly flip? Does an LTR product name inside an RTL sentence render correctly?
- **Tall Diacritics**: Do accented characters (`Å`, `g`, `j`, `ŷ`) get clipped by tight line boxes (`leading-none`)?
- **Tabular Figures**: Do changing numbers in columns or timers cause horizontal layout jittering?

### Axis 3: Quantity Stress
- **Zero Items (Empty State)**: Does the UI show a broken blank white box, or an intentional empty state guiding the user on how to populate data?
- **Single Item**: Does a grid or list designed around 3+ items stretch awkwardly across the screen?
- **10× Realistic Volume**: What happens when an inbox or table receives 1,000 rows instead of 10? Does it paginate, virtualize, or crash browser memory? Do sticky headers stay pinned?

### Axis 4: Container Stress
- **320px Narrow Viewport**: The ultimate mobile stress test. Does any button or table trigger horizontal window scroll?
- **Squeezed Flex / Grid Sibling**: Does placing a complex component next to an expanding sidebar cause a min-content blowout?
- **Ultra-Wide 4K Viewports**: When opened on a 3840px display, does body copy stretch into an unreadable 300ch line, or is it contained by `max-w-7xl mx-auto`?

### Axis 5: State Stress
- **Skeleton Layout Shift**: Does the skeleton loader have the exact same bounding box as the loaded content, or does the page jump 80px when data arrives (CLS)?
- **Long Error Messages**: Does an API validation error wrap gracefully below the input, or does it clip inside an `overflow: hidden` parent?
- **Disabled State Usability**: Does a disabled control retain sufficient visual affordance to be discovered, while preventing accidental click events?

### Axis 6: Environmental Stress
- **OS Theme Crossover**: Does switching from dark mode to light mode preserve contrast, or do white hardcoded icons disappear into white backgrounds?
- **200% Browser Zoom**: Does the page reflow cleanly without overlapping text or obscuring interactive controls?
- **Reduced Motion Preference**: When the OS requests reduced motion, do animations stop or gracefully transition to simple opacity fades?

# Anti-AI Voice & De-Slopping Reference Guide

This reference provides the authoritative rules for eliminating machine-generated artifacts, ensuring all prose reads as authentic, practitioner-authored technical writing.

---

## 1. The Core Philosophy: Market-Weary Senior Practitioner

The voice is modeled on senior infrastructure and product engineers (Stripe, PostHog, ChartMogul, Userpilot):
- **Confident and direct**: Avoids apologies, over-hedging, and corporate fluff.
- **Slightly market-weary**: Has seen tools over-promise and under-deliver; values simplicity and verified outcomes.
- **Empirical**: Values numbers, terminal logs, and actual diffs over grand conceptual summaries.
- **Respects reader intelligence**: Never explains obvious boilerplate; moves quickly to the non-obvious engineering insight.

---

## 2. Hard Invariants (Zero Tolerance)

| Tell | Rule | Human Alternative |
|---|---|---|
| **Em-dashes (`—`) & En-dashes (`–`)** | **100% BANNED**. The primary statistical tell of LLMs. | Use a period (split sentence), a comma, a colon, or parentheses. |
| **Smart / Curly Quotes (`“`, `”`, `‘`, `’`)** | **BANNED**. Typical artifact of LLM chat pasting. | Use standard ASCII straight quotes (`"`, `'`). |
| **Throat-Clearing Openers** | Never announce what you are about to say. | Start directly with the subject, data point, or action. |
| **Binary Contrasts** | Ban "Not X, but Y" or "It's not just X, it's Y". | State Y directly without the rhetorical buildup. |
| **Negative Listing** | Ban "Not a tool. Not a script. A system." | State what it is in one clean clause. |
| **False Agency** | Inanimate things do not act. ("The code decides") | Name the engineer or use "you" to put the reader in the room. |
| **Dramatic Fragmentation** | Do not stack short pull-quote sentences. | Write complete sentences with natural syntactic flow. |
| **AI Buzzword Tapestry** | Ban *delve, tapestry, game-changer, seamless, elevate, leverage, robust, testament, pivotal, vibrant*. | Use precise verbs and concrete technical nouns. |
| **Rule-of-Three Compulsion** | LLMs constantly force ideas into trios. | Use two items, or one solid item with an explanation. |
| **Copula Avoidance** | LLMs write "serves as a testament to". | Write "is" or "shows". |

---

## 3. Burstiness & Cadence Engineering

AI text suffers from **metronomic cadence**: almost every sentence is between 14 and 20 words long. 

To achieve human burstiness:
1. **The Short declarative hammer (3 to 6 words)**: Drop a short, blunt sentence every 3-4 sentences.
2. **The Complex analytical clause (24 to 36 words)**: Follow with a multi-clause sentence explaining the mechanics, dependencies, and caveats.
3. **The Grounded closer (8 to 14 words)**: Close the paragraph on a concrete practical detail.

### Example Transformation

**AI Metronome (Fail)**:
> Model Context Protocol is an innovative standard for connecting AI models to data sources. It allows developers to seamlessly expose tools and context directly into coding assistants. By implementing this protocol, developers can significantly enhance their engineering workflows and build higher-quality applications faster.

**Human Burstiness (Pass)**:
> Most AI coding assistants fail on frontend tasks for one reason: they cannot see the live site. You spend twenty minutes copying hex codes, font weights, and layout paddings from Chrome DevTools into Cursor chat, hoping the model stitches them together without inventing classes. A local MCP server fixes this in one command. It crawls the target URL, extracts the exact Tailwind classes, and injects them directly into Cursor's prompt context.

---

## 4. De-Slopping Transformation Catalog

### 4.1 Banned Openers
- *AI*: "In today's fast-paced digital landscape, frontend developers face numerous challenges..."
- *Human*: "Frontend developers waste hours rebuilding interfaces that already exist in production."

- *AI*: "Here's the thing: context is everything when using Cursor."
- *Human*: "Cursor generates hallucinated styles when it lacks access to production CSS."

- *AI*: "Let's dive into how you can configure your MCP server."
- *Human*: "To configure the MCP server, add its stdio binary path to your settings file."

### 4.2 Eliminating Binary Contrasts
- *AI*: "It's not about writing more code, it's about providing better context."
- *Human*: "High-accuracy code generation requires precise context rather than longer prompts."

- *AI*: "The issue isn't the model's intelligence; it's the lack of real-world tokens."
- *Human*: "The model produces broken Tailwind classes because it never saw the computed styles."

### 4.3 Eliminating False Agency
- *AI*: "The workflow emerges naturally as the prompt evolves."
- *Human*: "You refine the prompt after checking the generated component in the browser."

- *AI*: "The data tells us that developers prefer automated scraping."
- *Human*: "In our benchmarks with 40 developers, 34 chose automated extraction over manual inspection."

### 4.4 Eradicating Empty Adverbs
- *AI*: "You can literally extract genuinely complex design systems completely seamlessly."
- *Human*: "You can extract complex design systems in 30 seconds."

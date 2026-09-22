# LLM, AGENTIC SYSTEM & MCP TOOL SECURITY AUDIT GUIDE
*Archon Security Architecture -- Saltzer Advisor Reference*

---

## 1. CORE DISCIPLINE & MINDSET

1. **Prompt injection alone is NOT a vulnerability**: Do not report text manipulation or jailbreak demonstrations as security findings unless they violate a concrete code-level boundary:
   - Untrusted content reaches another principal's context (cross-tenant bleed).
   - Untrusted content invokes authority the requester lacks (privilege escalation).
   - Untrusted content discloses data the caller cannot access directly (data exfiltration).
   - Untrusted content triggers a dangerous sink without authorization or intentional confirmation.
2. **Untrusted Inputs by Default**: Model outputs, persistent memory, tool schemas, and MCP responses are external, untrusted inputs. Always locate the code that validates them before they write durable state or feed a sink.
3. **Guardrails are NOT Security Boundaries**: System prompt admonitions (*"Do not reveal secrets"*, *"Do not run dangerous commands"*) are not deterministic security controls. Only deterministic code-level enforcement, schema validation, scoped credentials, and human-in-the-loop gates constitute boundaries.
4. **Action Binding vs. Authorization**: A user may have valid authority to perform an action (e.g., delete a workspace). However, if an attacker-controlled prompt injection payload induces the model to execute that action without the user's intentional knowledge or approval, this is an **action-binding failure**, regardless of whether the user possesses the necessary underlying permission.

---

## 2. CONTEXT, RETRIEVAL & MEMORY ATTACK CLASSES

### Indirect Prompt Injection via Ingested Content
- **Vulnerability**: Attacker-controlled text in RAG documents, indexed web pages, emails, database rows, ticket comments, or third-party API payloads enters an agent's context and overrides developer or user instructions.
- **Audit Steps**: Trace who can write to each ingested data source; verify tenant isolation in retrieval queries; check whether retrieved data is encapsulated in rigid prompt delimiters (e.g., XML `<user_data>...</user_data>`) with strict instructions not to interpret content as operational directives.

### Cross-Session & Cross-Tenant Context Bleed
- **Vulnerability**: Conversation history, semantic embeddings, retrieved chunks, or prompt caches are shared or keyed without complete tenant and ACL isolation.
- **Audit Steps**: Verify tenant filtering in vector database queries, search queries, and in-memory caches. Ensure batch retrieval or background workers cannot accidentally mix context between distinct principals.

### Persistent Memory & Second-Brain Poisoning
- **Vulnerability**: Attacker-influenced content or untrusted model summaries are saved into durable agent memory (e.g., user profiles, custom instructions, knowledge graphs) that subsequently conditions future privileged tasks.
- **Audit Steps**: Audit memory write, merge, and deletion endpoints. Verify provenance tagging (distinguishing verified user directives from external tool observations). Check whether untrusted data can alter permanent agent behavioral rules.

---

## 3. TOOL DISPATCH & ACTION BINDING ATTACK CLASSES

### Confused-Deputy Authority & Excessive Agency
- **Vulnerability**: The agent executes tools using a broad service account or elevated system credential, while the tool handler fails to verify the requesting end-user's granular authorization on the target resource.
- **Audit Steps**: Verify that the tool execution layer validates the effective end-user identity and permissions per resource, not just the model/agent runner's identity.

### Action Confirmation & Intent Binding
- **Vulnerability**: A UI prompts the user to approve action $A$ with arguments $X$, but execution executes mutated arguments $X'$, targets a different resource $R'$, or executes in a subsequent unconfirmed turn.
- **Audit Steps**: Verify that human approval cryptographically or deterministically binds: (1) normalized tool name, (2) complete argument hash, (3) target resource ID, (4) session identity, and (5) expiration nonce. Ensure retried or resumed sessions cannot execute mutated actions under prior approvals.

### Tool Schema vs. Dispatcher Disagreement
- **Vulnerability**: Tool parameter schemas defined for the LLM accept aliases, type coercions, permissive object types, or unvalidated extra keys that the underlying implementation handles insecurely or executes with unexpected defaults.
- **Audit Steps**: Compare the LLM-visible JSON schema against the internal dispatcher parsing logic. Check for parameter smuggling, prototype pollution, path traversal in coerced string arguments, and unvalidated dictionary inputs.

### Tool-Argument Injection into Dangerous Sinks
- **Vulnerability**: LLM-generated arguments pass directly into SQL queries, operating system commands, file paths, URL fetching (SSRF), or serialization sinks.
- **Audit Steps**: Ensure tool handlers treat LLM arguments with the same skepticism as raw HTTP query parameters. Enforce parameterization, realpath traversal defenses, and strict URL allowlists.

---

## 4. MCP (MODEL CONTEXT PROTOCOL) & SUB-AGENT SECURITY

### MCP Server & Tool Identity Confusion
- **Vulnerability**: Multiple MCP servers connected to the same client declare identical tool names or resource URIs, allowing a low-trust server to shadow or hijack invocations intended for a high-trust server.
- **Audit Steps**: Verify namespace enforcement (e.g., `server_name__tool_name`). Verify connection-specific routing and request-ID binding. Ensure server reconnects cannot redirect pending requests.

### MCP Metadata & Prompt Injection via Prompts/Resources
- **Vulnerability**: Untrusted MCP servers supply malicious prompt templates, completion hints, or resource contents designed to hijack the client assistant.
- **Audit Steps**: Treat MCP server-provided prompts and completion templates as untrusted data. Ensure administrative approval is required before installing or enabling external MCP servers.

### Unbounded Sub-Agent Trust Inheritance
- **Vulnerability**: Delegated sub-agents inherit ambient credentials, full host filesystem access, or unconstrained network egress from the parent orchestrator.
- **Audit Steps**: Enforce strict privilege narrowing for subagents (read-only worktrees, scratch-directory isolation, empty environment variables, and explicit tool allowlists).

---

## 5. SUPPLY CHAIN & RUNTIME CONFIGURATION

- **Strict Package Pinning**: MCP servers executed via `npx` or `uvx` must specify exact immutable version tags (`package@1.2.3`). Unpinned package invocations (`npx package`) represent an immediate supply-chain vulnerability.
- **Deterministic MCP Configuration Auditing**: Run the deterministic auditor script on every MCP configuration file before deployment:
  ```powershell
  python skills/saltzer/scripts/audit_mcp_config.py --file mcp.json
  ```
- **Zero Committed Plaintext Secrets**: Ensure API keys, tokens, and connection strings are injected strictly via environment variables, never hardcoded in `.mcp.json` or system prompts.

---

## 6. VALIDATION RULES (APPLY BEFORE REPORTING)

1. **State the complete boundary path**:
   - Lower-trust principal / input source &rarr; Model context &rarr; Dispatcher / Tool handler &rarr; Downstream resource / sink &rarr; Observable security impact.
2. **Verify preventing layers**: If deterministic schema validation, parameter binding, or human-in-the-loop authorization prevents the downstream effect, classify the observation as an **Informational hardening note**, not a vulnerability.
3. **Distinguish certainty**: If the vulnerability depends on live model stochastic behavior or unobserved external prompt templates, record as `needs_validation` with a concrete local test plan.

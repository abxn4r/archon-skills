# LLM, AGENTIC SYSTEM & MCP TOOL SECURITY CHECKLIST
*Archon Security Architecture -- Saltzer Advisor*

---

## 1. PROMPT INJECTION & UNTRUSTED CONTEXT
- [ ] **Direct Prompt Injection**: Clear structural separation between developer system instructions, retrieved user documents, and untrusted inputs.
- [ ] **Indirect Prompt Injection**: Web pages, external API payloads, database records, and emails treated as untrusted data; never allow retrieved text to silently override system commands.
- [ ] **Delimitation**: Use rigid prompt delimiters (e.g. XML tags `<user_input>...</user_input>`) and instruct the model never to parse user text as command directives.

---

## 2. AGENTIC TOOL EXECUTION & PRIVILEGE BOUNDARIES
- [ ] **No Raw Shell Tools**: MCP tools and agent toolkits must never expose raw shell execution (`bash`, `sh`, `powershell`, `cmd`).
- [ ] **Filesystem Sandboxing**: Tools must restrict read/write access to project workspace subdirectories. Root filesystem access (`/`, `C:\`, `~`) is strictly forbidden.
- [ ] **Human-in-the-Loop (HITL)**: Irreversible or high-consequence operations (deleting data, executing external transactions, sending external emails, dropping tables) require explicit user approval.
- [ ] **Network Egress Controls**: Tool HTTP requests restricted to explicitly whitelisted domains; prevent Server-Side Request Forgery (SSRF) against internal metadata services (`169.254.169.254`).

---

## 3. MCP CONFIGURATION & SUPPLY CHAIN
- [ ] **Package Pinning**: All MCP servers executed via `npx` or `uvx` must specify exact version tags (`package@1.2.3`). Unpinned package execution triggers a HIGH finding.
- [ ] **Secret Management**: API keys and database credentials injected via runtime environment variables; zero plaintext secrets in MCP JSON configs.
- [ ] **Empirical Audit**: Run `python skills/saltzer/scripts/audit_mcp_config.py` to deterministically verify all MCP server definitions before deployment.

# OWASP TOP 10 FOR MODEL CONTEXT PROTOCOL (MCP) & AGENTIC TOOLS
*Archon Security Architecture -- Saltzer Advisor*

---

## 1. MCP01: ARBITRARY COMMAND & TOOL INJECTION
- **Risk**: MCP servers exposing raw shell access (`cmd.exe`, `bash`, `powershell.exe`, or unvalidated shell execution functions) allowing LLMs or prompt injection payloads to execute arbitrary host commands.
- **Defense**: Never expose raw shells as MCP tools. Whitelist discrete, tightly constrained executables with validated arguments.

## 2. MCP02: OVER-PRIVILEGED FILESYSTEM ACCESS
- **Risk**: Granting tools recursive read/write access to filesystem roots (`C:\`, `/`, `~`, or wildcard `*`), exposing SSH keys, `.env` files, browser caches, and credentials.
- **Defense**: Strictly scope tool permissions to designated project subdirectories. Never grant recursive root access.

## 3. MCP03: SENSITIVE CONTEXT LEAKAGE & SECRET EXPOSURE
- **Risk**: MCP tool configurations embedding plaintext API tokens, database connection strings, or cloud keys in configuration `env` or `args` blocks.
- **Defense**: Store secrets in system keychains or runtime environment variables; never commit plaintext secrets in config files.

## 4. MCP04: SSRF & UNCONTROLLED NETWORK ACCESS
- **Risk**: Tools capable of performing arbitrary HTTP requests making internal network calls to cloud metadata endpoints (`169.254.169.254`), localhost dev servers, or internal VPC services.
- **Defense**: Restrict outbound requests with strict domain whitelisting and block all link-local, loopback, and private IP CIDRs.

## 5. MCP05: INDIRECT PROMPT INJECTION VIA TOOL RESPONSES
- **Risk**: Tool outputs (web scrape, database fetch, email body) containing malicious prompt injections that hijack the assistant's subsequent actions.
- **Defense**: Treat all tool returns as untrusted user data. Maintain strict system prompt delimiters and enforce human-in-the-loop for destructive operations.

## 6. MCP06: INSECURE PARAMETER & SCHEMA VALIDATION
- **Risk**: Tool schemas that fail to validate input boundaries (path traversal `../`, command separators `;`, `&`, `|`, or format string exploits).
- **Defense**: Enforce rigid schema typing, sanitize file paths using resolved realpaths, and reject unvalidated input.

## 7. MCP07: HUMAN-IN-THE-LOOP (HITL) BYPASS
- **Risk**: Destructive tools (file deletion, database drops, git push, money transfer) executing automatically without user authorization.
- **Defense**: Require explicit user confirmation for irreversible or destructive actions.

## 8. MCP08: MCP STDIO PROCESS HIJACKING & ESCAPE
- **Risk**: Stdio communication channels manipulated via malformed JSON-RPC frames or process injection.
- **Defense**: Run MCP server processes under unprivileged service accounts with constrained process tokens.

## 9. MCP09: UNPINNED PACKAGES & SUPPLY CHAIN COMPROMISE
- **Risk**: Running `npx -y package` or `uvx package` without version pinning, making the system vulnerable to package takeover or upstream poisoning.
- **Defense**: Always pin exact versions (e.g., `package@1.2.3`) and verify checksums/hashes.

## 10. MCP10: INSUFFICIENT LOGGING & AUDIT TRAILS
- **Risk**: Inability to reconstruct agent actions after a compromise due to ephemeral or omitted tool invocation logs.
- **Defense**: Maintain persistent, tamper-evident audit logs of every tool invocation and parameter set in `.archon/` or `~/.archon/`.

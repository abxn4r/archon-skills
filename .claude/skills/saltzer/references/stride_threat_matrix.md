# STRIDE THREAT MODEL FOR AGENTIC SYSTEMS
*Archon Security Architecture -- Saltzer Advisor*

---

| Threat Category | Agentic System Surface | Attack Vector | Saltzer Invariant & Defense |
|---|---|---|---|
| **S - Spoofing** | Subagent identity, tool credentials | Untrusted agent impersonating coordinator | Mutual authentication, authenticated session tokens |
| **T - Tampering** | Tool arguments, persistent memory | Prompt injection tampering with memory | Validate JSON schemas, verify disk hashes, sanitization |
| **R - Repudiation** | Destructive commands, file writes | Agent denying action origin | Non-repudiable audit logs in persistent memory (`.archon/`) |
| **I - Information Disclosure** | Context window, tool outputs | Leaking `.env` or user profile data to external API | Zero outbound network calls without explicit domain whitelist |
| **D - Denial of Service** | Infinite tool recursion, unbounded context | Runaway loops exhausting tokens or process memory | Strict loop limits, timeouts (max 10s), execution budgets |
| **E - Elevation of Privilege** | Stdio escape, terminal sandbox breakout | Agent escaping sandbox to host admin | Principle of Least Privilege: run as standard user, block admin escalation |

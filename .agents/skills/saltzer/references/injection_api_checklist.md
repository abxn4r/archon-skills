# INPUT VALIDATION, INJECTION DEFENSE & API SECURITY CHECKLIST
*Archon Security Architecture -- Saltzer Advisor*

---

## 1. INPUT VALIDATION & INJECTION PREVENTION
- [ ] **SQL Injection**: All database interactions use parameterized queries or prepared statements; zero string interpolation or format strings in queries.
- [ ] **Command Injection**: Zero execution of raw shell processes (`sh`, `bash`, `cmd`, `powershell`). Use explicit argument lists (`subprocess.run(["cmd", "arg1"])`) without `shell=True`.
- [ ] **Path Traversal**: Validate and canonicalize all file paths using realpaths. Reject `../`, null bytes, and verify target resides within designated project sandbox.
- [ ] **Allowlist Validation**: Enforce strict boundary validation using allowlists for characters, formats, enums, and lengths.
- [ ] **File Upload Validation**: Validate file contents via magic bytes/signatures, not user-supplied file extensions or MIME types. Store outside web root.

---

## 2. OUTPUT ENCODING & CLIENT PROTECTION
- [ ] **Context-Aware Encoding**: HTML, JavaScript, URL, and CSS context-specific escaping applied before rendering untrusted input.
- [ ] **Content Security Policy (CSP)**: Restrict script execution to trusted nonces or hashes; forbid `unsafe-inline` and `unsafe-eval`.
- [ ] **Anti-MIME Sniffing**: Header `X-Content-Type-Options: nosniff` present on all HTTP responses.
- [ ] **Frame Protection**: `X-Frame-Options: DENY` or `frame-ancestors 'none'` to block clickjacking.

---

## 3. API SECURITY & RATE LIMITING
- [ ] **Authentication & Scoping**: Every API route authenticated server-side; reject unauthenticated access to internal endpoints.
- [ ] **Rate Limiting**: Applied to IP, user ID, and API token buckets with `429 Too Many Requests` and standard `Retry-After` headers.
- [ ] **CORS Restrictions**: Explicit origin allowlists; never use `Access-Control-Allow-Origin: *` with credentials.
- [ ] **Signature Verification**: Webhooks and callbacks verified using HMAC signatures (`X-Hub-Signature-256`) with timing-safe comparison.
- [ ] **Information Disclosure**: Stack traces, server versions, database schema names, and internal paths stripped from all production error responses.

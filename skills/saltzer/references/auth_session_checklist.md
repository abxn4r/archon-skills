# AUTHENTICATION, AUTHORIZATION & SESSION SECURITY CHECKLIST
*Archon Security Architecture -- Saltzer Advisor*

---

## 1. AUTHENTICATION CONTROLS
- [ ] **Server-Side Enforcement**: Identity verification is performed server-side on every authenticated request.
- [ ] **Password Hashing**: Passwords stored using modern adaptive algorithms (Argon2id, bcrypt with cost >= 12, PBKDF2 with SHA-256 and >= 600k iterations).
- [ ] **Account Enumeration Prevention**: Generic error messages on login/reset ("Invalid credentials", "If an account exists, instructions have been sent").
- [ ] **Brute Force Defense**: Rate limiting and progressive exponential backoff applied to login, registration, and password-reset endpoints.
- [ ] **Multi-Factor Authentication (MFA)**: TOTP / WebAuthn enforced for sensitive administrative operations.
- [ ] **SSO / OAuth Integrity**: State parameter validation, PKCE (Proof Key for Code Exchange), strict redirect URI allowlists, and nonce checks.

---

## 2. AUTHORIZATION & ACCESS CONTROL
- [ ] **Complete Mediation**: Authorization checked on every resource access server-side; UI checks are purely visual ergonomics.
- [ ] **Direct Object References (IDOR)**: Numerical or predictable IDs validated against the authenticated tenant/user scope (`WHERE id = ? AND tenant_id = ?`).
- [ ] **Privilege Separation**: Strict role-based (RBAC) or attribute-based (ABAC) boundaries separating user, tenant, and super-admin actions.
- [ ] **Principle of Least Privilege**: Service accounts and internal tokens granted minimal database and API permissions.
- [ ] **Administrative Re-Authentication**: Sensitive actions (deleting tenants, exporting data, changing billing) require password confirmation or step-up MFA.

---

## 3. SESSION & TOKEN MANAGEMENT
- [ ] **Token Entropy**: Cryptographically secure random number generators (`secrets` module, `/dev/urandom`) with >= 128 bits of entropy.
- [ ] **Cookie Security Flags**: `HttpOnly`, `Secure`, and `SameSite=Lax` (or `Strict`) set on all session cookies.
- [ ] **Session Invalidation**: Immediate server-side token revocation upon user logout, password reset, or privilege revocation.
- [ ] **JWT Verification**: Explicit algorithm enforcement (reject `none` or unexpected HMAC/RSA confusion); validate `exp`, `nbf`, and `iss`.
- [ ] **Token Rotation**: Refresh tokens rotated upon use; detect replay attempts and invalidate entire token family.

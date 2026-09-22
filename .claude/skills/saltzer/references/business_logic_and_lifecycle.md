# BUSINESS LOGIC, LIFECYCLE & FEATURE ABUSE AUDIT GUIDE
*Archon Security Architecture -- Saltzer Advisor Reference*

---

## 1. CORE DISCIPLINE

Business logic flaws cannot be detected by automated vulnerability scanners. They stem from deviations between the intended business requirements and the software's actual state transitions under adversarial input.
- **Rule of Intent**: Do not ask merely *"does a permission check exist?"*; ask *"is this the correct check for the complete business operation?"*
- **Rule of Rollback**: Verify what occurs during partial failures. If step 2 of a 3-step operation fails, is step 1 rolled back or does it leave an exploitable dangling state?
- **Rule of Invariant**: For every workflow, identify the invariant that must hold true (e.g., *account balance >= 0*, *order items cannot change after payment authorization*).

---

## 2. STATE MACHINE & CONCURRENCY ATTACK CLASSES

### State Machine Violations & Step Skipping
- **Vulnerability**: Multi-step workflows (e.g., registration, checkout, KYC verification, password reset, multi-factor challenge) permit skipping intermediate steps, replaying completed steps, or navigating backwards.
- **Audit Steps**: Trace the state transition table. Can an attacker call `POST /checkout/confirm` without calling `POST /checkout/pay`? Does the application track step completion server-side or rely on client-supplied flags?

### Partial Failure & Rollback Inconsistencies
- **Vulnerability**: Distributed or multi-table updates where a failure in a secondary step leaves primary records in a mutated, inconsistent state.
- **Audit Steps**: Inspect exception handlers, database transactions, and saga orchestrators. If an email verification fails or third-party webhook times out, are created accounts or assigned permissions revoked?

### Concurrency & Non-Atomic Race Conditions
- **Vulnerability**: Check-then-act operations that allow double-spending, coupon reuse, over-allocation of inventory, or duplicate permission grants when executed concurrently.
- **Audit Steps**: Look for non-atomic database read-then-write operations without pessimistic locking (`SELECT ... FOR UPDATE`), optimistic locking with version checks, or atomic update constraints (`UPDATE accounts SET balance = balance - X WHERE balance >= X`).

### Numeric, Currency & Quantity Manipulation
- **Vulnerability**: Business endpoints processing negative quantities, zero amounts, extreme integer values, floating-point precision inaccuracies, or string-to-number type coercion quirks.
- **Audit Steps**: Audit all quantity, price, transfer, and balance calculation paths. Verify bounds checking at API boundaries: reject negative inputs, non-integer cents, and scientific notation (`1e10`).

---

## 3. FEATURE ABUSE & DATA LEAKAGE ATTACK CLASSES

### Export & Backup as Exfiltration
- **Vulnerability**: High-volume export or backup features (e.g., CSV export, database snapshots, archive downloads) that bypass normal row-level access controls or object filtering.
- **Audit Steps**: Verify whether exports include soft-deleted records, drafts, internal metadata, credentials, or data belonging to sibling tenants. Ensure the export worker evaluates authorization for every single item included in the export batch.

### Import & Restore as Injection
- **Vulnerability**: Bulk import (CSV, JSON, XML) or restore functions that bypass validation applied during standard single-item creation.
- **Audit Steps**: Verify that imported records undergo full schema validation, authorization checks, and sanitization. Can an import overwrite existing records belonging to other users or set administrative fields (e.g., `role: "admin"`)?

### Search, Filter & Sort as Information Oracle
- **Vulnerability**: Search endpoints, filter parameters, or sorting options that reveal the existence or content of private, inaccessible records through side-effects or ordering differences.
- **Audit Steps**:
  - *Response timing / Error differentials*: Does querying for an unshared resource return `404 Not Found` vs. `403 Forbidden`?
  - *Result counts*: Does searching with a filter leak whether a specific record exists in another tenant?
  - *Sorting as oracle*: Does sorting by a sensitive hidden column (e.g., `salary`, `ssn`, `is_vip`) reveal the ranking of restricted records?

### Preview, Draft & Staging Leakage
- **Vulnerability**: Unauthenticated or weakly tokenized preview URLs, draft APIs, or staging endpoints leaking unreleased content or sensitive internal assets.
- **Audit Steps**: Verify token entropy, expiration, and strict single-resource binding for preview links. Ensure CDN caching rules do not cache draft or preview responses on public edge nodes.

### Webhook & Notification Callback SSRF
- **Vulnerability**: Features allowing users to configure webhook URLs, avatar URLs, or callback endpoints that the application backend fetches.
- **Audit Steps**: Check for Server-Side Request Forgery (SSRF) defenses: DNS rebinding protections, blocking private/internal IP ranges (RFC 1918, RFC 3927 `169.254.169.254`, IPv6 loopback `::1`), and validating redirect targets.

---

## 4. CHAINED VULNERABILITIES & SECOND-ORDER ATTACKS

- **Cross-Component Trust Gaps**: Component $A$ validates input and passes it to Component $B$. Does Component $B$ assume stronger invariants than $A$ guaranteed (e.g., string length truncation, Unicode normalization, type conversion)?
- **Second-Order Execution**: Data that was safe when written to storage becomes dangerous when read by a different subsystem (e.g., a username rendered into a PDF generator, an internal path used in an archive extraction, or a stored tag used in a cache key).
- **Rollback and Undelete Re-authorization**: Features that restore soft-deleted items or rollback revisions must re-evaluate current authorization, ownership, and integrity constraints.

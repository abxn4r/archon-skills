# DATA ISOLATION, MULTI-TENANCY & LIFECYCLE AUDIT GUIDE
*Archon Security Architecture -- Saltzer Advisor Reference*

---

## 1. CORE DISCIPLINE & TENANCY INVARIANTS

In multi-tenant SaaS applications, tenant boundaries are the primary trust barrier.
- **Tenant Scope Everywhere**: Every database query, cache key, search filter, background job payload, and export task must be explicitly scoped to the authenticated tenant.
- **Implicit vs. Explicit Scoping**: Relying on application-level filtering after fetching data (`records.filter(r => r.tenantId === currentTenant)`) is an anti-pattern. Scoping must be enforced at the storage engine level (Row-Level Security, partition keys, parameterized `WHERE tenant_id = ?`).
- **Absence of Proof is Not Proof of Safety**: If multi-tenancy depends on deployment-level VPC peering, database user switching, or proxy routing that is not visible in the repository, document the condition as `needs_validation` with a verification plan.

---

## 2. TENANT ISOLATION ATTACK CLASSES

### Cross-Tenant Query Bleed & Missing WHERE Clauses
- **Vulnerability**: Endpoints, bulk operations, or batch jobs that query resources by object ID (`SELECT * FROM items WHERE id = ?`) without binding the tenant ID (`AND tenant_id = ?`).
- **Audit Steps**: Review all ORM queries, custom SQL builders, and GraphQL resolvers. Check whether batch APIs, bulk update endpoints, or nested relational queries (`include: { comments: true }`) omit tenant constraints on joined tables.

### Shared Cache Key Collisions & Context Bleed
- **Vulnerability**: Shared key-value stores (Redis, Memcached) caching objects using global keys (`cache:user:123`, `cache:item:456`) without tenant prefixing (`cache:{tenant_id}:user:{user_id}`).
- **Audit Steps**: Inspect cache key generation helpers. Can Tenant $A$ poison, invalidate, or retrieve cached records belonging to Tenant $B$? Are session tokens or permissions cached without tenant binding?

### Search Index & Vector Store Isolation Failures
- **Vulnerability**: Elasticsearch, OpenSearch, Solr, or vector database (Pinecone, Qdrant, Milvus) queries executing without mandatory tenant filter clauses in the query payload.
- **Audit Steps**: Audit all search client wrappers. Does every query include a mandatory `filter: [{ term: { tenant_id: current_tenant } }]`? Can a user inject wildcard syntax (`*`) or boolean operators (`OR 1=1`) to bypass filtering?

### Cross-Tenant Object Linking & Foreign Key Forgery
- **Vulnerability**: Creating or updating an object in Tenant $A$ with a foreign key referencing an object owned by Tenant $B$ (e.g., assigning a project to an unauthorized organization or linking an integration belonging to another customer).
- **Audit Steps**: Verify foreign-key validation during writes. The application must prove that both the source record and all referenced parent/child records belong to the active tenant.

---

## 3. LIFECYCLE & RETENTION ATTACK CLASSES

### Soft-Delete Authorization Bypasses
- **Vulnerability**: Soft-deleted records (`deleted_at IS NOT NULL`) accessible via direct ID lookups, search endpoints, batch exports, or related resource joins.
- **Audit Steps**: Verify global query filters or ORM scopes for soft-delete flags. Ensure deleted records are excluded from permissions checks, search indexes, and active caches.

### Undelete & Revision Restore Privilege Escalation
- **Vulnerability**: Restoring a soft-deleted item or rolling back to a previous revision without re-verifying current authorization or quota constraints.
- **Audit Steps**: Verify that the restore/rollback handler checks whether the actor currently has permission to create or own that item, whether the item's target container still belongs to their tenant, and whether active quota limits are respected.

### Data Export & Backup Cross-Tenant Leakage
- **Vulnerability**: Asynchronous export jobs generating downloadable files (S3 URLs, zip archives) with predictable filenames or unauthenticated access links.
- **Audit Steps**: Verify pre-signed S3 URL expiration, tenant scoping in export generation workers, and access control on the final download endpoint.

### Migration & Background Job Isolation
- **Vulnerability**: Asynchronous task queues (Celery, BullMQ, Sidekiq) enqueuing jobs with raw object IDs but lacking tenant context in the worker execution environment.
- **Audit Steps**: Trace background job processors. Ensure workers reconstruct and validate the tenant execution context before processing payloads.

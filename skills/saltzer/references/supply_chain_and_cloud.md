# SUPPLY CHAIN, CI/CD & CLOUD DEPLOYMENT AUDIT GUIDE
*Archon Security Architecture -- Saltzer Advisor Reference*

---

## 1. CI/CD WORKFLOWS & PIPELINE SECURITY

GitHub Actions, GitLab CI, and deployment pipelines operate at the highest privilege tier, often holding cloud deployment credentials and production access.

### Untrusted Script & Expression Injection
- **Vulnerability**: Workflow `run` steps interpolating untrusted GitHub context variables directly into bash/powershell commands (e.g., `run: echo "${{ github.event.issue.title }}"`).
- **Audit Steps**: Search for inline context expressions `${{ github.event... }}` in `run:` blocks. Context values must be passed strictly through environment variables:
  ```yaml
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}
  run: |
    echo "$ISSUE_TITLE"
  ```

### `pull_request_target` Misconfiguration
- **Vulnerability**: Workflows triggered by `pull_request_target` (which runs in the context of the base repository and has access to secrets) checking out the pull request head commit (`ref: ${{ github.event.pull_request.head.sha }}`) and executing build scripts or tests.
- **Audit Steps**: Verify that `pull_request_target` workflows NEVER checkout untrusted fork code and run executable steps (`npm test`, `make`, build scripts). Fork code execution must be isolated in `pull_request` triggers without access to write tokens or production secrets.

### Unpinned Third-Party Actions & Dependencies
- **Vulnerability**: Referencing GitHub Actions by mutable branch or tag names (e.g., `uses: actions/checkout@v3`, `uses: thirdparty/action@main`) rather than immutable full commit SHAs.
- **Audit Steps**: Require commit SHA pinning with comment annotations (e.g., `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1`).

### Secret Exposure in CI Logs & Artifacts
- **Vulnerability**: Pipeline jobs printing environment variables, dumping debug logs, or uploading build artifacts (e.g., coverage reports, test output, diagnostics) that capture tokens or API keys.
- **Audit Steps**: Audit `upload-artifact` steps and log outputs. Verify that secrets are masked and temporary credentials expire immediately.

---

## 2. SUPPLY CHAIN & DEPENDENCY MANAGEMENT

### Package Pinning & Lockfile Integrity
- **Vulnerability**: Unpinned dependencies (`^1.2.3` or `latest`), uncommitted lockfiles (`package-lock.json`, `poetry.lock`, `uv.lock`, `Cargo.lock`), or missing hash/integrity verification.
- **Audit Steps**: Verify that production dependencies are strictly pinned and lockfiles are version-controlled and enforced during builds (`npm ci`, `poetry install --frozen`, `cargo --locked`).

### Dependency Confusion & Scoped Registries
- **Vulnerability**: Internal private package names (e.g., `@mycompany/auth`) falling back to the public npm/PyPI registry when internal repository configuration is missing or misconfigured.
- **Audit Steps**: Verify `.npmrc` or `pip.conf` configuration. Ensure private scopes are explicitly routed to internal artifact registries with strict fallback prevention.

---

## 3. CLOUD, CONTAINER & RUNTIME CONFIGURATION

### IAM Least Privilege & Confused-Deputy Roles
- **Vulnerability**: Workload identities (AWS IAM Roles for Service Accounts, GCP Workload Identity) granted wildcard permissions (`*`) or cross-account trust policies without external ID / audience validation.
- **Audit Steps**: Inspect Terraform, CloudFormation, or Pulumi templates. Enforce least-privilege resource policies and verify trust conditions.

### Cloud Metadata Service (IMDS) SSRF Exposure
- **Vulnerability**: Applications susceptible to SSRF that can contact the link-local metadata address (`http://169.254.169.254`) to steal node credentials.
- **Audit Steps**: Ensure AWS IMDSv2 (requiring session tokens with `X-aws-ec2-metadata-token`) is enforced with a hop limit of 1 on containerized workloads.

### Container Sandboxing & Least Privilege
- **Vulnerability**: Containers executing as `root` (UID 0), mounting host filesystems (`/var/run/docker.sock`), or running with `privileged: true`.
- **Audit Steps**: Check `Dockerfile` for `USER nonroot`. In Kubernetes manifests, verify `securityContext`:
  ```yaml
  securityContext:
    runAsNonRoot: true
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
    capabilities:
      drop: ["ALL"]
  ```

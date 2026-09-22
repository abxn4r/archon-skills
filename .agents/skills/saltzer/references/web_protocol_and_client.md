# WEB PROTOCOL, AUTH & CLIENT-SIDE AUDIT GUIDE
*Archon Security Architecture -- Saltzer Advisor Reference*

---

## 1. HTTP PROTOCOL & CACHE SECURITY

### HTTP Request Framing & Desync (Smuggling)
- **Vulnerability**: Discrepancies between edge proxies (Cloudflare, AWS ALB, NGINX) and upstream backend servers in interpreting `Content-Length` vs. `Transfer-Encoding: chunked` or HTTP/2-to-HTTP/1 translation.
- **Audit Steps**: Inspect custom HTTP parsers and gateway configurations. Look for trailing whitespace, duplicate headers, or ambiguous line terminators (`\r\n` vs. `\n`).

### Web Cache Poisoning & Cache Deception
- **Vulnerability**: Edge CDNs or reverse proxies caching unauthenticated or attacker-poisoned responses and serving them to legitimate users.
- **Audit Steps**: Trace how unkeyed headers (e.g., `X-Forwarded-Host`, `X-Original-URL`, `X-Rewrite-URL`) influence response content. Verify that dynamic user data endpoints explicitly send `Cache-Control: no-store, private`.

### CORS & Origin Trust Misconfigurations
- **Vulnerability**: Backend endpoints reflecting the request `Origin` header blindly into `Access-Control-Allow-Origin` while setting `Access-Control-Allow-Credentials: true`, or trusting `null` origins.
- **Audit Steps**: Verify CORS middleware: require a strict, non-regex-bypassable allowlist of trusted origins. Never allow `Access-Control-Allow-Origin: *` in combination with credentialed requests.

---

## 2. CLIENT-SIDE & BROWSER SECURITY

### `postMessage` Origin & Message Trust
- **Vulnerability**: `window.addEventListener("message", ...)` handlers that fail to verify `event.origin`, or send messages using wildcard targets (`postMessage(data, "*")`).
- **Audit Steps**: Ensure every message handler strictly validates `event.origin === EXPECTED_ORIGIN`. Ensure sensitive tokens or commands are never transmitted to wildcard targets.

### DOM-Based XSS & Client-Side Sinks
- **Vulnerability**: Client-side JavaScript reading attacker-controlled sources (`location.hash`, `location.search`, `document.referrer`, `localStorage`, `postMessage`) and passing them directly into raw DOM sinks (`innerHTML`, `outerHTML`, `document.write`, `eval`, `setTimeout(string)`).
- **Audit Steps**: Audit all client-side template rendering. Enforce Safe-DOM primitives (`textContent`, `setAttribute`, or DOMPurify sanitization before insertion).

### Client-Side Prototype Pollution
- **Vulnerability**: Recursive object merge, clone, or query-string parsing utilities that accept `__proto__`, `constructor`, or `prototype` properties without sanitization.
- **Audit Steps**: Inspect deep-merge functions. Verify that prototype keys are stripped or rejected:
  ```javascript
  if (key === "__proto__" || key === "constructor" || key === "prototype") continue;
  ```

### Webview Bridges & Native App IPC
- **Vulnerability**: Hybrid mobile/desktop apps (Electron, React Native, Tauri) exposing native bridges (`window.electronAPI`, Android JavascriptInterface) to untrusted or external web content.
- **Audit Steps**: Ensure `contextIsolation: true` and `nodeIntegration: false` are enforced in Electron. Scope native bridge functions to least-privilege operations with strict argument validation.

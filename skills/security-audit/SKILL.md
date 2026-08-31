---
name: security-audit
description: Walk a web-service security checklist — OWASP Top 10, auth, data exposure, configuration, dependencies. For a service taking untrusted input over a network; on a mobile, embedded, library, or pipeline target it reports cleanly about the wrong threats.
disable-model-invocation: true
---

# /specseal:security-audit — a checklist walked the same way every time

A scan finds what it was built to look for. The value of a written checklist
is the opposite property: it covers the same ground on a bad day as on a good
one. Walk every heading and say `none found` explicitly — a silently skipped
section reads exactly like a clean one.

**What this checklist assumes.** It describes a service that takes untrusted
input over a network: injection through request data, sessions and
authorization, data at rest and in transit, deployment configuration. That is
the shape of most OWASP material and it is the shape of this file.

Other projects have real threats this will not name. A mobile or desktop
client worries about local storage, keychain use, certificate pinning, and
what a rooted device can read. An embedded target worries about firmware
signing and physical access. A library worries about what it does with
attacker-controlled input on behalf of its callers, and about its own supply
chain. A data pipeline worries about what leaks into logs and derived
datasets.

Say which of those the project is before walking the list. If the answer is
"none of the above", a clean report here means the checklist did not apply —
say that instead of reporting a pass.

## OWASP Top 10 Check

### Injection
- SQL: parameterized queries used?
- XSS: output encoding applied?
- Command: user input in shell commands?
- Path traversal: file paths validated?

### Authentication & Authorization
- Passwords properly hashed (bcrypt/argon2)?
- Session management secure?
- Auth checks on every endpoint?
- RBAC/ABAC properly implemented?

### Data Protection
- Sensitive data encrypted at rest?
- TLS for data in transit?
- PII handling compliant?
- No secrets in code/logs/errors?

### Configuration
- Debug mode off in production?
- CORS properly configured?
- Security headers present?
- Dependencies up to date?

### Input Validation
- All user input validated at boundary
- Whitelist over blacklist
- File upload restrictions
- Rate limiting on sensitive endpoints

## Rules
- Critical findings: report immediately, suggest fix
- Check actual code, not just patterns
- Consider the threat model (internal tool vs public API)
- No false sense of security: "no findings" ≠ "secure"

## Output

```
## Security Audit: [scope]

**Critical** (fix immediately)
- [vulnerability] at file:line → [remediation]

**High** (fix before deploy)
- [vulnerability] at file:line → [remediation]

**Medium** (fix soon)
- [vulnerability] → [suggestion]

**Recommendations**
- [proactive security improvements]
```

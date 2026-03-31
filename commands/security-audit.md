# /security-audit - Security Vulnerability Scan

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

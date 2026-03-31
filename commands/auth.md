# /auth - Authentication & Authorization Review/Design

## Authentication Check

### Session/Token Management
- Token storage: httpOnly cookies > localStorage
- Token expiry: access (short) + refresh (longer)
- Rotation: refresh tokens rotated on use
- Revocation: mechanism exists for invalidation

### Password Security
- Hashing: bcrypt/argon2 (never MD5/SHA)
- Requirements: length > complexity rules
- Rate limiting on login attempts
- Account lockout policy

### OAuth/SSO
- State parameter for CSRF prevention
- PKCE for public clients
- Proper scope management
- Token validation on backend

## Authorization Check

### Access Control
- Principle of least privilege
- Role-based or attribute-based (RBAC/ABAC)
- Authorization on EVERY endpoint (not just UI)
- Resource-level permissions (not just role-level)

### Common Pitfalls
- IDOR: checking ownership, not just authentication
- Privilege escalation: role changes validated
- Missing auth on new endpoints
- Client-side only authorization

## Output

```
## Auth Review: [scope]

**Authentication**
- Method: [JWT/Session/OAuth]
- Issues: [findings by severity]

**Authorization**
- Model: [RBAC/ABAC/custom]
- Issues: [findings by severity]

**Recommendations**
- [prioritized improvements]
```

# /api-design - API Design Review & Creation

## Scope
Design or review REST/GraphQL/gRPC APIs.

## Design Checklist

### Endpoints
- Resource-oriented URLs (nouns, not verbs)
- Consistent naming (plural resources, kebab-case)
- Appropriate HTTP methods (GET/POST/PUT/PATCH/DELETE)
- Logical nesting (max 2 levels)

### Request/Response
- Consistent envelope structure
- Pagination for list endpoints (cursor or offset)
- Filtering, sorting, field selection where appropriate
- Proper status codes (don't 200 everything)

### Error Handling
- Consistent error format with code, message, details
- Actionable error messages
- Don't leak internal details in production

### Security
- Authentication method appropriate for use case
- Authorization on every endpoint
- Rate limiting on public endpoints
- Input validation and sanitization

### Versioning
- Strategy defined (URL path, header, or query param)
- Breaking change policy documented

## Rules
- Follow project's existing API patterns first
- Don't over-design: YAGNI applies to APIs too
- Consider API consumers' developer experience

## Output

```
## API Design: [resource/feature]

### Endpoints
| Method | Path | Description | Auth |
|--------|------|-------------|------|

### Request/Response Examples
[key endpoint examples with JSON]

### Error Codes
[project-specific error codes]

### Notes
[versioning, pagination, special behaviors]
```

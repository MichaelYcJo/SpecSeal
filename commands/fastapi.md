# /fastapi - FastAPI Best Practices

## Patterns

### Routing
- Router organization by domain/feature
- Consistent path naming (kebab-case, plural resources)
- Proper HTTP methods and status codes
- Dependency injection for shared logic

### Request/Response
- Pydantic models for all request/response schemas
- Proper validation with Field constraints
- Consistent error response format
- Use response_model for automatic serialization

### Database
- Async SQLAlchemy or similar for async DB
- Dependency injection for DB sessions
- Proper transaction management
- Use Alembic for migrations

### Error Handling
- Custom exception handlers
- HTTPException with appropriate status codes
- Don't expose internal errors to clients
- Structured error responses

### Security
- OAuth2/JWT for authentication
- Dependency-based authorization
- CORS configuration
- Rate limiting (slowapi or similar)

### Performance
- Async endpoints for I/O operations
- Background tasks for long operations
- Proper connection pooling
- Caching where appropriate

## Rules
- Check FastAPI version and available features
- Follow project's existing FastAPI patterns
- Use type hints consistently

## Output

```
## FastAPI Review: [scope]

**Issues by priority**:
1. [issue] at file:line → [fix]

**Patterns to adopt**:
- [suggestion]
```

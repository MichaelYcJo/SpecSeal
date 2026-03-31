# /docker - Docker Configuration Review & Creation

## Review Checklist

### Build Optimization
- Multi-stage builds to reduce image size
- Layer ordering: dependencies before source code
- .dockerignore configured properly
- No unnecessary files in image
- Pinned base image versions

### Security
- Non-root user in container
- No secrets in image/Dockerfile
- Minimal base image (alpine/distroless/slim)
- Read-only filesystem where possible
- Health checks defined

### Runtime
- Proper signal handling (exec form CMD)
- Environment variables for configuration
- Volume mounts for persistent data
- Resource limits defined
- Logging to stdout/stderr

### Compose
- Service dependencies (depends_on with healthcheck)
- Network isolation between services
- Named volumes for data persistence
- Environment variable management (.env files)

## Rules
- Match project's existing Docker patterns
- Python: use uv for dependency management
- Node.js: use pnpm with frozen lockfile
- Prefer official base images

## Output

```
## Docker Review: [scope]

**Issues**:
- [severity] [issue] → [fix]

**Optimizations**:
- [suggestion with expected impact]

[Dockerfile if creation requested]
```

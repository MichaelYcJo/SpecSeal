# /cicd - CI/CD Pipeline Design & Review

## Pipeline Stages

### Build
- Dependency caching (restore before install)
- Parallel jobs where possible
- Fail fast on lint/type-check
- Artifact creation

### Test
- Unit tests (parallel, fast)
- Integration tests (may need services)
- Coverage reporting (but don't gate on percentage alone)
- Flaky test detection

### Security
- Dependency scanning (Dependabot/Snyk)
- Secret scanning
- SAST where appropriate
- Container scanning if applicable

### Deploy
- Environment promotion (dev → staging → production)
- Rollback mechanism
- Health check after deploy
- Smoke tests post-deploy

## Platform-Specific

### GitHub Actions
- Reusable workflows for common patterns
- Matrix builds for multi-version testing
- Concurrency control (cancel in-progress on push)
- Proper secret management

### General
- Pipeline as code (versioned with repo)
- Minimal permissions (least privilege)
- Notifications on failure
- Duration monitoring

## Output

```
## CI/CD Review: [scope]

**Issues**:
- [issue] → [fix]

**Optimizations**:
- [suggestion]

[Pipeline file if creation requested]
```

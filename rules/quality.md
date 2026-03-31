# Quality Rules

## Engineering Principles
- **DRY**: Don't abstract too early — 3 occurrences before extracting
- **KISS**: Three similar lines > premature abstraction
- **YAGNI**: Current requirements only. No speculative features.

## Implementation Completeness
- No TODO in core functionality
- No mock data or placeholder stubs in production code
- No "not implemented" throws
- Start = Finish: once started, complete it

## Scope Discipline
- Only what's requested — no unrequested feature additions
- MVP first, expand after feedback
- Don't add auth/monitoring/deployment unless specified

## Code Organization
- Follow existing project patterns first
- Tests in `tests/` or `__tests__/`, not next to source
- Clean up temp files after work

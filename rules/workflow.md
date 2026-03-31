# Workflow Rules

## Two-Stage Review (detailed)

### Stage 1: Spec Compliance
- Read actual code (never trust the report)
- Compare line-by-line with requirements
- Identify: missing features AND unrequested additions
- Output: ✅ Compliant | ❌ Issues list

### Stage 2: Code Quality
- Only run AFTER Stage 1 passes
- Check: SOLID, error handling, test quality, security, performance
- Severity: Critical (fix now) > Important (fix before merge) > Minor (later OK)

### Review Loop
```
Implement → Spec Review → [fail: fix → re-review] →
Quality Review → [fail: fix → re-review] →
/verify → /audit → Complete
```

## Planning Efficiency
- Identify parallelizable tasks explicitly
- Map dependencies: separate sequential vs parallel
- >3 steps → use task tracking
- >3 files affected → plan before implementing

## PDCA for Features
| Phase | Deliverable |
|-------|-------------|
| Plan | Requirements, scope, milestones |
| Design | API spec, data model, architecture |
| Do | Implementation |
| Check | Gap analysis (design vs code, ≥90% match) |
| Act | Fix gaps (max 5 iterations) |

## Git Workflow
- Meaningful commit messages (not just "fix" or "update")

# Agent Orchestration Rules

## Role Separation

| Role | DO | DON'T |
|------|-----|-------|
| **Orchestrator** | Create tasks, spawn agents, synthesize results, ask user | Write code, explore codebase |
| **Worker** | Use tools directly, report with absolute paths | Spawn sub-agents, create tasks |

## Worker Prompt Templates

### Implementer
```
You are implementing: [task description]
Context: [location, dependencies, architecture]
Your job: implement → test → verify → commit → report
Report: What / Test results / Changed files (absolute paths) / Issues
```

### Spec Reviewer
```
You are reviewing spec compliance.
Requirements: [full text]
CRITICAL: Do NOT trust the implementer's report. Read code directly.
Check: Missing? Extra? Misunderstood?
Output: ✅ Compliant | ❌ Issues [specific list with file:line]
```

### Quality Reviewer
```
You are reviewing code quality (only after spec passes).
Focus: SOLID, error handling, test quality, security, performance
Output: Strengths / Issues (Critical > Important > Minor) / Assessment
```

## Model Selection for Agents
- **(default)**: Inherit parent model — most tasks
- **haiku**: Info gathering, simple search (5-10 parallel OK)
- **sonnet**: Well-defined implementation (1-3 parallel)
- **opus**: Architecture, complex reasoning (1-2 parallel)

## Error Recovery
- Timeout → split task, retry smaller pieces
- Wrong approach → add explicit constraints, retry (max 2)
- Still failing → escalate to user (AskUserQuestion)

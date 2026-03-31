# /architecture - Architecture Analysis & Design

## When to Use
- New system/feature design
- Evaluating architectural changes
- Reviewing existing architecture

## Analysis Framework

### 1. Current State
- Component inventory and relationships
- Data flow and dependencies
- Technology stack
- Pain points and bottlenecks

### 2. Requirements
- Functional: what it must do
- Non-functional: scale, latency, availability, security
- Constraints: team size, timeline, existing infra

### 3. Design Options
Present 2-3 options with trade-offs:

| Aspect | Option A | Option B |
|--------|----------|----------|
| Complexity | | |
| Scalability | | |
| Maintainability | | |
| Time to implement | | |

### 4. Recommendation
- Recommended option with reasoning
- Migration path if changing existing architecture
- Risks and mitigations

## Rules
- No over-engineering: match complexity to requirements
- Consider team capabilities
- Prefer boring technology unless requirements demand otherwise
- Show trade-offs honestly

## Output

```
## Architecture: [system/feature]

**Current**: [brief description of current state]
**Requirements**: [key requirements]

**Options**:
1. [option] - [pros] / [cons]
2. [option] - [pros] / [cons]

**Recommendation**: [which and why]
**Migration**: [steps if applicable]
**Risks**: [what to watch for]
```

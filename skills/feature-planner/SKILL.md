---
name: feature-planner
description: Plan feature implementation with scope control and dependency mapping.
---

# Feature Planner

Use when feature touches >3 files or requires architectural decisions.

## Planning Steps

### 1. Requirements Clarification
- What exactly is being requested?
- What's explicitly NOT in scope?
- What are the acceptance criteria?
- Any constraints (performance, compatibility, timeline)?

### 2. Existing Code Analysis
- What related code already exists?
- What patterns does the project use?
- What can be reused/extended vs built new?
- What will break if we change X?

### 3. Implementation Plan
- Break into ordered tasks (dependencies mapped)
- Identify parallel vs sequential work
- Estimate which files change
- Flag risky parts that need extra care

### 4. Scope Lock
- List what's IN scope (explicit)
- List what's OUT of scope (explicit)
- Get user confirmation before starting

## Rules
- No gold-plating: plan only what's requested
- Identify the MVP path first
- Flag unknowns early (don't discover them mid-implementation)
- If >10 files affected, suggest phased approach

## Output Format

```
## Feature: [name]

**Scope**: [in] / **Not**: [out]

**Tasks** (in order):
1. [task] - [files affected]
2. [task] - [files affected]
   ↳ depends on #1
3. [task] - [files affected] (parallel with #2)

**Risks**: [what could go wrong]
**Questions**: [what needs user input]
```

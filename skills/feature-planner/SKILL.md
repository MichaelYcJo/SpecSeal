---
name: feature-planner
description: |
  Decompose work into ordered tasks with dependencies mapped, then lock scope
  in writing before starting.
  Use when: the work spans more than about three files or needs phasing, and
  no plan exists yet.
  NOT for: firing on your own while the smith is driving — its design gate
  invokes this when decomposition is what the work needs. Not for
  single-file changes.
---

# feature-planner — write the scope down before it moves

Scope that lives in someone's head grows quietly, and nobody can point to
when it did. Decomposing the work orders it; writing down what is *not* in
it is what makes the boundary hold later.

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

## Where the output goes

Into `specs/<work-item-id>/plan.md`, as its Phases table — one row per phase,
with the **Verified by** and **Status** columns that table carries. There is
no separate task-list file and no separate root for one.

What that costs: a phase row holds an ordered slice, not a dependency graph,
so the parallel markers in the format below do not survive into the file. They
are for the conversation that produces the plan. Work finishing in one session
needs no file at all.

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

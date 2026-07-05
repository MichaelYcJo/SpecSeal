# Review Handoff Protocol — draft 0.1

A file convention for handing review work between agent sessions — across
time, machines, and tools. Tool-agnostic on purpose: nothing here requires
Claude Code or this plugin; any coding agent that can read and write files in
a git repo can conform.

## Problem

Review findings normally live in PR comments, written for humans. The next
agent session — a re-review round, or the session fixing the findings —
cannot reliably recover from comments: which axes were already judged, what
was empirically probed, which regression tests were prescribed and where.
Measured consequence: round *n* of a review costs *n* full walks of the same
code, and prescribed tests silently drop when only inline comments get acted
on.

## Layout

```
_ai/review-history/
└── PR-<id>/            one directory per change — parallel reviews never share a file
    ├── round-1.md
    ├── round-N.md
    ├── tests-todo.md
    └── evidence-todo.md
```

`<id>` is the change identifier (PR number, MR id, change-list id).
The `_ai/` root is **committed** — ignored files do not follow worktrees or
other machines — and deleted per-change before merge, after draining (below).

## Files

### round-N.md — what this round did

| Field | Required | Content |
|---|---|---|
| Target SHA | yes | commit(s) the round actually reviewed — branches move between rounds; record both if HEAD moved mid-review |
| Verdict table | yes | per finding: location, verdict, grounds |
| Executed probes | yes (may be "none") | what was RUN, with results — distinguished from what was read |
| Inherited axes | for N>1 | axes carried from earlier rounds without re-walking |

### tests-todo.md — regression tests prescribed, not written

One row per test: what it asserts · **destination file** · grounds · status.
The reviewer prescribes; the implementer plants. Prescriptions embedded in
fix-suggestion snippets get lost (measured) — this file is the contract.

### evidence-todo.md — verified facts awaiting the ledger

One row per fact: the fact · destination ledger row · status. Reviewers do
not write the ledger directly: parallel writers clobber each other, and
worker findings are pre-verification.

## Conformance

A tool claiming to support this protocol:

1. **Reads before reviewing** — an existing `PR-<id>/` directory is prior
   state: inherit judged axes, re-check (don't re-run) executed probes.
2. **Writes after posting** — the session that posted a review writes
   round-N and the two todo files immediately; it is the only moment the
   verdicts and probe results still exist anywhere.
3. **Drains before merging** — every unresolved row moves to a durable home
   (the repo's evidence ledger, follow-up list, or open-questions section)
   before the directory is deleted. Deleting without draining discards the
   handoff.

## Non-goals

- Not a memory system: no automatic capture, no embeddings, no store beyond
  the repo. Structured handoff for one workflow (review), nothing broader.
- Not a comment replacement: human-facing findings still go to the code
  host; this directory is for the next session, and the two audiences never
  share a file.

## Status

Draft 0.1, extracted from the convention this plugin's `code-review` and
`implement` skills already operate (they are its reference implementation).
Field names and layout may change; the three conformance rules are stable.

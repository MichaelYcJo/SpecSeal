---
name: implement
description: |
  Spec-driven implementation methodology: document layout (docs/specs/_ai), policy-first
  judgment, evidence feedback, and review incorporation.
  Use when: implementing a feature, starting a ticket, incorporating review feedback,
  or when a repo needs its document layout bootstrapped.
  NOT for: reviewing someone else's code (use code-review), pure Q&A.
---

# implement — spec-driven implementation

Methodology for implementing against written specs, leaving durable evidence,
and closing the loop with review. Loaded by the `developer` agent; usable directly.

## Document layout — three axes

Every artifact this skill produces goes to exactly one of three roots, split by
**lifetime**, not by who wrote it:

| Root | Lifetime | Test | Authority |
|---|---|---|---|
| `docs/` | Permanent, cumulative | Must still be true in 6 months (policies, `_evidence.md`, `_follow-up.md`) | **Norms, ratified by humans** — AI may fill gaps by inference, marked as inference |
| `specs/` | One work item | Its role ends when this work ships (SDD, overview) | The contract this work executes against — humans set direction, agents work to it |
| `_ai/` | Between sessions | Safe to delete wholesale — **after** the export rules below have run | Written by and for AI sessions |

The axis is lifetime and authority, **not audience** — humans and AI read all
three. (Labeling policies "for humans" would push sessions away from reading
them, and policy is the root of judgment precedence.)

`_ai/` is committed (gitignored files don't follow worktrees or other machines),
but deleted per-PR before merge. "Committed yet short-lived" is its nature.

### Bootstrap — create what's missing

When a root or file this skill needs doesn't exist, create it from
`templates/` in this plugin and continue. In particular:

- `docs/policies/<domain>/_evidence.md` — stamp the baseline (current HEAD SHA,
  date) into its header at creation time. The baseline is what makes recorded
  coordinates verifiable later; an unstamped ledger cannot be trusted.
- `_ai/README.md` — carries the export rules so sessions that never load this
  skill still see them.
- Leave evidence rows empty. They fill through the feedback rule below as work
  happens — do not pre-populate speculatively.

## Procedure

### 1. Read the spec before the code

Judgment precedence: **policy (`docs/`) > SDD (`specs/`) > existing code**.
A spec that contradicts policy gets fixed, not followed.

- Policy documents delegate to each other. "This document doesn't answer it"
  is not a policy gap until sibling documents in the same domain are checked.
- Read `docs/policies/<domain>/_follow-up.md` before starting. It holds items
  whose answer exists but which waited on prerequisite work — **this work may
  be that prerequisite.** If so, include the item in this change and delete its
  row; what remains in that file is the definition of remaining scope.
- Verify clause numbers a ticket cites. Tickets are written before (or drift
  from) the documents they cite; a missing clause means writing it is part of
  this work, with a freshly allocated number.

### 2. Implement, and feed evidence back where you verified it

When you open code or run something to settle a judgment, record the outcome in
`_evidence.md` on the row it belongs to (spec clause ↔ `file:line`), marked with
the date. Only rows in this work's scope — full-ledger audits verify what is
already correct and return nothing.

This record is the input for the reviewer and the next ticket. Unrecorded
verification gets redone by every session that follows — the single largest
avoidable cost in multi-session work.

### 3. The SDD file set

A work item's directory is `specs/<unix-epoch-seconds>-<slug>/` (e.g.
`specs/1784780439-center-list-sort/`), bootstrapped from `templates/`. The
timestamp prefix keeps directories in creation order and collision-free
without a registry — take it from `date +%s` when creating the directory.

| File | Holds | When |
|---|---|---|
| `spec.md` | WHAT — scope, mandatory user scenarios & acceptance, grounding clauses | before implementing |
| `plan.md` | HOW — phases as vertical slices, alternatives with failure scenarios; this is the Design Gate's artifact | before implementing (gated work) |
| `questions.md` | decisions only a human can make — extracted so nothing ships on a silent assumption | as they arise |
| `overview.md` | the closing record (below) | when implementation ends |

### 4. Write the overview

When implementation ends, write `specs/<work-item>/overview.md`:

1. What was done — purpose and scope in a paragraph or two.
2. What changed — each file path with a one-line description. A reader must
   see the shape of the change without opening the code.
3. Where spec and implementation diverged — both sides quoted, which side won,
   and the grounds. "The document probably said so" is not grounds; quote it.
4. What was not verified — with **who has to answer it** per item.
5. What was fed back into the spec — clauses this work added, marked as
   *inferred during implementation* so planners know they may overturn them.

Never record something as passing that you did not run. Findings from reading
and findings from execution are labeled separately.

### 5. Incorporate review — read the handoff directory first

A session fixing review feedback starts at `_ai/review-history/PR-<n>/`,
**not** at the inline comments. Two of its files are owned by the implementer:

| File | Written by | Acted on by |
|---|---|---|
| `round-N.md` | review orchestrator | next review round |
| `tests-todo.md` | review orchestrator | **implementer** — plant each test in the file the row names |
| `evidence-todo.md` | review orchestrator | **implementer** — merge each fact into `_evidence.md` |

Inline comments may not contain these lists at all. Fixing only the comments
ships the code change and silently drops the tests and the evidence.
Probes already run by a previous round (listed in `round-N.md`) are not
rebuilt — only re-checked for whether the finding is now fixed.

### 6. Export before merge — `_ai/` is deleted, so drain it first

Before the PR merges, every unresolved (⬜) row must move out:

| Remaining item | Destination |
|---|---|
| Doable within this PR | Do it now — deletion removes the last chance |
| Waiting on prerequisite work | `docs/policies/<domain>/_follow-up.md` |
| Needs a decision | The policy document's open-questions section |

Deleting without exporting is discarding the list. The PR directory dies with
the PR; the two destinations accumulate.

## Proof block

End the response with this block whenever the skill was applied. Its values
cannot be filled without actually opening the documents — that is the point.
Never invent them; write `none — <reason>` for anything not actually read.

```
📋 implement applied
· spec:     <policy/SDD files and clauses actually read>
· evidence: <_evidence.md rows added or updated>
· verified: <what was executed vs. what was only read>
```

When the skill matched but did not apply, say so explicitly with the reason —
silence is indistinguishable from failure to trigger.

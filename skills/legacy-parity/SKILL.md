---
name: legacy-parity
description: |
  Behavior-equivalence methodology for legacy migrations: three-way judgment
  (policy ↔ original code ↔ new code) with original-preservation as the default.
  Use when: a project declares a migration config (.specseal/parity.md), porting or
  reviewing ported behavior, judging divergence from a legacy original.
  NOT for: greenfield work — implement/code-review alone cover that.
---

# legacy-parity — the original is the fallback spec

Extends `implement` and `code-review` when the work is a **migration**: the
same behavior rebuilt on different technology. Active only in projects that
carry a migration config (below); invisible elsewhere.

## Premise

**Preserve the original's behavior.** A migration is not a redesign. "Safer
design" or "more consistent API" is never grounds to diverge. If the original
looks wrong, report that judgment — changing it is the planner's call, not
yours.

## Migration config — `.specseal/parity.md`

A migrating project declares, committed with the repo:

| Field | Example |
|---|---|
| Original repo | org/legacy-api, module `apps/foo` |
| Baseline commit | SHA the evidence ledger's coordinates refer to |
| Policy root | `docs/policies/` |
| Coordinate-trust exceptions | paths whose recorded coordinates need re-verification, and why |

Machine-local checkout paths never go in the repo. They live in
`~/.claude/specseal/parity-paths.md`, keyed by the origin remote URL (so
worktrees and multiple checkouts resolve to one entry). Resolution order:
recorded path → sibling directory of the current repo → verify by
`git remote -v` against the declared original → **ask the user and record the
answer**. Never guess; a comparison against a guessed original proves nothing.

## Three-way judgment

Divergence found between policy, original, and new code:

| Situation | Follow |
|---|---|
| Policy explicitly covers the divergence, and it holds up | **Policy** — grounds means a quotable sentence with its source; "the document probably said so" is not grounds |
| Policy silent | **The original**, exactly |
| Grounds exist but look wrong | Neither silently — record both texts side by side and escalate |

Before raising "needs a product decision": if the policy is silent but **the
original already does the thing, inherit the original and mark it decided** —
only rules that exist in *neither* place need a planner. Inflating the
open-questions count with inheritable items hides what actually needs
deciding; silently deciding genuinely new rules hides that a decision was made.

### When "follow the original" is itself ambiguous

Storage, query conditions, and response assembly may disagree inside the
original. The canonical answer is **what the original sends to the client**.
Trace from the endpoint to the finished response; a mid-layer condition that
never changes the response needs no reproduction. Check git history too — if
the original later fixed a behavior, the fix is its final intent; cloning the
pre-fix version preserves nothing.

## Evidence ledger

`.specseal/map.md` maps spec clauses to **original**
coordinates (`path#anchor@hash`). Start every comparison
there instead of grepping the original; feed newly verified original behavior
back into the row you used (see `implement`). When a coordinate is suspect,
open the baseline commit directly: `git show <baseline>:<path>`.

## Replacement annotation

Every ported endpoint/entry point states, where its API docs render (e.g. the
handler docstring), **what it replaces**: original method + path + function.
This line declares the judgment default — "same business logic as the
original" — so any policy-grounded divergence is listed right below it.
1:N splits name the branch each new handler took; N:1 merges list *all*
originals; partial ports state what was left behind. `none (new)` for
additions, with the grounding clause.

## Parity review

`code-review` runs as usual with one change of frame: stage 1 compares
against **the original** (via the ledger's coordinates), not only the written
spec, across the same comparison axes. Verdict labels:

```
🔴 differs from original · no grounds   — align with the original
🟡 differs from original · has grounds  — quote the grounds, confirm intent
🟢 equivalent (different implementation, same observable behavior)
❓ out of verified scope (original or policy not found — never a pass)
```

## Recording the comparison

When you have actually compared against the original — coordinates opened,
behavior read, verdicts assigned — record it so the commit gate can recognize
this cycle:

```bash
git rev-parse HEAD > "$(git rev-parse --git-dir)/specseal-parity"
```

A commit closes the cycle; the next change to code starts an uncompared one.
In a repo that declares `.specseal/parity.md`, committing code with no such record
makes the gate ask — approving is the waiver, and `[no-parity]` skips it
visibly. Type it in FRONT of the command, quotes included:
`: '[no-parity]'; git commit …`. After `git commit` a bare word is a pathspec
and git rejects the whole command.

**Write this only after the comparison happened.** A mark for work you did not
compare is worse than no mark: it converts "nobody checked" into "someone
checked and it was fine", which is the one claim this whole skill exists to
keep honest.

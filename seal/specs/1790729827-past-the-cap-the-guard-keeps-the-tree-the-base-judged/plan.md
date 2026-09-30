# Implementation Plan: past the cap, the guard keeps the tree the base judged

<!-- seal/specs/1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-30 by the orchestrating session, when `smith` was spawned.

<!-- The approval is the spawn: the orchestrating session wrote the plan's
content into the spawn prompt (round 3's fix, its regression case, the class
to enumerate, the invariant) and spawned `smith` to build it. `smith` wrote
this file from that prompt, after its first fix commit, and chose the second
row of the alternatives below over the prompt's first on the grounds that row
gives. -->

## Summary

`walk_directories` puts the base thread's directories in front of the walk's
wherever the walk's own FIRST directory is unresolved, instead of wherever it
names no readable directory at all. Past `STATE_CAP` the collapsed walk's
first is unresolved, so the worktree guard and the consent writer take the
tree `86256492` took, whatever the walk regains behind it.

## Technical context

- `hooks/cmdline.py#walk_directories`, the ordering added by `879df3b4` (Q7 of
  `1790660768`): `ordered = wheres + base_wheres` when any of `wheres` is
  readable, else the reverse.
- `hooks/cmdline.py#_branches`: `wheres = running + skipped`, so `wheres[0]` is
  a shell the segment runs in. `running` is never empty, and `_capped` keeps
  one state.
- Consumers (round 3's grep, re-run): `hooks/worktree-guard.py#main` takes the
  first directory `classify` answers for, through `judgeable`, which reads an
  unresolved one as the session's own; `hooks/worktree_consent.py#creation_directory`
  takes the first readable one; `hooks/commit-review-gate.py#commit_invocations`
  judges every directory, so its verdict does not depend on order, and the
  deny's list of unresolved directories does.
- Failure scenario of the chosen approach: the walk leads wherever its first
  directory is readable, so a future reading that puts a readable directory
  FIRST that the shell did not run in would lead again. Every current source
  of a readable first is a running shell's landing (`_branches`, and I13's
  landing placed in front of the as-written answer).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Round 3's fix**: a `collapsed` flag set at the walk's first collapse, and the base thread first from then on | Measured. It closes round 3's rows, but (1) past the cap a `cd` landed past its redirections stops leading: `cd w; ` + 9 × `2>/dev/null cd nosuch; ` + `2>/dev/null cd O && git switch` judges the dirty `w` where bash switches in `O`, and files `O`'s creation under `w`, which is I13's own claim broken past the cap; (2) the same cause with no cap reached stays open: `cd w; 2>/dev/null cd nosuch \|\| (cd O) && git worktree add` is filed under `w/nosuch`, where `86256492` and bash have `w` | rejected. It is what the spawn named |
| **B. The walk leads where its first directory is readable** | The failure scenario in *Technical context*. It changes the order before the cap too, which is where (2) is closed; every such change hands the consumers the base thread's answer | **chosen**. It closes every row A closes, both of A's failures, and is one condition where A is a flag and two edits |
| **C. The walk leads where its LAST directory is readable** | Mutant only: 5 of the 12 new cases turn red | rejected |
| **D. The consent writer and the guard read only the running shells** | `walk_directories` returns one tuple to three consumers; separating running from skipped is a new interface on all three | rejected, out of scope |

**The spawn's invariant, and the reading this plan takes.** The prompt said
"nothing `86256492` asks or stops may read silent after the fix". Under B one
shape the base asked about reads silent: the capped chain followed by
`2>/dev/null cd O && git switch`, where the base asked about the dirty `w`
because it never read that `cd`, and bash switches in the clean `O`. The same
shape before the cap has read silent since round 2 of `1790660768` (I13), which
was reviewed and accepted. This plan reads the invariant as holding for the
commit gate's stops, and for the guard's where bash runs the switch in the
tree the base judged; S7 measures the first and S1–S4 the second. Under A the
literal reading holds, and the guard asks about a tree the switch never
touches.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | B in `walk_directories`; S1–S6 planted, each seen red at `542f920b` or at the named alternative; the two policy sentences; ⬜ 2's correction and the drifted rows re-read; this item's ledger and changelog fragments; ⬜ 3 and ⬜ 4 refused with grounds in `overview.md` | S1–S7. Narrow: the gate, reader, guard and consent modules through `bin/test`, `ruff check` and `ruff format --check` on the changed Python, `bin/evidence-check --strict .`, `bin/unverified-check`, `bin/survivor-check`. The broad gate is the sealer's | |

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.**

## Operational impact

None. No migration, variable or dependency.

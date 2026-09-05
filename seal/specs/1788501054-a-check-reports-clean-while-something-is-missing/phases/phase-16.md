# 1788501054-a-check-reports-clean-while-something-is-missing — phase 16

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-16.md
— what this phase of the build did, written by the session that ran it when
the phase closed. Not in `plan.md`'s original four: round 13's fixes are work
the plan did not contain, and the phase row was added beside them the way
phases 6 through 15 were. -->

| Field | Value |
|---|---|
| Phase | 16 |
| Commit | 404e769 |
| Ran by | orchestrator on fable-5.1 — no smith was spawned, on the owner's standing answer for this branch's fixes |

## What this phase was asked

Round 13's 🔴 and five 🟡 — the verifying round at phase 15's one-line fix:

- **🔴 1** — `os.path.normpath` collapses `lnk/..` lexically, so where a
  `--ledger` pattern crosses a symlink before a `..` the returned path
  names a different file than `glob` matched, and `main` opens the returned
  path. A ledger with a broken row went unread and the run exited 0.
- **🟡 2** — the class was half closed: case, symlink and hard link still
  counted one file twice.
- **🟡 3** — the docstring presented the hole as the virtue.
- **🟡 4** — `phase-15.md` gave a false reason for `Contract changes: none`.
- **🟡 5** — the removed `round-13.md` had closed a deferral that did not
  land in round 12's Deferred table.
- **🟡 6** — round 12's `PR` cell said *not yet opened* two rows above a
  cell naming #162.

## What this phase found

**The first repair was composed where a copy existed, thirty lines away.**
`skipped_by_narrowing`'s docstring states the identity this branch chose for
this class in round 1 — *two names are one file when they reach one inode*
— and why a fold on the spelling has a platform inside it. Phase 15 wrote
`normpath` instead. That is round 11's lesson — copy the direction the other
carriers agree on, never compose a fourth — arriving in code an hour later,
from the same orchestrator. The fold is `st_dev`/`st_ino` now with the
`normcase(abspath())` fallback for a path `stat` cannot answer for, the two
lines R3 already records, and the docstring names the earlier fold as the
half-repair it was.

**The path returned is never normalized, because the caller opens it.**
That sentence is the whole of 🔴 1, and it is the sentence phase 15 got
backwards — *which every caller already normalises or opens*, as if opening
were tolerant of a changed spelling. `main` opens; `skipped_by_narrowing`
stats. The fold is the inode; the return is `glob`'s own string.

**Three cases, seen red against the `normpath` fold first, on this machine.**
Two case spellings on a case-insensitive volume → `total: 2 ok` (skipped by
`case_insensitive()` where the volume keeps them apart); a symlink and a hard
link beside the ledger → `total: 3 ok`; a pattern crossing a symlink before a
`..` → exit 0 where exit 2 and one BROKEN row is the truth. All three green
after the change, with R8's two cases and both suites — 46 passed.

**§13, stated and then removed.** Phase 15's fix rested on *every alias
differs only in separators and dot segments*; its one case removed the
`os.sep` guarantee and no other. These three remove the case, link and
symlink-traversal guarantees on the machine that fixes them, and the Windows
leg's green at `c590961` is the platform's own answer for the separator
half — carried in round 13's broad-gate row, not claimed here.

**`Contract changes` names `resolve_patterns` this time.** Signature, arity
and return type are unchanged; the set of returnable values is not — the
spelling returned is now the pattern's, not a normalized one — and both
call sites were revisited: `main` (two calls) opens what it gets and is the
reason 🔴 1 existed; `skipped_by_narrowing` stats what it gets and is
indifferent. An AST comparison of `1380c9f` against `404e769` with
docstrings stripped finds `resolve_patterns` the one changed unit.

**The record corrections carry what they used to say.** Round 12's 🔴 8
grounds, its `PR` cell and its Deferred table, and phase 15's paragraph,
each say what was believed and what round 13 measured.

**The prompt budget is zero. Platform**: seen red on macOS through the
class; the Windows leg's next run on the pull request is the platform half,
and this record does not claim it before that run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `normpath` fold in `resolve_patterns`, and the docstring calling its not folding case a virtue | The inode fold with the pattern's own spelling returned, and a docstring naming the half-repair; R13 |
| *which every caller already normalises or opens* in `phase-15.md` | The same paragraph, saying which caller stats and which opens |
| Round 12's `PR | not yet opened |`, and the Deferred row still naming the Windows leg as owing the `st_ino` answer | `#162, draft since 🔴 8`; the row split, the leg's question marked answered at `3bf0fd6` |

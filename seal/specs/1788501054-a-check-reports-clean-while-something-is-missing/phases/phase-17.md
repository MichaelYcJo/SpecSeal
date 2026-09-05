# 1788501054-a-check-reports-clean-while-something-is-missing — phase 17

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-17.md
— what this phase of the build did, written by the session that ran it when
the phase closed. Not in `plan.md`'s original four: round 14's fixes are work
the plan did not contain, and the phase row was added beside them the way
phases 6 through 16 were. -->

| Field | Value |
|---|---|
| Phase | 17 |
| Commit | 35fbf67 |
| Ran by | orchestrator on fable-5.1 — no smith was spawned, on the owner's standing answer for this branch's fixes |

## What this phase was asked

Round 14's 🔴 and three 🟡 — the verifying round at phase 16's fix:

- **🔴 1** — the Windows leg red at `54819ca` on
  `test_the_path_returned_is_the_one_the_pattern_named`, one of round 13's
  own three cases: it asserted the POSIX answer on both platforms, and
  Win32 collapses `..` lexically before the filesystem is consulted.
- **🟡 2** — the printed ledger name still collapses `lnk/..` through
  `os.path.relpath` in four sites, so a BROKEN row is reported under a
  different existing file.
- **🟡 3** — round 12's corrected Deferred row closed *whether `st_ino == 0`
  arrives on `windows-latest`* on grounds that do not reach it.
- **🟡 4** — the identity rule spelled twice, verbatim, thirty lines apart,
  against `skipped_by_narrowing`'s own closing sentence.

## What this phase found

**Which file a pattern names is the platform's to say, not the case's.**
POSIX follows the symlink before it meets the `..`, so `x/lnk/../ledger.md`
names `<root>/ledger.md` — the ledger with the broken row. Win32 collapses
the `..` first, so the same pattern names `x/ledger.md` — the clean one —
and the leg's log at `54819ca` shows the checker opening exactly that:
`x\ledger.md · 1 ok`, exit 0, against an assertion of exit 2. Both platforms
are right about their own semantics and the checker is right on both. The
case now branches on `os.name` and states each platform's answer, and holds
the checker to it. It does not ask `realpath` for the answer — that was the
first repair, uncommitted, and round 14 declined it for the reason the
file's first case already states: a fixture that asks for its own expected
value agrees with a broken checker.

**Seen red, per branch, per platform.** The POSIX branch is round 13's
assertion unchanged, seen red against the `normpath` fold in phase 16. The
Windows branch was seen red by the leg itself, at run 33942403876 — the
platform printed `1 ok` and exit 0 where the case demanded exit 2 — and the
branch now asserts what the platform printed. **§13 stated**: this machine
cannot execute the Windows branch, the leg's next run at this commit is what
says it is green, and this record does not claim it before that run. Three
consecutive fixes on this branch were green here and red there; this is the
first whose Windows assertion was written from the leg's own output rather
than from a POSIX reading of what Windows would do.

**The rule has one spelling now.** `file_identity(path)` holds the nine
lines — `st_dev`/`st_ino` when `stat` answers with a non-zero inode, the
`normcase(abspath())` fallback otherwise — and both folds call it:
`resolve_patterns`' loop keys on `file_identity(p)`, and
`skipped_by_narrowing`'s loop is one dict comprehension over it. Its
docstring says why one spelling, and points at `skipped_by_narrowing` for
the reasoning it does not repeat. With the `st_ino` guard dropped in the one
copy, `test_an_inode_of_zero_does_not_fold_two_files_into_one` alone goes
red — 1 failed, 20 passed — which is the guard held from one place. Both
suites 46 passed; ruff clean on both files.

**A built zero cannot show one arrives.** Round 12's Deferred row said the
leg's run at `3bf0fd6` had *answered* the question, and what that run
showed is the cases that build a zero inode passing there — what the checker
does with a zero, not that one arrives. The row is reopened with the leg
named as before, and it says what it used to claim. `overview.md:51` had
kept the question open the whole time; the two carriers agree again. A
green leg can never close it: a platform that never produces a zero never
reaches the branch, and the fix is correct either way.

**The named-file half goes to the tracker.** Round 13 closed the class for
the file the checker **opens**; four sites still name the file through
`relpath`, which normalises `..` the way `normpath` does. Exit code and row
are right; the name a person reads is wrong, POSIX-only. Closing it is a
printing helper and four call sites — mechanism from a fix pass, which
#161's first rule refuses — so it is issue #163 for 0.8.1, with the fixture
and the case named.

**`Contract changes` is `none`, by AST.** `7beb9cc` against `35fbf67` with
docstrings stripped: `file_identity` added; `resolve_patterns` and
`skipped_by_narrowing` the two changed units, each body replaced by a call
computing the same value the inline lines did. Signature, arity, return type
and the set of returnable values are unchanged for both — `resolve_patterns`
still returns the pattern's own spelling, `skipped_by_narrowing` the same
candidates. **`New units`** is `file_identity`, depth 1: extracted from
`resolve_patterns`, which predates the run, to answer a finding in it.

**Anchors.** R3 and R13 gain `file_identity`; `skipped_by_narrowing`,
`resolve_patterns` and the third case moved. Stamped from a scratch copy of
the fragment, the diff read before it was copied back — those four anchors
and nothing else. Unscoped read: `545 ok · 1 drifted · 0 broken`, S8 alone.

**The prompt budget is zero. Platform**: the POSIX branch executed here,
the Windows branch written from the leg's output and owed to the leg's next
run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The second copy of the inode fold — nine lines each in `resolve_patterns` and `skipped_by_narrowing` | `file_identity`, read by both; R3 and R13 anchor it |
| The unconditional POSIX assertion in `test_the_path_returned_is_the_one_the_pattern_named` | A branch per platform, each stating what its platform says the pattern names |
| Round 12's Deferred row saying the `st_ino` question was answered at `3bf0fd6` | The same row, reopened, saying what it used to claim; `overview.md:51` unchanged |
| The named-file half of round 13's class — four `relpath` sites | Issue #163, milestone 0.8.1 |

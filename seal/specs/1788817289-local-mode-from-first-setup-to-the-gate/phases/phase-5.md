# 1788817289-local-mode-from-first-setup-to-the-gate — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | the commit this record rides on |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Write the records: the changelog and ledger fragments, `pr-notes.md` with the
four answers `CONTRIBUTING.md` asks a gate change for, the closing memo, the
phase records, and the routing of what this work did not close.

## What this phase found

**`evidence-check --reverify` rewrites a row's hash and does NOT move its
`Checked` date.** Run over the whole tree it re-verified 17 rows in
`seal/ledger.md` — every row whose anchor this branch's edits moved — and each
would then have carried today's content under a date from 2026-09-02, which is
the one thing that column exists to prevent. The shared ledger was reverted
and its nine rows left DRIFTED, which is both the true state and its own
instruction; CI treats drift as a warning (`.github/workflows/test.yml` exits
only at 2 or above), and `overview.md` names what a re-reader owes.

**The fragment is reverified alone with `--ledger <path> .`** — the run says
so itself: *a branch falsifies rows in ledgers it does not own, and those are
the rows with the longest reach.*

**A fragment's table header is read, and the shipped one is `| Clause | Code
grounds | Verified behavior | Checked | Notes |`.** With any other header the
checker reports `0 ok` for the whole file, which is indistinguishable from a
fragment nobody wrote rows into. A markdown anchor is a quoted heading path —
`CLAUDE.md#"## Git">"Routing, decided at the start"` — and a bare `#Git` is
BROKEN.

**`plan.md`'s Alternatives table had to be corrected, not just annotated.**
Two of its rows were overturned by the build, and one of them recorded a
rejection whose stated reason was simply wrong. A plan left arguing with the
code it produced is worse than a plan with a correction in it, so both rows
say what happened and point at `phases/phase-3.md`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `plan.md`'s row rejecting a Bash-wide trigger, and its row's stated reason for rejecting a third arm | corrected in place in the same table, with `phases/phase-3.md` and `overview.md` §*Where spec and implementation diverged* carrying the reasoning |
| nothing else — the 17-row rewrite of `seal/ledger.md` was reverted rather than kept | the nine drifted rows stay in `seal/ledger.md`, named in `overview.md` §*Not done* |

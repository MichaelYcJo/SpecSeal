# 1788501054-a-check-reports-clean-while-something-is-missing — phase 15

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-15.md
— what this phase of the build did, written by the session that ran it when
the phase closed. Not in `plan.md`'s original four: this fix answers a
finding that arrived after the run's terminal record, from the reader the
records had named, and the phase row was added beside it the way phases 6
through 14 were. -->

| Field | Value |
|---|---|
| Phase | 15 |
| Commit | 3026a33 |
| Ran by | orchestrator on fable-5.1 — no smith was spawned; the repository owner chose *fix by the rules* when the Windows leg went red at the pull request, and the fix is one line |

## What this phase was asked

Round 12's 🔴 8 — the finding the `pytest (windows-latest, 3.12)` job made
at `3bf0fd6` on pull request #162, after `round-12.md` was written and
`Pass` ticked: `test_one_file_matched_by_two_patterns_is_read_once` red,
`seal\ledger.md` listed twice with `1 ok` each and `total: 2 ok`. Rounds 2
through 12 had each deferred one question to that leg by name — whether
`st_ino == 0` arrives there. Those cases passed. The leg answered in the
unit beside them.

## What this phase found

**The fold had a platform inside it, one function over from where round 1
took one out.** `resolve_patterns` deduplicated on the string `glob.glob`
returns. `glob` keeps a literal pattern's spelling and joins a wildcard's
matches with `os.sep`, so on Windows `seal/ledger.md` and `seal/*.md` name
one file as `seal/ledger.md` and `seal\ledger.md`, and a set of raw strings
keeps both. Round 1's 🟡 9 found the same shape in `skipped_by_narrowing`
and this branch replaced it there with the inode; `resolve_patterns` kept a
string fold because its concern is *the same glob hit spelled two ways*, and
that is a fold `os.path.normpath` is for — separators and `.` segments
collapse, case does not, so two different files stay two and it is not the
`normcase` mistake. One line.

**The class is testable off Windows, and that is what §15 needed.** *One
file, two spellings* is `./seal/ledger.md` against `seal/ledger.md` on every
platform. The new case built that and failed on macOS with `total: 2 ok`
before the change — R8's case had been green through twelve rounds and every
local run because on macOS and Linux both spellings come back the same.
Executed on the platform where the leg found it is the leg's job; executed
on the class is this phase's, and it is what keeps the fix from being *green
on CI, unverified here*.

**A finding that arrives after the terminal record has no legal round of
its own, and the checker said so.** The first shape tried was a
`round-13.md` recording the CI leg's finding, `Ran by` the leg. `chain_check`
then refused `round-11.md`: round 12 had met the floor with `no` and answered
`no`, so any record after round 12 is a second record after a floor — the
walk this branch itself corrected in rounds 7 through 11 fired on the
branch's own records and named `round-13.md` as the one too many, correctly.
The legal shape is the one `wrote_fixes` was built for: the finding lives in
round 12's own table as 🔴 8, `fixed` at this commit, so round 12 becomes a
record that wrote fixes, the count stops there, and round 13 is the
verifying round that reads them. Round 12's `Pass` is unticked until then
and its `Fixes checked by` says why. The mis-shaped `round-13.md` was
removed in this commit; nothing it said is lost — the row and this record
carry it.

**The reviewer's `no` still stands.** 🔴 8 was not round 12's finding; the
record says who found it and when, in the row and in its trailing comment.
`Needs a fix` stays `no`.

**`Contract changes` is `none`.** `resolve_patterns` returns the same shape
— a sorted list of paths — with the same arity; what changed is which
spelling of a path it returns, which every caller already normalises or
opens. **`New units`** is the one case, depth 1: `resolve_patterns` predates
the run.

**The prompt budget is zero. Platform honesty**: the fix was seen red on
macOS through the class and is expected green on Windows through the
platform; the Windows leg's next run on the pull request is what says so,
and this record does not claim it before that run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The raw-string fold in `resolve_patterns` | `os.path.normpath` over each match, with the docstring saying why and what it does not fold |
| `rounds/round-13.md` as written at `eabbd44` — a record of the CI leg's finding, `Ran by` the leg | Round 12's verdict row 🔴 8 and its trailing comment, and this record; round 13 is now the verifying round's record, written when that round posts |

# 1788501054-a-check-reports-clean-while-something-is-missing — phase 2

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-2.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 93c8b89 |
| Ran by | specseal:smith on opus |

## What this phase was asked

Build phase 2 only: make `evidence_check.py` say which ledgers it did not read
when `--ledger` narrowed it, with a case on the output seen red before the line
exists. Phase 1's guidance binds a session that reads it; this binds the
session that narrows on its own initiative, which is the one the trap was
sprung on.

Coordinate given rather than searched for:
`skills/evidence-check/scripts/evidence_check.py:1379`, `--ledger`,
`action="append"` — the narrowing is a list, so the tool knows exactly what it
was given and can say what it therefore skipped.

## What this phase found

**The default discovery had to become a function before it could be
subtracted from.** The three patterns lived inline in `main`, and the skipped
set is *those patterns minus what was given* — so a second copy would have
been one rule today and two after the first edit to either, with the quiet
half deciding whether a skipped ledger gets named at all. `default_patterns`
and `resolve_patterns` exist for that, and `main` is shorter than it was.

**The notice belongs ABOVE the empty-ledgers exit, and that is the case worth
having.** `--ledger` with a typo in it matches nothing, and the run then says
`no evidence ledgers found — nothing to check` and exits 0. That is the same
sentence a repository with no ledger at all gets, printed in a repository whose
ledgers are sitting right there. Printing the notice first also puts it above
the per-ledger output rather than behind the totals.

**Two paths are compared by real path and normalized case, and a plain string
compare passes every obvious case.** `--ledger seal/ledger.md` and the
resolver's own answer are string-equal, so the mutation that drops the
normalization survived until a case was written for the spelling a person
actually types — `--ledger ./seal/ledger.md`, which globs to a path with `./`
inside it and reads as a second file. That case is
`test_a_second_spelling_of_the_same_file_is_not_reported_as_skipped`.

**`--reverify` gets the notice too, and it is the run that needs it most.**
The narrowing exists FOR the write, so the write is the run most likely to be
narrowed, and every row it did not re-stamp stays whatever it was. Nothing
about the notice reads a skipped ledger: it is a report on what was skipped,
pinned by the case asserting that the broken row in the skipped file never
appears in the output.

**Eight mutations, none surviving.** Return nothing from
`skipped_by_narrowing`; compare raw paths; move the notice below the empty
exit; always plural; count without naming; drop the way back out; exempt
`--reverify`; print it on an unnarrowed run. Each one at a time, restored from
a kept copy rather than from `HEAD`.

**What the branch itself now demonstrates.** The unscoped read at this commit
reports four rows in `seal/ledger.md` that this branch drifted — the handoff
section, the verifying-round section, `evidence_check.py#main` and
`#seal_home` — none of them in this work item's own fragment, so a scoped read
would have reported clean. That is #153's measurement reproduced on the branch
that fixes it. The re-verify is phase 4's, because phase 3 has not finished
editing yet.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The three default ledger patterns spelled inline in `main`, with the comment explaining each | `default_patterns`, whose docstring carries the same comment — and the function is now the single source the skipped set is subtracted from |

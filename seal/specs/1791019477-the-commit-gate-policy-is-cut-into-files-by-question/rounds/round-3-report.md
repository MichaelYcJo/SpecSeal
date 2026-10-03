# Round 3 report — the commit gate's policy is cut into files by question (#727)

| Field | Value |
|---|---|
| Round | 3, verifying round 2's fixes; the run's last round |
| Target SHA | 794cc6a2 |
| Fix range | `70680f16..f7b31c42`, three commits; then the close commit `794cc6a2` |
| Ran by | specseal:warden on claude-opus-5-5 |

This round's target is the diff of round 2's fixes and the close commit, not
the branch. The diff touches three files: `docs/the-record-layout.md` (F1's
last two sentences), this work item's ledger fragment (rows C2 and C5) and
`overview.md` (the K3 and D5 rows). Every probe ran in a `git clone
--no-local` of the worktree at `794cc6a2`, under the round's scratch
directory, with `origin/release/v0.18.0` fetched into it at `9511f6cd`, the
same commit the worktree's remote-tracking ref names. Nothing was written in
the worktree but this file.

Carried from rounds 1 and 2, not re-established: the S1 move probe, the
citation resolver's 21 citations, the `git grep` for a live sentence saying
the row goes away, and the close commit's pin of round 1's report line 141.
None of them sits in the fix range. Re-derived: every verdict below.

## What the account claimed, and what the code showed

- **🟡 4: F1 no longer says the ceiling check depends on the `none` row**
  (commit `9a3db2eb`). True. `docs/the-record-layout.md:179-182` now says
  the row stays and reads `none`, *which says the listing is empty*, and that
  the ceiling is the `Document line ceiling` row, which `fold-check` holds
  every unlisted document to. Both halves hold. `seal/config.md` carries
  `Document line ceiling | 1000` and `Over the ceiling | none`.
  `skills/settle/scripts/fold_check.py#parse_over` returns an empty listing
  for an absent row and for `none` alike, and
  `skills/settle/scripts/fold_check.py#run` skips the length check only when
  the ceiling row is absent. I deleted the row in the clone and ran
  `fold-check`. The output and the exit code were the same with the row
  deleted and with `none`, on the tree and on a padded arms file. The cited
  section, `docs/the-evidence-ledger.md` §*The fold, and what tells it from a
  deletion*, says the ceiling and the list are rows of `seal/config.md`. It
  makes no claim about an absent row, so the citation supports the sentence.
- **C5 is re-stamped with a second Corrected note.** True. Its first anchor
  moved from `0374c5a5` to `d85475bb`, and `evidence-check --strict` reports
  0 drifted. The note reads *Corrected again 2026-10-03 in round 2's fix pass
  (🟡 4)* and states what changed. `correction-check` reads a qualifier
  between the verb and the date as part of the marker
  (`skills/evidence-check/scripts/correction_check.py`, module docstring), so
  a merge that dropped this note would be named. C5's claim cell did not
  change and still holds: the paragraph says the entry went and the row
  stays, reading `none`.
- **⬜ 5: C2's note was corrected** (commit `8d68574a`). True. The note no
  longer says an absent row turns that half of the check off. It now says
  `fold-check` reads an absent row as an empty listing and holds every
  document to the `Document line ceiling`, and my probe confirms that. It
  cites D8 for the decision only: *`none` states the empty listing*. D8's
  grounds do say that, quoting #526's *the listing … empty*. D8's second
  ground repeats the false reason. Round 2 chose to leave D8 and round 1's
  grounds as records of how the decision was made, and I carry that choice.
  The corrected C2 note no longer leans on that ground. No anchor moved, and
  `evidence-check` agrees.
- **⬜ 6: the K3 and D5 rows each have their own cells** (commit
  `f7b31c42`). True. An `awk` cell count over `overview.md:22-28` reads four
  cells on every line, matching the four-column header. Line 24 counts five
  because of its escaped pipe, and it renders as four. K3's row got its
  Grounds back, *`evidence-check` named no drift on S2…*. The D5 row lost
  that trailing cell, and its text is otherwise byte-identical to round 1's
  fix of ⬜ 3.
- **The close commit `794cc6a2`** rewrites only `rounds/round-2.md`. It fills
  the `Fixes checked by`, `Fix range`, `Contract changes` and `New units`
  fields and the three verdicts, and changes no row this round checks.
  `New units` reads `none`, and that is true: the fix range edits prose and
  ledger notes and adds no function, class or heading.

## Findings

None. This round opened nothing that needs a fix and no correction to the
records.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 4 is closed — F1 no longer says the `none` row keeps the ceiling check running; it names `Document line ceiling` as the ceiling | `docs/the-record-layout.md:179-182` | confirmed | executed: `fold-check` with the row deleted gives exit 0 on the tree and exit 1 on a padded arms file, the same output as with `none`; read: `skills/settle/scripts/fold_check.py#parse_over`, `#run`, `#declared`, `seal/config.md`, the cited section of `docs/the-evidence-ledger.md` |
| 🟢 | C5 re-stamped in place with a second dated Corrected note | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C5) | confirmed | executed: `evidence-check --strict` exit 0, 0 drifted; `correction-check` exit 0; read: the note, and the qualifier rule in `skills/evidence-check/scripts/correction_check.py` |
| 🟢 | round 2's finding 5 is closed — C2's note no longer says an absent row turns the check off | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C2) | confirmed | executed: the absent-row probe above; read: the note against `spec.md` D8 and the code |
| 🟢 | round 2's finding 6 is closed — K3 and D5 each have four cells, and K3 has its Grounds back | `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/overview.md:27-28` | confirmed | executed: `awk` cell count, four on lines 22–28 (24 counts its escaped pipe); read: the diff of `f7b31c42` |
| 🟢 | the four checks over `794cc6a2` pass | `794cc6a2` | confirmed | executed: `evidence-check --strict .` exit 0, 0 drifted, 0 refused; `correction-check --range origin/release/v0.18.0...HEAD` exit 0; `survivor-check --range 2b1dcb1f...HEAD --exempt survivors.md` exit 0; `fold-check --root .` exit 0 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/evidence-check --strict .` | exit 0: 4080 ok, 0 drifted, 0 broken; records arm 5 work items read, 1217 names read, 0 refused, 0 drifted |
| `bin/correction-check --range origin/release/v0.18.0...HEAD` | exit 0: one merge commit examined in `9511f6c..794cc6a`, no correction marker dropped, no released ledger file changed |
| `bin/survivor-check --range 2b1dcb1f...HEAD --exempt` this item's `survivors.md` | exit 0: 679 files against 66 removed sentences; one exempt place, 1790815613's overview line 49 |
| `bin/fold-check --root .` | exit 0: 157 statements in 18 documents, 0 listed over the ceiling of 1000 |
| a one-file `test_tmp_*` probe, run once and deleted: `fold-check` with `Over the ceiling` at `none` and with the row deleted, each on the tree and with the arms file padded to 2,650 lines | `none` and deleted gave identical output: exit 0 on the tree; exit 1 on the padded file, naming the arms file over the ceiling of 1000. Both files restored, clone status empty |
| `awk` cell count over `overview.md:18-30`, the pipe as separator | 4 cells on lines 22, 23 and 25–28; 5 on line 24, from its escaped pipe |
| `bin/test -q` over the docs line-wrap, fold-room and no-real-identifiers modules | 83 passed |
| the broad gate: full suite, repository-wide lint, typecheck | not yet. It belongs to the sealer and runs once after the rounds settle. Nothing in this round ran it |

## What was read and not executed

- That deleting the `Document line ceiling` row turns the length check off:
  read from `skills/settle/scripts/fold_check.py#run`, not run. F1's sentence
  rests on this half only by naming the row.
- That D8's first ground quotes #526's *the listing … empty*: read in
  `spec.md` at D8.

## The gate has come due

This report leaves nothing open. The sealer's spawn is now due for the broad
gate. That run is the sealer's, not one for the session reading this report
to assemble.

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, all at `794cc6a2` in the clone:
- `docs/the-record-layout.md` (lines 165–186)
- `docs/the-evidence-ledger.md` (lines 290–312)
- `seal/config.md`
- `templates/config.md` (the ceiling rows, via `grep`)
- `skills/settle/scripts/fold_check.py` (lines 509–620; the function list)
- `skills/evidence-check/scripts/correction_check.py` (the marker lines, via `grep`)
- `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (rows C2 and C5, through the diff)
- `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/`: `rounds/round-2.md`, `rounds/round-2-report.md` (header and lines 112–145), the D8 lines of `rounds/round-1-report.md` and `rounds/round-1.md` (via `grep`), `spec.md` (D8 and the lines that cite it), `overview.md` (lines 18–30)
- `git diff 70680f16..794cc6a2`

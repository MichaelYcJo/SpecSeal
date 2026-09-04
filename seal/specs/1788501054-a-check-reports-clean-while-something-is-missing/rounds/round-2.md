# 1788501054-a-check-reports-clean-while-something-is-missing — review round 2

| Field | Value |
|---|---|
| Target SHA | 4b72d7e |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | not yet — no broad run has happened on this branch at all |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | `fix_surface` gained an arm and a second cutoff, its return shape unchanged → `main`, its only call site; `skipped_by_narrowing` now falls back on a zero `st_ino` as well as on `OSError` → `main` |
| New units | `says_not_yet` (depth 1); `NOT_YET` (depth 1); `surface_run` (depth 1); `PENDING` (depth 1); `checker_module` (depth 1); `test_the_pending_spelling_is_the_one_the_template_prints` (depth 1); `test_a_surface_still_pending_after_a_round_read_the_fixes_fails` (depth 1); `test_the_same_arm_reaches_contract_changes` (depth 1); `test_the_honest_mid_run_state_is_not_refused` (depth 1); `test_a_bare_none_after_the_fixes_landed_passes` (depth 1); `test_a_reason_the_checker_does_not_recognise_passes` (depth 1); `test_the_pending_surface_only_prints_before_the_cutoff` (depth 1); `test_a_work_item_between_the_two_cutoffs_owes_the_rows_and_not_this_arm` (depth 1); `test_the_pending_surface_cutoff_is_this_work_items_own_second` (depth 1); `test_every_description_of_which_add_is_read_says_the_latest` (depth 1); `test_the_docstring_says_what_the_flag_now_protects` (depth 1); `test_the_spec_points_at_the_row_it_means` (depth 1); `test_the_spec_carries_the_delete_and_re_add_state` (depth 1); `test_an_inode_of_zero_does_not_fold_two_files_into_one` (depth 1); `test_a_ledger_that_cannot_be_stat_ed_is_named_rather_than_crashing` (depth 1) |
| Needs a fix | yes — seven 🟡. The heaviest is that this branch's own rule made `round-1.md`'s fix surface start as `none` and left nothing requiring the second step, so a verifying round reading the record alone sees no finding surface at all |
| Loses a record or crashes | no |

- [ ] Pass

<!-- Written and committed before the fix pass it commissions. And its own
`New units` row above will need the reach-back this round's 🟡 3 is about —
which is the point: the row is honest now and becomes false by omission if
nobody returns to it. -->

## What this round was asked

The verifying round at `git diff 148bd10..HEAD`, with round 1's ten verdicts as
the agenda and the six units its fix pass created as the finding surface.

**And one instruction it was right to disobey.** The prompt said `round-1.md`'s
`New units` names those six. It did not — it read `none — the fixes are not yet
written`. The prompt also told the round to *read the record, not any prose
about it*, which is what caught it. That is the **fourth** instance on #150 of
prose about a record disagreeing with the record, all four the orchestrator's,
and none of the four visible to a check.

Seven surfaces in order: whether the `found[-1]` → `found[0]` inversion moved
anything nobody re-measured; the surviving mutation and what was done instead;
whether 🟡 7's bound sentence sits where a reader meets the refusal; whether the
eight ledger claims were re-read rather than re-dated; the inode fold's fallback;
`phases/phase-5.md` against the round record's own columns; and the
self-application in the state this round would actually put the record in.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 1's four, in code | four files | answered | All four closed. `found[0]` reverted → exactly one red, the new delete-and-re-add case. The inode fold takes hard links, case spellings and symlinks in one rule, executed. The reach case runs the **same late record twice**, differing only in whether the cell carries a SHA — 1 refused, 0 passed — so the exit code cannot have come from elsewhere |
| 🟢 2 | The six new units, as code | two test files | answered | `case_insensitive` probes the same filesystem the fixture is built on, closing the one path that would make it meaningless. The hard link is named outside the candidate glob so it stands on the read side alone. `late()` rewinds with `git checkout -B` each call, so the same item twice does not contaminate. AST diff over the range: **zero top-level units added or removed in either checker**, six added in test files — the depth argument holds |
| 🟢 3 | The self-application, in the state this round creates | `chain_check.py` | answered | Executed in a clone: round-1's four cells set to `**fixed** \`b87ba49\``, `Pass` checked, `Fixes checked by` set, committed — **the ordering refusal still does not fire**. `merge-base --is-ancestor b87ba49 148bd10` exits 1, and the range holds one add (`4b72d7e` is a touch) |
| 🟡 4 | `added_on_branch`'s summary line still says *first added* while its body says the opposite twenty-six lines later | `chain_check.py:1945` | open | A reader skimming the function reads the summary. This is the function round 1 found undefended, and the inversion left its first line stating the old rule |
| 🟡 5 | The case docstring and the spec both still say *oldest commit that touched the file*, and both are now false by measurement | `tests/…:381`, `docs/review-chain-spec.md:885` | open | Executed: dropping `--diff-filter=A` turns **two** cases red, one of them the updated-in-place case the docstring says it does not reach. `phases/phase-5.md` knew — *"the mutation count moved from 1 red to 2"* — and put it in the ledger row alone. The spec is the costlier copy because it is what a reader opens |
| 🟡 6 | `round-1.md`'s fix surface is still `none — the fixes are not yet written`, so a verifying round reading the record alone sees no finding surface | `rounds/round-1.md:10-11` | fixed by the orchestrator at this commit | **This branch created the state.** Before `ORDER_FROM` a record could be written after its fixes and the rows filled from the start; now they must start empty and nothing requires the second step. `fix_surface` accepts `none — <reason>`, so the checker is silent — which is this work item's own title, produced by this work item |
| 🟡 7 | The `Needs a fix` row still carried 231/19 after the commit that existed only to correct that count | `rounds/round-1.md:12` | fixed by the orchestrator at this commit | §12: the correction went to the coordinates it was pointed at and did not sweep the class. That row is the one an orchestrator copies forward and the one holding the run's terminal condition |
| 🟡 8 | The inode fold goes **silent** where `st_ino` is 0 | `evidence_check.py:930` | open | Python's own contract is *"if non-zero, uniquely identifies the file"*, and CPython's Windows `stat` leaves both fields 0 when it cannot open a file. Executed with both zeroed: an unread fragment is named by nothing. That is the silence this notice exists to end, and the reverse of the direction its docstring declares. `OSError` reaches the fallback; a zero does not. CI runs a `windows-latest` leg |
| 🟡 9 | The bound sentence's pointer names the wrong row | `docs/review-chain-spec.md:888` | open | *"the third style above"* — counting all rows or pass rows alone, neither third is the no-commit row it means. The sentence exists so a reader can find the limit themselves, so a wrong pointer is the whole of it |
| 🟡 10 | Fragment row R6 says no column can distinguish a re-read that happened from one that did not, and the same commit disproved it four times | `seal/ledger/1788501054-*.md` R6 | open | Four of the eight rows carry a `Re-read 2026-09-04` clause in Notes; four do not, and their re-reads live in `phases/phase-4.md`. The date cannot distinguish; the Notes column can, and the fix pass used it |
| ⬜ 11 | `phases/phase-5.md` itself is legitimate | `phases/phase-5.md` | answered | A round's fixes made a commit and that commit's record belongs somewhere. What is wrong is not the file but that the round record's own designated columns were left empty while the fact lived only here — 🟡 6 |

## Executed probes

| What was run | Result |
|---|---|
| `pytest`, the two changed suites plus `test_evidence_check.py` | 59 passed |
| the ledger sample — two suites two re-read rows cite | 45 passed |
| `evidence_check.py .` **unscoped** | exit 1, `521 ok · 1 drifted · 0 broken` — S8 only, as on the base |
| `found[0]` → `found[-1]`, 23 cases | **1 red** — the delete-and-re-add case |
| `--diff-filter=A` dropped, 23 cases | **2 red** — 🟡 5 |
| `C12`: `SHA_RE.findall(...) or ["HEAD"]` | **23 passed** — survivor confirmed, and `overview.md` says so |
| `skipped_by_narrowing` with `st_ino`/`st_dev` zeroed | **skipped comes back empty — silent** — 🟡 8 |
| the same with `os.stat` raising, on either side | over-reports, as declared |
| AST diff of top-level units over `148bd10..HEAD` | 0 in both checkers, 6 in test files |
| the self-application with the cells filled | ordering refusal does not fire |
| `uvx ruff check`, four changed Python files · `unverified-check` | clean · exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `added_on_branch` and everything that describes it | Round 1 found it undefended; round 2 found the inversion left three descriptions of the old rule standing, one of them false by measurement |
| round 1 | the eight re-stamped `seal/ledger.md` rows | Round 1 found three impossible dates; round 2 found the repair recorded on four rows and not the other four, and R6 claiming that is impossible |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `st_ino == 0` actually occurs on `windows-latest` — the round measured what the code does with a zero, not that a zero arrives | `overview.md` §Not verified | the windows CI leg at this pull request |
| `questions.md` Q2 and `seal/ledger.md` S8 | carried from round 1 | the repository owner |
| **The broad gate, still not run at all on this branch** | `overview.md` §Not verified | the orchestrator, once the rounds settle |

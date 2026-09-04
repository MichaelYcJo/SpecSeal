# 1788501054-a-check-reports-clean-while-something-is-missing — review round 3

| Field | Value |
|---|---|
| Target SHA | 8af3494 |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | not yet — no broad run has happened on this branch at all |
| Fixes checked by | round-4 |
| Contract changes | none — measured, not asserted. An AST comparison of `8af3494` against `ae271ba` with docstrings stripped shows **zero** top-level units added, removed or changed in either checker: `fix_surface`, `says_not_yet` and `skipped_by_narrowing` are executable-identical, and every fix to them is a docstring, a document, a record or a ledger row |
| New units | `test_a_forgotten_checker_cell_leaves_the_arm_nothing_to_key_on` (depth 1) → pytest only; `test_the_terminal_value_is_in_the_specs_table_with_what_it_costs` (depth 1) → pytest only; `test_the_declared_limit_names_what_escapes_with_the_words_unchanged` (depth 1) → pytest only; `test_two_devices_that_share_an_inode_number_are_two_ledgers` (depth 1) → pytest only; `test_the_skipped_set_is_subtracted_from_the_list_the_defaults_come_from` (depth 1) → pytest only; `test_one_file_matched_by_two_patterns_is_read_once` (depth 1) → pytest only |
| Needs a fix | yes — eight 🟡, and the two heaviest are this branch breaking the rule it adds. 🟡 1: the pending arm's key is `Fixes checked by`, which the same lapse leaves unwritten, so it reaches the half-forgetful session and not the forgetful one — and `round-1.md`, the record whose state the arm was built to refuse, passes it. 🟡 2: `c528161` re-stamped ten `seal/ledger.md` rows and left two without a re-read clause, which R6 — written in that same commit — forbids |
| Loses a record or crashes | no |

- [ ] Pass

<!-- The verifying round of this run, and it reopened it. The floor's bound
allows exactly this: a verifying round that opens something is a finding
round, so its own fixes need a reader in turn, and the count stops at this
record. Written and committed before the fix pass it commissions, so both
fix-surface rows start pending and owe the reach-back this work item's own
arm was built to require.

TWO CASES WERE WIDENED rather than added, and the two were widened for
different reasons. This sentence used to sit inside the `New units` cell,
where `depth_problems` read it as part of the sixth entry and refused the
whole cell for carrying several units and a comma under one `(depth 1)` —
round 4's 🔴 1. It belongs here because the cell is parsed and this comment
is not.

  `test_a_reason_the_checker_does_not_recognise_passes` — the finding is
  inside `says_not_yet`, which round 2's fix pass created and `round-2.md`'s
  own `New units` names. A unit added to answer a finding there is depth 2,
  which the rule refuses. Widened because it HAD to be.

  `test_an_inode_of_zero_does_not_fold_two_files_into_one` — the finding is
  inside `skipped_by_narrowing`, which this branch's PHASE 2 created at
  `93c8b89` (`phases/phase-2.md`'s `Commit` cell), before the review run
  began. Depth is measured per run, so a unit there is depth 1 and the rule
  allows one. Widened BY CHOICE, to keep the identity rule under one case
  rather than two.

  The cell gave the first reason for both, which is round 4's 🟡 2: it is
  true of the first and false of the second. Round 3's fix pass had written
  the correction down and this cell wrote it back out.

CORRECTED IN PLACE, and this is the trace the record itself owes (round 4's
🟡 7, applied as one rule to every such correction on this branch):

  `New units` — round 4's fix pass, at this commit. It carried the widening
  paragraph above inside its sixth entry; the six entries now stand alone.
  Marking it inside the cell is what the checker refuses, so the trace is
  here. -->

## What this round was asked

The verifying round at `git diff 4b72d7e..8af3494`, with round 2's eleven
verdicts as the agenda and what round 2's `New units` row names as the finding
surface — a unit the fixes created has been reviewed by nobody.

**Ten specific things to try to break**, named in the prompt with their
coordinates so the round did not spend itself finding them: the pending arm's
behaviour at the terminal state this round's own record creates; what escapes
`says_not_yet` beyond the declared rewording; the cutoff the arm is keyed to,
by mutation; every new case against §15; `skipped_by_narrowing`'s zero-`st_ino`
fallback for over-reporting and for one field zero rather than both; the
`Contract changes` reach, by `grep`; `New units` as a measurement, by AST diff;
§12 on 🟡 4, 5 and 9 — class or coordinate; the ten ledger rows and the
unscoped `evidence_check`; and the self-application re-measured at HEAD.

**Four axes named for this change beyond the table's floor**, because it is a
gate change: failure direction (the branch takes `allow` for the pending arm,
the only such place in the file, while `CONTRIBUTING.md` and this branch's own
`plan.md` declare `blocks more`); grandfathering boundaries (two cutoffs, and
an arm keyed to one of them); self-application; and document claims pinned by
tests.

**And the correction it was handed:** the orchestrator's prose about a record
had been wrong four times on this branch, none of them visible to a check, so
the instruction was to open the record and not the prose about it — including
the prose in that prompt. It found a fifth, below.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The pending arm cannot fire on the record it was built for. `fix_surface` reads the pending cell only when `Fixes checked by` matches `^round-\d+$`, and a `nobody — <why>` cell is a notice everywhere else in the checker. A session that forgets the reach-back leaves all three cells, so the arm reaches only the half-forgetful one | `chain_check.py#fix_surface`, `rounds/round-1.md:9` | open | **Executed** in a `--no-local` clone at HEAD: `round-1.md` with both rows pending and `Fixes checked by | nobody |` exits 0 and the arm says nothing; the same rows with `round-2` exit 1 naming both. Orchestrator re-verified: `git merge-base --is-ancestor b87ba49 4b72d7e` exits 0, so round 2 did open round 1's fixes and the cell is stale. Two things are owed and they separate — the cell is data, the escape is a paragraph in `docs/review-chain-spec.md:668` |
| 🟡 2 | Two `seal/ledger.md` rows re-stamped by `c528161` carry no re-read clause. R6, rewritten in that same commit, reads *"the trace goes in the Notes, on every row a re-stamp touched"* | `seal/ledger.md:181`, `seal/ledger.md:191`, `seal/ledger/1788501054-…md` R6, `phases/phase-4.md:64` | open | **Executed**, row by row against `origin/release/v0.8.0`: `changed=10 restamped=10 with_reread_clause=8`. Orchestrator re-verified the same two counts. Only the hash moved on each — `fix_surface@912ae33e → @b1766d9d` — and `Checked` stayed at `2026-09-04`, the date round 1 already showed cannot tell a re-read from a re-stamp. This is §12: `phase-4.md:64` enumerated the class as eight and phase 6 grew it to ten with nobody re-enumerating. The third `fix_surface` row, `:189`, did get its clause in the same pass, which makes this an omission rather than a policy |
| 🟡 3 | `Fixes checked by` has three legal values and the spec's new table enumerates two of them against the pending cell, omitting `no fixes to check` — the value the terminal record of every run carries | `docs/review-chain-spec.md:653-655` | open | **Executed** in the clone at the state this record creates: a round-3 record with `Needs a fix: no` and `Pass` ticked exits 0, so the run's legal ending is not refused. What is unsafe is that a round commissioning no fixes will never have fixes, so *not yet written* on its rows is false the moment it is written and nothing will ever say so. Whether the arm should also refuse that pair is a judgment, deferred below |
| 🟡 4 | `says_not_yet`'s docstring states its own match backwards — *"the reason after the separator is matched as a PREFIX of `NOT_YET`"*, where the code makes `NOT_YET` the prefix of the reason | `chain_check.py:1567-1570` vs `:1589` | open | **Read**, and orchestrator re-verified both lines. As written, `none — the` would match and `none — the fixes are not yet written (round 2)` would not, the reverse of both examples beside it. This is the class the round under review spent itself on — three descriptions corrected at its own 🟡 4 and 🟡 5 — recurring in the function the same commit added |
| 🟡 5 | The declared limit is narrower than the limit that exists. `docs/review-chain-spec.md:674`, ledger row R7 and the changelog fragment all say the escape is a **rewording**; three spellings escape with the template's words unchanged | `docs/review-chain-spec.md:674`, `seal/ledger/1788501054-…md` R7 | open | **Executed**, 23 spellings through `says_not_yet` and `says_none`. Case, emphasis, trailing clause, trailing punctuation and every separator in `SEPARATORS` are caught as declared. Orchestrator re-ran the three that are not: `none ― …` (U+2015), `none — the  fixes…` (doubled space) and `none — nothing yet; the fixes…` all return `says_none` True and `says_not_yet` False. `says_none` tests `rest[0]` alone while `says_not_yet` strips `SEPARATORS` from both ends, so one dash outside that set passes the cell as `none` and silences the arm |
| 🟡 6 | The choice of `st_ino` over `st_dev` as the identity test is argued in the docstring and held by nothing | `evidence_check.py:946`, `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:225` | open | **Executed** on a purged bytecode cache: swapping `info.st_ino` for `info.st_dev` leaves the suite green. Orchestrator re-ran the mutation — 38 passed, nothing red. `test_an_inode_of_zero_does_not_fold_two_files_into_one` zeroes **both** fields, so it cannot separate them; a zero inode on a real device is the state that does. This is round 1's 🟡 8 shape — a documented decision twenty green cases did not hold — one commit later, on the fix for round 2's 🟡 8 |
| 🟡 7 | Nothing pins that the template's phrase has to START the reason | `chain_check.py:1589` | open | **Executed**: replacing `rest.strip(SEPARATORS).startswith(NOT_YET)` with `NOT_YET in rest` leaves every case green. Orchestrator re-ran it — **164 passed**. The docstring's own contrast, `none — nothing was added`, cannot separate them because it contains the phrase nowhere |
| 🟡 8 | `Contract changes` calls `main` the only call site of `fix_surface`, and both changed units have a second one — in tests, which is #57's largest regression class exactly | `rounds/round-2.md:10` | open | **Read**, and orchestrator re-grepped: `tests/test_chain_check_at_the_pull_request.py:1301` calls `chain.fix_surface` directly inside the case that runs the per-record checks over **every real round record in this repository**, and `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:260` calls `module.skipped_by_narrowing` directly. Four real records in this tree sit in the refused state today and only the cutoff keeps that case green |
| 🟢 9 | Round 2's 🟡 4 — `added_on_branch`'s summary line said *first added* | `chain_check.py:2033` | answered | **Executed**: the summary now reads *"The LATEST commit on THIS BRANCH that added `rel`"*, and restoring the old wording turns `test_every_description_of_which_add_is_read_says_the_latest` red |
| 🟢 10 | Round 2's 🟡 5 — the case docstring and the spec said *oldest commit that touched*, false by measurement | `chain_check.py:2066`, `docs/review-chain-spec.md:907` | answered | **Executed**: dropping `--diff-filter=A` turns two cases red — `test_a_record_updated_in_place_when_the_fixes_landed_passes` and `test_a_record_added_before_the_base_and_updated_on_the_branch_passes`. Both descriptions now say what the flag protects. The class was swept: the only surviving copy of the old rule is `phases/phase-3.md:53`, kept deliberately as a record of its own moment, and the new needle is built from two pieces so it does not satisfy itself |
| 🟢 11 | Round 2's 🟡 6 — `round-1.md`'s fix surface stuck at the pending value | `rounds/round-1.md:10-11` | answered as data, and reopened as a rule at 🟡 1 | **Executed**, AST diff over `148bd10..b87ba49`: the six units the row now names are exactly the six the fix pass added. The rows are filled at `47e6ebf`. What is not closed is that the checker built to stop the recurrence cannot fire on this record |
| 🟢 12 | Round 2's 🟡 7 — the `Needs a fix` row carried 231/19 after the commit that existed to correct it | `rounds/round-1.md:12` | answered | **Read**: the row now reads 20/235, and every surviving `231`/`212`/`19` in the tree is a record describing the correction rather than repeating it |
| 🟢 13 | Round 2's 🟡 8 — the inode fold went silent where `st_ino` is 0 | `evidence_check.py:930` | answered for the behaviour, reopened for the choice at 🟡 6 | **Executed** on a clean bytecode cache: with both fields zeroed the unread fragment is named, and dropping the `st_ino` test makes the run silent again. It does not name a ledger it read at any spelling `abspath` unifies; it over-reports a hard link once the inode is zero, which is the declared direction |
| 🟢 14 | Round 2's 🟡 9 — the bound sentence's pointer named the wrong row | `docs/review-chain-spec.md:911` | answered | **Executed**: it now reads *"the bolded row above"*, the bolded row above it is the no-commit one, and restoring *"the third style above"* turns `test_the_spec_points_at_the_row_it_means` red |
| 🟢 15 | Round 2's 🟢 1, 🟢 2, 🟢 3 and ⬜ 11 | four files, `chain_check.py`, `phases/phase-5.md` | answered | Carried on round 2's own coordinates and not re-derived: nothing in `4b72d7e..8af3494` disturbs them. `New units` re-measured as a claim rather than inherited — AST diff over the range gives 2 units in `chain_check.py`, 3 and 15 in the two test files, **20**, matching the row entry for entry, every one depth 1 |
| ⬜ 16 | Round 2's 🟡 10 — R6 claimed no column can show a re-read | `seal/ledger/1788501054-…md` R6 | open, carried as 🟡 2 | The rewrite landed; the class it names did not. Ten rows, eight clauses. Kept as its own row because a deferral that leaves this file leaves the inheritance range |

## Executed probes

| What was run | Result |
|---|---|
| `.venv/bin/pytest` over the five suites reading the two checkers | **164 passed** — reviewer, then orchestrator, at `8af3494` |
| twelve mutations across `chain_check.py`, `evidence_check.py` and `docs/review-chain-spec.md`, each against three suites, `PYTHONDONTWRITEBYTECODE=1` and `__pycache__` purged between runs | ten died, **two survived** — 🟡 6 and 🟡 7. A first pass returned a false survivor from a stale `.pyc`, which is why the cache is purged |
| `rest.strip(SEPARATORS).startswith(NOT_YET)` → `NOT_YET in rest` | **164 passed** — orchestrator re-ran it; the survivor is real |
| `info.st_ino` → `info.st_dev` in `skipped_by_narrowing`, cache purged | **38 passed** — orchestrator re-ran it; the survivor is real |
| `excused_order` keyed to `SURFACE_FROM`, to `False`, to `True` | 1 red, 2 red, 3 red — the keying is held, and `test_a_work_item_between_the_two_cutoffs_owes_the_rows_and_not_this_arm` is what holds it |
| 23 spellings through `says_not_yet` and `says_none` | three escape with the words unchanged — 🟡 5. Orchestrator re-ran the three |
| six `skipped_by_narrowing` scenarios — both fields zero, inode only, device only, hard link each way — at HEAD and under the `st_dev` swap | a zero inode on a real device is the separating state; the swap returns the silence |
| `--diff-filter=A` dropped, the case battery | 2 red, naming the ordinary updated-in-place case |
| `chain_check.py --baseline base` in a `git clone --no-local`, at five record states | HEAD · round 3 written · round 3 left pending · `round-1.md` reverted to pending · `round-1.md` set to `round-2` |
| the proposed one-cell replacement for 🟡 1, applied in the clone | `chain_check.py` prints **nothing at all** for `round-1.md`; the only lines left are `round-2.md`'s honest mid-run pair. The replacement is below this table |
| AST diff of top-level units over `4b72d7e..8af3494` and over `148bd10..b87ba49` | 20 and 6 — both `New units` rows are accurate, entry for entry |
| row-by-row diff of `seal/ledger.md`, `origin/release/v0.8.0` against `8af3494` | `changed=10 restamped=10 with_reread_clause=8` — 🟡 2. Orchestrator re-ran both counts |
| `grep` for the call sites of `fix_surface` and `skipped_by_narrowing` | two each, not one — 🟡 8. Orchestrator re-grepped |
| `evidence_check.py .` **unscoped** | exit 1, `525 ok · 1 drifted · 0 broken` — S8 alone, `@45edf260` intact, as on the base |
| `chain_check.py --baseline origin/release/v0.8.0` | exit 1, four lines. `release/v0.8.0` does not resolve in this worktree and exits 2 refusing to compare |
| `uvx ruff check` on the four changed Python files · `bin/unverified-check` · `fold_ledger.py --check` | clean · exit 0 · exit 1 on the branch **and on the base** — four ungathered fragments, the ordinary state between releases |
| `git status --porcelain`, `git rev-parse HEAD` after the round | empty, `8af3494` — HEAD did not move, the probe file is deleted, both scratch clones are removed |

The replacement the tenth row ran, which is 🟡 1's data half:

```
| Fixes checked by | round-2 |
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `added_on_branch` and everything that describes it | Round 1 found it undefended, round 2 found three descriptions of the old rule standing, round 3 found the class swept and one copy deliberately kept. The next round opens it to check nothing returned |
| round 1, round 2 | the re-stamped `seal/ledger.md` rows | Three rounds, three different counts of the same class — three impossible dates, then four rows repaired and four not, now ten touched and eight clauses. The count is what keeps moving |
| round 2 | `round-2.md`'s `New units`, the 20 units | Re-measured here and accurate. It is the finding surface a fourth round inherits only if the fixes add to it |
| round 3 | `chain_check.py#says_not_yet`, `chain_check.py#fix_surface`, `evidence_check.py#skipped_by_narrowing` | The three units this round's eight findings sit in. Two carry surviving mutations |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **The broad gate, still not run at all on this branch** — the full suite, the repository-wide lint and the typecheck | `overview.md` §Not verified | the orchestrator, once the rounds settle. `agent-contract` §2 gives it one run after that |
| Whether `st_ino == 0` actually arrives on `windows-latest` — what is measured is what the checker does with a zero, not that a zero comes | `overview.md` §Not verified | the windows CI leg at this pull request — carried from round 2, unchanged |
| Whether the pending arm should also refuse the cell beside `no fixes to check` (🟡 3). A refusal there lands on merged records whose repair is honest, unlike the `nobody` case | `questions.md` | the repository owner |
| `questions.md` Q2 and `seal/ledger.md` S8 | carried from rounds 1 and 2 | the repository owner |
| The orchestrator's prose about a record was wrong a **fifth** time — this round's spawn prompt said the target range held three commits and named `4b72d7e` as where 🟡 6 and 🟡 7 were fixed. It holds four, and the fixes landed at `47e6ebf`, the record's own commit. The round checked it because it was inside the range | this row, and `docs/flow.md` has no numbered row for it | nobody yet — no check sees this class, and the habit that catches it is *open the record, not the prose about it* |

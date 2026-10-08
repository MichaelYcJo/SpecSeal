# Implementation Plan: a round-record cell has one reader (#866)

<!-- seal/specs/1791384155-a-round-record-cell-has-one-reader/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

Five judgments about a round record are each read by two to four scripts and
the copies disagree (`spec.md` §*Scope*). Every one gets one reader in
`chain_check.py`, which `round_record.py`, `broad_gate.py` and
`release_seal.py` already load, and each copy leaves the tree. Where two
callers legitimately differ — the generator printing a bound the gate would
refuse, the broad gate checking a cell it is about to write — the difference
is a parameter of the one reader, printed, not a second copy. Seven phases,
one judgment or one coupled pair each, in the order that keeps the sibling
seams smallest.

## Technical context

- **Loader shapes**, so the one reader needs no new home.
  `round_record.py:264` loads `chain_check.py` at import and refuses with
  exit 2 when it is missing; `broad_gate.py:228,357` loads it by path under
  `Refused`; `release_seal.py:265–280` loads it lazily and runs only in
  `.github/workflows/publish-release.yml`. `chain_check.py:363,870` loads only
  `unverified_check.py` and `hooks/routing.py`. Adding a module would put a
  fourth file on three load paths and a new row in
  `tests/test_a_script_copied_alone_exits_2.py`; adding to `chain_check.py`
  changes none of that.
- **The copies**, with the lines a phase opens: `spec.md` §*Scope* table.
- **The pull-request state's consumers.** `chain_check.py:5083–5084` sets
  `strict = state != "draft"` once and hands it to `check_round`, `checked_by`,
  the record-count arm and `broad_gate`. `--sealing` is read beside it and
  reaches only the `broad_gate` arm on the last record.
- **Where the gate calls the check.** `broad_gate.py:3441–3445` runs the
  chain arm after the suite, the ledger and the unverified arm, with
  `env=draft_env(keep)`; `seal` then runs `run_check` after the write
  (`round_record.py:5004`). The arm's kept text (`chain.txt`) is read by
  `tests/test_the_seal_is_taken_once_by_the_sealer.py:7971` as an arm's input.
- **The generator's exit is the check's.** `new`, `close` and `seal` each
  `return run_check(…)` (`round_record.py:2855,4592,5004`), so J4's change in
  the no-`gh` population shows up as those commands' exit codes.
- **Two documents sit at the ceiling.** `docs/review-chain-spec.md` is 999
  lines and `docs/round-record-spec.md` 994 of the 1,000 `seal/config.md`
  allows (`Document line ceiling`), and `Over the ceiling` reads `none`. Every
  document edit in this work is a replacement measured by `wc -l` after the
  edit; `questions.md` W1 is the fallback.
- **What breaks in six months.** A fifth script that needs a cell and reads
  it with a one-line regex rather than loading `chain_check.py`, because the
  loader is a `spec_from_file_location` dance and the regex is shorter. The
  registry #835 frames is what makes that visible; this work's part is to
  leave no copy for the next one to be copied from, and to say the class of
  every reader it adds so the registry can take it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A new `record_reader.py` under `skills/code-review/scripts/` holding every cell reader, loaded by all four scripts | a fourth sibling on three load paths; `chain_check.py` would load it too, so the copied-alone test gains a row and a second refusal sentence per script; and `chain_check.py` already is the reader the documents name as the authority | rejected — the module exists, it is `chain_check.py` |
| J1: the panel reads a bare `yes` as `capped`, as today, because the gate refuses it anyway | the gate refuses it only above `NEEDS_FROM` and prints below it, so a grandfathered record's panel claims a cap the check never read | rejected — a cell the check refuses answers nothing |
| J2: keep the panel's prose reading (an issue or a path anywhere after the word) and make it the one reader | the release seal and the generator would then read prose too, and `deferred #854 — see #858` would name two homes in one; the inventory's class is the prose reading | rejected — the writer's shape is the grammar |
| J2: refuse a `deferred` whose home is not `#N` or a path | `deferred the frame` is written by `new` and `deferred a new issue` by a smith, both legitimate; refusing words is a new wall for a shape the documents allow | rejected — the home is read as written and an issue is recognised, not required |
| J3: an owned `Unit` column in the verdict table, filled by the reviewer | changes `VERDICT_HEADER`, pinned in three places (`tests/test_the_report_standard_is_one_in_three_places.py`), every fixture table, and the warden's report format; and a column a reviewer fills by hand is prose with a heading until something refuses it | rejected — the path-form reading is already the owned shape, and the warden is already told to write it |
| J3: keep the wide reading for `depth_two` and declare it, as #823 decided | two readers of one cell is the class this issue is about, and the wide reading has read nothing the narrow one would not on any record in the tree | rejected — overturned on the measurement, `spec.md` J3 |
| J4: make `pull_request_state` accept an `assumed` state the generator passes, and keep `gh` in the generator | an override with a name, which the policy table rejected; and the generator's `gh` call would still be a second source of one fact | rejected — the source moves into the reader |
| J4: drop the broad gate's pre-seal chain arm and let `seal`'s post-write check be the one run | removes a reader and a payload writer at once; but the arm has a panel row and a kept `chain.txt` that the stamp's cases and the preflight read, so dropping it moves #869's rows | rejected here; named for #869's frame as a seam |
| J4: judge the gate's chain arm as a draft when `gh` says draft and otherwise strict, with no flag | the cell the run is about to write still fails under a ready pull request on a re-seal, which is the ordinary post-review path | rejected — the excuse is about the cell, not the state |
| J5: leave the walks as two implementations with the equivalence argued in a docstring | that is today, and the inventory's row 71 is the finding | rejected |
| J5: `field` refuses a duplicated row by raising | every caller of `field` in `chain_check.py` would need a handler; an error reported once from `check_round` with `field` answering None is the shape `pass_checked` already uses for an absent box | chosen |

## Phases

Vertical slices — each phase ends with something runnable and verified. The
status column is empty or the commit that closed the phase.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | J1. `broad_gate.py#rounds_rows` reads `Needs a fix` through `chain.says_reopened`; True → ` · capped`, False → not capped, None → `<R>` alone. `agents/sealer.md`'s `rounds` row sentence (:123) by replacement. The `Re-read ·` rows for `rounds_rows` | S1's cases red with `startswith` restored, then green; `tests/test_the_seal_is_taken_once_by_the_sealer.py` module green | d9c71475 |
| 2 | J2. deferred_home and issue_of in `chain_check.py`; `rounds_rows`, `release_seal.py#chain_counts` and `round_record.py#fix_table` read through them; `HOME_TOKEN`, `HOME_END`, the panel's `deferred_home`, the `findall` and the fix table's own prefix test leave. `docs/review-chain-spec.md`'s paragraph *The vocabulary the exit needs*, one sentence by replacement. The fourteen prose cases replaced by S2's | S2, S3, S4 red first; `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_release_seal_is_drawn.py`, `tests/test_the_fixes_close_the_record.py`, `tests/test_chain_check_at_the_pull_request.py` green | 984e45c8 |
| 3 | J3. `depth_two` reads through `path_forms`; location_units and its five patterns leave; `depth_two`'s docstring and `docs/round-record-spec.md` §*The depth in `New units`* by replacement; the `tests/test_a_fix_of_a_fix_is_counted.py:176` docstring | S5's bare-name case red against today's `depth_two`; S6; `tests/test_the_fixes_close_the_record.py` and `tests/test_a_fix_of_a_fix_is_counted.py` green | |
| 4 | J4. `pull_request_state` gains the `gh` source and prints it; `--sealing` on `chain_check.main`, reaching the `broad_gate` arm of the last record; `run_check`'s payload and pull_request_is_ready leave `round_record.py`; draft_env leaves `broad_gate.py` and the chain arm passes the flag. `docs/round-record-spec.md` §*`Pass` has to be checked* third row and its paragraph by replacement, the flag named there | S7, S8, S9 red first; the environment-leak case re-pinned; `tests/test_chain_check_at_the_pull_request.py`, `tests/test_the_record_is_generated.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_local_mode_reaches_the_review_chain.py` green | |
| 5 | J5, the walks and the cut. record_facts, floor_walks and cut_runs in `chain_check.py`; `stopping_floor`, `runs_of`, `floor_and_fixes` and `current_run` call them and keep their names and signatures; the two loops in `stopping_floor`, the `seen` walk and the loop in `current_run` leave | S10 red with either old loop restored; `tests/test_the_reopening_is_one.py`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`, `tests/test_a_fix_of_a_fix_is_counted.py`, `tests/test_the_record_is_generated.py` green | |
| 6 | J5, the rest. gate_before_review for the `broad_gate` arm and `seal`; close_prefixes for `doubled_grounds` and `close`; fields and pass_boxes under `field`, `pass_checked`, `field_index`, `close` and `seal`, and the duplicate error in `check_round`. `docs/round-record-spec.md`: the duplicate row and box, one table row each by replacement of the sentence that says the first wins where one does | S11, S12 red first; `tests/test_chain_check_at_the_pull_request.py`, `tests/test_the_fixes_close_the_record.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py` green | |
| 7 | The closing: `docs/round-record-spec.md`'s opening sentence on the one reader; the input-class table from `spec.md` §*Data & interfaces* checked against what was built; `changelog.md` from the seven phases; the ledger fragment's rows for the new units and the last `--reverify --into`; `overview.md` | S13, S14; `fold-check`, `evidence-check` and the five text-hygiene modules the brief names, run narrow; the broad gate is the sealer's | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. What a phase discovers while
it is being built, and needs the next phase to know, goes to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes. **Re-read the Status column after any rebase**: a
squash or a rebase orphans the commits it names, quietly.

### Why this order

Phases 1–3 touch one function each in one script and no walk; they land
whatever the siblings do. Phase 4 is the one with a flag and a document table,
so it comes after the three that can be reverted alone. Phases 5 and 6 change
the most lines of `chain_check.py` and `round_record.py` and are the ones a
sibling's squash can conflict with textually, so they come last and are
merged after the siblings where the release branch allows it (§*Seams*).

### Seams with the siblings

| Sibling | Units it touches | This work's nearest unit | What to do at the merge |
|---|---|---|---|
| #837 (⬜ closes once) | `round_record.py#close` and `#new` (what a ⬜ commissions), `chain_check.py` (a records-level finding's verdict), `skills/code-review/orchestration.md` | `close`'s doubled-grounds guard and `Pass` box count (phase 6), `fix_table`'s deferred arm (phase 2). No verdict word or severity rule is touched here | textual; take both. If #837 changes which rows `close` demands a fix-table row for, phase 2's S4 fixture is written with a 🟡 row so it is unaffected |
| #860 (a fix range across a merge) | `round_record.py#touched`, `chain_check.py#walk_tip`, `#commits_after` | none — `landings` reads the range's ends through `chain.resolves_to` and is not changed; `depth_two` reads `added` from `measure`, which #860 may feed differently | no shared unit; same files. Merge in either order |
| #869 (the gate reads its counts from the recorder) | `broad_gate.py#suite_counts`, the recorder, the panel's `suite` row | `rounds_rows` (phase 1), the chain arm's call at :3441 (phase 4), the removed `deferred_home` (phase 2) | distinct functions in one file; textual conflicts at most. The rejected alternative *drop the pre-seal chain arm* is theirs to take or leave |
| #835 (a reader declares its input class) | a registry and its test; `docs/` home | every function `spec.md` §*Data & interfaces* adds, with its class | phase 7 checks the table against #835's registry shape if it has landed; otherwise the table is what #835 reads |

## Operational impact

- **No migration, no new dependency, no new environment variable.** `gh` was
  already invoked by the generator; it is now invoked by the check, once per
  run, only where no payload exists.
- **One compatibility change a person meets.** On a machine with no
  pull-request payload and no `gh` that can answer, `round-record new`,
  `close` and `seal` exit 1 on the record they just wrote, with the state line
  saying so; the record is written. The orchestrator's environment has `gh`
  by construction (it opens the pull request); a consuming repository without
  it meets the policy table's third row where it used to meet a silent draft.
- **One new flag**, `chain_check --sealing`, used by the broad gate's chain
  arm and printed in the state line. CI passes no flag.
- **Fewer panel and release-seal claims**: a prose home prints as prose and
  names no issue; a bare `yes` draws no `capped`.
- **Bookkeeping.** 172 released ledger rows drift (`spec.md` §*Data &
  interfaces*), 111 of them on three units — `broad_gate.py#gate`,
  `chain_check.py#main`, `round_record.py#close` — that the sibling frames
  edit in the same release. Each phase writes its `Re-read ·` rows into this
  work item's fragment with the claim corrected where the edit made it
  false. Two documents are at the ceiling; every edit is a replacement,
  measured.

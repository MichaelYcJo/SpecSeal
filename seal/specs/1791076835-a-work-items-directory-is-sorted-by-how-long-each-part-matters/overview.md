# 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show, each part written when it happened. -->

📋 implement applied
· spec:     spec.md §Grounding, §The readers, D1–D6, S1–S11; plan.md's phases and its fallback cut; questions.md Q1–Q6
· evidence: seal/ledger/1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters.md
· verified: each phase record carries its runs, labelled executed or read

## Why this work exists

Two thirds of `seal/specs/` was the process record of released work items, read by nothing and waiting on a fold that had not run since 2026-09-24. `settle --retire-process` now removes it at every release, and `routing.md` and the SDD set stay for the fold.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether the survivor sweep already accepts a drop | §Grounding: the sweep "already names the class this work removes … so a range that deletes those files reports nothing from them" / the real drop's range reported 34 places from two `handoff.md` and one `broad-gate.md` | a fix in the sweep: a pull-request file removed whole leaves the range, after the pairing | plan.md phase 2: "Any reader that refuses is fixed here". The first real drop is a pull request into a release branch, where `hygiene.yml` runs the sweep (phase 2, executed) |
| What the agreement case pins | plan.md phase 2: the leave-list and `records_a_past_state` "agree on `rounds/`, `phases/` and `survivors.md`" / the sweep now holds the rest of the list too | every entry of the list, durable files included | a second list in the sweep that only three entries are held to can grow alone |
| How `anchored_rows` and `citations` are reused | spec §Data & interfaces: the arm "reuses … `anchored_rows` and `citations`; it does not re-derive any of them" / both answer the fold's question, the whole directory | reused, then narrowed: `process_anchored` filters `anchored_rows`' result, and `citations` gained an `inside` parameter | an anchor or citation into `spec.md` keeps resolving after this arm, so holding or listing it would be false (phase 1) |
| How many items the first run takes | spec: "the first run takes all 55" / 54 hold a process record | 54, as measured | 1788177600 holds only `routing.md` and `overview.md`; the arm takes nothing from it, and naming it would claim a removal that does not happen |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck over the whole repository | the sealer, once the review rounds settle |
| The first real `settle --retire-process` run, at 0.18.1's step 2b or later, on its own `[no-review]` pull request, including the survivor sweep at that pull request | the orchestrator, at the release that runs it |
| `evidence-check --strict .` exits 2 on one drifted row, `tests/test_a_record_precedes_the_fixes_it_commissions.py#test_the_declared_limit_names_what_escapes_with_the_words_unchanged`, which drifts at e141980a too | the orchestrator, when the release branch is merged in, or that row's owner |

## Not done

The first run over the 55 released items, by spec D5 and Q3: it is its own pull request at a release's step 2b.

The opening sentence of `docs/the-record-layout.md` §*What is decided and not built yet*, *F1 is built; the other three are not yet.*, is stale now that F3 is built. This branch was told to edit only the F3 paragraph and the line under the table, and #728 and #730 build F2 and F4 in the same release, so correcting it belongs to whichever of the three lands last.

The cheat sheets in `README.md` and `README.ko.md` name `settle [--retire]` and not the new flag. They are not among spec D6's carriers, and `tests/test_settle_reads_before_it_removes.py#test_both_cheat_sheets_carry_the_command` pins their present row.

`REMOVED_SAYS` and `RELEASED_SAYS`, which the arm prints beside an anchored row, speak of "a directory a retirement removes" and "the fold's own fragment". The action they prescribe is the same for this arm, and rewording them would move `--retire`'s pinned output.

## Fed back into the spec

- *Inferred during implementation:* the survivor sweep leaves a `broad-gate.md`, `handoff.md`, `pr.*.md`, `tests-todo.md` or `evidence-todo.md` that a range removed whole out of that range, and keeps a standing one in its pool. Recorded in `skills/code-review/scripts/survivor_check.py`'s module docstring, §*A process record removed whole is out of the range too*.

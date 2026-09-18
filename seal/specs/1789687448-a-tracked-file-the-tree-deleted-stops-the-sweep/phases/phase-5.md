# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | filled by the commit that closes this phase |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

The documents and the records: one sentence in `docs/release-checklist.md`
step 3's preamble, `changelog.md`,
`seal/ledger/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep.md`,
the re-stamp of the three drifted shared rows, and `overview.md`. Verified by
`evidence_check.py --strict .` before and after the re-stamp with the exit
read directly, and by reading `docs/release-checklist.md` for the
version-naming rule.

## What this phase found

**Nine rows drifted, not three, and all nine claims still hold.** The frame
read the ledger for the units it expected to touch. Two things widened it:
phase 4 guarded a sixth helper the frame's enumeration could not see, and
phases 2 and 3 moved four `test_` functions into root-parameterised bodies,
which changed units the frame did not list. Each was re-read before
`--reverify` was allowed to write:

| Anchor | What the claim says, and why it still holds |
|---|---|
| `test_no_document_names_the_old_roots.py#test_no_shipped_document_names_the_old_roots` | S15, no document names the old roots. The body now calls `offenders_under()`; the rule and the refusal are unchanged |
| `test_no_document_names_the_old_roots.py#test_every_keep_entry_is_still_in_use` | a reason no line carries fails too. Still red on a whole tree; on a shrunken one it declines instead of reporting a live entry dead, which is the claim kept rather than weakened |
| `test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | the below/at-or-above rule and its three exemptions. The body calls `timer_offenders()`; `timers_in` is untouched |
| `test_a_script_says_which_interpreter_it_needs.py#shipped_python` | every shipped `.py` is re-enumerated. It returns the `on_disk` pair now; the corpus rule is the same |
| `test_a_script_says_which_interpreter_it_needs.py#test_no_shipped_script_needs_more_than_the_floor_without_saying_so` | an unclassified file above the floor is refused. The `new` half is untouched; the `gone` half moved into `classifications_of_nothing` |
| `test_a_release_is_sized_by_a_criterion.py#test_one_document_states_a_releases_size` | one document states a release's size. The body calls `restatements()`; `hits` and `STATES_A_SIZE` are untouched |
| `test_a_finding_id_is_a_bare_integer.py#committed_records` | every reader of the round records lists from HEAD, never from the index. Unchanged — this work added the disk guard and did not touch the listing source |
| `test_a_finding_id_is_a_bare_integer.py#test_an_uncommitted_record_is_not_in_the_committed_corpus` | the case pinning that listing. It unpacks the pair now |
| `test_a_finding_id_is_a_bare_integer.py#test_the_committed_records_only_lose_a_miscount` | no record the old rule reads correctly is refused by the new one. An invariant over a population, unaffected by a corpus one file shorter |

Those nine anchors sit in **eight** rows of `seal/ledger.md`, and each row's
`Date` moved to 2026-09-18 — the column holds the date somebody read the code,
and the precedent is the same act at `5bf22ddb`.

**The records arm asked for a tenth correction the plan did not name.**
`evidence_check.py --strict .` stayed at exit 2 after the ledger was clean,
because `spec.md`'s *Ledger rows this work drifts* table quotes three
coordinates with their pre-work hashes and the records arm resolves a stamp in
a live work item exactly as a ledger row's. A stamp naming a row that no
longer exists names nothing, so the three were re-stamped and the table gained
a sentence saying the count was nine.

**Q1 of the checklist sentence: the fold's own tree produces no skipped case.**
`spec.md` asked for a sentence saying *a non-zero skip count is the expected
reading*. Phase 3 measured that a fold alone leaves its missing paths under
`seal/ledger/`, which no declining check reads, so the sentence is written to
the measurement: the sweeps judge what remains, a skipped case with reasons
naming paths is that state rather than something to debug, and it appears when
the tree is also mid-edit under `docs/`, `skills/`, `templates/` or a shipped
`.py`. The sentence names no version, which
`test_no_loaded_file_names_a_version_at_or_above_the_running_one` scans for,
and it stays inside 88 columns.

**Verification, exit codes read from `$?`.**

| Command | Before | After |
|---|---|---|
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 2 — 1320 ok · 9 drifted in `seal/ledger.md` | exit 0 — **1353 ok · 0 drifted · 0 broken**, records arm 2 work items read · 3 stamps read · 0 drifted |
| `python3 skills/evidence-check/scripts/evidence_check.py --reverify .` | — | exit 0, **24 rows re-verified** |
| `uvx ruff check .` · `uvx ruff format --check .` | — | exit 0, exit 0 |
| `bin/test -q` over the 22 modules these files touch | — | exit 0, **726 passed** |
| `python3 .github/scripts/gather_changelog.py --check` · `fold_ledger.py --check` | — | exit 1 each, naming the two ungathered fragments — the expected state on a feature branch, and what the release preparation folds |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase only adds documents and records | none |

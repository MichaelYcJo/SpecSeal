# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — phase 4

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-4.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 759af110 |
| Ran by | smith on Fable 5.1 |

## What this phase was asked

The records: re-read then `bin/evidence-check --reverify .` over the drifted
`seal/ledger.md` rows `spec.md` §*Data & interfaces* names; the ledger
fragment `seal/ledger/<work-item-id>.md` with new rows anchored on the
phase 1–3 units; `seal/specs/<id>/changelog.md`; `overview.md` with its
`## Not verified` table and Q3's count; the branch's own sweep and
`survivors.md` for the docstring sentences this branch rewrites that ledger
rows quote; `bin/evidence-check --strict .` exit 0;
`bin/unverified-check --baseline origin/release/v0.15.1 seal/specs/` exit 0.

## What this phase found

**What drifted was narrower than the frame's table.** `bin/evidence-check
--strict .` at `c44bcf61` named three drifted anchors — `corrected`,
`corpus` and `whole_range` — cited by nine `seal/ledger.md` rows: S3 and S6
of `1788873640`, G5 and G6 of `1788912166`, S1 of `1789211172`, the
12,100-survivors row of `1790076070`, G5 of `1790138190`, E1 and E4 of
`1790174139`. The docstring-heading anchor
(`#"## What is excluded, by construction rather than by list"`) that S3 of
`1789211172` and E2, E5 of `1790174139` sit on did **not** drift when a
paragraph was added under it, and `records_a_past_state` and `report` were
not edited, so those rows stand as they were. Each of the nine was re-read
against the new code and takes a dated `Re-read 2026-09-24 by work item
1790206435` note saying what moved and why the claim holds; then
`--reverify` re-stamped 45 rows (the nine, and the fragment's own
placeholders). `--strict .` then exits 0: 1695 ok, 0 drifted, 0 broken.

**A ledger row may not spell a sweep coordinate as `path:line`.** The
fragment's first draft quoted five of them in prose (`seal/ledger.md:2053`
and the like) and `--strict` reported each as an `OLD-FORMAT` coordinate to
migrate. They are spelled as *the sweep's `seal/ledger.md` place at its
line 2053* now. Nothing in `templates/ledger.md` says so; the checker does.

**No `survivors.md` for this branch.** The sweep over
`origin/release/v0.15.1...HEAD` with every `seal/specs/*/survivors.md`, at
`759af110`: exit 0, `examined 386 files`, `against 14 sentence(s)`, zero
places, zero `unresolved` and zero `not yours` lines. The docstring
sentences this branch rewrote (`sentences`' one-line docstring, the
`whole_range` paragraph) are quoted by no ledger row closely enough to
clear the floor, so the file the plan reserved for them is not written —
an exemption file with nothing to excuse would be refused as empty.

**Q3's count is in `overview.md` §*Not done*:** 17 code-idiom and 3
released-changelog rows of the 56 path rows across seven files, none
edited.

**Executed at `759af110`**, all exit 0 unless stated:
`bin/evidence-check --reverify .` (45 rows), `bin/evidence-check --strict .`,
`bin/unverified-check --baseline origin/release/v0.15.1 seal/specs/`
(15 overviews, 33 open, 4 closed, 0 unreadable — this item's three rows
open by design), the branch sweep above, and the other modules that read
`survivor_check.py` or the records this branch writes —
`test_the_contributor_has_a_procedure.py`,
`test_the_gate_asks_the_range_ci_will_ask.py`,
`test_unverified_rows_close.py`, `test_a_phase_hands_the_next_one_a_record.py`,
`test_a_record_says_what_ran_it.py`,
`test_a_segments_record_says_what_it_was_asked.py`,
`test_the_ledger_fragments_fold_at_release.py`,
`test_the_implementer_is_recorded.py`, `test_routing_is_recorded.py`,
`test_a_record_states_what_the_tree_has.py` — 443 passed in one run at
`c44bcf61` with the records in the working tree, and the record readers
again after this file was written.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

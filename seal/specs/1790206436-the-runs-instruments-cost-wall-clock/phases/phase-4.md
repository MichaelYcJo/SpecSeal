# 1790206436-the-runs-instruments-cost-wall-clock — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 4bc6778c |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

The records: re-read then `bin/evidence-check --reverify .` over the drifted
rows `spec.md` §*Data & interfaces* names, the ledger fragment
`seal/ledger/<work-item-id>.md` with its new rows, the changelog fragment
with the before-and-after wall-clock figures, `overview.md` with its
`## Not verified` table, `questions.md` M1/M2/W1/W2 filled from what was
measured, the branch's own sweep `bin/survivor-check --range
origin/release/v0.15.1...HEAD` with a `survivors.md` only if it reports rows
this branch should excuse, and `bin/unverified-check --baseline
origin/release/v0.15.1 seal/specs/` exit 0.

## What this phase found

**Twelve anchors drifted, not five, and every claim on them stands.**
`evidence-check --strict` at `8a234674` reported 12 DRIFTED units across 18
rows: the five the frame named (`run_tests.py#build`, `#main`,
`broad_gate.py#panel`, `agents/warden.md#"## Where you work"`,
`agents/sealer.md#"## The command"`), and seven it did not — `broad_gate.py#gate`
(the one-argument change `phases/phase-2.md` records), `bin/test`'s
*Typed as* comment block (its unit is lines 1–35, so the reworded last
paragraph moved it), `CONTRIBUTING.md#"## Running the checks"`,
`docs/release-checklist.md` §3, and three test functions whose docstrings or
failure message lost *five-minute* (`test_the_protocol_hands_over_the_narrow_form`,
`test_the_cheat_sheet_does_not_offer_the_runner`,
`test_the_section_says_the_full_run_is_the_sealers`). Each row's claim was
read against the unit as it stands now, in `seal/ledger.md` sections
`1788632199`, `1788844127`, `1789002694`, `1789445605`, `1789687448`,
`1789956662` and `1789985781`; none is about the part that changed.
`--reverify` rewrote the 22 hashes (`22 rows re-verified`), and each of the
18 rows took `2026-09-24` in its `Checked` cell and a
`**Re-read 2026-09-24 in work item 1790206436 (#337 · #475 · #544).**` note
naming what moved in the unit and why the claim holds — the shape the
`Re-read <date>` marker `correction-check` reads.

**The fragment's hashes were written by the checker, not by hand.** Seven
rows were written with `@00000000` in every anchor and `--reverify` rewrote
41 hashes to what each unit holds (`41 rows re-verified`); `--strict` then
read `1702 ok · 0 drifted · 0 broken`.

**The records arm reads this work item once the fragment exists**, and it
found two things. `phases/phase-1.md` named `pytest_cmdline_main`, an xdist
function the tree does not carry, so that line took the `NAME NOT IN TREE`
marker. `overview.md`'s divergence row quoted the R6 anchor with an ellipsis
inside the locator, which the arm read as a stamp and reported BROKEN
(`locator not found`); the row now names the anchor in prose. After both,
`--strict` is exit 0 with `73 names read · 0 refused`, and
`tests/test_a_record_states_what_the_tree_has.py`'s real-corpus case, which
had failed on the same quote, passes. The frame's own markers came off the
seven lines whose names the work created (`has_xdist`, `shipped_gate`, the
inverted pin, the new module); the two on `with_xdist` — the frame's NAME NOT IN TREE
placeholder for a name the phase chose differently — and on the
`pytest_xdist-3.8.0.dist-info` directory entry stay, because neither is in
the tree.

**The sweep reports nothing to excuse.** `survivor-check --range
origin/release/v0.15.1...HEAD` at `8a234674`: 398 files examined against 29
sentences the range removed, `no removed wording is still standing`, exit 0.
So no `survivors.md` is written — the plan's *if the sweep reports the
reworded cost sentences standing in `CHANGELOG.md` or the ledger* did not
come to pass. The one standing carrier of the serial figure is the clause
cell of `seal/ledger.md`'s R6 row (*five-minute suite*), which the sweep
does not read as a removed sentence and which `overview.md` §*Not done*
leaves as a record's wording.

**`unverified-check --baseline origin/release/v0.15.1 seal/specs/`** is exit
0: 15 overviews, 33 open, 4 closed, 0 unreadable, this item's three rows
among the open.

**The 57 modules that read the real seal corpus** ran as one batch after the
overview was written: `1 failed, 2938 passed, 1 skipped in 152.82s`, the one
failure being the BROKEN quote above; the two modules concerned re-ran green
after the fix (`117 passed`). The overview case of
`tests/test_chain_hooks_hardening.py` that phase 3 left red is among them.

**M1 stays half-answered by design.** The suite's own wall clock under
`-n auto` on this branch is the sealer's reading, and the spawn prompt keeps
the whole suite off this segment; `questions.md` M1 says which reading is
taken and which is the orchestrator's to read off the sealer's report.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| seven `NAME NOT IN TREE` markers from `spec.md` and `plan.md`, on lines naming units the work created | none — the names are in the tree and the records arm reads them there |

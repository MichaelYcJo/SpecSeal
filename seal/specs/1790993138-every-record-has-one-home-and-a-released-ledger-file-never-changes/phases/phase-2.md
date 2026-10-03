# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | b6f1c578 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`--reverify --into <fragment> --checked <date>` (D4); the refusals under
`Ledger frozen from`; the row added to `seal/config.md` and documented in
`templates/config.md`; `hooks/evidence-advisor.py`'s repair text; and this
branch's own drifted rows re-read into
`seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md`
with the new tool, each row read first. Scenarios S5 and S15, the phase-1
module extended for S5 with sha256 equality of every released file,
`tests/test_dispatch.py` and `tests/test_gates_do_not_fail_open.py` run for
the advisor, and `evidence-check --strict .` read directly.

## What this phase found

**The frame holds for this phase, with one gap.** `#reverify` is untouched
and runs over the files the freeze leaves writable; the new writer sits
beside it, as `plan.md` says. The gap: a released row whose anchor MOVED
(BROKEN, with a destination the scan can prove) cannot be cleared by a
`Re-read ·` row, because the family union is keyed on the coordinate and the
old and new spellings differ. `--into` names such a row and its repair, a
`Corrected ·` row, and writes nothing for it. In `overview.md` under the
divergences.

**How a run is ordered.** Without `--into` and without the row, `--reverify`
is what it was. Otherwise the fragments are re-stamped in place first, then
the view is read again, so a fragment's own re-read is counted before a row
is written for its family; then `reverify_into` writes one `Re-read ·` row
per released row a re-read owes (`released_drift`): a row outside every
family with a drifted coordinate, or the root of a family where no reading
holds a coordinate's current content. The row cites the root, so it joins
the family. Any value of the row freezes `--reverify`; the cutoff matters
only to `correction-check` (phase 3).

**W1's other half, decided: the first cell is `Re-read · ` and the cited
row's first cell as the naming block prints it** (72 characters, `…` past
that), pipes escaped. The Notes cell is `Re-read <date> by work item <id>
(`evidence-check --reverify --into`)`, the id taken from the fragment's file
name, because the spec's example names the work item and a fragment is named
for one.

**Where the row is read.** The plugin's copy reads `seal/config.md` through
`hooks/config.py#config_rows`, loaded by path; a vendored copy, alone in a
repository's `tools/`, reads it with `vendored_config_rows`, the same table
shape without the fence walk. The phase-2 run of the 44 modules found that
reader splitting lines with `.splitlines()`, which
`tests/test_every_reader_ends_a_line_where_gfm_does.py` refuses for a
markdown reader; it reads `gfm_lines` now.

**S15: no case held the config rows to the template, so one is planted.**
`test_every_row_this_repository_declares_is_documented_in_the_template`
holds every row of this repository's `seal/config.md` — six now — to a
`` `Item` `` or `## Item` in `templates/config.md`, and the new row's value.
Searched first: the thirteen test modules naming `templates/config.md`, by
name and by content; none reads every row.

**M3 for phase 2 (executed): 22 released rows drifted**, the 16 coordinate
findings of phase 1 plus `main` of both scripts, `#check_ledger` again, and
`templates/config.md#"# Repository config"` from the new section. A frozen
`--reverify .` on this tree wrote nothing, exited 1 and named all 22. Each
row was read against this branch's edits before writing (the list and the
judgement are in the session: every claim holds), then
`--reverify --into seal/ledger/1790993138-….md --checked 2026-10-03 .` wrote
22 rows, exit 0, `git status` showing only the new fragment. Six of them —
H1 of 0.16.0, four rows of 0.4.0 and R2 of 0.9.0 — describe the anchor
reading that moved into `classify`, so `classify` was added to their grounds
at its current hash and their Verified behavior says so. `--strict .` then:
`3653 ok · 0 drifted · 0 broken`, exit 0.

**Seen red (§15).** Before any code: 7 failed, 23 passed. The two that
passed were `--into` without `--checked` (argparse refused an unknown
`--into` with exit 2) and the no-row case (the old behaviour). Both went red
under breaks of their units. Every unit this phase added was broken with
`mutation-check`, 21 breaks; two survived their first run — the
`--into`-needs-`--reverify` guard, which had no case of its own (now
`test_into_without_reverify_says_which_command_it_belongs_to`), and the
unfrozen branch, run first against the unfrozen case — and both went red
after.

**Narrow runs (executed).** The phase module: 33 passed. The 44 modules that
name `evidence_check`, `evidence-advisor`, `templates/config.md` or
`seal/config.md`, plus `tests/test_dispatch.py` and
`tests/test_gates_do_not_fail_open.py`: 2,666 passed, 7 skipped, 1 failed
(the `.splitlines()` pin above), which passes after the repair (153 passed
in its module).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

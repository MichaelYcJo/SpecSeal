# 1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 1752792c |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 3: this item's ledger fragment, `overview.md` and
`changelog.md`. The orchestrator added: Q1 answered with its default (a) and
recorded in `questions.md`, the build touching no `changelog/`; any released
row whose anchor drifted re-read and written with `evidence-check --reverify
--into seal/ledger/<id>.md --checked 2026-10-05`; and the `changelog.md`
describing what ships at the head, since the new arm reads it.

## What this phase found

**21 released rows cited anchors this branch moved**, 24 drifted anchors in
all: `agents/smith.md`'s `## Phases` (12), `chain_check.py#main` (6),
`RULES` (3), the orchestration file's fix-pass section and the file itself
(one each), and `docs/the-record-layout.md`'s `## docs/` (one). Each claim was read against the edit
and holds: every edit here adds a sentence, a call or a row and changes none of
what those rows state. `--reverify --into` wrote 21 `Re-read ·` rows; each row's
note was then extended with what the branch changed at its anchor, by a script
asserting every match. No released file changed.

**The fragment's own four rows** were written with placeholder hashes and
stamped by `evidence-check --reverify --checked 2026-10-05 --ledger <fragment>`.

**The `changelog.md` fragment was written after the arm, and the arm reads
it.** It changed last at `1752792c`, after every behaviour commit of the
build, so the arm, run on this branch after round 1, names nothing until a fix
changes a behaviour path without it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

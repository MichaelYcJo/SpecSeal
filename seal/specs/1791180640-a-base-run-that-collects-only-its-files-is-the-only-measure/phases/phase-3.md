# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8cf7c855 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 3 and `spec.md` Scope 10: the ledger fragment
`seal/ledger/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure.md`
with new rows for what phases 1 and 2 built; `Corrected ·` rows for every
released row this work makes false, at least `seal/releases/0.18.2.md` D1,
D2, `Corrected · B3` and `Corrected · S5`, and `seal/releases/0.18.1.md` B4;
`Re-read ·` rows for the rest, written by `evidence-check --reverify --into
seal/ledger/<id>.md --checked 2026-10-05`; and the work item's
`changelog.md` fragment, saying what ships at the head, what becomes
stricter included. Identifiers not in the tree stay out of backticks in the
records. `evidence-check --strict .` must report 0 drifted, and
`survivor-check` runs over the range from a3aa139a.

## What this phase found

**Five new rows and five corrections.** R1 is the report and its reader, R2
the proof pass and its reader, R3 the groups and the run of a file alone, R4
the documents, R5 the corpus. The corrections are 0.18.2's D1, D2,
`Corrected · B3` and `Corrected · S5`, each cited by its own line, and
0.18.1's B4, whose "the two reasons are pinned whole" is now four. The
first build corrected the same five; this fragment says what holds at this
head instead of what that build shipped.

**The `--into` writer re-read 16 released rows**, from 0.5.0 to 0.18.1.
Each cites the `Broad gate` section of `templates/config.md`, the broad-gate
section of `skills/verify/SKILL.md`, `row_prefixes`, or
`VERSIONS_OF_ANOTHER_PRODUCT`, and each was read against what it claims: a
missing row is a refusal, the trailing `&`, the pipe, `cmd.exe`'s command
names, the fence and comment rules, the preflight, the panel's CI row, the
version table's git rows, and the cut. None of them is about the base
comparison's words, and every one holds, so none became a correction.

**The records arm refused two lines of `spec.md`** for naming
test_the_one_counterfeit_the_gate_cannot_see_is_named, which phase 1
removed. Each carries the checker's ` · NAME NOT IN TREE` marker now, and
no word of the frame changed; that marker is the only thing written into
the framer's file. With it `evidence-check --strict .` exits 0: 5653 ok, 0
drifted, 0 broken, and the records arm 0 refused.

**`survivor-check` over a3aa139a..HEAD.** One place it reported was live
and is corrected: the section comment over #747's cases in
`tests/test_the_seal_is_taken_once_by_the_sealer.py` still said each prefix
is tried until one prints pytest's summary. The 40 that stand are rows of
`survivors.md`, each with a quote and its grounds: rows of the released
0.18.1 and 0.18.2 ledgers this fragment corrects, the shipped records of
#747 and #761, two test comments and a docstring that state facts about
pytest or the history of a case and still hold, and `COUNTS_RE`, which
shares regex tokens with the removed summary reader. Per-place rows, not one
range row, because this range edits code as well as records.

**The changelog fragment says what ships at the head.** It is under `Fixed`
for the permissive word no longer given to a file the base passes, and
under `Changed` for what becomes stricter: the rows that now read `new?`
and how a row earns the word back, a part that drops the arguments, the
reasons, and the proof run's cost. It names #789, #812 and #807.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

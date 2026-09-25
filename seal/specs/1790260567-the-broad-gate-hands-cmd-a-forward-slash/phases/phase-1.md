# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b75b05ad |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#448, the rewrite. A pure function, `handed_to_shell(command, windows=None,
comspec=None)`, turns `/` into `\` inside the command words of a string
handed to `cmd.exe`, and only there. `run` applies it when `shell=True`,
keeps the row as written and the handed line in `<name>.txt`, and prints one
stderr line when the two differ. `gate`, `compare_at_base`, `first_command`
and `quote` stay unedited. `templates/config.md` §*Broad gate* gains one
paragraph, the drifted rows citing it are re-read and re-stamped where they
live, and the fragment rows for A1–A4 are written.

The phase was built by two sessions. The first wrote `5c161ddd` and
`160324ae` and died at about 23:57 with one change uncommitted in
`broad_gate.py`. The second was asked to read that change, keep or discard
it against this phase's intent, run the Verified-by checks and close the
phase.

## What this phase found

- **The uncommitted change was half kept.** It carried two edits in the
  spirit of `160324ae`, removing scan branches that change no output. The
  first read `&&` and `||` as two separators in a row instead of stepping
  over both characters at once. That changes no output for any string, and
  it was kept. The second dropped the `^` branch's move out of command
  position. That does change output: under it, `^a b/c` was handed as
  `^a b\c`, rewriting an argument. It was put back, with a case that pins
  it, seen red against the dropped branch (`af001546`).
- **One scan branch had no case behind it.** Mutating the redirection arm so
  that it left command position open stayed green across the whole module,
  37 passed. The strings that tell it apart put a blank between the `>` and
  its target, so `> out/log.txt bin/test` now pins it (`2498f139`). After
  that, every one of fourteen mutations across `handed_to_shell`,
  `command_names_backslashed`, `run` and `handed_line` turned the module red.
  The mutations were run from a script that restored the file from the bytes
  it read, clearing `tests/__pycache__` between them.
- **§14 reached the template as well as the stderr line.** The template's
  new paragraph had no case. `test_the_template_says_which_positions_are_rewritten`
  now pins what it says is rewritten and the two positions that are not. It
  was seen red with the `call`/`start`/`if` sentence cut.
- **Three ledger anchors drifted, not two.** The plan names
  `seal/releases/0.10.0.md` S4 and one row of `0.12.0.md`. The check found
  three rows in `0.12.0.md` on the same anchor, and a fifth row,
  `seal/releases/0.5.0.md` S8, anchored on the whole file
  (`templates/config.md#"# Repository config"`). Each was re-read against the
  new paragraph, and each claim holds. Each carries a dated `Re-read` note and
  a new `Checked` date.
- **The records check reads this work item once a fragment exists.** With
  the fragment written, `evidence-check` began reading this directory. It
  refused `spec.md`'s coordinate for `gate`, which spelled the path from
  the file name alone, and that is corrected to the full path in `spec.md`
  §*Data & interfaces*. The anchor's hash is unchanged, and `gate` was not
  edited. It also refuses, as not in the tree, three of the four token
  variables `spec.md` Scope 3 names and the host variable `questions.md`
  Q2 holds as a fallback. Phase 3 writes the tokens into
  `tests/conftest.py`, and settles the fallback.
- **Verified by (executed, 2026-09-25):** `bin/test
  tests/test_the_gate_hands_cmd_a_path_it_can_run.py
  tests/test_the_seal_is_taken_once_by_the_sealer.py
  tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py -q`.
  191 passed at `af001546`. At the phase boundary, those three and the 23
  modules that read `templates/config.md` or a ledger file ran together:
  1487 passed, 7 skipped, and 1 failed,
  `test_unverified_rows_close.py::test_this_repositorys_own_overviews_are_all_readable`,
  because no `overview.md` stood under `seal/specs/` at all. Opening this
  work item's `overview.md` turned it green (178 passed with
  `test_docs_line_wrap.py`). A4's `cmd.exe` half is
  `unverified — CI windows leg`, and `questions.md` Q1 stays open for it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

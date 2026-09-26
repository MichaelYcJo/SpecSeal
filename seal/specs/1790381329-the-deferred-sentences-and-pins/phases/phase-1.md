# 1790381329-the-deferred-sentences-and-pins — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 31ccd45d |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#610. `seal.py` checks for `hooks/config.py` and `hooks/optin.py` before its
`import` lines and exits 2 with one sentence per missing file, naming the
path and its purpose. `payload_meter.py#_session_cost` checks for
`session_cost.py` and exits 2 the same way, matching the file's floor
refusal. `seal.py`'s exit-code line and `payload_meter.py`'s docstring name
the new code. Two `CASES` rows in `tests/test_a_script_copied_alone_exits_2.py`,
each seen red first; the module docstring and the `CASES` comment say six
scripts and both loader shapes.

## What this phase found

- **The frame holds.** The class under `skills/` was re-enumerated at the
  build tip by construction: every `spec_from_file_location`,
  `sys.path.insert`/`append`, `import_module` and `runpy` in
  `skills/*/scripts/*.py`, and every bare `import` or `from` of a module
  named like a file in `skills/*/scripts/` or `hooks/`. The only bare imports
  are `seal.py`'s two; every other by-path loader already refuses at 2
  (`fold_check.py`, `settle.py`, `round_record.py`, `chain_check.py`,
  `broad_gate.py`, `survivor_check.py` ×3) or falls back by design
  (`evidence_check.py` ×2, work item B's file). So the class is exactly
  the issue's two scripts.
- **The `seal.py` check is a function, `refuse_without_hooks`, called at
  module level before `sys.path.insert`.** A module-level `if` block is not
  a unit `evidence-check` can anchor, and the ledger row needs one. The
  `import` lines now carry `# noqa: E402`: ruff exempts a `sys.path.insert`
  before imports, but not a call.
- **Q4, answered on a different invocation than the default.** `measure`
  calls `calibration_of` before `agents_in`, and `calibration_of` calls
  `_session_cost()` on its second line, before `spawns_in` opens the
  transcript. So the transcript need not exist, and the row passes
  `--calibrate {root}/main.jsonl`, a path in the empty repository. The
  default's *existing empty file* would have meant editing
  `test_a_script_copied_alone_exits_2_and_names_what_it_misses`, which a
  0.15.4 ledger row (M1) anchors, for a file the loader never reads. If a
  later edit moves the load after the open, the row goes red rather than
  passing for the wrong reason.
- **Seen red (§15).** Both new rows against the code at `09034979`: 2 failed,
  5 passed — `seal.py` exit 1 with `ModuleNotFoundError: No module named
  'config'`, `payload_meter.py` exit 1 with a traceback. After the fix, 7
  passed. Mutations, each restored from bytes kept before it and each red:
  `refuse_without_hooks`'s missing test forced false, its exit forced to 1,
  the `optin.py` purpose reworded; `_session_cost`'s file check forced false,
  its exit forced to 1.
- **Verified by (executed, 2026-09-26):** `tests/test_a_script_copied_alone_exits_2.py`,
  `tests/test_the_payload_meter_says_what_it_measured.py`,
  `tests/test_the_mode_is_a_row_and_a_command.py`,
  `tests/test_the_records_can_be_carried_out_and_in.py`,
  `tests/test_a_script_says_which_interpreter_it_needs.py` and
  `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`:
  267 passed, 7 skipped; after the function refactor the first three again,
  179 passed. `evidence-check .`: 0 drifted, 0 broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal.py`'s docstring sentence *There is no third one* | the same docstring's exit-code line, which now names 2 |

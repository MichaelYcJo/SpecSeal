# 1790635412-an-overflow-cell-is-refused-in-every-repository — phase 2

<!-- seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | ba9f879b |
| Ran by | unknown — the spawn prompt did not hand this value over, and the template forbids a segment to source it from its own idea of what it is; the orchestrator fills it |

## What this phase was asked

Build `plan.md`'s Phase 2, the commit hears it. In
`hooks/evidence-advisor.py`: `OVERFLOW` in `failing_rows`' filter, its own
block in `main`, and the module docstring's count and list. Fill the
advisor's `OVERFLOW` cell in `skills/evidence-check/SKILL.md`'s reader table.
A10 in `tests/test_dispatch.py`, beside
`test_a_commit_with_a_malformed_ledger_row_is_told_so`. Draft the lines
`CONTRIBUTING.md` §*What a change to a gate must carry* asks a pull request
to carry.

## What this phase found

- **The row's coordinate needs its file here.** The checker's `OVERFLOW`
  coordinate is `line <n>`, which the checker prints under a per-ledger
  heading. The advisor prints no heading and reads every ledger, so
  `failing_rows` puts `display_name(ledger, root)` in front of the line for
  this verdict alone. The other three verdicts' coordinates name their own
  path and are unchanged.
- **No closing line.** Each row's detail already carries the checker's
  remedy, as `MALFORMED`'s do, and round 1 of 1790297087 (⬜ 3) is why a
  closing line repeating a remedy is not added.
- **Seen red, and how.** A10 ran against phase 1's advisor at `b94cd230`:
  `assert 'evidence-check: 1 ledger row wider than its header — …' in ''`,
  the hook printing nothing. Green after. Mutation, restored from kept bytes
  with `tests/__pycache__` cleared: the filter dropping `OVERFLOW`, the
  ledger's name left off the line, and the block not printed each turned A10
  red, and nothing else in `tests/test_dispatch.py`.
- **Narrow runs.** `bin/test tests/test_dispatch.py
  tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py
  tests/test_docs_line_wrap.py`: 69 passed. `uvx ruff check` and
  `uvx ruff format --check` over the two changed Python files: clean.

**For the pull request body** (`CONTRIBUTING.md` §*What a change to a gate
must carry*), drafted here:

- **A test seen red.** `tests/test_dispatch.py::test_a_commit_with_a_ledger_row_wider_than_its_header_is_told_so`
  failed against the advisor before this phase, which printed nothing for a
  fragment row split into six cells.
- **Failure direction.** The advisor never blocks; it prints after a commit.
  Wrong-silent loses one reminder that the lenient CI job and `broad-gate`
  still give; wrong-print is one true line early. A crash inside the arm is
  isolated by `hooks/dispatch.py` and loses the same one reminder.
- **Prompt budget.** Zero. It asks nothing, ever.
- **Platform.** Pure Python, one in-process import of the checker; no
  process inspection. The line's path goes through `display_name`, whose
  Windows separators are covered by its own cases; A10 normalises `os.sep`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

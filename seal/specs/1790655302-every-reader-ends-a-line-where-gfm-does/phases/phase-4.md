# 1790655302-every-reader-ends-a-line-where-gfm-does — phase 4

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 2c253dce |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 4: the transcript tails.
`hooks/worktree-guard.py#last_user_snippet` and `#last_active_event_epoch`
split at LF, as every other transcript reader here does by iterating the
file (questions.md D7). Verified by S16 red at base and the worktree
guard's modules.

## What this phase found

- **Both readers are red at base on their real answer.** With a raw
  U+2028 in the newest record, `last_user_snippet` returned the earlier
  message's timestamp, and `last_active_event_epoch` the earlier event's
  time. Each record's two halves failed `json.loads` and were skipped
  without a word.
- **The fixture writes JSON the way a JavaScript writer does.** Python's
  `json.dumps` escapes U+2028 by default, so a fixture written with it holds
  `\u2028` as six ASCII characters and could not show the defect. The case
  writes with `ensure_ascii=False`.
- **`split("\n")` rather than `gfm_lines`.** A hook does not load a skill
  module on every call (`unverified_check.py#fence_opener`'s docstring),
  and the record end JSON Lines names is LF. A CRLF record keeps its CR,
  which `json.loads` reads as trailing whitespace.
- **No ledger row cited either unit.** G11 is the first.
- **The guard's modules**: `tests/test_worktree_guard.py`,
  `test_worktree_guard_signals.py`, `test_lease_liveness.py`,
  `test_guard_resolves_the_tree_it_judges.py`,
  `test_the_guard_asks_once_per_session.py` and
  `test_gates_do_not_fail_open.py`, with this item's module, 279 passed and
  1 skipped.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

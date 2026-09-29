# 1790635415-a-gate-that-fails-to-load-says-so — phase 4

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 005a9843 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s Phase 4, which the owner added after round 1 so that #661
is fixed in this branch rather than filed. A gate's output that is JSON but
not an object no longer ends its group. `classify` raised on `[1]` and `3`,
and `merge` on `null` and `0`, after every gate ran and outside `run_gate`'s
isolation, so the group exited 1 and a neighbour's `deny` was lost. Such
output is read as text or dropped with a line, never allowed to end the
group, and the builder chooses which and records it. The verification: a
case planting a gate that prints each of `null`, `0`, `3` and `[1]` beside a
denying gate, seen red at `e8e5f977`; `bin/test` over the dispatch modules;
one mutant per changed branch. The spawn also asked for the ledger rows and
the changelog entry naming #661, and every drifted row re-read in place.

## What this phase found

- **The class was wider than four values and one neighbour, and the plan's
  case as written would not have gone red for two of them.** Before writing
  the case, `merge` was called directly over eleven shapes, each beside a
  deny and beside a JSON message:
  - `null` and `0` survive beside a deny and end a group beside a message.
    Beside a deny alone, the case the plan names passes on the old code.
  - `3`, `[1]`, a string, `true`, a `hookSpecificOutput` that is not an
    object, a `permissionDecision` that is not text, and a
    `permissionDecisionReason` that is not text end the group beside either.
  - A `systemMessage` that is not text ends it beside another message.
  - `[]` passed, merged as `{}` and printed.

  So the case plants each shape twice: in `pre-bash`, beside the commit
  gate's deny, and in `session-start`, beside a `systemMessage`. It went red
  on its first shape, `null` in `session-start`.
- **Dropped with a line, not read as text.** Treated as text, `null`, `3` or
  `[1]` alone on a group's stdout would reach the harness as JSON of a shape
  it does not expect, which nothing here has measured. Dropped, the group
  decides as if the gate printed nothing. The "line" is this work item's
  own report: `main()` records the gate as failing while running, with
  `ValueError: printed JSON the dispatcher cannot read: <what it printed>`,
  so it is said once per session at the end of the turn. That kept the
  change inside what phase 1 built: no new channel, and no new record
  shape.
- **One function names the rule.** `dispatch.readable` says what the merge
  reads: an object whose `hookSpecificOutput` is an object and whose
  decision, reason and message are text, each wherever present and not
  null. Null is allowed because the merge already treated a null field as
  absent, and refusing it would have dropped output it read correctly.
  `test_json_the_merge_can_read_is_merged_as_before` pins that half.
- **`zip(strict=True)` is not available.** Ruff's B905 asks for it, and it
  needs 3.10, while a hook runs under 3.9 on a stock macOS. `main()` builds
  the outputs in a loop, and the file was parsed and run once under
  `/usr/bin/python3` 3.9.6.
- **Mutants.** Eight, one per changed branch, were each killed by
  `tests/test_a_gate_that_fails_says_so.py`: the non-object check, the null
  `hookSpecificOutput`, the non-object `hookSpecificOutput`, the field
  types, null fields, the `unreadable` sort, the record in `main()`, and the
  kept outputs.
- **What the plan's wording no longer says.** Its row says `classify`
  raises on `[1]` and `3`. After this phase neither raises, and the
  Delivers cell describes the defect as it stood, which is what a
  delivery description is for.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `merge()` crash from `overview.md` §*Not done* | the same section, now saying phase 4 fixed it (#661) |

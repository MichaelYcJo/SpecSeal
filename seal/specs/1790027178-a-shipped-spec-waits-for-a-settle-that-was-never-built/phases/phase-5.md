# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `86b5bf25` |
| Ran by | `specseal:smith` on Opus 5 (1M context) — the agent definition names no `model`, and the spawning session passed no override, so the segment inherited the session's model |

## What this phase was asked

**The plugin counts what it ships.** Both READMEs' skills rows and *Run it
yourself* cheat sheets, `NUMBER_WORDS[24]`, and `docs/release-checklist.md`'s
by-hand step.

Verified by A8.

## What this phase found

**Four numbers moved, not one, and the suite named all four before a word was
edited.** `tests/test_chain_hooks_hardening.py` derives the total AND the
three group counts from the tree, so shipping a twenty-fourth skill moved the
total from `Twenty-three` to `Twenty-four` and the on-demand group from
`Eleven` to `Twelve`, in both languages, plus the name in both lists. Phase 3
ran those cases and read their messages so this phase owed no searching.

**The cheat-sheet row is the one thing nothing derives.** The count and the
name are both checked against the tree; the row a reader actually types from
is prose in a table, and `CONTRIBUTING.md`'s *both editions move together* is
enforced by a workflow step that only warns. So this phase plants the case.

**The checklist step says the fold is its own branch, and that sentence is the
load-bearing half.** G5 puts `settle` in `docs/release-checklist.md` by hand,
and a step written into the list beside `gather_changelog.py` and
`fold_ledger.py` would read as *do this in the preparation commit* — which is
exactly the arrangement `plan.md`'s Alternatives table rejected, because it
puts a judgment act inside a mechanical commit and a release then stops for
somebody to write documentation. The step is numbered `2b`, sits before the
verification step, and says in its own words that it is a separate branch and
a separate pull request, and that skipping it fails nothing.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `Twenty-three` / `스물세` and `Eleven` / `열한` from the two skills rows | the same rows, now derived-correct at `Twenty-four` / `스물네` and `Twelve` / `열두`; `tests/test_chain_hooks_hardening.py#NUMBER_WORDS` carries the spelling |

# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | ee631b6b |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 1: `without_the_policy_span` ends where GFM ends the statement's paragraph (#831 finding 1), with the `re.search` from `post-review-check-2.md` §*Paste-ready fixes* ⬜ 1 replacing the one-line search, and the docstring left as it stands. Each of the six block plants seen red and the lazy continuation line green, by the means `questions.md` W1 left to the work, defaulting to a `test_tmp_*` probe.

## What this phase found

- **W1 is the probe.** `tests/test_tmp_policy_span_plants.py` patched `builtins.open` for `docs/the-pact.md` only, so both sweep cases read the planted text through their own paths (`read` for the first, a plain `open` for the tree-wide one) and no tracked file was touched. It was run before the change and after it, and deleted before the commit; `git status` showed only the module.
- Before: all seven plants green in both cases. After: the six blocks red in both, the continuation line green, and a control plant after a blank line red both times, which is what shows the probe could go red at all.
- The fence's regex holds against the statement as it stands: none of its lines begins with a listed marker, so the module stayed green (21 passed).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the one-line `end = re.search(…)` in `without_the_policy_span` | the widened search in the same unit |

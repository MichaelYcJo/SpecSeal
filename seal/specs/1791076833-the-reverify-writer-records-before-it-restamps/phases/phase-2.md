# 1791076833-the-reverify-writer-records-before-it-restamps — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 4a9bdd06 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The writer meets W8, W9 and W10 of `spec.md`. W8: a line saying a write
happened prints after the write lands, and none print when the run writes no
ledger. W9: a file the run writes is read strictly, and one that will not
decode is `LEFT` unreadable; code under a coordinate keeps the lenient read
(Q4). W10: a step-3 write failure is a `LEFT` line, the rest are written,
exit 1. Add W1's step-1 stop, W2's mid-apply stop, W3's sibling case and
W6's missing-file arm wherever no carried case holds them. `docs/the-pact.md`
and `skills/evidence-check/SKILL.md` say all of it, the power-loss limit
included (Q3: no `fsync`), each sentence pinned. Every new case seen red;
`bin/mutation-check` over the units this phase changes. Q6 is decided here.

## What this phase found

**Q6, answered by the build.**

- **W8 lives in a `told` list, passed the way `moves` is.** `reverify` and
  `reverify_into` hand their write lines to `told_now` as a function of the
  planned keys that landed. With `told` None — a direct caller, no plan
  open — they print at once, as before. `main` passes a list, and
  `recorded_then_applied` calls each function with what `apply_plan`
  returned, after the record step. `landed_at` is the filter: a ledger's
  hash lines, its dated and undated rows, and its share of the count print
  only where its key landed. So a run that writes no ledger prints none of
  them, and a run whose apply step loses one file prints the others'.
- **W9 is a `strict` flag on `read`**, taken by `reverify` for each ledger
  and by `record_pact_changes` for the record. A file that will not decode
  then reads as None, which both callers already answer: `ledger
  unreadable`, and `the record could not be read`, which is W5. `--into` is
  read leniently inside `reverify_into`, because `main`'s step 0 already
  refuses an `--into` that will not decode. A strict read there survived its
  mutation, so it was taken back out (`4a9bdd06`).
- **W10 is split between `apply_plan` and `recorded_then_applied`.**
  `apply_plan` catches an `OSError` per file, keeps writing, and returns
  `(landed, failed)`. `recorded_then_applied` names each failed file with
  `built_name`, which `apply_plan` has no root for, and exits 1.

**What W8 moves for every `--reverify` user.** The `LEFT` lines of `reverify`
(unreadable, malformed, overflow, undatable) and of `reverify_into` now print
before the hash lines and the counts, because they say nothing was written
and are not held back. Under `--into`, `N citing rows written · M released
rows left` is held back with the `wrote` lines, so a run that cannot record
prints neither. Seventeen modules that drive `--reverify` were run to find
an assertion on the old order: none held one.

**A carried case faked `read` with one argument.**
`tests/test_gates_do_not_fail_open.py`'s unreadable-ledger case patches
`ec.read` with `lambda path: None`, and `reverify` now calls it with
`strict=True`. The fake takes `strict=False` now; its assertion is
unchanged. `tests/test_a_record_states_what_the_tree_has.py` fakes the
records arm's own `read`, which takes no flag.

**The cases the plan asked for, and which already existed.** W3's sibling
case is carried
(`test_a_ledger_that_will_not_read_survives_a_run_that_cannot_record`), so
none was added. W1's step-1 stop, W2's stop between two ledger files and
W6's missing-file arm had no case, and each has one now.

**Seen red (§15), executed.** Against the carried code (`466a1370`), before
any change to `evidence_check.py`: the W8 pair, the W9 pair and the W10 case
failed, 5 of 8; the W10 case's output was a `PermissionError` traceback. The
three that passed against the carried code describe what it already did, so
each was seen red through `bin/mutation-check` instead: applying the plan
before the record step turned both kill cases red; answering a missing
`config.md` as unreadable turned the W6 case red. Every other break, one at
a time, each `red`: `told_now` printing at once (both W8 cases), `landed_at`
answering true (W10), `read` lenient under `strict` (both W9 cases), the
apply step catching `ValueError` instead of `OSError` (W10), the exit
ignoring `failed` (W10), each strict call site made lenient (W9), `read`
catching `OSError` alone (W9), the into report's landed filter dropped (the
`--into` case, after it SURVIVED the whole module first), and each of the
four pinned document sentences reworded (its own parametrized case).

**Verified, executed:** the 21 modules that drive `--reverify` or read the
documents this phase changed, 1054 passed; `bin/fold-check --root .`, 168
statements, exit 0; `uvx ruff check` and `uvx ruff format --check` on the
three Python files changed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `record_pact_changes`'s sentence that `main` puts the ledger back (`restore`) | nowhere: no `restore` exists since `f9469ad8..b4c9deb2`, and the docstring now says `main` writes no ledger file |

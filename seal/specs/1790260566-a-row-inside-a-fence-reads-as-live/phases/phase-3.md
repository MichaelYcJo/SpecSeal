# 1790260566-a-row-inside-a-fence-reads-as-live — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 3ef82a81 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

One open-rows rule, where a line that excuses something must be live
(#487). `fold_ledger.py#open_rows` becomes a load of `todo_open_rows`, and
its copy and the docstring clause "it may not depend on this" go.
`todo_open_rows` takes `drained` only from a line `live_lines` calls live,
and reads no row inside a closed fence (phase 1's rule), while rows inside a
comment stay read. `survivor_check.py#gathered_fragments` counts a marker on
a live line only, as `folded_items` does. Correct the docstrings of
`todo_open_rows` and `settle.py#open_rows`, and `fold_ledger.py`'s module
docstring rule 2 ("wherever it stands"). Cases S7 (both commands), S8 and S9,
each seen red. Q4 answered by the narrow run of the interpreter-floor module.

## What this phase found

**The frame holds.** Each coordinate the plan names reads as it says, and
the two copies of the rule were character for character the same.

**The two halves of `todo_open_rows` read by opposite rules, as the
direction rule says.** `drained` excuses a file, so it is taken only from a
line `live_lines` calls live. A row holds a fact, so it is skipped only
inside a fence that closes (`closed_fence_lines`). The docstring says so,
and says why a row in an unclosed fence or a comment is still open.

**The fold's copy is gone, and `open_rows` is still its name.**
`fold_ledger.py` defines `READER`, `load_reader()` and
`open_rows = load_reader().todo_open_rows`, so the three callers and the
fold's own cases did not change. S8 checks that the function is
`todo_open_rows` from the shipped file, by name and by `co_filename`, and not
by `is`, because every loader makes its own module object. The unused
`DRAINED_RE` in the fold script was removed with the copy.

**The class had two more documents that state the rule.** `CONTRIBUTING.md`
§*House rules* and `docs/branch-and-release.md` §*Work accumulates on a
release branch* both said a `drained` line closes the file. Both now say the
line must be live and a fenced example row is not a row. A grep for
`drained` over `docs/`, `skills/`, `templates/`, `agents/`, `CONTRIBUTING.md`
and the READMEs found no other statement of the rule.

**Cases seen red (executed).** The body of `todo_open_rows` was swapped for
`c52e8350`'s, and `c52e8350`'s `fold_ledger.py` and `survivor_check.py`
were swapped in. Each file was restored from a saved copy of this tree and
compared byte for byte with `cmp`, and `tests/__pycache__` was cleared:

| Case | Against `c52e8350` |
|---|---|
| S7 settle, `test_a_quoted_drained_line_closes_nothing` | red: the quotations closed gamma's file, and gamma was offered for the fold |
| S7 fold, `test_a_quoted_drained_line_closes_nothing`, fence and comment | red, exit 0 on both |
| `test_a_fenced_example_row_is_not_an_open_row` (settle) | red: the example counted as open |
| `test_a_fenced_example_row_does_not_refuse_the_fold` | red: the fold refused over the example |
| S8 `test_the_fold_asks_the_shipped_open_rows_rule` | red: `open_rows` was the script's own |
| S9 `test_a_marker_quoted_in_a_fence_gathers_nothing` | red: exit 0, the fragment excused |

**What the real tree says (executed).** `CHANGELOG.md` carries 110 fold
markers and `live_lines` calls all 110 live, so the sweep's gathered set does
not move. No `seal/specs/*/evidence-todo.md` exists in this tree.

**Q4 (executed).** `bin/test tests/test_a_script_says_which_interpreter_it_needs.py
tests/test_the_release_check_watches_what_ships.py tests/test_release_hygiene.py -q`
gave 105 passed. The new load trips no interpreter-floor case.
`fold_ledger.py --check` on the branch loads the reader and exits 1 for
the one reason a branch has: this work item's fragment has not folded.

**The ledger (executed).** The edit drifted 4 rows plus this work item's own
`fence_opener`. Each was read against it:

- `seal/releases/0.13.0.md` S4 and `seal/releases/0.14.0.md` D3 hold, and
  each got a `Re-read` note.
- `seal/releases/0.15.1.md` C2 said a fragment is gathered when its marker
  "stands in `CHANGELOG.md`". That is false for a quoted marker, so it was
  **corrected in place** to "stands on a live line of `CHANGELOG.md`", with a
  `Corrected 2026-09-25` note.
- **Two rows of `seal/releases/0.4.0.md` were REMOVED.** They were anchored
  on `.github/scripts/fold_ledger.py#open_rows` when that was the copy: the
  `drained`/✅ rule, and the split on `\n` alone. The function they described
  is gone. The anchor would still resolve to the one-line alias, and
  re-stamping it would point a claim about the rule at an assignment. Their
  claims are rewritten, narrowed by #487, as P3-1 in the fragment, anchored
  on `todo_open_rows`.
- The two document edits drifted 5 anchors in 5 rows: 0.12.2 C8, 0.15.0 P1c,
  0.15.1 D1 and E1, and the 0.4.0 `--check` row. Each holds and got a note.

After `--reverify`: `2091 ok · 0 drifted · 0 broken · 0 old-format`, exit
0. **One slip, caught before this record:** the phase's commit was first
made after the ledger check had printed exit 2, because formatting two
cases had drifted two of this work item's own rows. The check's exit was
printed and not read. The re-stamp was amended into the phase's commit,
which is the hash above, and the check was run again at exit 0.

**Modules run (executed).** Phase 2's 79, plus every module naming
`CONTRIBUTING`, `branch-and-release`, `fold_ledger` or `survivor_check`, for
87: `3590 passed, 8 skipped`, exit 0. The two test files were formatted
after that run and before the commit. Formatting changes no case, and the
case the formatter touched was rerun alone: 1 passed. `uvx ruff check` and
`format --check` over the seven edited Python files are clean.

**What `CONTRIBUTING.md` §*What a change to a gate must carry* asks:**

- **The case seen red:** the table above.
- **Failure direction:** a quoted `drained` or a quoted marker now excuses
  nothing, so the fold, `settle` and the sweep block more. That is the safe
  direction for a guard, and a person sees it. A fenced example row is no
  longer counted as open, which allows more. That is justified only for a
  fence that closes, the same ground as phase 2, and a row in an unclosed
  fence or a comment is still open.
- **Prompt budget:** 0.
- **Platform note:** pure text processing, with lines split on `\n` alone
  as before. Run on macOS only, and CI runs the Linux leg.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `.github/scripts/fold_ledger.py#open_rows`' copy of the rule, and its unused `DRAINED_RE` | `skills/verify/scripts/unverified_check.py#todo_open_rows`, loaded by the fold |
| two rows of `seal/releases/0.4.0.md` anchored on that copy | `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md` P3-1 |

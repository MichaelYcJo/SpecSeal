# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | c3afabf8 |
| Ran by | unknown — the spawn prompt did not name the agent and model, and the segment does not source that value from itself |

## What this phase was asked

`plan.md` phase 1: `fold_ledger.py#demote` on `fence_opener` / `fence_closes`
with its `# RIDER:` retired; `is_marked` (so `folded`), `doubled_markers` and
the `--check` count reading markers through `live_lines`; `version_headings`,
`section_heading` and `insert`'s walk to the next `## ` skipping fenced
lines; `docs/branch-and-release.md` saying a quoted marker is not a fold
where it describes `--check`. Verified by S1–S5 in
`tests/test_the_ledger_fragments_fold_at_release.py`. Q4 (one helper or a
call each) is this phase's to answer.

## What this phase found

- **Q4 is answered: one helper.** `fenced_lines(lines)` returns the indices
  inside a fence span, an unclosed block to the end, over
  `unverified_check.py#fence_spans`. `demote`, `version_headings`,
  `section_heading` and `insert` all ask it, so the four cannot drift apart.
- **The marker readers read each ledger once.** `live_markers(text)` returns
  `(id, line number)` for every marker on a live line. `folded` reads each
  ledger's set once rather than calling `is_marked` per fragment per ledger,
  because `live_lines` computes two readings of the whole file.
  `is_marked` stays, as a one-line wrapper, because
  `gather_changelog.py`, `unverified_check.py` and three test modules cite it
  by name as the line-anchor precedent.
- **`section_heading` keeps its return shape.** It still returns a match on
  the whole text, the first one whose line is not fenced, so `main` and
  `insert` read `.start()` and `.group(0)` as before.
- **S5 needed a second case.** The spec's S5 covers `version_headings`.
  `section_heading` and `insert` are two more readers of the same line, and
  each has its own case in
  `test_a_fenced_heading_neither_joins_nor_ends_a_release_section`: a file
  whose only `## 0.4.0` is fenced is refused rather than joined, and a second
  fold into a file ending in a fenced `## 0.5.0` appends after the example.
  Each half was killed by its own mutation.
- **`--split` reads two rules now, on purpose.** `doubled_versions` goes
  through `version_headings` and skips fenced headings; `release_sections`
  keeps its own walk, as `spec.md` puts it out of scope. `--split` is a
  migration this repository has taken, so the difference reaches no run.
- **Nothing in this tree changes answer.** `fold_ledger.py --check` over this
  tree reads 125 markers before and after, exit 0. `rider_check.py` reads 22
  riders at `c2478597` and 21 after, the one retired.
- **Ledger rows.** Two rows were false after the edit and are corrected in
  place with dated notes (`seal/releases/0.4.0.md`: `demote`'s fence rule,
  and a fenced marker being a mark). Eleven more were re-read and re-stamped,
  among them `fence_opener`'s two rows, whose note covers every phase of this
  work item because each one edits only that docstring. The row anchored on
  the `### 1788331011` section took the usual two `--reverify` passes.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `# RIDER:` above `demote`'s fence close, which recorded the three-character rule as a known misread | nowhere — its condition is met. `seal/releases/0.4.0.md`'s `demote` row is corrected to say so, and S1/S2 pin the rule the rider asked for |
| `.github/scripts/fold_ledger.py#demote` in `fence_opener`'s list of readers that keep their own rule | the same docstring's list of readers that ask it |

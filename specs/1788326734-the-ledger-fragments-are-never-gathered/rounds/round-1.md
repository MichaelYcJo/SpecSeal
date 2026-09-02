# 1788326734-the-ledger-fragments-are-never-gathered — review round 1

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered/rounds/round-1.md —
what this round of the review chain did, written by the review orchestrator
right after verifying the reviewer's report. `docs/review-handoff-protocol.md`
carries the format. -->

| Field | Value |
|---|---|
| Target SHA | e4b74fc |
| PR | none yet |
| Broad gate | not yet — the one full run follows the verifying round |
| Fixes checked by | nobody — the fixes are not yet written; round 2 verifies them and this cell is set to it then |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (the messages print `os.path.join` paths, so three tests fail on the Windows leg) and 🔴 2 (the self-check test reads the fragment the fold removes, so the release-preparation commit turns the tests red) |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 0 | Stage 1: the fold moves every row byte for byte and removes the fragment, an unmerged item keeps its fragment because it is not in the tree, an open evidence-todo row refuses the whole fold naming the file, a folded item is marked not matched, a second run folds nothing twice, `--dry-run` writes nothing, `--check` runs on pull requests into `main` only and says how many items it saw, no document says *never gathered*, an empty fragment is removed and named | `.github/scripts/fold_ledger.py:90-152, 160-202, 244-326`, `.github/workflows/hygiene.yml:84-90`, `specs/…/spec.md` S1–S10 | pass | executed by the reviewer on a `git archive` copy of the tree at e4b74fc: 7 fragments, 99 table rows identical after the fold, `.specseal/map/` gone, second run exit 1, `--check` exit 1 before and exit 0 `7 work items marked` after; 36 cases green |
| 🟢 0b | The checker's totals move by exactly the rows two files cited with one `(coordinate, hash)`: 155 ok → 154 ok, 0 drifted, 0 broken | `skills/evidence-check/scripts/evidence_check.py:828-839` (`seen` is local to `check_ledger`, so the dedup is per file) | pass | orchestrator read the dedup; reviewer executed the fold on the copy |
| 🟢 0c | `questions.md` Q1–Q3 defaults each fail toward a named stop: an old item's undrained file blocks the release; the section is appended because the checker reads no position; `--check` runs the guard too | `specs/…/questions.md` | pass, defaults stand until the owner answers | reviewer's reading; the position claim executed |
| 🔴 1 | `LEDGER` and `FRAGMENTS` are built with `os.path.join` and printed as such, so on Windows the `--check` output and the already-folded refusal print `.specseal\map…`; three assertions expect forward slashes, and `test.yml` runs the whole suite on `windows-latest` with no skip on this file | `.github/scripts/fold_ledger.py:76-77, 250, 271, 286`; `tests/test_the_ledger_fragments_fold_at_release.py:287, 457-458, 477` | open | orchestrator executed `ntpath.join(".specseal","map")` → `.specseal\map`; `open_items` already normalises with `replace(os.sep, "/")` at `:201`, the constants do not. Fix: keep the constants `/`-joined for messages and build disk paths through one helper (reviewer's paste-ready `under(root, rel)`) |
| 🔴 2 | `test_this_work_item_wrote_its_own_fragment` asserts the fragment file exists; the release-preparation commit runs the fold, which removes it, so the first real run of the script turns the `tests` workflow red on the release pull request. A permanent test reading a between-releases file is the shape the dependency rule names "would break on removal" | `tests/test_the_ledger_fragments_fold_at_release.py:566-577`; `docs/one-root-by-lifetime.md` §The dependency rule | open | orchestrator read the test; reviewer executed the fold on the copy and ran the repository-level tests: this one failed alone (1 failed / 184 passed). Fix: accept the fragment while it exists, else its marker in `map.md` (reviewer's snippet) |
| 🟡 3 | `folded()` tests the marker as a substring while `--check` counts it line-anchored, so a marker quoted in `map.md` prose refuses the fold, and the refusal's advice ("compare against the folded section, then remove the fragment") would have a person delete the only copy of the rows | `.github/scripts/fold_ledger.py:106-108, 251, 288-290` vs `:82, 268` | open | reviewer probe F executed; today's `map.md` quotes only a placeholder, so nothing refuses now. Fix: one line-anchored test for both |
| 🟡 4 | `open_rows` splits with `splitlines()`, which also breaks on U+2028, U+0085 and `\x0c`; a cell holding one of those followed by `drained` closes the file, the silent direction for a guard | `.github/scripts/fold_ledger.py:169` | open | reviewer probe E executed (`0 open` where one row is open). Fix: `text.split("\n")` |
| 🟡 5 | `demote` is not byte-for-byte in three shapes: `.strip()` drops the last row's trailing whitespace, `splitlines()` splits a row on U+2028, and a `#` line inside a code fence is demoted as a heading | `.github/scripts/fold_ledger.py:120-129`; `specs/…/spec.md:120-121` | open | reviewer probes A–C executed; today's seven fragments have none of the three (grep 0), so the real fold was 99/99. Fix: split on `\n`, strip only newlines, skip fenced lines |
| 🟡 6 | The ledger fragment's row 11 cites `72cf296`, a commit this branch made; the squash into the release branch orphans it, which is what `CLAUDE.md`'s rule against stamping a row with a branch commit exists for. `plan.md:76` carries the same SHA with an explicit "nothing measured from here" | `.specseal/map/1788326734-…md:11` | open | orchestrator grep confirmed; the Checked cell holds the date alone, so `tests/test_a_row_points_by_content.py` does not catch it. Fix: describe the tree state without the SHA |
| 🟡 7 | `.specseal/map.md:40` still says the file "empties as work items retire the claims it holds", the pre-fold picture; the new header at `:11-16` says it grows once per release. S9's phrase list does not contain this sentence | `.specseal/map.md:40` | open | orchestrator read both. Fix: the reviewer's replacement sentence |
| 🟢 8 | An interrupted run (ledger written, removal not reached) is refused at the next run rather than resumed, and the docstring says so | `.github/scripts/fold_ledger.py:28-31, 283-292` | pass — the safe direction, documented; 🟡 3 removes the one way that advice loses rows | reviewer's reading |
| 🟢 9 | The broad gate has not run and the account says so honestly: `overview.md` separates executed (36 cases, 5 mutations, 9-file scope run) from read | `specs/…/overview.md:9, 29-32` | pass | orchestrator read |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `tests/test_the_ledger_fragments_fold_at_release.py` on the real tree | 36 passed |
| reviewer: fold on a `git archive` copy at e4b74fc — `--check` before, `--version`, row identity, second run, `--check` after | exit 1 naming 7 fragments · folded 7 · 99/99 rows identical · exit 1 `nothing to fold` · exit 0 `7 work items marked` |
| reviewer: `evidence_check.py .` on the copy before and after | 155 ok → 154 ok · 0 drifted · 0 broken |
| reviewer: repository-level tests (6 files) on the folded copy | 1 failed (`test_this_work_item_wrote_its_own_fragment`) / 184 passed |
| reviewer: mutation — the ✅ rule removed | exactly 1 case red |
| reviewer: probes A–F (fence, trailing whitespace, U+2028 in a row, U+2028 before `drained`, separator-less table, `- drained` list item, marker quoted in prose) | fence demoted · trailing tab dropped · row split · `0 open` · `2 open` · `1 open` · refused as already folded |
| orchestrator: `ntpath.join(".specseal", "map")`, `ntpath.join(".specseal", "map.md")` | `.specseal\map`, `.specseal\map.md` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `questions.md` Q1–Q3 — an earlier release's undrained file, append vs insert, `--check` running the guard | `specs/…/questions.md`, defaults taken and named in the pull request body | the repository owner |
| The hygiene step and the fold on a real release commit | `specs/…/overview.md` §Not verified | the repository owner, at the 0.4.0 release |

# 1788326734-the-ledger-fragments-are-never-gathered — review round 2

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered/rounds/round-2.md —
the verifying round for round 1's fixes (target: the diff 27e5059..855b8e8,
never the branch). It opened one thing needing a fix, so it is a finding
round and consumes the cap: two of three used, five allowed while a 🔴 is
open. Written by the review orchestrator after opening the coordinates. -->

| Field | Value |
|---|---|
| Target SHA | 855b8e8 (the fix diff from 27e5059); HEAD a96ffdc at review time, a record-only commit after it |
| PR | none yet |
| Broad gate | not yet — a 🔴 is open |
| Fixes checked by | round-3 |
| Contract changes | `demote` → `section` (same signature, a title after whitespace-only lines is dropped rather than demoted, and `~~~` fences are honoured, each closed only by its own kind) |
| New units | `tests/test_the_ledger_fragments_fold_at_release.py#test_a_blank_line_above_the_title_and_a_tilde_fence_are_read_right`; `#test_this_work_items_rows_are_still_found_after_the_release_folds_them` rewritten on the `tree` fixture (same name, `import shutil` removed) |
| Needs a fix | yes — 🔴 1 (the new after-fold test copies the real tree, so once the release-preparation commit has folded it the copy has nothing to fold and the test fails with `nothing to fold`, 1 failed / 41 passed on a folded copy); 🟡 3 is a ledger cell a run refutes; 🟡 2 and 🟡 4 can be answered with grounds |

- [ ] Pass

## Verdicts

Round 1's verdicts first, each answered on this round's grounds; then what this round opened.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r1 🔴 1 | messages printed `os.path.join` paths | `.github/scripts/fold_ledger.py:79-80, 118, 230, 268, 350, 352` | fixed | reviewer read: the constants are `/`-joined and every disk access goes through `under()`; the two remaining `os.path.join` are the script's own location. Executed: the new slash test passes |
| r1 🔴 2 | the self-check test read the fragment the fold removes | `tests/…fold_at_release.py:660-684` | fixed for the original test; the fix's own new test reopens the same shape — this round's 🔴 1 | reviewer executed the fold test file on a folded copy: 1 failed / 41 passed, the failure being the new test |
| r1 🟡 3 | `folded()` substring vs `--check` line-anchored | `.github/scripts/fold_ledger.py#is_marked` | fixed | executed: the quoted-marker test is red against the script at 27e5059 and green at HEAD; `is_marked` on a marker with no trailing newline → True |
| r1 🟡 4 | `splitlines()` in `open_rows` | `.github/scripts/fold_ledger.py#open_rows` | fixed | executed: the U+2028-before-`drained` test red at 27e5059, green at HEAD |
| r1 🟡 5 | `demote` not byte-for-byte | `.github/scripts/fold_ledger.py#demote` | fixed for the three named shapes; two more in the new unit — this round's 🟡 4 | executed: the three cases red at 27e5059, green at HEAD |
| r1 🟡 6 | fragment row cited a branch commit | `.specseal/map/1788326734-…md` | fixed | reviewer grep: no 7-hex outside `@hash` |
| r1 🟡 7 | `map.md` said the file "empties" | `.specseal/map.md:39-40` | fixed | orchestrator read: the new sentence matches the header at `:11-16` |
| r1 evidence-todo | three rows to drain | `specs/…/evidence-todo.md` | fixed | executed: `open_rows` on all three evidence-todo files in the tree → `[]`; `fold_ledger.py --check` names the seven fragments and prints no evidence-todo section |
| r1 Contract changes | reach of `folded`, `demote`, `open_rows`, `section`, `LEDGER`/`FRAGMENTS` | `fold_ledger.py:118, 171, 233, 275, 337` and the 13 message sites | pass | reviewer read every site; nothing imports the script, `hygiene.yml:90` and the documents call it by command line only |
| 🔴 1 | `test_this_work_items_rows_are_still_found_after_the_release_folds_them` copies `ROOT`'s `.specseal/` and `specs/` and asserts the fold exits 0. After the release-preparation commit folds this tree, the copy holds no fragment, the script exits 1 `nothing to fold`, and the `tests` workflow is red on `main` and every branch cut from it until a work item writes a fragment. Round 1's 🔴 2 named exactly this window, and the fix's own test reopens it | `tests/…fold_at_release.py:686-695` | open | orchestrator executed: folded a copy of the tree, then ran the fold on a copy of that copy → exit 1 `nothing to fold`. Fix: fold this work item's fragment on the `tree` fixture instead of a copy of `ROOT` (reviewer's paste-ready test in the report) |
| 🟡 2 | the same test copies `specs/`, so an open evidence-todo row anywhere in the tree fails it — the review's own mid-state between a reviewer writing rows and the smith draining them, which `hygiene.yml` deliberately keeps off feature pull requests | `tests/…fold_at_release.py:690-691` | open — answer with grounds or let the 🔴 1 fixture fix close it | reviewer executed with this work item's evidence-todo at its 27e5059 state: 1 failed, `3 open rows` |
| 🟡 3 | the fragment row's Notes say "the backslash test fails on every leg"; with the constants reverted to `os.path.join` it passes on macOS, because only Windows produces `\`. `plan.md:78` says the opposite, correctly | `.specseal/map/1788326734-…md:14` | open | reviewer executed `-k slash_joined` on a reverted copy: 1 passed. Fix: the reviewer's replacement cell |
| 🟡 4 | the new `demote`: a whitespace-only first line before `# <id>` leaves the title to be demoted into a second `### <id>`; and `~~~` fences are not recognised, so a `#` line inside one is demoted | `.github/scripts/fold_ledger.py:145-147, 151` | open | reviewer executed both shapes; today's seven fragments have neither (grep 0). Fix: skip leading blank lines, recognise both fence forms (reviewer's snippet) |
| 🟢 5 | `is_marked` reads a marker standing alone inside a code fence as a mark; inline quotes and padded lines are not. Fold and `--check` agree, and the safe direction (refuse) | `.github/scripts/fold_ledger.py:106` | pass — say "quoted inline" in fragment row 13 | reviewer executed 8 cases |
| 🟢 6 | the after-fold helper takes everything after the marker as this work item's section; with S10 (an empty fragment gets no marker) the marker assertion is the real proof | `tests/…fold_at_release.py:672-675` | pass | reviewer read |
| 🟢 7 | `under()` on `./x`, an absolute path and `a//b` — all joined below root; callers pass constants and a basename-derived id only | `.github/scripts/fold_ledger.py#under` | pass | reviewer executed 5 cases |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the fold test file on a copy of HEAD's tree after `--version 9.9.9` folded it | 1 failed (`…still_found_after_the_release_folds_them`, `nothing to fold`) / 41 passed |
| reviewer: HEAD's tests against the script at 27e5059 | exactly 4 red: quoted marker, U+2028 row, trailing whitespace/fence, U+2028 before `drained` |
| reviewer: HEAD's tests with this work item's evidence-todo reverted to 27e5059 | 1 failed, `3 open rows` |
| reviewer: `-k slash_joined` with `LEDGER`/`FRAGMENTS` reverted to `os.path.join` | 1 passed on macOS |
| reviewer: `is_marked` 8 cases, `demote` 9 cases, `under` 5 cases, `open_rows` on the three real evidence-todo files | as recorded in the verdicts |
| reviewer: `evidence_check.py --strict .` on the real tree; `.` on a folded copy | 160 ok · 0 · 0; 160 → 158 ok on the copy |
| orchestrator: fold a copy of the tree, then fold a copy of the folded copy | `folded 7 fragments` then exit 1 `nothing to fold` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `.github/scripts/fold_ledger.py#demote`, `#open_rows`, `#is_marked`, `#under` | every unit round 1's fixes touched or created; round 3 opens the fix diff again |
| round 1 | `tests/…fold_at_release.py` "this repository" block | where both 🔴s of this run lived |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the Windows leg is green after the slash fix | the first CI run of the pull request | the repository owner reads the `windows-latest` job |
| `questions.md` Q1–Q3 | `specs/…/questions.md`, defaults taken | the repository owner |

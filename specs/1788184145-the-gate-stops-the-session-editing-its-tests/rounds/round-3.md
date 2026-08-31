# 1788184145-the-gate-stops-the-session-editing-its-tests — review round 3

| Field | Value |
|---|---|
| Target SHA | `eaec4936e03bf251c15780b6e186e5a058571ab4`, and `d3fe44da65d6d58085a78d0662913667d1696054` after this round's fixes |
| PR | opens onto `release/v0.0.2` after this record |
| Broad gate | `d3fe44d`, against base `release/v0.0.2` (`f1cd65d`) |

- [x] Pass

<!-- Round 3 is the last of the run. The four findings below were raised by the
reviewer, verified by the orchestrator and fixed by the orchestrator in
`d3fe44d` rather than by a fourth round: none needed a judgment, every wording
was already drafted and measured, and a fourth round with no 🔴 open is the
loop failing to converge rather than another fix. -->

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The refuted one-branch rule survived in the only prose that ships outward. Every other place had been corrected; `CHANGELOG.md` still said the gate *counts a segment whose command word is `git`* and stopped there | `CHANGELOG.md:11-18` | **fixed** `d3fe44d` | Executed: `grep -c "eval\|cannot expand" CHANGELOG.md` returned 0, and the file had not been touched since `2a28c35`. A reader learning the rule from the release notes would check a patch for a commit, find none, and conclude it was clear. The entry now carries both branches, in the same shape the agent files use |
| 🟡 2 | `questions.md` Q2 was outside the table. A blank line between the Q1 and Q2 rows ends a markdown table, so the row a human is meant to answer rendered as a paragraph of pipe characters | `questions.md:12` | **fixed** `d3fe44d` | Read, confirmed byte-for-byte with `sed -n l`. Q2 is one of the two rows this work hands to the repository owner; the file exists so nothing ships on a silent assumption, and an unreadable row is a silent assumption with extra steps |
| 🟡 3 | The prose named two of the seven expansion characters. `a variable or a command substitution` covers `$` and `` ` ``; `EXPANDS = "$`*?[]{}"` also holds the glob and brace characters | `agents/smith.md:110-111` · `agents/warden.md:163-164` | **fixed** `d3fe44d` | Executed by the orchestrator, `scratchpad/verify_round3_glob.py`: `eval 'ls *.py'` TRIPS · `eval 'cat f?'` TRIPS · `eval 'echo [ab]'` TRIPS · `eval 'echo {a,b}'` TRIPS · `eval 'echo hello'` clean. Round 2's failure one layer shallower — a session checking `$` and a backtick would clear a glob `eval` and still meet the prompt. Both files now say *a variable, a command substitution or a glob* |
| 🟡 4 | The rider at `agents/smith.md:43` started at column 0, splitting the numbered list item it sits inside, and cited `specs/1788184145-…/questions.md` — a path that does not exist in a repository that installed the plugin | `agents/smith.md:47-53` | **fixed** `d3fe44d` | Read. The same rule round 1's finding 2 established and the memo's divergence row already invokes: a shipped agent file does not point at what its reader's repository lacks. Indented to three spaces, and the citation is now *Q2 in the work item's questions.md*. The rider still does not quote the waiver example — re-probed, `agents/smith.md` trips at line 43 alone |
| 🟢 5 | Round 2's seven verdicts all hold on round 3's own grounds | `round-2.md` | answered | Executed by the reviewer: both branches stated separately with the reason the second counts; phase 4 names `2a28c35` and phase 5 was closed by the commit after the one that wrote it; `plan.md` carries five coordinates and `evidence_check` resolves eleven; the rider and Q2 both landed with no prompt raised |
| 🟢 6 | Six test cases, thirteen mutations, every one red | `tests/test_edits_go_through_the_edit_tool.py` | answered | Executed: six pass unmutated; each mutation asserts the file actually changed before running; the tree was restored and checked after every one. Includes the property the implementer reported — dropping `command position` from `agents/warden.md` turns round 1's case red at baseline, which is how its own rewrite was caught |
| 🟢 7 | The apostrophe rule as sharpened is the true one | `.specseal/map.md` · `agents/warden.md` | answered | Executed: the waiver row is now `:179`, with 11 apostrophes above it — odd — and the file clean, so the absolute count does not predict the verdict. Parity of *added* prose still holds: 1 → True, 0 → False, 2 → False |
| 🟢 8 | `spec.md` had not caught up with what three rounds delivered — the regression test, the rider and Q2 appear in no acceptance row | `spec.md:35` | **fixed** `d3fe44d` | Read. Two acceptance rows added: that the wording cannot be deleted without a check going red, and that the warden's own file does not trip the gate it warns about. Both name the test that proves them |

## Executed probes

| What was run | Result |
|---|---|
| `verify_round3_glob.py` — seven `eval` bodies through `_hides_a_commit` | four unnamed expansion characters all TRIP; `eval 'echo hello'` clean |
| `grep -c "eval\|cannot expand" CHANGELOG.md`, before the fix | 0 |
| `final_gate_and_width.py` — both agent files after every fix | `agents/smith.md` trips, at line 43 only · `agents/warden.md` whole-file False |
| thirteen mutations over six test cases | every one RED; six pass unmutated; tree restored each time |
| the narrow suite, 12 files, after the orchestrator's fixes | 193 passed |
| **the broad gate, once, at `d3fe44d`** | **886 passed, 1 skipped** in 72.54s |
| `ruff check .` · `ruff format --check .` | All checks passed · 59 files already formatted |
| `bin/evidence-check` | 11 ok · 0 drifted · 0 broken · 0 external |
| `unverified_check.py` | this work item: 1 open · 1 closed after the memo was marked |

## Inherited coordinates

Nothing inherits from here — this is the last round. What round 2's table
taught, recorded because it outlives this work item: **a relative instruction
survives the fix and an absolute line number does not.** Round 2 wrote the
waiver row as `agents/warden.md:173`; the fixes moved it to `:179` and the
reviewer's script failed to find its anchor. The instruction beside it —
*above the waiver row, never below it, because quote state flows forward* —
was still exactly right and is what got used. A line number carried forward
needs the SHA it was taken at in the same cell, or it should be written as a
relation instead.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Q1 — should the gate skip a heredoc body being written to a file? Round 3 raises its value again: skipping would cover the `eval` branch and the glob half too | `questions.md` Q1, and the PR body | the repository owner |
| Q2 — how to resolve `agents/smith.md:43` tripping its own file. Three priced options; a rider is planted at the coordinate so the fact reaches whoever opens the line either way | `questions.md` Q2, and the PR body | the repository owner |
| That an agent following the new instruction actually stops meeting the prompt. The change is prose, so nothing in the suite can execute it | the memo's `## Not verified`, still open by design | the repository owner, at the next session editing the gate's own test files |
| The command string that actually triggered issue #34 | `round-1.md`, and no longer load-bearing — the delta-debugged body was reproduced directly | the session that opened issue #34 |

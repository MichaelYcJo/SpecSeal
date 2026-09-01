# 1788184145-the-gate-stops-the-session-editing-its-tests — review round 2

| Field | Value |
|---|---|
| Target SHA | `2a28c3541c06a13e02aa8d10c56ddf9d456979d5` |
| PR | not open yet — it lands on `release/v0.0.2` after the rounds settle |
| Broad gate | not yet |
| Fixes checked by | round-3 |

<!-- The row was added later, by
`specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody`. Round 3's
finding 5 is what it records — *Round 2's seven verdicts all hold on round 3's
own grounds*, executed by the reviewer. Nothing else about this record
changed. -->

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The corrected rule states one branch of two. `What it counts is a segment whose command word is `git`` reads as the whole rule; a segment the reader cannot expand counts the same way, with no `git` in the body at all | `agents/smith.md:91-94` · `agents/warden.md:156-158` | **fixed** `96a1ae3` | Executed by the orchestrator, `scratchpad/verify_round2_eval.py`: `eval "$CMD"` TRIPS · `eval $(cat f)` TRIPS · `eval "echo hello"` clean · `print('hello')` clean. Neither agent file contains the word `eval` (checked directly). `hooks/commit-review-gate.py:148-150` reads `_eval_argument`, and `_eval_hides_a_commit` returns True on an expansion character it cannot resolve — the docstring at `:183-186` says why: nothing can tell *reduces to a commit* from *reduces to something else* without running the shell. **Why it bites**: a smith following this prose searches its patch for `git commit`, finds none, proceeds, and meets the prompt anyway. `tests/test_what_the_reader_understands.py:89` is `("an eval", "eval 'cd %s'; git commit -m x", …)`, so a partial patch of that file is exactly the case | **Re-ran the probe independently** rather than taking the table: all four bodies reproduce, and `EXPANDS = "$`*?[]{}"` at `hooks/cmdline.py:678` is what makes an unresolvable argument count. Both files now state the two branches separately, the second with the reason it counts rather than as a special case. Pinned by a sixth test case asserting both `` `eval` `` and `cannot expand` in each file; three mutations turn it red. The reviewer's paragraphs were used as a starting point and rewritten — while doing so I dropped `command position` from `agents/warden.md`, and round 1's own test caught it at the baseline run before any mutation |
| 🟡 2 | Half of round 1's work is in no phase row. `2a28c35` carried the corrected mechanism into `CHANGELOG.md`, `overview.md` and the ledger, and no Status column names it | `plan.md:70-71` | **fixed** `96a1ae3`, closed by a final commit | Confirmed `git show --stat 8b6c6ff` myself. Phase 4 now names `2a28c35` beside it, and a phase 5 row carries round 2's own work. Phase 5's Status was left EMPTY in `96a1ae3` and filled by the commit after it, following `4a48eee`. I first typed a SHA that did not exist yet and caught it before committing — which is the failure this column exists to prevent, met from the inside. Original grounds: `git show --stat 8b6c6ff` touches only the two agent files and the new test, which matches phase 4's text exactly — so the gap is real rather than a mislabel. This is round 1's finding 4 recurring one commit later. The repository already has the answer: `4a48eee` exists to do nothing but close a phase with the commit that carried it |
| 🟡 3 | `plan.md`'s Technical context still cites `hooks/commit-review-gate.py:151` alone — the coordinate round 1 recorded as not reaching the rule | `plan.md:39` | **fixed** `96a1ae3` | Technical context now carries `:144-147` (the segment scan), `:148-150` with `_eval_hides_a_commit` at `:176-188` (the second branch), `EXPANDS` at `hooks/cmdline.py:678`, and `:262-286` (`commit_invocations`). `:151` is kept with a note that it alone does not reach the rule, so a reader who arrives at it is not left guessing. `evidence_check` resolves all eleven coordinates. Original grounds: `round-1.md:43` says it in as many words: *"`:151` alone does not reach it"*. The ledger gained `:144-147` and `:262-286`; the plan did not, so the next session opening the plan for grounds lands on a recursion line |
| 🟡 4 | `agents/smith.md` trips the gate at its own waiver example, so a smith patching its own contract by heredoc meets the prompt this work item exists to remove. The fact is recorded in a ledger aside with no answerer and no schedule | `agents/smith.md:43` · `.specseal/map.md:51` | **fixed** `96a1ae3` | Both halves delivered. A `# RIDER:` sits at the coordinate, stamped `Verified 2026-08-31 at f1cd65d` — an ancestor of the base, never a commit this branch made — and `tests/test_a_rider_reaches_its_file.py` passes, 8 cases. The rider deliberately does NOT quote the waiver example, because repeating it verbatim would have created a second trip line in the file the rider is about; re-probed after planting and `agents/smith.md` still trips at line 43 alone. `questions.md` Q2 carries three options with what each costs, and the repository owner as answerer. I did not raise it as a prompt. Original grounds: whole-file `_hides_a_commit` returns True, and the trip line is `43: … `: '[no-review]'; git commit …``. `.specseal/follow-up.md` states the rule for exactly this shape — *anything tied to a coordinate is a `# RIDER:` comment at the line it is about* — and there is no rider at `:43`. It also needs a decision, because a waiver example is only useful shown verbatim |
| 🟢 5 | The apostrophe claim reproduces, down to parity | `agents/warden.md:162` · `tests/test_edits_go_through_the_edit_tool.py` | answered, and **sharpened** in `96a1ae3` — what is parity-sensitive is the apostrophes ADDED above the waiver row, not the file's absolute count. Measured after this round: 11 apostrophes above that row, an odd number, and the file is clean. Backticks and double quotes interact, so only the whole-file verdict answers it. The ledger row now says so, because a reader counting characters would draw the wrong conclusion | Executed by the reviewer at the coordinate the prose actually occupies: baseline False · one apostrophe **True** · same text with none False · two False · three **True**. The inserted paragraph contains no `commit` at all |
| 🟢 6 | All five cases of the new test can fail | `tests/test_edits_go_through_the_edit_tool.py` | answered | Executed: ten mutations, each asserting the file actually changed before running, each turning its case red; five pass unmutated; the tree was restored and `git status` checked after every one |
| 🟢 7 | Round 1's findings 2 and 6 hold. No agent file names a repository, no stale copy of the refuted diagnosis survives outside the round records and the test that pins its absence, the three ledger stamps are `f1cd65d`, and `evidence_check` resolves all seven rows | `agents/*.md` · `.specseal/map.md` | answered | Executed: `grep -i "this repository\|this one's\|the gate's own tests"` returns 0 in both agent files · 184 narrow tests pass · `evidence_check` 7 ok · 0 drifted · 0 broken · `ruff check` and `ruff format --check` pass |

## Executed probes

| What was run | Result |
|---|---|
| `verify_round2_eval.py` — five bodies through `_hides_a_commit` | `git commit -m x` TRIPS · `eval "$CMD"` TRIPS · `eval $(cat f)` TRIPS · `eval "echo hello"` clean · `print('hello')` clean |
| the same, does either agent file contain `eval` | both False |
| `tests/test_what_the_reader_understands.py:89` | `("an eval", "eval 'cd %s'; git commit -m x", "eval 'cd %s'")` |
| apostrophe parity, paragraphs inserted at `agents/warden.md:162` | 0 → False · 1 → **True** · 2 → False · 3 → **True** |
| ten mutations over the five new test cases | every one RED; unmutated 5 passed; tree restored each time |
| the narrow suite, 11 files | 184 passed |
| `evidence_check.py` · `unverified_check.py` · `ruff check` · `ruff format --check` | 7 ok · 0 broken · 2 open · passed · already formatted |
| `git show --stat 8b6c6ff` | `agents/smith.md`, `agents/warden.md`, `tests/test_edits_go_through_the_edit_tool.py` only |

## Inherited coordinates

Round 1's coordinates carried and were each opened once. What round 3 inherits,
with the column round 2 asked for — **where to measure**, because two findings
in this work item flipped their answer on measurement point alone:

| From | Coordinate | Where to measure | Why it is still worth opening |
|---|---|---|---|
| r1 f1 | `hooks/commit-review-gate.py:144-147` · `:262-286` | — | The segment scan and where the judgment is assembled. `:151` alone does not reach the rule |
| r2 f1 | `hooks/commit-review-gate.py:148-150` · `_eval_hides_a_commit` at `:176-188` | a body with an `eval` and an expansion character, and one without | The second branch, fail-closed by design |
| r1 f1 | issue #34's eight-line body, in `scratchpad/verify_round1_finding.py` | a **partial patch** body, never a whole file — a whole fixture file is clean and the same experiment on a fragment TRIPS | The measured case the prose must stay true to |
| r2 f5 | `agents/warden.md:162` | **above** the waiver row at `:173`, never below it — quote state flows forward, so a paragraph appended at the end cannot move that row | Where the apostrophe parity is visible at all |
| r2 f4 | `agents/smith.md:43` | whole-file `_hides_a_commit` | The waiver example that trips the file the smith reads as its contract |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the gate should skip a heredoc body being written to a file (issue #34's second checkbox). Round 2 notes it would cover the `eval` branch too | `questions.md` Q1 — out of scope, not judged in either round | the repository owner |
| How to resolve `agents/smith.md:43` tripping its own file — a rider at the coordinate, a change to the example, or leaving it. A waiver example is only useful shown verbatim, so this is a trade rather than a fix | `questions.md` Q2, plus a rider at the coordinate so it reaches whoever opens the line (finding 4) | the repository owner |
| The command string that actually triggered issue #34. Carried from round 1, and no longer load-bearing: the delta-debugged body was reproduced directly | `round-1.md`, and the memo's `## Not verified` | the session that opened issue #34 |

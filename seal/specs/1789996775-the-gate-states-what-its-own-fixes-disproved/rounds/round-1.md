# 1789996775-the-gate-states-what-its-own-fixes-disproved — review round 1

| Field | Value |
|---|---|
| Target SHA | 9948b8af |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 479 |
| Broad gate | 6af8406c against 8531c858 |
| Fixes checked by | no fixes to check |
| Fix range | `9948b8afae53a754d1165e7270dfe297c7a102a2..9948b8afae53a754d1165e7270dfe297c7a102a2`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first round of the work item: the whole branch `release/v0.12.3..9948b8af` — that is `a66e1352..9948b8af`, ten commits — against its own frame, spec compliance before quality. The frame is `spec.md` A1–A8 and §*The correction marker*, `plan.md`'s four phases and §*Alternatives considered*, and `questions.md` Q1–Q4. The work is issues 461, 464 and 465, each read with its *Not this* section, and the earlier reports they cite in work item 1789956662's `rounds/`. The reviewer was given five things the build disclosed about itself and asked to weigh each rather than take it: A6's grep criterion returning two lines where `spec.md` says none; the `seal_stamp.letter` A5 marker sitting after the table rather than beside the row; three of the four A5 markers reading *It is not false, and that is the point* where the fixed template reads *It is false because*; `evidence-check --reverify` re-stamping three ledger rows where A7 counts two; and A2's guard being one `git check-ref-format` call, with the claim that `origin/HEAD` passes that call and never reaches it. A declared divergence is still a divergence, so each was judged rather than accepted. The ledger was read with `evidence_check.py .` unscoped and with no `--reverify`. The broad gate was withheld for the `sealer`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | ⬜ correction — `overview.md` §*Not done* says no `survivors.md` row was written; two were, in the next commit, and `questions.md` Q4, `phases/phase-2.md` and `phases/phase-3.md` all say so | `seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/overview.md#"## Not done"` | answered | Corrected in place at `c4d4bd40` under a `CORRECTED` marker quoting what stood there, with round 1's own measurement of the cause carried into the new paragraph. A prose correction inside a record writes no code for a later round to open, so `Fixes checked by` still reads `no fixes to check`. Read: the paragraph landed at `cfa718ce`, `survivors.md` at `95503f60`. A finding under `seal/specs/` is a correction and not a round (`docs/review-chain-spec.md` §*The last round verifies*), so `Needs a fix` does not count it |
| 2 | ⬜ writing `survivors.md` pushes the survivors it excuses under `FLOOR`, so the arm prints nothing where the skill says it prints `exempt` with the grounds | `skills/code-review/scripts/survivor_check.py#FLOOR` | deferred #308 | Executed over four tree states: 2 places at `f7c9dd39`, 0 at `9948b8af` with and without `--exempt`, 2 again with `survivors.md` removed in a probe commit, and 1 printed as `exempt` with the blockquote elided. Out of scope — issues 461, 464 and 465 do not reach that file and the branch does not touch it |
| 🟢 | A1 and Q2 verified — the docstring states the property the command has | `skills/verify/scripts/broad_gate.py#names_a_branch` | not a defect | Executed on git 2.54.0 in a scratch repository, exit codes read from `returncode`: `@{-1}` exits 0 printing `base`; `HEAD`, `HEAD~1`, `base@{u}`, `topic@{1}` each exit 128 |
| 🟢 | A2 and Q3 verified — the guard is git's own answer, with no string test in the function | `skills/verify/scripts/broad_gate.py#a_runner_could_hold` | not a defect | Executed: `origin/@{-1}`, `origin/HEAD~1`, `origin/base@{u}`, `origin/topic@{1}` exit 1; `origin/base`, `origin/HEAD`, `origin/abc1234`, `origin/release/v0.1.0` exit 0. Issue 461's *Not this* is satisfied |
| 🟢 | A2's case verified not vacuous, and the red reproduces round 2's finding 10 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_the_line_does_not_name_a_ref_a_runners_checkout_cannot_hold` | not a defect | Executed: the guard mutated to `return True` turns that case red alone, at *— not the origin/@{-1} a runner reads —*. Mutation reverted, tree verified clean |
| 🟢 | the `origin/HEAD` claim verified by driving the resolver, not by reading it | `skills/verify/scripts/broad_gate.py#moved_line` | not a defect | Executed: `--base HEAD` and `--base origin/HEAD` both resolve to the ref as given, `Base.moved` is False and the line is None; `--base base` still prints the `CI reads` filling. The Notes cell's mechanism is one link short and is recorded above |
| 🟢 | A6 verified — all three sites say what the branch did, and A3 of the shipped `spec.md` is untouched | `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_a_repository_with_no_remote_at_all_resolves_to_the_ref_as_given` | not a defect | Read the three sites against round 3's finding 15; executed the module at 154 passed with `tests/test_the_seal_is_taken_once_by_the_sealer.py` |
| 🟢 | A6's criterion returns two lines, and leaving round 3's paste-ready text is the right call | `seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/spec.md` | not a defect | The criterion's two halves disagree and the build met the one carrying the claim. Both hits are corrections. The divergence row in `overview.md` is the right home and is written |
| 🟢 | the A5 marker after the table verified — the placement moved, the two fixed properties did not | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md` | not a defect | Read: a comment line between two rows ends the table, three rows sit below the one being corrected, and the marker's first sentence names where it sits and which row it is about |
| 🟢 | the three markers reading *It is not false* verified — the template's slot still carries the grounds with the coordinate | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/overview.md` | not a defect | Read all four markers. The three A4 statements are true, so asserting falsity would add a second false statement to a record being corrected for carrying one |
| 🟢 | A7 verified — three rows marked where A7 counts two, and the third is the right one to mark | `seal/ledger.md` | not a defect | Executed `evidence_check.py .` unscoped: exit 0, 1399 ok, 0 drifted, 0 broken, records arm refuses nothing. `correction-check` over the range reports no dropped correction. Read R4, R5 and G6 for the markers |
| 🟢 | A8 verified — no exit code, verdict or resolution moved beyond A2's one sentence | `skills/verify/scripts/broad_gate.py#panel` | not a defect | Executed 225 cases across six modules, all green; `panel`'s rows and elision are unchanged in source |
| 🟢 | §12 verified — no stale copy of the runner clause outside the past-state records | `agents/sealer.md` | not a defect | Read a tree-wide sweep for the clause and for the printed line's prefix: the only carriers are `broad_gate.py` and the case module, both corrected. `agents/sealer.md` quotes the command, not the line |
| 🟢 | Q1 verified built and not answered | `seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/questions.md` | not a defect | Executed `unverified-check --baseline origin/release/v0.12.3`: four open rows here, exit 0. The row is ⬜, and `seal/follow-up.md` carries the item for the owner |

## Paste-ready fixes

```markdown
**Two `survivors.md` rows were written, and the file is why the check is
now silent.** Phase 3's first removal was too wide, `survivor-check` over
the range reported two standing places at 1.90 and 1.67 against a floor of
1.6, and both were excused with a quote and grounds rather than reworded.
Measured afterwards at `9948b8af`: the same command reports nothing, with
`--exempt` and without it. Removing `survivors.md` in a probe commit brings
both places back. The file's own quotes raise the document frequency of the
phrases it excuses, which is the arithmetic
`skills/code-review/scripts/survivor_check.py` documents for a work item's
`rounds/` records and excludes them for — so the two rows are silenced
rather than printed under `exempt` with their grounds, and a reader of the
step learns nothing. The tool question is a `seal/follow-up.md` row for the
repository owner; the rows and their grounds stand as written.
```

## Executed probes

| What was run | Result |
|---|---|
| `git check-ref-format --branch` over nine spellings in a scratch repository, exit code read from `returncode` | `@{-1}` exit 0 printing `base`; `HEAD`, `HEAD~1`, `base@{u}`, `topic@{1}` exit 128; `base`, `release/v0.1.0`, `abc1234`, `origin/HEAD` exit 0 |
| `git check-ref-format` on the constructed runner label, eight spellings | `origin/@{-1}`, `origin/HEAD~1`, `origin/base@{u}`, `origin/topic@{1}` exit 1; `origin/base`, `origin/HEAD`, `origin/abc1234`, `origin/release/v0.1.0` exit 0 |
| `moved_line` driven against a clone with a remote for `HEAD`, `origin/HEAD`, `@{-1}`, `base`, `HEAD~1` | the first two and the last return None with `moved` False; `@{-1}` prints the no-counterpart filling; `base` prints the `CI reads` filling |
| `a_runner_could_hold` mutated to `return True`, the two new cases re-run | `test_the_line_does_not_name_a_ref_a_runners_checkout_cannot_hold` red alone, reproducing round 2's finding 10 verbatim; mutation reverted, tree clean |
| `bin/test tests/test_the_gate_asks_the_range_ci_will_ask.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q` | 154 passed |
| `bin/test` over `tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py`, `tests/test_the_gate_names_every_step_ci_runs.py`, `tests/test_docs_line_wrap.py` | 71 passed |
| `bin/evidence-check .` unscoped, no `--reverify` | exit 0 · 1399 ok · 0 drifted · 0 broken · records arm 0 refused |
| `bin/correction-check --range origin/release/v0.12.3...HEAD` | exit 0, no merge commit in the range so no correction can have been dropped |
| `bin/unverified-check --baseline origin/release/v0.12.3` | exit 0, four open rows for this work item |
| `bin/survivor-check --range origin/release/v0.12.3...HEAD` at four tree states, with and without `--exempt` | 2 places at `f7c9dd39`; 0 at `9948b8af` either way; 2 with `survivors.md` removed in a probe commit; 1 printed as `exempt` with the blockquote elided. Finding 2 |
| the grep `spec.md` A6 names, over the case module | two lines, `:22` and `:74`, both corrections; the third replacement wraps and is not matched |
| the broad gate — full suite, repository-wide lint, typecheck | not yet — withheld for the `sealer`, which takes it once after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 2 — a `survivors.md` raises the document frequency of the phrases it quotes and pushes its own survivors under `FLOOR`, so the arm prints nothing where the skill promises an `exempt` line with the grounds. The `rounds/` exclusion in the same module is the shape of the repair | **#308**, as a comment carrying the four-tree-state measurement. The reviewer's report sends it to `seal/follow-up.md`; that file already holds the row, and the row itself assigns this half to #308 — *#308 is the CORPUS half, where the same quote joins the pool as a further carrier, raises `df` and drops the score under the floor before `--exempt` is consulted*. A second row would have been the same class tracked twice, so the measurement went to the ticket the existing row names. The comment also says out loud that #308's TITLE reads as the range half, which is what #371 closed, so whoever schedules it decides whether the title moves or the row re-points | the repository owner |

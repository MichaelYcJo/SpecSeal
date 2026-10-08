# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — review round 1

| Field | Value |
|---|---|
| Target SHA | 7e68ed00f83d53a36ffdd6e2347e015b8f0d1168 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 878 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `d2b765876c8ba9e1ef1f8f5b9518767f5c2f718f..27920e587aa2345c12ff9edcc7200d198e874744`, 2 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (CI red on the suite-wide path-list guard) and 🟡 2 (the rule's home states a limit-free guarantee two merge shapes break) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the build at 7e68ed00, against origin/release/v0.21.0. The spawn named six things to attack. First, own_commits on a start that is a merge, a criss-cross merge, a rebase that rewrote the start, a cherry-picked sibling fix and an empty range. Second, whether close's two new refusals fire before any write and whether a legitimate range trips them. Third, the overview's three divergences (own_units' return shape, touched intersecting with paths at b, and -I in call_sites). Fourth, the -z parsing of renames, newlines and the Windows leg. Fifth, the Corrected rows. Sixth, the round's own axes. Facts arrived labelled. Executed by the orchestrator: bin/test over five modules (427 passed) and ruff. Read from the smith: the reds, the mutations, evidence-check, survivor-check, and the measurement of #860's own range. Read: #837 is reviewed at the same time on neighbouring lines, and #877 holds the survivor-check range case.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The S10 case lists paths with `git ls-tree` and is unclassified in the suite-wide path-list guard, so CI fails on ubuntu and on windows group 2 | `tests/test_a_shrunken_corpus_declines_to_judge.py:245` | **fixed** `e6fc73f9` | fixed at e6fc73f9 — the S10 case is classified in `LISTS_A_FIXTURE` with the reason the paste-ready fix gave; `tests/test_a_shrunken_corpus_declines_to_judge.py` 17 passed; executed: CI on PR #878, 2 failed on each leg; reproduced in the clone (exit 1), and green with the paste-ready fix (exit 0, 17 passed) |
| 🟡 2 | The rule's home says a merged-in commit descends from the range's start never; a back-merge makes a sibling's commit owned, and an own commit on a topic forked before the start is not owned, and the limit paragraph names neither | `docs/the-record-layout.md:121` | **fixed** `27920e58` | fixed at 27920e58 — the home's ownership sentence names the squashed sibling it holds for, and its limit paragraph names both shapes the probes measured; the fragment section, `own_commits`' and `fragment_left_behind`'s docstrings, the ledger fragment's S7–S9, S12 and `Corrected · S2, S3, S4, S6` rows, `overview.md` and `phases/phase-1.md` say the same. `changelog.md` is unchanged: none of its sentences states the limit-free claim; executed: probe A owned `S(sibling)`, probe B dropped `topic-fix` and `topic.py`; the same sentence also appears at `docs/the-record-layout.md:101`, in the two docstrings and in two ledger rows |
| ⬜ 3 | `own_units` shows and diffs prose paths that `measure` skips, and `own_commits` runs twice per `close` and per `fix_pass_units` | `skills/code-review/scripts/round_record.py:2384` | answered | a note, left as it stands: a cost, not a wrong answer — `own_units` reads prose files `measure` skips, and `own_commits` runs twice per `close`; read; cost only |
| ⬜ 4 | A `Contract changes` entry can be a sibling's signature change when an own commit changed only the unit's body | `skills/code-review/scripts/round_record.py:4450` | answered | a note, left as it stands: a signature a merged-in sibling changed reaches `Contract changes` only where an own commit also changed that unit, and the row then names a real change in the unit the fix touched; read; the home's sentence is true, its consequence is unstated |
| ⬜ 5 | "It refuses depth 2" now has a document as its antecedent | `skills/code-review/orchestration.md:372` | answered | a note, left as it stands: the sentence at `skills/code-review/orchestration.md:372` reads in its section, where the refusal it names is `close`'s; read |
| 🟢 | `close`'s two new refusals both raise before any cell is written | `skills/code-review/scripts/round_record.py:4370` | confirmed | read: `parse_range` at 4370 and the guard at 4422-4443, with the first write after 4516 |
| 🟢 | The `-z` readers parse hostile names verbatim, and `-I` hides no call site the old split read | `skills/code-review/scripts/round_record.py:3711` | confirmed | executed: probes D and E |

## Paste-ready fixes

```python
    "tests/test_chain_check_at_the_pull_request.py#test_a_clean_copy_in_the_working_tree_cannot_hide_a_committed_failure": 1,
    # #860: `ls-tree` over the fixture's own commit, to assert git quotes the
    # name the case wrote; no path in it is opened.
    "tests/test_the_fixes_close_the_record.py#test_a_path_git_would_quote_is_read_as_the_path_it_is": 1,
}
```
```markdown
**A range `a..b` owns the non-merge commits that descend from `a` and that `b`
reaches** — `git log --ancestry-path --no-merges a..b`. A sibling's commit
that a merge of the base brought in reaches `b` only through the merge, and
in a repository that squashes into its base it descends from `a` never, so it
is not owned, whichever side the merge was made from. Two readers walked a
```
```markdown
What no reader can see is a change made only inside a merge's conflict
resolution. The merge is owned by no range, so `close` refuses a `fixed` row
that names it. Descent is the whole test, so two shapes read against the
item's history. Where the base merged any of the item's commits with a merge
commit (a back-merge, or a stacked branch merged first), every commit made on
the base after that merge descends from `a` and is owned. And an own commit on
a topic forked before `a` descends from it never and is not owned, so its
units leave the surface and a `fixed` row naming it is refused. A range whose
start does not reach its end owns nothing, and `close` refuses it rather than
writing an empty surface.
```
```markdown
checkout, the pull request merged into its base, reads the same commits as the
branch does, because a squash on the base descends from round 1's target never
(the next section names the merge shape where that fails).
```

## Executed probes

| What was run | Result |
|---|---|
| `test_tmp_probe.py`, case A: back-merge, then a sibling on the base, then the branch merges the base; `own_commits(T, HEAD)` — NAME NOT IN TREE | `['f1', 'S(sibling)', 'f2']` — the sibling is owned |
| case B: own fix on a topic forked before `T`, merged after; `own_commits` and `touched` | `['f']` and `['own.py']` — the topic's fix and `topic.py` are absent |
| case C: start is a merge; range `a..a` | `['f']`; `[]` |
| case D: names holding a newline, a leading newline, a leading `\x01`, a `:`, `ï`; an empty commit; a move and a delete | every path verbatim; empty commit `[]`; move read as `D` + `A`; `tracked_at` holds all of them |
| case E: `call_sites` with a newline-named caller, a file with a NUL after 8000 bytes, and a `.py` marked `binary` | `['late_nul.txt', 'caller', 'odd_caller', 'zz_caller']`; with the attribute, `zz_caller` gone, and plain `git grep` printed `Binary file … zz.py matches` — NAME NOT IN TREE |
| `bin/test tests/test_a_shrunken_corpus_declines_to_judge.py` at the target SHA | exit 1, 2 failed, 15 passed |
| the same, with 🔴 1's fix applied in the clone (then reverted) | exit 0, 17 passed |
| PR #878 CI, read with `gh pr checks` and the job logs | ubuntu: fail (2 failed, 12758 passed); windows group 1: pass (2738 passed); windows group 2: fail (the same 2); windows group 3: pass (1038 passed); windows group 4: pass (2149 passed, 66 skipped); macOS: still running when this report was written. No Windows shard failed a case of the changed modules, and the S10 case carries no skip marker, so `questions.md` Q3 is answered (a) by CI on git 2.55.0.windows.5 |
| broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

# 1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches — review round 1

| Field | Value |
|---|---|
| Target SHA | 71e4b3a3496bb9d3505692fc569852aa0d43c172 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #855 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of #854's review run, at 71e4b3a3, the head of draft PR #855, over `origin/release/v0.20.0...HEAD` from 3d78c220. The frame is round 3 of work item 1791270162.

The reviewer was asked:
- whether the fix closes the class: every way git ends option parsing and every long-option prefix git accepts for `rebase`, against the installed git, including options taking a value and short-option clusters;
- whether the git-binding case's new coverage is portable to the CI gits;
- whether the in-place re-stamps of 1791270162's fragment rows are faithful;
- to read every workflow of `gh pr checks 855`.

It did not run the full suite.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | brace expansion hands git words the guard reads as one: `git rebase {main,feature/x}` and `git rebase --ro{,} feature/x` switch HEAD and are silent in an ACTIVE tree | `hooks/worktree-guard.py:2250` | deferred a new issue | executed under git 2.50.1 and bash; silent at the base too, so not a regression; the same gap reaches `stash` and `worktree` (read), so the fix is the guard's word reading and outside this item's frame |
| ⬜ 2 | the docstring and R1 say `--root` is read off the words bash hands git, and the code reads them only once redirections are off | `hooks/worktree-guard.py:2246` | open | read; the phrase is false for a brace-expanded word (finding 1); wording only |
| ⬜ 3 | the changelog fragment says every other option passes, and a one-word rebase with an option taking a value stops | `seal/specs/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches/changelog.md:12` | open | executed: `-X theirs main`, `-s ort main` and `-ix true main` deny in an ACTIVE tree, as at the base; a paperwork correction, not counted in `Needs a fix` |
| 🟢 | round 3's finding 1 of work item 1791270162 is closed — `--end-of-options` and every prefix of `--root` git accepts are read | `hooks/worktree-guard.py:2257` | confirmed | executed: 29 spellings under git 2.50.1, every switch denies but the two brace rows; the new rebase rows and the git-binding case red at `3d78c220`, green here |
| 🟢 | round 3's note 2 of work item 1791270162 is closed — §A says a one-tree reason calls its tree "this tree" | `docs/worktree-guard-spec.md:102` | confirmed | read; the policy pin red at `3d78c220` (executed) |
| 🟢 | round 3's note 3 of work item 1791270162 is closed — §Known limits names `cd w 2>&1` and a cut git in an `if` body | `docs/worktree-guard-spec.md:807` | confirmed | read; the policy pin red at `3d78c220` (executed) |
| 🟢 | the in-place re-stamps of 1791270162's fragment change hashes only, and each claim holds at the new content | `seal/ledger/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest.md` | confirmed | executed: word diff shows hashes only; `evidence-check --strict --ledger` 127 ok at the base and at the head; read: each claim against the changed text |
| 🟢 | the git-binding case's new forms run on the CI gits | `tests/test_worktree_guard.py:2008` | confirmed | read from CI at 71e4b3a3: passed on Ubuntu and macOS (git 2.55.0) and on Windows (git 2.55.0.windows.5, shard 4, 16.46 s against a 90 s ceiling); passes here under git 2.50.1 (executed) |
| 🟢 | every workflow of #855 at 71e4b3a3 passed | `gh pr checks 855` | confirmed | read: `lint`, `ledger`, both `arm-check-grammar` legs, `release`, Ubuntu, macOS and Windows shards 1 to 4 |

## Paste-ready fixes

```python
# hooks/worktree-guard.py, _rebase_names_a_branch, the docstring's third
# paragraph, from "refuses it." on:
    refuses it. `--root` is the one option of `git rebase -h` that changes how
    many words name a branch, and it is read off the words once their
    redirections are off, so `--root>/dev/null` is `--root` too. An option
    taking a value counts its value as a word, as above (git 2.50.1; #854,
    round 3 of work item 1791270162, yellow 1)."""
```
```markdown
seal/ledger/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches.md,
row R1's claim: "off the words bash hands git" becomes
"off the words once their redirections are off"
```
```markdown
seal/specs/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches/changelog.md,
the paragraph's last sentence becomes:

  A rebase of the branch HEAD is on still passes, and so does one carrying
  `--rebase-merges` or another option that takes no value.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py tests/test_docs_line_wrap.py -q --durations=5` in this round's clone at 71e4b3a3 | 288 passed in 7.32 s; `test_no_listed_form_moves_head_under_git` 3.04 s |
| the head's two guard test modules copied into a clone at `3d78c220`, then `bin/test … -k "rebase or listed_form or one_tree_reason or guard_policy_says or cannot_place"` | 8 failed, 36 passed: the five new switching rebase rows, the git-binding case naming exactly `rebase --end-of-options {start} -x` and `rebase --ro feature/x`, and both policy pins. The new listed rows, the one-tree case and the two `UNPLACED` rows pass at the base, as they pin behaviour the base already had; the smith showed each red through `bin/mutation-check` (not rerun here) |
| a deleted probe running 29 rebase spellings under bash and git 2.50.1 in copies of the `repo` fixture, and through the build's and the base's `main()` in an ACTIVE tree | the class table above |
| `bin/evidence-check --strict --ledger <file> .` on 1791270162's fragment and this item's at the head, on 1791270162's at `3d78c220`, and on `seal/releases/0.17.0.md`, `0.18.0.md`, `0.18.2.md`, `0.18.3.md` and the broad-gate fragment at the head | every run exit 0, 0 drifted, 0 broken |
| `git diff --word-diff=porcelain 3d78c220 71e4b3a3` of 1791270162's fragment | hash tokens only |
| `gh pr checks 855` until every leg ended, and the logs of the Ubuntu, macOS and four Windows `pytest` jobs (`gh api …/actions/jobs/<id>/logs`) | every leg passed; git versions and the case's 16.46 s on Windows shard 4, in the CI section above |
| this report copied into the scratch clone, then `bin/evidence-check --strict --ledger` on this item's fragment, `bin/test tests/test_no_real_identifiers.py -q`, and `round_record.py new` with the report as its input | exit 0, nothing refused; 5 passed; the record parsed, with `Needs a fix` and `Loses a record or crashes` both `no`. The clone, and the record written in it, were deleted |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. This report opens nothing that needs a fix, so it comes due now |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — brace expansion hands git words the guard reads as one, in `rebase`, `stash` and `worktree` alike | candidate home: a new issue against the worktree guard's word reading | the orchestrator opens it, and the repository owner decides whether the guard reads brace expansion or names it in §*Known limits* |

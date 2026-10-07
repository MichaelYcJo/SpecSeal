# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — review round 3

| Field | Value |
|---|---|
| Target SHA | 2c3a7f920204672160299f8ee2026655cdc70282 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #850 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | second — 🟡 1 at hooks/worktree-guard.py#_rebase_names_a_branch, a unit round-2's fixes changed; the fix passes stop here and the work item goes back to its framer |
| Needs a fix | yes — 🟡 1: `git rebase --ro <branch>` and `git rebase --end-of-options <upstream> <branch>` switch HEAD and are listed, so each is silent in an ACTIVE tree |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 of #826 is the verifying round for round 2's fixes at `3c9a1161..a3164380`, reviewed at 2c3a7f92. It is also the review run's last record: round 2 was the run's first fix of a fix, and the reopening is spent.

The reviewer was asked to open each fix, and to treat round 2's `New units` as a finding surface. In particular it judged:
- `_merged_findings`' new return shape and `main`'s placement by the cut's first part;
- the per-tree stop reason in English and Korean;
- the rebase revision spellings;
- the base behaviour of the seven no-`cd` cut rows;
- the two survivors the smith called equivalent.

It also read every workflow of `gh pr checks 850`, and it did not run the full suite.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_rebase_names_a_branch` ends the options only at `--` and reads `--root` by exact match, so `git rebase --ro feature/x` and `git rebase --end-of-options main -x`, which git runs as a switch, are listed and silent in an ACTIVE tree | `hooks/worktree-guard.py:2245` | open | executed: git 2.50.1 moved HEAD in both; the build, `3c9a1161` and the base silent in an ACTIVE tree; the trial fix denies both and the 21 rebase and git-binding cases pass; a fix of a fix in a unit round 2's fixes changed, home candidate the frame |
| ⬜ 2 | §A says the stop's reason names each tree that matters, and a one-tree reason names none: `git -C W checkout feature/x` with only `W` dirty asks about "this tree" | `docs/worktree-guard-spec.md:97` | open | executed; the text predates round 2 and the decision is right |
| ⬜ 3 | §Known limits' bullet on a tree the guard cannot place names neither `cd W 2>&1 && git switch x` nor a cut git in an `if` body after `cd W`, and both are silent with `W` ACTIVE | `docs/worktree-guard-spec.md:793` | open | executed against the build, `3c9a1161` and the base; the base's ask on the `if` rows was tree-blind (it asked with `W` clean); the behaviour is the owner's rule of 2026-10-03 |
| ⬜ 4 | a carried closure quotes the earlier finding's red glyph in its Grounds beside `confirmed`, so `release` fails at 2c3a7f92 | `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/rounds/round-2.md:42` | open | executed: `chain_check.py` fails on that line, and passes it with the cell corrected; a paperwork correction, not counted in `Needs a fix` |
| 🟢 | round 2's blocking finding 1 is closed for the lone `-` and every word after `--` | `hooks/worktree-guard.py:2245` | confirmed | executed: `git rebase - feature/x` denies in an ACTIVE tree, silent at `3c9a1161` and the base; the rebase cases pass; two further spellings are this round's finding 1 |
| 🟢 | round 2's blocking finding 2 is closed — a cut git is placed by its first part and its glued words | `hooks/worktree-guard.py:2996` | confirmed | executed: the seven rows of `CUT_GROUPS` without a `cd` ask with `W` dirty and deny with `W` ACTIVE, all silent at `3c9a1161`; the base asked on five and was silent on the two `stash` rows |
| 🟢 | round 2's finding 3 is closed — a broken reader places a cut by the part before it | `hooks/worktree-guard.py:2422` | confirmed | executed through the new case in both broken modes |
| 🟢 | round 2's finding 4 is closed — the reason names each tree that matters, or the ACTIVE ones | `hooks/worktree-guard.py:2765` | confirmed | executed: two ACTIVE trees each named in the deny; an IDLE `W` beside a dirty session tree named in Korean; `TREES_EN` and `TREES_KO` match the output |
| 🟢 | round 2's note 5 is closed — the git-binding case asserts each exit code | `tests/test_worktree_guard.py:1959` | confirmed | read; the case passes under git 2.50.1 (executed) |
| 🟢 | round 2's note 6 is closed — `spec.md` gives the current signature | `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/spec.md:322` | confirmed | read |
| 🟢 | the two equivalent survivors are equivalent: `index - 1` in `_cut_unread`, and `>&` left out of `_OPERATORS` | `hooks/worktree-guard.py:2422` | confirmed | executed: the walk gave both parts of every cut the same first directory over six commands, an `if` body included; four spaced `>&` and `<&` rows reach the guard glued and deny |
| 🟢 | round 2's question on the git-binding case's Windows cost is answered | `tests/test_worktree_guard.py:1959` | confirmed | read from CI's logs: 7.41 s on Windows shard 4 at 2c3a7f92 (job 112563064324), and in no Windows shard's 50 slowest at 274e29bb (run 37546586846), against a 90 s ceiling |
| 🟢 | every pytest workflow of #850 at 2c3a7f92 passed | `gh pr checks 850` | confirmed | read: Ubuntu, macOS and Windows shards 1 to 4 passed, with `lint`, `ledger` and both `arm-check-grammar` legs; `release` failed, which is finding 4 |

## Paste-ready fixes

```python
# hooks/worktree-guard.py, _rebase_names_a_branch, the body:
    words = _plain_words(args)
    end = next(
        (i for i, w in enumerate(words) if w in ("--", "--end-of-options")),
        len(words),
    )
    plain = [w for w in words[:end] if w == "-" or not w.startswith("-")]
    plain += words[end + 1 :]
    # git takes any unambiguous prefix of a long option, so `--ro` is
    # `--root` (git 2.50.1; round 3 of work item 1791270162).
    root = any(w.startswith("--r") and "--root".startswith(w) for w in words[:end])
    return len(plain) >= (1 if root else 2)
```
```python
# tests/test_worktree_guard.py, test_a_rebase_naming_a_branch_is_unrecognised:
# two more parameters.
        "git rebase --ro feature/x",
        "git rebase --end-of-options main -x",

# test_a_rebase_of_the_current_branch_stays_listed: one more.
        "git rebase --rebase-merges main",

# SWITCHING: one more form.
    "rebase --ro feature/x",
```
```markdown
docs/worktree-guard-spec.md §A, the rebase sentence's last clause becomes:

A lone `-` is a word, since git reads it as `@{-1}`, and so is every word
after a `--` or an `--end-of-options`: `git rebase - feature/x` switches
too. git takes a prefix of `--root` (`--ro`) as `--root`, and so does the
guard.
```
```markdown
docs/worktree-guard-spec.md §A, the sentence at line 97 becomes:

The stop's reason names each tree that matters and why, its changes, its
IDLE sessions or its detection unusable, because approving the `ask` runs
the line in every one of them; a reason that describes one tree calls it
"this tree", and where one is ACTIVE, the reason describes the ACTIVE trees
alone.
```
```markdown
docs/worktree-guard-spec.md §Known limits, the bullet at line 793, after
"`cd "$W"` with `W` unset, and `2>&1 cd w`":

, and `cd w 2>&1`, whose `&` the frozen splitter cuts so the walk keeps
the directory before the `cd` first. An unrecognised shape the walk cannot
place takes the same fallback: a cut git inside an `if` body after `cd w`
(`cd w && if …; then 2>&1 git switch x; fi`) is judged in the session's
own tree, where the guard before #826 asked in every tree.
```
```markdown
seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/rounds/round-2.md:42,
the Grounds cell ends:

executed through the new cases; the lone `-` is red 1 of this round
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py -q --durations=6` in this round's clone at 2c3a7f92 | 235 passed in 5.41 s; `test_no_listed_form_moves_head_under_git` 2.37 s, `test_a_cut_group_is_judged_in_the_tree_its_own_c_names` 1.30 s |
| a deleted probe loading the build's guard, `3c9a1161`'s and the base's (`git show` of each, kept outside `hooks/`; the readers they import are unchanged since `86cbd9a2`), with `sessions_in_tree` stubbed per tree | the `CUT_GROUPS` table; the ⬜ 3 table; the reason texts in both languages; the first directories of both parts of each cut; the spaced `>&` and `<&` rows |
| the same probe driving git 2.50.1 and bash in copies of the `repo` fixture | the 🟡 1 table; `cd W 2>&1 && pwd` and `cd W &>/dev/null && pwd` print `W` |
| 🟡 1's fix applied in the clone, the probe rerun, then `bin/test tests/test_worktree_guard.py -q -k "rebase or listed_form or carries_its_counts"` | both spellings deny; 21 passed. The clone was reverted |
| `chain_check.py --baseline origin/release/v0.20.0` in the clone, at 2c3a7f92 and again with row 42's cell corrected and committed there | line 42 refused, then not refused; the other refusals it printed are those of a ready pull request, which a draft only notices. The clone was reset to 2c3a7f92 |
| `gh pr checks 850`, read until the last leg ended, and the failed `release` job's log | `release` failed on `round-2.md:42`; `lint`, `ledger`, both `arm-check-grammar` legs, Ubuntu, macOS and Windows shards 1 to 4 passed. The scratch clone and the probe were deleted afterwards |
| the four Windows jobs' logs at 2c3a7f92 (`gh api …/actions/jobs/<id>/logs`) | 2686, 6731, 915 and 2227 passed; `test_no_listed_form_moves_head_under_git` 7.41 s on shard 4 |
| `gh run view 37546586846 --log`, the `tests` run at 274e29bb | every leg succeeded; the git-binding case was in no shard's 50 slowest |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. This record ends the run, so it comes due once the orchestrator has taken 🟡 1 to its home |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:2699` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/worktree-guard.py:2161` | round 1's 🔴 2 — fixed |
| round-1 | `hooks/worktree-guard.py:2086` | round 1's 🔴 3 — fixed |
| round-1 | `hooks/worktree-guard.py:2321` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/worktree-guard.py:2397` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/worktree-guard.py:157` | round 1's ⬜ 6 — fixed |
| round-1 | `hooks/worktree-guard.py:2056` | round 1's ⬜ 7 — fixed |
| round-1 | `hooks/worktree-guard.py:2878` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` | round 1's 🟢 — confirmed |
| round-1 | `docs/worktree-guard-spec.md` | round 1's 🟢 — confirmed |
| round-1 | `gh pr checks 850` | round 1's ❓ — out of verified scope |
| round-2 | `hooks/worktree-guard.py:2235` | round 2's 🔴 1 — fixed |
| round-2 | `hooks/worktree-guard.py:2941` | round 2's 🔴 2 — fixed |
| round-2 | `hooks/worktree-guard.py:2393` | round 2's 🟡 3 — fixed |
| round-2 | `hooks/worktree-guard.py:2981` | round 2's 🟡 4 — fixed |
| round-2 | `tests/test_worktree_guard.py:1772` | round 2's ⬜ 5 — fixed |
| round-2 | `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/spec.md:312` | round 2's ⬜ 6 — answered |
| round-2 | `hooks/worktree-guard.py:2775` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2155` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2226` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2383` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2971` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — `git rebase --ro <branch>` and `--end-of-options` are listed | candidate home: the frame, as the run's second fix of a fix (`skills/code-review/orchestration.md` §*A fix of a fix twice sends the work item back to its framer*); the orchestrator applies the count | the framer, re-spawned with the run's round records, or the orchestrator where it reads the count otherwise |
| P5 — whether an unrecognised shape in an ACTIVE tree is denied whatever the press | `questions.md` P5, already deferred in round 1 | the repository owner, at the pull request |

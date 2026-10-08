# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — review round 4

| Field | Value |
|---|---|
| Target SHA | e0e01532f64d65e286a9009e655e4bcc4272a8da |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 878 |
| Broad gate | not yet |
| Fixes checked by | round-5 |
| Fix range | `6445933a4845ccba449c37bf636df539b403ea3f..76de29c33fced53ec0b798f32f97a6c855c187bc`, 2 commits |
| Contract changes | none |
| New units | test_a_sentence_linking_the_home_uses_no_listed_word (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1 (the home says every reader of a range imports `own_commits`, and the `Fix range` count and the notice's clearing step do not) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 4, the redesign's first finding round after the reframe of round 3. Its target is a15c4057..e0e01532, phases 5 to 7: the shapes as test cases, the texts pointing at one owner sentence, and the records restated. Rounds 1 to 3's coordinates were inherited, and round 3's four deferred findings were the agenda. The spawn named six things to judge. First, whether the owner sentence equals what own_commits runs. Second, whether any carrier still defines rather than points. Third, whether the guard can be passed by a false sentence or refuses a true one. Fourth, whether every shape case can fail. Fifth, whether the head_ref change is a contract change and safe where CI sets nothing. Sixth, whether the restated ledger rows and the changelog are true. It also ran the eight guard modules once. Facts arrived labelled. Read from the smith: the shape module, the guard, 531 passed, survivor-check and evidence-check at exit 0.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The home says every reader of a range in the two scripts imports `own_commits`; the `Fix range` count on both sides and the notice's clearing step read the range with their own `rev-list`, and the same section says the count reads it another way | `docs/the-record-layout.md:125` | **fixed** `f2d7d9ab` | fixed at f2d7d9ab — the home's clause "and every reader of a range in `round-record` and `chain-check` imports it" is dropped, as the paste-ready block does, and nothing replaces it; read: `round_record.py:4503`, `chain_check.py:1992`, `chain_check.py:4623`, and the section's fourth paragraph |
| ⬜ 2 | The owner sentence's gloss, "a non-merge commit that has `a` as an ancestor and that `b` reaches", includes `a` under git's reflexive ancestry, which the git command never lists | `docs/the-record-layout.md:122` | **fixed** `f2d7d9ab` | fixed at f2d7d9ab — the owner sentence is the git command alone, without the gloss that included `a`; rule 17 pins the shorter sentence; executed: `merge-base --is-ancestor T T` exits 0, `own_commits(T, HEAD)` omits `T`; read: `parse_range` uses the reflexive test |
| ⬜ 3 | The guard's docstring says it keeps shapes out of the prose; three false sentences outside its list pass it, and it refused a true docstring row because it reads the four docstrings whole | `tests/test_the_range_rule_states_no_shape.py:10` | **fixed** `f2d7d9ab` | fixed at f2d7d9ab — the guard's docstring says it is a word list: a shape stated in other words passes it, a true sentence that needs a listed word is refused, and review is what keeps shapes out; executed: three pastes into the home, 7 passed each; the restored "squashed away" row turns the docstring case red |
| ⬜ 4 | The silent-state row the guard forced says round 1's target is gone once its branch merged; a merge commit keeps it, and the replaced "squashed away" was true | `skills/code-review/scripts/chain_check.py#fragment_left_behind` | **fixed** `f2d7d9ab` | fixed at f2d7d9ab — the silent-state row says "squashed away" again, and the guard reads the home's section and every sentence linking the home, each of the four docstrings through its own linking sentence; the same two checks remain, over a narrower text; read: `chain_check.py:4585`, `phases/phase-6.md` naming the rewording; behaviour unchanged |
| ⬜ 5 | The fragment section's input sentence adds "which a branch checkout that has not merged the base does not hold", a shape clause outside the guard, and in #805's rebuilt history the branch holds those commits without merging the base | `docs/the-record-layout.md:102` | **fixed** `f2d7d9ab` | fixed at f2d7d9ab — the fragment section's input sentence drops "which a branch checkout that has not merged the base does not hold", as the paste-ready block does; executed: the rebuilt branch and the merge ref both give `['S', 'f1', 'f2']`; true under the `git branch --merged` reading |
| 🟢 | round 3's finding 1 is closed — the fragment section states the notice's input instead of an equality, and S17's case pins both checkouts | `docs/the-record-layout.md:100` | confirmed | executed: the case is red with `--first-parent` added; read: the equality sentence is gone |
| 🟢 | round 3's finding 2 is closed — the home states no example, and the shapes are cases | `tests/test_a_range_owns_what_git_lists_for_it.py` | confirmed | executed: the module passes, and every case is red under one of the two mutations |
| 🟢 | round 3's finding 3 is closed — the `own_commits` docstring names the git command, the home and the shape module | `skills/code-review/scripts/chain_check.py#own_commits` | confirmed | read: the docstring; the guard's docstring case for it passes (executed) |
| 🟢 | round 3's note 4 is closed — the corrected ledger row and the phase 1 correction are restated in the owner's terms | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:4` | confirmed | read against the owner sentence; one #805 clause remains and is true by definition; `evidence-check --strict` exit 0 (executed) |
| 🟢 | the `head_ref` argument is a test helper's, defaulted, and mirrors the workflow's `GITHUB_HEAD_REF`; no shipped interface changed | `tests/test_a_fragment_left_behind_is_named.py:181` | confirmed | read: the two scripts' diff is docstrings only; `chain_check.py:1350` reads the same variable |
| 🟢 | the changelog fragment is true against the owner sentence | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:27` | confirmed | read; its CI sentence carries no shape clause |
| ❓ | whether `close` over the redesign's range lists `check` and `judged` under `Contract changes` | `tests/test_a_fragment_left_behind_is_named.py#check` | ❓ out of verified scope | not run this round; the orchestrator answers it when it runs `close` |

## Paste-ready fixes

```markdown
**A range `a..b` owns exactly the commits `git log --ancestry-path
--no-merges a..b` lists: a non-merge commit that has `a` as an ancestor and
that `b` reaches.** That is the whole test `chain_check.py#own_commits` runs.
It does not read which parent of a merge a commit sits behind, which branch
the commit was made on, or when it was made. Whether a given commit of a
given history is owned is answered by running `own_commits` on that history.
```
```markdown
**A range `a..b` owns exactly the commits `git log --ancestry-path
--no-merges a..b` lists: a non-merge commit other than `a` that has `a` as
an ancestor and that `b` reaches.** That is the whole test
`chain_check.py#own_commits` runs.
```
```python
        "A range `a..b` owns exactly the commits `git log --ancestry-path "
        "--no-merges a..b` lists: a non-merge commit other than `a` that has "
        "`a` as an ancestor and that `b` reaches.",
```
```python
the second fix of a fix. The reframe moved every shape into
`tests/test_a_range_owns_what_git_lists_for_it.py` as a case, and this module
refuses, in the home's section, the docstrings of the four units that read a
range, and every sentence that links the home, the vocabulary those false
examples used. It is a word list and not a reader of meaning: a shape stated
in other words passes it, and a true sentence that needs a listed word is
refused. What keeps a shape out of the prose is the rule in the home and
review; this module keeps the sentences the rounds found from coming back.
```
```text
      round 1's target           not fetched into this clone, or left out
      unresolvable, or not an    of HEAD's history when its branch merged
      ancestor of HEAD           as one new commit, or off the branch after
                                 a rebase. Walking `<target>..HEAD` from a
                                 commit HEAD does not descend from reads the
                                 build itself as late
```
```markdown
move lists both its paths, so a file moved under `tests/` is named. The
notice reads `<round 1's Target SHA>..HEAD` wherever it runs. On CI's
checkout HEAD is the pull request merged into its base, so there the range
also holds every base commit that has round 1's target as an ancestor, and
CI can name a commit a branch checkout does not.
```

## Executed probes

| What was run | Result |
|---|---|
| a `--no-local` clone of the worktree at e0e01532, in the round's scratch directory | HEAD e0e01532f64d65e286a9009e655e4bcc4272a8da |
| `bin/test` over the eight guard modules the spawn named | exit 0; 435 passed |
| `bin/test` over the shape module, the guard module, the fragment module and the one-owner module | exit 0; 112 passed |
| `test_tmp_round4.py` in the round's scratch directory, run once and deleted — NAME NOT IN TREE | exit 0; results in the rows below |
| `own_commits` with `--ancestry-path` dropped, over the shape module and S17's case | 4 red: A2, B, B3, C |
| `own_commits` with `--first-parent` added, over the same | 4 red: A, B2, D, and S17's fragment case |
| three false sentences pasted one at a time into the home's section, then the guard module | green each time, 7 passed |
| the "squashed away" row restored in the `fragment_left_behind` docstring, then the guard module | 1 failed: the `fragment_left_behind` docstring case |
| `git merge-base --is-ancestor T T`; `own_commits(T, T)`; whether `own_commits(T, HEAD)` lists `T` | exit 0; `[]`; not listed |
| #805's rebuilt history after the base merged `T`: the branch, and the merge ref | `['S', 'f1', 'f2']` on both |
| `bin/evidence-check --strict` in the clone | exit 0 |
| `bin/survivor-check --range a15c4057..e0e01532 --exempt` the item's `survivors.md`, in the clone | exit 0; 12 survivors excused |
| `gh pr checks 878`, read three times, the last after this report was written | head e0e01532: 8 pass, 5 pending, none failed; at the second read the passes were release, lint, ledger, both arm-check-grammar legs, the Ubuntu leg and macOS shard 1, and the pending were macOS shards 2–3 and Windows shards 1–4 |
| broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle; never run in this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_shrunken_corpus_declines_to_judge.py:245` | round 1's 🔴 1 — fixed |
| round-1 | `docs/the-record-layout.md:121` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2384` | round 1's ⬜ 3 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:4450` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/orchestration.md:372` | round 1's ⬜ 5 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:4370` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py:3711` | round 1's 🟢 — confirmed |
| round-2 | `docs/the-record-layout.md:148`, `skills/code-review/scripts/chain_check.py#own_commits` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/orchestration.md:370` | round 2's 🟡 2 — fixed |
| round-2 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:13` | round 2's ⬜ 3 — answered |
| round-2 | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:11` | round 2's ⬜ 4 — answered |
| round-2 | `tests/test_a_shrunken_corpus_declines_to_judge.py:248` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/round_record.py:2402` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md:70` | round 2's 🟢 — confirmed |
| round-3 | `docs/the-record-layout.md:99` | round 3's 🟡 1 — deferred |
| round-3 | `docs/the-record-layout.md:126` | round 3's 🟡 2 — deferred |
| round-3 | `skills/code-review/scripts/chain_check.py#own_commits` | round 3's 🟡 3 — deferred |
| round-3 | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:4` | round 3's ⬜ 4 — deferred |
| round-3 | `docs/the-record-layout.md:150` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:7` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/survivors.md:27` | round 3's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

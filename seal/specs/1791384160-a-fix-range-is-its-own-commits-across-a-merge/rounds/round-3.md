# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — review round 3

| Field | Value |
|---|---|
| Target SHA | 4cf41ee400920a3424fea5b6e78b46fffefa8ce0 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 878 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | second — 🟡 3 at skills/code-review/scripts/chain_check.py#own_commits, a unit round-2's fixes changed; the fix passes stop here and the work item goes back to its framer |
| Needs a fix | yes — 🟡 1 (the fragment section says CI reads the same commits as the branch, false after a back-merge), 🟡 2 (two of the home's examples are false in shapes C and B3) and 🟡 3 (the own_commits docstring carries the B3 example, a fix of a fix) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 3 of round 2's fixes: 24cfb66f..fadd8270 (fb5ba994 fix, fadd8270 record corrections), plus 1b595fa4 and the close at 4cf41ee4. It was announced as the run's last record, since the one reopening was spent. The job was the answers to round 2's four verdicts; round 2's New units read none. The spawn asked three things: whether each carrier's sentence is true of own_commits as written, re-running probes A, A2, B and B2; whether the git grep for the claim's phrases missed any shipped coordinate; and whether the corrected ledger rows are true. Facts arrived labelled. Executed by the orchestrator: survivor-check at exit 0, 589 passed over the guard and record modules, and the close (2 fixed, 2 answered). Read from the smith: the ancestry wording, the pinned refusal words, and the spec.md sentences excused in survivors.md.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The fragment section says CI's merge ref reads the same commits as the branch; after a back-merge of the target into the base, CI also owns the base's commits made on top of it, and the fix removed the hedge that said so | `docs/the-record-layout.md:99` | open | executed: probe D, the branch gives `['f2']` and CI's merge ref `['S(sibling)', 'f2']` |
| 🟡 2 | The home's examples are phrased by time and topic state; a sibling's commit made after the base merged `a` on a branch forked before that merge is not owned, and a topic fix made before the topic merged `a` is not owned once it has | `docs/the-record-layout.md:126` | open | executed: probe C gives `['f2']`, probe B3 gives `[]` |
| 🟡 3 | The `own_commits` docstring says an own fix on a topic forked before `a` is owned once that topic has merged `a`; probe B3 is the counterexample | `skills/code-review/scripts/chain_check.py#own_commits` | open | executed: probe B3 gives `[]`; read: fb5ba994 wrote the sentence, inside a unit round 2's range changed |
| ⬜ 4 | The ledger row `Corrected · S1, S5, S8, S10` still says the branch and CI read the same commits and a sibling's squash is named on neither side; `phases/phase-1.md` carries the B3 example | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:4` | open | executed: probes A and D; read: fadd8270 moved the row's anchors and left its claim; a correction, since the files are under `seal/` |
| 🟢 | round 2's finding 1 is closed — the limit sentences round 2 measured as wider than the code are gone, and the home states the ancestry test | `docs/the-record-layout.md:150` | confirmed | executed: probes A2 and B2 re-run at 4cf41ee4 give `['f2']` and `['topic-fix']`, matching the new examples; the class continues as this round's findings 2 and 3 |
| 🟢 | round 2's finding 2 is closed — the four carriers state the ancestry test, and the refusal's new words are pinned | `skills/code-review/orchestration.md:370` | confirmed | read: the four sentences and the S6 assertion; executed: probes A, A2, B2, B3 and C agree with each sentence |
| 🟢 | round 2's note 3 is closed — the changelog fragment states the ancestry rule | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:7` | confirmed | read against probes A and B3 |
| 🟢 | round 2's note 4 is closed at the rows it named | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:11` | confirmed | read; CI's ledger job passed at 4cf41ee4; one unlisted row is this round's note 4 |
| 🟢 | the two `spec.md` sentences excused in `survivors.md` are the framer's and the convention holds | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/survivors.md:27` | confirmed | executed: `survivor-check` over `24cfb66f..fadd8270` with the exemption file, exit 0; read: round 2's convention |

## Paste-ready fixes

```markdown
move lists both its paths, so a file moved under `tests/` is named. CI's
checkout, the pull request merged into its base, reads every commit the branch
reads, because the walk asks each commit's ancestry and never which parent of
a merge it sits behind. Where the base merged round 1's target, CI also reads
the base's commits made on top of it that the branch has not merged yet, so
CI can name a commit a branch checkout does not (the next section says which
commits that ancestry makes the item's own).
```
```markdown
For example, a sibling's squash on a base that never merged `a` is not owned.
A sibling's commit made on the base after the base merged `a` is owned, and
one made on a branch forked from the base before that merge is not. On a
topic forked before `a`, a fix made after the topic merged `a` is owned, and
a fix made before that merge is not, even once the topic has merged `a`. Two
readers walked a
```
```python
    `git merge` set is not read. Ancestry alone decides, so a commit a merge
    brought in counts exactly when it was made on top of `a`: a sibling's
    squash on a base that never merged `a` is not owned, and on a topic
    forked before `a` a fix made after the topic merged `a` is owned, while
    one made before that merge is not. A start that does not reach its end
    owns nothing, and the answer is `[]`.
```
```text
— with no reading of a merge's parent order, so a sibling's squash on a base
that never merged the target is named on neither side of a merge, a merge made
from the base's side below HEAD included (#805); CI's merge of the pull
request into its base reads every commit a branch checkout reads, and also
the base's commits made on top of the target that the branch has not merged —
```
```text
code, because the back-merge must merge the start or a commit after it, and
a fix on a topic forked before the start is owned only when it was made after
the topic merged the start.
```

## Executed probes

| What was run | Result |
|---|---|
| `test_tmp_probe.py` in the round's scratch directory, against the clone at 4cf41ee4 — NAME NOT IN TREE | exit 0; seven repositories, results below |
| case A, round 1's back-merge after `T`; `own_commits`, `touched`, `fix_pass_units` | `['S(sibling)', 'f1', 'f2']`; `['own.py', 'sib.py']`; the sibling's `s` listed |
| case A2, the base merges a stack holding an item commit older than `T` | `['f2']`; `['own.py']`; the sibling's unit not listed |
| case B, a topic forked before `T` and merged after | `['f']`; `['own.py']` |
| case B2, a topic forked before `T` merges `T`, then fixes, then is merged | `['topic-fix']`; `['topic.py']`; the topic's commit before the merge not owned |
| case B3, a topic forked before `T` fixes, then merges `T`, then is merged | `[]`; `[]` |
| case C, a sibling branch forked before the base merged `T` commits after it and is merged into the base; the branch merges the base | `['f2']`; `['own.py']`; the sibling's unit not listed |
| case D, the base merges `T`, a sibling lands on the base, the branch adds `f2` without merging the base; CI's merge ref built with the base as first parent | branch `['f2']`, `['own.py']`; merge ref `['S(sibling)', 'f2']`, `['own.py', 'sib.py']` |
| `survivor-check --range 24cfb66f..fadd8270 --exempt` the item's `survivors.md`, in the clone | exit 0 |
| `gh pr checks 878` and the run's head SHA | 13 of 13 pass at head 4cf41ee4; nothing running |
| `round-record new --round 3` over this report, in the clone only; the record it wrote was deleted with the clone | exit 0; the tables parsed; `Fix of a fix` read `second — 🟡 3 at skills/code-review/scripts/chain_check.py#own_commits, a unit round-2's fixes changed`, and it printed that the work item goes back to its framer |
| `evidence-check --strict` and `bin/test` over `test_no_real_identifiers`, `test_docs_line_wrap`, `test_one_word_one_meaning` and `test_a_record_states_what_the_tree_has`, in the clone with this report staged | exit 0 each; 165 passed |
| broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — review round 2

| Field | Value |
|---|---|
| Target SHA | 1923d2049d604a4684995f33cdb87f819b060aff |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 878 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | first — 🟡 1 at skills/code-review/scripts/chain_check.py#own_commits, a unit round-1's fixes changed |
| Needs a fix | yes — 🟡 1 (the fix's limit sentences are wider than `own_commits` in two shapes the probes measured) and 🟡 2 (four shipped carriers still state the limit-free claim) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 2 of round 1's fixes: d2b76587..27920e58 (e6fc73f9, 27920e58), plus the fix table at 4933eba5 and the close at 1923d204. The job was the answers to round 1's fixed and answered verdicts; round 1's New units row read none. The spawn asked three things. First, whether every coordinate stating the limit-free claim now carries the limit, searching the tree rather than only the five the smith named. Second, whether the limit sentences are true of own_commits as written, re-running round 1's probes A and B. Third, whether spec.md §In, left as the framer wrote it, is a sentence a reader acts on. It also ran the eight suite-wide guard modules once. Facts arrived labelled. Executed by the orchestrator: bin/test over two modules (132 passed) and the close (2 fixed, 3 answered). Read from the smith: the fixes, evidence-check --strict and survivor-check. Read: release/v0.21.0 moved to 9b644676, which the branch has not merged yet.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The fix's two limit sentences are wider than `own_commits`: a base that merged an item commit older than `a` owns no later base commit, and a topic forked before `a` that merged `a` owns its fix; the same wording is in two docstrings round 1's fixes changed, three ledger rows, `overview.md` and `phases/phase-1.md` | `docs/the-record-layout.md:148`, `skills/code-review/scripts/chain_check.py#own_commits` | open | executed: probe A2 gave `['f2']` with no sibling, probe B2 gave `['topic-fix']` and `['topic.py']` |
| 🟡 2 | Four shipped carriers still say a merge of the base brings nothing into the surface: `orchestration.md:369`, `docs/round-record-spec.md:693`, the `fix_pass_units` docstring and the `touched` docstring | `skills/code-review/orchestration.md:370` | open | executed: probe A, where `touched` read `sib.py` and `fix_pass_units` listed the sibling's unit; read: the four sentences, none qualified and none in round 1's list |
| ⬜ 3 | The changelog fragment states the limit-free claim twice, and the fix table says it states none | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:13` | open | read against probe A; a correction, since the file is under `seal/specs/` |
| ⬜ 4 | Five ledger rows state the limit-free claim: `S1, S2, S3`, `S4`, `S6`, `S12`, `Corrected · A1` | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:11` | open | read; a correction, since the file is under `seal/ledger/` |
| 🟢 | round 1's blocking finding is closed — the S10 case is classified, and CI is green on every leg | `tests/test_a_shrunken_corpus_declines_to_judge.py:248` | confirmed | executed: `gh pr checks 878` at 1923d204, 11 of 11 pass; the eight modules in the clone, exit 0, 435 passed |
| 🟢 | round 1's finding 2 is closed at the coordinates it named — the home and the five listed places carry the limit | `docs/the-record-layout.md:121` | confirmed | read; executed: probes A and B reproduce the two shapes the home names. The class continues as this round's findings 1 and 2 |
| 🟢 | round 1's notes 3, 4 and 5 stand as answered | `skills/code-review/scripts/round_record.py:2402` | confirmed | read: the grounds in the fixes file hold against the code at 1923d204 |
| 🟢 | `spec.md` §*In* left as the framer wrote it follows the convention | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md:70` | confirmed | read: `spec.md` is the framer's, `overview.md` holds the divergence and quotes the sentence, and `settle` reads the set together |

## Paste-ready fixes

```markdown
What no reader can see is a change made only inside a merge's conflict
resolution. The merge is owned by no range, so `close` refuses a `fixed` row
that names it. Descent is the whole test, so two shapes read against the
item's history. Where the base merged `a`, or a commit that descends from it,
with a merge commit (a back-merge, or a stacked branch forked after `a` and
merged first), every base commit after that merge descends from `a`, and is
owned once `b` reaches it. And an own commit on a topic forked before `a` that
never merged `a` descends from it never and is not owned, so its units leave
the surface and a `fixed` row naming it is refused. A range whose start does
not reach its end owns nothing, and `close` refuses it rather than writing an
empty surface.
```
```python
    Descent is the whole test, so the home's two limits are this function's
    too: once the base has merged `a`, or a commit after it, with a merge
    commit, a later base commit descends from `a` and is owned, and an own
    commit on a topic forked before `a` that never merged `a` is not. A start
    that does not reach its end owns nothing, and the answer is `[]`.
```
```python
    nothing here reads which parent of a merge is the first. Where the base
    merged round 1's target, or a commit after it, with a merge commit, the
    walk reads later base commits too: `own_commits` states that limit. Every
    owned
```
```text
where the base merged the start, or a commit after it, with a merge commit,
a later base commit is owned; an own commit on a topic forked before the
start that never merged it is not
```
```text
because it descends from round 1's target never unless the base merged that
target, or a commit after it, with a merge commit before it
```
```markdown
Two more rows, and `round_record.py close --range <a>..<b>` derives both from
the fix range: `Contract changes` from an AST comparison of every top-level
Python unit the range's own commits changed, with the call sites found by
search, and `New units` from the same comparison with a depth per entry. In a
repository that squashes into its base, a merge of the base inside the range
brings none of its units into either row: `docs/the-record-layout.md` §*A
range owns the commits that descend from its start* owns which commits are
the range's own, and names the merge shape where a base commit is one.
`close` refuses depth 2 before writing any cell. The rows cost no question to
anyone, because the diff answers them.
```
```markdown
changed: present at both ends with a different `ast.dump`, so a re-commented
unit has not changed, and written by one of the range's own commits, so in a
repository that squashes into its base a unit a merge brought in has not
(`docs/the-record-layout.md` §*A range owns the commits that descend from its
start* names the merge shape where it has). The form is a whole token, a code
span or a word: a path
```
```python
    Kept only where one of the range's own commits added or changed the unit
    (`own_units`, #860): in a repository that squashes into its base, a unit
    a merge in the range brought in was written by nobody this run reviewed,
    so a finding inside it is no fix of a fix. Once the base has merged the
    range's start with a merge commit, a later base commit is owned and its
    units land (`chain.own_commits` states that limit).
```
```python
    The commits are `chain.own_commits`: the non-merge commits that descend
    from `a` and that `b` reaches (#860). A path only a sibling's squash
    brought in through a merge is not this range's (`own_commits` names the
    merge shape where a base commit is), and the path-level answer is the
    first of two filters: `own_units` is the second, because a file an own
    commit touched can carry a merged-in unit too. A path the range deleted is
```

## Executed probes

| What was run | Result |
|---|---|
| `test_tmp_probe.py` case A, round 1's back-merge after `T`; `own_commits`, `touched`, `fix_pass_units` — NAME NOT IN TREE | `['f1', 'S(sibling)', 'f2']`; `['own.py', 'sib.py']`; the sibling's `s` listed |
| case A2: the base merges a stack holding an item commit older than `T`, then a sibling lands, then the branch merges the base | `['f2']`; `['own.py']`; the sibling's unit not listed |
| case B, round 1's topic forked before `T` and merged after | `['f']`; `['own.py']` |
| case B2: a topic forked before `T` merges `T`, then fixes, then is merged | `['topic-fix']`; `['topic.py']`; `tf` listed |
| `bin/test` over the eight modules the spawn named, in the clone at 1923d204 | exit 0, 435 passed |
| `gh pr checks 878` at head 1923d204 | 11 of 11 pass; macOS 20m17s, ubuntu 8m36s, Windows groups 1-4 pass; nothing running |
| `round-record new --round 2` over this report, in the clone only; the record it wrote was deleted with the clone | exit 0; the tables parsed; `Fix of a fix` read `first — 🟡 1 at skills/code-review/scripts/chain_check.py#own_commits, a unit round-1's fixes changed`; its chain-check printed the fragment notice naming `27920e5` as a commit the changelog fragment was left behind by, which is ⬜ 3's file |
| `evidence-check --strict` and `bin/test` over `test_no_real_identifiers`, `test_docs_line_wrap`, `test_one_word_one_meaning` and `test_a_record_states_what_the_tree_has`, in the clone with this report staged | exit 0 each; 43 and 127 passed |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

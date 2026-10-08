# Round 3 report — 1791384160, a fix range is its own commits across a merge

Verifying round, by warden at `4cf41ee400920a3424fea5b6e78b46fffefa8ce0`.
The target is round 2's fix range `24cfb66f..fadd8270` (fb5ba994, fadd8270),
plus the fix table at 1b595fa4 and the close at 4cf41ee4. Reviewed in a
`--no-local` clone. Round 2's `New units` row reads `none`, so there is no new
unit to judge as code. Coordinates are carried from round 2's report and round
1's record; every verdict below is re-derived. The spawn says this round ends
the run, so what it leaves open is the orchestrator's to file.

## How the findings relate

```
round 2, finding 1   the limit sentences were wider than own_commits  -> closed
round 2, finding 2   four carriers stated the limit-free claim       -> closed
round 2, note 3      the changelog fragment                          -> closed
round 2, note 4      five ledger rows                                -> closed where it pointed
   |
   the fix replaced the enumerated shapes with the ancestry rule, which is right,
   and then wrote three sentences beside it that the rule does not support:
   |
   +-- 🟡 1  the fragment section now says CI reads the same commits as the
   |         branch, and dropped the hedge that said where that fails (probe D)
   +-- 🟡 2  the home's examples are phrased by time and topic state, and two
   |         of them are false in shapes C and B3
   +-- 🟡 3  the own_commits docstring carries the B3 example (a unit round
   |         2's fixes changed, so this one is a fix of a fix)
   +-- ⬜ 4  one ledger row was never corrected, and phase-1.md carries B3
```

The rule sentence itself is now true at every coordinate I opened: a commit is
owned when it is a non-merge commit that has `a` as an ancestor and that `b`
reaches. The three 🟡 findings are all sentences written next to that rule that
claim something narrower or wider than it.

## Round 2's four verdicts are answered

Executed: I re-ran round 2's probes A, A2, B and B2 against the code at
4cf41ee4 in a fresh probe. The results match round 2's exactly. A gives
`['S(sibling)', 'f1', 'f2']`, A2 gives `['f2']`, B gives `['f']`, and B2 gives
`['topic-fix']`. `touched` and `fix_pass_units` agree with `own_commits` in
each.

- **Round 2's finding 1 is closed.** The home's limit paragraph at
  `docs/the-record-layout.md:150-156` now says "Ancestry is the whole test" and
  names no merge shape. The words round 2 measured as false ("any of the
  item's commits", "descends from it never") are gone from the home, the
  `own_commits` docstring and the `fragment_left_behind` docstring. A2's base
  never merged `a`, and the new example says such a base owns nothing. B2's
  fix was made after the topic merged `a`, and the new example says it is
  owned. Both match the code.
- **Round 2's finding 2 is closed.** Read against probes A, A2, B2 and C:
  `skills/code-review/orchestration.md:369-371`, `docs/round-record-spec.md`
  §*A fix of a fix* at lines 693-696, the `fix_pass_units` docstring and the
  `touched` docstring each state the ancestry test, and each is true in every
  shape I built. `close`'s `fixed` refusal now says "a commit a merge brought
  in that was not made on top of" the start. In B3 the topic's fix is exactly
  such a commit, so the refusal is true there too. The S6 case pins the new
  words, and its assertion is a strict superset of the old one, so the old
  message fails it.
- **Round 2's note 3 is closed.** Read: `changelog.md` now says a commit is
  the range's own when it has the start as an ancestor, and the `fixed`
  refusal names "a commit not made on top of the start". Both are true in
  probes A and B3.
- **Round 2's note 4 is closed where it pointed.** Read: the rows `S7, S8,
  S9`, both `S12` rows, `Corrected · S2, S3, S4, S6`, `S1, S2, S3`, `S4`, `S6`
  and `Corrected · A1` state the ancestry test. One row round 2 did not list
  is still false; it is ⬜ 4 below. CI's `ledger` job passed at 4cf41ee4, so
  the re-anchored coordinates resolve (executed by CI, read by me).

The smith's `survivors.md` rows excuse `spec.md:71` and the S9 row at
`spec.md:191`. Read: both are the framer's text, and round 2 confirmed the
convention that `overview.md` carries the divergence. Executed:
`survivor-check --range 24cfb66f..fadd8270 --exempt` the item's
`survivors.md`, in the clone, exit 0.

## 🟡 1 — The fragment section says CI reads the same commits as the branch, and that is false after a back-merge

`docs/the-record-layout.md:99-103` now reads: "CI's checkout, the pull request
merged into its base, reads the same commits as the branch does, because the
walk asks each commit's ancestry and never which parent of a merge it sits
behind."

Before fb5ba994 the sentence ended with "(the next section names the merge
shape where that fails)". The fix removed that hedge and kept the equality.
But the equality only holds when the base never merged round 1's target.

Executed, probe D. The base merges the branch at `T` (a back-merge). A sibling
commit `S` lands on the base. The branch adds `f2` and does not merge the base.
Then CI's merge ref is built as GitHub builds it, with the base as the first
parent:

- the branch: `own_commits(T, HEAD)` gives `['f2']`
- CI's merge ref: `own_commits(T, ref)` gives `['S(sibling)', 'f2']`, and
  `touched` reads `sib.py`

So in CI the fragment notice reads `S` as one of the item's commits, and a
branch checkout does not. If `S` changed a behaviour path, CI names it and a
local `chain-check` stays silent. The notice never refuses, so nothing is lost
or blocked. But this section is what tells a reader that the local run and CI
agree, and in this shape they do not.

Why it matters: the item's own rule says a commit made on top of `a` is owned
wherever it was made. CI's merge ref contains every base commit, so it owns
the base's commits made on top of `a`. The sentence draws a conclusion the
rule beside it contradicts. Round 1 found the same claim limit-free, round 1's
fix added the hedge, and this fix removed it.

Read and not counted: the `fragment_left_behind` docstring at
`skills/code-review/scripts/chain_check.py:4566-4569` says CI's merge ref, the
branch's own merge of its base and a rebuilt branch "all read the same
commits". It names no comparand. Read as "the same as each other", it holds
in D, because all three contain the base's tip. So I do not count it. The
ledger row `S7, S8, S9` carries the same words and the same reading.

## 🟡 2 — The home's examples are phrased by time, and two of them are false

`docs/the-record-layout.md:126-129` gives the ancestry rule three examples:

- "a sibling's commit made after the base merged `a` is" owned
- "an own fix on a topic forked before `a` is owned once that topic has
  merged `a`, and not before"

Both describe when something happened, not what it descends from. The rule
one line above them says "a commit a merge brought in counts exactly when it
was made on top of `a`". Where *after* and *on top of* differ, the examples
are false.

Executed:

- **Probe C.** The base merges `T`. A sibling branch forked from the base
  before that merge makes its commit after it, and is then merged into the
  base with a merge commit. The branch merges the base. `own_commits` gives
  `['f2']`. The sibling's commit was made after the base merged `a`, and it is
  not owned.
- **Probe B3.** A topic forks before `T` and makes its fix. Then the topic
  merges `T`, and the branch merges the topic. `own_commits` gives `[]`. The
  topic has merged `a`, and its fix is not owned.

Why it matters: this is the rule's one home. A reader who updates a topic
with the item's branch before merging it back reads "owned once that topic has
merged `a`" and expects the fix in `New units`. The code leaves it out, and
`close` refuses a `fixed` row naming it. The refusal's own words ("not made on
top of") are correct and contradict the home. Round 2 rated the same kind of
sentence 🟡, and the fix table says the shapes are "examples only". An example
still has to be true.

The `own_commits` docstring carries the B3 example too. It is a separate
finding, 🟡 3, because it sits at a different depth.

## 🟡 3 — The `own_commits` docstring carries the B3 example

`skills/code-review/scripts/chain_check.py:4498-4499`: "an own fix on a topic
forked before `a` is owned once that topic has merged `a`". Probe B3 gives
`[]` with the topic having merged `a`, so the sentence is false in the same way
as 🟡 2.

This finding is written apart from 🟡 2 because the docstring is inside
`own_commits`, and fb5ba994 changed that unit. Its `Location` names
`chain_check.py#own_commits`, so `new` should read it as a fix of a fix. The
reading is right: the sentence is text round 2's fixes wrote.

## ⬜ 4 — One ledger row still states the limit-free claim, and `phase-1.md` carries B3

These are corrections, because both files sit under `seal/ledger/` or
`seal/specs/`.

- The row `Corrected · S1, S5, S8, S10`, line 4 of the item's ledger
  fragment, says "the same commits on a branch checkout and on CI's merge of
  the pull request into its base" and "a sibling's squash on the base is named
  on neither side of a merge". Probe D breaks the first, and probe A names the
  sibling's commit on the branch's side. fadd8270 moved this row's anchors and
  left its claim as it was. It was not in round 2's list of five rows either,
  so round 2's `git grep` and the fix's both missed it.
- The row `Corrected · S2, S3, S4, S6`, line 5, opens with "the branch's own
  merge of the base names none of the sibling's commits". The qualifier
  arrives at the end of the row, so this one reads true as a whole. I name it
  for the same edit.
- `phases/phase-1.md`'s round 2 correction says "a topic forked before the
  start is owned once it has merged the start". Probe B3 is the counterexample.

## Did the `git grep` miss a shipped coordinate

Read, by searching the tree outside `seal/releases/` and `seal/specs/` for
"descends … never", "neither side", "brings none", "a merge brought in",
"same commits", "back-merge" and "forked before":

- No shipped sentence still states the limit-free claim as its own rule.
- The one shipped sentence that is now false is 🟡 1's, and the fix wrote it
  rather than missed it.
- Three test names and one test docstring state the claim in its old form:
  `test_a_unit_a_merge_brought_into_a_file_an_own_commit_touched_is_not_new`,
  `test_a_unit_a_merge_brought_into_the_previous_range_is_no_fix_of_a_fix`,
  `test_a_branch_rebuilt_on_the_base_names_its_own_commits_and_not_the_siblings`
  and the docstring of
  `test_the_ci_merge_ref_names_the_items_commit_and_not_the_siblings`. Each
  describes its own fixture, whose sibling never descends from the target, so
  each is true of its case. I count none of them.

## Not verified

| Item | Who answers |
|---|---|
| The full suite, the repository-wide lint and the typecheck: `unverified` by me, and the broad gate is `not yet` | the sealer, once, after the rounds settle |
| Whether the fragment notice itself prints `S` in CI in shape D. I measured `own_commits` and `touched` on the merge ref, which is what the notice walks, and did not build a work item around it | the orchestrator, if the reading of `fragment_left_behind` is not taken as the answer |

## Regression tests to plant

- `tests/test_a_fragment_left_behind_is_named.py`: shape D. The base merges
  round 1's target, a sibling commit changing a behaviour path lands on the
  base, and the branch does not merge the base. CI's merge ref names the
  sibling's commit and the branch checkout does not. This pins the limit 🟡 1
  restores.
- `tests/test_the_fixes_close_the_record.py`: shapes C and B3 as cases of
  `own_commits`. A sibling branch forked before the base merged the start owns
  nothing, and a topic fix made before the topic merged the start is not
  owned after it does.

## Facts for the evidence ledger

- Executed 2026-10-08, git 2.50.1 on macOS, against `own_commits` and
  `touched` at 4cf41ee4. After a back-merge of the range's start into the
  base, CI's merge ref owns the base commits made on top of the start, and a
  branch that has not merged the base does not. A commit made after the base
  merged the start, on a branch forked before that merge, is not owned. A
  topic fix made before the topic merged the start is not owned after the
  topic merges it.

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

## Paste-ready fixes

### 🟡 1

`docs/the-record-layout.md`, lines 99-103, the end of the fragment section's
second paragraph:

```markdown
move lists both its paths, so a file moved under `tests/` is named. CI's
checkout, the pull request merged into its base, reads every commit the branch
reads, because the walk asks each commit's ancestry and never which parent of
a merge it sits behind. Where the base merged round 1's target, CI also reads
the base's commits made on top of it that the branch has not merged yet, so
CI can name a commit a branch checkout does not (the next section says which
commits that ancestry makes the item's own).
```

### 🟡 2

`docs/the-record-layout.md`, lines 126-129, the examples after the rule:

```markdown
For example, a sibling's squash on a base that never merged `a` is not owned.
A sibling's commit made on the base after the base merged `a` is owned, and
one made on a branch forked from the base before that merge is not. On a
topic forked before `a`, a fix made after the topic merged `a` is owned, and
a fix made before that merge is not, even once the topic has merged `a`. Two
readers walked a
```

### 🟡 3

`skills/code-review/scripts/chain_check.py`, `own_commits`' docstring, lines
4496-4500:

```python
    `git merge` set is not read. Ancestry alone decides, so a commit a merge
    brought in counts exactly when it was made on top of `a`: a sibling's
    squash on a base that never merged `a` is not owned, and on a topic
    forked before `a` a fix made after the topic merged `a` is owned, while
    one made before that merge is not. A start that does not reach its end
    owns nothing, and the answer is `[]`.
```

### ⬜ 4

The ledger row `Corrected · S1, S5, S8, S10`, the clause between its two dashes:

```text
— with no reading of a merge's parent order, so a sibling's squash on a base
that never merged the target is named on neither side of a merge, a merge made
from the base's side below HEAD included (#805); CI's merge of the pull
request into its base reads every commit a branch checkout reads, and also
the base's commits made on top of the target that the branch has not merged —
```

`phases/phase-1.md`, the round 2 correction's second sentence:

```text
code, because the back-merge must merge the start or a commit after it, and
a fix on a topic forked before the start is owned only when it was made after
the topic merged the start.
```

Needs a fix: yes — 🟡 1 (the fragment section says CI reads the same commits as the branch, false after a back-merge), 🟡 2 (two of the home's examples are false in shapes C and B3) and 🟡 3 (the own_commits docstring carries the B3 example, a fix of a fix)
Loses a record or crashes: no

## Proof

Files opened: `rounds/round-2.md`, `rounds/round-2-fixes.md`,
`rounds/round-2-report.md`, `rounds/round-1.md` lines 1-30; `survivors.md`;
the diff `24cfb66f..fb5ba994` over `docs/`, `skills/` and `tests/` whole; the
diff `fb5ba994..fadd8270` for `overview.md` and `phases/phase-1.md`, and a
word diff of the ledger fragment's `Corrected · S1, S5, S8, S10` row;
`changelog.md`; `overview.md`; the item's ledger fragment, every row's claim
and anchors; `spec.md` lines 68-73 and 188-193; `docs/the-record-layout.md`
lines 78-158; `docs/round-record-spec.md` lines 684-700;
`skills/code-review/orchestration.md` lines 40-56 and 362-378;
`skills/code-review/scripts/chain_check.py` lines 4487-4547 (`own_commits`)
and 4550-4600 (`fragment_left_behind`);
`skills/code-review/scripts/round_record.py`'s import lines and the
`fix_pass_units` and `touched` docstrings through the diff;
`tests/test_the_rules_have_one_owner.py` lines 330-345; the docstrings of
the four test cases named under the `git grep` heading. The probe file, the
seven repositories it built and the clone are deleted after this round.

# Round 2 report — 1791384160, a fix range is its own commits across a merge

Verifying round, by warden at `1923d2049d604a4684995f33cdb87f819b060aff`.
The target is round 1's fix range `d2b76587..27920e58` (e6fc73f9, 27920e58),
plus the fix-table commit 4933eba5 and the closing commit 1923d204. Reviewed in
a `--no-local` clone. Round 1's `New units` row reads `none`, so there is no
new unit to judge as code. Coordinates are carried from round 1's report;
every verdict below is re-derived.

## How the findings relate

```
round 1, blocking finding 1   CI red on the path-list guard   -> closed (CI green, all legs)
round 1, finding 2            the home said "never"            -> closed where it pointed
   |
   +-- 🟡 1  the fix's own limit sentences are wider than own_commits
   |         (two shapes the probes measured)
   +-- 🟡 2  §12: four shipped carriers still state the limit-free claim
   +-- ⬜ 3  the changelog fragment states it twice (paperwork)
   +-- ⬜ 4  five ledger rows state it (paperwork)
round 1, notes 3-5             answered as notes                -> the answers hold
```

Both 🟡 findings belong to round 1's finding 2. The fix stated the limit in the
five places round 1 listed, and those five are now right. But the limit
sentences it wrote overreach in two shapes, and the class has more carriers
than round 1 listed.

## Round 1's blocking finding 1 is closed

Executed: `gh pr checks 878` at head `1923d204`. All 11 checks pass: lint,
ledger, release, both `arm-check-grammar` legs, ubuntu, macOS, and all four
Windows shards. Nothing is running and nothing is red. Round 1's red was
ubuntu and Windows group 2, with macOS still running. All three are green now.

Executed in the clone: the eight modules the spawn named, including
`tests/test_a_shrunken_corpus_declines_to_judge.py`. Exit 0, 435 passed.

Read: e6fc73f9 adds the one `LISTS_A_FIXTURE` entry and the reason that round
1's paste-ready fix gave. Nothing else changed in that file.

## Round 1's finding 2 is closed where it pointed

Read: the home's first paragraph at `docs/the-record-layout.md:121-124` now
limits "never" to a repository that squashes into its base. Its last paragraph
names both shapes. The fragment section at line 100 points to the next section.
Round 1 listed five more places, and each now carries the limit: the
`own_commits` and `fragment_left_behind` docstrings, and the ledger rows
`S7, S8, S9`, `S12` and `Corrected · S2, S3, S4, S6`.

Executed: I re-ran round 1's probes A and B against the code at 1923d204. A
gave `['f1', 'S(sibling)', 'f2']`, so the sibling is owned. B gave `['f']`,
and `touched` gave `['own.py']`, so the topic's fix is dropped. The home's two
shapes match the code in the shapes round 1 built.

The finding is closed at those coordinates. The two findings below are about
the same class.

## 🟡 1 — The fix's limit sentences are wider than what `own_commits` does

`docs/the-record-layout.md:148-151` says two things:

- "Where the base merged **any of the item's commits** with a merge commit (a
  back-merge, or a stacked branch merged first), every commit made on the base
  after that merge descends from `a` and is owned."
- "An own commit on a topic forked before `a` **descends from it never** and
  is not owned."

Neither holds as written. Descent from `a` needs `a` itself in the base's
history. An item commit older than `a` is not enough. And a topic that has
merged `a` does descend from it.

Executed, by a probe in the round's scratch directory, `test_tmp_probe.py` — NAME NOT IN TREE:

- **Probe A2.** The base merges a stacked branch that holds the item's commit
  `p1`, made before `T`. A sibling lands on the base. The branch merges the
  base. `own_commits(T, HEAD)` gives `['f2']`, so the sibling is not owned.
  The sentence's own example, "a stacked branch merged first", is the shape
  where it fails whenever the stack forked before `a`.
- **Probe B2.** A topic forks before `T` and merges the branch at `T`. Then
  its fix lands, and the branch merges the topic. `own_commits(T, HEAD)` gives
  `['topic-fix']`, and `touched` gives `['topic.py']`. The fix is owned.

Why it matters: this section is the rule's one home (rule 17 of
`tests/test_the_rules_have_one_owner.py`). Round 1's finding was that the home
stated a guarantee the code does not give. The fix replaced that sentence with
two others, and both of them also state something the code does not do. In
both shapes the code behaves better than the sentence says. But a reader who
merges stacked branches with merge commits is told to expect a sibling's
units in `New units`, and the code will not list them.

The same wording appears in more places (§12):

- the `own_commits` docstring, `skills/code-review/scripts/chain_check.py:4497-4501`
- the `fragment_left_behind` docstring, `chain_check.py:4568-4570`
- the ledger fragment's `S7, S8, S9`, `S12` and `Corrected · S2, S3, S4, S6`
  rows
- `overview.md`'s last divergence row and `phases/phase-1.md`'s note

The two docstrings sit inside units that round 1's fix range changed.
Because the `Location` cell carries `chain_check.py#own_commits`, `new` will
read this finding as a fix of a fix (`first`). That reading is correct: the
defect is in text the fix wrote.

Round 1's own paste-ready fix carried the words "any of the item's commits".
The smith pasted them, so the overreach started in round 1's report.

## 🟡 2 — Four shipped carriers still state the limit-free claim (§12)

Round 1 listed five places besides the home. The tree has four more in shipped
files, and none of them is qualified. Each one states that a merge of the base
brings nothing into the surface:

- `skills/code-review/orchestration.md:369-371`: "A merge of the base inside
  the range brings none of its units into either row". The link after the
  colon is to *which commits are the range's own*, not to the limit.
- `docs/round-record-spec.md:693-694`, §*A fix of a fix*: "written by one of
  the range's own commits, so a unit a merge brought in has not".
- `skills/code-review/scripts/round_record.py:2350-2352`, the
  `fix_pass_units` docstring: "a unit a merge in the range brought in was
  written by nobody this run reviewed, so a finding inside it is no fix of a
  fix".
- `round_record.py:3391-3392`, the `touched` docstring: "A path only a merge
  brought in is not this range's".

Executed, probe A (the back-merge): `touched` gives `['own.py', 'sib.py']`, and
`fix_pass_units` gives `('sib.py', 's')` among its units. The sibling's file
is read and the sibling's unit lands as a fix of a fix. Both docstrings say
the opposite, and so do the two documents.

Why it matters: this is round 1's finding 2 in four more places. The
orchestration sentence is the one an orchestrator reads before it trusts the
`New units` row. The plugin ships to repositories that merge with merge
commits, and there this sentence is false. It is 🟡 for the same reason round
1's finding was.

None of the four units is one round 1's fixes changed. So this finding is not
a fix of a fix, and its `Location` names the skill file.

## ⬜ 3 — The changelog fragment states the claim twice

`changelog.md:13-14`: "so a finding inside a unit a merge brought in reads
`no`". And at lines 15-17, `close` refuses "a `fixed` row naming a merge or a
commit a merge brought in". Probe A shows both are false after a back-merge.
The sibling's unit lands, and a `fixed` row naming the sibling's commit would
be accepted, because that commit is owned.

Round 1's fix table says "`changelog.md` is unchanged: none of its sentences
states the limit-free claim". That claim is false. It is a correction because
the file is under `seal/specs/`. But the release gathers this fragment
verbatim into the release note, so it is the one paperwork file a user reads.

## ⬜ 4 — Five ledger rows state the claim

These rows are in the item's ledger fragment, and none of them is qualified:

- `S1, S2, S3`: "A sibling's unit a merge of the base brought into a file an
  own commit also touched is not listed".
- `S4`: "a finding inside a unit a merge of the base brought into that range
  reads `no`".
- `S6`: `close` refuses "a commit a merge brought in".
- `S12`: "`docs/round-record-spec.md` §*A fix of a fix* says a unit a merge
  brought in does not land".
- `Corrected · A1`: "a unit a merge in the range brought in … land nowhere".

These are corrections because the file is under `seal/ledger/`. When 🟡 2's
fix edits `docs/round-record-spec.md` §*A fix of a fix*, the `S12` anchor on
that section goes stale, so that row has to be re-anchored either way.

## Round 1's notes 3, 4 and 5 — the answers hold

Read against the code at 1923d204:

- **Note 3** (cost). The answer is "a cost, not a wrong answer". That is right.
  `own_units` reads prose paths that `measure` never keeps, which costs time
  and changes no row.
- **Note 4** (a sibling's signature change in `Contract changes`). The answer
  is that the entry appears only where an own commit also changed the unit,
  and that the entry then names a real change in a unit the fix touched. That
  is true of the filter at `round_record.py:4449-4451`. The verifying round is
  sent to a unit the fix did touch.
- **Note 5** (the pronoun at `orchestration.md:372`). The answer is that the
  sentence reads in its section. That is acceptable for a ⬜. 🟡 2's
  paste-ready fix rewrites that paragraph and writes "`close` refuses", so the
  pronoun goes away at no cost.

## `spec.md` §*In*, left as the framer wrote it

The orchestrator asked whether this sentence is one a reader acts on. Read:
`skills/implement/SKILL.md` gives `spec.md` to the framer and `overview.md` to
the builder for divergences. `skills/settle/SKILL.md` reads the whole SDD set
together when it folds. The overview's last divergence row quotes the spec's
sentence and says where it is false. So a reader who acts on `spec.md` §*In*
also has that row in front of them, and leaving the sentence alone follows the
convention. That row carries 🟡 1's wording "after a back-merge of the item's
commits", so it is part of 🟡 1's fix list.

## Not verified

| Item | Who answers |
|---|---|
| The full suite, the repository-wide lint and the typecheck: `unverified` by me, and the broad gate is `not yet` | the sealer, once, after the rounds settle |
| `evidence-check --strict` after 27920e58's re-anchored ledger rows. Not run by me. CI's `ledger` job passed at 1923d204 | the orchestrator, if CI's ledger job is not taken as the answer |
| Merging `release/v0.21.0` at 9b644676 into the branch | the orchestrator, before the seal, as the spawn says |

## Regression tests to plant

- `tests/test_a_fix_of_a_fix_is_counted.py`: a back-merge case. The base
  merges the branch after round 1's target, a sibling adds a unit on the base,
  and the branch merges the base. Then a finding inside the sibling's unit
  reads `first`. This pins the limit the home states, so a later change to
  `own_commits` cannot quietly make the sentence false again.
- `tests/test_a_fragment_left_behind_is_named.py` or
  `tests/test_the_fixes_close_the_record.py`: probes A2 and B2 as cases of
  `own_commits`. A stack merged from before the start owns no later base
  commit, and a topic that merged the start owns its fix.

## Facts for the evidence ledger

- Executed 2026-10-08, git 2.50.1 on macOS, against `own_commits` and
  `fix_pass_units` at 1923d204. A base that merged a commit older than the
  range's start owns no later base commit. A topic forked before the start
  that merged the start owns its later fix. After a back-merge of a commit at
  or after the start, `touched` reads the sibling's file, and `fix_pass_units`
  lists the sibling's unit.

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

## Paste-ready fixes

### 🟡 1

`docs/the-record-layout.md`, the section's last paragraph:

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

`skills/code-review/scripts/chain_check.py`, `own_commits`' docstring:

```python
    Descent is the whole test, so the home's two limits are this function's
    too: once the base has merged `a`, or a commit after it, with a merge
    commit, a later base commit descends from `a` and is owned, and an own
    commit on a topic forked before `a` that never merged `a` is not. A start
    that does not reach its end owns nothing, and the answer is `[]`.
```

`skills/code-review/scripts/chain_check.py`, `fragment_left_behind`'s
docstring:

```python
    nothing here reads which parent of a merge is the first. Where the base
    merged round 1's target, or a commit after it, with a merge commit, the
    walk reads later base commits too: `own_commits` states that limit. Every
    owned
```

The ledger rows `S7, S8, S9` and `S12`, `overview.md`'s last divergence row,
and `phases/phase-1.md`'s note take the same two qualifiers:

```text
where the base merged the start, or a commit after it, with a merge commit,
a later base commit is owned; an own commit on a topic forked before the
start that never merged it is not
```

`Corrected · S2, S3, S4, S6`, its last clause:

```text
because it descends from round 1's target never unless the base merged that
target, or a commit after it, with a merge commit before it
```

### 🟡 2

`skills/code-review/orchestration.md`, §*And name the fix surface, in the same
record*, first paragraph. This also answers round 1's note 5:

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

`docs/round-record-spec.md`, §*A fix of a fix*:

```markdown
changed: present at both ends with a different `ast.dump`, so a re-commented
unit has not changed, and written by one of the range's own commits, so in a
repository that squashes into its base a unit a merge brought in has not
(`docs/the-record-layout.md` §*A range owns the commits that descend from its
start* names the merge shape where it has). The form is a whole token, a code
span or a word: a path
```

`skills/code-review/scripts/round_record.py`, `fix_pass_units`' docstring:

```python
    Kept only where one of the range's own commits added or changed the unit
    (`own_units`, #860): in a repository that squashes into its base, a unit
    a merge in the range brought in was written by nobody this run reviewed,
    so a finding inside it is no fix of a fix. Once the base has merged the
    range's start with a merge commit, a later base commit is owned and its
    units land (`chain.own_commits` states that limit).
```

`skills/code-review/scripts/round_record.py`, `touched`'s docstring:

```python
    The commits are `chain.own_commits`: the non-merge commits that descend
    from `a` and that `b` reaches (#860). A path only a sibling's squash
    brought in through a merge is not this range's (`own_commits` names the
    merge shape where a base commit is), and the path-level answer is the
    first of two filters: `own_units` is the second, because a file an own
    commit touched can carry a merged-in unit too. A path the range deleted is
```

After the `docs/round-record-spec.md` edit, re-anchor the ledger's `S12`
coordinate on §*A fix of a fix*.

Needs a fix: yes — 🟡 1 (the fix's limit sentences are wider than `own_commits` in two shapes the probes measured) and 🟡 2 (four shipped carriers still state the limit-free claim)
Loses a record or crashes: no

## Proof

Files opened: `rounds/round-1.md`, `rounds/round-1-fixes.md`,
`rounds/round-1-report.md`; the diff `d2b76587..1923d204` whole;
`docs/the-record-layout.md` lines 80-160; `docs/round-record-spec.md` lines
372-381 and 685-700; `skills/code-review/orchestration.md` lines 360-380;
`skills/code-review/scripts/chain_check.py` lines 4480-4530 (`own_commits`)
and the `fragment_left_behind` docstring;
`skills/code-review/scripts/round_record.py` lines 60-100, 2339-2425
(`fix_pass_units`, `commit_units`, `own_units`), 2470-2500, 3380-3400
(`touched`) and 4418-4455 (`close`'s guard and filter);
`tests/test_the_rules_have_one_owner.py` lines 325-365;
`tests/test_a_fix_of_a_fix_is_counted.py` lines 255-325; the item's ledger
fragment, rows 1-17; `changelog.md`; `spec.md` lines 60-80; `overview.md`'s
divergence rows; `phases/phase-1.md` lines 18-40 and `phases/phase-2.md`
lines 64-74; `skills/settle/SKILL.md` lines 80-125;
`skills/implement/SKILL.md` line 425. The probe file, every repository it
built, the clone and the clone's virtualenv are deleted after this round.

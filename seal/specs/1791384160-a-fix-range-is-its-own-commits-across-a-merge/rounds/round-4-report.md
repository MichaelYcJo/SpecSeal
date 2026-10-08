# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — review round 4 report

Reviewer: specseal:warden on Opus 5.5. Target SHA
e0e01532f64d65e286a9009e655e4bcc4272a8da (draft PR #878 into
`release/v0.21.0`, labelled `chain: reframed`). Target diff `a15c4057..e0e01532`,
20 files, seven commits: phases 5–7 of the reframe after round 3.

## What this round was asked

This is the redesign's first finding round. Rounds 1–3 stopped on a second fix
of a fix, the framer reframed the item (`spec.md` §*Reframed after round 3*,
S14–S18; `plan.md` §*Reframe after round 3*), and the smith built phases 5–7.
Round 3's four findings were `deferred the frame` and are the redesign's
agenda. The spawn asked six things: whether the owner sentence equals what
`own_commits` runs, whether any carrier still defines, whether the guard can
be passed by a false sentence or refuses a true one, whether every shape case
can fail, whether the `head_ref` change is a contract change and safe where CI
sets nothing, and whether the restated ledger rows and the changelog are true.

Coordinates were carried from `rounds/round-1.md` to `round-3.md` and opened
where they pointed; no earlier verdict was carried as a conclusion.

## How the findings relate

The reframe works where it was aimed. Every round-3 finding is answered, the
shape cases are real can-fail cases, and the code is unchanged. What remains
comes from one source: the reframe forbids derived claims, and a few derived
claims were written or reshaped by the redesign itself.

1. The home's second sentence adds a universal claim about readers that the
   same section contradicts (🟡 1).
2. The owner sentence's gloss is wider than the git command by one commit
   (⬜ 2).
3. The guard is a word list. It lets false sentences through and refused a
   true one, and the rewording it forced is less true than what it replaced
   (⬜ 3, ⬜ 4).
4. The fragment section's new input sentence keeps one shape clause the guard
   does not read (⬜ 5).

## Findings

### 🟡 1 The home says every reader of a range imports `own_commits`, and three readers in the same two scripts do not

Read. `docs/the-record-layout.md:125` says the owner test is what
`own_commits` runs, "and every reader of a range in `round-record` and
`chain-check` imports it." Three readers of a range in those scripts do not:

- the `Fix range` count on the writer side, `round_record.py:4503`, is `git
  rev-list --count a..b`;
- the same count on the checker side, `chain_check.py:1992`, is the same
  command;
- the fragment notice's clearing step, `chain_check.py:4623`, runs its own
  `git rev-list --ancestry-path ^<target>` over the fragment commits.

The same section says so itself four paragraphs later: "the count and the
surface read one range two ways." The sentence is new in this diff, and it is
a claim derived from the rule rather than the rule. That is the shape the
reframe was written to stop. A maintainer adding a range reader would read
this sentence as saying the count already goes through `own_commits`, when
§*Out* of `spec.md` keeps it apart on purpose.

The fix is to drop the clause. The paragraph keeps the owner sentence, what it
does not read, and the pointer to the shape module.

### ⬜ 2 The owner sentence's gloss includes the start itself, which git never lists

Read, and executed. The git half of the owner sentence matches the call at
`chain_check.py:4510`. The extra flags there (`--no-renames --name-status -z
--format --reverse`) change what is printed for each commit and its order,
never which commits are listed. The gloss after the colon, "a non-merge
commit that has `a` as an ancestor and that `b` reaches," is wider by one
commit: `a` itself. Git's own ancestry test is reflexive. The probe's `git
merge-base --is-ancestor T T` exits 0, and this module's `parse_range` uses
that reflexive reading through `chain.is_ancestor`. Under that reading, `a`
has `a` as an ancestor and `b` reaches it. But `own_commits(T, HEAD)` does not
list `T` (executed).

The leading clause, "exactly the commits … lists," still governs. A `fixed`
row naming `a` is refused with a message, so nothing goes wrong silently. The
rule-17 pin and ledger row 16 quote the sentence, so a fix touches all three.

### ⬜ 3 The guard passes false sentences outside its list and refuses true ones across whole docstrings

Executed. I pasted each of three false sentences into the home's section, and
`tests/test_the_range_rule_states_no_shape.py` stayed green, 7 passed each
time:

- "A commit a merge brought in is never one of the range's own commits."
  Shape A is the counterexample.
- "A commit on the base after the base merged `a` is not owned." Shape A
  again.
- "An own commit on a branch cut before `a` never descends from `a`." Shape
  B2 is the counterexample. The list's last pattern catches only the "descends
  from X never" word order.

Restoring the true row `fragment_left_behind` carried before phase 6 ("squashed
away") turns the docstring case red. The reason is that the guard reads the
four docstrings whole, including rows that are not about ownership.
`phases/phase-6.md` records that this is why the row was reworded (⬜ 4).

This is how a word list behaves, and the spec designed it as one (S16 asks
only that no listed word appears). The defect is the module's own claim. Its
docstring says it "keeps the shapes out of the prose," and that is wider than
what it does. The barrier against a shape sentence is the home's rule plus
review; the guard catches the sentences the rounds already found.

### ⬜ 4 The silent-state row the guard forced is less true than the one it replaced

Read. `skills/code-review/scripts/chain_check.py#fragment_left_behind`, the
row at `chain_check.py:4585`, now says round 1's target is "gone from this
clone once its branch merged." The row it replaced said "squashed away,"
which was true. A branch merged with a merge commit keeps its target, both in
the clone and as an ancestor of the base. A squashed branch's target often
stays in a local clone too, and is only off HEAD's history. This plugin ships
to repositories that merge with merge commits. The state is hard to reach,
because `chain_check` reads only the declarations naming the branch it runs
on, so the row costs a reader a wrong expectation and does not change
behaviour.

### ⬜ 5 The fragment section's input sentence keeps a shape clause the guard does not read

Read, and executed. `docs/the-record-layout.md:102–103` says the merge ref's
range holds every base commit with round 1's target as an ancestor, "which a
branch checkout that has not merged the base does not hold." Whether that
holds depends on what "merged" means. In #805's own history the branch was
rebuilt on the base with its old tip merged in, and never ran a merge of the
base. I built that history after the base had merged `T`, and the branch
owned the base's `S` exactly as the merge ref did: `['S', 'f1', 'f2']` on both
checkouts. Under `git branch --merged`'s meaning the clause is true, and the
sentence's conclusion, "CI can name a commit a local run does not," holds
either way. The clause adds a shape and no information. The guard does not
read this section (`phases/phase-6.md`).

## What the account claimed, and what I found

- **"No code unit's logic changed except that the fragment notice's `check`
  and `judged` gained a `head_ref` argument."** Read: in
  `skills/code-review/scripts/chain_check.py` and `round_record.py` the diff
  changes docstrings only. `check` and `judged` are not the notice's units.
  They are helpers of the test module,
  `tests/test_a_fragment_left_behind_is_named.py#check` and `#judged`, and
  the shipped scripts' interfaces are unchanged. `head_ref` defaults to None,
  every existing caller passes the same arguments as before, and the helper
  deletes `GITHUB_HEAD_REF` first, so a case that passes nothing reads exactly
  as before. Setting it reproduces what `chain_check.py:1350` reads in a
  workflow, which GitHub sets on every `pull_request` run. Where CI sets
  nothing, the code reaches the branch name or the reason it already reports,
  which this diff does not touch. It is not a contract change of shipped code.
  Whether `close` over this range lists the two helpers under `Contract
  changes` with reach `pytest only` was not run (unverified; the orchestrator
  answers it at `close`).
- **"Every case turns red under one of two `own_commits` mutations."**
  Executed, and confirmed. With `--ancestry-path` dropped, A2, B, B3 and C go
  red. With `--first-parent` added, A, B2, D and S17's fragment case go red.
  All eight are covered, and the split matches `phases/phase-5.md`'s table
  row for row.
- **"The guard refuses shape/time vocabulary plus `descends? from \S+
  never`."** Executed: it does, and that is all it does (⬜ 3).
- **"Ten modules 531 passed; `survivor-check` and `evidence-check --strict`
  exit 0."** I did not rerun the smith's ten. I ran my own set, listed under
  Executed probes, and both checkers at exit 0.

## Round 3's findings, answered

- 🟡 1, CI reads the same commits as the branch: the equality is gone.
  Lines 100–104 state the input instead, and S17's case pins both checkouts.
  `--first-parent` turns it red (executed).
- 🟡 2, the home's examples by shape and time: the home carries none. The
  shapes are now seven cases, C and B3 among them, asserting what round 3's
  probes printed (`{"f2"}` and the empty set).
- 🟡 3, the B3 example in the `own_commits` docstring: gone. The docstring
  names the git command, the home and the shape module.
- ⬜ 4, the ledger row and `phases/phase-1.md`: both restated. The
  `Corrected · S1, S5, S8, S10` row no longer says the branch and CI read the
  same commits, and states the S17 input. It keeps one #805 clause ("a merge
  made from the base's side below HEAD reads the item's own commits"). That
  clause is true by definition, though it is the kind of shape example S18's
  wording excludes.

The changelog fragment was read against the owner sentence and is true. Its
CI sentence ends at "CI can name a commit a local run does not," without
⬜ 5's clause.

## Regression tests to plant

- None owed for 🟡 1. It is a sentence to drop, and no word list would catch
  "every reader" without refusing true sentences.
- For ⬜ 2, if the sentence changes, rule 17 in
  `tests/test_the_rules_have_one_owner.py` pins the new text. Seeing it red
  means deleting "other than `a`" from the home.

## Facts for the evidence ledger

- If 🟡 1's fix lands, nothing in the fragment changes: no row states "every
  reader."
- If ⬜ 2's fix lands, row 16 (`S12, S14, S16`) quotes the owner sentence and
  is restated with it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The home says every reader of a range in the two scripts imports `own_commits`; the `Fix range` count on both sides and the notice's clearing step read the range with their own `rev-list`, and the same section says the count reads it another way | `docs/the-record-layout.md:125` | open | read: `round_record.py:4503`, `chain_check.py:1992`, `chain_check.py:4623`, and the section's fourth paragraph |
| ⬜ 2 | The owner sentence's gloss, "a non-merge commit that has `a` as an ancestor and that `b` reaches", includes `a` under git's reflexive ancestry, which the git command never lists | `docs/the-record-layout.md:122` | open | executed: `merge-base --is-ancestor T T` exits 0, `own_commits(T, HEAD)` omits `T`; read: `parse_range` uses the reflexive test |
| ⬜ 3 | The guard's docstring says it keeps shapes out of the prose; three false sentences outside its list pass it, and it refused a true docstring row because it reads the four docstrings whole | `tests/test_the_range_rule_states_no_shape.py:10` | open | executed: three pastes into the home, 7 passed each; the restored "squashed away" row turns the docstring case red |
| ⬜ 4 | The silent-state row the guard forced says round 1's target is gone once its branch merged; a merge commit keeps it, and the replaced "squashed away" was true | `skills/code-review/scripts/chain_check.py#fragment_left_behind` | open | read: `chain_check.py:4585`, `phases/phase-6.md` naming the rewording; behaviour unchanged |
| ⬜ 5 | The fragment section's input sentence adds "which a branch checkout that has not merged the base does not hold", a shape clause outside the guard, and in #805's rebuilt history the branch holds those commits without merging the base | `docs/the-record-layout.md:102` | open | executed: the rebuilt branch and the merge ref both give `['S', 'f1', 'f2']`; true under the `git branch --merged` reading |
| 🟢 | round 3's finding 1 is closed — the fragment section states the notice's input instead of an equality, and S17's case pins both checkouts | `docs/the-record-layout.md:100` | confirmed | executed: the case is red with `--first-parent` added; read: the equality sentence is gone |
| 🟢 | round 3's finding 2 is closed — the home states no example, and the shapes are cases | `tests/test_a_range_owns_what_git_lists_for_it.py` | confirmed | executed: the module passes, and every case is red under one of the two mutations |
| 🟢 | round 3's finding 3 is closed — the `own_commits` docstring names the git command, the home and the shape module | `skills/code-review/scripts/chain_check.py#own_commits` | confirmed | read: the docstring; the guard's docstring case for it passes (executed) |
| 🟢 | round 3's note 4 is closed — the corrected ledger row and the phase 1 correction are restated in the owner's terms | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:4` | confirmed | read against the owner sentence; one #805 clause remains and is true by definition; `evidence-check --strict` exit 0 (executed) |
| 🟢 | the `head_ref` argument is a test helper's, defaulted, and mirrors the workflow's `GITHUB_HEAD_REF`; no shipped interface changed | `tests/test_a_fragment_left_behind_is_named.py:181` | confirmed | read: the two scripts' diff is docstrings only; `chain_check.py:1350` reads the same variable |
| 🟢 | the changelog fragment is true against the owner sentence | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:27` | confirmed | read; its CI sentence carries no shape clause |
| ❓ | whether `close` over the redesign's range lists `check` and `judged` under `Contract changes` | `tests/test_a_fragment_left_behind_is_named.py#check` | ❓ out of verified scope | not run this round; the orchestrator answers it when it runs `close` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 — `docs/the-record-layout.md`, the home's first paragraph

```markdown
**A range `a..b` owns exactly the commits `git log --ancestry-path
--no-merges a..b` lists: a non-merge commit that has `a` as an ancestor and
that `b` reaches.** That is the whole test `chain_check.py#own_commits` runs.
It does not read which parent of a merge a commit sits behind, which branch
the commit was made on, or when it was made. Whether a given commit of a
given history is owned is answered by running `own_commits` on that history.
```

### ⬜ 2 — the owner sentence, in the home and in rule 17

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

### ⬜ 3 — `tests/test_the_range_rule_states_no_shape.py`, the module docstring's claim

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

### ⬜ 4 — `chain_check.py#fragment_left_behind`, the silent-state row

```text
      round 1's target           not fetched into this clone, or left out
      unresolvable, or not an    of HEAD's history when its branch merged
      ancestor of HEAD           as one new commit, or off the branch after
                                 a rebase. Walking `<target>..HEAD` from a
                                 commit HEAD does not descend from reads the
                                 build itself as late
```

### ⬜ 5 — `docs/the-record-layout.md`, the fragment section's input sentence

```markdown
move lists both its paths, so a file moved under `tests/` is named. The
notice reads `<round 1's Target SHA>..HEAD` wherever it runs. On CI's
checkout HEAD is the pull request merged into its base, so there the range
also holds every base commit that has round 1's target as an ancestor, and
CI can name a commit a branch checkout does not.
```

Needs a fix: yes — 🟡 1 (the home says every reader of a range imports `own_commits`, and the `Fix range` count and the notice's clearing step do not)
Loses a record or crashes: no

## Proof — files opened

- `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md`
  (§*In*, §*Reframed after round 3*, §*Out*, the scenarios, §*Data &
  interfaces*)
- `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/plan.md`
  (§*Reframe after round 3*, the phases table)
- `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/rounds/round-3.md`
- `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/phases/phase-5.md`
  (the mutation table) and `phases/phase-6.md` (the guard's notes)
- `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md`
- `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md`
  (every row's claim)
- the diff `a15c4057..e0e01532` of `docs/`, `skills/`, `tests/` and the
  item's `overview.md`, `phases/phase-1.md`, `questions.md` and `survivors.md`
- `docs/the-record-layout.md:96–160`
- `skills/code-review/scripts/chain_check.py` (lines 40–62, 1330–1370, and
  4420–4660)
- `skills/code-review/scripts/round_record.py` (lines 60–100, 2395–2425,
  3340–3420, 4160–4200, and 4415–4460)
- `tests/test_a_range_owns_what_git_lists_for_it.py` and
  `tests/test_the_range_rule_states_no_shape.py`, whole
- `tests/test_a_fragment_left_behind_is_named.py` (lines 140–200 and 456–480,
  and the new S17 case)
- `bin/test`

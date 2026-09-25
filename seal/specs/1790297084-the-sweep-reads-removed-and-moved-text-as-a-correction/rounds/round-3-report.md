# 1790297084 — review round 3 report (verifying round, run capped)

Target SHA: `de177dae5fc3daab5c34101118d243a02c374c5e`. Fix range under
review: `dc9fb40c..6ffa4aef`, 2 commits (round 2's fixes); `de177dae` only
closes round 2's record. This round answers round 2's five verdicts and judges
the two new units round 2's `New units` row names. It did not re-read the
branch. The run is capped: nothing found here is fixed on this branch, so each
finding carries a deferral candidate.

## Summary

The code fixes hold. The statement fix does not.

- **Round 2's 🟡 1 (the count guard) is closed.** Against the real ledgers,
  every one of the 31 rows in the 13 repeated `(heading, id)` groups behaves
  both ways: removed with its anchors gone, it takes the exit; corrected in
  place with every anchor renamed, it stays measured. At `66df04df` the same
  probe had all 31 removals kept measured. Reverting the guard to membership
  turns the planted case red.
- **Round 2's 🟡 2 (`P1-1`) is closed.** All 520 id-bearing anchored rows,
  the 14 hyphenated ones included, stay measured when corrected in place with
  every anchor renamed. Reverting the pattern turns the planted case red.
- **Round 2's ⬜ 4 and ⬜ 5 are closed.** The same-line tie case goes red
  without `raw` in the key. P3 states the condition as built, and
  `bin/evidence-check .` exits 0.
- **Round 2's 🟡 3 is not closed (🟡 1 below).** The three statements of the
  silent set now say that rows are silent which the check measures. They also
  disagree with each other, and the function's own enumeration misses one
  silent shape. The count they cite is the pre-widening one (⬜ 2).

Two residuals are ⬜: the `>=` half of the count guard is pinned by no case
(⬜ 3), and 28 older ledger rows carry id-like heads the pattern does not read
(⬜ 4). Both behave as documented. Neither loses a record or crashes.

## Findings

### 🟡 1: the silent set is now stated wider than it is, and three ways

The rule as built (`skills/code-review/scripts/survivor_check.py:1127` and
the fallback at `:1140-1145`) is a conjunction. A row corrected in place, with
an anchor renamed or gone, goes silent only when **both** hold:

1. the id does not name it: no id `ROW_ID` reads, its own heading retitled or
   the row moved section, or its `(heading, id)` count fell; **and**
2. no live row of the file cites every anchor of it that still resolves:
   every anchor renamed or gone, or a still-resolving one dropped and cited
   by no other row.

The three statements written in `6ffa4aef` flatten that into alternatives.
Executed at the target, in the round's clone, through the module's own
`ledger_range` helper:

| Shape | Exit | What the statements say |
|---|---|---|
| S1: no id, one anchor renamed, the other kept and still cited | 1, measured | spec: *goes silent if it has no id* |
| S2: id, own heading retitled, one anchor renamed, the other kept | 1, measured | function: shape 1; module: *renamed its own section heading*; spec: *changed section* |
| S3: id standing, a still-resolving anchor dropped with the rename | 1, measured | spec: *dropped an anchor* |
| S4: id lost a sibling, every anchor renamed | 0, silent | function: in none of the four shapes (shape 3 needs a dropped anchor, shape 4 needs no id) |
| S5: moved to another section, one anchor renamed, the other kept | 1, measured | function: shape 2; module: *moved it to another section*; spec: *changed section* |
| S6: own heading retitled, every anchor renamed | 0, silent | all three, correctly |

So, statement by statement:

- **`docs/review-chain-spec.md:924-928`.** The first sentence (*where its id
  stands under the same heading, and otherwise only while a live row cites
  every anchor it kept*) is right. The *So* sentence after it is contradicted
  by each of its disjuncts taken alone (S1, S2, S3, S5).
- **Module docstring, `survivor_check.py:198-201`.** Of its four silencing
  conditions, *renamed every anchor it kept* and *dropped one along with a
  rename* are right. *Renamed its own section heading* and *moved it to
  another section* are reasons the id stops naming the row, not reasons the
  row goes silent (S2, S5).
- **Function docstring, `survivor_check.py:1078-1087`.** The bold umbrella
  (*a row corrected in place, with an anchor renamed or gone, that the id does
  not name*) is contradicted by S1, S2 and S5. The *four shapes* are wider
  than the code in shapes 1 and 2 and narrower in missing S4.

Why it matters: round 2's 🟡 3 was opened because the statement disagreed
with the code, and it still does, now in the other direction as well. A
reader deciding whether an id-less row, corrected with one anchor renamed, is
still measured gets *no* from the policy document. The code says yes. The
module docstring defers to the function's docstring (*states the whole set*),
and that docstring also leaves out S4. The ledger fragment's P3 is the one
statement that matches the code, because it states the condition rather than
enumerating its outcomes.

This is a statement defect, and the probes show the behaviour is the
documented design. The pairing that would close the silent set was not built
on purpose, and this finding does not ask for it.

### ⬜ 2: the id-less count is the one from before `P1-1` was read

`survivor_check.py:1084` says *298 of about 800*, and `:201` and
`docs/review-chain-spec.md:927` say *about 37%*. Executed at the target over
all 33 ledger files: 800 anchored rows, of which 280 (35.0%) carry no id
`ROW_ID` reads. With the pattern from before `14546dd3` the same survey reads
294 (36.8%). The figure was measured before round 2's own widening and never
re-measured after it. The paste-ready fix under 🟡 1 carries the corrected
number.

### ⬜ 3: the "count grew" half of the guard is pinned by nothing

`survivor_check.py:1127` reads `>=`. Mutated to `==`, the seven id-rule cases
stay green, so no case pins a correction that splits one row into two under
the same id. Under `==` that split falls to the anchor rule and goes silent
once its anchor was renamed. A case for it is below. Executed at the target it
passes, and under the `==` mutation it fails, so it has been seen red.

### ⬜ 4: 28 older rows carry id-like heads `ROW_ID` does not read

Round 2's 🟡 2 was the `P1-1` instance. Enumerating the class at the target:
28 anchored rows in `seal/releases/0.4.0.md` (4), `seal/releases/0.5.0.md`
(20) and `seal/releases/0.10.0.md` (4) open their first cell with a
finding-shaped id before ` · ` (`🟡 2`, `🔴 1`, `r3 4`, and compound ones
such as `S4 / S12` or `🟡 1 / 🟡 4 / r3 1`). They are among the 280 id-less
rows, so they fall to the anchor rule exactly as the statements say. The
compound ones name more than one row and cannot be one id. Reading the single
ones is a choice for whoever takes up the pairing, and no behaviour differs
from what is documented.

## Regression tests to plant

- `tests/test_a_corrected_sentence_survives_elsewhere.py`: the split-row case
  in ⬜ 3's fence below, beside the hyphenated-id case.

## Facts for the evidence ledger

- At `de177dae`: 800 anchored ledger rows over 33 files; 280 carry no id
  `ROW_ID` reads; 13 `(heading, id)` groups of 31 rows repeat an id, all in
  `seal/releases/0.14.0.md` and `seal/releases/0.5.0.md`. Executed.
- `removed_ledger_rows` keeps a row corrected in place measured whenever a
  live row cites every still-resolving anchor of it, whatever its id (S1, S2,
  S5 above). Executed. This is the claim a corrected statement should rest on.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | round 2's 🟡 3 is not closed: the three statements of the silent set call measured rows silent (S1, S2, S3, S5), disagree with each other, and the function's four shapes miss S4 | `docs/review-chain-spec.md:926` | deferred new issue | Executed: six shapes at target, exits as tabled; the fix is the three texts in the paste-ready block, no code. The run is capped and the units are existing ones edited in `6ffa4aef`; the orchestrator files the issue, labelled `from-review` |
| ⬜ 2 | the id-less share is stated as 298 / about 37%, measured before `P1-1` was read; at target it is 280 of 800, 35.0% | `skills/code-review/scripts/survivor_check.py:1084` | deferred new issue | Executed: survey of 33 ledger files at target, and 294 with the old pattern; the same issue as 🟡 1, whose paste-ready text carries the number |
| ⬜ 3 | the `>=` half of the count guard (a correction splitting one row into two under its id) is pinned by no case | `skills/code-review/scripts/survivor_check.py:1127` | deferred new issue | Executed: `==` mutation leaves the seven id-rule cases green; the fenced case passes at target and fails under `==` |
| ⬜ 4 | 28 anchored rows in 0.4.0, 0.5.0 and 0.10.0 open with id-like heads (`🟡 2 ·`, `r3 4 ·`, `S4 / S12 ·`) that `ROW_ID` does not read | `skills/code-review/scripts/survivor_check.py:1030` | deferred new issue | Executed: enumeration at target; they fall in the documented anchor fallback, so behaviour matches the statement; whether to read them belongs with the pairing |
| 🟢 | round 2's 🟡 1 is closed — a shared id no longer keeps a removed row of its group measured | `skills/code-review/scripts/survivor_check.py:1127` | verified | Executed: all 31 rows of the 13 real groups, removal taken and correction measured; at `66df04df` all 31 removals kept measured; membership mutation turns the planted case red |
| 🟢 | round 2's 🟡 2 is closed — `P1-1 ·` ids are read | `skills/code-review/scripts/survivor_check.py:1030` | verified | Executed: 520 id rows (14 hyphenated) corrected in place with every anchor renamed, 0 silent; pattern reverted turns the hyphenated case red |
| 🟢 | round 2's ⬜ 4 is closed — two tied sentences on one line print in one order | `skills/code-review/scripts/survivor_check.py:1564` | verified | Executed: `raw` removed from the key turns the 16-seed case red; the case passes at target |
| 🟢 | round 2's ⬜ 5 is closed — P3's closing clause states the condition as built | `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` | answered | Read: P3 names the counted id and the anchor fallback, matching the code; executed: `bin/evidence-check .` exit 0 at target |
| carried | round 2's confirmations of #591, #592 and the missing-checker refusal | `skills/code-review/scripts/survivor_check.py` | confirmed | Read: the fix range touches `ROW_ID`, `removed_ledger_rows`, `score` and two docstrings only, never `corrected`, `paired_across_paths` or `evidence` |
| ❓ | PR #609's `pytest (windows-latest, 3.12)` leg at `de177dae` | PR #609 checks | ❓ out of verified scope | pending when this round ended; the orchestrator reads it before the sealer's spawn |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -p no:xdist -k` over the id-rule, tie and hyphenated cases, at `de177dae`, in the round's clone | 9 passed |
| Mutations, one at a time, each against its case: guard to membership; `ROW_ID` without `(?:-\d+)?`; `raw` out of the sort key; guard to `==` | 1 failed; 1 failed; 1 failed; 7 passed (⬜ 3) |
| Real-ledger count-guard probe: `removed_ledger_rows` over each of the 31 grouped rows, with anchor resolution patched per row (removed with every anchor gone, removed with one gone, corrected with every anchor renamed, corrected with a sibling removed) | at target: 31/31 taken, 31/31 taken, 31/31 measured, 31/31 corrected row silent and sibling taken. At `66df04df`: 0/31 taken on both removals |
| Every id-bearing anchored row, corrected in place with every anchor renamed, same probe | 520 rows (14 hyphenated), 0 silent; at `66df04df` 506 rows, the 14 `P1-1` rows not read as ids |
| Six silent-set shapes through the module's `ledger_range` helper, at target | S1 1, S2 1, S3 1, S4 0, S5 1, S6 0 (🟡 1's table) |
| Split-row case (⬜ 3's fence) at target and under the `==` mutation | 1 passed; 1 failed |
| Survey of the 33 ledger files at target: anchored rows, id-less rows, id-like heads missed | 800; 280 (35.0%), 294 with the old pattern; 28 id-like heads, 3 of them not ids (`S-row`, `S1–S4`, `S7–S10`) |
| `bin/evidence-check .` at target | exit 0 |
| `gh pr checks 609`, head `de177dae` | lint pass, ledger pass, pytest ubuntu pass, pytest macos pass, pytest windows pending; release fail |
| The `release` leg's failure, read from its log | `chain_check` refuses round-2.md: `Pass` checked beside `Fixes checked by: nobody`. This round is the verifying round that cell asks for, so the leg should clear once round-3.md names it. Not a code defect |
| The broad gate: full suite, repository-wide lint and typecheck | not yet. Nobody has run it. It is the sealer's. With this round closing the run, the sealer's spawn is due |

```python
# The count-guard probe's core, as run (probe file deleted with the round directory).
# Anchor resolution is patched so a chosen set of anchors fails at the right end.
for p, key, v in groups:
    for n, h, i, l in rows_of(key):
        a = cited(l)
        after = lines_without(n)
        assert (p, n) in run({p: texts[p]}, {p: after}, a)          # removed: exit taken
        cor = lines_with(n, l.replace("·", "· corrected ·", 1))
        assert (p, n) not in run({p: texts[p]}, {p: cor}, a)        # corrected: measured
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1, ⬜ 2, ⬜ 3, ⬜ 4: the silent set's statements, its count, the unpinned `>=` direction, and the id-like heads the pattern does not read | a new issue, labelled `from-review`, which the orchestrator files at the capped exit, since #603 closes with this pull request and no open issue owns the ground | the orchestrator files it, and the repository owner schedules it; the text fix in it needs no design decision, while the pairing it points at does |

## Paste-ready fixes

### 🟡 1 and ⬜ 2

`removed_ledger_rows`' docstring, replacing its last paragraph:

```text
    **What stays silent is a row corrected in place, with an anchor renamed
    or gone, that neither rule keeps.** The id does not name it -- it has no
    id `ROW_ID` reads, its own section heading was retitled or it moved to
    another section in the same range, or its id lost a sibling row -- and
    no live row of the file cites every anchor of it that still resolves:
    every anchor was renamed or gone, or the corrected line dropped one that
    still resolves and no other row cites the rest. A row the id does not
    name whose corrected line still cites each anchor it kept stays
    measured. It is not a rare corner: 280 of the 800 anchored rows in this
    repository's ledger (35%) carry no id the pattern reads. Pairing a
    removed line with the added line that replaced it would close it, and
    that is a design choice beyond this branch (round 2's 🟡 3)."""
```

The module docstring, from "same heading. A row the id does not name":

```text
same heading. A row the id does not name -- no id, a lost sibling, or a
section retitled or changed -- falls back to its anchors, and goes silent
only when no live row cites every anchor of it that still resolves: the
correction renamed every anchor it kept, or dropped one along with a rename
(`removed_ledger_rows` states the whole set). About 35% of anchored rows
here carry no id, so that is not a rare corner.
```

`docs/review-chain-spec.md`, the sentence after "every anchor it kept.":

```text
every anchor it kept. So one whose correction renamed an anchor goes silent
only when both fail: the id does not name it (it has no id, as about 35% of
rows do; its id lost a sibling; or it changed section), and no live row cites
what it kept (every anchor was renamed, or a kept one was dropped). In a
`.py` file only
```

### ⬜ 3

```python
def test_a_claim_split_into_two_rows_as_it_is_corrected_stays_measured(tmp_path):
    """A row corrected in place and split across two rows under its id, its
    anchor re-pointed at the renamed unit. The id stands more times at the
    tip than at the left end, so it still names the row. Red with the count
    guard read as equality: exit 0."""
    repo = tmp_path / "probe"
    renamed = MODULE.replace("def helper(", "def helper_renamed(")
    half = ledger_row(REPAIRED, ("pkg/mod.py#helper_renamed",))
    head = ledger_range(
        repo,
        half + ledger_row("The rest of the claim.", ("pkg/mod.py#other",)),
        renamed,
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a split correction lost its row:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text
```

Needs a fix: yes — 🟡 1 (the silent set's three statements call measured rows silent and miss one silent shape), deferred to a new issue as the capped exit requires.
Loses a record or crashes: no

## Proof block

Files opened this round:

- `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/rounds/round-2.md`
- `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/rounds/round-2-report.md` (head)
- `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/changelog.md`
- `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` (P3, and the fix-range word diff)
- `skills/code-review/scripts/survivor_check.py` (`:190-205`, `:999-1146`, `:1560-1566`, and the fix-range diff)
- `skills/evidence-check/scripts/evidence_check.py` (`ANCHOR_RE`, `resolve_unit` signature)
- `tests/test_a_corrected_sentence_survives_elsewhere.py` (the ledger helpers and the fix-range diff)
- `docs/review-chain-spec.md` (`:920-929`, `:486-500`)
- `skills/code-review/scripts/round_record.py` (the `deferred` reading, by search)
- `bin/test`
- PR #609's checks and the `release` leg's failed log

The round's clone, its virtual environment and every probe file lived under
the round's own scratchpad directory and were removed with it.

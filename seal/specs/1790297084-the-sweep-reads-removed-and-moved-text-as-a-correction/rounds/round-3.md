# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — review round 3

| Field | Value |
|---|---|
| Target SHA | de177dae5fc3daab5c34101118d243a02c374c5e |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 609 |
| Broad gate | 6a9b72b0 against a53699ec; earlier run: 7fcd328c against 7b557144 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (the silent set's three statements call measured rows silent and miss one silent shape), deferred to a new issue as the capped exit requires. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790297084 is the verifying round after the run's one reopening. It reads round 2's fixes (dc9fb40c..6ffa4aef) at de177dae and ends the run whatever it finds. It asks whether the count guard, the widened ROW_ID and the raw sort key close round 2's findings against the real ledgers in both directions, whether the three statements of the silent set agree with each other and with the code, and whether PR #609's CI is green at that tip.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | round 2's 🟡 3 is not closed: the three statements of the silent set call measured rows silent (S1, S2, S3, S5), disagree with each other, and the function's four shapes miss S4 | `docs/review-chain-spec.md:926` | deferred #615 | Executed: six shapes at target, exits as tabled; the fix is the three texts in the paste-ready block, no code. The run is capped and the units are existing ones edited in `6ffa4aef`; the orchestrator files the issue, labelled `from-review` |
| ⬜ 2 | the id-less share is stated as 298 / about 37%, measured before `P1-1` was read; at target it is 280 of 800, 35.0% | `skills/code-review/scripts/survivor_check.py:1084` | deferred #615 | Executed: survey of 33 ledger files at target, and 294 with the old pattern; the same issue as 🟡 1, whose paste-ready text carries the number |
| ⬜ 3 | the `>=` half of the count guard (a correction splitting one row into two under its id) is pinned by no case | `skills/code-review/scripts/survivor_check.py:1127` | deferred #615 | Executed: `==` mutation leaves the seven id-rule cases green; the fenced case passes at target and fails under `==` |
| ⬜ 4 | 28 anchored rows in 0.4.0, 0.5.0 and 0.10.0 open with id-like heads (`🟡 2 ·`, `r3 4 ·`, `S4 / S12 ·`) that `ROW_ID` does not read | `skills/code-review/scripts/survivor_check.py:1030` | deferred #615 | Executed: enumeration at target; they fall in the documented anchor fallback, so behaviour matches the statement; whether to read them belongs with the pairing |
| 🟢 | round 2's 🟡 1 is closed — a shared id no longer keeps a removed row of its group measured | `skills/code-review/scripts/survivor_check.py:1127` | verified | Executed: all 31 rows of the 13 real groups, removal taken and correction measured; at `66df04df` all 31 removals kept measured; membership mutation turns the planted case red |
| 🟢 | round 2's 🟡 2 is closed — `P1-1 ·` ids are read | `skills/code-review/scripts/survivor_check.py:1030` | verified | Executed: 520 id rows (14 hyphenated) corrected in place with every anchor renamed, 0 silent; pattern reverted turns the hyphenated case red |
| 🟢 | round 2's ⬜ 4 is closed — two tied sentences on one line print in one order | `skills/code-review/scripts/survivor_check.py:1564` | verified | Executed: `raw` removed from the key turns the 16-seed case red; the case passes at target |
| 🟢 | round 2's ⬜ 5 is closed — P3's closing clause states the condition as built | `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` | answered | Read: P3 names the counted id and the anchor fallback, matching the code; executed: `bin/evidence-check .` exit 0 at target |
| carried | round 2's confirmations of #591, #592 and the missing-checker refusal | `skills/code-review/scripts/survivor_check.py` | confirmed | Read: the fix range touches `ROW_ID`, `removed_ledger_rows`, `score` and two docstrings only, never `corrected`, `paired_across_paths` or `evidence` |
| ❓ | PR #609's `pytest (windows-latest, 3.12)` leg at `de177dae` | PR #609 checks | ❓ out of verified scope | pending when this round ended; the orchestrator reads it before the sealer's spawn |

## Paste-ready fixes

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
```text
same heading. A row the id does not name -- no id, a lost sibling, or a
section retitled or changed -- falls back to its anchors, and goes silent
only when no live row cites every anchor of it that still resolves: the
correction renamed every anchor it kept, or dropped one along with a rename
(`removed_ledger_rows` states the whole set). About 35% of anchored rows
here carry no id, so that is not a rare corner.
```
```text
every anchor it kept. So one whose correction renamed an anchor goes silent
only when both fail: the id does not name it (it has no id, as about 35% of
rows do; its id lost a sibling; or it changed section), and no live row cites
what it kept (every anchor was renamed, or a kept one was dropped). In a
`.py` file only
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:1083` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1501` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/scripts/survivor_check.py:1273` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1341` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1003` | round 1's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1103` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1021` | round 2's 🟡 2 — fixed |
| round-2 | `skills/code-review/scripts/survivor_check.py:194` | round 2's 🟡 3 — fixed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1539` | round 2's ⬜ 4 — fixed |
| round-2 | `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/plan.md` | round 2's 🟢 — answered |
| round-2 | `skills/code-review/scripts/survivor_check.py` | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1, ⬜ 2, ⬜ 3, ⬜ 4: the silent set's statements, its count, the unpinned `>=` direction, and the id-like heads the pattern does not read | a new issue, labelled `from-review`, which the orchestrator files at the capped exit, since #603 closes with this pull request and no open issue owns the ground | the orchestrator files it, and the repository owner schedules it; the text fix in it needs no design decision, while the pairing it points at does |

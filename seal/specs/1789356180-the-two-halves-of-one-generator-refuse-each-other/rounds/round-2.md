# 1789356180-the-two-halves-of-one-generator-refuse-each-other — review round 2

| Field | Value |
|---|---|
| Target SHA | 5bf88c1 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 394 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 7 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round. Target is the diff of round 1's fixes, `c9912a4..5bf88c1`, four commits, and not the branch — everything before `c9912a4` had been reviewed by round 1. Round 1's record was committed and its six verdicts inherited; the job was the answers rather than new findings.

The exempt surface, handed over as a finding surface because units the fixes created have been reviewed by nobody: the six round 1's record names — `OWED_MARKERS` and five cases. The sharpest question was put on the constant, because `OWED_MARKERS` decides which severity markers mean *somebody owes this row an answer* and is the whole of what now separates an admitted row from a refused one. The round was asked what it holds, what it leaves out, and whether the set is the right set, with the fix pass's own stated residual — a reviewer who writes 🟢, ❓ or ⬜ on a row that really is an open finding is still not caught — given as the starting point rather than the conclusion.

Four acts of the fix pass were handed over as facts rather than left to rediscover: that it went past round 1's own paste-ready code because that code read the severity and an empty `#` cell carries none, so the empty cell round 1 had itself listed as half of the serious pair still came through; that round 1's 🟡 3 was understated, with all four separators broken rather than the comma alone; that the corrected corpus split was re-derived with the module's own reader before being written into nine places, after round 1's own first pass reproduced the frame's wrong numbers with a naive split; and that `survivor-check` found two stale claims round 1 did not flag, one left standing with a dated note and exempted rather than corrected. The round was asked to judge that exemption, it being the branch's only choice of an exemption over a correction.

One further claim was named as load-bearing for every record already in the tree and asked to be checked rather than taken: that `verdict_rows` has no reader outside `round_record.py`, so no gate re-reads the 44 committed letter-keyed rows under the new refusal.

What the orchestrator had already executed at `a28bb03`, handed over so the round would not repeat it: four modules — `test_a_finding_id_is_a_bare_integer.py`, `test_the_fixes_close_the_record.py`, `test_the_rules_have_one_owner.py`, `test_the_record_is_generated.py` — 282 passed, exit 0; `survivor-check --range c9912a4..a28bb03 --exempt …` exit 0; and `finding_number` and the `Pass` box computation read at their coordinates while verifying round 1's 🔴.

The round was told to number every row of its verdict table while noting that this branch now refuses a no-digit `#` cell carrying 🔴 or 🟡 and refuses an empty one, so the table is written against the generator as it stands on the branch. The broad gate was withheld by name as the sealer's single act after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's 🔴 1 is closed for the owed-marker and empty-cell arms: the refusal fires inside `new` before a record is written, and both arms die under mutation | `skills/code-review/scripts/round_record.py:2447`, `:3073` | answered | executed at `5bf88c1` — four owed parameters and the empty cell refuse at exit 2 with no record; dropping `not text or` turns the empty case red on its own |
| 2 | `OWED_MARKERS` holds the right pair: 🔴 and 🟡 are exactly the severities `Needs a fix` counts, ❓ is a closing verdict, ⬜ is defined as the one that never counts | `skills/code-review/scripts/round_record.py:2366` | answered | executed at `5bf88c1` — removing 🟡 from the tuple turns two of the four parameters red, so both members are pinned |
| 3 | Round 1's 🟡 2 is closed and the corrected split re-derives exactly: 199 / 51 / 44 letter-keyed / 7 admitted / 0 empty / 0 `✅` / 0 em dash, and 26 owed splitting 11 fixed, 4 answered, 11 open | `skills/code-review/scripts/round_record.py:2354`; `docs/review-chain-spec.md` §*A verdict row that commissions nothing*; `skills/code-review/SKILL.md`; `templates/sdd-round.md`; `phases/phase-1.md` | answered | executed at `5bf88c1` — re-derived through `table_body` and the unverified reader, not a naive split |
| 4 | Round 1's 🟡 3 is closed, and wider than round 1 read it: all four separators were broken when no space follows the word, not the comma alone | `skills/code-review/scripts/round_record.py:3025` | answered | executed at `5bf88c1` — reverting `head` to the anywhere-split turns all four parameters red; the case pastes the advised row back into `close` and asserts the verdict lands as `answered` |
| 5 | Round 1's 🟡 4 is closed — the home comes off the front of the note and the grounds survive | `skills/code-review/scripts/round_record.py:3000` | answered | executed at `5bf88c1` — reverting to the equality test turns the case red; it asserts the home appears once with the grounds still present |
| 6 | Round 1's ⬜ 5 is closed — an empty id list renders as `no numbered rows at all` | `skills/code-review/scripts/round_record.py:3262` | answered | executed at `5bf88c1` — removing the fallback turns the case red |
| 7 | 🟡 The admission rule reads the `#` cell's marker and never the Verdict cell, so six admitted shapes whose Verdict cell reads `open` still come through `new` at exit 0 with `Pass` ticked — round 1's 🔴 1 one cell over, and free to close | `skills/code-review/scripts/round_record.py:2447`, `:3063` | open | executed at `5bf88c1` — six shapes through `new`; the proposed fix applied in the clone closes all six with the two changed modules still at 113 passed, exit 0; zero committed rows change |
| 8 | ⬜ `survivors.md`'s round 1 fix-pass comment says *Five more* over a six-row table and names `plan.md` as absent from a table it is row 3 of; the row was added at `a28bb03` without the comment following | `seal/specs/1789356180-…/survivors.md:27` | open | read at `5bf88c1` — the table held five rows at `53d92ac` when the comment was written. A correction, under `seal/specs/`, and `Needs a fix` does not count it |
| 9 | ⬜ A report carrying both a malformed id and an owed row refuses on `bad` alone, so the mixed case costs two round trips — the #303 class, at one extra run rather than one per row | `skills/code-review/scripts/round_record.py:3073` | open | executed at `5bf88c1` — `R2-1` plus `🔴 A` refuses naming `R2-1` only |
| 10 | Round 1's finding 6 is closed: `seal/ledger.md` R1's clause now names what each table does and carries the severity rule | `seal/ledger.md`, row R1 · a finding id is a bare integer | answered | read at `5bf88c1` against `fix_table`, which passes `False` for `idless`, and against the admitting arm |
| 11 | The compatibility claim holds — `finding_number` and `verdict_rows` have no caller outside `round_record.py`, `inherited_rows` reads earlier records through `table_of` and `verdict_words`, and CI's hygiene job runs `chain_check.py`. The 44 committed letter-keyed rows are re-read by no gate | `skills/code-review/scripts/round_record.py`, `#inherited_rows`; `.github/workflows/hygiene.yml:191` | answered | executed at `5bf88c1` — the 26 owed rows located in 10 records across four shipped work items, none of them reachable by a gate |
| 12 | The `plan.md` exemption is right, and it persists: it is a survivors-table row rather than a one-off flag, the quote is its anchor, and the grounds name what would be falsified by the alternative. `phases/phase-1.md`'s neighbouring sentence was corrected instead, which is the correct side of that line | `seal/specs/1789356180-…/survivors.md`; `plan.md:72`; `phases/phase-1.md:64`; `skills/verify/scripts/broad_gate.py:584` | answered | read at `5bf88c1` — the broad gate and CI both pass every `seal/specs/*/survivors.md` as `--exempt`; the `<!-- CORRECTED -->` form is used by seven files across five work items |
| 13 | §14 and §15 hold — `58511d0` carries code, cases and all four prose carriers together, and every one of the five new cases was seen red by reverting the line it pins | `58511d0` | answered | executed at `5bf88c1` — six mutations, each killing its own case |
| 14 | The record's `New units` row names exactly the six units the fix commits create, and each has been reviewed here | `seal/specs/1789356180-…/rounds/round-1.md` | answered | read at `5bf88c1` — one module-level constant and five test functions; no seventh in the diff |

## Paste-ready fixes

```python
OWED_MARKERS = ("\N{LARGE RED CIRCLE}", "\N{LARGE YELLOW CIRCLE}")
# The one verdict word that says the row is open in as many letters. It is
# read only on a row whose `#` cell already admitted it, where the two cells
# then contradict each other, and it is exact rather than a vocabulary test:
# `verified` is in no vocabulary and therefore OPEN, which is why reading the
# verdict as OPEN/CLOSED cannot serve -- and why reading this one word can.
# Free against the corpus: of the 25 admitted no-digit rows in the committed
# records, not one has a Verdict cell reading `open` (round 2's 🟡 7).
OPEN_WORD = "open"
```
```python
        flagged = len(bad) + len(owed)
        number = finding_number(
            RECORD_LABEL, seen[NUMBER_COL], lines[i], taken, bad, True, owed
        )
        if number is not None:
            out[number] = (i, cells)
        elif len(bad) + len(owed) == flagged and (
            chain.verdict_of(seen, VERDICT_COL) == OPEN_WORD
        ):
            # The `#` cell says this row commissions nothing and the Verdict
            # cell says it is open. The marker arm above catches the reviewer
            # who wrote the severity and forgot the id; this catches the one
            # who wrote the wrong severity and said `open` anyway -- which the
            # marker cannot reach, and which the record states in words.
            owed.append((seen[NUMBER_COL].strip(), lines[i]))
```
```python
            f"the {RECORD_LABEL} has {len(owed)} row{many} that commissions "
            "nothing by its `#` cell and owes an answer by another: the cell "
            "is empty, or carries a severity that owes an answer, or the "
            f"`{chain.VERDICT_COLUMN}` cell reads `{OPEN_WORD}`. "
```
```python
@pytest.mark.parametrize(
    "cell",
    [
        "\N{LARGE GREEN CIRCLE} fix-surface",
        "carried",
        "\N{WHITE LARGE SQUARE}",
        "\N{BLACK QUESTION MARK ORNAMENT}",
        "A",
        "\N{EM DASH}",
    ],
)
def test_a_row_that_commissions_nothing_cannot_read_open(repo, cell):
    """Round 2's 🟡 7, and round 1's 🔴 1 one cell over. The severity check
    reads the `#` cell and the record says `open` in the column beside it, so
    every shape the rule admits came through `new` at exit 0, silently, with
    `Pass` ticked over a row its own table calls open.

    Free against the corpus: of the 25 admitted no-digit cells in the
    committed records, none has a Verdict cell reading `open`, so no record
    that reads correctly today is refused by this.
    """
    code, out = a_report(repo, f"| {cell} | one | `f.py:1` | open | read |\n")
    assert code == 2, out
    assert "open" in out, out
    assert "- [x] Pass" not in out, "a record was written"
```
```
<!-- Six, from rewriting the grounds sentence in five carriers and the overview
row beside them. Three of the six are noise: a different work item's closing
memo twice and a shipped spec once, all colliding on the phrase `one row in`.
The `plan.md` row is the branch's one exemption over a correction — that
paragraph is the approved plan's own text, so it is left standing with a dated
note under it rather than rewritten, and the row is what keeps the exemption
alive across runs. The live stale claim of this range is not here: phase 1's
*one row in thirty-seven* sentence was the reading round 1's 🟡 2 overturned,
and it was corrected rather than exempted. -->
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py tests/test_the_fixes_close_the_record.py -q` in a clone at `5bf88c1` | 113 passed, exit 0 |
| Six one-at-a-time mutations of `round_record.py`, each restored before the next: the empty-cell guard, the whole owed arm, 🟡 out of `OWED_MARKERS`, `head` reverted to the anywhere-split, the deferred home reverted to equality, the empty-id-list fallback removed | every one red, exit 1 in all six. The owed arm takes 5 cases with it; the `head` revert takes all four separators |
| Six no-digit `#` cells with a Verdict cell reading `open` through `new` — `🟢 fix-surface`, `carried`, `⬜`, `❓`, `A`, `—` (a `test_tmp_*` probe, NAME NOT IN TREE — deleted) | all six: exit 0, silent, record written with `- [x] Pass`. Finding 7 |
| The same six with finding 7's paste-ready fix applied in the clone | all six refuse at exit 2, no record written; the two changed modules still 113 passed, exit 0 |
| A report carrying `R2-1` and `🔴 A` together through `new` | exit 2 naming `R2-1` alone; the owed row appears nowhere. Finding 9 |
| Corpus re-derivation through `table_body` and the unverified reader over the committed records | 199 refused with digits · 51 without · 44 marker-plus-letter · 7 admitted · 0 empty · 0 `✅` · 0 bare em dash · 26 owed, splitting 11 `fixed` / 4 `answered` / 11 `open`. Every figure the fix pass wrote matches |
| The 26 owed rows located by record, and every caller of `finding_number` and `verdict_rows` enumerated | 10 records across four shipped work items; two call sites, both inside `round_record.py`. Finding 11 |
| The full suite, the repository-wide lint, the typecheck | **not yet** — not run in this round. §2 puts the broad gate with the sealer, after the rounds settle; `agents/sealer.md` names its `Broad gate` cell and nothing here writes it |
| `evidence-check --strict .` and `survivor-check --range <base>...HEAD` | **not yet** — `skills/verify/scripts/broad_gate.py` names both as members of the broad gate, so they are the sealer's. My judgments on the ledger re-stamps and the exemption are labelled `read` above, and the sealer's run is what executes them |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:2392` | round 1's 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2332`, `:2363`; `docs/review-chain-spec.md` §*The finding id*; `skills/code-review/SKILL.md` §*A row that commissions nothing takes no id at all*; `templates/sdd-round.md` | round 1's 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2950` | round 1's 3 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2936` | round 1's 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:3166` | round 1's 5 — fixed |
| round-1 | `seal/ledger.md`, row R1 · a finding id is a bare integer | round 1's 6 — answered |
| round-1 | `seal/specs/1789356180-…/phases/phase-1.md`, `phases/phase-3.md` | round 1's 7 — answered |
| round-1 | `skills/code-review/scripts/chain_check.py#MARKER`, `#verdict_of` | round 1's 8 — answered |
| round-1 | `9d1e324`, `26c7696` | round 1's 9 — answered |
| round-1 | `skills/code-review/scripts/round_record.py#fix_table` | round 1's 10 — answered |
| round-1 | `git diff release/v0.11.4...HEAD` | round 1's 11 — answered |
| round-1 | `seal/ledger.md` | round 1's 12 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain |  |  |

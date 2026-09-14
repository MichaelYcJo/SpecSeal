# 1789356180-the-two-halves-of-one-generator-refuse-each-other — review round 3

| Field | Value |
|---|---|
| Target SHA | 867f39c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 394 |
| Broad gate | not yet |
| Fixes checked by | round-4 |
| Contract changes | none |
| New units | says_open (depth 1); test_a_numbered_short_row_is_refused_rather_than_raising (depth 1); test_a_row_missing_only_its_grounds_is_still_written_short (depth 1); test_every_spelling_of_open_the_records_hold_is_refused (depth 1); test_a_word_that_merely_begins_with_open_is_not_the_open_verdict (depth 1); test_the_verdict_ruling_is_against_a_vocabulary_test_not_against_reading (depth 1) |
| Needs a fix | yes — 1, 2 and 3 |
| Loses a record or crashes | yes — 1 |

- [x] Pass

## What this round was asked

Round 3, spawned as the last round the chain's reopening bound allows: round 1 met the floor and round 2 closed on a fix, so the spawn said this record ends the run whatever it finds, and that anything it opened would end the run `capped`. The round was told to weigh that by writing each finding so somebody else could act on it without its author, rather than by lowering the bar.

Target is the diff of round 2's fixes, `89e7944..867f39c`, three commits. Rounds 1 and 2 had reviewed everything before `89e7944`. Round 2's record was committed and its three verdicts inherited; the job was the answers rather than new findings.

The exempt surface, handed over as a finding surface because units the fixes created have been reviewed by nobody: the four round 2's record names — `OPEN_WORD` and three cases. Two of those cases exist because the fix pass went past the finding, and both were named for judgement on their own rather than only as closures: the bounds guard, because reading a verdict cell that may not exist would have turned a silent pass into a traceback and `Loses a record or crashes` is its own gate; and the double-naming guard, found by mutation rather than by reading, with the round asked what else in that refusal path counts rather than names.

`OPEN_WORD` was named as the whole of the new arm, matching a literal word deliberately, with the stated reason that a vocabulary test would refuse every confirmation row because `verified` belongs to no vocabulary. The round was asked to judge that reasoning and to ask what a reviewer can write that means open and is not the word `open`.

One act of the fix pass was handed over to be verified rather than taken: its first version of the main case asserted `"open" in out`, which the OLD refusal already satisfied, so six cases went green against the defect on the first run. It reports strengthening the assertion to require the Verdict column be named. The round was asked to check the committed assertion cannot pass against the pre-fix refusal.

Three things were handed over as read rather than left to rederive: the corpus split at 199 / 51 / 44 / 7 with `✅`, `—` and empty at zero and 26 owed rows at 11 fixed / 4 answered / 11 open; the compatibility claim, with `finding_number` and `verdict_rows` having two call sites both inside `round_record.py`; and the `survivors.md` exemption of `plan.md`'s approved *what breaks in six months*, judged sound by round 2.

What the orchestrator had already executed at `bb1354e`, handed over so the round would not repeat it: four modules — `test_a_finding_id_is_a_bare_integer.py`, `test_the_fixes_close_the_record.py`, `test_the_record_is_generated.py`, `test_the_rules_have_one_owner.py` — 290 passed, exit 0; `survivor-check --range 89e7944..bb1354e --exempt …` exit 0; and `verdict_rows`' call into `finding_number` read at its coordinates.

The round was told to number every row of its verdict table including confirmations, and that this branch now refuses a no-digit `#` cell that is empty, carries 🔴 or 🟡, or sits beside a Verdict cell reading `open`. The broad gate was withheld by name as the sealer's single act after the rounds settle.

**What followed from its answer, decided by the repository owner.** The round answered the floor `yes` — a reachable input crashes — and the orchestrator confirmed the mechanism at its coordinates: the base computed `Pass` through `verdict_words`, which bounds-checks and raises a refusal, and round 2's fix replaced that path with an unguarded index. So the crash is this branch's own regression over code that handled the case correctly, which is the one thing the floor exists to refuse deferring. The owner chose a further round over shipping it capped: the findings are fixed and a fourth round reads those fixes.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A verdict row shorter than the header but carrying a digit is keyed by `verdict_rows` and then read at `VERDICT_COL` by every caller with no bounds check, so `new` and `close` both die with an `IndexError` instead of refusing. The fix pass guarded the one read inside `verdict_rows` and named the class in its case docstring | `skills/code-review/scripts/round_record.py:1970`, `:3307`, `:3324`, `:3383` | deferred #395 — its fix was reverted at 1ff0a6c with round 3's, so the record says what the branch carries. The run had been taken one round past the chain's reopening bound; the broad gate showed that merging those records would leave this repository's own suite red for every branch after it, and the owner pulled the run back to where the bound put it | fixed at fec2c88; executed at `867f39c` — `\| 1 \| one \|` through `new` gives exit 1 and `IndexError` at `round_record.py:1970` → `chain_check.py:1466`; the same row hand-edited into a record gives exit 1 at `:3307` through `close`. Both reads are identical at `89e7944`, so the defect is pre-existing and the class is the fix pass's own. Zero of the 1,691 committed verdict rows are short, so refusing is free |
| 2 | 🟡 `OPEN_WORD` is matched by equality while `agents/warden.md`, `templates/sdd-round.md` and `skills/code-review/SKILL.md` all describe a match on the word. 7 of the 95 open verdicts in the committed records — `open — deferred`, `open, comment only` and five more — are outside the equality and inside the documented rule | `skills/code-review/scripts/round_record.py:2376`, `:3095` | deferred #395 — its fix was reverted at 1ff0a6c with round 3's, so the record says what the branch carries. The run had been taken one round past the chain's reopening bound; the broad gate showed that merging those records would leave this repository's own suite red for every branch after it, and the owner pulled the run back to where the bound put it | fixed at fec2c88; executed at `867f39c` — all 95 cells that begin with `open` counted through `verdict_of`; 88 bare, 7 wider, none in `CLOSED_WORDS`. A head match ended by `chain_check.SEPARATORS` reaches all 95 and newly refuses 0 of the 25 admitted committed rows. The vocabulary-test grounds hold separately: 18 of the 25 admitted rows carry a verdict outside `CLOSED_WORDS` |
| 3 | 🟡 The grounds this diff overturned — *the verdict word cannot do this job* — were replaced in `skills/code-review/SKILL.md` and `templates/sdd-round.md` and left standing in four other places, including a bolded section of the spec twenty lines under the paragraph that overturns it | `docs/review-chain-spec.md:790`, `skills/code-review/scripts/round_record.py:2363`, `:2423`, `tests/test_a_finding_id_is_a_bare_integer.py:236` | deferred #395 — its fix was reverted at 1ff0a6c with round 3's, so the record says what the branch carries. The run had been taken one round past the chain's reopening bound; the broad gate showed that merging those records would leave this repository's own suite red for every branch after it, and the owner pulled the run back to where the bound put it | fixed at fec2c88; read at `867f39c`, and executed: `survivor-check --range 89e7944..867f39c` exits 0 over 28 removed sentences, because the sentence was removed nowhere. The fourth site is split across a line break, the blind spot `test_a_corrected_sentence_survives_elsewhere` names in its own docstring |
| 4 | ⬜ `finding_number`'s docstring was re-indented from column 4 to column 8 and the new paragraph was left at column 4, so `inspect.getdoc` renders 64 of 65 body lines one level in and that one at the margin | `skills/code-review/scripts/round_record.py:2387` | deferred #395 — its fix was reverted at 1ff0a6c with round 3's, so the record says what the branch carries. The run had been taken one round past the chain's reopening bound; the broad gate showed that merging those records would leave this repository's own suite red for every branch after it, and the owner pulled the run back to where the bound put it | fixed at fec2c88; executed at `867f39c` — rendered through `inspect.getdoc` and measured per line; `ruff format --diff` reports the file already formatted, so no gate sees it and nothing behavioural changes |
| 5 | ⬜ The verdict arm exists in the generator alone — `chain_check.open_blocking` at the pull request still reads only 🔴 rows, so a record hand-edited after `close` carries the shape past CI | `skills/code-review/scripts/chain_check.py#open_blocking` | answered | read at `867f39c`. Not a new gap and the spec states it; both generator subcommands refuse the shape, which is where the rule belongs. Recorded so the next round does not open it as new |
| 6 | Round 2's 🟡 7 is closed and was seen red: all six admitted shapes whose Verdict cell reads `open` are refused | `skills/code-review/scripts/round_record.py:3091` | answered | executed at `867f39c` — the committed module against `89e7944`'s `round_record.py`: 6 failed, 49 passed, the six parametrized cases red. At `867f39c`: 55 passed, exit 0 |
| 7 | The strengthened assertion is right, and cannot pass against the pre-fix refusal | `tests/test_a_finding_id_is_a_bare_integer.py:302` | answered | executed at `867f39c` — 0 occurrences of `` `Verdict` cell reads `open` `` anywhere in the pre-fix run's output. The strengthening is still load-bearing because the pre-fix marker-arm message does contain *ticked over an open finding* |
| 8 | The both-arms guard is load-bearing — without it a row failing both arms is quoted twice and the message counts two rows over a table holding one | `skills/code-review/scripts/round_record.py:3092` | answered | executed at `867f39c` — mutation: dropping `len(bad) + len(owed) == flagged` turns `test_a_row_failing_both_arms_is_named_once` red with *has 2 rows* and the row quoted twice |
| 9 | The bounds guard is load-bearing for the unnumbered short row, which is the member finding 1 leaves standing | `skills/code-review/scripts/round_record.py:3094` | answered | executed at `867f39c` — mutation: dropping `len(seen) > VERDICT_COL` raises `IndexError` and turns `test_a_row_too_short_to_have_a_verdict_cell_does_not_crash` red. Both new guards were green pre-fix |
| 10 | The `Free against the corpus` claim is exactly true: of the 25 admitted no-digit rows in the committed records, none reads `open` or anything beginning with it | `skills/code-review/scripts/round_record.py:2367`, `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` row 1 | answered | executed at `867f39c` — re-derived through the module's own `table_body`: 51 no-digit rows, 26 owed by the marker arm, 25 admitted, 0 reading `open`. Round 2's split reproduces |
| 11 | The ledger fragment's anchors survive the fix — `finding_number` and `verdict_rows` both moved and both re-hash | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | answered | executed at `867f39c` — `evidence-check .` exits 0: 1,220 ok, 0 drifted, 0 broken, 28 of them this work item's fragment |
| 12 | Round 2's own record is a truthful application of its fix table: 🟡 7 reads `**fixed** 7b2c0d7`, the two ⬜ rows read `answered` with grounds, and `New units` names all four | `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-2.md` | answered | read at `867f39c` against the three commits. Under `seal/specs/`, so a correction surface rather than a fix surface |
| 13 | The last commit changes one committed round record, and nothing that scans committed records reddens over it | `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-2.md` | answered | executed at `867f39c` — the eight modules that glob `round-*.md` and were not in the handoff's four: 361 passed, exit 0. The handoff's own four were run at `bb1354e`, one commit earlier |

## Paste-ready fixes

```python
        seen = [reader.visible(c) for c in cells]
        if len(seen) < len(VERDICT_HEADER):
            raise Refused(
                f"a verdict row has {len(seen)} cells and this table has "
                f"{len(VERDICT_HEADER)}: {lines[i].strip()!r}. Every reader "
                "downstream of this one indexes the `Verdict` column by "
                "position, so a short row that carries a digit is keyed here "
                "and then reaches them as an IndexError rather than as a "
                "refusal naming the row. `fix_table` has refused the same shape "
                "since it was written; this is the other table catching up, "
                "and it is free — zero of the 1,691 committed verdict rows "
                "are short."
            )
        flagged = len(bad) + len(owed)
```
```python
def test_a_numbered_short_row_is_refused_rather_than_raising(repo):
    """Finding 1 of round 3, and the member round 2's guard did not reach.

    A digit in the `#` cell keys the row, and every caller of `verdict_rows`
    then indexes `VERDICT_COL` on it: `new` at the `words` comprehension,
    `close` at `open_now`, at the `already` message and at the write. Measured
    before the repair -- exit 1 and an IndexError out of `verdict_of`, on both
    subcommands.
    """
    code, out = a_report(repo, "| 1 | one |\n")
    assert code == 2, out
    assert "Traceback" not in out, out
    assert "2 cells" in out and "this table has 5" in out, out
    assert "- [x] Pass" not in out, "a record was written"
```
```python
OPEN_WORD = "open"


def says_open(word):
    """`word` is the open verdict, however the reviewer ended it.

    The grounds for not running a VOCABULARY test hold and are untouched:
    `verified` is in no vocabulary and would be refused, and that would refuse
    18 of the 25 admitted no-digit rows in the committed records. What does not
    follow from those grounds is equality. `verdict_of` already ends a
    vocabulary word on `chain.SEPARATORS`, which is what makes `fixed d3fe44d`
    read as `fixed`, and the same boundary here reaches `open -- deferred` and
    `open, comment only` -- 7 of the 95 open verdicts this repository has
    written, and the spelling `agents/warden.md`, `templates/sdd-round.md` and
    `skills/code-review/SKILL.md` all describe. Measured over every committed
    record: 95 cells reached, none in `CLOSED_WORDS`, and 0 of the 25 admitted
    rows newly refused.
    """
    if not word.startswith(OPEN_WORD):
        return False
    rest = word[len(OPEN_WORD) :]
    return not rest or rest[0] in chain.SEPARATORS
```
```python
            and says_open(chain.verdict_of(seen, VERDICT_COL))
```
```python
@pytest.mark.parametrize(
    "verdict",
    ["open", "open — deferred", "open, comment only", "**open** — still"],
)
def test_every_spelling_of_open_the_records_hold_is_refused(repo, verdict):
    """Round 3's 🟡 2. Three documents say a row whose Verdict cell reads
    `open` is refused; the arm read it as equality, and 7 of the 95 open
    verdicts in the committed records end the word with a separator."""
    code, out = a_report(repo, f"| carried | one | `f.py:1` | {verdict} | read |\n")
    assert code == 2, out
    assert "`Verdict` cell reads `open`" in out, out
```
```markdown
**The verdict word was ruled out once, and the ruling was too wide.** A
confirmation row reads `verified`, which is in no vocabulary and therefore
OPEN, so a test of the form *anything not closed* would refuse every
confirmation — one refusal traded for another. That is an argument against a
vocabulary test and not against reading the cell, which is why the rule above
reads one word and composes with the `#` cell rather than replacing it.
```
```python
# is. A VOCABULARY test of the verdict cannot do this job: a confirmation
# reads `verified`, which is in no vocabulary and therefore OPEN, so reading
# the verdict as OPEN/CLOSED would trade one refusal for another. Reading the
# one word `open` is the narrower thing `OPEN_WORD` below does.
```
```python
        A vocabulary test of the verdict cannot serve here: a confirmation reads
        `verified`, which is in no vocabulary and therefore OPEN, so reading the
        verdict as OPEN/CLOSED would trade one refusal for another. Reading the
        one word `open` does not, and the paragraph below is that arm.
```
```python
    The severity marker is what already means *somebody owes this an answer* —
    🔴 blocks merge and 🟡 needs grounds — so it is what this rule reads. A
    vocabulary test of the verdict cannot serve in its place: a confirmation row
    reads `verified`, which is in no vocabulary and therefore OPEN, so it would
    trade one refusal for another. Reading the single word `open` is a separate
    arm and composes with this one —
    `test_a_row_that_commissions_nothing_cannot_read_open` below.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py -q` at `867f39c` | 55 passed, exit 0 |
| the same module against `89e7944`'s `round_record.py` | 6 failed, 49 passed — all six `test_a_row_that_commissions_nothing_cannot_read_open` parameters red; the two other new cases green, as guards on new code should be |
| mutation: `len(bad) + len(owed) == flagged` dropped | `test_a_row_failing_both_arms_is_named_once` red — *has 2 rows*, `\| 🔴 A \|` quoted twice |
| mutation: `len(seen) > VERDICT_COL` dropped | `test_a_row_too_short_to_have_a_verdict_cell_does_not_crash` red — `IndexError` out of `verdict_of` |
| probe: `\| 1 \| one \|` (short **and** numbered) through `new` | exit 1, `IndexError` at `round_record.py:1970` → `chain_check.py:1466`. Finding 1 |
| probe: the same row hand-edited into a record, through `close` | exit 1, `IndexError` at `round_record.py:3307`. Finding 1 |
| every committed `round-N.md` through the module's own `table_body`: `#` cells split by digit, marker and admission | 175 of 215 records parse, 1,691 verdict rows, 51 no-digit — 26 owed by the marker arm, **25 admitted**, of which 0 read `open`. Round 2's split reproduces |
| every committed verdict cell through `verdict_of`, counting cells that begin with `open` | 95 across 8 spellings — 88 bare, 7 wider; none in `CLOSED_WORDS`. Finding 2 |
| the proposed head match, ended by `chain_check.SEPARATORS`, over the same corpus | reaches all 95; newly refuses 0 of the 25 admitted rows. Finding 2 |
| short verdict rows across the committed corpus | 0 of 1,691, so refusing one outright is free. Finding 1 |
| `bin/survivor-check --range 89e7944..867f39c --exempt <the work item's survivors.md>` | exit 0 — 977 files examined against 28 removed sentences, *no removed wording is still standing*. Finding 3: the sentence was removed nowhere |
| `bin/evidence-check .` | exit 0 — 1,220 ok · 0 drifted · 0 broken; this work item's fragment 28 ok |
| `uvx ruff format --diff skills/code-review/scripts/round_record.py` | *1 file already formatted* — finding 4 is invisible to the formatter |
| `finding_number.__doc__` through `inspect.getdoc`, indent measured per line | 64 of 65 body lines at column 4, one at column 0. Finding 4 |
| the eight modules that scan committed round records and were not in the handoff's four | 361 passed, exit 0 |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** §2 leaves it to the sealer, whose spawn is what comes due once this record is written; this round ran none of the three |

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
| round-2 | `skills/code-review/scripts/round_record.py:2447`, `:3073` | round 2's 1 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2366` | round 2's 2 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2354`; `docs/review-chain-spec.md` §*A verdict row that commissions nothing*; `skills/code-review/SKILL.md`; `templates/sdd-round.md`; `phases/phase-1.md` | round 2's 3 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3025` | round 2's 4 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3000` | round 2's 5 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3262` | round 2's 6 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2447`, `:3063` | round 2's 7 — fixed |
| round-2 | `seal/specs/1789356180-…/survivors.md:27` | round 2's 8 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3073` | round 2's 9 — answered |
| round-2 | `skills/code-review/scripts/round_record.py`, `#inherited_rows`; `.github/workflows/hygiene.yml:191` | round 2's 11 — answered |
| round-2 | `seal/specs/1789356180-…/survivors.md`; `plan.md:72`; `phases/phase-1.md:64`; `skills/verify/scripts/broad_gate.py:584` | round 2's 12 — answered |
| round-2 | `58511d0` | round 2's 13 — answered |
| round-2 | `seal/specs/1789356180-…/rounds/round-1.md` | round 2's 14 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | — | — |

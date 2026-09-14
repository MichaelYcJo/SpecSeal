# Round 3 — the verifying round over round 2's fixes

Target: `git diff 89e7944..867f39c`, three commits, HEAD `867f39c`. Reviewed in
a scratch clone of the repository at that SHA; nothing was written in the
working tree except this file.

Round 2 closed one finding on a fix and answered two. The fix is real and the
arm it added works for the spelling it was written against. What this round
opens is one crash and two places where the fix stopped at the coordinate the
finding named.

**The shape of it, in one line each.**

1. The fix pass guarded the verdict cell it was about to read and left the two
   readers downstream of it unguarded, so a verdict row that is short **and
   numbered** still reaches them — as an `IndexError` rather than a refusal.
2. The arm matches `open` by equality. Three documents now tell a reviewer that
   a row whose Verdict cell *reads* `open` is refused, and 7 of the 95 open
   verdicts in this repository's committed records are not spelled that way.
3. The grounds the arm overturned — *the verdict word cannot do this job* —
   were replaced in `skills/code-review/SKILL.md` and in
   `templates/sdd-round.md`, and left standing verbatim in four other places,
   one of them the spec.

Items 1 and 2 are the same mistake as item 3 read from the other side: the fix
went where the finding pointed.

---

## 🔴 1 — a numbered short row crashes `new` and `close`

`skills/code-review/scripts/round_record.py:1970` (the `new` path),
`:3307`, `:3324`, `:3383` (the `close` path).

The new arm bounds-checks the cell it reads:

```python
        elif (
            len(bad) + len(owed) == flagged
            and len(seen) > VERDICT_COL
            and chain.verdict_of(seen, VERDICT_COL) == OPEN_WORD
        ):
```

`verdict_rows` returns those same cells to its callers, and every caller
indexes `VERDICT_COL` by position with no guard at all:

```python
    keyed = verdict_rows(reader, lines)
    words = [
        chain.verdict_of([reader.visible(c) for c in cells], VERDICT_COL)
        for _i, cells in keyed.values()
    ]
```

A short row reaches that list whenever its `#` cell carries a digit, because
then `finding_number` returns a number and the row is keyed. The new case
covers `| carried | one |`, which carries none.

**Executed.** A report whose verdict table holds `| 1 | one |`:

```
NEW exit: 1
  File ".../round_record.py", line 1970, in build
  File ".../chain_check.py", line 1466, in verdict_of
IndexError: list index out of range
```

`close` over a record hand-edited to the same row fails identically, at
`:3307`. Both reads predate this diff — they are at the same two coordinates in
`89e7944` — so the defect is not new. What is new is that the fix pass named
this class in its own case docstring (*"a repair that trades a silent pass for
a traceback is not a repair"*) and closed one member of it.

**Why it matters beyond the traceback.** The orchestrator reads an exit code.
This one is 1 with a stack trace, where every other malformed row in the same
table is 2 with a sentence naming the row. `Loses a record or crashes` is the
gate the fix pass itself invoked, and the answer for a numbered short row is
still yes.

**The repair is one function over, and the module already has its shape.**
`fix_table` refuses a short row outright before it keys anything:

```python
        if len(seen) < len(FIXES_HEADER):
            raise Refused(f"a fix row has {len(seen)} cells: {raw[i].strip()!r}")
```

The verdict table is the one of the two that never got it. Refusing there is
free: across the 1,691 body rows of the 175 committed records that parse,
**zero** verdict rows are short.

---

## 🟡 2 — the arm reads `open` by equality and the documents say it reads the word

`skills/code-review/scripts/round_record.py:2376` and `:3095`.

The reasoning against a vocabulary test is sound, and I checked it rather than
took it: `verdict_of` hands back the normalized cell for anything it does not
recognise, so of the 25 admitted no-digit rows in the committed records, 18
carry a verdict outside `CLOSED_WORDS` — `truthful`, `record only`,
`anchors resolve`, `consistent`, `nit, no fix`. Refusing everything not closed
would refuse all 18. The grounds hold.

What does not follow from those grounds is exact equality. The step from *not a
vocabulary test* to *string equality* is argued nowhere, and the module next
door already matches its vocabulary the right way — as a head of the cell ended
by one of `chain_check.SEPARATORS`, which is what makes `fixed d3fe44d` read as
`fixed`.

**Executed, over every committed record.** Of the 95 verdict cells that
normalize to something beginning with `open`, 88 are the bare word and **7 are
not**:

| spelling | where |
|---|---|
| `open — deferred` | `1788472135-…/rounds/round-2.md` |
| `open, comment only` | `1788360817-…/rounds/round-5.md` |
| `open, and closed by the same three arguments as 1` | `1788360817-…/rounds/round-4.md` |
| `open, and the answer is the ledger row rather than the check` | `1788360817-…/rounds/round-3.md` |
| `open — answer with grounds or let the 🔴 1 fixture fix close it` | `1788326734-…/rounds/round-2.md` |
| `open — it reads the row now and then indexes a three-entry dictionary…` | `1788360817-…/rounds/round-2.md` |
| `open — and not by another patch here without an answer to q2` | `1788229400-…/rounds/round-5.md` |

That is 7.4% of how the reviewers of this repository actually spell an open
verdict. None of the seven slips through today, because each row also carries
🔴 or 🟡 in its `#` cell and the marker arm takes it — but that is the coincidence
the arm exists because it cannot rely on.

**The documents state the wider rule, not the narrower one.** All three were
written in this diff:

- `agents/warden.md:189` — *"a row whose Verdict cell reads `open` is refused
  whatever its `#` cell says"*
- `templates/sdd-round.md:316` — *"any row whose Verdict cell reads `open`"*
- `skills/code-review/SKILL.md:304` — *"It is the literal word rather than a
  vocabulary test"*

A reviewer who reads any of those and writes `| carried | … | open — still
`open` | … |` gets `Pass` ticked over the row. The gap between what a gate
refuses and what its documentation says it refuses is the shape of this whole
work item.

**Executed: the wider rule is free too.** Matching `open` as a head ended by
`chain_check.SEPARATORS` reaches all 95 cells, none of which is in
`CLOSED_WORDS`, and newly refuses **zero** of the 25 admitted rows in the
committed records. The prefix rule is a strict improvement at the same cost.

---

## 🟡 3 — the overturned grounds are still standing in four places

`docs/review-chain-spec.md:790`, `skills/code-review/scripts/round_record.py:2363`
and `:2423`, `tests/test_a_finding_id_is_a_bare_integer.py:236`.

The spec now carries, twenty lines apart:

```
769: **The record is read in two cells, not one.** … So a row whose Verdict
     cell reads `open` is refused whatever its `#` cell says.

790: **The verdict word cannot do this job.** A confirmation row reads
     `verified`, which is in no vocabulary and therefore OPEN, so reading the
     verdict would refuse every confirmation — one refusal traded for another.
```

The second paragraph is the reasoning the first one overturns, left in place
with its own bold heading and no qualification. `skills/code-review/SKILL.md`
and `templates/sdd-round.md` had the same sentence and both **replaced** it in
this diff; the spec got an insertion instead and kept its copy.

The two in-module copies are softer but real. `:2363` says *the verdict word
cannot do this job* and the `OPEN_WORD` comment three lines below corrects it;
`:2423` says *the verdict word cannot serve here* and the paragraph that
corrects it is 15 lines further down the same docstring. A reader who stops at
either sentence has read a claim this module's own code contradicts.

**`survivor-check` cannot see any of this, and that is the interesting part.**
Executed over the full range: `survivor-check --range 89e7944..867f39c` exits
0, *"no removed wording is still standing"*, against the 28 sentences the range
removed. The check looks for wording a change removed HERE that survives THERE.
This diff removed the sentence nowhere — it wrote the refutation beside it — so
there is nothing for the check to hunt. The fourth site compounds it: in
`tests/test_a_finding_id_is_a_bare_integer.py` the sentence is split across a
line break, which is the exact blind spot `test_a_corrected_sentence_survives_elsewhere`
names in its own module docstring.

---

## ⬜ 4 — the docstring was re-indented and one paragraph was left behind

`skills/code-review/scripts/round_record.py:2387`–`:2452`.

The diff moves every line of `finding_number`'s docstring from column 4 to
column 8 and leaves line 2438 — the new paragraph — at column 4. Nothing
behavioural turns on it and `ruff format --diff` reports the file already
formatted, so no gate sees it. What a reader sees does change: `inspect.getdoc`
computes the common indent as 4, strips that, and renders 64 of 65 body lines
one level in with the new paragraph alone at the margin.

Executed: rendered through `inspect.getdoc` and measured per line — column 4 on
every paragraph except the one at index 51, which is column 0.

---

## ⬜ 5 — the arm is in the generator and nowhere else

Answered on my own grounds. `chain_check.open_blocking` at the pull request
still reads only 🔴 rows, so a record hand-edited after `close` carries a
`| carried | … | open | … |` row past CI unseen. This is not a new gap and the
spec states it; the generator is the only reader that refuses the shape, and
both of its subcommands do, which is where the rule belongs. Recorded so the
next round does not rediscover it as new.

---

## What round 2's closures look like from here

**Finding 7 is genuinely closed, and seen red.** The committed test module run
against the module `89e7944` carried: 6 failed, 49 passed — every one of the
six parametrized shapes red. At `867f39c`: 55 passed, exit 0.

**The strengthened assertion holds.** The fix pass says it replaced
`"open" in out` with a check that the Verdict column is named. Verified rather
than taken: the pre-fix refusal text contains neither `` `Verdict` cell reads
`open` `` nor, on these six inputs, any output at all — the pre-fix module exits
0 and writes the record, so `assert code == 2` is what reddens first. The
strengthening is still right, because the pre-fix message for the *marker* arm
does contain the words *"ticked over an open finding"*, and a bare `"open" in
out` would have passed against it. Measured: 0 occurrences of
`` `Verdict` cell reads `open` `` in the pre-fix run's output.

**Both guards the fix pass added past the finding are load-bearing.** Mutation,
one at a time, with the rest of the module intact:

- dropping `len(bad) + len(owed) == flagged` → the message reads *"has 2 rows"*
  over a table holding one, and quotes `| 🔴 A |` twice.
  `test_a_row_failing_both_arms_is_named_once` goes red.
- dropping `len(seen) > VERDICT_COL` → `IndexError` out of `verdict_of`.
  `test_a_row_too_short_to_have_a_verdict_cell_does_not_crash` goes red.

Both were green pre-fix, which is what a guard on new code should be. Neither is
decoration.

**The corpus claim is exactly true as written.** Re-derived through the module's
own `table_body`: 51 no-digit rows, 26 taken by the marker arm, **25 admitted**,
and of those 25 not one has a Verdict cell reading `open` or anything beginning
with it. The `Free against the corpus` sentence in the `OPEN_WORD` comment and
in the ledger fragment is measured and correct.

**The three facts carried from round 2 rather than re-derived.** The corpus
split (199 / 51 / 44 / 7 and 26 owed at 11 / 4 / 11), the compatibility claim,
and the `survivors.md` exemption of `plan.md`. The first I re-derived anyway on
the two numbers my own findings rest on (51 and the 26 / 25 split, both
reproduced); the other two I carried, and neither has a check that fails.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A verdict row shorter than the header but carrying a digit is keyed by `verdict_rows` and then read at `VERDICT_COL` by every caller with no bounds check, so `new` and `close` both die with an `IndexError` instead of refusing. The fix pass guarded the one read inside `verdict_rows` and named the class in its case docstring | `skills/code-review/scripts/round_record.py:1970`, `:3307`, `:3324`, `:3383` | open | executed at `867f39c` — `\| 1 \| one \|` through `new` gives exit 1 and `IndexError` at `round_record.py:1970` → `chain_check.py:1466`; the same row hand-edited into a record gives exit 1 at `:3307` through `close`. Both reads are identical at `89e7944`, so the defect is pre-existing and the class is the fix pass's own. Zero of the 1,691 committed verdict rows are short, so refusing is free |
| 2 | 🟡 `OPEN_WORD` is matched by equality while `agents/warden.md`, `templates/sdd-round.md` and `skills/code-review/SKILL.md` all describe a match on the word. 7 of the 95 open verdicts in the committed records — `open — deferred`, `open, comment only` and five more — are outside the equality and inside the documented rule | `skills/code-review/scripts/round_record.py:2376`, `:3095` | open | executed at `867f39c` — all 95 cells that begin with `open` counted through `verdict_of`; 88 bare, 7 wider, none in `CLOSED_WORDS`. A head match ended by `chain_check.SEPARATORS` reaches all 95 and newly refuses 0 of the 25 admitted committed rows. The vocabulary-test grounds hold separately: 18 of the 25 admitted rows carry a verdict outside `CLOSED_WORDS` |
| 3 | 🟡 The grounds this diff overturned — *the verdict word cannot do this job* — were replaced in `skills/code-review/SKILL.md` and `templates/sdd-round.md` and left standing in four other places, including a bolded section of the spec twenty lines under the paragraph that overturns it | `docs/review-chain-spec.md:790`, `skills/code-review/scripts/round_record.py:2363`, `:2423`, `tests/test_a_finding_id_is_a_bare_integer.py:236` | open | read at `867f39c`, and executed: `survivor-check --range 89e7944..867f39c` exits 0 over 28 removed sentences, because the sentence was removed nowhere. The fourth site is split across a line break, the blind spot `test_a_corrected_sentence_survives_elsewhere` names in its own docstring |
| 4 | ⬜ `finding_number`'s docstring was re-indented from column 4 to column 8 and the new paragraph was left at column 4, so `inspect.getdoc` renders 64 of 65 body lines one level in and that one at the margin | `skills/code-review/scripts/round_record.py:2387` | open | executed at `867f39c` — rendered through `inspect.getdoc` and measured per line; `ruff format --diff` reports the file already formatted, so no gate sees it and nothing behavioural changes |
| 5 | ⬜ The verdict arm exists in the generator alone — `chain_check.open_blocking` at the pull request still reads only 🔴 rows, so a record hand-edited after `close` carries the shape past CI | `skills/code-review/scripts/chain_check.py#open_blocking` | answered | read at `867f39c`. Not a new gap and the spec states it; both generator subcommands refuse the shape, which is where the rule belongs. Recorded so the next round does not open it as new |
| 6 | Round 2's 🟡 7 is closed and was seen red: all six admitted shapes whose Verdict cell reads `open` are refused | `skills/code-review/scripts/round_record.py:3091` | answered | executed at `867f39c` — the committed module against `89e7944`'s `round_record.py`: 6 failed, 49 passed, the six parametrized cases red. At `867f39c`: 55 passed, exit 0 |
| 7 | The strengthened assertion is right, and cannot pass against the pre-fix refusal | `tests/test_a_finding_id_is_a_bare_integer.py:302` | answered | executed at `867f39c` — 0 occurrences of `` `Verdict` cell reads `open` `` anywhere in the pre-fix run's output. The strengthening is still load-bearing because the pre-fix marker-arm message does contain *ticked over an open finding* |
| 8 | The both-arms guard is load-bearing — without it a row failing both arms is quoted twice and the message counts two rows over a table holding one | `skills/code-review/scripts/round_record.py:3092` | answered | executed at `867f39c` — mutation: dropping `len(bad) + len(owed) == flagged` turns `test_a_row_failing_both_arms_is_named_once` red with *has 2 rows* and the row quoted twice |
| 9 | The bounds guard is load-bearing for the unnumbered short row, which is the member finding 1 leaves standing | `skills/code-review/scripts/round_record.py:3094` | answered | executed at `867f39c` — mutation: dropping `len(seen) > VERDICT_COL` raises `IndexError` and turns `test_a_row_too_short_to_have_a_verdict_cell_does_not_crash` red. Both new guards were green pre-fix |
| 10 | The `Free against the corpus` claim is exactly true: of the 25 admitted no-digit rows in the committed records, none reads `open` or anything beginning with it | `skills/code-review/scripts/round_record.py:2367`, `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` row 1 | answered | executed at `867f39c` — re-derived through the module's own `table_body`: 51 no-digit rows, 26 owed by the marker arm, 25 admitted, 0 reading `open`. Round 2's split reproduces |
| 11 | The ledger fragment's anchors survive the fix — `finding_number` and `verdict_rows` both moved and both re-hash | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | answered | executed at `867f39c` — `evidence-check .` exits 0: 1,220 ok, 0 drifted, 0 broken, 28 of them this work item's fragment |
| 12 | Round 2's own record is a truthful application of its fix table: 🟡 7 reads `**fixed** 7b2c0d7`, the two ⬜ rows read `answered` with grounds, and `New units` names all four | `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-2.md` | answered | read at `867f39c` against the three commits. Under `seal/specs/`, so a correction surface rather than a fix surface |
| 13 | The last commit changes one committed round record, and nothing that scans committed records reddens over it | `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-2.md` | answered | executed at `867f39c` — the eight modules that glob `round-*.md` and were not in the handoff's four: 361 passed, exit 0. The handoff's own four were run at `bb1354e`, one commit earlier |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | — | — |

## Paste-ready fixes

Finding 1 — refuse a short verdict row where the fix table already refuses one,
rather than guarding each reader. In `verdict_rows`, replace the `#`-cell guard:

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

The `and len(seen) > VERDICT_COL` clause in the arm below becomes unreachable
and should come out with it, so that one guard stands rather than two saying
different things. The case that pins the closed member:

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

Finding 2 — match the word the way `verdict_of` matches its own vocabulary.
Beside `OPEN_WORD`:

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

and at the arm:

```python
            and says_open(chain.verdict_of(seen, VERDICT_COL))
```

The refusal message keeps its wording — it already says *reads `open`*, which
is what this makes true. A case for the widened spelling:

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

Finding 3 — replace the superseded section in the spec rather than leaving it
beside its refutation. At `docs/review-chain-spec.md:790`:

```markdown
**The verdict word was ruled out once, and the ruling was too wide.** A
confirmation row reads `verified`, which is in no vocabulary and therefore
OPEN, so a test of the form *anything not closed* would refuse every
confirmation — one refusal traded for another. That is an argument against a
vocabulary test and not against reading the cell, which is why the rule above
reads one word and composes with the `#` cell rather than replacing it.
```

The two in-module copies, so the class is closed rather than its loudest
member. At `skills/code-review/scripts/round_record.py:2363`:

```python
# is. A VOCABULARY test of the verdict cannot do this job: a confirmation
# reads `verified`, which is in no vocabulary and therefore OPEN, so reading
# the verdict as OPEN/CLOSED would trade one refusal for another. Reading the
# one word `open` is the narrower thing `OPEN_WORD` below does.
```

At `:2423`:

```python
        A vocabulary test of the verdict cannot serve here: a confirmation reads
        `verified`, which is in no vocabulary and therefore OPEN, so reading the
        verdict as OPEN/CLOSED would trade one refusal for another. Reading the
        one word `open` does not, and the paragraph below is that arm.
```

And at `tests/test_a_finding_id_is_a_bare_integer.py:236`, the same correction
in the sentence that spans the line break:

```python
    The severity marker is what already means *somebody owes this an answer* —
    🔴 blocks merge and 🟡 needs grounds — so it is what this rule reads. A
    vocabulary test of the verdict cannot serve in its place: a confirmation row
    reads `verified`, which is in no vocabulary and therefore OPEN, so it would
    trade one refusal for another. Reading the single word `open` is a separate
    arm and composes with this one —
    `test_a_row_that_commissions_nothing_cannot_read_open` below.
```

Finding 4 — re-indent the docstring body back to column 4 throughout, which is
where every line of it sat at `89e7944` and where line 2438 still sits.

## Regression tests to plant

| Case | Destination |
|---|---|
| `test_a_numbered_short_row_is_refused_rather_than_raising` — finding 1, the member the round-2 guard did not reach; seen red as exit 1 with an `IndexError` | `tests/test_a_finding_id_is_a_bare_integer.py`  NAME NOT IN TREE |
| the same row through `close`, hand-edited into a record the way `hand_edited` already does — the second reader, and the one a record on disk reaches | `tests/test_a_finding_id_is_a_bare_integer.py` |
| `test_every_spelling_of_open_the_records_hold_is_refused` — finding 2, parametrized over the separators the corpus actually uses | `tests/test_a_finding_id_is_a_bare_integer.py`  NAME NOT IN TREE |

## Facts for the evidence ledger

| Claim | Grounds |
|---|---|
| A verdict row shorter than the header is refused at `verdict_rows`, the way `fix_table` has always refused one, so no caller downstream indexes `VERDICT_COL` off the end — measured free at 0 short rows in 1,691 committed verdict rows | `skills/code-review/scripts/round_record.py#verdict_rows`, `#fix_rows` |
| `open` is read as a head of the verdict cell ended by `chain_check.SEPARATORS`, not as the whole cell: 95 of the committed cells are reached, 7 of them wider than the bare word, none in `CLOSED_WORDS`, and 0 of the 25 admitted no-digit rows newly refused | `skills/code-review/scripts/round_record.py#says_open`, `skills/code-review/scripts/chain_check.py#SEPARATORS` |

`says_open` NAME NOT IN TREE.

## What I could not settle, and who answers it

| Question | Answerer |
|---|---|
| 40 of the 215 committed `round-N.md` files do not parse through the generator's own `table_body` — an older heading or an older header, both pre-dating this branch. Every count in this report and in round 2's is over the 175 that do | ❓ out of verified scope. The repository owner, or whichever work item next touches the record format |
| Whether findings 1–3 are fixed on this branch or become `deferred #N` issues. The run is capped, so the decision is not this round's | the orchestrator |

## Proof block

Executed, in a scratch clone at `867f39c` (deleted with its virtualenv at the
end of the round; no probe file, worktree or branch outlives it):

- `bin/test tests/test_a_finding_id_is_a_bare_integer.py -q` — 55 passed, exit 0
- the same module against `89e7944`'s `round_record.py` — 6 failed, 49 passed
- two mutations, one at a time, each killed by the case written for it
- two probes for the numbered short row, through `new` and through `close`
- five corpus passes through `table_body`, `finding_number`'s arms and
  `verdict_of` over every committed `round-N.md`
- `bin/survivor-check --range 89e7944..867f39c` — exit 0
- `bin/evidence-check .` — exit 0, 1,220 ok
- `uvx ruff format --diff skills/code-review/scripts/round_record.py` — already formatted
- eight record-scanning test modules — 361 passed, exit 0

Read at `867f39c`:

- `skills/code-review/scripts/round_record.py` — `finding_number`, `id_refusal`,
  `verdict_rows`, `fix_table`, `table_body`, `row_cells`, `build`, `close`,
  `OPEN_WORD`, `OWED_MARKERS`, `DIGIT_RE`, `NUMBER_COL`, `VERDICT_COL`,
  `VERDICT_HEADER`, `FIXES_HEADER`, `main`
- `skills/code-review/scripts/chain_check.py` — `verdict_of`, `SEPARATORS`,
  `CLOSED_WORDS`, `VERDICT_COLUMN`, `MARKER`
- `tests/test_a_finding_id_is_a_bare_integer.py` in full;
  `tests/test_the_record_is_generated.py` helpers; `tests/test_lint_python.py`;
  `tests/test_a_corrected_sentence_survives_elsewhere.py` header
- `docs/review-chain-spec.md` §the `#` cell rule; `skills/code-review/SKILL.md`
  §Findings format; `agents/warden.md`; `templates/sdd-round.md`; `ruff.toml`;
  `CONTRIBUTING.md` §the runner
- `seal/specs/1789356180-…/rounds/round-2.md` and `round-2-report.md`;
  `seal/ledger/1789356180-….md`; the `seal/ledger.md` rows this range touched

Read but not opened as evidence: round 2's report prose and the spawn prompt.
Every claim either of them carried that this report repeats was re-derived
above, and the two aggregates I did not re-derive are named as carried.

Needs a fix: yes — 1, 2 and 3

Loses a record or crashes: yes — 1

Finding 1 is a crash rather than a lost record: `new` dies at
`round_record.py:1970` inside `build`, before any record is written, and
`close` dies at `:3307` before it rewrites one. Nothing on disk is damaged. What
the gate is answering is that a reachable input leaves the generator as a stack
trace at exit 1 instead of a refusal at exit 2, on the path this whole work
item is about.

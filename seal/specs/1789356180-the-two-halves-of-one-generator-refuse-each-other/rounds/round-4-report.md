# 1789356180-the-two-halves-of-one-generator-refuse-each-other — review round 4

Target is the diff of round 3's fixes, `c2b2b30..151792e`, three commits, and
the six units round 3's record names as reviewed by nobody. Round 3's four
verdicts are inherited as closed; the work was the answers and the new units.

Reviewed in a `git clone --no-local` at `151792e`, with the repository's own
runner in a virtual environment inside that clone. Nothing was written in the
working tree except this file.

**The run's own position, since it decides what a finding here can be asked
to do.** This round exists past the reopening bound: `docs/review-chain-spec.md`
§*The reopening — one, and then the run is capped* says the record that reads a
reopening round's fixes ends the run whatever it finds, and every finding still
open there becomes an issue with `deferred #N`. So the four findings below are
written to be applied without me — each is a prose or assertion edit with a
paste-ready block — and if the owner would rather ship, each is an issue with
its coordinate and its measurement already in it.

## What the fix pass got right, stated first because it decides the rest

**The narrower bound is the right bound and it is safe.** Round 3 proposed
`len(seen) < len(VERDICT_HEADER)`; the fix pass chose `VERDICT_COL`, refusing
exactly what crashes. Both halves of that choice were executed rather than
read.

- The wider bound really does turn a shipped case red. Applied to the
  generator, `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one`
  fails and the rest of its module passes — 1 failed, 118 passed, against 119
  passed unmutated.
- What the narrower bound now admits reaches no index anywhere. A four-cell row
  is indexed at `NUMBER_COL` and `VERDICT_COL` only; `GROUNDS_COL` is read in
  `close`'s write pass and only after the padding loop above it, and `close`'s
  recomputation of the verdict words re-reads through `row_cells`, which returns
  the row's own width and is then indexed at `VERDICT_COL`. Probed end to end: a
  four-cell row through `new` exits 0 and is written short, the same row through
  `close` inside the fix table is rewritten and padded, and the same row outside
  the fix table is copied back untouched. No traceback on any of the three.
- The crash round 3 opened is closed on both subcommands, not only the one the
  new case covers. A two-cell numbered row hand-edited into a record and run
  through `close` exits 2 with the new refusal, quoting the row.

**`says_open` is right about the corpus and the documents.** Every one of the <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
committed verdict cells that begins `open` is reached, none of them is in
`CLOSED_WORDS`, and no admitted no-digit row is newly refused. Re-derived
through the module's own reader rather than carried.

## 1. 🟡 The re-measurement does not reproduce, and it is now in three files

`skills/code-review/scripts/round_record.py:2391`,
`tests/test_a_finding_id_is_a_bare_integer.py:379`

Both docstrings state *127 verdict cells begin `open` and 9 of them continue,
so equality reached 118 of 127*, and the spawn prompt carries *0 of 2,028
verdict rows short* beside it. Re-derived at `151792e` through the module's own
`table_body` over every committed `round-N.md`: **1,704 verdict rows in 176
records that parse, 95 cells beginning `open`, 7 of them wider, 88 reached by
equality, 0 in `CLOSED_WORDS`.**

Those are round 3's figures, and the fix pass reports having got different ones
because *the corpus grew by this run's own records*. It did not. I measured six
populations to find the one that yields 127, and none does: records alone give
95; records plus this work item's own reports give 108; records plus every
report in the tree give 570; the loosest pipe-row reading of the records gives
95 again, and `chain_check`'s own verdict reader gives 95 again. The nearest
figure I can produce is 129, and only by counting every cell of every column of
every record that begins with `open` — which is not a count of verdict cells.

Why it matters here rather than as a nit: the number is the evidence for the
design. It is what says the equality was losing rows and the boundary match is
free, it is the same sentence the ledger fragment now carries, and a reader who
re-measures it finds 95. Two of the three claims around it do reproduce — *15 of
the 25 admitted rows carry a verdict outside `CLOSED_WORDS`* is exact, and *0
newly refused* is exact — which is what makes the wrong one worth removing
rather than discounting.

## 2. 🟡 The boundary it borrows is not the boundary it names

`skills/code-review/scripts/round_record.py:2386`, `:2470`,
`docs/review-chain-spec.md:776`,
`tests/test_a_finding_id_is_a_bare_integer.py:382`

Four live coordinates say the same thing in four wordings: *`verdict_of`
already ends a vocabulary word on `chain.SEPARATORS` — that is what makes
`fixed d3fe44d` read as `fixed`*, *the boundary `verdict_of` already uses*,
*the boundary `verdict_of` already uses for its own vocabulary*. The ledger
fragment carries a fifth copy.

`verdict_of` does not do that. It ends its vocabulary on a space or a comma —
`s == word or s.startswith(word + " ") or s.startswith(word + ",")` — and its
own docstring says so in as many words: *ended by a space or a comma*.
`chain.SEPARATORS` appears in that function once, in the separate question of
whether a home word has anything after it. Executed: `fixed d3fe44d` reads as
`fixed` and `fixed—d3fe44d` reads as the whole cell, as do `fixed-d3fe44d` and
`fixed:d3fe44d`. So the sentence is wrong about the set and wrong about what
makes the example work.

The behaviour follows the sentence rather than the code, and is wider than
every document describing it. `says_open` returns True for `open-ended <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
question` and for `open: see 5`, because `-` and `:` are in the wider set — and
the refusal a reviewer then reads says *the `Verdict` cell reads `open`*, of a
cell that does not. That is the same over-reach the module names one function
above, where dropping the boundary would let `not a defect` swallow `not a
defective reading`.

And the coupling runs the wrong way. `chain.SEPARATORS` has five other readers
and `chain_check.py`'s own prose weighs widening it; widening it now silently
widens what counts as the open verdict, while the vocabulary boundary the
documents say it shares would not move at all.

**The fix that makes all five sentences true at once is the narrower test, not
five rewrites.** Executed: ending the word on a space or a comma reaches all 95
committed cells — every wider spelling in the corpus continues with one or the
other — excludes `open-ended` and `open:`, and leaves both modules green, 63
and 119 passed. Taking it means the borrowed-boundary claim becomes accurate
where it stands, and only the example in it needs correcting.

## 3. 🟡 The claim the fix overturned is still standing seven lines above it

`skills/code-review/scripts/round_record.py:2370`

The comment introducing `OPEN_WORD` reads *and exact rather than a vocabulary <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
test, which is the distinction the grounds for NOT reading the verdict missed*.
The match stopped being exact in this commit. `says_open` is defined ten lines <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
below that sentence, and the comment directly above it — in the same block, on
the same screen — was rewritten by this same fix pass.

This is round 3's 🟡 3 reproduced by the commit that closed it: an overturned
claim corrected in four carriers and left standing in a fifth, inside the file
being edited. Every other live carrier is clean — I grepped the class and the
only remaining copies are in committed round records and reports, which are
history and correctly left alone. `test_the_verdict_ruling_is_against_a_vocabulary_test_not_against_reading` <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
guards the spec's copy and nothing guards this one, which is why it survived.

## 4. 🟡 The case guarding the narrower bound states a mechanism that does not happen

`tests/test_a_finding_id_is_a_bare_integer.py:348`

`test_a_row_missing_only_its_grounds_is_still_written_short` carries the comment <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
*The row IS refused, by the verdict arm — it reads `open` with a `#` cell that
keys it, so `Pass` is decided on it*, and then asserts `code in (0, 2)`.

The row is not refused. Executed at `151792e`: `| 1 | one | \`f.py:1\` | open |`
through `new` exits **0** and the record is written, carrying the row at four
cells. The verdict arm never sees it — that arm runs only where `finding_number`
returned `None`, and a row with a digit in its `#` cell is keyed. A numbered row
reading `open` is an ordinary open finding, which is why `Pass` is simply not
ticked.

The assertion was written to hedge that uncertainty and it admits both answers,
so the case cannot fail on the regression it exists to name: a future change
that starts refusing this shape with any message other than the one the case
greps for leaves it green. The case's other assertion does kill round 3's
proposed bound, which is what makes it worth repairing rather than replacing —
executed, that bound turns exactly this case red and nothing else in the module.

## 5. ⬜ The short-row refusal stops at the first offending row

`skills/code-review/scripts/round_record.py:3126`

`finding_number`'s docstring states the rule the loop around it follows:
*`bad` is a list rather than a raise. #303 measured five offending rows against
a message naming one, at two round trips per repair.* The new guard raises
immediately, quoting one row, so a report with three short verdict rows costs
three runs.

Left as a note rather than a fix: the guard was already an immediate raise
before this commit — only its condition widened — and zero committed verdict
rows are short, so the cost falls on a reviewer's first draft and nowhere else.
Worth a sentence in the comment if anyone opens the function again.

## 6. ⬜ The spec paragraph's rewrap left a three-word line

`docs/review-chain-spec.md:776`

The inserted clause left *test, and the* alone on its own line. It renders
correctly and the claim is finding 2's, not this one's; this is only the wrap.

## Answers to what round 3 left, and to what the fix pass asked to be checked

**Round 3's ⬜ 5 was left alone deliberately, and the reasoning holds.** I read
`chain_check.open_blocking` rather than the report of it: it selects rows by
`BLOCKING in "".join(seen)` and an unclosed verdict, so a record hand-edited
after `close` to carry `| carried | … | open | … |` is invisible to it, exactly
as stated. Both generator subcommands refuse the shape, the record is a
generated file, and a hand-edit after the last generator run is the residual
class the checker already only partly covers. A second gate would be mechanism
no finding required, and I would not open it. What is worth saying out loud,
because there is no round after this one: the rule lives in
`docs/review-chain-spec.md`, which is the checker's own specification, so the
gap is a stated divergence rather than an oversight, and it should be recorded
as one if the branch ships.

**The mutation report is accurate.** Four mutations run here, each killed, and
the survivor the fix pass reports is real: dropping the separator test from
`says_open` leaves the whole module green except <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
`test_a_word_that_merely_begins_with_open_is_not_the_open_verdict`, which is <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
the case written for it.

**The new cases were seen red where they could be.** Against `c2b2b30`'s
generator the module gives 4 failed, 59 passed:
`test_a_numbered_short_row_is_refused_rather_than_raising` and three of the four <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
parameters of `test_every_spelling_of_open_the_records_hold_is_refused` — the <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
bare `open` parameter stays green because equality already caught it, which is
correct. The other two new cases are green pre-fix by construction, and each is
killed by the mutation named for it.

**The ledger fragment's anchors survive.** `evidence-check .` exits 0 at
`151792e`: 1,220 ok, 0 drifted, 0 broken, this work item's fragment 28 ok. Both
functions moved and both re-hash.

**Round 3's record is a truthful application of its fix table.** Findings 1
through 4 read `**fixed** fec2c88`, the rest read `answered`, and `New units`
names `says_open` and all five cases. Under `seal/specs/`, so a correction <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
surface.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The re-measurement *127 verdict cells begin `open`, 9 continue, equality reached 118* does not reproduce under any population. The module's own reader gives 95, 7 and 88 over 1,704 rows in 176 records — round 3's figures. The same sentence is in the ledger fragment | `skills/code-review/scripts/round_record.py:2391`, `tests/test_a_finding_id_is_a_bare_integer.py:379` | open | executed at `151792e` — six populations measured through `table_body` and through `chain_check.verdict_table`: records 95/7, records plus this item's reports 108/7, records plus all reports 570/15, loose pipe-row reading 95/7. The nearest figure to 127 is 129, and only by counting every cell of every column. The two neighbouring claims, *15 of 25* and *0 newly refused*, both reproduce exactly |
| 2 | 🟡 Four live coordinates say `says_open` borrows the boundary `verdict_of` uses for its vocabulary. `verdict_of` ends its vocabulary on a space or a comma and says so in its own docstring; `chain.SEPARATORS` is six characters wide, so `open-ended question` and `open: see 5` are refused as the open verdict and the refusal names a word the cell does not carry | `skills/code-review/scripts/round_record.py:2386`, `:2470`, `docs/review-chain-spec.md:776`, `tests/test_a_finding_id_is_a_bare_integer.py:382` | open | executed at `151792e` — `fixed d3fe44d` reads `fixed`; `fixed—d3fe44d`, `fixed-d3fe44d` and `fixed:d3fe44d` read as the whole cell. `says_open` is True for `open-ended question` and `open: see 5`. The proposed narrower boundary reaches all 95 committed cells, excludes both, and leaves the two modules green at 63 and 119 passed <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| 3 | 🟡 The comment introducing `OPEN_WORD` still reads *exact rather than a vocabulary test*, ten lines above the function that replaced the exact match, and directly under a comment this same commit rewrote. Round 3's 🟡 3 class, one member left standing in the edited file | `skills/code-review/scripts/round_record.py:2370` | open | read at `151792e`, class enumerated by grep: every other live carrier of the overturned ruling is corrected, and the only remaining copies are in committed records and reports, which are history. The spec's copy is guarded by a case; this one is guarded by nothing <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| 4 | 🟡 `test_a_row_missing_only_its_grounds_is_still_written_short` says the four-cell row *IS refused* and asserts `code in (0, 2)`. It is not refused: `new` exits 0 and writes the record with the row at four cells, because a keyed row never reaches the verdict arm. The assertion admits both answers, so the case cannot fail on the regression it names | `tests/test_a_finding_id_is_a_bare_integer.py:348` | open | executed at `151792e` — the case's own input through `generate` gives exit 0, the record on disk, and `\| 1 \| one \| \`f.py:1\` \| open \|` in its verdict table. The repaired assertions were run and pass <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| 5 | ⬜ The new short-row guard raises on the first offending row, inside the loop whose docstring states #303's rule that offending rows are collected and refused once. Pre-existing in shape — only the condition widened — and zero committed rows are short | `skills/code-review/scripts/round_record.py:3126` | open | read at `151792e` against `finding_number`'s own docstring and the `bad`/`owed` accumulation beside the guard |
| 6 | ⬜ The inserted clause left *test, and the* alone on a line | `docs/review-chain-spec.md:779` | open | read at `151792e`; renders correctly |
| 7 | Round 3's 🔴 1 is closed on both subcommands, not only the one the new case covers | `skills/code-review/scripts/round_record.py:3112` | answered | executed at `151792e` — a two-cell numbered row through `new` exits 2 with the new refusal; the same row hand-edited into a record and run through `close` exits 2 with the same message, no traceback |
| 8 | The narrower bound admits nothing that reaches an index elsewhere. Every caller indexes `NUMBER_COL`, `VERDICT_COL`, or `GROUNDS_COL` behind the padding loop | `skills/code-review/scripts/round_record.py:1970`, `:3360`, `:3377`, `:3426`, `:3444` | answered | executed at `151792e` — a four-cell row through `new` (written short, exit 0), through `close` inside the fix table (rewritten and padded) and through `close` outside it (copied back untouched). No traceback on any path; read at all five index sites |
| 9 | The grounds for refusing round 3's own paste-ready bound are true | `tests/test_the_record_is_generated.py:2214` | answered | executed at `151792e` — with the bound widened to the header width, `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one` is the one failure, 1 failed and 118 passed against 119 passed unmutated |
| 10 | The new cases were seen red where they can be, and the rest are killed by the mutation each was written for | `tests/test_a_finding_id_is_a_bare_integer.py:324`, `:370`, `:397` | answered | executed at `151792e` — the module against `c2b2b30`'s generator: 4 failed, 59 passed. Mutations: bound back to `NUMBER_COL` kills the short-row case; dropping the separator test kills the longer-word case; equality restored kills three of the four spelling parameters |
| 11 | `says_open` reaches the corpus it claims and costs nothing, whatever the count beside it says | `skills/code-review/scripts/round_record.py:2380` | answered | executed at `151792e` — all 95 committed cells beginning `open` reached, none in `CLOSED_WORDS`, 0 of the 25 admitted no-digit rows newly refused <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| 12 | Round 3's 🟡 3 class is otherwise fully enumerated; the only remaining copies of the overturned ruling are in committed records and reports | `docs/review-chain-spec.md:790`, `skills/code-review/scripts/round_record.py:2363`, `:2449`, `tests/test_a_finding_id_is_a_bare_integer.py:236` | answered | read at `151792e` — grep of the claim across the tree; four live carriers corrected, one missed and opened as finding 3 |
| 13 | Round 3's ⬜ 5 was left alone on sound grounds, and its premise is what the checker does | `skills/code-review/scripts/chain_check.py#open_blocking` | answered | read at `151792e` — rows are selected by `BLOCKING in "".join(seen)` and an unclosed verdict, so a no-digit row reading `open` is invisible at CI. Both generator subcommands refuse it. Named here rather than reopened, and worth recording as a stated divergence if the branch ships |
| 14 | The ledger fragment's anchors survive the fix and both moved functions re-hash | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | answered | executed at `151792e` — `evidence-check .` exits 0: 1,220 ok, 0 drifted, 0 broken, this fragment 28 ok |
| 15 | Round 3's record is a truthful application of its fix table, and `New units` names all six | `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-3.md` | answered | read at `151792e` against the three commits. Under `seal/specs/`, so a correction surface rather than a fix surface |
| 16 | The ledger fragment carries findings 1 and 2 in its own words — the count 127 and the borrowed boundary. A correction, taken with whichever fix those two findings get | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | open | read at `151792e`. Under `seal/ledger/`, so a correction surface and not counted by `Needs a fix` |

## Paste-ready fixes

Finding 1 — `skills/code-review/scripts/round_record.py`, the second paragraph
of `says_open`: <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->

```python
    Measured over every committed record: 95 verdict cells begin `open` and 7
    of them continue, so equality reached 88 of 95 while `agents/warden.md`,
    `templates/sdd-round.md` and `skills/code-review/SKILL.md` all describe a
    match on the word. None of the 95 is in `CLOSED_WORDS`, and the boundary
    match newly refuses 0 of the 25 admitted rows (round 3's 🟡 2).
```

Finding 1 — `tests/test_a_finding_id_is_a_bare_integer.py`, inside
`test_every_spelling_of_open_the_records_hold_is_refused`: <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->

```python
    Measured over every committed record: 95 verdict cells begin `open` and
    **7 of them continue** — `open — deferred`, `open, comment only` and five
    more — so the equality reached 88 of 95 while the documents described all
    of them. A head match ended the way `verdict_of` ends its own vocabulary,
    on a space or a comma, reaches all 95 and newly refuses **0** of the 25
    admitted no-digit rows.
```

Finding 2 — `skills/code-review/scripts/round_record.py`, the boundary itself
and the paragraph that justifies it. This is the variant that makes the
borrowed-boundary sentence true rather than rewriting it in five places:

```python
# The boundary `verdict_of` ends its own vocabulary on -- `fixed d3fe44d` and
# `fixed, d3fe44d` are both `fixed`. Spelled here rather than reached for in
# `chain.SEPARATORS`, which is six characters wide and has five other readers:
# borrowing it made `open-ended question` and `open: see 5` read as the open
# verdict, and tied what counts as open to a constant the `deferred` home
# reader is free to widen.
OPEN_BOUNDARY = (" ", ",")


def says_open(word):
    """`word` is the open verdict, however the reviewer ended it.

    The grounds for not running a VOCABULARY test hold and are untouched:
    `verified` is in no vocabulary and would be refused, which costs 15 of the
    25 admitted no-digit rows in the committed records. What never followed
    from those grounds is EQUALITY. `verdict_of` ends a vocabulary word on a
    space or a comma — that is what makes `fixed d3fe44d` read as `fixed` —
    and the same boundary here reaches `open — deferred` and `open, comment
    only`.

    Measured over every committed record: 95 verdict cells begin `open` and 7
    of them continue, so equality reached 88 of 95 while `agents/warden.md`,
    `templates/sdd-round.md` and `skills/code-review/SKILL.md` all describe a
    match on the word. Every one of the 7 continues with a space or a comma,
    so the narrow boundary reaches all 95; none of them is in `CLOSED_WORDS`,
    and the match newly refuses 0 of the 25 admitted rows (round 3's 🟡 2).
    """
    if not word.startswith(OPEN_WORD):
        return False
    rest = word[len(OPEN_WORD) :]
    return not rest or rest[0] in OPEN_BOUNDARY
```

Finding 2 — `skills/code-review/scripts/round_record.py`, inside
`finding_number`:

```python
    **The `#` cell is not the only cell that says a row owes an answer**, which
    is why `verdict_rows` reads the Verdict cell beside it. Reading the marker
    alone admitted six shapes whose Verdict cell said `open` — three of them
    carrying no marker at all, so the residual stated here for a round did not
    describe them (round 2's 🟡 7). It matches the WORD — `says_open` ends it
    on a space or a comma, the boundary `verdict_of` uses for its own
    vocabulary — rather than a vocabulary, and that is what makes it free:
    `verified` is in no vocabulary and therefore OPEN, so refusing everything
    outside `CLOSED_WORDS` would refuse 15 of the 25 admitted rows.
```

Finding 2 — `docs/review-chain-spec.md`, the paragraph at line 776, which also
carries finding 6's rewrap:

```markdown
That is a match on the word — ended by a space, a comma, or nothing, the
boundary `verdict_of` uses for its own vocabulary, so `open — deferred` and
`open, comment only` are reached and `opened` is not — rather than a
vocabulary test, and the difference is what makes it free. `verified` is in no
vocabulary and therefore reads OPEN, so refusing everything outside
`CLOSED_WORDS` would refuse every confirmation row — one refusal traded for
another. Refusing the word `open` refuses none of them: of the 25 admitted
no-digit cells in the committed records, not one reads it.
```

Finding 2 — `tests/test_a_finding_id_is_a_bare_integer.py`, inside
`test_a_word_that_merely_begins_with_open_is_not_the_open_verdict`, so the <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
boundary has a case of its own rather than only a sentence:

```python
@pytest.mark.parametrize(
    "verdict", ["opened in round 2", "openly carried", "open-ended question"]
)
def test_a_word_that_merely_begins_with_open_is_not_the_open_verdict(repo, verdict):
    """The boundary is what makes `says_open` match a WORD rather than a
    prefix of one — the same distinction `verdict_of` states for its own
    vocabulary, where without it `not a defect` would swallow `not a defective
    reading`.

    It is the same boundary as well as the same distinction: a space or a
    comma, not `chain.SEPARATORS`. The wider set reached `open-ended question`
    and `open: see 5`, and the refusal then named a word the cell does not
    carry.

    Found by mutation: dropping the separator test left every other case in
    this module green, because no case fed it a longer word.
    """
    _code, out = a_report(repo, f"| carried | one | `f.py:1` | {verdict} | read |\n")
    assert "`Verdict` cell reads `open`" not in out, out
```

Finding 3 — `skills/code-review/scripts/round_record.py`, the comment above
`OPEN_WORD`: <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->

```python
# The one verdict word that says the row is open in as many letters. Read only
# on a row whose `#` cell has already admitted it, where the two cells then
# contradict each other -- and one WORD rather than a vocabulary test, which
# is the distinction the grounds for NOT reading the verdict missed.
# `verified` is in no vocabulary and therefore OPEN, so reading the verdict as
# OPEN/CLOSED would refuse every confirmation; reading this one word refuses
# none of them. `says_open` below is where the word ends. Free against the
# corpus: of the 25 admitted no-digit rows in the committed records, not one
# has a Verdict cell reading `open` (round 2's 🟡 7).
```

Finding 4 — `tests/test_a_finding_id_is_a_bare_integer.py`, the body of
`test_a_row_missing_only_its_grounds_is_still_written_short`. Run here and <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. -->
green:

```python
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(verdicts="| 1 | one | `f.py:1` | open |\n")
    )
    assert "Traceback" not in out and "IndexError" not in out, out
    assert "no `Verdict` cell" not in out, out
    # ADMITTED, and written at the width the reviewer left. The verdict arm
    # never sees this row -- a digit in the `#` cell keys it, and that arm runs
    # only where `finding_number` returned None -- so `new` exits 0 and the
    # record carries four cells. Round 3's wider bound turns exactly this case
    # red, which is why the bound is `VERDICT_COL`.
    assert code == 0, out
    assert "| open |" in text, text
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py -q` at `151792e` in the clone | 63 passed, exit 0 |
| `bin/test tests/test_the_record_is_generated.py -q` at `151792e` in the clone | 119 passed, exit 0 |
| the same bare-integer module against `c2b2b30`'s `round_record.py` | 4 failed, 59 passed — the short-row case and three of the four spelling parameters red; the bare `open` parameter green, because equality already caught it |
| mutation: bound back to `len(seen) <= NUMBER_COL` | 1 failed — `test_a_numbered_short_row_is_refused_rather_than_raising` <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| mutation: bound widened to `len(seen) < len(VERDICT_HEADER)`, round 3's proposal | in the bare-integer module, 1 failed — `test_a_row_missing_only_its_grounds_is_still_written_short`; in `test_the_record_is_generated.py`, 1 failed and 118 passed — `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one`, against 119 passed unmutated. Finding 9's grounds <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| mutation: `says_open` returns True without testing the boundary | 2 failed — both parameters of `test_a_word_that_merely_begins_with_open_is_not_the_open_verdict`. The fix pass's survivor reproduces <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| mutation: the verdict arm restored to equality | 3 failed — the three wider spelling parameters |
| probe: `\| 1 \| one \|` through `new`, and the same row hand-edited into a record through `close` | exit 2 both times with the new refusal quoting the row; no traceback, no record written. Finding 7 |
| probe: a four-cell row through `new`, through `close` inside the fix table, and through `close` outside it | exit 0 and written short; rewritten and padded; copied back untouched. No traceback on any path. Finding 8 |
| every committed `round-N.md` through the module's own `table_body` | 176 of 216 parse, 1,704 verdict rows, **0 short**, 51 no-digit, 25 admitted, 15 of those outside `CLOSED_WORDS`. Finding 1 |
| every committed verdict cell through `verdict_of`, counting cells that begin `open` | **95** across 8 spellings — 88 bare, 7 wider, none in `CLOSED_WORDS`; `says_open` reaches all 95 and newly refuses 0 of the 25 admitted rows. Findings 1 and 11 <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| the same count over five other populations — records plus this item's reports, records plus all reports, every `.md` in the tree, the loose pipe-row reading, and `chain_check.verdict_table` | 108, 570, 570, 95, 95. None is 127. Finding 1 |
| `verdict_of` over `fixed d3fe44d`, `fixed, d3fe44d`, `fixed—d3fe44d`, `fixed-d3fe44d`, `fixed:d3fe44d` | `fixed`, `fixed`, and the whole cell for the last three — the vocabulary boundary is a space or a comma, not `chain.SEPARATORS`. Finding 2 |
| `says_open` over 22 spellings a reviewer might write | `open-ended question` and `open: see 5` are refused as the open verdict; `still open`, `open?` and `open; see 5` are not reached. Finding 2 <!-- NAME NOT IN TREE: the unit was reverted at 1ff0a6c and the seam lives in #395; the record keeps the name as the round read it. --> |
| the proposed narrow boundary applied to the generator | reaches 95 of 95 committed cells, excludes `open-ended question` and `open: see 5`; 63 passed and 119 passed across the two modules, exit 0 both. Finding 2 |
| the repaired assertions for finding 4, run as written | 1 passed — exit 0, the record on disk, the row at four cells |
| `bin/evidence-check .` at `151792e` | exit 0 — 1,220 ok · 0 drifted · 0 broken; this work item's fragment 28 ok. Finding 14 |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** Contract §2 leaves all three to the sealer, and this round ran none of them. It has not come due: findings 1 through 4 are open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-3 | `skills/code-review/scripts/round_record.py:3112`, `:1970`, `:3360`, `:3426` | round 3's 🔴 1 — fixed, re-checked here on both subcommands |
| round-3 | `skills/code-review/scripts/round_record.py:2380`, `:3148` | round 3's 🟡 2 — fixed; its grounds are findings 1 and 2 |
| round-3 | `docs/review-chain-spec.md:790`, `skills/code-review/scripts/round_record.py:2363`, `:2449`, `tests/test_a_finding_id_is_a_bare_integer.py:236` | round 3's 🟡 3 — fixed at four carriers; the fifth is finding 3 |
| round-3 | `skills/code-review/scripts/round_record.py:2411` | round 3's ⬜ 4 — fixed, the docstring re-indents whole |
| round-3 | `skills/code-review/scripts/chain_check.py#open_blocking` | round 3's ⬜ 5 — answered, premise verified here |
| round-3 | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | round 3's 11 — anchors re-hash, `evidence-check` exit 0 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | — | — |

Needs a fix: yes — 1, 2, 3 and 4

Loses a record or crashes: no

Nothing found here leaves the root or crashes. The crash round 3 opened is
closed on both subcommands and the bound that closed it admits nothing that
reaches an index elsewhere — both executed rather than read. Findings 1 through
4 are a false measurement, a false mechanism, a stale comment and an assertion
that cannot fail; each is a prose or assertion edit with a block above, and
none of them is a shipped behaviour except finding 2's over-refusal of
`open-ended`, which the same block closes.

## Proof

Opened at `151792e`: `skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`,
`tests/test_a_finding_id_is_a_bare_integer.py`,
`tests/test_the_record_is_generated.py`,
`tests/test_the_rules_have_one_owner.py`, `docs/review-chain-spec.md`,
`skills/code-review/SKILL.md`, `agents/warden.md`, `templates/sdd-round.md`,
`bin/test`, `seal/ledger.md`,
`seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md`,
`seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-3.md`,
`seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/changelog.md`.
Every probe ran in a `git clone --no-local` at `151792e`; the clone and its
probe files are deleted.

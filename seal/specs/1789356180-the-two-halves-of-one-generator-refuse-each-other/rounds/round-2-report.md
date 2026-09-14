# Round 2 — 1789356180-the-two-halves-of-one-generator-refuse-each-other

| Field | Value |
|---|---|
| Target SHA | `5bf88c1` |
| Reviewed | `git diff c9912a4..5bf88c1` — round 1's fix pass, four commits, 15 files |
| Earlier rounds | round 1 at `aaeb5dd`, five fixed and one answered |
| Kind | verifying round |

## What this round did

Reviewed in a `git clone --no-local` at `5bf88c1`, deleted at the end along
with every probe. The surface is round 1's fix diff and nothing wider: six
verdicts to check, six new units nobody has reviewed, and the four things the
handover asked me to read rather than rediscover.

Round 1's five fixed verdicts are all genuinely closed, and each of the five
cases that pins them was seen red by reverting the line it pins. The corpus
split was re-derived independently and matches. The exemption is sound.

One thing is open, and it is the class round 1's 🔴 1 belongs to, one cell
over.

---

## The finding

### 🟡 7 — The admission rule reads the `#` cell and never the Verdict cell, so a row that says `open` in its own record still ticks `Pass`

`skills/code-review/scripts/round_record.py:2447` (`finding_number`'s admitting
arm) · `skills/code-review/scripts/round_record.py:3063` (`verdict_rows`)

The repair reads one of the two columns that say whether a row owes an answer.
`OWED_MARKERS` is the right pair — 🔴 and 🟡 are exactly the two severities
`agents/warden.md` §Report counts toward `Needs a fix`, and the corpus backs
that without a margin — but the marker is not the only place a row says it is
open. The Verdict cell says it in as many letters, and nothing reads it.

Executed at `5bf88c1`, one work item per shape, each row's Verdict cell reading
the literal word `open`:

| The verdict row the report carried | `new` | The record it wrote |
|---|---|---|
| `\| 🟢 fix-surface \| … \| open \| read \|` | exit **0**, silent | `- [x] Pass` |
| `\| carried \| … \| open \| read \|` | exit **0**, silent | `- [x] Pass` |
| `\| ⬜ \| … \| open \| read \|` | exit **0**, silent | `- [x] Pass` |
| `\| ❓ \| … \| open \| read \|` | exit **0**, silent | `- [x] Pass` |
| `\| A \| … \| open \| read \|` | exit **0**, silent | `- [x] Pass` |
| `\| — \| … \| open \| read \|` | exit **0**, silent | `- [x] Pass` |

That is round 1's 🔴 1 as written: a record asserting a review passed while its
own verdict table says otherwise, `new` exiting 0 and printing nothing.

The build states a residual, and this is wider than the sentence it states.
`docs/review-chain-spec.md` §*A verdict row that commissions nothing* says the
check *cannot catch a reviewer who picks the wrong marker*, which frames what is
left as a judgment call nothing could recover. It is not: in every row above the
record itself carries the answer, in the column beside the one the rule reads.
Three of the six shapes — `carried`, `A`, `—` — carry no severity marker at all,
so the stated residual does not reach them even as a description.

**Why the build's own grounds do not cover it.** The documents and the constant
both say *the verdict word cannot do this job*, because a confirmation reads
`verified`, which is in no vocabulary and therefore OPEN. That is true of
**replacing** the marker check and false of **composing** with it. The word
wanted here is not *anything outside `chain_check.CLOSED_WORDS`* — it is the
literal `open`, which is unambiguous and which no admitted row uses.

**Free against the corpus.** Re-derived through `table_body` and the unverified
reader over the 209 committed records: of the 51 no-digit `#` cells, the 25 that
the rule still admits carry the verdict words `fixed`, `answered`, `truthful`,
`out of verified scope`, `record only`, `nit, no fix`, `carried, not re-judged`,
`anchors resolve` and `consistent`. **None reads `open`.** Zero committed rows
change.

I applied the paste-ready fix below in the clone and measured it: all six shapes
above refuse at exit 2 with no record written, and
`tests/test_a_finding_id_is_a_bare_integer.py` and
`tests/test_the_fixes_close_the_record.py` stay at 113 passed, exit 0 —
including `test_every_no_digit_shape_the_corpus_holds_is_admitted`, whose five
parameters all carry `verified`.

§12 is the reason this is a finding rather than a preference. Round 1's 🔴 1
named a class — *a row admitted as commissioning nothing while the record says
something is owed* — and the fix enumerated two members of it, the owed marker
and the empty cell. This is the third, and it is the one the record states in
words.

### ⬜ 8 — `survivors.md`'s header comment says five survivors and names one as absent that is in the table

`seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/survivors.md:27`

At `53d92ac` the section's comment was true: five rows in the table, and
`plan.md`'s standing paragraph exempted separately. At `a28bb03` the `plan.md`
row was added to the table, making six, and the comment was not touched. It now
says *Five more* over six rows, and *ONE survivor … is not in this table:
`plan.md`'s What breaks in six months paragraph*, which is row 3 of the table
immediately below it.

Located under `seal/specs/`, so a correction rather than a fix to commission,
and `Needs a fix` does not count it. Worth saying in the same breath as finding
9 below: the exemption itself is right and only its prose has come loose.

### ⬜ 9 — A report carrying both a malformed id and an owed row costs two round trips

`skills/code-review/scripts/round_record.py:3073`

`bad` is a list rather than a raise because #303 measured five offending rows
against a message naming one, at two round trips per repair. `owed` is a second
list and is refused after `bad`, so a report holding one of each surfaces only
the first. Executed: a report carrying `R2-1` and `🔴 A` refuses naming `R2-1`
alone, and the `🔴 A` row appears nowhere in the message.

The build states this as a design call and the grounds are real — the two
messages say different things and merging them would read worse. Recorded
rather than commissioned, because it is one extra run in a mixed-error report
and not the N-per-row cost #303 was about.

---

## What I checked and found closed

Each of round 1's six verdicts, on my own grounds.

**🔴 1 is closed for the two arms the fix enumerated.** The refusal now fires
inside `new`, at `verdict_rows`, before any record is written. Executed: the
four owed parameters (`🔴 A`, `🟡 A`, `🔴`, `🟡 fix-surface`) and the empty cell
all refuse at exit 2 with no `- [x] Pass` in the output. The empty-cell arm is
there and it is load-bearing — dropping `not text or` from the guard turns
`test_an_empty_hash_cell_is_refused` red on its own. The fix went past round 1's
paste-ready code and was right to: that code read the severity only, and an
empty cell carries none.

`OWED_MARKERS` holds 🔴 and 🟡 and leaves out 🟢, ❓, ⬜ and `✅`. That is the
right pair for what it does. `agents/warden.md` §Report puts the line at *would
the release ship a defect if this stands?*, which is exactly 🔴 and 🟡; ❓ is a
closing verdict in `chain_check.CLOSED_WORDS`; ⬜ is defined as the severity
`Needs a fix` never counts. Dropping 🟡 from the tuple turns two of the four
parameters red, so both members are pinned. What the set leaves out is finding 7
above, and that is about the column the rule reads, not about the tuple.

**🟡 2's corpus correction is right, re-derived rather than carried.** Through
`table_body` and the unverified reader over the committed records: 199 refused
cells carrying digits, 51 carrying none, 44 of those a severity marker and a
single letter, 7 the admitted shape (`carried` ×2, `🟢 fix-surface` ×2,
`🟢 fragment`, `🟢 grep`, `🟢 overview`), `✅` at zero, a bare em dash at zero,
empty at zero. 26 carry 🔴 or 🟡, splitting 11 `fixed` / 4 `answered` / 11 `open`.
Every figure the fix pass wrote into nine places holds.

My total verdict-row count is 2,001 against round 1's 1,989, because round 1's
own record and one other landed between the two reads. The 199 / 51 / 44 / 7 /
26 figures are unaffected, and they are the ones the documents state.

**🟡 3 was understated by round 1 and the fix pass was right.** Reverting `head`
to the anywhere-split turns all four separators red — `,`, `—`, `:` and `-` —
not the comma alone. Round 1's *the em-dash spelling works* was true only of
`answered — corrected`, where a space follows the word; `answered— corrected` is
broken exactly like the comma. The case asserts by extracting the advised row
from the message and running `close` over it, then checking the verdict landed
as `answered` with the suffix in the Grounds cell. That is the only shape that
catches a refusal advising a row that is itself refused, and it is the shape the
case has.

**🟡 4 is closed.** Reverting the front-strip to the equality test turns
`test_a_deferred_row_whose_third_cell_begins_with_its_home_says_it_once` red;
the case asserts `one[4].count("#309") == 1` with the grounds still present.

**⬜ 5 is closed.** Reverting the `or "no numbered rows at all"` fallback turns
`test_the_unknown_finding_refusal_says_so_when_the_table_holds_no_id` red.

**Finding 6's ledger correction is true as corrected.** `seal/ledger.md` row R1's
clause now reads *a cell carrying none is refused in the fix table, where the row
is the commission, and in the verdict table is admitted as a row that commissions
nothing unless it is empty or carries 🔴 or 🟡*. Both tables are named and the
severity rule is carried. Read against `fix_table`, which passes `False` for
`idless`, and against the admitting arm.

**The compatibility claim is load-bearing and it holds.** `finding_number` and
`verdict_rows` have no caller outside `round_record.py` — two call sites, both
in that module. The path that does read committed records, `inherited_rows`,
goes through `table_of` and `verdict_words` and never reaches the id rule, so a
round 2 inheriting a round 1 full of `🔴 A` rows is unaffected. CI's hygiene job
runs `chain_check.py`, not the generator. Measured: 10 committed records across
four shipped work items hold the 26 owed rows, and no gate re-reads any of them.

What does change is narrower than the claim and worth a sentence: re-running
`round-record close` on one of those ten rounds would now refuse. Nothing does
that, and the records are shipped.

**The `plan.md` exemption is the right call.** Three things make it sound. It is
a row in the survivors table rather than a flag typed once, so it persists —
`skills/verify/scripts/broad_gate.py` passes every `seal/specs/*/survivors.md` as
`--exempt`, and CI's hygiene job does the same. The quote is the anchor, so the
exemption rots loudly the moment the paragraph is edited. And the grounds are
honest about what is being bought: rewriting an approved plan's own text would
falsify the record of what was approved, and the dated note under it carries
what building it found. The neighbouring claim in `phases/phase-1.md` was
corrected instead, which is the right line — that sentence is the build's own
reading of its own measurement, not something a person signed off.

The correction notes are HTML comments, invisible in a rendered view. That is
this repository's established form for exactly this — seven files across five
work items carry `<!-- CORRECTED <date> -->` notes — so it is convention rather
than a choice this branch made.

**§14 and §15 are both satisfied.** `58511d0` carries the code, the five cases,
`docs/review-chain-spec.md`, `skills/code-review/SKILL.md`,
`templates/sdd-round.md` and `agents/warden.md` together, so no message a person
reads changed without a case pinning the new text. Every one of the five new
cases was seen red here by reverting the line it pins.

**The six new units are all reviewed.** `OWED_MARKERS` under finding 7 above;
the five cases under the verdicts they close. The record's `New units` row names
exactly them, and the fix commits create no seventh.

---

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

Carried from the spawn, executed by the orchestrator at `a28bb03` and not
re-run here: four test modules, 282 passed, exit 0;
`survivor-check --range c9912a4..a28bb03 --exempt …` exit 0.

**The broad gate has not come due.** Finding 7 is open and it is a 🟡 in the
tool, so the sealer's spawn waits on the orchestrator's answer to it rather than
on this report.

Probe leavings: the `git clone --no-local` at `5bf88c1`, its `.venv`, one
`test_tmp_*` file and three scratch scripts — all deleted before this report was
written. Nothing was written in the working tree except this file.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | | |

## Paste-ready fixes

**Finding 7** — `skills/code-review/scripts/round_record.py`. Three edits: a
constant beside `OWED_MARKERS`, an arm in `verdict_rows`' loop, and the
refusal's first sentence. Applied and measured in a clone at `5bf88c1`: all six
shapes refuse, the two changed modules stay at 113 passed.

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

The case, and the four prose carriers `58511d0` already edited together —
`docs/review-chain-spec.md` §*A verdict row that commissions nothing*,
`skills/code-review/SKILL.md`, `templates/sdd-round.md` and `agents/warden.md` —
each say the residual is a wrongly chosen marker. Each needs the same one-clause
narrowing: the check reaches the Verdict cell too, and what is left is a
reviewer who writes a closing verdict word on a row that is open.

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

**Finding 8** — `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/survivors.md`,
the comment under `## Round 1's fix pass`. Six rows, and the exempted one is in
the table:

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

**Finding 9** needs no code. If the two-list order is kept, the sentence saying
so belongs in `verdict_rows`' docstring rather than only in `finding_number`'s:
a reader who hits the `bad` refusal has no way to know a second list is waiting.

---

Needs a fix: yes — finding 7

Loses a record or crashes: no

Nothing here loses a record or crashes. Finding 7 is the closest and is round
1's 🔴 1 in the same shape: the record is written and complete, and what is
false in it is the `Pass` box. Findings 8 and 9 are prose and a round trip.
Finding 8 is under `seal/specs/`, so it is a correction rather than a round, and
`Needs a fix` does not count it.

## Proof block

Files opened at `5bf88c1`:

- `skills/code-review/scripts/round_record.py` — the diff in full, plus
  `finding_number`, `verdict_rows`, `fix_table`, `table_body`,
  `inherited_rows`, `earlier_records`, `reach_back`, `close`, `build`'s verdict
  read, the constants block
- `skills/code-review/scripts/chain_check.py` — `CLOSED_WORDS`, `OUT_OF_SCOPE`,
  `HOME_WORDS`, `READER`, `round_records`
- `skills/code-review/scripts/survivor_check.py` — the exemption reader and its
  `--exempt` contract
- `skills/verify/scripts/broad_gate.py` — what the broad gate runs
- `docs/review-chain-spec.md`, `skills/code-review/SKILL.md`,
  `templates/sdd-round.md`, `agents/warden.md` — the diff against `c9912a4`
- `tests/test_a_finding_id_is_a_bare_integer.py`,
  `tests/test_the_fixes_close_the_record.py` — the diff and the helpers around it
- `seal/ledger.md` — row R1 in full, the 10 rewritten rows located
- `seal/specs/1789356180-…/` — `plan.md`, `survivors.md`, `phases/phase-1.md`,
  `changelog.md`, `overview.md`, `rounds/round-1.md`, `rounds/round-1-report.md`
- `.github/workflows/hygiene.yml`, `.github/workflows/test.yml`, `bin/test`,
  `bin/broad-gate`
- the committed corpus: 209 `seal/specs/*/rounds/round-*.md`, read through
  `round_record.table_body`

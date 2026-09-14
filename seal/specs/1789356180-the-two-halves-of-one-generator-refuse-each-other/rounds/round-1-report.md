# Round 1 — 1789356180-the-two-halves-of-one-generator-refuse-each-other

| Field | Value |
|---|---|
| Target SHA | `aaeb5dd` |
| Base | `release/v0.11.4` at `5bae06e` |
| Reviewed | `git diff release/v0.11.4...HEAD` — 24 files, 2144 insertions, 140 deletions |
| Earlier rounds | none |

## What this round did

Reviewed in a `git clone --no-local` at `aaeb5dd`, deleted at the end along
with every probe. Two stages: spec compliance against `spec.md`, `plan.md` and
`questions.md` first, then quality. The five press points the spawn named were
each executed rather than read, and the three reported facts were re-derived
rather than carried.

Nothing under `seal/specs/*/rounds/` is touched by the diff, so the scope fence
holds: the 66 reduced grounds and the 210 empty spans already committed stand
where they were. Confirmed from the diffstat, which carries no `rounds/` path.

---

## The findings, in the order one causes the next

### 🔴 1 — A `#` cell with no digit admits an open finding, and the record then ticks `Pass` over it

`skills/code-review/scripts/round_record.py:2392`

The three-way read admits any `#` cell with no digit anywhere in it, whatever
else the row says. A row is therefore admitted as *commissioning nothing* on
the strength of its `#` cell alone, while the cells that say whether anything
is owed — the severity marker and the verdict — are never consulted.

Executed at `aaeb5dd`, three shapes, one work item each:

| The verdict row the report carried | `new` | The record it wrote | `close` |
|---|---|---|---|
| `\| 🟡 A \| … \| open \| read \|` | exit **0**, silent | `- [x] Pass` | exit 2, and only because the fix table named a finding the table no longer holds |
| `\| \| … \| open \| read \|` (empty `#`) | exit **0**, silent | `- [x] Pass` | same |
| `\| 🔴 A \| … \| open \| executed \|` | exit 1 | `- [x] Pass` | — |

The 🟡 and the empty cell are the serious pair. `new` exits 0, prints nothing
about the row, and writes a record whose `Pass` box is checked while its own
verdict table holds an open finding. Nothing downstream catches it:
`chain_check.open_blocking` reads only rows carrying 🔴.

The 🔴 case is this work item's own title met inside its fix. `new` writes
`- [x] Pass` and its own `run_check` then refuses the record it just wrote:

```
seal/specs/…/rounds/round-1.md:28  `Pass` is checked, and this 🔴 row reads
`open` — a blocking finding that is not fixed, answered or withdrawn: 🔴 A
```

Two halves of one generator, disagreeing about one row. And the message sends
the reader to the **Verdict** column, where nothing is wrong; the cause is the
`#` column, which the message never names.

Before this branch every one of the three was refused at the `#` cell, by a
message that told the reviewer to number the findings 1..N. That guard is what
the change removes.

The build states this direction — `finding_number`'s docstring,
`docs/review-chain-spec.md` §*A verdict row that commissions nothing*, the
ledger fragment's first row — as *a finding no fix table will be asked to
close, and `close` exits 0 over it*. That understates it by one step: the
record does not merely omit the finding, it **asserts `Pass`** over it, and
`Pass` on the last record is what `skills/verify/SKILL.md` reads as the rounds
having settled.

The fix does not need the verdict vocabulary, which cannot serve here — a
confirmation row reads `verified`, which is in no vocabulary and therefore
OPEN, and the build is right that reading it would trade one refusal for
another. It needs the severity marker, which already means exactly this.
Measured over the same corpus: of the 51 no-digit cells, the 26 carrying 🔴 or
🟡 are **all** genuine findings (11 later closed `fixed`, 4 `answered`, 11 still
`open`), and the 25 carrying 🟢, ❓ or no marker are the shapes the documents
describe. The split is exact, and
`test_every_no_digit_shape_the_corpus_holds_is_admitted`'s five parameters
(`A`, `carried`, `✅`, `🟢 fix-surface`, `—`) all stay green.

### 🟡 2 — The corpus cited as grounds for the discriminator says the opposite of what is written

`skills/code-review/scripts/round_record.py:2332` (the `DIGIT_RE` comment) ·
`skills/code-review/scripts/round_record.py:2363` (`finding_number`'s
docstring) · `docs/review-chain-spec.md` §*The finding id*, the `no digit
anywhere in it` table row · `skills/code-review/SKILL.md` §*A row that
commissions nothing takes no id at all* · `templates/sdd-round.md`, the `#`
cell comment

Five places state the same sentence: *a cell carrying none was never an id — it
is `✅`, `carried`, `🟢 fix-surface`, an em dash*, and *the two populations do
not overlap on anything a reviewer writes*.

Re-derived at `aaeb5dd` through the module's own `table_body` and reader, over
the same 207 records:

| Shape of the 51 no-digit `#` cells | How many |
|---|---|
| a severity marker and a single **letter** — `🔴 A` … `🟢 O`, `❓ a` | **44** |
| `carried` | 2 |
| `🟢 fix-surface` | 2 |
| `🟢 fragment`, `🟢 grep`, `🟢 overview` | 3 |
| `✅` | **0** |
| `—` | **0** |

So 44 of the 51 are ids written in letters instead of digits — the cell *was*
reaching for an id and used the wrong alphabet — and the two exemplars the
documents lead with appear nowhere in the population. The evidence actually
behind the rule is 7 rows, not 51.

Why it matters beyond the prose: this sentence is the whole argument that the
direction in finding 1 is cheap. If the corpus's dominant no-digit shape is a
finding id, then the mistake the new rule stops catching is the one reviewers
made 44 times, and the one it now admits silently is not rare.

The claim is stale rather than invented — all 44 rows are from 2026-09-02/03
and `round_record.py` first appears 2026-09-05, so they are hand-written
records from before the generator existed. That is worth saying in the same
place, because it is the honest reading: the shape is not what a reviewer
reaches for *today*, and it is also not what the documents say it is.

The same sentence is in `seal/ledger/1789356180-…md` row 1 and
`phases/phase-1.md`; both are records rather than the tool and are listed as
corrections below.

### 🟡 3 — The suffixed-verdict refusal prints a paste-ready row that is itself refused

`skills/code-review/scripts/round_record.py:2950`

`head` is meant to be the vocabulary word the cell begins with. It is computed
by splitting on the first character of `chain.SEPARATORS` that occurs
*anywhere* in the cell, not on the separator that actually ends the word — and
`SEPARATORS` begins with a space, so any cell containing a space splits there
regardless of what followed the word.

Executed at `aaeb5dd`, a fix table carrying
`| 1 | answered, corrected at 7cc00b1 | x |`:

```
round-record: finding 1's verdict `answered, corrected at 7cc00b1` begins with
`answered,` and then carries more. The Verdict cell holds the word alone and
everything after it goes in `Commit or grounds`: write
`| 1 | answered, | corrected at 7cc00b1 |`. …
```

The row it tells the fixer to write carries `answered,` as the verdict, which
`fix_table` refuses on the next run — so the message costs the round trip it
was added to save. The em-dash spelling the documents name works, because its
separator happens to be the space; the comma spelling does not.

This is the arm phase 2 added precisely so a reader who followed the old spec
would be told what to write. For the comma spelling it tells them wrong.

### 🟡 4 — A `deferred` row whose third cell begins with its home says the home twice

`skills/code-review/scripts/round_record.py:2936`

The guard against repeating the home is exact equality, so it catches
`| N | deferred #12 | #12 |` and misses the shape immediately next to it.

Executed at `aaeb5dd`, a fix table carrying
`| 1 | deferred #309 | #309 — the parity arm is out of scope |`, the shape of
#391's own worked example:

```
#309 — #309 — the parity arm is out of scope; executed
```

The home is printed twice before the reviewer's grounds. #391 is about a
`deferred` row's Grounds cell being unreadable; this leaves a smaller version
of the same noise in the cell the fix exists to repair.

### ⬜ 5 — `close`'s "not in the verdict table" message renders an empty list as `(which has )`

`skills/code-review/scripts/round_record.py:3166`

Observed during the probe for finding 1, where every verdict row was id-less:

```
round-record: the fix table names finding 1, not in round 1's verdict table (which has )
```

The parenthetical is there to tell the fixer which ids the table does hold; on
an empty mapping it renders as nothing and the reader learns less than the
sentence promises. Pre-existing, and unchanged by this branch — but the new
rule is what makes an empty mapping reachable from a well-formed report, so it
is worth a sentence rather than silence.

---

## What I checked and found sound

Each of these was executed, not read.

**The corpus numbers are exact.** Re-derived through `round_record.table_body`
and the unverified reader over the 208 records on disk, 207 of which parse:
1,989 verdict body rows · 199 refused carrying digits · 51 refused carrying
none · 210 rows with an empty code span beside a fix commit · 66 `deferred`
rows whose Grounds cell is its home alone. Every figure matches the build's to
the unit, and the frame's 1,992 / 54 / 103 do not.

Worth recording how: my first pass used a naive `|` split and reproduced the
frame's wrong numbers almost exactly — 1,992 / 54 / 209 — because a pipe inside
a code span splits a row. The loose match is the whole mechanism behind this
release's four wrong measurements, and the build's decision to re-derive
through the module's own reader is what made the difference.

**`verdict_of`'s blast radius is exactly one cell.** Ran both readings —
`5bae06e`'s and `aaeb5dd`'s — over all 1,989 committed verdict rows. One cell
changes: `❓ out of verified scope` in
`1789081272-the-writer-of-the-contract-is-not-its-executor/rounds/round-1.md`,
which is the row #353 is about. `MARKER` is anchored and cannot backtrack
catastrophically: the group requires a leading non-word character, so it either
matches greedily at position 0 or fails there.

**The phase 3 / phase 4 split is honest.** `9d1e324` touches only the Grounds
join, the `deferred` third cell and the code-span cut; `26c7696` touches only
`WRITTEN_CHECKER`, `landing_values`' docstring and `close`'s checker-row block.
Neither commit's code diff carries any of the other's behaviour.

**The rider's replacement is right about the fact it corrects.**
`chain.EMPHASIS` is `` [*_`]+ `` and `fix_table` applies it at the `verdict =`
line, which runs before the home is taken with `.strip(chain.SEPARATORS)` — so
a home written as a code span does already arrive stripped, and the rider's
stated reason did not hold at that site. The comment that replaces it says both
halves and leaves the constant alone for its other two callers, which nothing
here measured either.

**The scope fence holds.** No `seal/specs/*/rounds/round-*.md` appears in the
diff; nothing migrated the 66 reduced grounds or the 210 empty spans.

**The ledger re-stamps are honest.** 14 rows rewritten: 6 carry a
`Re-read 2026-09-14 by work item 1789356180` note naming what drifted, and 8
are hash-only re-stamps whose `Checked` date is unchanged — so no row asserts a
re-read that did not happen. The two corrected claims are true as corrected:
R1's `anything else is refused` became `a cell carrying digits that is not one
is refused`, and S13 lost the word `only` from `re-derives the row to no fixes
to check only where nothing commissioned a fix`, which is what `close` now does.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A no-digit `#` cell admits an open 🔴/🟡 finding and the record ticks `Pass` over it; `new` exits 0 for the 🟡 and the empty cell, and for the 🔴 the generator's own check refuses the record it just wrote, naming the wrong column | `skills/code-review/scripts/round_record.py:2392` | open | executed at `aaeb5dd` — three shapes run end to end through `new` and `close`; `chain_check.open_blocking` reads only 🔴 rows, so nothing catches the other two |
| 2 | The corpus cited as grounds for the discriminator says the opposite: 44 of the 51 no-digit cells are letter-keyed finding ids, and the two exemplars the documents lead with (`✅`, `—`) appear zero times | `skills/code-review/scripts/round_record.py:2332`, `:2363`; `docs/review-chain-spec.md` §*The finding id*; `skills/code-review/SKILL.md` §*A row that commissions nothing takes no id at all*; `templates/sdd-round.md` | open | executed at `aaeb5dd` — re-derived through `table_body` and the unverified reader over the same 207 records the build counted |
| 3 | The suffixed-verdict refusal splits on the first `SEPARATORS` character anywhere in the cell rather than the one ending the word, so `answered, corrected at <sha>` prints the paste-ready row `\| 1 \| answered, \| … \|`, which `fix_table` refuses on the next run | `skills/code-review/scripts/round_record.py:2950` | open | executed at `aaeb5dd` — `close` over that fix table, message read in full |
| 4 | A `deferred` row whose third cell begins with its home prints the home twice, in the cell #391 exists to make readable | `skills/code-review/scripts/round_record.py:2936` | open | executed at `aaeb5dd` — `\| 1 \| deferred #309 \| #309 — the parity arm is out of scope \|` lands as `#309 — #309 — the parity arm is out of scope; executed` |
| 5 | `close`'s "not in the verdict table" refusal renders an empty id list as `(which has )`; pre-existing, but the new rule makes an empty mapping reachable from a well-formed report | `skills/code-review/scripts/round_record.py:3166` | open | executed at `aaeb5dd` — observed while probing finding 1 |
| 6 | `seal/ledger.md` R1's corrected clause states the digits-only refusal of a pattern it says "both the verdict table and the fix table share", but the fix table refuses a no-digit cell too (`idless=False`) — the correction is true of the verdict table and silent about the other half | `seal/ledger.md`, row R1 · a finding id is a bare integer | open | read at `aaeb5dd` against `round_record.py#fix_table`, which passes `False` for `idless` |
| 7 | The corpus numbers are exact — 1,989 / 199 / 51 / 210 / 66 — and the frame's 1,992 / 54 / 103 are what a loose `\|` split yields | `seal/specs/1789356180-…/phases/phase-1.md`, `phases/phase-3.md` | answered | executed at `aaeb5dd`; my own naive split reproduced 1,992 / 54 / 209 before I re-ran it through the module's reader |
| 8 | `verdict_of`'s marker strip changes the reading of exactly one committed cell, and `MARKER` cannot backtrack catastrophically | `skills/code-review/scripts/chain_check.py#MARKER`, `#verdict_of` | answered | executed at `aaeb5dd` — both readings run over all 1,989 rows; the one cell is `1789081272-…/rounds/round-1.md` finding 15 |
| 9 | The phase 3 / phase 4 split is honest: neither commit's code diff carries the other's behaviour | `9d1e324`, `26c7696` | answered | read at `aaeb5dd` — the two commit diffs of `round_record.py`, disjoint by function |
| 10 | The replaced rider's correction is right: `chain.EMPHASIS` runs over the verdict cell before `SEPARATORS` is reached, so a home written as a code span already arrives stripped | `skills/code-review/scripts/round_record.py#fix_table` | answered | read at `aaeb5dd` — the `verdict =` line precedes the `.strip(chain.SEPARATORS)` on the home |
| 11 | The scope fence holds — no committed round record is rewritten | `git diff release/v0.11.4...HEAD` | answered | executed at `aaeb5dd` — the diffstat carries no `rounds/` path |
| 12 | The ledger re-stamps are honest: 6 rows carry a re-read note, 8 are hash-only with `Checked` unchanged, and both corrected claims are true as corrected | `seal/ledger.md` | answered | executed at `aaeb5dd` — word-diff of all 14 rewritten rows, `Checked` column compared before and after |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_tmp_warden_r1.py -q -s` (NAME NOT IN TREE — a probe, deleted) in a clone at `aaeb5dd` — a `🔴 A` open row through `new` and `close`, a comma-suffixed `answered` verdict, a `deferred` row whose third cell begins with its home | findings 1, 3 and 4 reproduced; `new` wrote `- [x] Pass` and exited 1 on its own check |
| `bin/test tests/test_tmp_warden_r2.py -q -s` (NAME NOT IN TREE — a probe, deleted) in the same clone — `🟡 A`, an empty `#` cell and a prose cell through `new` and `close` | 🟡 and empty: `new` exit 0, `- [x] Pass`, silent. Prose carrying a digit (`see round 2`): refused, as intended |
| Corpus re-derivation through `round_record.table_body` and the unverified reader over the 208 committed records | 207 parse; 1,989 verdict rows · 199 refused with digits · 51 without · 210 empty spans · 66 `deferred` grounds equal to the home — every figure matches the build's |
| Both readings of `verdict_of` — `5bae06e`'s and `aaeb5dd`'s — over all 1,989 committed verdict rows | exactly one cell changes, and it is #353's |
| Classification of the 51 no-digit cells by shape and by severity marker | 44 marker + single letter, 7 other; 26 carry 🔴/🟡 and all 26 are genuine findings (11 `fixed`, 4 `answered`, 11 `open`) |
| The full suite, the repository-wide lint, the typecheck | **not yet** — not run in this round. §2 puts the broad gate with the sealer, after the rounds settle. `agents/sealer.md` names its `Broad gate` cell, and nothing in this report writes it |

Carried from the spawn, executed by the orchestrator at `aaeb5dd` and not
re-run here: seven test modules, 417 passed / 1 skipped / exit 0;
`bin/evidence-check --strict .` exit 0; `ruff check skills/ tests/` exit 0.

Probe leavings: the `git clone --no-local` at `aaeb5dd`, its `.venv`, the two
`test_tmp_*` files and one detached worktree created and removed inside the
measurement script — all deleted before this report was written.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | | |

## Corrections — records rather than the tool, and `Needs a fix` does not count them

- **`seal/ledger/1789356180-…md`, row 1, Clause column** and
  **`phases/phase-1.md` §*A row with no id needs no spelling of its own***
  carry the sentence finding 2 is about — *51 carry none and were never an id
  (`✅`, `carried`, `🟢 fix-surface`, `—`)*. The count is right and the reading
  of it is not: 44 of the 51 are letter-keyed ids and neither `✅` nor `—`
  occurs. The fragment's own Notes column is the honest half and should carry
  the split.
- **`seal/ledger.md`, row R1**, as finding 6 above.

## Paste-ready fixes

**Finding 1** — `skills/code-review/scripts/round_record.py`. Two edits: a
constant beside `DIGIT_RE`, and the arm at line 2392.

```python
DIGIT_RE = re.compile(r"\d")
# The two severities that mean somebody owes this row an answer, per
# `skills/code-review/SKILL.md`'s scheme: 🔴 blocks merge, 🟡 needs grounds.
# 🟢, ❓ and ⬜ commission nothing by definition, which is why they are not
# here. A no-digit cell carrying one of these two was an id written in the
# wrong alphabet, not a row that commissions nothing: measured over the same
# 207 records, all 26 such rows are genuine findings -- 11 later closed
# `fixed`, 4 `answered`, 11 still `open` -- and none of the 25 carrying 🟢, ❓
# or no marker is. The verdict word cannot do this job: a confirmation reads
# `verified`, which is in no vocabulary and therefore OPEN.
OWED_MARKERS = ("\N{LARGE RED CIRCLE}", "\N{LARGE YELLOW CIRCLE}")
```

```python
    text = chain.EMPHASIS.sub("", seen).strip()
    m = FINDING_ID_RE.match(text)
    if not m:
        if idless and not DIGIT_RE.search(text):
            if any(marker in text for marker in OWED_MARKERS):
                owed.append((text, line))
            return None
        bad.append((text, line))
        return None
```

`finding_number` takes one more list, `owed`, and `verdict_rows` passes it and
refuses on it:

```python
def verdict_rows(reader, lines):
    out, taken, bad, owed = {}, {}, [], []
    for i, cells in table_body(reader, lines, VERDICTS, VERDICT_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) <= NUMBER_COL:
            raise Refused(f"a verdict row has no `#` cell: {lines[i].strip()!r}")
        number = finding_number(
            RECORD_LABEL, seen[NUMBER_COL], lines[i], taken, bad, True, owed
        )
        if number is not None:
            out[number] = (i, cells)
    refusal = id_refusal(RECORD_LABEL, bad)
    if refusal is not None:
        raise refusal
    if owed:
        many = "s" if len(owed) > 1 else ""
        rows = "\n".join(f"    {text!r}: {line.strip()}" for text, line in owed)
        raise Refused(
            f"the {RECORD_LABEL} has {len(owed)} row{many} whose `#` cell "
            "carries a severity that owes an answer and no finding id. "
            "\N{LARGE RED CIRCLE} blocks merge and \N{LARGE YELLOW CIRCLE} "
            "needs grounds, so both commission a fix-table row — and a row "
            "with no id is never keyed, never asked for a closure and never "
            "counted toward `Pass`, so `Pass` would be ticked over an open "
            "finding. Number it, or write the severity the row actually has "
            "(\N{LARGE GREEN CIRCLE}, \N{BLACK QUESTION MARK ORNAMENT}, "
            f"\N{WHITE LARGE SQUARE}).\nThe row{many}:\n{rows}"
        )
    return out
```

`fix_table` passes `[]` for the new argument, since `idless` is off there and
the arm is unreachable:

```python
        number = finding_number(
            FIX_TABLE_LABEL, seen[0], raw[i], taken, bad, False, []
        )
```

**Finding 2** — `skills/code-review/scripts/round_record.py`, the `DIGIT_RE`
comment. The same correction is owed to `finding_number`'s docstring,
`docs/review-chain-spec.md`, `skills/code-review/SKILL.md` and
`templates/sdd-round.md`, each in its own words.

```python
# What tells a row that names NO finding apart from a row that names one
# badly. A cell carrying a digit was reaching for an id and missed -- `R2-1`,
# `1-1`, `1b` -- and is refused. A cell carrying none is admitted unless its
# severity says otherwise (`OWED_MARKERS` below).
#
# The corpus split is 199 carrying digits to 51 carrying none, and the 51 are
# NOT one population. 44 of them are a severity marker and a single letter --
# `🔴 A` through `🟢 O` -- which is an id written in the wrong alphabet, and
# all 44 predate `round_record.py` (2026-09-02/03 against the generator's
# 2026-09-05). Seven are the shape this rule is for: `carried`, `🟢
# fix-surface`, `🟢 fragment`, `🟢 grep`, `🟢 overview`. Neither `✅` nor a bare
# em dash occurs in a committed record at all -- the 21 bare em dashes are in
# reviewers' REPORTS, which is a different corpus.
DIGIT_RE = re.compile(r"\d")
```

**Finding 3** — `skills/code-review/scripts/round_record.py:2950`. Split on the
separator that ends the word, which the arm's own test already identified:

```python
        elif any(
            word.startswith(w) and word[len(w)] in chain.SEPARATORS
            for w in (FIXED, ANSWERED)
        ):
            # The cell BEGINS with a word this table admits and carries a
            # suffix, which is one cell doing two cells' work.
            # `docs/review-chain-spec.md` prescribed exactly that for a
            # correction — `answered — corrected at <sha>` — for as long as
            # `agents/smith.md` prescribed the two-cell shape beside it, so a
            # reader who followed the spec met a message listing three words
            # and had to work out that their cell had begun with one of them
            # (#341's comment). `deferred <home>` is the one word that
            # legitimately carries a suffix and is handled above.
            #
            # `head` is the word the arm matched on, taken from the arm's own
            # test rather than by splitting the cell: `SEPARATORS` begins with
            # a space, so splitting on the first of its characters found
            # ANYWHERE in the cell gave `answered,` for `answered, corrected
            # at <sha>` -- a paste-ready row this table refuses on the next
            # run.
            head = next(
                w
                for w in (FIXED, ANSWERED)
                if word.startswith(w) and word[len(w)] in chain.SEPARATORS
            )
            raise Refused(
                f"finding {number}'s verdict `{seen[1]}` begins with `{head}` "
                f"and then carries more. The Verdict cell holds the word alone "
                f"and everything after it goes in `{FIXES_HEADER[2]}`: write "
                f"`| {number} | {head} | {verdict[len(head) :].strip(chain.SEPARATORS)} |`. "
                f"Only `{DEFERRED_WORD} <home>` carries its own suffix, because "
                "the home is what makes a deferral readable"
            )
```

**Finding 4** — `skills/code-review/scripts/round_record.py:2936`. Take the
home off the front of the third cell rather than testing the whole of it:

```python
            # The third cell is the fix pass's reasoning — why the finding
            # could not be closed on the branch, what it measured, what a
            # reader should open — and it was discarded whenever the verdict
            # cell carried the home. A deferred finding is the one verdict
            # whose reasoning is the whole of its value, because nothing else
            # in the tree will explain why it left (#391 part 1).
            #
            # The home comes off the FRONT of the note rather than being
            # compared with the whole of it: `| N | deferred #12 | #12 |` and
            # `| N | deferred #12 | #12 — because … |` are the same shape, and
            # an equality test caught only the first, so the second printed
            # `#12 — #12 — because …`.
            note = third[len(home) :].strip(chain.SEPARATORS) if third.startswith(home) else third
            out[number] = (DEFERRED_WORD, home, note)
```

**Finding 5** — `skills/code-review/scripts/round_record.py:3166`. Say so when
the table holds none:

```python
        held = ", ".join(map(str, sorted(rows))) or "no numbered rows at all"
        raise Refused(
            f"the fix table names finding {number}, not in round {args.round}'s "
            f"verdict table (which has {held})"
        )
```

**Finding 6** — `seal/ledger.md`, row R1's Clause cell. Restore the half the
narrowing dropped:

```
R1 · a finding id is a bare integer behind an optional severity marker, read
through one pattern that both the verdict table and the fix table share; a cell
carrying digits that is not one is refused in either table, and a cell carrying
none is refused in the fix table and admitted in the verdict table as a row
that commissions nothing — refused naming the format and quoting the row, and a
genuine duplicate quotes both rows
```

---

Needs a fix: yes — findings 1, 2, 3 and 4

Loses a record or crashes: no

Nothing here loses a record or crashes. Finding 1 is the closest: the record is
written and complete, and what is false in it is the `Pass` box. Findings 3 and
5 are refusal messages a person reads and acts on; finding 4 is a generated
cell. Finding 6 is under `seal/ledger.md` and is a correction rather than a
round, and `Needs a fix` does not count it.

## Proof block

Files opened at `aaeb5dd`:

- `skills/code-review/scripts/round_record.py` — `finding_number`, `id_refusal`,
  `fix_table`, `verdict_rows`, `landing_values`, `build`, `close`, the constants
  block
- `skills/code-review/scripts/chain_check.py` — `verdict_of`, `open_blocking`,
  `closed_with_a_fix`, `MARKER`, `OUT_OF_SCOPE`, `SEPARATORS`, `CLOSED_WORDS`
- `docs/review-chain-spec.md`, `agents/smith.md`, `agents/warden.md`,
  `skills/code-review/SKILL.md`, `skills/implement/SKILL.md`,
  `templates/sdd-round.md` — the diff against `5bae06e`
- `seal/ledger.md` — the 14 rewritten rows, word-diffed; R1 read in full
- `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md`
- `seal/specs/1789356180-…/` — `spec.md`, `plan.md`, `questions.md`,
  `overview.md`, `survivors.md`, `routing.md`, `changelog.md`,
  `phases/phase-1.md` … `phases/phase-4.md`
- `tests/test_a_finding_id_is_a_bare_integer.py`,
  `tests/test_the_fixes_close_the_record.py` — the harness and the new cases
- `CONTRIBUTING.md` — §*Running the checks*
- the committed corpus: 208 `seal/specs/*/rounds/round-*.md`, read through
  `round_record.table_body`

# 1789356180-the-two-halves-of-one-generator-refuse-each-other — review round 1

| Field | Value |
|---|---|
| Target SHA | aaeb5dd |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 394 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | finding_number → 1789356180-the-two-halves-of-one-generator-refuse-each-other.md, phase-1.md, round-1-report.md, round-1.md, fix_table, verdict_rows, pytest |
| New units | OWED_MARKERS (depth 1); test_a_no_digit_cell_whose_severity_owes_an_answer_is_refused (depth 1); test_an_empty_hash_cell_is_refused (depth 1); test_the_row_the_suffixed_refusal_prints_is_a_row_the_table_accepts (depth 1); test_a_deferred_row_whose_third_cell_begins_with_its_home_says_it_once (depth 1); test_the_unknown_finding_refusal_says_so_when_the_table_holds_no_id (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the branch's first review, against the whole diff `release/v0.11.4...aaeb5dd` with nothing inherited. Spec compliance first against the work item's own `spec.md`, `plan.md`, `questions.md`, `overview.md`, four phase records and `survivors.md`, then quality.

The round was given the change cut the way the frame cut it — by the record's COLUMN rather than by ticket — and five places to attack, each because a claim rests on it.

1. **The three-way read of the `#` cell**, because *a cell with no digit anywhere in it* is the whole admission rule. The round was asked what it admits that it should not — a cell that is prose, a cell that is empty, a cell carrying a severity marker and no number, a cell whose digits are inside a word — and whether `Pass` and the fix-table requirement skip exactly the rows intended.
2. **The direction this fails.** The build states it allows more and names the enabled mistake as a reviewer leaving the id off a row that really is an open finding, with nothing catching it. The round was asked to judge whether that is as cheap as claimed.
3. **`verdict_of` stripping a leading severity marker**, which the build says changes the reading of exactly one cell across all 1,989 committed rows, and which `chain_check` reads.
4. **`seal/ledger.md`**, where ten rows drifted and two claims became false and were corrected in place in the shared file.
5. **The scope fence** — records already in the tree are not rewritten, so the 66 reduced grounds and 210 empty spans stay.

Three facts were handed over rather than left to rediscover: that the frame's corpus numbers were wrong in three places and the build re-derived them with the module's own patterns; that phases 3 and 4 were committed together by mistake, reset and split, with phase 4's case seen red again on phase 3's committed tree; and that the rider the build spent states a reason false at its own site. The round was told this release has had four wrong measurements across three work items, every one an aggregate taken from a loose match, and to re-derive anything it relied on.

What the orchestrator had already executed at `aaeb5dd`, handed over so the round would not repeat it: seven modules — `test_a_finding_id_is_a_bare_integer.py`, `test_the_fixes_close_the_record.py`, `test_the_rules_have_one_owner.py`, `test_the_record_is_generated.py`, `test_the_reopening_is_one.py`, `test_chain_check_at_the_pull_request.py`, `test_docs_line_wrap.py` — 417 passed, 1 skipped, exit 0; `bin/evidence-check --strict .` exit 0; `ruff check skills/ tests/` exit 0.

The round was told to number every row of its verdict table while noting that this branch is the one making unnumbered rows legal, so the table is written against the generator as it stands on the branch. The broad gate was withheld by name as the sealer's single act after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A no-digit `#` cell admits an open 🔴/🟡 finding and the record ticks `Pass` over it; `new` exits 0 for the 🟡 and the empty cell, and for the 🔴 the generator's own check refuses the record it just wrote, naming the wrong column | `skills/code-review/scripts/round_record.py:2392` | **fixed** `58511d0` | fixed at 58511d0; executed at `aaeb5dd` — three shapes run end to end through `new` and `close`; `chain_check.open_blocking` reads only 🔴 rows, so nothing catches the other two |
| 2 | The corpus cited as grounds for the discriminator says the opposite: 44 of the 51 no-digit cells are letter-keyed finding ids, and the two exemplars the documents lead with (`✅`, `—`) appear zero times | `skills/code-review/scripts/round_record.py:2332`, `:2363`; `docs/review-chain-spec.md` §*The finding id*; `skills/code-review/SKILL.md` §*A row that commissions nothing takes no id at all*; `templates/sdd-round.md` | **fixed** `58511d0` | fixed at 58511d0; executed at `aaeb5dd` — re-derived through `table_body` and the unverified reader over the same 207 records the build counted |
| 3 | The suffixed-verdict refusal splits on the first `SEPARATORS` character anywhere in the cell rather than the one ending the word, so `answered, corrected at <sha>` prints the paste-ready row `\| 1 \| answered, \| … \|`, which `fix_table` refuses on the next run | `skills/code-review/scripts/round_record.py:2950` | **fixed** `58511d0` | fixed at 58511d0; executed at `aaeb5dd` — `close` over that fix table, message read in full |
| 4 | A `deferred` row whose third cell begins with its home prints the home twice, in the cell #391 exists to make readable | `skills/code-review/scripts/round_record.py:2936` | **fixed** `58511d0` | fixed at 58511d0; executed at `aaeb5dd` — `\| 1 \| deferred #309 \| #309 — the parity arm is out of scope \|` lands as `#309 — #309 — the parity arm is out of scope; executed` |
| 5 | `close`'s "not in the verdict table" refusal renders an empty id list as `(which has )`; pre-existing, but the new rule makes an empty mapping reachable from a well-formed report | `skills/code-review/scripts/round_record.py:3166` | **fixed** `58511d0` | fixed at 58511d0; executed at `aaeb5dd` — observed while probing finding 1 |
| 6 | `seal/ledger.md` R1's corrected clause states the digits-only refusal of a pattern it says "both the verdict table and the fix table share", but the fix table refuses a no-digit cell too (`idless=False`) — the correction is true of the verdict table and silent about the other half | `seal/ledger.md`, row R1 · a finding id is a bare integer | answered | Corrected at 58511d0. Located in `seal/ledger.md`, so a correction rather than a fix to commission: R1's clause now says what each table does and carries the severity rule; read at `aaeb5dd` against `round_record.py#fix_table`, which passes `False` for `idless` |
| 7 | The corpus numbers are exact — 1,989 / 199 / 51 / 210 / 66 — and the frame's 1,992 / 54 / 103 are what a loose `\|` split yields | `seal/specs/1789356180-…/phases/phase-1.md`, `phases/phase-3.md` | answered | executed at `aaeb5dd`; my own naive split reproduced 1,992 / 54 / 209 before I re-ran it through the module's reader |
| 8 | `verdict_of`'s marker strip changes the reading of exactly one committed cell, and `MARKER` cannot backtrack catastrophically | `skills/code-review/scripts/chain_check.py#MARKER`, `#verdict_of` | answered | executed at `aaeb5dd` — both readings run over all 1,989 rows; the one cell is `1789081272-…/rounds/round-1.md` finding 15 |
| 9 | The phase 3 / phase 4 split is honest: neither commit's code diff carries the other's behaviour | `9d1e324`, `26c7696` | answered | read at `aaeb5dd` — the two commit diffs of `round_record.py`, disjoint by function |
| 10 | The replaced rider's correction is right: `chain.EMPHASIS` runs over the verdict cell before `SEPARATORS` is reached, so a home written as a code span already arrives stripped | `skills/code-review/scripts/round_record.py#fix_table` | answered | read at `aaeb5dd` — the `verdict =` line precedes the `.strip(chain.SEPARATORS)` on the home |
| 11 | The scope fence holds — no committed round record is rewritten | `git diff release/v0.11.4...HEAD` | answered | executed at `aaeb5dd` — the diffstat carries no `rounds/` path |
| 12 | The ledger re-stamps are honest: 6 rows carry a re-read note, 8 are hash-only with `Checked` unchanged, and both corrected claims are true as corrected | `seal/ledger.md` | answered | executed at `aaeb5dd` — word-diff of all 14 rewritten rows, `Checked` column compared before and after |

## Paste-ready fixes

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
```python
        number = finding_number(
            FIX_TABLE_LABEL, seen[0], raw[i], taken, bad, False, []
        )
```
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
```python
        held = ", ".join(map(str, sorted(rows))) or "no numbered rows at all"
        raise Refused(
            f"the fix table names finding {number}, not in round {args.round}'s "
            f"verdict table (which has {held})"
        )
```
```
R1 · a finding id is a bare integer behind an optional severity marker, read
through one pattern that both the verdict table and the fix table share; a cell
carrying digits that is not one is refused in either table, and a cell carrying
none is refused in the fix table and admitted in the verdict table as a row
that commissions nothing — refused naming the format and quoting the row, and a
genuine duplicate quotes both rows
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_tmp_warden_r1.py -q -s` (NAME NOT IN TREE — a probe, deleted) in a clone at `aaeb5dd` — a `🔴 A` open row through `new` and `close`, a comma-suffixed `answered` verdict, a `deferred` row whose third cell begins with its home | findings 1, 3 and 4 reproduced; `new` wrote `- [x] Pass` and exited 1 on its own check |
| `bin/test tests/test_tmp_warden_r2.py -q -s` (NAME NOT IN TREE — a probe, deleted) in the same clone — `🟡 A`, an empty `#` cell and a prose cell through `new` and `close` | 🟡 and empty: `new` exit 0, `- [x] Pass`, silent. Prose carrying a digit (`see round 2`): refused, as intended |
| Corpus re-derivation through `round_record.table_body` and the unverified reader over the 208 committed records | 207 parse; 1,989 verdict rows · 199 refused with digits · 51 without · 210 empty spans · 66 `deferred` grounds equal to the home — every figure matches the build's |
| Both readings of `verdict_of` — `5bae06e`'s and `aaeb5dd`'s — over all 1,989 committed verdict rows | exactly one cell changes, and it is #353's |
| Classification of the 51 no-digit cells by shape and by severity marker | 44 marker + single letter, 7 other; 26 carry 🔴/🟡 and all 26 are genuine findings (11 `fixed`, 4 `answered`, 11 `open`) |
| The full suite, the repository-wide lint, the typecheck | **not yet** — not run in this round. §2 puts the broad gate with the sealer, after the rounds settle. `agents/sealer.md` names its `Broad gate` cell, and nothing in this report writes it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain |  |  |

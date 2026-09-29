# 1790635412-an-overflow-cell-is-refused-in-every-repository — review round 3

| Field | Value |
|---|---|
| Target SHA | a719166b1b7433890e7b9f12ba4380366347368f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #659 |
| Broad gate | b183b6e8 against 551c7967; earlier run: 3b76ca2a against 551c7967 |
| Fixes checked by | no fixes to check |
| Fix range | `a719166b1b7433890e7b9f12ba4380366347368f..b690379e0df9915c81a878b14138a3aa5b2fe5f3`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, the new `gfm_lines` docstring says a markdown anchor is shifted and that switching moves every region holding or following one of the characters, and neither is true |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 reopened the run, so this record ends it whatever it finds. Target round 2's fix diff `b5a41796..b934c847` at HEAD `a719166b`, plus the orchestrator's record corrections to `round-1.md` in `b5a41796`. Asked whether each verdict round 2 closed is closed, and whether every sentence of the new `gfm_lines` docstring is true.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The new `gfm_lines` docstring says `ast` and GFM number lines so that the region hashed after a form feed, NEL or U+2028 is not the unit, and that switching moves the hash of every region holding or following one; a markdown anchor is numbered and sliced on the same `splitlines` lines and is not shifted, and a region holding one at a line end or on a blank line keeps its hash | `skills/evidence-check/scripts/evidence_check.py:279` | deferred #664 | #664 — The run is capped: round 2 closed on its one reopening. #664 fixes the `.py` hash side, and that fix rewrites this docstring. The corrected claim (a markdown anchor is not shifted; a character at a line end or on a blank line moves no hash) is added to #664; Executed at `a719166b`: a markdown section after each of the three characters hashed the same on both splitters and read DRIFTED after an edit; a region holding one moved only when it sat mid-line. True for `.py` anchors: `ast` line 2, splitlines line 3, and an edit to the unit passed |
| ⬜ 2 | The same docstring says "in this branch", which names nothing after the squash, and names three of the eight characters before calling them "those characters" | `skills/evidence-check/scripts/evidence_check.py:280` | deferred #664 | #664 — The same docstring's wording ("in this branch", three of the eight characters) is rewritten with it; Read: the `GFM_LINE_RE` comment at line 266 says eight. Wording only; the fix block for 🟡 1 covers it |
| ⬜ 3 | `round-1.md`'s correction grounds its claim on "no tracked file holds such a character", while `round-1-report.md` held one U+2028 and `round-2-report.md` now holds another | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | answered | a record correction in `b690379e`: `round-1.md` no longer says no tracked file holds such a character; Executed: a scan of every tracked file for the eight characters found U+2028 at `round-1-report.md:202` and `round-2-report.md:113`. The conclusion holds because no ledger row anchors into either file. A correction to the run's paperwork |
| ⬜ 4 | `round-2-report.md` says the planted case spells U+2028 as a literal; `NOT_A_LINE_END` spells it `\u2028` | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-2-report.md:113` | answered | a record correction in `b690379e`: the U+2028 in `round-1-report.md` and `round-2-report.md` is written as the `; Read: `tests/test_a_row_wider_than_its_header_is_named.py:294`. `round-2.md` did not copy the line. A correction to the run's paperwork |
| 🟢 | round 2's 🟡 1 finding is closed — the "separate question" sentence is gone and the `.py` mechanism is stated truly | `skills/evidence-check/scripts/evidence_check.py:279` | confirmed | Executed: `ast` and splitlines disagree by one line for all eight characters; an edit to a `.py` unit below a form feed, NEL or U+2028 left the hash unchanged; #664 is open on milestone 0.16.0. The overreach the new text adds is 🟡 1 |
| 🟢 | round 2's ⬜ 2 is closed — both deferrals in `round-1.md` read fixed at `17e8f667` and the "moves every hash" reason is replaced | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | confirmed | Read: the diff of `b5a41796`. The new ground's parenthetical is ⬜ 3 |
| 🟢 | round 2's ⬜ 3 is closed — `round-1.md`'s case carries U+2028 as the escape and parses | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | confirmed | Executed: the fourth fenced block equals the report's with U+2028 replaced by its escape, and it parses; the other three blocks are byte-identical to the report's |
| 🟢 | the fix commit drifted no ledger row | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 0 drifted; no row anchors `gfm_lines` |

## Paste-ready fixes

```python
def gfm_lines(text, keepends=False):
    """TEXT's lines as GFM reads them, the way `str.splitlines` returns them
    otherwise: no trailing empty line, and each line's end kept only when
    KEEPENDS asks.

    For every walk of markdown lines that reads a table or a fence. The
    lines a hash covers and an anchor spans are still `splitlines`', and
    for a `.py` anchor that is a known defect: `ast` numbers lines at LF,
    CR and CRLF alone, so below a line holding one of the eight characters
    `splitlines` also ends a line at, the region hashed is not the unit
    `ast` names, and an edit to that unit can pass without a DRIFTED. A
    markdown or generic anchor is numbered and sliced on the same
    `splitlines` lines, so it is not shifted. #664 fixes the `.py` side;
    switching moves the recorded hash of every `.py` unit that holds or
    follows such a character, and of any region where one sits mid-line,
    so it is a change of its own."""
    lines = GFM_LINE_RE.findall(text)
    return lines if keepends else [line.rstrip("\r\n") for line in lines]
```
```
is false (no ledger row anchors a region that holds or follows such a character)
```
```
planted spells the character as `"\u2028"`, so no code was harmed. The record
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_row_wider_than_its_header_is_named.py` at `a719166b` | exit 0, 38 passed |
| `bin/evidence-check .` at `a719166b` | exit 0; `2662 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow`; records arm 0 refused |
| `bin/correction-check --range 853600fa...a719166b` | exit 0; no merge commit in the range |
| probe file test_tmp_r3.py (deleted), part 1: each of the eight characters on a comment line above `def f`, then `ast.parse` | `ast` put `f` on line 2 for all eight, and for CR and CRLF; `str.splitlines` put it on line 3 for all eight |
| the same probe, part 2: a `.py` unit below a form feed, NEL and U+2028 each, hashed as the checker slices it, then its last line edited | the hash did not move for any of the three; switching the slice to GFM lines moved the recorded hash for all three |
| the same probe, part 3: a markdown `## Sec` after a paragraph holding each character, resolved through `resolve`, then its last line edited | splitlines lines 6 to 9, GFM lines 5 to 8, same content hash on both; the edit moved the hash (DRIFTED) for all three |
| the same probe, part 4: a region holding each character on its own line, at a line end, and mid-line, hashed on both splitters | the hash moved only mid-line |
| the same probe, part 5: `round-1.md`'s fenced Python blocks against the report's | blocks 1 to 3 identical; block 4 equal after the U+2028-to-escape substitution, and it parses |
| a scan of every tracked file for U+2028, U+2029, NEL, VT, FF, FS, GS and RS | two files, each with one U+2028: `round-1-report.md:202`, `round-2-report.md:113` |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet; nobody has run it, and the sealer answers it once the run settles |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1714` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1798` | round 1's ⬜ 2 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1722` | round 1's ⬜ 3 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1609` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2089` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | round 1's 🟢 — confirmed |
| round-1 | `README.md:270` | round 1's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:278` | round 2's 🟡 1 — fixed |
| round-2 | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | round 2's ⬜ 2 — answered |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:274` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md:198` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md:161` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #664's body says GFM numbers a markdown anchor's lines, so the hashed region is shifted after one of the characters; the checker numbers and slices a markdown anchor on the same `splitlines` lines, so only `.py` anchors are shifted, and a markdown case would not go red | #664, by correcting its body | the orchestrator, who opened #664 |

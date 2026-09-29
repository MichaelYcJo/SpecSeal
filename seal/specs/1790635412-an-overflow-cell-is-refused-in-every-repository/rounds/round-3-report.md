# Round 3 report — 1790635412-an-overflow-cell-is-refused-in-every-repository

Reviewer: warden. This is a verifying round and the run's last, since round 2
reopened the run. The target is round 2's fix diff, `b5a41796..b934c847` (one
commit, the `gfm_lines` docstring). The record corrections the orchestrator
made to `rounds/round-1.md` in `b5a41796` are also in scope. The branch was
read at `a719166b` in a `git clone --no-local` of the orchestrator's tree, and
nothing was run in that tree.

Carried from round 2 rather than re-established: the coordinates of the
hash-side splits (`resolve_unit`, `recorded_here`, `file_units`) and the fact
that `py_spans` numbers from `ast`. Every verdict below is re-derived.

## What this round found, in one view

Round 2's three verdicts are closed. The new docstring then says more than is
true, and two record lines carry small false facts.

```
round 2's 🟡 1: "a separate question" is gone, the .py mechanism is stated  (closed)
  └─ the replacement generalises the .py defect to GFM and to "every region" (🟡 1)
       ├─ a markdown anchor is numbered and sliced on the same splitlines
       │  lines, so it is not shifted and an edit to it does drift     (executed)
       └─ a region holding one of the characters at a line end or on a
          blank line keeps its hash when the splitter switches          (executed)
     the same docstring says "in this branch" and names 3 of the 8      (⬜ 2)
round 2's ⬜ 2 and ⬜ 3: round-1.md corrected                             (closed)
  └─ the correction's own ground says no tracked file holds such a
     character; round 1's report did, and round 2's report now does     (⬜ 3)
round 2's report says the planted case spells U+2028 literally; it does not (⬜ 4)
```

## Round 2's verdicts

**🟡 1 is closed for what it named.** The sentence that called the hash side
"a separate question" is gone (`skills/evidence-check/scripts/evidence_check.py:279`).
The new text says the hash side is a known defect, names #664, and states the
`.py` mechanism correctly. Executed: for each of the eight characters on a
comment line above a function, `ast` put the function on line 2 while
`str.splitlines` put it on line 3. For a form feed, NEL and U+2028 each, an
edit to the unit's last line left the splitlines-sliced hash unchanged, which
is the silent pass round 2 measured. Issue #664 is open, on milestone 0.16.0,
and says it is taken by work item C.

**⬜ 2 is closed.** Read against `b5a41796`: both deferral rows in
`round-1.md` now say fixed at `17e8f667`, and the "moves every hash" reason is
replaced with a dated correction naming #664. Its new ground carries a false
parenthetical of its own, which is ⬜ 3 below.

**⬜ 3 is closed.** Executed: `round-1.md` has four fenced Python blocks, and
each is identical to the report's block of the same position except the fourth,
which differs from the report only in spelling U+2028 as the `\u2028` escape.
That fourth block parses. The two that do not parse are indented fragments and
are the same in the report.

**The fix commit drifted nothing.** Executed at `a719166b`: `bin/evidence-check
.` exits 0 with `2662 ok · 0 drifted`, the changed module passes, and
`correction-check` over `853600fa...a719166b` exits 0. No ledger row anchors
`gfm_lines`, so a docstring edit cannot drift one.

## The new docstring says the markdown side is shifted too, and it is not (🟡 1)

The docstring's second paragraph (`evidence_check.py:279`–`286`) says: "`ast`
and GFM number lines at LF, CR and CRLF alone, so after a form feed, NEL or
U+2028 the region hashed is not the unit the row names". Then: "switching
moves the recorded hash of every region that holds or follows one of those
characters".

The first half is true for a `.py` anchor, and for no other kind. Nothing in
the checker numbers a markdown anchor with GFM. `resolve_unit` hands
`heading_path`, `text_regions` and `generic_units` the same `text.splitlines()`
lines that the hash is later sliced from. The numbering and the slicing agree,
so the region is not shifted. Executed: a `## Sec` section after a paragraph
holding a form feed, NEL or U+2028 resolved to lines 6 to 9 on splitlines lines
and 5 to 8 on GFM lines, and the content hashed is the same in both. An edit to
the section's last line reads DRIFTED today.

The second half is false in two ways:

- **A markdown region that follows one does not move.** Executed: for the same
  section, the splitlines hash and the GFM hash are equal for all three
  characters.
- **A region that holds one at a line end or on a blank line does not move.**
  All eight characters are whitespace to `str.isspace`, so `normalise` strips
  them at a line end and drops a line that holds only one. Executed: for the
  form feed, NEL and U+2028, switching moved the hash only when the character
  sat mid-line.

Why it matters: this docstring is the one place in the tree that tells the
author of #664 what their change covers and what it will move. Read as written,
it sends them to plant a markdown case that will not go red, because the
markdown side is not broken in this way. It also tells them to expect DRIFTED
on markdown rows that will not drift. §15 of the agent contract would catch the
first, one round late. #664's own body carries the same GFM sentence, which the
orchestrator can correct there; it is outside the tree and is listed under
*Deferred*.

## The same docstring says "in this branch" and names three of the eight (⬜ 2)

"Still `splitlines`' in this branch" is a docstring sentence that outlives the
branch. After the squash into the release branch it points at nothing. The
docstring also names the form feed, NEL and U+2028 and then says "those
characters", while the comment on `GFM_LINE_RE` six lines above says there are
eight. The fact behind both is right, so this is a wording finding. The fix
block for 🟡 1 covers it.

## round-1.md's correction says no tracked file holds such a character (⬜ 3)

The correction `b5a41796` wrote into `round-1.md`'s 🟡 1 grounds says the
first reason was false "(no tracked file holds such a character)". Executed: at
`a719166b`, `round-1-report.md` holds one U+2028 (line 202) and
`round-2-report.md` holds one (line 113). The first was tracked when the
correction was written. The conclusion the parenthetical supports is still
true, because no ledger row anchors a region in either file, so no hash here
moves. What is false is the ground as stated. This is a correction to the run's
paperwork and is not counted in *Needs a fix*.

## Round 2's report says the planted case spells U+2028 literally (⬜ 4)

`round-2-report.md:113` says the planted case "spells the character as" a
quoted literal U+2028. The planted list
(`tests/test_a_row_wider_than_its_header_is_named.py:294`, `NOT_A_LINE_END`)
spells it as the `\u2028` escape. The report line is also the second tracked
file to hold the character, which is what ⬜ 3 counts. `round-2.md` did not
copy that prose, so the record is right and only the report is wrong. This is a
paperwork correction.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The new `gfm_lines` docstring says `ast` and GFM number lines so that the region hashed after a form feed, NEL or U+2028 is not the unit, and that switching moves the hash of every region holding or following one; a markdown anchor is numbered and sliced on the same `splitlines` lines and is not shifted, and a region holding one at a line end or on a blank line keeps its hash | `skills/evidence-check/scripts/evidence_check.py:279` | open | Executed at `a719166b`: a markdown section after each of the three characters hashed the same on both splitters and read DRIFTED after an edit; a region holding one moved only when it sat mid-line. True for `.py` anchors: `ast` line 2, splitlines line 3, and an edit to the unit passed |
| ⬜ 2 | The same docstring says "in this branch", which names nothing after the squash, and names three of the eight characters before calling them "those characters" | `skills/evidence-check/scripts/evidence_check.py:280` | open | Read: the `GFM_LINE_RE` comment at line 266 says eight. Wording only; the fix block for 🟡 1 covers it |
| ⬜ 3 | `round-1.md`'s correction grounds its claim on "no tracked file holds such a character", while `round-1-report.md` held one U+2028 and `round-2-report.md` now holds another | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | open | Executed: a scan of every tracked file for the eight characters found U+2028 at `round-1-report.md:202` and `round-2-report.md:113`. The conclusion holds because no ledger row anchors into either file. A correction to the run's paperwork |
| ⬜ 4 | `round-2-report.md` says the planted case spells U+2028 as a literal; `NOT_A_LINE_END` spells it `\u2028` | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-2-report.md:113` | open | Read: `tests/test_a_row_wider_than_its_header_is_named.py:294`. `round-2.md` did not copy the line. A correction to the run's paperwork |
| 🟢 | round 2's 🟡 1 finding is closed — the "separate question" sentence is gone and the `.py` mechanism is stated truly | `skills/evidence-check/scripts/evidence_check.py:279` | confirmed | Executed: `ast` and splitlines disagree by one line for all eight characters; an edit to a `.py` unit below a form feed, NEL or U+2028 left the hash unchanged; #664 is open on milestone 0.16.0. The overreach the new text adds is 🟡 1 |
| 🟢 | round 2's ⬜ 2 is closed — both deferrals in `round-1.md` read fixed at `17e8f667` and the "moves every hash" reason is replaced | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | confirmed | Read: the diff of `b5a41796`. The new ground's parenthetical is ⬜ 3 |
| 🟢 | round 2's ⬜ 3 is closed — `round-1.md`'s case carries U+2028 as the escape and parses | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | confirmed | Executed: the fourth fenced block equals the report's with U+2028 replaced by its escape, and it parses; the other three blocks are byte-identical to the report's |
| 🟢 | the fix commit drifted no ledger row | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 0 drifted; no row anchors `gfm_lines` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #664's body says GFM numbers a markdown anchor's lines, so the hashed region is shifted after one of the characters; the checker numbers and slices a markdown anchor on the same `splitlines` lines, so only `.py` anchors are shifted, and a markdown case would not go red | #664, by correcting its body | the orchestrator, who opened #664 |

## Paste-ready fixes

### 🟡 1 and ⬜ 2 — say which anchors are shifted, and what switching moves

In `skills/evidence-check/scripts/evidence_check.py`, the whole of `gfm_lines`:

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

### ⬜ 3 — the parenthetical in round-1.md's correction

In `rounds/round-1.md`, 🟡 1's grounds, replace the parenthetical:

```
is false (no ledger row anchors a region that holds or follows such a character)
```

### ⬜ 4 — round 2's report line

In `rounds/round-2-report.md` line 113, replace the quoted literal with the
escape the case uses:

```
planted spells the character as `"\u2028"`, so no code was harmed. The record
```

## Regression tests to plant

- None for 🟡 1 or ⬜ 2, which are a docstring.
- For #664, in `tests/test_a_row_points_by_content.py`: only the `.py` case
  round 2 described (a form-feed line above a function, a row reverified onto
  it, the function's last line edited, DRIFTED expected). A markdown case of
  the same shape passes at `a719166b` (executed above), so it cannot be seen
  red first.

## Facts for the evidence ledger

- For #664's work item, not this one: a markdown or generic anchor is numbered
  and sliced on the same `splitlines` lines in `resolve_unit`, so the shift is
  `.py`-only; and all eight characters are whitespace to `str.isspace`, so a
  region holding one at a line end keeps its hash when the splitter switches.
  Executed in this round.

Needs a fix: yes — 🟡 1, the new `gfm_lines` docstring says a markdown anchor is shifted and that switching moves every region holding or following one of the characters, and neither is true
Loses a record or crashes: no

The broad gate has not run. This round is the run's last, so 🟡 1 and ⬜ 2
take the filing ladder or a fix commit by the orchestrator's decision. ⬜ 3 and
⬜ 4 are the orchestrator's corrections to the run's paperwork. Once that is
settled, the sealer's spawn comes due.

## Proof block

Files opened in the clone at `a719166b`:
`skills/evidence-check/scripts/evidence_check.py` (260–560, 740–830, and the
fix diff), `tests/test_a_row_wider_than_its_header_is_named.py` (line 294, by
search), this work item's `rounds/round-2.md`, `rounds/round-2-report.md`,
`rounds/round-1.md` and `rounds/round-1-report.md` (the diff of `b5a41796`,
the fenced Python blocks, and the U+2028 lines), and the ledger rows that
mention `gfm_lines` or `GFM_LINE_RE` (by search). Issue #664, read with `gh`.

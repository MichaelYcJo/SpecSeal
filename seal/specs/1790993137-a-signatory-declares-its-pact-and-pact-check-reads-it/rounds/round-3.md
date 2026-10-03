# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — review round 3

| Field | Value |
|---|---|
| Target SHA | f2c542eac16f30ed2ab5b7e415f82811bcc871cf |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 735 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 18 (an autolink row in the `Signatory` table is dropped and `pact-check` exits 0), 🟡 19 (an anchor missing its `/` is graded by nobody, exit 0, which round 1's fix had refused) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 is a verifying round and the run's last, since round 2 closed on fixes and spent the one reopening. It targets `f2c542ea` over round 2's fix range `652275a0..d9602677`. It was asked:
- whether round 2's fixes hold;
- whether the units that fix pass created are correct: the fourteen table-ending ways in `pact_signatories` and `_stops_at`, checked against the GFM spec; `PACT_MENTION_RE`'s one grammar; the Signatory-entry lead-in; `PACT_PRINTED`'s wider reach;
- whether the P8 and P9 corrections hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 18 | `TABLE_BREAK`'s `<` arm ends the table at an autolink row, which GFM reads as a signatory: `pact-check` prints *1 of 1 signatory read* and exits 0 with a second signatory in the rendered table; the thematic break, which ends a GFM table, is refused as a row | `hooks/config.py:831` | open | executed: 21 shapes against cmark-gfm, three silent drops all through the `<` arm; `pact-check` end to end exit 0; removing the `<` arm survives every case |
| 🟡 19 | `PACT_MENTION_RE` passes an anchor whose `/` is missing (no slash, `:` or a space for it, or `@hash` alone), which round 1's net refused: read by nobody, exit 0 | `skills/evidence-check/scripts/pact_check.py:113` | open | executed: four shapes exit 0 at the target and match round 1's pattern; `skills/evidence-check/SKILL.md:465` says exit 2; the grammar is stated only in the account |
| ⬜ 20 | P8's claim says the walk `config_rows` uses, and its note says each branch was seen red; three `TABLE_BREAK` arms survive | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:8` | open | read: the two walks share `unfenced` alone; executed: three arms survived; a correction to the run's paperwork |
| ⬜ 21 | The census comment says the pact's table is walked as `config_rows` walks its own | `tests/test_every_reader_ends_a_line_where_gfm_does.py:663` | open | read: the reason `F` still holds and the comment does not |
| ⬜ 22 | An indented header, delimiter or row is refused in a sentence naming another cause | `hooks/config.py:868` | open | executed against cmark-gfm: GFM reads all three; each refused at exit 2, nothing lost |
| ⬜ 23 | `pact:<name>/` in prose and a documented form with a real heading and `@<hash>` are refused at exit 2 | `skills/evidence-check/scripts/pact_check.py:113` | open | executed: both exit 2; the stated grammar's consequence; the remedy is a fence |
| 🟢 | round 2's finding 12 is closed — a row below a blank line inside the `Signatory` table is refused | `hooks/config.py:837` | confirmed | executed: the blank-line half and the gap half each broken, 4 and 2 cases red; the class has one more way, 🟡 18 |
| 🟢 | round 2's finding 13 is closed — prose, a code span, the placeholder form and a sentence's end naming the pact are exit 0 | `skills/evidence-check/scripts/pact_check.py:113` | confirmed | executed: the lookahead, the placeholder exception and the span skip each broken, every one red; the narrowing reopened part of round 1's finding 4, 🟡 19 |
| 🟢 | round 2's finding 14 is closed — every entry refusal reads after *the pact* | `hooks/config.py:931` | confirmed | executed: the lead-in dropped, red; read: both callers print `the pact {refusal}` |
| 🟢 | round 2's finding 15 is closed — the word case reads the refusals written in `hooks/config.py` | `tests/test_one_word_one_meaning.py:597` | confirmed | executed: *home* planted in the sentence of `_stops_at`, red |
| 🟢 | round 2's finding 16 is closed — P9 cites the three cases it lacked | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:9` | confirmed | read: the three coordinates are in the cell; executed: `evidence-check --strict` exit 0, the fragment 93 ok |
| 🟢 | round 2's finding 17 is closed — round 1's spliced Grounds | `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-1.md:36` | confirmed | read: 🟡 3 mended at `652275a0`; ⬜ 5's text reads as its two commits' range |
| 🟢 | round 1's findings 1, 2, 3 and 5 to 11 stay closed, carried as round 2 confirmed them | `rounds/round-2.md` | confirmed | carried; executed: the five pact modules green at the target; round 2's fix pass rewrote `pact_signatories` (finding 2's unit), and its stray-row cases are green; finding 4 is not carried, 🟡 19 |

## Paste-ready fixes

```python
# A one-cell delimiter row, and the starts of the blocks that break a GFM
# table: a heading, a block quote, an HTML block, a fence, a list item, a
# thematic break.
SIGNATORY_DELIMITER = re.compile(r"^\|\s*:?-+:?\s*\|\s*$")
TABLE_BREAK = re.compile(
    r"^ {0,3}(?:#{1,6}(?:\s|$)|>|`{3,}|~{3,}|[-*+](?:\s|$)|\d{1,9}[.)](?:\s|$)"
    # An HTML block's start, and not an autolink: GFM reads `<https://…>`,
    # or `<` and a space, as one of the table's rows (round 3 of #647).
    r"|<(?:!--|\?|!\[CDATA\[|![A-Za-z]|/?[A-Za-z][A-Za-z0-9-]*(?:[\s/>]|$))"
    # A thematic break, which ends the table as a heading does.
    r"|(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$)"
)
```
```text
      a blank line, a fence,  end the table; a `| … |` line after them and
      an HTML block, a quote,   before the first heading is a signatory the
      a list item, a            walk never reaches, and is refused
        thematic break
      ...
      a line with no pipe     refused: GFM reads it as one of the table's
        (an autolink among      rows, and it should be written as one
        them)
```
```python
    (
        "an autolink row",
        HEAD + f"<{MOBILE}>\n" + CLAUSE,
        f"has a `Signatory` table that continues with `<{MOBILE}>`, a line with "
        "no pipe that GFM reads as one of its rows — write it as `| … |`",
    ),
    ("an HTML block", HEAD + f"<div>\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("an ordered list item", HEAD + f"1. a note\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("a thematic break", HEAD + f"***\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("a thematic break, then a clause", HEAD + "---\n" + CLAUSE, None),
```
```python
# **The grammar, in one rule** (round 2, yellow 13; round 3): a token begins
# an anchor where `pact:<name>` is followed at once by `/` or `#`, or where
# the rest of an anchor follows with its `/` missing -- a quoted heading path
# closed by `@`, or `@` and a hash, at once or after one mark or one space.
# It is refused where it does not go on to parse. Anything else naming the
# pact is a mention and is left alone. The one form that begins an anchor and
# is not an attempt is the one this plugin prints to show the shape, its
# locator opening with a placeholder, `/"<heading path>"`.
PACT_MENTION_RE = re.compile(
    r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>[A-Za-z0-9_.-]+)"
    r"(?:(?=[/#])(?!/\"<)"
    r"|(?=[^\s`|/#]?[ \t]?[\"'“‘][^\n]*?[\"'”’]@)"
    r"|(?=[^\s`|/#]?@[0-9A-Fa-f]))"
    r"[^\s`|]*"
)
```
```python
@pytest.mark.parametrize(
    "shape",
    [
        "pact:orders-api{loc}@{h}",
        "pact:orders-api:{loc}@{h}",
        "pact:orders-api {loc}@{h}",
        "pact:orders-api@{h}",
    ],
    ids=["no slash", "a colon for the slash", "a space for the slash", "no heading path"],
)
def test_an_anchor_missing_its_slash_is_refused(world, shape):
    """An anchor whose `/` went missing is still an attempt, and the shipped
    section says one that does not parse is exit 2 (round 3 of #647)."""
    anchor = shape.format(loc=LOCATOR, h=clause(V2))
    write(world["web"], "seal/ledger/1790000000-x.md", ledger_row(anchor))
    code, out = run(world)
    assert code == 2, out
    assert "does not parse" in out, out
```
```markdown
`pact_signatories` reads a pact's `\| Signatory \|` table through `unfenced`, as `config_rows` does, so a table in a comment or a fence is not the table, and ends it where GFM ends a table;
```
```python
        # The pact's `Signatory` table, read through `unfenced` as
        # `config_rows` reads its own (#647).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on five modules: `test_pact_check`, `test_a_signatory_declares_its_pact`, `test_one_word_one_meaning`, `test_a_signatorys_ci_prints_its_pact`, `test_a_pact_anchor_is_no_coordinate_of_the_signatory` | 114 passed, exit 0, with the fixes below applied in the clone; the same modules at the target are green (each mutation run's baseline) |
| `bin/evidence-check --strict .` at the target | exit 0; the work item's fragment 93 ok; records arm 0 refused |
| `bin/mutation-check`, eleven breaks one at a time over the fix pass's units (the tables above) | eight red; three `TABLE_BREAK` arms SURVIVED (`<`, the fences, the ordered list) |
| 21 table shapes through `pact_signatories` and through cmark-gfm, cells compared | three silent drops (autolink, scp-style autolink, `<` and a space); thematic breaks refused where GFM ends the table; the indented shapes refused where GFM reads them |
| `pact-check` over a pact listing an autolink row (🟡 18) | *1 of 1 signatory read*, exit 0 |
| `pact-check` over a pact with `***`, `---`, `___` under the last row | exit 2, *continues with … a line with no pipe that GFM reads as one of its rows* |
| `pact-check` and the signatory's `evidence-check` over four missing-slash shapes (🟡 19) | `pact-check` exit 0 with 0 anchors; `evidence-check` 0 malformed; `#` for `/` refused by both |
| Round 1's net (`652275a0`) over the missing-slash shapes | all three tested shapes match, so each was refused before round 2's fix |
| The paste-ready fixes for 🟡 18 and 🟡 19 applied in the clone, with the proposed cases; then the code reverted and the cases kept | 114 passed with the fixes; 7 of the proposed ids red without them; the 21-shape comparison shows no silent drop with the fix |
| The full suite, the repository-wide lint and the typecheck | not yet — not run in this round; the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/pact_check.py:240` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/config.py:820` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2930` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:437` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/config.py:799` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/releases/0.15.4.md:54` | round 1's ⬜ 6 — answered |
| round-1 | `seal/releases/0.5.0.md:212` | round 1's ⬜ 7 — answered |
| round-1 | `skills/evidence-check/scripts/pact_check.py:393` | round 1's ⬜ 8 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:387` | round 1's ⬜ 9 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:195` | round 1's ⬜ 10 — answered |
| round-1 | `tests/test_one_word_one_meaning.py:565` | round 1's ⬜ 11 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1658` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:295` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py:4514` | round 1's 🟢 — confirmed |
| round-1 | `skills/implement/scripts/seal.py:284` | round 1's 🟢 — confirmed |
| round-1 | `skills/config/SKILL.md:31` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-pact.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.13.1.md:65` | round 1's 🟢 — confirmed |
| round-2 | `hooks/config.py:851` | round 2's 🟡 12 — fixed |
| round-2 | `skills/evidence-check/scripts/pact_check.py:104` | round 2's 🟡 13 — fixed |
| round-2 | `hooks/config.py:856` | round 2's ⬜ 14 — fixed |
| round-2 | `tests/test_one_word_one_meaning.py:588` | round 2's ⬜ 15 — fixed |
| round-2 | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:9` | round 2's ⬜ 16 — answered |
| round-2 | `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-1.md:36` | round 2's ⬜ 17 — answered |
| round-2 | `skills/evidence-check/scripts/pact_check.py:254` | round 2's 🟢 — verified |
| round-2 | `hooks/config.py:849` | round 2's 🟢 — verified |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2940` | round 2's 🟢 — verified |
| round-2 | `skills/evidence-check/scripts/pact_check.py:476` | round 2's 🟢 — verified |
| round-2 | `tests/test_pact_check.py:446` | round 2's 🟢 — verified |
| round-2 | `skills/evidence-check/scripts/pact_check.py:402` | round 2's 🟢 — verified |
| round-2 | `tests/test_one_word_one_meaning.py:581` | round 2's 🟢 — verified |
| round-2 | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:5` | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

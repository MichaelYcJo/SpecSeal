# Round 3 report — #647 steps A and B (PR #735), verifying round 2's fixes

| Field | Value |
|---|---|
| Round | 3 (verifying, the run's last) |
| Target SHA | f2c542ea |
| Fix range read | `652275a0..d9602677`, then the close commit `f2c542ea` |
| Ran by | specseal:warden on claude-opus-5-5 |

The round ran in a scratch clone (`git clone --no-local`) checked out at the
target, under the session scratchpad. Nothing in the worktree was written but
this file. Every break and every proposed fix was applied in the clone only,
and the clone was restored after each; the clone, the probe files and their
outputs were removed before hand-over.

## What this round was asked, and how the account was read

The target is round 2's fix diff, not the branch. The account is the prompt,
`rounds/round-2.md`, `rounds/round-2-report.md`, the five fix commits'
messages, and the corrected P8 and P9 rows. Each claim was checked against the
code at `f2c542ea`, and the two new surfaces were judged as code.

- **Claimed** (commit `5b45e4c4`, P8's note, the docstring of
  `pact_signatories`): every way a GFM table ends or breaks is read as GFM
  reads it, or refused, so no signatory is dropped while the table reads as
  complete. **Found**: not true for a row written as an autolink, which GFM
  reads as a signatory and the reader drops at exit 0 (🟡 18, executed against
  cmark-gfm, the renderer library GFM is defined by). The list also leaves out
  the thematic break.
- **Claimed** (P8's note): "one case per way, each branch seen red by
  `mutation-check`". **Found**: three arms of `TABLE_BREAK` survive their · NAME NOT IN TREE
  removal: the `<` arm, the two fence arms, and the ordered-list arm (executed).
  The `<` arm is the one that carries 🟡 18.
- **Claimed** (commit `7090a9f4`, P9's note, the comment above
  `PACT_MENTION_RE`): one stated grammar decides, and "the three malformed
  shapes are still refused". **Found**: the three shapes are refused. But the
  grammar now passes an anchor whose `/` is missing, which round 1's fix
  refused and which `skills/evidence-check/SKILL.md:465` says is exit 2. The
  grammar is stated only in the account: the code comment, the commit and
  P9's note. No policy document carries it (🟡 19, executed).
- **Claimed** (P8 and P9 re-stamped in `d9602677`). **Found**: true.
  `evidence-check --strict` reads the fragment at 93 ok and exits 0. P8's
  claim cell was not corrected for the new walk (⬜ 20).

## Round 2's findings at their fix commits

Each fix was broken once in the clone with `bin/mutation-check`, one at a
time, and the cases were run. Each went red.

| Round 2 finding | Fix | Broken how | Cases red |
|---|---|---|---|
| 🟡 12 | `5b45e4c4` | a blank line no longer ends the table | 4, among them `a blank line, then a row` |
| 🟡 12 | `5b45e4c4` | a gap in the line numbers no longer ends the table | 2: the fence and the HTML comment cases |
| 🟡 13 | `7090a9f4` | the `(?=[/#])` lookahead dropped | 2: the prose and code-span cases |
| 🟡 13 | `7090a9f4` | the placeholder exception dropped | 1 |
| 🟡 13 | `7090a9f4` | the graded-span skip back to the start alone | 1: the name-inside-a-heading case |
| ⬜ 14 | `64c5704c` | the entry lead-in dropped | red |
| ⬜ 15 | `8705cdd4` | *home* planted in the sentence of `_stops_at` | the word case red |

### 🟡 12 holds for a blank line, and the class has one more way (🟡 18)

`hooks/config.py:837`. A row below a blank line is refused in its own
sentence, and both halves of the end rule (a blank line, a gap) are watched.
The walk was rewritten whole, so round 1's 🟡 2 was re-run too. The stray-row
cases are green.

### 🟡 13 holds for the prose it named, and the narrowing reopened part of round 1's 🟡 4 (🟡 19)

`skills/evidence-check/scripts/pact_check.py:113`. Prose, a code span, the
placeholder form and a sentence's end are each exit 0, and `#` for `/` is
still refused.

### ⬜ 14, ⬜ 15, ⬜ 16 and ⬜ 17 hold

- ⬜ 14: both callers print `the pact {refusal}` (`pact_check.py:405`,
  `chain_check.py:4092`), and each entry sentence now reads after
  *has a `Signatory` entry that will not read:*. Four sentences are pinned whole.
- ⬜ 15: `PACT_PRINTED` reads `pact_declaration`, `remote_entries`,
  `pact_signatories` and `_stops_at`. The case finds each by name with `next`,
  so a misspelt unit fails it and is never skipped.
- ⬜ 16: P9's Code grounds cite the two config and anchor-file `UNREADABLE`
  cases and the pact-side stray case.
- ⬜ 17: `round-1.md`'s 🟡 3 Grounds read *fixed at bf035a2f, ledger notes
  at `f299c650`*. ⬜ 5's *fixed at 1e1bb977 — `62726cb9`* reads as the range
  of its two commits.

## Findings from execution

### 🟡 18 — A signatory written as an autolink is dropped, and `pact-check` exits 0

`hooks/config.py:831` (`TABLE_BREAK`, a unit round 2's fix pass created). The · NAME NOT IN TREE
`<` arm reads any line that starts with `<` as an HTML block. So it ends the
table there and reads nothing more. But GFM starts an HTML block only for a
few shapes. An autolink, `<https://…>`, or a `<` and a space, is a body row
of the table under GFM.

Executed, as two comparisons. First, 21 table shapes were run through
`pact_signatories` and through cmark-gfm (the `cmarkgfm` binding), and their
cells were compared:

| Shape after the last row | GFM's cells | The reader | Refused |
|---|---|---|---|
| `<https://example.com/org/orders-mobile>` | both signatories | the first only | nothing |
| `<git@example.com:org/orders-mobile.git>` | both | the first only | nothing |
| `< https://example.com/org/orders-mobile` | both | the first only | nothing |
| `***`, `---`, `___` | the first; the table ends | the first | *continues with `***`, a line with no pipe that GFM reads as one of its rows* |

Second, through `pact-check` itself: a pact whose table lists the signatory and
then `<https://example.com/org/orders-mobile>` prints *1 of 1 signatory read*
and exits 0. `chain-check`'s count reads the same function, so it says
*lists 1 signatory*.

Why it matters: this is the silence 🟡 2 and 🟡 12 were opened for, reached
by a third line, and in the unit whose docstring promises it cannot happen.
An autolink is an ordinary way to write a URL in markdown, and the rendered
pact shows the person a two-row table. A signatory nobody checks keeps citing
clauses, and nothing tells anyone.

The thematic break is the other direction of the same list. GFM ends the
table there, but the reader refuses it, and the sentence says the opposite of
what GFM does. Its advice, `| --- |`, is then refused as *a delimiter row out
of place*. That half is refused at exit 2 and loses nothing. It goes in this
finding because it is fixed in the same pattern.

The fix narrows `<` to the starts of an HTML block. An autolink then falls
through to the no-pipe refusal, which is accurate for it. The fix also adds
the thematic break. With the fix applied in the clone, the 21-shape comparison
shows no silent drop, and the five pact modules pass (114 cases). Three of the
five proposed cases fail against the target. The other two, `an HTML block`
and `an ordered list item`, pass against the target, and they are the cases
that watch the two arms that survived their removal.

`Loses a record or crashes`: no. A signatory unread is not a record leaving
the root.

### 🟡 19 — An anchor whose `/` went missing is graded by nobody, as round 1's 🟡 4 was

`skills/evidence-check/scripts/pact_check.py:113` (`PACT_MENTION_RE`). The
grammar refuses a token only where `pact:<name>` is followed at once by `/`
or `#`. An anchor with every other part in place and no `/` is therefore a
mention, and the line is read by nobody.

Executed, each written as the only pact anchor of a signatory's ledger row:

| Text | `pact-check` | The signatory's own `evidence-check` |
|---|---|---|
| `pact:orders-api"## Order response shape / ### Fields"@<the clause's hash>` | exit 0, *0 pact anchors* | 0 malformed |
| the same with `:` for `/` | exit 0 | 0 malformed |
| the same with a space for `/` | exit 0 | 0 malformed |
| `pact:orders-api@<the clause's hash>` | exit 0 | 0 malformed |
| `pact:orders-api#…` (control) | exit 2, refused | 1 malformed |

At `652275a0` the net was `pact:<name>\S*`, and each of the first four
matched it and was refused (executed against that pattern). So round 2's fix
moved them from refused to silent. That is round 1's 🟡 4, *a pact anchor that
does not parse is graded by nobody, and `pact-check` exits 0*, for the most
likely typo. `skills/evidence-check/SKILL.md:465` says `pact-check` exits 2
for "an anchor naming the pact that does not parse". The grammar that
excludes these shapes exists only in the code comment, the commit message
and P9's note. That is the account, not a policy.

Why it matters: the signatory believes it cites a clause. When the clause
changes, no report names the citation, which is the one job `pact-check` has.

The fix keeps the `/`-or-`#` rule and the placeholder exception. It adds the
missing-slash shapes: a quoted heading path closed by `@`, or `@` and a hash,
at once or after one mark or one space. Every round-2 prose shape stays exit
0. With the fix applied in the clone, the five pact modules pass (114 cases),
and the proposed case's four ids are red against the target.

## Findings from reading

### ⬜ 20 — P8's claim still says the walk `config_rows` uses, and its note overstates what was seen red (paperwork)

`seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:8`.
The claim cell says `pact_signatories` reads the table "through the walk
`config_rows` uses", and the Notes say "it is the same walk". After
`5b45e4c4` the two share `unfenced` and nothing else. The new walk has a
delimiter-adjacency rule, a gap rule, a `TABLE_BREAK` list and its own · NAME NOT IN TREE
refusals, so the claim was made false and was not corrected in place. The
round-2 note says "the 14 ways ... one case per way, each branch seen red by
`mutation-check`". But `TABLE_ENDS` holds 16 cases, and three arms of
`TABLE_BREAK` survived their removal here (executed). This is a correction to · NAME NOT IN TREE
the run's paperwork, not counted in `Needs a fix`.

### ⬜ 21 — The census comment repeats P8's stale sentence

`tests/test_every_reader_ends_a_line_where_gfm_does.py:663`. *The pact's
`Signatory` table, walked as `config_rows` walks its own.* The census reason
`F` still applies, because it is about where a line ends. The comment does not.

### ⬜ 22 — An indented header, delimiter or row is refused for the wrong cause

`hooks/config.py:868`. `SIGNATORY_HEADER`, `SIGNATORY_ROW` and · NAME NOT IN TREE
`SIGNATORY_DELIMITER` all anchor at `^\|`. Executed against cmark-gfm: GFM · NAME NOT IN TREE
reads one to three leading spaces (and a leading tab, on a row) on each of
them, and the reader refuses each in a sentence that names another cause.
An indented header gets *holds no `| Signatory |` table*. An indented
delimiter gets *a delimiter row of 1 cells, so GFM renders no table there*.
An indented row gets *not a one-cell row written `| … |`*. Each is refused at
exit 2 and loses nothing, which the docstring's *read, or refused* allows. Only
the sentences are wrong.

### ⬜ 23 — `pact:<name>/` in prose, and a documented form with a real heading, are refused

`skills/evidence-check/scripts/pact_check.py:113`. Executed: *The clauses sit
under pact:orders-api/ in that repository.* and
*Cite as pact:orders-api/"## Clause"@<hash>.* in a signatory's `spec.md` each
exit 2. Both follow from the stated grammar (a `/` begins an anchor), and the
placeholder exception covers only a heading that begins `<`. The remedy is a
fence. This is recorded as the edge of the grammar 🟡 19 extends, and nothing
here asks for it to change.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 18 | `TABLE_BREAK`'s `<` arm ends the table at an autolink row, which GFM reads as a signatory: `pact-check` prints *1 of 1 signatory read* and exits 0 with a second signatory in the rendered table; the thematic break, which ends a GFM table, is refused as a row | `hooks/config.py:831` | open | executed: 21 shapes against cmark-gfm, three silent drops all through the `<` arm; `pact-check` end to end exit 0; removing the `<` arm survives every case | · NAME NOT IN TREE
| 🟡 19 | `PACT_MENTION_RE` passes an anchor whose `/` is missing (no slash, `:` or a space for it, or `@hash` alone), which round 1's net refused: read by nobody, exit 0 | `skills/evidence-check/scripts/pact_check.py:113` | open | executed: four shapes exit 0 at the target and match round 1's pattern; `skills/evidence-check/SKILL.md:465` says exit 2; the grammar is stated only in the account |
| ⬜ 20 | P8's claim says the walk `config_rows` uses, and its note says each branch was seen red; three `TABLE_BREAK` arms survive | `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md:8` | open | read: the two walks share `unfenced` alone; executed: three arms survived; a correction to the run's paperwork | · NAME NOT IN TREE
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

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on five modules: `test_pact_check`, `test_a_signatory_declares_its_pact`, `test_one_word_one_meaning`, `test_a_signatorys_ci_prints_its_pact`, `test_a_pact_anchor_is_no_coordinate_of_the_signatory` | 114 passed, exit 0, with the fixes below applied in the clone; the same modules at the target are green (each mutation run's baseline) |
| `bin/evidence-check --strict .` at the target | exit 0; the work item's fragment 93 ok; records arm 0 refused |
| `bin/mutation-check`, eleven breaks one at a time over the fix pass's units (the tables above) | eight red; three `TABLE_BREAK` arms SURVIVED (`<`, the fences, the ordered list) | · NAME NOT IN TREE
| 21 table shapes through `pact_signatories` and through cmark-gfm, cells compared | three silent drops (autolink, scp-style autolink, `<` and a space); thematic breaks refused where GFM ends the table; the indented shapes refused where GFM reads them |
| `pact-check` over a pact listing an autolink row (🟡 18) | *1 of 1 signatory read*, exit 0 |
| `pact-check` over a pact with `***`, `---`, `___` under the last row | exit 2, *continues with … a line with no pipe that GFM reads as one of its rows* |
| `pact-check` and the signatory's `evidence-check` over four missing-slash shapes (🟡 19) | `pact-check` exit 0 with 0 anchors; `evidence-check` 0 malformed; `#` for `/` refused by both |
| Round 1's net (`652275a0`) over the missing-slash shapes | all three tested shapes match, so each was refused before round 2's fix |
| The paste-ready fixes for 🟡 18 and 🟡 19 applied in the clone, with the proposed cases; then the code reverted and the cases kept | 114 passed with the fixes; 7 of the proposed ids red without them; the 21-shape comparison shows no silent drop with the fix |
| The full suite, the repository-wide lint and the typecheck | not yet — not run in this round; the sealer's, once the rounds settle |

## Paste-ready fixes

### 🟡 18

`hooks/config.py`, the constant and its comment:

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

The docstring of `pact_signatories`, two lines of its table:

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

`tests/test_a_signatory_declares_its_pact.py`, in `TABLE_ENDS` after
`the end of the file`:

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

### 🟡 19

`skills/evidence-check/scripts/pact_check.py`, the constant, with the last
paragraph of its comment:

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

`tests/test_pact_check.py`, at the end:

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

### ⬜ 20 and ⬜ 21

P8's claim cell, the first clause corrected in place under a dated
`Corrected` note, and the census comment:

```markdown
`pact_signatories` reads a pact's `\| Signatory \|` table through `unfenced`, as `config_rows` does, so a table in a comment or a fence is not the table, and ends it where GFM ends a table;
```

```python
        # The pact's `Signatory` table, read through `unfenced` as
        # `config_rows` reads its own (#647).
```

## Regression tests to plant

Each proposed case was run red against the target with the code reverted,
except the two that watch arms that already exist and survived their removal.

| Finding | Destination | Case |
|---|---|---|
| 🟡 18 | `tests/test_a_signatory_declares_its_pact.py` | five more `TABLE_ENDS` entries: an autolink row refused (red), an HTML block and an ordered list item (watch two surviving arms), a thematic break before a row refused and before a clause read clean (red) |
| 🟡 19 | `tests/test_pact_check.py` | an anchor missing its slash, four shapes, exit 2 and *does not parse* (four ids red) — the case is the second fence under 🟡 19 above |

## Facts for the evidence ledger

| Claim | Where it is grounded | How it was established |
|---|---|---|
| GFM reads a line starting `<` that is not an HTML block start (an autolink, `<` and a space) as a body row of the table above it, and ends the table at a thematic break | the `cmarkgfm` binding of cmark-gfm | executed, 21 shapes |

This belongs in P8's note when 🟡 18 is fixed.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 18 (an autolink row in the `Signatory` table is dropped and `pact-check` exits 0), 🟡 19 (an anchor missing its `/` is graded by nobody, exit 0, which round 1's fix had refused)
Loses a record or crashes: no

The run is capped, so this round's open findings go where the orchestrator
sends them. Nothing here was softened for that. The broad gate has not come
due on this round's answer, and its state is `not yet`: no full-suite run has
happened on this branch.

## Proof block

Files opened in this round, at `f2c542ea`: `rounds/round-1.md`,
`rounds/round-2.md`, `rounds/round-2-report.md`; the diff
`652275a0..d9602677` over `hooks/config.py`,
`skills/evidence-check/scripts/pact_check.py`, `tests/` and `seal/ledger/`;
the messages of `5b45e4c4` and `7090a9f4`; `hooks/config.py`
(`CELL`, `CONFIG_SEPARATOR`, the head of `unfenced`'s docstring,
`config_rows`' docstring, `normalise_remote`'s docstring, `remote_entries`,
`pact_declaration`'s tail, `declared_pacts`, `SIGNATORY_HEADER` through
`_stops_at`); `skills/evidence-check/scripts/pact_check.py` (`PACT_MENTION_RE`,
the refusal print, the anchor and near-miss loops, the summary);
`skills/evidence-check/scripts/evidence_check.py` (`PACT_NAME`,
`PACT_ANCHOR_RE`, `blank_pact_anchors`);
`skills/code-review/scripts/chain_check.py` (the pact table print);
`tests/test_pact_check.py` (fixtures and the round-2 cases);
`tests/test_a_signatory_declares_its_pact.py` (the round-2 cases);
`tests/test_one_word_one_meaning.py` (the pact case);
`tests/test_every_reader_ends_a_line_where_gfm_does.py` (the census rows);
`templates/pact.md`; `skills/evidence-check/SKILL.md` (§*pact-check*);
`spec.md` item 9; `skills/verify/scripts/mutation_check.py` (its docstring);
`bin/test`; the P8 and P9 rows of the fragment in full.

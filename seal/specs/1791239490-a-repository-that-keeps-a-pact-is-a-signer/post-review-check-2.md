# Post-review check 2 — 1791239490-a-repository-that-keeps-a-pact-is-a-signer

| Field | Value |
|---|---|
| What this is | a narrow verifying pass over the second post-review fix of #830, not a round; the run is capped at round 3, and this pass ends the post-review loop |
| Target SHA | ae5dec8a |
| Range checked | f1722cec..ae5dec8a: ae5dec8a alone (the fix, `#830`) |
| Base | `origin/release/v0.19.0` at e6d5a055 |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at ae5dec8a, with f1722cec's `hooks/config.py` and sweep module swapped in for the before runs, under `<scratchpad>/<id>/post-review-2/`; all of it removed at hand-over |
| git | 2.50.1 |

## Summary

All four claims hold in the shapes the first check named. Three shapes beside
them are open, and one record states more than the code does:

- **The first check's ⬜ 1 is closed for the four plants it named.** All four
  are green at f1722cec and red at ae5dec8a. The span still ends only at a
  blank line, an ATX heading or a fold marker. A block that starts right
  under the statement with no blank line stays exempt (⬜ 1). One such shape
  was red at f1722cec and is green now.
- **The first check's ⬜ 2 is closed, and no case pins it.** With the filter
  moved back into the branch, all six pact modules stay green (⬜ 2).
- **The first check's ⬜ 3 is closed.** The new sentence is printed for a
  pact and for a review record, end to end. The rows under a glued header
  are read, as the sentence now allows. The sentence contradicts neither
  `docs/the-pact.md` nor the changelog fragment. It quotes the old header
  in its spaced form, not as the line is written (⬜ 3).
- **The first check's ⬜ 4 is closed.** R1 and R6 gained text, and the four
  re-stamped rows read 432 ok. Each of the two rows now claims one shape
  more than the code gives (⬜ 4).

Nothing else moved. The range touches four files, and they are the four the
commit names. No other ledger row cites a unit whose hash moved.

All four findings are ⬜. None ships a defect. Every shape still exits 2.
⬜ 1 and ⬜ 2 are gaps in a test, ⬜ 3 is a quoted string, and ⬜ 4 is the
run's paperwork.

## What the account claimed, and what was found

- **Claimed for ⬜ 1:** `without_the_policy_span` takes the text as written
  and cuts it before flattening, both callers pass raw text, and four plants
  now go red. Read: both callers pass the file as written. The first caller
  now reads `docs/the-pact.md` itself instead of using the text
  `pact_texts()` handed it. That changes nothing, because the handed text is
  the same file with its whitespace collapsed. Executed: the four plants are
  green with f1722cec's module and red at ae5dec8a, in both sweep cases. The
  docstring's "whatever follows it" does not hold, as ⬜ 1 explains.
- **Claimed for ⬜ 2:** the filter runs whenever an old header is held, so a
  glued header with a separate old table below is named once. Executed, and
  true. In the first check's exact shape (glued header, blank line, whole
  old table) there is one refusal, the stray-row one, and no entry refusal.
  The case the commit planted for it does not reach that shape, as ⬜ 2
  explains.
- **Claimed for ⬜ 3:** a glued header gets its own sentence, rows under it
  with no delimiter row are read as signers, and the S4 case pins this and
  was seen red against 00b5a549's reader. Executed, and true. The S4 case
  fails with f1722cec's `hooks/config.py`, which is 00b5a549's. Through
  `pact-check` the new sentence is printed after "the pact " and after "the
  record ". A glued header with one or two rows under it reads `1 of 2` and
  `1 of 3 signers read` at exit 2. In a review record the row under the
  glued header is read and takes its change.
- **Claimed for ⬜ 4:** R1 and R6 gained claim, grounds and notes text, and
  P8, P11, R1 and R6 were re-stamped. Read: the word diff shows exactly
  those four rows. P8 and P11 changed only hashes. Executed:
  `bin/evidence-check --ledger` on the fragment reads 432 ok, 0 drifted.

## The new sentence against the policy and the changelog

The new sentence is "holds a `| Signatory |` line inside its `| Signer |`
table, the word before 0.19.0, which GFM reads as one of that table's rows —
delete the line". `docs/the-pact.md` (the statement under the
`1791239490` fold marker) and the changelog fragment both say that an old
header *beside* the new table is refused, because its rows would otherwise go
unread. Their remedy is to move the rows into the new table and delete the old
one.

A glued header is not beside the table but inside it, and neither text
describes that shape. That was already so at 00b5a549, where the same shape
printed the "beside" sentence. Nothing contradicts the new sentence. Deleting
the line is the same act as the documents' remedy, minus the move, because
GFM has already moved the rows. This is not a finding.

## Findings from execution

### ⬜ 1 — a block that starts under the statement without a blank line is still exempt

`tests/test_one_word_one_meaning.py:737`. The span ends at a blank line, an
ATX heading or a fold marker. In GFM several other blocks can also begin
directly under a paragraph's last line, and each one ends the paragraph.
Plants placed directly under the statement's `Enforced by:` line, with no
blank line, each run through both sweep cases:

| Plant | GFM renders | f1722cec | ae5dec8a |
|---|---|---|---|
| a list item saying the word | `ul` after the paragraph | green | green |
| a block quote | `blockquote` | green | green |
| a fenced block | `pre` | green | green |
| `***`, then a paragraph | `hr`, then `p` | green | green |
| a `div` line | an HTML block | green | green |
| `---`, then a paragraph | the statement becomes an `h2`, then `p` | **red** | **green** |
| a line continuing the paragraph | the same `p` | green | green |

The last row is part of the statement, so it is exempt by design. The other
six are blocks of their own, and the docstring says the exemption ends where
the statement does, "whatever follows it". R6 says the span ends "at the end
of its paragraph" (⬜ 4).

The `---` row is a regression of the sweep. The f1722cec module ended the
span at any `---`. The new pattern ends it only at a blank line. The shape
needs a person to underline the policy statement itself, so it is narrow.

Ending the span also where one of those blocks begins turned all six red and
kept the continuation line green. The baseline stays green in both cases, and
the sweep module stays green (21 passed). None of the statement's own lines
begins with one of those markers, which is why the baseline holds. The fix is
under `## Paste-ready fixes`.

### ⬜ 2 — moving the filter out of the branch is pinned by nothing

`tests/test_a_signer_declares_its_pact.py:1260`. The commit's third glued
shape puts `## X` between the glued header and the second old table. The walk
stops at the heading, so the stray-row refusal never quotes the old header.
The branch is taken in that shape at f1722cec too, and the filter already ran
there. That shape goes red only because the sentence changed.

With the filter moved back inside the branch and the new sentence kept, the S4
case passes. So do all six pact modules (3447 passed). The first check's exact
shape, a blank line and no heading, is the one that tells the two apart. Added
as a case, it passes at ae5dec8a and fails with the filter moved back. Under
§15 this fix has not been seen red. The case is under `## Paste-ready fixes`.

### ⬜ 3 — the new sentence quotes the old header spaced, whatever the line holds

`hooks/config.py:1364`. The sentence builds the quote from the header's
cells, so a glued `|Signatory|` line is printed as "holds a `| Signatory |`
line". A person who searches the file for the quoted line finds nothing. The
"beside" sentence quotes the same way, but it says "header", while this one
says "line" and asks for that line to be deleted.

The rows carry their line numbers, so the line can be quoted as written. With
that change the glued sentences read `|Signatory|` and
`|Signatory|Change|Verdict|`, and the spaced shapes are unchanged. Four pact
modules stay green (786 passed). The S4 case fails, because its first glued
shape is unspaced and it expects the spaced quote. The fix and the case's
edit are under `## Paste-ready fixes`.

## Findings from reading

### ⬜ 4 — R1 and R6 each claim one shape more than the code gives

`seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:29`
(R1) and `:34` (R6).

- **R1** says a glued old header "is refused once, as a line inside that
  table". In ⬜ 2's shape it is not refused at all. The one refusal is the
  stray-row refusal naming the second old table. Executed: the reader and
  `pact-check` both print that one refusal. Exit 2 holds. Once the second
  table is deleted, the next run names the glued line.
- **R6** says the span ends "at the end of its paragraph". For the six
  blocks in ⬜ 1 the paragraph ends and the span does not.

This is paperwork, a correction not counted in `Needs a fix`. If ⬜ 1's fix
is taken, R6 becomes true as written, and only R1 needs words. Text for R1 is
under `## Paste-ready fixes`.

## Regression tests to plant

- ⬜ 2: the case in its fence, at the end of the S4 case. Executed: green at
  ae5dec8a, red with the filter moved back inside the branch. It was run as
  an edit in the clone and deleted with it, so as a committed case it is
  **unverified**. Whoever writes ⬜ 2's fix answers it.
- ⬜ 1: no new case. The two sweep cases hold it, and the six plants in the
  table are the ones to see red.
- ⬜ 3: the S4 case's first glued shape changes its expected quote, as in the
  fence.

## Facts for the evidence ledger

- R1: ⬜ 4's fence.
- R6: the plants in ⬜ 1's table, if ⬜ 1's fix is taken: each red after it,
  and the continuation line green.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The policy span ends only at a blank line, an ATX heading or a fold marker, so a list item, block quote, fence, thematic break, HTML block or `---` directly under the statement stays exempt; the `---` shape was red at f1722cec and is green now | `tests/test_one_word_one_meaning.py:737` | open | executed: six plants green at ae5dec8a in both sweep cases; the widened end turns all six red and keeps the module green |
| ⬜ 2 | Moving the glued-row filter out of the branch is pinned by no case: the planted shape puts a heading in front of the second old table, so the stray-row refusal never fires | `tests/test_a_signer_declares_its_pact.py:1260` | open | executed: the filter moved back inside the branch keeps six pact modules green (3447 passed); the proposed case is green at ae5dec8a and red with it moved back |
| ⬜ 3 | The glued sentence quotes the old header spaced, so a `\|Signatory\|` line is named as a `\| Signatory \|` line the file does not hold | `hooks/config.py:1364` | open | executed through `pact_signers` and `pact_reviews`; the as-written quote keeps four pact modules green and changes the S4 case's first expectation |
| ⬜ 4 | R1 claims a glued header is refused as a line inside the table, which ⬜ 2's shape does not do; R6 claims the span ends at the paragraph's end, which ⬜ 1's shapes do not do | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:29` | open | read, with the shapes executed under ⬜ 1 and ⬜ 2; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | the first check's ⬜ 1 is closed for the four plants it named | `tests/test_one_word_one_meaning.py:737` | confirmed | executed: four plants green with f1722cec's module and red at ae5dec8a, both sweep cases; the remainder is ⬜ 1 |
| 🟢 | the first check's ⬜ 2 is closed — a glued header beside a second old table is not refused as an entry | `hooks/config.py:1354` | confirmed | executed: one refusal through the reader and through `pact-check` for a pact; the review record's shape the same through the reader |
| 🟢 | the first check's ⬜ 3 is closed — the glued header has its own sentence, and the rows under it are read | `hooks/config.py:1364` | confirmed | executed: the S4 case red with f1722cec's reader; `pact-check` end to end over seven pact and three review-record shapes, every one exit 2; no contradiction with `docs/the-pact.md` or the changelog fragment |
| 🟢 | the first check's ⬜ 4 is closed — R1 and R6 gained text and the four rows are re-stamped | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:34` | confirmed | read: the word diff touches P8, P11, R1 and R6 only; executed: `bin/evidence-check --ledger`, 432 ok; the overstatements are ⬜ 4 |
| 🟢 | nothing else moved | f1722cec..ae5dec8a | confirmed | read: four files, the four the commit names; `hooks/config.py` changes inside `read_table` only; the moved hashes are cited only in this fragment and in the first check |

## Executed probes

| What was run | Result |
|---|---|
| six modules in the clone at ae5dec8a: the signer, sweep, `pact-check`, pact-review, table-walker and signers' CI modules | exit 0, 3447 passed |
| the S4 signer case with f1722cec's `hooks/config.py` | exit 1, 1 failed |
| the S4 signer case with the glued sentence never chosen | exit 1, 1 failed |
| the filter moved back inside the branch, the new sentence kept: the S4 case, then the six modules | exit 0, 1 passed; exit 0, 3447 passed |
| ⬜ 2's proposed case, at ae5dec8a and with the filter moved back | exit 0, 1 passed; exit 1, 1 failed |
| `pact_signers` over seven glued shapes and `pact_reviews` over three, at ae5dec8a | as in the claims above; ⬜ 2's shape gives the stray-row refusal alone |
| `pact-check` end to end from a `test_tmp_` probe, seven pact and three review-record glued shapes | exit 2 in all ten; the new sentence after "the pact " and "the record "; rows under a glued header read |
| eleven policy-span plants through both sweep cases, with f1722cec's module and at ae5dec8a | as in ⬜ 1's table, plus the four claimed plants green before and red after; the baseline green in both |
| ⬜ 1's widened end, the same eleven plants, then the sweep module | the ten block plants red in both cases, the continuation line green; exit 0, 21 passed |
| ⬜ 3's as-written quote, the readers, the S4 case, then four pact modules | the quotes as written; exit 1, 1 failed (its spaced expectation); exit 0, 786 passed |
| `cmarkgfm` over the eleven plants | as in ⬜ 1's table |
| `bin/evidence-check --ledger` on the fragment, in the clone at ae5dec8a | exit 0; `total: 432 ok · 0 drifted · 0 broken` |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this check ran none of it, and the sealer answers it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |

## Paste-ready fixes

### ⬜ 1

```python
    end = re.search(
        r"\n[ \t]*\n"  # a blank line
        r"|\n {0,3}(?:#{1,6}[ \t\n]"  # an ATX heading
        r"|(?:[-*+]|1[.)])[ \t]"  # a list item that can interrupt a paragraph
        r"|>|`{3}|~{3}|<"  # a block quote, a fence, an HTML block
        r"|(?:[-*_][ \t]*){3,}\n|=+[ \t]*\n|-+[ \t]*\n)"  # a break or an underline
        r"|<" + "!--",
        rest,
    )
```

It replaces the one-line `end = re.search(...)` in the span function. The
docstring's first sentence then reads true as it stands, because every
alternative is a place GFM ends the paragraph.

### ⬜ 2

```python
    # A glued old header above a second old table after a blank line: the
    # walk's stray-row refusal names the second, and the glued line is not
    # also refused as an entry (post-review check of #830, white 2).
    signers, refusals, _ = config.pact_signers(
        signer
        + "| Signatory |\n\n| Signatory |\n|---|\n| https://example.com/org/billing |\n"
    )
    assert [s[2] for s in signers] == ["orders-web"], signers
    assert refusals == [
        "has a `Signer` table that ends above `| Signatory |`, a row the walk "
        "never reaches — it and every signer below it would go unread"
    ], refusals
```

It goes at the end of the S4 signer case, after `assert refusals == [glued]`.

### ⬜ 3

```python
        glued = [
            text.splitlines()[line - 1].strip()
            for line, cells in rows
            if holds_old and cells == old
        ]
```
```python
                    f"holds a `{glued[0]}` line inside its {new} table, the word "
```
```python
        signers, refusals, _ = config.pact_signers(signer + under)
        assert [s[2] for s in signers] == ["orders-web"], signers
        assert sum("Signatory" in r for r in refusals) == 1, refusals
        quoted = under.split("\n", 1)[0]
        assert glued.replace("`| Signatory |`", f"`{quoted}`") in refusals, refusals
```

The first fence replaces the line that sets `glued`, and the second the first
line of the glued sentence. Both were executed as above. The third replaces
the body of the S4 case's glued loop. It was not run, so it is
**unverified**, and whoever writes ⬜ 3's fix answers it.

### ⬜ 4 (the run's paperwork)

```text
R1, the claim's last clause, reworded: an old header GFM reads as a row of
the new table (no blank line above it) is not read as a row; it is refused
once, as a line inside that table, unless the walk's stray-row refusal already
names an old header further down, and rows under it with no delimiter row are
the new table's rows and are read (#830).
R1, appended to the grounds: In post-review check 2, at ae5dec8a: a glued
header above a second old table after a blank line gives the stray-row
refusal alone, through the reader and through `pact-check`.
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened: `hooks/config.py` (`gfm_table`, `_stops_at`, `read_table`,
`pact_signers`, `pact_reviews`, `_signer`, `renamed_header`),
`tests/test_one_word_one_meaning.py` (`read`, `flat`, the pact sweep section
from `PACT_LINES` through `test_no_live_text_says_the_word_0_19_0_renamed`),
`tests/test_a_signer_declares_its_pact.py` (the module head, the S4 case and
the case above it), `tests/test_pact_check.py` (`write`, `pact`, `clause`,
`config`, `make_world`, `cite`, `run`, the S4 end-to-end case),
`tests/test_a_pact_review_takes_a_pact_change.py` (the imports, `record`,
`review`, `world`, the S5 both-headers case), `docs/the-pact.md` (the
statement under the `1791239490` fold marker and the heading after it), the
changelog fragment, the overview's S4 row, `bin/test`, the ledger fragment's
rows R1 and R6 and the word diff of P8, P11, R1 and R6, `post-review-check.md`,
and the range's diff and commit message.

# Post-review check — 1791239490-a-repository-that-keeps-a-pact-is-a-signer

| Field | Value |
|---|---|
| What this is | a narrow verifying pass over #830's post-review fix, not a round; the run is capped at round 3 |
| Target SHA | 00b5a549 |
| Range checked | 20eeb185..00b5a549: 00b5a549 alone (the fix, `#830`) |
| Base | `origin/release/v0.19.0` at e6d5a055 |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 00b5a549, with 20eeb185's `hooks/config.py` and sweep module swapped in for the before runs, under `<scratchpad>/<id>/post-review/`; all of it removed at hand-over |
| git | 2.50.1 |

## Summary

All five of round 3's findings are closed as the commit says. The closures
hold in the shapes round 3 named, and a few shapes next to them are still open:

- **⬜ 11 is closed, for a pact and for a review record, end to end.** At
  20eeb185 `pact-check` named the glued old header twice in both files. In a
  review record the second refusal was `the pact review names Signatory`.
  At 00b5a549 it names the header once, as the old header, in every glued
  shape tried. Two shapes beside it are not closed (⬜ 2, ⬜ 3). Both exit 2.
- **⬜ 12 is closed.** An all-caps constant and an all-caps plural in a
  compatibility module are green at 20eeb185 and red at 00b5a549.
- **⬜ 13 is closed for underlines of two or more characters.** The limit
  the orchestrator states is real and is wider than stated (⬜ 1). Round 3's
  own reproduction, `Signatory history` over a dash underline, is still
  green at 00b5a549.
- **⬜ 14 and ⬜ 15 are closed.** The overview's S4 row and R6 say what the
  code does. The three re-stamped rows read 432 ok. Their grounds record
  nothing executed for #830 (⬜ 4).

Nothing else moved. The range touches five files, and they are the five the
commit names. No other ledger row cites a unit whose hash moved.

All four findings are ⬜. None ships a defect: every shape still exits 2, and
the sweep's gap is in a test's exemption, not in shipped behaviour.

## What the account claimed, and what was found

- **Claimed for ⬜ 11:** the old header is named once and not also as an
  entry, and the S4 case gained two shapes that were seen red against
  20eeb185's reader. Executed: the S4 case fails with 20eeb185's
  `hooks/config.py` (`assert 2 == 1`, the entry refusal and the old-header
  refusal both counted). Through `pact_signers` and `pact_reviews`, and
  through `pact-check` end to end for both files, every glued shape names
  the old header once at 00b5a549. The review record path, which round 3
  left unrun, is in the probe table.
- **Claimed for ⬜ 12:** all-caps spellings are swept. Executed, and true.
  The pattern is also stricter than before: `SignatoryURL` in a
  compatibility module is now red, because `\b` does not hold before `U`.
  The five modules are green with it, so this changes no case.
- **Claimed for ⬜ 13:** a paragraph after a setext heading is now red.
  Executed, and true for `---` and `===` underlines. The stated limit is
  that the heading's own text stays inside the span. Executed, and true.
  The limit is wider than stated, as ⬜ 1 explains.
- **Claimed for ⬜ 14 and ⬜ 15:** the S4 row and R6 were reworded, and R1,
  P8 and R6 were re-stamped. Read: both rewordings match round 3's
  paste-ready text. Executed: `evidence-check --ledger` on the fragment reads
  432 ok, 0 drifted. The new hashes `read_table@f83b5a2f`,
  `PACT_HEADER_WORD@275f105e` and `without_the_policy_span@9befc731` are
  cited in this fragment and nowhere else under `seal/` or `docs/`, and so
  is the S4 case's new hash.

## Findings from execution

### ⬜ 11 closed: the glued shapes, before and after

| Shape under the new table, no blank line | 20eeb185 | 00b5a549 |
|---|---|---|
| pact: `\|Signatory\|`, its delimiter row, a row | 3 refusals; the old header named as an entry and as the old header | 2 refusals: the delimiter stop and the old header |
| pact: `\| Signatory \|` alone | 2 refusals, both naming the old header | 1 refusal, the old header |
| review record: old header, its delimiter row, a row | the old header returned as a row; `pact-check` adds `the pact review names Signatory` | 2 refusals: the delimiter stop and the old header; no row returned |
| review record: the old header alone, spaced and unspaced | as above, without the delimiter stop | 1 refusal, the old header; no row returned |

Every `pact-check` run exits 2 at both versions. At 00b5a549 no review run
prints `NOT TAKEN`, and none counts the old header as a signer.

### ⬜ 1 — the policy span still exempts whatever stands before the next heading, a single-character underline included

`tests/test_one_word_one_meaning.py:734`. The span runs from the fold marker
to the next heading or fold marker in the flattened text, and it does not
stop where the statement's paragraph ends. Plants after the statement's
`Enforced by:` line, each run through both sweep cases:

| Plant | 20eeb185 | 00b5a549 |
|---|---|---|
| `History` over `-------`, then a paragraph saying the word | green | red |
| `History` over `=======`, then the same paragraph | green | red |
| `Signatory history` over a dash underline, nothing after it (round 3's plant) | green | **green** |
| `History` over a one-character `=` underline, then the paragraph | green | **green** |
| `History` over a one-character `-` underline, then the paragraph | green | **green** |
| a plain paragraph after a blank line, saying the word | green | **green** |
| `### Signatory history` | red | red |

cmark-gfm renders both one-character underlines as headings, `h1` and `h2`
(executed with the clone's `cmarkgfm`). So the fix misses the shortest
underline of its own class, and the stated limit is one case of a wider one.
The span exempts anything between the statement and the next heading. The
docstring's sentence, "so the exemption ends where the statement does",
does not hold for any of the three bold rows. R6 describes the mechanism
and stays true.

The statement is one paragraph, so the paragraph's end is where it ends.
Ending the span at the first blank line, an ATX heading at the start of a
line, or a fold marker turned every row above red. It kept the sweep module
green (21 passed) and the baseline green in both cases. The fix has to cut
the raw text and flatten it afterwards, because flattening is what erases
the blank line. It is under `## Paste-ready fixes`.

The limit is acceptable only if it is written down, and today it is not.
The orchestrator's prompt is the only place that states it. The docstring
claims more than the code does, so the fix below is the better answer.

### ⬜ 2 — two old headers: a glued one and a separate old table below it

`hooks/config.py:1354`. The row filter sits inside the branch that adds the
old-header refusal. That branch is skipped when the walk's stray-row refusal
already quotes the old header. Text: the `Signer` table, then `| Signatory |`
glued under it, a blank line, and a whole old table. At 00b5a549 the glued
line is refused as an entry: "`Signatory` is not a remote URL". The second
header is named by the stray-row refusal. The S4 docstring (lines 1222-1225)
says a glued old header "is named as the old header rather than as an entry".
In this shape that sentence is false.

The shape needs two old headers in one file, so it is narrow. Moving the
filter out of the branch drops the glued row in every shape where the old
header is held. With that change the shape gives one refusal, the stray row
quoting `| Signatory |`. The five pact modules stay green (3426 passed).

### ⬜ 3 — a glued old header with rows under it and no delimiter row: "nothing under it is read" is false

`hooks/config.py:1358`. Text: the `Signer` table, `| Signatory |` glued under
it, and `| https://example.com/org/billing |` under that, with no delimiter
row. GFM reads all of it as one table. `pact_signers` returns `billing` as a
signer, and `pact-check` prints `1 of 2 signers read`. The one refusal says
that "nothing under it is read while the `| Signer |` table stands". The row
under it was read. The review record behaves the same way: the row under
the glued header comes back as a review row.

This is the same at 20eeb185, so it is not a regression of #830. The exit is
2, and the remedy the sentence gives ("move its rows into that table and
delete it") still produces a correct file. A person reads one false clause.
Nothing is lost. A sentence for this shape would change a printed line, and
under §14 it would need its own pin. This check wrote none and ran none.

## Findings from reading

### ⬜ 4 — R1 and R6 carry #830's change in their hashes, but their grounds record nothing executed for it

`seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:34`
(R6) and `:29` (R1). R6's claim gained "a setext underline included" and
"upper case included (#830)". Its grounds still end at round 2's fix pass,
and its notes record no rewording for #830. Each earlier pass appended what
it saw red, so this row breaks its own pattern. R1's claim did not gain the
glued clause from round 3's *Facts for the evidence ledger*. The overview's
S4 row carries that clause. R1's existing sentence, "refused, naming it,
wherever its table stands", stays true. This is paperwork, a correction not
counted in `Needs a fix`. Text for both rows is under `## Paste-ready fixes`,
and the executed facts it states are this check's.

## Regression tests to plant

- If ⬜ 1's fix is taken: no new case. The two sweep cases hold it. The
  one-character underline plants and the heading-text plant are the ones to
  see red, as the plants table above shows.
- If ⬜ 2's fix is taken: one more `under` shape in the S4 case's glued
  loop, `"| Signatory |\n\n| Signatory |\n|---|\n| https://example.com/org/billing |\n"`,
  asserting `sum("Signatory" in r for r in refusals) == 1` and no entry
  refusal. Executed through the readers only. It was not written as a case,
  so it is **unverified** as a case. Whoever writes ⬜ 2's fix answers it.

## Facts for the evidence ledger

- R6: the executed sentence in ⬜ 4's fence.
- R1: the glued-shape clause and its executed sentence in ⬜ 4's fence.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The policy span ends at a heading or fold marker, not at the statement's paragraph end, so a setext heading's text, a one-character `=` or `-` underline and a plain paragraph after the statement all stay exempt; the docstring says the exemption ends where the statement does | `tests/test_one_word_one_meaning.py:734` | open | executed: three plants green at 00b5a549; the blank-line end turns all seven plants red and keeps the module green |
| ⬜ 2 | A glued old header beside a second old table below it is still refused as an entry, because the row filter sits inside the branch the stray-row refusal skips | `hooks/config.py:1354` | open | executed through `pact_signers`; the filter outside the branch gives one refusal and keeps five pact modules green |
| ⬜ 3 | With rows under a glued old header and no delimiter row, those rows are read as signers or review rows, while the refusal says nothing under it is read | `hooks/config.py:1358` | open | executed: `1 of 2 signers read` and the refusal at exit 2; the same at 20eeb185, not a regression |
| ⬜ 4 | R6's and R1's grounds record nothing executed for #830, and R1 did not gain the glued clause round 3 listed | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:34` | open | read; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | round 3's ⬜ 11 is closed — a glued old header is named once, as the old header, for a pact and for a review record | `hooks/config.py:1354` | confirmed | executed: the S4 case red with 20eeb185's reader; `pact-check` end to end over three pact and three review shapes at both versions |
| 🟢 | round 3's ⬜ 12 is closed — all-caps spellings are swept in the compatibility modules | `tests/test_one_word_one_meaning.py:809` | confirmed | executed: both all-caps plants green with 20eeb185's module and red at 00b5a549; capitalised prose stays green by design |
| 🟢 | round 3's ⬜ 13 is closed for underlines of two or more characters | `tests/test_one_word_one_meaning.py:734` | confirmed | executed: `---` and `===` plants green before, red after; the remainder is ⬜ 1 |
| 🟢 | round 3's ⬜ 14 and ⬜ 15 are closed — the S4 row and R6 say what the code does, and the re-stamped hashes are current | `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md:34` | confirmed | read against round 3's fences; executed: `evidence-check --ledger`, 432 ok |
| 🟢 | nothing else moved | 20eeb185..00b5a549 | confirmed | read: five files, the five the commit names; the moved hashes are cited only in this fragment |

## Executed probes

| What was run | Result |
|---|---|
| four modules in the clone at 00b5a549: the signer, sweep, `pact-check` and pact-review modules | exit 0, 2760 passed |
| the S4 signer case with 20eeb185's `hooks/config.py` | exit 1, 1 failed (`assert 2 == 1`) |
| `pact_signers` over six pact shapes and `pact_reviews` over three review shapes, at both versions | at 00b5a549 every glued shape names the old header once and returns no old-header row; the two-old-headers shape (⬜ 2) and the rows-without-delimiter shape (⬜ 3) as described |
| `pact-check` end to end from a `test_tmp_` probe, three pact and three review-record glued shapes, at both versions | exit 2 in all twelve runs; 20eeb185 adds the entry refusal or the `names Signatory` review refusal, 00b5a549 does not |
| compatibility-module plants, tree case: all-caps constant, all-caps plural, `SignatoryURL`, lowercase, capitalised prose | 00b5a549: the first four red, prose green; with 20eeb185's module: lowercase red, the rest green |
| seven policy-span plants through both sweep cases, at both versions | as in ⬜ 1's table |
| ⬜ 1's blank-line end applied, the same seven plants, then the sweep module | all seven red in both cases; exit 0, 21 passed |
| ⬜ 2's filter outside the branch, the reader shapes, then five pact modules (the signer, `pact-check`, pact-review, table-walker and signers' CI modules) | the shape gives one refusal; exit 0, 3426 passed |
| `cmarkgfm` on one-character `=` and `-` underlines | `h1` and `h2` |
| `bin/evidence-check --ledger` on the fragment, in the clone at 00b5a549 | exit 0; `total: 432 ok · 0 drifted · 0 broken` |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this check ran none of it, and the sealer answers it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| none | — | — |

## Paste-ready fixes

### ⬜ 1

```python
def without_the_policy_span(where, text):
    """TEXT, as written, flattened with the policy's statement about the old
    header taken out: from its fold marker to the end of its paragraph, a
    heading at the start of a line, or the next fold marker, whichever comes
    first. The statement is one paragraph, so the exemption ends where the
    statement does, whatever follows it -- a setext heading's own text and an
    underline of one character included (round 1 of #822, white 2; round 2,
    white 6; round 3, white 13; #830). The cut is made before flattening,
    which is what would erase the blank line."""
    span = PACT_RENAMED_SPANS["docs/the-pact.md"]
    head, marker, rest = text.partition(span)
    assert marker, f"{where}: the excluded span `{span}` is gone"
    end = re.search(r"\n[ \t]*\n|\n {0,3}#{1,6}[ \t\n]|<" + "!--", rest)
    assert end, (
        f"{where}: the excluded span is the last statement in the file, "
        "so this exclusion now removes everything after it"
    )
    return " ".join((head + " " + rest[end.start() :]).split())
```
```python
            text = without_the_policy_span(where, read("docs", "the-pact.md"))
```
```python
            text = without_the_policy_span(rel, text)
```

The second fence replaces the call in
`test_no_pact_text_names_a_signer_the_way_0_18_did`, and the third the one
in `test_no_live_text_says_the_word_0_19_0_renamed`.

### ⬜ 2

```python
        named = f"`| {' | '.join(old)} |`" if old else None
        if holds_old:
            # An old header with no blank line above it is one of this
            # table's rows to GFM; it is the old header, named below or by the
            # walk's stray-row refusal, never an entry (#830).
            rows = [(line, cells) for line, cells in rows if cells != old]
        if holds_old and not any(
            table_cells(quoted) == old
            for r in refusals
            for quoted in re.findall(r"`([^`]*)`", r)
        ):
            refusals = [
```

### ⬜ 4 (the run's paperwork)

```text
R6, appended to the grounds: In #830's post-review fix, at 00b5a549: an
all-caps constant and an all-caps plural in `tests/test_pact_check.py`, and a
paragraph after a `---` or `===` setext heading, each green with 20eeb185's
module and red after it (the constant and plural the tree case, the paragraph
both cases).
R6, appended to the notes: Reworded 2026-10-06 in #830's post-review fix
(round 3, white 12, 13, 15): a setext underline ends the span, and the
compatibility modules are swept for every spelling but the capitalised
singular.
R1, appended to the claim: an old header GFM reads as a row of the new table
is refused once, as the old header, and is not read as a row (#830).
R1, appended to the grounds: In #830's post-review fix, at 00b5a549: the S4
case's glued shapes red against 20eeb185's reader; `pact-check` end to end,
for a pact and for a review record, names the glued header once.
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened: `hooks/config.py` (`table_cells`, `table_end`, `gfm_table`,
`_stops_at`, `read_table`, `pact_signers`, `pact_reviews`, `_signer`,
`renamed_header`), `tests/test_one_word_one_meaning.py` (`read`, `flat`,
`pact_texts`, the sweep section from `PACT_RENAMED` through
`test_no_live_text_says_the_word_0_19_0_renamed`),
`tests/test_a_signer_declares_its_pact.py` (the S4 case),
`tests/test_pact_check.py` (`commit`, `write`, `pact`, `clause`, `config`,
`make_world`, `cite`, `run`, the S4 end-to-end case),
`tests/test_a_pact_review_takes_a_pact_change.py` (the module head,
`record`, `review`, the S5 both-headers case), `docs/the-pact.md` (the
statement under the fold marker and the heading after it), `bin/test`, the
ledger fragment's rows P8, R1 and R6 at both versions, the overview's S4
row, `rounds/round-3-report.md`, the range's diff and commit message, and
the model record on `origin/main`.

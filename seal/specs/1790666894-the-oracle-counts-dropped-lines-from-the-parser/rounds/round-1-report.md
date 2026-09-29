# 1790666894-the-oracle-counts-dropped-lines-from-the-parser — round 1 report

| Field | Value |
|---|---|
| Round | 1 |
| Target | `test/677-the-oracle-counts-dropped-lines-from-the-parser` at `2ee3e62f`, diff `cd56113c...2ee3e62f` |
| Reviewed by | specseal:warden on claude-opus-5-5, in a `git clone --no-local` of the target, with a second clone at the base |
| Earlier rounds | none |

## What this round found

The fix holds. The oracle now takes the dropped-line count from the parser on
every path this round could build, and every new case goes red against the
code it was written for. Nothing needs a fix.

1. The count is right on every rule path the prompt named, measured against a
   ground truth that reads no count and no marker (executed; 117,206 line
   questions, 0 disagreements at the head, 26 at the base).
2. Every new row is red where the phase records say, and the guard fails
   where its docstring says (executed; seven mutations).
3. Wrapping the two rules changes nothing else the parser does and leaks
   into no other parser (executed). The module is green on 3.12 and 3.14.
4. H's record edits are true, and the checkers agree (executed).
5. Two wording findings, both ⬜. The fragment and two docstrings say "Unicode
   space" where the fix also covers U+001F, which is a C0 control and no
   Unicode space (⬜ 1). H's P1-1 row keeps a round 2 note that the deletion
   also made false, and the new `Corrected` note names only round 1's
   sentence (⬜ 2, paperwork).

## Findings from execution

### 🟢 The wrapper reads the count the parser drops, on every path through both rules

`tests/commonmark_oracle.py:73` (`_recording_lines`).

This was judged by a differential that shares nothing with the count. The
ground truth for "line K begins inside inline HTML" appends a mark to the
**end** of line K-1 and parses again. It then asks whether an `html_inline`
token holds the mark. Appending at a line's end reads no container marker and
no dropped line, so it cannot inherit the count's mistakes. It is asked only
where line K-1 ends in an ASCII letter (a run of letters is appended) or holds
only non-space, non-tab whitespace (a run of en and em spaces is appended). In
both cases appending cannot change the block structure.

The documents were random, 60,000 per run, seeded. Each opened with zero to
two lines of only U+00A0, U+001F, U+3000, U+2000, U+000C, U+0085 or U+2028,
some with a space or a tab before, behind random container prefixes (`>`,
` > `, `   > `, `>     `, `- `, `10. `, `- > `, `> > `, `\t`, `* `, `1) `).
Then came an opener and a closer of four inline kinds (a processing
instruction, a comment, an open tag split across lines, a declaration),
mixed with lazy `>` lines, `    >` and `\t>`, setext underlines, fences, an
HTML block, ATX headings, list markers, a reference definition, table rows,
blank lines and the end of input.

| Oracle | Line questions asked | Disagreements |
|---|---|---|
| head, `2ee3e62f` | 117,206 | 0 |
| base, `cd56113c` | 117,206 | 26, every one a lazy `>` four columns in or behind a tab |

The base count proves the differential can fail, and it fails on exactly the
class #677 names. A companion count over the same documents found where the
parser dropped lines. It found 2,990 paragraph tokens and 51 setext heading
tokens that dropped at least one line and held inline HTML, at the top level
and nested. So both wrapped rules were exercised with the count mattering.

The reading agrees. In markdown-it-py 4.2.0 both rules build their content
as `state.getLines(start, next, state.blkIndent, False).strip()` and push
the inline token with `map = [start, next]`; `lheading` excludes the
underline from that map. Neither rule touches `blkIndent`, `bMarks` or
`tShift`. A block quote and a list item restore the marks they moved only
after their inner tokenize returns, so the wrapper's second `getLines` call
reads the same state the rule read.

### 🟢 The expected answers are CommonMark's, checked against cmark

The spec's expected values were read from the specification and not run
(Q1). This round ran the 24 rows of
`test_the_oracle_counts_the_lines_the_parsers_strip_dropped` and all 34
shapes of `test_the_oracle_counts_every_character_the_strip_drops` through
cmark 0.29.0.gfm.2 (the `cmarkgfm` package, unsafe HTML on). The check was
that the opener and closer render as one raw inline HTML run across the line
break, and that the closer's line is the one the row says is hidden. All 58
agree. This check is weaker than the differential above. It confirms which
line is hidden, not where a paragraph starts, and the row's claim needs
nothing more.

### 🟢 Every new case is red against the code it was written for

The module was run with `-p no:xdist` under each mutation. The clone was
restored after each one, and `git status` was clean at the end.

| Mutation | Result |
|---|---|
| none | exit 0, 129 passed |
| the oracle file from `cd56113c` | exit 1, 6 failed: the five S1 rows and `test_where_the_walk_claims_to_be_exact_it_is` (S5) |
| `lheading` left unwrapped | exit 1, 3 failed: the three S2 rows alone |
| `paragraph` left unwrapped | exit 1, 50 failed |
| the count forced to 0 on the read side | exit 1, 53 failed: 11 existing marker rows, all 24 new rows, all 17 S4 characters, and S5 |
| the S4 set emptied | exit 1: the guard fails, and S4 is `SKIPPED ... got empty parameter set` |
| the S4 set replaced by a space and a tab | exit 1: the guard fails alone, and S4 passes on both |

The first assertion of the S4 case stops it, so its second shape (behind a
list marker) was run on its own under the count-0 mutation. All 17 characters
were red. At the base oracle, all 34 S4 shapes were green, as phase 2
recorded (Q2).

### 🟢 No state leaks, and the parser's output is unchanged

`parser()` builds its own `MarkdownIt`. `Ruler.at` replaces the rule on that
instance's ruler alone. A `MarkdownIt("commonmark").enable("table")` built
after the oracle is imported still holds the library's own `paragraph` and
`lheading` functions. On the oracle's ruler both rules keep an empty `alt`
list and stay enabled, in the library's order. Over 30,000 generated
documents, the wrapped parser's token stream (type, tag, map, content,
level, markup, info, nesting, hidden and children, recursively) was
identical to that fresh parser's. `meta` is written per token per parse and
is never read back across parses.

The module passed 129 of 129 on Python 3.14.3 (`bin/test`'s environment) and
on 3.12.11 (`uv run --isolated --python 3.12` with `markdown-it-py==4.2.0`).
CI's matrix runs 3.12.

### 🟢 H's record edits are true, and the checkers agree

- **The markers.** With the 24 appended markers stripped, the records arm
  refuses 26 names on exactly those 24 lines. Every refusal names the
  deleted marker helper and nothing else. With the markers in place it
  refuses none. Each marked line differs from the base only by the appended
  marker. On a table row the marker sits inside the last cell, which is
  `Grounds` or `Result` there and never a `Verdict` cell.
- **R1-1 removed.** Its claim was the helper's marker reading, and the helper
  is gone. `CLAUDE.md`'s rule is that a row whose anchor a change removes is
  REMOVED, not re-pointed.
- **P1-1 corrected.** The new `Corrected` note is true. It says the count now
  comes from the two wrapped rules, `_inline_html_lines` takes no lines, and
  the row's own claim holds. Its `_inline_html_lines` anchor was re-stamped,
  and its test anchor did not move. ⬜ 2 below is about an older note on the
  same row.
- **F's P1-2 and P2-1, and H's P2-1.** Each `Re-read` note matches the code.
  In S5 at the base, the oracle put the inline HTML on the blank line after
  the paragraph, line 4, which the walk claims live.
- `bin/evidence-check .` exits 0: 2,992 ok, 0 drifted, 0 broken. `--strict`
  also exits 0. `bin/correction-check --range cd56113c...HEAD` (the SHA
  `origin/release/v0.16.0` resolves to) exits 0 and reports no merge commit
  in range, so it had nothing to compare. `bin/unverified-check` on the work
  item reports one open row, the sealer's.

## Findings from reading, confirmed by execution

### ⬜ 1 — The fragment and two docstrings say "Unicode space", and the fix also covers U+001F

`seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/changelog.md:4`,
`tests/commonmark_oracle.py:84` (`_recording_lines`' docstring),
`tests/commonmark_oracle.py:123` (`_inline_html_lines`' docstring, in the
paragraph this diff rewrote), and
`tests/test_the_hooks_hide_what_a_renderer_hides.py:262`.

The fragment names the trigger as "a line of only a Unicode space". U+001F
triggers the same false red at the base. With `[U+001F, "    >", "x <? a",
"b ?>"]` the base oracle gives `{}` and the head gives `{3}`, exactly as with
U+00A0 (executed, all 17 characters of the S4 set). U+001F is category Cc,
Information Separator One, and is not a Unicode space. CommonMark's own
definition of whitespace does not include it either, which the S4 case's
docstring says correctly. A line mixing a space or a tab with those
characters triggers it too (`" " + NBSP`, executed).

The fragment's sentence is not false. It is narrower than the fix, and a
reader who meets U+001F learns nothing from it. The three docstrings say the
same thing, and one sentence of the new case's docstring overstates the other
way: "Every row here opens with such a line". Two rows do not. The item that
opens on a blank line starts with `-`, and the reference-definition row
starts with `[a]: /u`. In both, the paragraph opens with such a line, not the
row. The behaviour is right everywhere. That is ⬜ by the findings format's
test: the release ships no defect if this stands.

## Paperwork

### ⬜ 2 — H's P1-1 keeps a round 2 note the deletion made false

`seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md`,
row P1-1.

The row's round 2 `Re-read` note says that `_inline_html_lines` "now tells"
the deleted helper whether a line opens the paragraph. It also says "R1-1 is
the claim about both". Both are false at the head: the helper is gone and
R1-1 is removed. The new `Corrected` note opens with "the round 1 note's
last sentence is no longer true" and names nothing of the round 2 note. A
reader who meets the round 2 note first is told of a row that no longer
exists. The next note does correct it in substance ("the helper is deleted
with R1-1"), so this is a correction to the record and not to the code. By
the verifying round's rule for a `seal/ledger/` location, it is ⬜ and stays
out of `Needs a fix`.

## The account, checked

| Claimed | Found |
|---|---|
| Phase 1: S1 and S5 red at the base oracle; S2 red with `lheading` unwrapped | Confirmed: 6 failed and 3 failed, the same ids |
| Phase 1: 20 failed with the count forced to 0 | True for phase 1's rows. At the head the same mutation gives 53, which is the fragment's phase 2 note's 70 less the 17 second shapes run apart |
| Phase 2: every S4 second shape red when run apart | Confirmed: 17 of 17 |
| Phase 2: only S1's five rows red at the base, over S1 to S4 | Confirmed, both from the module run and from the S4 probe (0 of 34 red at the base) |
| Overview: the guard is red with the set emptied and with a space and a tab | Confirmed, and S4 itself is skipped and green respectively, as its docstring says |
| Spec: `Ruler.at` resets `alt`, and both rules already had `[]` | Confirmed from `ruler.py` and from the built ruler |
| Spec: six places push an `inline` token, and only two join lines | Confirmed by grep in 4.2.0: `paragraph`, `lheading`, `heading`, `table` twice, and the alert title in `blockquote.py:299`, which the `commonmark` preset leaves off |
| Phase 1: 24 marked lines in five files, 26 refusals | Confirmed by the records arm itself with the markers stripped |
| The fragment: "a line of only a Unicode space" | Narrower than the fix: ⬜ 1 |

## Regression tests to plant

None required. The differential above found the base defect 26 times in
60,000 documents, about one in 2,300. A seeded case small enough for the
module's budget would miss it, so it stays a probe and not a case.

## Facts for the evidence ledger

- Over 30,000 generated documents, markdown-it-py 4.2.0's token stream is
  identical with and without the two wrapped rules, apart from `meta`. A
  `MarkdownIt` built after the oracle keeps the library's own rule functions
  (executed this round). This supports the fragment's P1-1 claim that the
  rule is "called unchanged". It needs no new row, and a `Re-read` note is
  optional.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The changelog fragment and three docstrings name the trigger as a line of only a Unicode space; U+001F, a C0 control, triggers the same false red and is fixed too, and one docstring says every row opens with such a line where two rows' paragraphs do | `seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/changelog.md:4` | open | Executed: all 17 characters of the S4 set, U+001F among them, give `{}` at the base and `{3}` at the head on the S1a shape; also `tests/commonmark_oracle.py:84`, `:123` and `tests/test_the_hooks_hide_what_a_renderer_hides.py:262` |
| ⬜ 2 | H's P1-1 keeps a round 2 `Re-read` note that the deletion made false, and the new `Corrected` note names only round 1's sentence | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` P1-1 | open | Read: the round 2 note says the helper is told whether a line opens the paragraph and that R1-1 is the claim about both; the helper and R1-1 are gone. Paperwork, so not counted in `Needs a fix` |
| 🟢 | The wrapper reads the count the parser drops on every path through `paragraph` and `lheading`: setext, lazy lines, interruption by a list, fence, HTML block or heading, end of input, and nested containers | `tests/commonmark_oracle.py:73` | confirmed | Executed differential against a mark appended at a line's end: 117,206 line questions, 0 disagreements at the head and 26 at the base |
| 🟢 | Every new case is red against the code it was written for, and the guard fails where its docstring says | `tests/test_the_hooks_hide_what_a_renderer_hides.py:186` | confirmed | Executed, seven mutations: base oracle 6 failed; `lheading` unwrapped 3; count 0 53, with the S4 second shape 17 of 17 run apart; set emptied and set of a space and a tab both red on the guard alone |
| 🟢 | Wrapping leaks no state and changes no token | `tests/commonmark_oracle.py:100` | confirmed | Executed: a fresh parser keeps the library's rule functions; 30,000 documents give identical token streams; the module passes 129 of 129 on 3.12.11 and 3.14.3 |
| 🟢 | H's R1-1 removal, P1-1 correction and 24 markers are true, and the checkers agree | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | confirmed | Executed: with the markers stripped the records arm refuses 26 names on those 24 lines, all the one deleted helper; `evidence-check` 0 drifted and `--strict` exit 0; `correction-check` exit 0 with no merge commit in range |
| 🟢 | The expected answers of the 24 rows and 34 S4 shapes are CommonMark's | `tests/test_the_hooks_hide_what_a_renderer_hides.py:186` | confirmed | Executed against cmark 0.29.0.gfm.2: 58 of 58 agree |
| ❓ | The module on Python 3.13 and on CI's Linux and Windows legs | `.github/workflows/test.yml:35` | ❓ out of verified scope | Only macOS on 3.12.11 and 3.14.3 ran here. The oracle is pure Python and reads no path, so the risk is low. The sealer's broad run and CI at the pull request answer it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q` in the clone at `2ee3e62f`, Python 3.14.3 | exit 0, 129 passed |
| the same module through `uv run --isolated --no-project --python 3.12 --with pytest --with markdown-it-py==4.2.0` | exit 0, 129 passed on 3.12.11 |
| the module under seven mutations, `-p no:xdist`, restored after each | as tabled under *Every new case is red*; `git status` clean after |
| differential: a mark appended at line K-1's end against the oracle's lines, 60,000 seeded documents, head and base | head 0 of 117,206 disagree; base 26 of 117,206 |
| coverage count over the same documents: inline tokens with a dropped line | 2,990 paragraph and 51 setext tokens with a dropped line and inline HTML |
| wrapped against fresh parser over 30,000 documents, and the fresh parser's rule functions | 0 documents differ; `paragraph` and `lheading` are the library's own |
| the S4 second shape under the count-0 mutation; all 34 S4 shapes at the base oracle | 17 of 17 red; 0 of 34 red |
| the S1a shape opened by each of the 17 S4 characters, and by mixed lines, base against head | base `{}` and head `{3}` for all 17, U+001F included, and for the mixed lines |
| the 24 new rows and 34 S4 shapes through cmark 0.29.0.gfm.2 | 58 of 58 agree |
| the records arm with H's 24 markers stripped, restored after | exit 2, 26 refused, every one the deleted helper, on exactly the 24 lines; `git status` clean after |
| `bin/evidence-check .` and `bin/evidence-check --strict .` | exit 0 both; 2,992 ok, 0 drifted, 0 broken; records arm 0 refused |
| `bin/correction-check --range cd56113c...HEAD` | exit 0: no merge commit in range |
| `bin/unverified-check` on the work item | exit 0: 1 open (the sealer's), 2 closed |
| a dry `round-record new` over this report, in the clone, the record deleted with the clone | the record was written: three tables, `Needs a fix` and `Loses a record or crashes` both `no`, and `Pass` unchecked over the two open ⬜ rows. Its chain-check exit 1 comes only from other work items' targets that the clone cannot reach |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, and this round ran none of it |

### The differential's ground truth

```python
def truth(src_lines, k):
    prev = src_lines[k - 1]
    if prev[-1:].isascii() and prev[-1:].isalpha():
        mark = "QzqMARKqzQ"
    elif prev and all(c.isspace() and c not in " \t" for c in prev) \
            and not set(prev) & {"\x0c", "\x85", "\u2028"}:
        mark = "\u2002\u2003\u2002"
    else:
        return None
    marked = list(src_lines)
    marked[k - 1] = prev + mark
    return any(t.type == "html_inline" and mark in t.content
               for t in all_tokens(P.parse("\n".join(marked))))
```

## Paste-ready fixes

### ⬜ 1 — name what the strip drops, not only Unicode spaces

In `seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/changelog.md`, lines 3–6:

```markdown
- The suite's CommonMark oracle no longer reports a false disagreement with
  the hooks' walk on a paragraph that opens with a line holding only
  characters Python's `str.strip` removes and CommonMark reads as text (a
  no-break space, another Unicode space, or U+001F) and has a `>` indented
  four columns, or behind a tab, on a later line (#677). markdown-it-py's
  strip drops such an opening line, and the oracle
```

In `tests/commonmark_oracle.py`, `_recording_lines`' docstring:

```python
    The joined lines end in `\\n` and only there, so every `\\n` inside what
    `lstrip` removes from the top ends a line it removed whole, whichever of
    the characters the strip removes that line held, U+001F among them
    (#677)."""
```

In `tests/commonmark_oracle.py`, `_inline_html_lines`' docstring:

```python
    `str.strip` applied to the whole by the parser. That strip also takes a
    line holding only a no-break space, another Unicode space or U+001F,
    which CommonMark reads as paragraph text, so the lines it dropped from
    the top are counted before an offset is turned into a line. The parser's own
```

In `tests/test_the_hooks_hide_what_a_renderer_hides.py`, the new case's docstring:

```python
    """#677. The parser joins a paragraph's lines from behind the container
    markers it consumed and applies `str.strip` to the whole, which also
    drops a line holding only a no-break space, another Unicode space or
    U+001F, which CommonMark reads as text. Every row's paragraph opens with
    such a line, so every row puts its inline HTML one line early or late
    wherever the oracle counts those lines wrong.
```

### ⬜ 2 — the new Corrected note names both notes it corrects

In H's P1-1 row, the opening of the `Corrected 2026-09-29 in phase 1 of work item 1790666894 (#677)` note:

```markdown
**Corrected 2026-09-29 in phase 1 of work item 1790666894 (#677):** the round 1 note's last sentence and the round 2 note are no longer true.
```

Needs a fix: no
Loses a record or crashes: no

The broad gate is not due yet, and only paperwork stands before it. This
round leaves nothing that needs a fix. But `round_record.py` ticks `Pass`
only when no verdict row reads `open`, and the two ⬜ rows do, so the record
this report produces has `Pass` unchecked (executed: a dry `round-record new`
in the clone). Once both ⬜ rows are closed, by the pasted wording or by an
answer with grounds, the sealer's spawn is what comes due.

## Proof block

Files opened this round, in the clone at `2ee3e62f` unless named:

- `seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`
- the diff `cd56113c...2ee3e62f` of `tests/commonmark_oracle.py` and `tests/test_the_hooks_hide_what_a_renderer_hides.py`, and `tests/commonmark_oracle.py` whole
- the diff of `seal/ledger/` and of H's `rounds/` records, and the 24 marked lines, eight of them read in place
- H's ledger P1-1 and P2-1 rows, and F's P1-2 row
- markdown-it-py 4.2.0's `rules_block/paragraph.py`, `rules_block/lheading.py`, `Ruler.at` in `ruler.py`, and the rule table in `parser_block.py`, from the clone's `.venv`
- `bin/test`, the head of `.github/scripts/run_tests.py`, and `.github/workflows/test.yml`'s Python lines
- the sample report's shape, in the `664-gfm-line-ends` worktree

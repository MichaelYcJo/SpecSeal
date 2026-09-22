# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 1 report

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

Target SHA `dab23fcb8a0e73211cc930e08d527bd7cead5296`, which was HEAD when this
round started and had not moved. Base `origin/release/v0.13.0` at `3cdfd8ad`.
Reviewed in a `git clone --no-local` of the repository at that SHA; the clone
and every probe are deleted.

## How the findings hang together

The build gives one rule one owner and both readers ask it. That shape is
right, and the three constraints it was held to all hold: `comment_scan`,
`strip_comments`, `blank_fences` and `readable` are byte-identical to the
base, so nothing pinned moved. What the three findings share is the rule's
**edge**, and they fall in causal order.

1. The span pass blanks a whole span. A span holding only the CLOSER is
   blanked too, so a closer quoted in prose stops closing a draft — and a real
   section marker below it stops being live. That is new at this SHA.
2. The pass is single-line, and the docstring says the limit's failure
   direction is the safe one. It is not: a marker inside a multi-line code
   span is read as a fold record, and `settle --retire` removes the directory
   at exit 0. The grounds for leaving that door open — *a shape this
   repository has never carried* — is false at this SHA.
3. The class is written as *a line stops being live two ways*. There is a
   third, for `coordinates`: an indented code block is a quotation too.

None of the three is reachable in the tree as it stands, which I measured
rather than assumed. They are ranked by what a release would ship, not by how
likely the shape is today.

---

## 🟡 1 · A closer quoted in prose no longer closes a parked draft, and the marker below it is lost

`skills/verify/scripts/unverified_check.py#live_lines` (the composition), by
way of `#blank_code_spans`.

`blank_code_spans` blanks an entire span, delimiters and content, and (NAME NOT IN TREE)
`live_lines` then asks the comment state of that text. A span holding a lone
`-->` therefore disappears before the scan sees it, so a draft that the
quotation used to close stays open and parks everything below.

**Executed**, the same six lines through the base's reader and through this
SHA's, with the section reader driven identically:

| | `1700000001-alpha` | `1700000002-beta` |
|---|---|---|
| base `3cdfd8ad` | `hooks/a.py` | `hooks/b.py` |
| this SHA | `hooks/a.py`, `hooks/b.py` | — the section is gone |

The fixture is a parked draft whose middle line reads *the draft ends with*
`-->` *said in prose*, followed by a real `<!-- specs/1700000002-beta -->`
marker and its row. `settle.coordinates` at this SHA answers
`{'1700000001-alpha': ['hooks/a.py', 'hooks/b.py']}` — one work item's row
attributed to another.

**Why it matters.** This is finding 2's own harm, arriving through the fix for
finding 2: `segment_of` groups two work items wrongly and the report names the
wrong segment. The `blank_code_spans` docstring calls *fewer lines live* the (NAME NOT IN TREE)
safe direction, and for `folded_items` it is — a fold reported as a deletion.
For `coordinates` it is not: a lost marker does not drop a row, it hands the
row to whichever section was open.

**Why it is not 🔴.** Measured over the whole corpus — `seal/ledger.md`, the
eight top-level `docs/` documents, every `seal/ledger/*.md` fragment — the
number of lines that go from live to not live between the two rules is **0**.
Nothing is mis-grouped today, and `bin/settle` prints what the record quotes.

The fix below keeps `comment_scan` the one scanner, so phase 2's pin survives
it. I tried two other shapes first and both failed: an interleaved walk that
asks the comment state itself reddens
`test_one_comment_scanner_serves_both_readers`, because that case stubs (NAME NOT IN TREE)
`comment_scan` and a walk of its own no longer answers from the stub; and
narrowing the blanking inside `blank_code_spans` unconditionally reddens four (NAME NOT IN TREE)
of the five shapes in
`test_a_code_span_closes_at_a_backtick_string_of_equal_length`. The predicate
form below is the one that leaves both pins standing.

## 🟡 2 · A marker inside a multi-line code span is read as a fold record, and the directory goes

`skills/verify/scripts/unverified_check.py#blank_code_spans`, the docstring's
single-line paragraph.

The docstring states the limit and then states its failure direction: *fewer
lines live: a fold reported as a deletion, never a directory removed with
nothing absorbing it.* The second half is false. It reasons only about a span
holding an OPENER. A span holding a MARKER is the other case, and it runs the
other way.

**Executed** against a repository whose `docs/x.md` opens a code span on one
line, carries `<!-- specs/1700000042-quoted -->` on the next and closes the
span on the third, with that work item's directory present and nothing having
absorbed it:

```
folded_items -> ['1700000042-quoted']
settle --retire -> exit 0 · removed seal/specs/1700000042-quoted/
                          retired 1 work items; 0 kept
```

The directory is gone. That is round 1's finding 1 of the parent chain, whole,
in a door nobody has named.

**It is not a regression.** The base's `folded_items` answers the same set —
I ran both. A multi-line span was never blanked, so this diff neither opens
the door nor closes it. What the diff adds is the sentence saying the door
cannot exist, in the place `questions.md` Q2 decided the answer would live.

**And the grounds are false at this SHA.** `spec.md` §*Scope*, Out, and
`plan.md` §*Technical context* both rest on *a shape this repository has never
carried*. Measured over the eight top-level `docs/` documents after fence
blanking: **fourteen multi-line code spans, in six documents** —
`branch-and-release.md`, `issues-and-milestones.md`, `release-checklist.md`,
`review-chain-spec.md` (five of them), `review-handoff-protocol.md`,
`worktree-guard-spec.md` (five). None holds a comment delimiter or a marker,
so nothing is at risk now. But the reason nothing is at risk is *none of them
holds one*, not *the shape does not occur*, and `docs/` is the one directory
`folded_items` reads.

## 🟡 3 · An indented code block is a third way a line is not live, and `coordinates` reads through it

`skills/settle/scripts/settle.py#coordinates`, the fragments loop.

`blank_fences` knows the two fenced forms and nothing else. Markdown's other
quotation is the indented code block, and a fragment that shows its example
row indented rather than fenced has that example counted as its own
coordinate.

**Executed** over a fragment holding one real row and one indented example:

```
{'1700000001-alpha': ['hooks/frag.py', 'hooks/quoted.py']}
```

`hooks/quoted.py` is the quotation. That is exactly finding 3's harm — *a
fragment's quoted coordinate is not the fragment's own* — through the door
`test_a_fragments_quoted_coordinates_are_not_the_fragments_own` does not
parametrise, and the case covers the fenced and the parked forms only.

`folded_items` is not reachable this way: `FOLD_MARKER` is line-anchored, so
four leading spaces already stop an indented marker matching. I confirmed
that — the indented fixture returns the empty set. The door is
`coordinates`-only, and only for coordinates.

**Pre-existing, and cheap to answer with grounds rather than code.** Widening
`blank_fences` would move `readable`, `check_text`, `round_record.py` and the
review-history guard all at once, which is the change
`tests/test_chain_hooks.py#reader_blanking_passes` exists to refuse. The
answer §12 asks for is the enumeration: `spec.md` §*The class, enumerated*
says the rule is *outside a fenced block and began outside an HTML comment*
and §*Scope*, Out lists what is deliberately left. The indented block is in
neither list, so a reader cannot tell it was considered.

## ⬜ The filter is written twice inside one function

`skills/settle/scripts/settle.py#coordinates`. The ledger loop spells it
`if not live: continue` and the fragments loop spells it `if live:`, four
lines apart. `folded_items` spells it a third way. All three call sites want
only the live lines and none reads a non-live one, so the pair `live_lines`
yields is generality nobody uses. A generator yielding the live lines alone
removes the filter from three places and the two spellings from one function.
Behaviour-neutral; worth doing while the surface is open, not worth a round.

## ⬜ The plan still records an alternative the suite now refuses

`plan.md` §*Alternatives considered*, the row for round 3's regex
`` `+[^`]*`+ ``, reads *not chosen — acceptable if the equal-length scan
proves awkward*. Since `29368ff2`'s successor planted
`test_a_code_span_closes_at_a_backtick_string_of_equal_length`, that
alternative is no longer acceptable: I applied it and two of the five shapes
go red. The case is right — see the correction answered below — and the row is
now a recorded permission the tree refuses. One clause on that row settles it.

## ⬜ A live count sits undated in a shipped docstring

`skills/settle/scripts/settle.py#coordinates` says *four rows of
`seal/ledger.md` hold* `<!--` *inside backticks with no* `-->` *on the line*,
in the present tense with no date. It is true at this SHA — I counted, lines
78, 762, 980 and 1612 — and it is a number over a file that grows at every
release fold, which is the shape `plan.md` itself cites
`skills/settle/SKILL.md` §3 for when it rejects asserting 94 sections.
`blank_code_spans`'s own paragraph does this correctly, with *Measured (NAME NOT IN TREE)
2026-09-22* in front. The same three words on this sentence.

---

## The four corrections, answered

**1 · The two-step repair of `spec.md:30` — both steps are right.** The line
now quotes `skills/verify/scripts/unverified_check.py#folded_items@7a8d3c99`
and `skills/settle/scripts/settle.py#coordinates@9b5febe4`. That row was
`@a1c78799` when this round read it; round 1's own fix pass moved the unit,
and the stamp here follows the row because the records arm reads it as a
live claim rather than as the past state this report is. I opened the
parent's fragment and both are byte-identical to the anchors S1 and S3 carry
after their re-stamp. The claims behind them are true as well, which is the
half a stamp cannot assert for itself: S1's re-read says the seventh comment
shape *reads as a fold now rather than parking every marker below it*, and the
`c-7` parametrisation is that shape and goes red when the span pass is removed;
S3's says the ids sectioned are the ids the fence-only reading sectioned, and I
reproduced that over the real corpus, extending it below from ids to segments.

**2 · The A2 divergence is the scanner's rule, and the case pins the right
thing.** HTML comments do not nest — `comment_scan` finds an opener and then
the next closer, which is what the format says — so a marker inside a draft
closes the draft with its own delimiter and the line after it is live. The
builder is right that this is `comment_scan`'s settled behaviour and not a
defect in the new rule. The case as built is worth more than the spec's
literal form: putting the draft's row before the marker satisfies A2's *Then*
exactly, and the extra assertion — that the row AFTER the marker lands in the
section that was open, with the reason beside it — pins the non-nesting rule
itself. That is the counter-intuitive half, and it is the half a later
"correction" would try to make nest.

**3 · The extra case is diligence, and the record is what needs the edit.**
A property chosen over an alternative the plan kept acceptable is precisely
the property a later simplification takes back in silence, and §15's whole
argument is that a rule with no case that can fail is not a rule. I applied
round 3's loose regex and two of the five shapes go red, so the case does what
it claims. The scope cost is real but it lands on `plan.md`, not on the code —
see the ⬜ above.

**4 · The `SyntaxWarning` is pre-existing.** `tests/test_a_row_points_by_content.py:763`
is inside a docstring that escapes a backtick in a non-raw string. The line is
byte-identical at `3cdfd8ad`, and this branch does not touch that file at all.
Confirmed, not fixed.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 A code span holding a lone comment closer is blanked, so a closer quoted in prose stops closing a parked draft and the section marker below it is lost | `skills/verify/scripts/unverified_check.py#live_lines` | open | Executed, base against this SHA: the same six lines give `{'1700000001-alpha': ['hooks/a.py'], '1700000002-beta': ['hooks/b.py']}` at `3cdfd8ad` and `{'1700000001-alpha': ['hooks/a.py', 'hooks/b.py']}` here. New at this SHA. 0 lines in the real corpus go from live to not live, so nothing is mis-grouped today |
| 2 | 🟡 The single-line limit's stated failure direction is false: a marker inside a multi-line code span is read as a fold record and the directory is removed at exit 0 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | open | Executed: `folded_items` returns the quoted id and `settle --retire` prints `removed seal/specs/1700000042-quoted/` at exit 0. The base answers the same, so the door is pre-existing; the sentence claiming it cannot exist is new. The grounds *a shape this repository has never carried* is refuted by 14 multi-line spans in 6 top-level `docs/` documents, none holding a delimiter or a marker |
| 3 | 🟡 An indented code block is a third way a line is not live, and a fragment's indented example row is counted as the fragment's own coordinate | `skills/settle/scripts/settle.py#coordinates` | open | Executed: a fragment with one real row and one indented example answers `['hooks/frag.py', 'hooks/quoted.py']`. Pre-existing; `FOLD_MARKER`'s line anchor keeps `folded_items` out of it, which I confirmed. Named in neither §*The class, enumerated* nor §*Scope*, Out |
| ⬜ 4 | The live-line filter is spelled two ways inside `coordinates` and a third in `folded_items`; no caller reads a non-live line | `skills/settle/scripts/settle.py#coordinates` | open | Read. Behaviour-neutral simplification |
| ⬜ 5 | `plan.md` records round 3's loose regex as an acceptable alternative that the planted case now refuses | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Alternatives considered* | open | Executed: applying the loose regex reddens two of the five shapes in `test_a_code_span_closes_at_a_backtick_string_of_equal_length` |
| ⬜ 6 | An undated present-tense count of four ledger lines sits in a shipped docstring over a file that grows at every fold | `skills/settle/scripts/settle.py#coordinates` | open | Executed: the count is 4 today — lines 78, 762, 980, 1612. `blank_code_spans` dates the same kind of claim; this one does not (NAME NOT IN TREE) |
| 🟢 confirmation | The two constraints the build was held to both hold | `skills/verify/scripts/unverified_check.py` | confirmed | Executed: `comment_scan`, `strip_comments`, `blank_fences` and `readable` are byte-identical to `3cdfd8ad`. `seal/ledger.md:80`'s pinned output cannot have moved, and `tests/test_chain_hooks.py#reader_blanking_passes` is green |
| 🟢 confirmation | No work item's segment or coordinate count moves on the real corpus | `skills/settle/scripts/settle.py#coordinates` | confirmed | Executed over `seal/ledger.md` and every fragment, composed rule against the fence-only rule the base used: 0 work items differ in segment or in coordinate count. Stronger than A4, which compares the id set only |
| 🟢 confirmation | The span rule is faithful to CommonMark 6.1 in every shape tried | `skills/verify/scripts/unverified_check.py#blank_code_spans` | confirmed | Executed over ten shapes including a run of five backticks, a two-opened/three-would-close pair, a span holding a longer run, and a line that is only backticks. Every answer matches the equal-length rule, and length is preserved in all ten |
| 🟢 confirmation | The three readers of the scratch marker agree on every shape | `skills/settle/scripts/settle.py#main` | confirmed | Executed: file, directory, symlink to a file, symlink to a directory and a dangling symlink. `home_at` answers `""` for all five and `settle` says *has opted out* for exactly the two `isfile` accepts |
| 🟢 confirmation | Every case the record claims red is red, on the case named | both test modules | confirmed | Executed, six mutations applied alone and restored from a byte copy, each pattern asserted to match once, `git status` clean after each |
| 🟢 confirmation | The reader still runs at the interpreter floor | `skills/verify/scripts/unverified_check.py` | confirmed | Executed on python 3.9.6: the module imports and `blank_code_spans` and `live_lines` both answer correctly. No construct in the diff needs newer (NAME NOT IN TREE) |
| ⬜ | The `SyntaxWarning` the builder reports is pre-existing | `tests/test_a_row_points_by_content.py:763` | confirmed | Read: byte-identical at `3cdfd8ad`, and the branch does not touch that file |

## Executed probes

| What was run | Result |
|---|---|
| `blank_code_spans` over ten CommonMark shapes, length and content checked | all ten match the equal-length rule; length preserved (NAME NOT IN TREE) |
| naive against composed liveness over `seal/ledger.md`, `docs/*.md` and every `seal/ledger/*.md` | 0 lines go from live to not live; `seal/ledger.md` 787 → 761 not live |
| the fence-only rule against the composed rule, per work item, through `segment_of` | 0 work items differ in segment or coordinate count |
| `folded_items` and `settle --retire` over a marker inside a multi-line code span | `['1700000042-quoted']`; exit 0, directory removed |
| the same at `3cdfd8ad`'s reader | same set — the door is pre-existing, not a regression |
| `coordinates` over a parked draft whose closer is quoted in prose, base against this SHA | base groups correctly, this SHA attributes the row to the previous section |
| `coordinates` over a fragment holding an indented example row | the quoted coordinate is counted as the fragment's own |
| multi-line code span census over the eight top-level `docs/` documents | 14 spans in 6 documents; 0 hold a comment delimiter or a marker |
| `settle` against the marker as file, directory, symlink to file, symlink to directory, dangling symlink | `home_at` and the refusal arm agree on all five |
| the module imported and exercised on `/usr/bin/python3` 3.9.6 | `blank_code_spans` and `live_lines` both correct (NAME NOT IN TREE) |
| six mutations, each alone, against both test modules | each red on the case the record names; `git status` clean after each restore |
| the proposed fix for finding 1, plus `tests/test_chain_hooks.py` and `tests/test_a_script_says_which_interpreter_it_needs.py` | 231 passed, exit 0, and the finding-1 shape answers correctly |
| two rejected fix shapes for finding 1 | an interleaved walk reddens the single-scan pin; unconditional narrowing reddens four of five span shapes |
| the four changed files and the two test modules at the tip, in the clone | 173 passed, exit 0 |
| the broad gate — `bin/test` over the whole tree, `ruff check .`, `ruff format --check .` | **not yet** — not run by this round and not this round's to run; the sealer takes it, and this report leaves nothing blocking that spawn but findings 1 and 2 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py`'s own readers are the same class one module over | `seal/follow-up.md`, two rows (#444 and the backticked-name-in-a-comment row) — already deferred by `spec.md` §*Scope*, Out, and re-derived here as the same class | the answerers those rows already name |
| `.github/scripts/fold_ledger.py#demote`'s fence tracking | already deferred in `spec.md` §*Scope*, Out — not shipped, and its own rider says what it misreads | the same, unchanged by this work |

## Paste-ready fixes

Finding 1 — `skills/verify/scripts/unverified_check.py`. Blank only the spans
that hold an opener, so a span holding a lone closer is left as it stands.
Inside a comment nothing is markdown, so a quoted closer really does end the
draft. `comment_scan` stays the one scanner, so phase 2's pin survives.
Verified: 231 passed at exit 0 across the four modules, and the finding-1
shape answers `[True, False, True]`.

Beside `FOLD_MARKER`, a constant whose defining line carries both delimiters:

```python
OPENER = "<!--"  # the predicate below looks for this; its pair is "-->"
```

Then the blanker takes a predicate:

```python
def blank_code_spans(lines, holding=None):
    """The same lines with inline code spans blanked to spaces, indices intact.

    `holding`, when given, blanks only the spans whose text contains it.
    `live_lines` passes the comment opener and nothing else, because a span
    holding a lone closer is not a quotation the comment state may ignore:
    inside a comment nothing is markdown, so a quoted closer really does end
    the draft, and blanking it parked a real section marker.
    """
```

and, in its body, the one assignment becomes:

```python
            span = line[start : runs[closer][1]]
            if holding is None or holding in span:
                chars[start : runs[closer][1]] = " " * len(span)
            i = closer + 1
```

and `live_lines` names the predicate:

```python
    fenced = blank_fences(lines)
    began = opens_outside_a_comment(blank_code_spans(fenced, holding=OPENER))
```

The case, in `tests/test_settle_reads_before_it_removes.py` beside
`test_a_parked_marker_in_the_ledger_opens_no_section`. Red against this SHA on
the last assertion, which reports the row under `1700000003-gamma`:

```python
def test_a_closer_quoted_in_prose_still_closes_a_parked_draft(tree):
    """The span pass blanks a whole span, delimiters and all, so a draft's
    closing delimiter quoted in a row or a sentence disappeared before the
    comment state was asked and the draft never closed. Every line below it
    stopped being live, including the next real section marker, and its rows
    went to whichever section was open — round 3's finding 2 again, arriving
    through the fix for it. Inside a comment nothing is markdown, so the
    quotation is not one and the pass must leave it alone."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the quoted --> below is what closes it
        + "the draft ends with `-->` said in prose\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" in rows["1700000002-beta"], dict(rows)
    assert "hooks/after.py" not in rows["1700000003-gamma"], dict(rows)
```

Finding 2 — `skills/verify/scripts/unverified_check.py#blank_code_spans`,
replacing the paragraph that begins *The rule is CommonMark's (6.1)* from
**Single-line only** to the end of that paragraph:

```
    **Single-line only, and the limit runs both ways.** CommonMark lets a code
    span cross a line break and this blanks none of those. Where such a span
    holds a comment OPENER, the opener survives and parks the lines below it
    until a closer: fewer lines live, a fold reported as a deletion, the
    cheaper mistake. Where it holds a MARKER, the marker survives too and
    reads as a fold record although it is a quotation — `settle --retire`
    removes that directory at exit 0 with nothing having absorbed it, which is
    round 1's finding 1 in a third door and the expensive mistake. Measured
    2026-09-22: six top-level `docs/` documents carry fourteen multi-line code
    spans and none holds a comment delimiter or a marker, so nothing is lost
    now — the shape occurs here, and what keeps it harmless is that no
    instance holds one.
```

Finding 3 — `skills/settle/scripts/settle.py#coordinates`, appended to the
docstring's last paragraph, with the parametrisation below it:

```
    A THIRD quotation is out of scope and named so it is not met as a
    surprise: markdown's indented code block. `blank_fences` knows the two
    fenced forms only, so a fragment that shows its example row indented four
    spaces has that example counted as its own coordinate. Widening the fence
    reader would move `readable`, `check_text`, `round_record.py` and the
    review-history guard at once, which
    `tests/test_chain_hooks.py#reader_blanking_passes` refuses by design; the
    ledger and every fragment in this repository carry rows as tables and an
    example as a fence, so the shape is answered by convention rather than by
    the reader. `FOLD_MARKER` is line-anchored, so `folded_items` is not
    reachable this way at all.
```

```python
def test_an_indented_example_row_is_counted_and_the_reader_says_so(tree):
    """The third quotation, pinned as read rather than as fixed. `blank_fences`
    knows the two fenced forms and markdown's indented code block is neither,
    so a fragment showing its example row indented has that example counted as
    its own coordinate. The case exists so a session that widens the fence
    reader one day is told what this one decided, and why it decided it in the
    docstring instead of in the code."""
    fragments = tree / "seal" / "ledger"
    fragments.mkdir()
    (fragments / "1700000001-alpha.md").write_text(
        "| r | `hooks/frag.py#real@12345678` | read | 2026-01-01 | |\n"
        "\nAn example, indented rather than fenced:\n\n"
        "    | q | `hooks/quoted.py#thing@99999999` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))["1700000001-alpha"]
    assert "hooks/frag.py" in rows, rows
    assert "hooks/quoted.py" in rows, (
        "an indented example is read as the fragment's own coordinate; the "
        "docstring says so on purpose, so change both or neither"
    )
```

Needs a fix: yes — finding 1, a behaviour regression at this SHA, and finding 2, a false safety claim in a shipped docstring
Loses a record or crashes: yes — finding 2, a work item directory removed at exit 0 with nothing having absorbed it

Finding 3 and the three ⬜ rows can each be answered with grounds rather than
an edit. Finding 2's door is pre-existing at `3cdfd8ad` and no shape in the
tree reaches it today, which is why the second line is stated and not left for
the reader to infer from the first.

## Proof block

Opened: `skills/verify/scripts/unverified_check.py`,
`skills/settle/scripts/settle.py`, `hooks/optin.py`,
`tests/test_settle_reads_before_it_removes.py`,
`tests/test_unverified_rows_close.py`,
`tests/test_a_row_points_by_content.py` (lines 758-768, and the same at the
base), `bin/test`, `seal/ledger.md`, the eight top-level `docs/*.md`, every
`seal/ledger/*.md` fragment, this work item's `routing.md`, `spec.md`,
`plan.md`, `questions.md`, `overview.md`, `changelog.md` and
`phases/phase-1.md` through `phase-3.md`, the parent's ledger fragment
`seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`,
`CLAUDE.md`, `CONTRIBUTING.md` (the runner section), and issue #489.

Not opened, and named because a verdict here would have needed them: the
parent work item's `rounds/round-1.md`, `round-2.md` and `round-3.md` and
their reports. Their coordinates reached this round through the ticket, the
spec and the plan, which quote them; no verdict above rests on a conclusion
carried from them.

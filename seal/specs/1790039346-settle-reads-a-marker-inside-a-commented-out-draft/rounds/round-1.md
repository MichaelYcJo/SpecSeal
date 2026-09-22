# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 1

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Target SHA | dab23fcb8a0e73211cc930e08d527bd7cead5296 |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 490 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `7db75512e2c5c117663e43cd9f0816f2cdff001d..6d8ebaaee1d81431bbfc2925406b9ed62a8f611b`, 3 commits |
| Contract changes | blank_code_spans → round-3-report.md, round-3.md, round-1-report.md, round-1.md, spec.md, live_lines, pytest |
| New units | OPENER (depth 1); test_a_closer_quoted_in_prose_still_closes_a_parked_draft (depth 1); test_an_indented_example_row_is_counted_and_the_reader_says_so (depth 1) |
| Needs a fix | yes — finding 1, a behaviour regression at this SHA, and finding 2, a false safety claim in a shipped docstring |
| Loses a record or crashes | yes — finding 2, a work item directory removed at exit 0 with nothing having absorbed it |

- [x] Pass

## What this round was asked

Round 1 of the build, against the whole branch — nine commits, four source
files and the work item's records, closing the five findings review round 3 of
the parent work item deferred to #489. Spec compliance first, then quality,
with the parent's three rounds inherited and not reopened.

The class named for it was every reader of `unverified_check.py` whose answer
the new `live_lines` could change, and every shape a line can be non-live in —
enumerated by construction, because the parent's chain paid three rounds for
exactly this class arriving one door at a time. Two pinned constraints were
named as places to break it: the ledger row that fixes `strip_comments`'s
output, and the case that fixes `readable`'s two passes.

Shapes to try: a ledger row quoting a bare comment opener inside backticks,
the equal-length backtick rule at its edges, a removal reached through the new
liveness rule, the opt-out marker as a symlink, and the interpreter floor.

Four corrections were handed over: the orchestrator's own two-step repair of
`spec.md:30`, whose first step was half a repair; the builder's three
divergences, the first being a fixture the spec described in a shape HTML
comments cannot take; a case the builder added that the plan did not ask for;
and a `SyntaxWarning` the builder reported as pre-existing.

The broad gate was withheld — the sealer's one act, after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 A code span holding a lone comment closer is blanked, so a closer quoted in prose stops closing a parked draft and the section marker below it is lost | `skills/verify/scripts/unverified_check.py#live_lines` | **fixed** `adb5607d` | fixed at adb5607d; Executed, base against this SHA: the same six lines give `{'1700000001-alpha': ['hooks/a.py'], '1700000002-beta': ['hooks/b.py']}` at `3cdfd8ad` and `{'1700000001-alpha': ['hooks/a.py', 'hooks/b.py']}` here. New at this SHA. 0 lines in the real corpus go from live to not live, so nothing is mis-grouped today |
| 2 | 🟡 The single-line limit's stated failure direction is false: a marker inside a multi-line code span is read as a fold record and the directory is removed at exit 0 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed** `adb5607d` | fixed at adb5607d — the false sentence is corrected. The multi-line span door itself predates this branch (the base reader answers the same set) and closing it needs span state carried across lines, which no phase of this plan covers; it is in `overview.md` §*Not done*; Executed: `folded_items` returns the quoted id and `settle --retire` prints `removed seal/specs/1700000042-quoted/` at exit 0. The base answers the same, so the door is pre-existing; the sentence claiming it cannot exist is new. The grounds *a shape this repository has never carried* is refuted by 14 multi-line spans in 6 top-level `docs/` documents, none holding a delimiter or a marker |
| 3 | 🟡 An indented code block is a third way a line is not live, and a fragment's indented example row is counted as the fragment's own coordinate | `skills/settle/scripts/settle.py#coordinates` | answered | Closing it means widening `blank_fences`, which moves `readable`, `check_text`, `round_record.py` and the review-history guard at once — the change `tests/test_chain_hooks.py#reader_blanking_passes` refuses by design. Instead `coordinates`' docstring names the third quotation form and `test_an_indented_example_row_is_counted_and_the_reader_says_so` pins the decision (`adb5607d`). `folded_items` cannot be reached through this door: `FOLD_MARKER` is line-anchored, so an indented marker gives the empty set, executed; Executed: a fragment with one real row and one indented example answers `['hooks/frag.py', 'hooks/quoted.py']`. Pre-existing; `FOLD_MARKER`'s line anchor keeps `folded_items` out of it, which I confirmed. Named in neither §*The class, enumerated* nor §*Scope*, Out |
| ⬜ 4 | The live-line filter is spelled two ways inside `coordinates` and a third in `folded_items`; no caller reads a non-live line | `skills/settle/scripts/settle.py#coordinates` | answered | The proposed shape has a measured cost. Asked of the phase 2 stub, the pair form answers `[('prose', False)]` against a real `[('prose', True)]`, while a filter form answers `[]` — byte-identical to a `live_lines` that yields nothing, which weakens the very pin round 3 finding 4 asked for. And a function that answers by omission cannot be asked about one line, so the next reader writing a diagnostic copies the rule again, which is the second copy this work item exists to remove. The two spellings inside the one function are the idioms of a multi-statement body and a single-statement one; unifying them makes one of the two worse. Behaviour-neutral, so refusing costs nothing; Read. Behaviour-neutral simplification |
| ⬜ 5 | `plan.md` records round 3's loose regex as an acceptable alternative that the planted case now refuses | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Alternatives considered* | answered | corrected at `5502d230`; Executed: applying the loose regex reddens two of the five shapes in `test_a_code_span_closes_at_a_backtick_string_of_equal_length` |
| ⬜ 6 | An undated present-tense count of four ledger lines sits in a shipped docstring over a file that grows at every fold | `skills/settle/scripts/settle.py#coordinates` | **fixed** `adb5607d` | fixed at adb5607d; Executed: the count is 4 today — lines 78, 762, 980, 1612. `blank_code_spans` dates the same kind of claim; this one does not (NAME NOT IN TREE) |
| 🟢 confirmation | The two constraints the build was held to both hold | `skills/verify/scripts/unverified_check.py` | confirmed | Executed: `comment_scan`, `strip_comments`, `blank_fences` and `readable` are byte-identical to `3cdfd8ad`. `seal/ledger.md:80`'s pinned output cannot have moved, and `tests/test_chain_hooks.py#reader_blanking_passes` is green |
| 🟢 confirmation | No work item's segment or coordinate count moves on the real corpus | `skills/settle/scripts/settle.py#coordinates` | confirmed | Executed over `seal/ledger.md` and every fragment, composed rule against the fence-only rule the base used: 0 work items differ in segment or in coordinate count. Stronger than A4, which compares the id set only |
| 🟢 confirmation | The span rule is faithful to CommonMark 6.1 in every shape tried | `skills/verify/scripts/unverified_check.py#blank_code_spans` | confirmed | Executed over ten shapes including a run of five backticks, a two-opened/three-would-close pair, a span holding a longer run, and a line that is only backticks. Every answer matches the equal-length rule, and length is preserved in all ten |
| 🟢 confirmation | The three readers of the scratch marker agree on every shape | `skills/settle/scripts/settle.py#main` | confirmed | Executed: file, directory, symlink to a file, symlink to a directory and a dangling symlink. `home_at` answers `""` for all five and `settle` says *has opted out* for exactly the two `isfile` accepts |
| 🟢 confirmation | Every case the record claims red is red, on the case named | both test modules | confirmed | Executed, six mutations applied alone and restored from a byte copy, each pattern asserted to match once, `git status` clean after each |
| 🟢 confirmation | The reader still runs at the interpreter floor | `skills/verify/scripts/unverified_check.py` | confirmed | Executed on python 3.9.6: the module imports and `blank_code_spans` and `live_lines` both answer correctly. No construct in the diff needs newer (NAME NOT IN TREE) |
| ⬜ | The `SyntaxWarning` the builder reports is pre-existing | `tests/test_a_row_points_by_content.py:763` | confirmed | Read: byte-identical at `3cdfd8ad`, and the branch does not touch that file |

## Paste-ready fixes

```python
OPENER = "<!--"  # the predicate below looks for this; its pair is "-->"
```
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
```python
            span = line[start : runs[closer][1]]
            if holding is None or holding in span:
                chars[start : runs[closer][1]] = " " * len(span)
            i = closer + 1
```
```python
    fenced = blank_fences(lines)
    began = opens_outside_a_comment(blank_code_spans(fenced, holding=OPENER))
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py`'s own readers are the same class one module over | `seal/follow-up.md`, two rows (#444 and the backticked-name-in-a-comment row) — already deferred by `spec.md` §*Scope*, Out, and re-derived here as the same class | the answerers those rows already name |
| `.github/scripts/fold_ledger.py#demote`'s fence tracking | already deferred in `spec.md` §*Scope*, Out — not shipped, and its own rider says what it misreads | the same, unchanged by this work |

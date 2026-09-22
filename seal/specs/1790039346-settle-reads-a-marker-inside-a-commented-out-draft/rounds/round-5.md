# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 5

<!-- Annotated 2026-09-22, round 5's fix pass. The lines below marked `NAME NOT IN TREE` name units that pass removed: `is_block_boundary` and its lookahead, which decided where a paragraph ended and whose incompleteness removed a work item's directory, and the fuzz oracle and case `a_character_level_reading` and `test_the_scan_agrees_with_a_character_level_reading`, replaced by a reading written from the specification and a case asserting the safety direction rather than full agreement. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Target SHA | 62f58ea574427af58b4a34bec6c15f744099673d |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 490 |
| Broad gate | not yet |
| Fixes checked by | round-6 |
| Fix range | `2aade426c39c27b6be7689183432052ec18d12b3..16a56bc871edff394f430dc8caa37670e1639007`, 3 commits |
| Contract changes | none |
| New units | _liveness (depth 1); _paragraph_ends_at (depth 1); _partner_ahead (depth 1); test_no_section_of_this_repositorys_ledger_loses_a_coordinate (depth 1); a_reading_from_the_commonmark_rules (depth 1); test_the_scan_never_reads_live_what_the_format_parks (depth 1); test_every_shape_five_review_rounds_named (depth 1); test_the_three_named_markers_are_live_in_this_repositorys_ledger (depth 1) |
| Needs a fix | yes — finding 1, the span lookahead's boundary list, which reads a marker inside a commented-out draft as live and removes a work item's directory at exit 0; and finding 2, the oracle, whose boundary list is the scan's own, so the case written for this class cannot report it. |
| Loses a record or crashes | yes — finding 1, a work item's whole SDD set removed at exit 0 with nothing having absorbed it, executed on a throwaway git repository at the target SHA. |

- [x] Pass

## What this round was asked

The last round the cap allows, against the diff of round 4's fixes —
`a9447415..e0ae20c7`, seven commits — rather than the branch. Round 4's record
read `Fixes checked by: nobody`, and closing that is the job.

What that diff carries is not the fifth patch. The owner stopped the chain
after round 4 and asked for the problem to be re-derived, so round 4's
paste-ready patch was deliberately not applied: `live_lines` is now one scan
carrying fence, comment and span state together, replacing a three-pass
composition whose middle pass had to guess the comment state, and the two
functions and the case that pinned their two views are gone.

So the round was asked to judge the scan as code rather than as a diff, on
seven shapes the earlier rounds did not reach; to judge the one design
judgment the fix pass made by measurement, the block-boundary list its
lookahead stops at; to read the oracle now in the tree as an independent
implementation and say whether it is independent; and to re-derive the marker
audit over the 55 record lines the removal refused, because the marker's rule
is per line and can silence a name that is in the tree.

Two acts of the orchestrator's were handed over to be judged: the two
`spec.md` lines it settled, one marked as the frame wrote it and one corrected
as a present-tense claim that had gone false. And an instruction of the
orchestrator's that the fix pass had caught as wrong was disclosed as such.

The broad gate was withheld — the sealer's, and nothing but this round's
findings stands between it and that spawn.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The span lookahead is bounded by three block starts and markdown has more, so a comment opener at the start of the next line is swallowed as quoted text — a marker inside a parked draft reads live and `settle --retire` removes the work item's directory at exit 0 | `skills/verify/scripts/unverified_check.py#is_block_boundary` | **fixed** `12ca883d` | fixed at 12ca883d — not the round's patch, which was a sixth guess at a block model. Both readings of a line are computed — a run that does not close on its line is literal text, or it is a span reaching its partner — and a line is live only where both call it live, so a disagreement parks rather than being decided. The lookahead and its boundary list are gone as a guess and survive only as where a paragraph ends, which the measurement below forced; Executed at this SHA. Five interrupting shapes — the draft opener itself, an ATX heading, a list item, a block quote, a thematic break — each read the marker live where the module's own `comment_scan` answers *began inside*. End to end on a throwaway git repository: `folded_items` returns the quoted id, `settle --retire` exits 0 and prints `removed seal/specs/1700000042-quoted/` with the directory deleted; the backtick-free control refuses at exit 1 and keeps it; the heading shape deletes too. Corpus unmoved and no instance today — 0 lines of eleven files differ, 903 not-live, 102 marker occurrences, 85 ids, the three named markers live at 767, 992 and 1619. The paste-ready fix applies the wider set only to lines AFTER the start line, because a list item ends the paragraph above it and still holds one of its own; applied to the start line it reads `docs/worktree-guard-spec.md` and `docs/release-checklist.md` differently on four lines. With it and the oracle corrected, both modules run 183 passed exit 0, and the new case is red against the shipped reader |
| 2 | 🟡 The character-level oracle is not independent where it counts: its `ends_the_block` is `live_lines`'s own boundary list, so the fuzz cannot report finding 1's class and goes red when the scan is corrected | `tests/test_unverified_rows_close.py#a_character_level_reading` | **fixed** `12ca883d` | fixed at 12ca883d — the oracle is rewritten from the format, borrowing no name and no rule from `live_lines`, and the case it feeds asserts the safety direction rather than agreement, because parking on disagreement is deliberate and agreement would forbid it; Executed. The shipped generator builds finding 1's neighbourhood in 10,763 of 40,000 documents and the fuzz reports 0 disagreements over the same 40,000 — the agreement is real for pairing, precedence and fences, and vacuous for the boundary list. Correcting `is_block_boundary` alone reddens this case and nothing else, 1 failed of 182, on documents where the scan is now right. The round 4 record's reading is right about the generator and open about the oracle (NAME NOT IN TREE) |
| 3 | 🟡 `comment_scan`'s docstring justifies the generator by a pair that no longer exists, `began` has no reader, and that false sentence is the only thing keeping a removed unit's name in `evidence-check`'s corpus | `skills/verify/scripts/unverified_check.py#comment_scan` | **fixed** `12ca883d` | fixed at 12ca883d — the sentence in `comment_scan`'s docstring that justified itself by a pair that no longer exists; Read and executed. `strip_comments` is the only caller in the repository and discards the first element of every tuple; the case beside it was renamed to say the pair is gone. Reword the sentence so it drops the name and the records arm goes from `0 refused` to 24 NOT-IN-TREE refusals at exit 2 across both live work items. The paste-ready fix keeps the name and makes the sentence true; a row is anchored on the unit, so the edit drifts it and `evidence-check --reverify` recomputes |
| ⬜ 4 | The corrected anchor list names five anchors and the fragment carries six — the row anchored on `OPENER` is a constant, not a case | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Data & interfaces* | **fixed** `16a56bc8` | fixed at 16a56bc8 — the anchor list was one short and had gone false a second time; it now names the helpers the two readings are built from; Read against the fragment's anchor column. All five named anchors are there and every remaining row is a case except the one on `OPENER`. The correction itself was the right call — the old list named a unit this range removed, and a present-tense claim that has gone false is corrected rather than marked. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ 5 | A6's note is an HTML comment at the end of a table row, so every rendered view shows a live acceptance criterion with nothing beside it | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | **fixed** `16a56bc8` | fixed at 16a56bc8 — A6 says in the cell that it is retired, so a rendered view no longer shows a live acceptance criterion with its note invisible; Read. Keeping the row as the frame wrote it is right and matches the repository's own rule about marking rather than deleting; what the note does not do is reach a reader of the rendered spec, which is the document a sealer checks the build against. Saying it in the cell renders; the comment then carries only what the checker needs. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ | The blank-line span reset in `live_lines` is unreachable, and the oracle's equivalent resets on a different condition | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Instrumented and executed over 60,000 generated documents and every `.md` file in the tree: never reached. The lookahead refuses a span whose partner sits past a boundary and a blank line is one, so the state it guards cannot arise. Harmless; named so the next reader does not take it for a live rule |
| ⬜ | `FENCE_RE` reads a line whose info string carries backticks as a fence opener where CommonMark reads a paragraph | `skills/verify/scripts/unverified_check.py` | confirmed | Read. The consequence is that lines below are parked — a fold record unread, a directory kept, a deletion reported at exit 1, which a person sees. `blank_fences` has read it this way since before this branch and `live_lines`'s docstring forbids moving one without the other |
| ⬜ | A stamp on a round report is tracked as a live claim, so a record states a value that did not exist at its own `Target SHA` | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md` | confirmed | Confirmed as asked rather than reopened. Executed at this SHA: `git merge-base --is-ancestor 281308c7 7f2d6f1c` exits 1. Its home is `seal/follow-up.md` and not this branch |
| 🟢 confirmation | The marker audit is right — nine silenced names are in the tree, every one still covered, and no record line claims a removed unit without a marker | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/` | confirmed | Re-derived rather than carried, over the 18 files per work item the records arm actually reads. Markers silence 11 distinct compound names here and exactly nine are names the tree carries; each is still read on at least one unmarked claim line, the smallest cover being one. Zero names the tree lacks appear on an unmarked claim line, in either live work item |
| 🟢 confirmation | The comment half of the scan is not a second guess — it agrees with `comment_scan` wherever markdown cannot change the answer | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed: 40,000 generated documents carrying comment delimiters, markers, table rows, headings and bullets and no backticks or fences — 0 documents where the two readings differ on any line |
| 🟢 confirmation | The fence half and the precedence pair hold on every shape I could build | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed, ten shapes: a fence opened inside a comment, a comment opened inside a fence, a `~~~` fence not closed by a ``` one, four backticks not closed by three then one, a run at the start of a line decided as a fence, a span opened on the last line, and an unclosed fence, comment or span at end of file. Each answers the way the docstring's table says |
| 🟢 confirmation | A multi-line span inside a table cell is correctly refused | `skills/verify/scripts/unverified_check.py#is_block_boundary` | confirmed | Read and executed. GFM parses a row's cells independently, so a backtick run on a table row reaches for nothing, and the start-line arm of the boundary test is what enforces it. This is the one question the start-line arm is right about |
| 🟢 confirmation | The `settle.py` half of the range is docstring only, and the docstring is true | `skills/settle/scripts/settle.py#coordinates` | confirmed | Read the whole diff for that file across the range: 26 lines, all prose. It names one scan carrying three states, which is what the code does, and hands the reasoning to `live_lines`'s own docstring rather than keeping a second copy |
| 🟢 confirmation | Both modules are green at this SHA before anything is touched | the two affected modules | confirmed | Executed in a clone at the target SHA: 182 passed, exit 0, read with `echo $?` and not through a pipe |
| ❓ out of verified scope | Whether the repository's full suite, the repository-wide lint and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports five modules at 397 passed exit 0, `evidence_check.py --strict .` at exit 0 with 0 refused, 0 drifted and 0 broken, and `survivor-check` at exit 0, all at this SHA; this round did not re-run them and does not certify them. The caller answers it |

## Paste-ready fixes

```python
# A line that starts a leaf block of its own. The paragraph above it has
# ended, so a backtick run in that paragraph cannot reach past it for a
# partner. `is_block_boundary` answers a DIFFERENT question — may a span
# start on this line — and the two are kept apart because a list item or a
# heading ends the paragraph above it and still holds a paragraph of its own:
# refusing a span that starts on one reads `docs/worktree-guard-spec.md` and
# `docs/release-checklist.md` differently, four lines, each a genuine wrapped
# span inside a bullet.
#
# The first alternative is the one that costs a directory. A line beginning
# `<!` opens an HTML block, so the comment opener on it is a real opener and
# not text quoted by a span reaching down from the line above. Read as
# quoted, the comment never opens and the marker below it reads live —
# `settle --retire` removing a work item's directory at exit 0 with nothing
# having absorbed it (round 5, finding 1; executed on a throwaway git
# repository, five interrupting shapes, every one of them deleting).
INTERRUPTS = re.compile(
    r"^ {0,3}(#{1,6}([ \t]|$)|>|[-*+][ \t]|\d{1,9}[.)][ \t]|<[!?]"
    r"|([-*_])[ \t]*(\3[ \t]*){2,}$)"
)
```
```python
        if is_block_boundary(lines[start_line]):
            return False
        for i in range(start_line, len(lines)):
            if i > start_line and (
                is_block_boundary(lines[i]) or INTERRUPTS.match(lines[i])
            ):
                return False
```
```python
def test_a_span_may_not_reach_across_a_line_that_starts_its_own_block():
    """Round 5's finding. The lookahead bounded a span by three block
    starts — blank line, table row, fence — and markdown has more. A line
    beginning a comment, a heading, a list item, a block quote or a thematic
    break ends the paragraph above it, so a backtick run in that paragraph
    cannot reach past it for a partner. Where it did, the comment opener on
    that line was read as quoted text, the comment never opened, and a marker
    inside the commented-out draft read live — `settle --retire` removing the
    work item's directory at exit 0 with nothing having absorbed it.
    """
    opener, closer = "<!" + "--", "--" + ">"
    marker = f"{opener} specs/1700000042-quoted {closer}"
    draft = f"{opener} a draft with `code` in it"
    for interrupter in (None, "## A heading", "- a bullet", "> quoted", "---"):
        lines = ["prose with a stray ` backtick"]
        if interrupter is not None:
            lines.append(interrupter)
        lines += [draft, marker, "more prose"]
        live = [flag for _, flag in uc.live_lines(lines)]
        assert live[lines.index(marker)] is False, (interrupter, live)
```
```python
    def interrupts_a_paragraph(line):
        """A line that starts a leaf block of its own. The paragraph above it
        has ended, so an inline span cannot reach past it — which is what a
        comment opener at the start of the next line relies on. Derived from
        the block rules, NOT from the reader this oracle judges: the boundary
        list was the one part of this reading copied from `live_lines`, and
        while it was, this case agreed with the scan on the shape that
        removed a directory (round 5, finding 2).
        """
        if len(line) - len(line.lstrip(" ")) > 3:
            return False
        s = line.lstrip(" ")
        if not s:
            return False
        if s[0] == ">" or s[:2] in ("<!", "<?"):
            return True
        if s[0] == "#":
            n = len(s) - len(s.lstrip("#"))
            return 1 <= n <= 6 and (len(s) == n or s[n] in " \t")
        bare = s.replace(" ", "").replace("\t", "")
        if s[0] in "-*_" and len(set(bare)) == 1 and len(bare) >= 3:
            return True
        if s[0] in "-*+":
            return len(s) > 1 and s[1] in " \t"
        digits = len(s) - len(s.lstrip("0123456789"))
        return (
            1 <= digits <= 9
            and len(s) > digits + 1
            and s[digits] in ".)"
            and s[digits + 1] in " \t"
        )

    def partner_on_a_later_line(start_line, width):
        """Whether an equal-width run waits on a LATER line of the block."""
        if ends_the_block(lines[start_line]):
            return False
        for k in range(start_line + 1, len(lines)):
            if ends_the_block(lines[k]) or interrupts_a_paragraph(lines[k]):
                return False
```
```python
    One scanner, because a second copy of the walk is what `check_text`'s
    docstring spent three review rounds undoing. `strip_comments` wants the
    text and is the only caller left: `opens_outside_a_comment`, which wanted
    the state the line STARTED in, went with the three-pass composition
    `live_lines` replaced, and `live_lines` carries that state itself now. The
    pair is why this yields both halves and the first half currently reaches
    nobody — the name above is kept deliberately, because it is the only
    mention outside the records, and dropping it refuses 24 record lines at
    exit 2 (round 5, finding 3).

    Why the state cannot be read off the text: a fold marker IS a comment, so
    a genuine one and one sitting inside a commented-out draft both come back
    with nothing kept.
```

## Executed probes

| What was run | Result |
|---|---|
| the two affected modules in a pristine clone at the target SHA | 182 passed, exit 0, read with `echo $?` and not through a pipe |
| ten adversarial shapes through the scan — fences inside comments, comments inside fences, mixed fence characters, unequal backtick runs, spans at end of file, a span in a table cell | nine answer as the docstring's table says; the tenth is finding 1 |
| five paragraph-interrupting shapes through the scan, each against `comment_scan` | the marker reads live in all five where `comment_scan` answers *began inside* |
| finding 1's document through `folded_items` and `settle --retire` on a throwaway git repository | `{'1700000042-quoted'}`, exit 0, `removed seal/specs/1700000042-quoted/`, directory deleted |
| the backtick-free control and, separately, the heading shape, through the same command | control exits 1 *nothing to retire* and keeps the directory; the heading shape exits 0 and deletes |
| the shipped fuzz generator, asked how often it builds finding 1's neighbourhood | 10,763 of 40,000 documents |
| the scan against the shipped oracle over 40,000 documents of that generator | 0 disagreements |
| `is_block_boundary` corrected, the oracle left alone, against the two modules | 1 failed of 182 — the fuzz case alone (NAME NOT IN TREE) |
| both corrected, against the two modules, with the new case added | 183 passed, exit 0 |
| the corrected reading against the shipped one over eleven corpus files | 0 lines differ; 903 not-live, 102 live marker occurrences, 85 unique ids, the three named markers live at `seal/ledger.md` 767, 992 and 1619 |
| the first, wider correction — the boundary applied to the start line too — over the same corpus | 4 lines differ in `docs/worktree-guard-spec.md` and `docs/release-checklist.md`, each a genuine wrapped span in a list item; this is why the shipped fix bounds only the lines after the start |
| the new case against the shipped reader | red, `assert True is False` on the first shape |
| `live_lines` against `comment_scan` over 40,000 documents with no backticks and no fences | 0 documents differ on any line |
| the blank-line span reset, instrumented, over 60,000 generated documents and every `.md` file in the tree | never reached |
| the marker audit re-derived over the files the records arm reads | 11 names silenced here, 9 of them in the tree, every one covered elsewhere, 0 uncovered; the other live work item: 10 silenced, 7 in the tree, 4 uncovered and correctly so |
| the removed unit's name dropped from the one docstring that still carries it, then `evidence-check --strict .` | exit 2, 24 NOT-IN-TREE refusals across both live work items, against `0 refused` before |
| `evidence-check --strict .` in the pristine clone | exit 0, `0 refused · 0 drifted · 0 external` in the records arm |
| `git merge-base --is-ancestor 281308c7 7f2d6f1c` | exit 1 — the round 2 record's stamp postdates its own `Target SHA` |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/unverified_check.py#live_lines` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | round 1's 2 — fixed |
| round-1 | `skills/settle/scripts/settle.py#coordinates` | round 1's 3 — answered |
| round-1 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Alternatives considered* | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/unverified_check.py` | round 1's 🟢 confirmation — confirmed |
| round-1 | `skills/settle/scripts/settle.py#main` | round 1's 🟢 confirmation — confirmed |
| round-1 | both test modules | round 1's 🟢 confirmation — confirmed |
| round-1 | `tests/test_a_row_points_by_content.py:763` | round 1's ⬜ — confirmed |
| round-2 | both test modules and `skills/verify/scripts/unverified_check.py` | round 2's 🟢 confirmation — confirmed |
| round-2 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/survivors.md` | round 2's ⬜ — confirmed |
| round-2 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-1-report.md:191` | round 2's ⬜ — confirmed |
| round-2 | the repository | round 2's ❓ out of verified scope — not run |
| round-3 | `skills/verify/scripts/unverified_check.py:107-110` | round 3's ⬜ 3 — fixed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md:61` | round 3's ⬜ — confirmed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:30` | round 3's 🟢 confirmation — confirmed |
| round-3 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Operational impact* | round 3's 🟢 confirmation — confirmed |
| round-4 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md:39` | round 4's ⬜ 3 — fixed |
| round-4 | `skills/verify/scripts/unverified_check.py:107-118` | round 4's 🟢 confirmation — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 and confirmed in round 4 | the orchestrator |

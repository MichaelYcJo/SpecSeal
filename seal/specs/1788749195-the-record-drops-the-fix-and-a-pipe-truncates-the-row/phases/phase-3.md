# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — phase 3

<!-- seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | c9b656d |
| Ran by | unknown — the spawn prompt named no model, and the template's rule is that a segment transcribes this value or leaves it, never sources it from its own idea of what it is |

## What this phase was asked

Name the heading in the reviewer's contract —
`skills/code-review/SKILL.md` §*Findings format*, and
`docs/review-handoff-protocol.md`'s description of what the record carries —
and pin whatever wording the suite can pin.

## What this phase found

**The contract is four documents, not two, and the two the plan named are
the two a reviewer does not read while writing a report.** A warden gets
`agents/warden.md` §Report at startup and reads the skill for the findings
format; the template and the protocol are read by whoever opens a record
afterwards. All four now carry it, each in the form it owes:

| Document | What it owes | Why that one |
|---|---|---|
| `agents/warden.md` §Report | the heading in the block of headings the reviewer is told to write | the only place a reviewer sees the report's shape as a shape |
| `skills/code-review/SKILL.md` §Findings format | that the block is the only place a fix survives the session | four paragraphs already say what a paste-ready fix IS and said nothing about where it goes |
| `templates/sdd-round.md` | the section, with its empty value | it names the record's sections for the person reading a record |
| `docs/review-handoff-protocol.md` | a row in the table of what the record carries, and the subsection it points at | it owns the format the two subcommands produce |

**One sentence in `agents/warden.md` was false and had to go, not be added
to.** It read *"`round_record.py new` copies these three tables into
`round-N.md` row for row and reads nothing else of the report"* — true when
the fenced blocks reached no file, which is what #187 measured. A reviewer
following it had every reason to describe a fix instead of fencing one.
`test_the_reviewer_is_not_told_the_report_is_read_for_tables_alone` asserts
the sentence's ABSENCE, which is the half that catches a document gaining the
correction and keeping the old line two paragraphs down.

**A presence-anywhere pin is not a pin, and mutation is what said so.** The
first version of `test_the_reviewer_is_told_where_the_paste_ready_fixes_go`
asserted `heading in document` for all four. Two of five mutations survived
it: the heading removed from `agents/warden.md`'s example block while the
prose two lines down still mentioned it, and the protocol's table row deleted
while the subsection below still carried the words. Both are exactly the
failure the pin exists to catch — the reviewer reads the block, and the table
is what a conforming tool's author reads.

Each assertion now names the FORM its document owes: `\n## Paste-ready
fixes\n` for the two that carry it as a heading, `` `## Paste-ready fixes` ``
for the skill that carries it as prose, and `| Paste-ready fixes |` for the
protocol's table row. Re-mutated, four for four red.

That is a class worth naming for the rest of this branch: a case asserting
that a string appears in a file cannot observe what its own guard removes,
because the string appears more than once and the guard removes one
occurrence.

**The heading is read out of the generator in every assertion**, the way
`test_the_wardens_report_headers_are_the_generators_constants` already reads
the table headers — one constant, five carriers, and a rename moves them
together or turns the pin red.

**What phase 4 inherits.** Nothing in the documents needs a ledger row of its
own; the rows this work item owes are about the generator's two behaviours,
and the coordinates are `round_record.py#row_cells`, `#split_cells` and
`#build`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `agents/warden.md`'s *"reads nothing else of the report"* | The same sentence, corrected: the generator takes every fenced block under two headings and reads no other prose. `test_the_reviewer_is_not_told_the_report_is_read_for_tables_alone` pins the removal so the old line cannot come back beside the new one |

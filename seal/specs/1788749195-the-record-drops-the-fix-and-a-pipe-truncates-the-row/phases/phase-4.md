# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — phase 4

<!-- seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | ca799b7 |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Write `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`, and check
them with `fold_ledger.py --check`.

## What this phase found

**Three ledger rows, and what each carries is the thing the diff cannot
show.** R1 is not the escaping — a reader can see that — but the measurement
that chose between two repairs, which exists nowhere in the code. R2 is a
decision about what a generator may CLAIM: it says the report carried no
paste-ready fix, never that none was needed, because it cannot tell those
apart. R3 is why `swallowed` reads two lists.

**Five rows in `seal/ledger.md` drifted, and none of their claims did.** The
anchors this branch changed are `SKILL.md#"## Findings format"`,
`round_record.py#build`, `#close`, `#swallowed`,
`test_the_record_is_generated.py#SECTION_TEXT` and its parametrized case.
Each citing row was re-read against the changed code before `--reverify`
touched it:

| Row | Claim | Still true because |
|---|---|---|
| axes/security | the findings format asks an OS-boundary fix to state its precondition | that paragraph is untouched; the two added paragraphs sit above it |
| R1 (`new`) | every field row is derived, a value it cannot write is refused, nothing is committed | the new section is spliced text, not a field |
| R2 (`close`) | the fix surface is measured from the range's ends, depth 2 refused, the checker cell re-derived | only how a verdict row's cells are READ moved |
| R6 (🟡/⬜) | the threshold and the note severity | the severity block is untouched |
| R9 (`## What this round was asked`) | the section sits between the field table and `## Verdicts` | the new section goes AFTER `## Verdicts`, which the template's heading order confirms |

**One row was narrowed and is corrected in place, not removed.** F1 said the
lines a fence may not cross are derived from `REPORT_TABLES`' headings and
`TERMINAL_LINES` — two constants. The heading loop now derives from
`READ_HEADINGS`. `CLAUDE.md`'s fragment rule has one exception for exactly
this, and the precedent is the previous work item's R2: the anchor still
resolves and what moved is the content inside it, so the false phrase is
struck through in `seal/ledger.md` with a pointer, and the new claim is R3 in
this work item's fragment. Removing F1 would have thrown away a correct
sentence about the row loop, which still reads `REPORT_TABLES`.

**`fold_ledger.py --check` exits 1, and it did before this branch.** Executed
on the working tree and again with the branch's changes stashed: exit 1 both
times, naming the fragments awaiting a release — which is what a feature
branch is supposed to look like. The hygiene workflow runs it on pull
requests into `main` only, so the state is the normal one and not something
this work item introduces. `evidence-check .` unscoped: 735 ok, 0 drifted, 0
broken, 0 old-format.

**One thing the ledger format forced.** A row may not contain a `path:line`
string anywhere, Notes included — the checker reads it as an old-format
coordinate. The first draft cited the eight measured rows as
`…/rounds/round-2.md:45` in its Notes and came back with two OLD-FORMAT
findings and no parsed rows; they are named by work item and round number
instead.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md`'s F1 phrase *"derived from `REPORT_TABLES`' headings and `TERMINAL_LINES`"* | Struck through in place, with a pointer to R3 of this work item's fragment, which carries the two-list claim that replaced it. The rest of F1 is unchanged and still true |

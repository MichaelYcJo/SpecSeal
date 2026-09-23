# 1790154761-folded-statements-pile-into-one-spec — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c43ffedf |
| Ran by | unknown — the spawn prompt named no value, and a segment does not source this row from its own idea of what it is |

## What this phase was asked

Add the shape rule to `skills/settle/SKILL.md` §2 only (PR #525 edits §1 and
§4): a bold rule sentence, then grounds, then one `Enforced by:` line naming
paths or `path::name`, or `nothing — <why>`; stacked markers share one
statement; the plugin ships no checker; a contradiction is review's. Add
`tests/test_a_folded_statement_names_what_enforces_it.py` binding markers with
id ≥ `SHAPE_CUTOFF = 1790154761`, with fixture cases A4–A6 each seen red and
A7 over the real `docs/`.

## What this phase found

- **Targets may be written in backticks.** Settle §2 says so and the check
  strips them. Markdown readers expect a path in backticks, and a rule that
  refused them would be refused on first use.
- **An `Enforced by:` line is one line, and six top-level documents under
  `docs/` are in the 88-column wrap limit** (`tests/test_docs_line_wrap.py#COVERED`). A
  folder naming several long targets in one of them has to name fewer, for
  example the test module rather than each case. The spec fixes the line as
  one line, and no fold has met the limit yet. The overview records this as a
  divergence to watch, not as a change.
- **Stacking was not covered by the first draft of its own case.** With the
  pre-cutoff marker on top, reading each marker as its own group gave the same
  result, so the mutation that disabled stacking stayed green. The case now
  puts the bound marker on top, and that mutation turns it red.
- **Mutations, executed one at a time and each restored from a copy kept
  outside the tree:** bold check off, count relaxed to at least one, target
  resolution off, the `::name` lookup off, the empty-reason check off, cutoff
  lowered to 0 (the real `docs/` goes red, since the 101 older statements lack
  the line), cutoff raised, stacking off, headings not ending a statement, and
  the live-line filter off. Each turned at least one case red. The settle pin
  was shown red with `skills/settle/SKILL.md` restored to `HEAD`.
- `docs/` holds no marker at or above the cutoff yet, so A7 passes over the
  real tree by reading every marker and binding none. The fixture cases carry
  the bound side.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

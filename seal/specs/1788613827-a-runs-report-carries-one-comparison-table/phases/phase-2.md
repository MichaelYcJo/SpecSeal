# 1788613827-a-runs-report-carries-one-comparison-table — phase 2

<!-- seal/specs/1788613827-a-runs-report-carries-one-comparison-table/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | ca62ada |
| Ran by | |

## What this phase was asked

`skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* gains
the run-level comparison table. The section says only what one segment's
reading is and where it goes; it must also say what a whole run's report
carries, with each row's source named, so a run's report is one shape rather
than one shape per run.

Nine rows, from the issue's own list, this run beside the last one measured.
Three sentences beside them, each pinned by a case: the tokens are counted
rather than estimated and counted the same way every time, naming the command;
a comparison against a run whose transcript covered only part of its branch
says so in the prose rather than as a column; and the table carries no verdict,
so what a row meant on one branch goes in the comment beside it. The section
also has to say plainly what the table is for, in its own terms — the reading
it holds is the run's, where everything else there is one segment's — and that
both go to the rolling log the section already names rather than to a third
place.

Four constraints came with it. The rows and the prose name no issue number and
no milestone, because the skill ships to repositories that have neither. The
file carries no HTML comments anywhere. The section's boundaries between
`## Seal block` and `## Counterfeits (stop on sight)` are pinned, so the table
goes inside it. And the file is deliberately not added to
`tests/test_docs_line_wrap.py`'s `COVERED`.

## What this phase found

**The structural case is the one that had to be written differently from every
other pin in the module.** Its existing style is plain substring checks over a
whitespace-collapsed section body, which is right for prose and destroys a
table: collapsing newlines leaves one long line of pipes with no row
boundaries. `test_every_row_of_the_run_level_table_names_its_source` needs the
rows as rows, so the module now carries a second reader, `section_text()`,
which keeps the lines, and a `run_table_rows()` helper that parses the table
under `| Row | Taken from |` into `[label, source]` pairs. That is not a
comment-stripping reader — `test_skill_has_no_html_comments_at_all` still holds
the premise that a substring match means "outside any comment", and both
readers lean on it.

**Nine cases, twelve mutations, and the last mutation is why the helper
asserts.** Deleting the table header alone turned five cases red, because
`run_table_rows()` cannot find its table. The helper raises an `assert` with a
message naming the header rather than letting `list.index` raise `ValueError`,
so that failure reads as "the section carries no run-level table" instead of a
traceback four frames deep.

**Two of the nine assertions were invisible in the first red run.** Every case
failed against the section as it stood, which proves each new case can fail —
but for `test_every_row_of_the_run_level_table_names_its_source` and for the
no-coverage-column assertion inside
`test_partial_coverage_is_stated_in_the_prose_and_not_as_a_column`, that red
came from the table being absent, not from the defect the assertion is about.
Both were then shown red against a table that exists: one row's source cell
emptied, and a `| Transcript coverage |` row added. A case seen red only
because its subject does not exist yet has not been seen red for its own
reason.

**For phases 3–4.** The prose the next phase must not contradict:

- `not a third destination` — the table goes to the rolling log, so
  `docs/review-handoff-protocol.md` should not read as though it names a new
  home for it.
- `Everything above measures one segment` and `this run beside the last run
  measured` — the run-versus-segment split is stated here, and phase 3's
  sentence in the handoff protocol is the other half of the same pair (the
  bars judge a segment, the table judges a run).
- The token row's source cell reads `` `session_cost.py`'s token line over the
  run's main transcript ``. `skills/commit-pr-convention/SKILL.md` naming the
  chain section's shape should point at this table rather than restate its
  rows; a second copy of nine rows is a second thing to keep in step.
- The counting rule names all three `usage` fields verbatim, so a phase that
  rewords it will trip `test_the_tokens_are_counted_rather_than_estimated`.

`skills/commit-pr-convention/SKILL.md` **is** in `tests/test_docs_line_wrap.py`'s
`COVERED` at 88 columns, unlike the two files touched here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase only adds. The section's existing text is untouched; the table and its three sentences sit after the closing timing paragraph, still inside the pinned boundaries | none |

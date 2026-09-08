# Feature Specification: every published reading carries three wrong rows

Three defects in `skills/verify/scripts/session_cost.py`, one file, one
release section. What binds them is not the file: **every per-segment reading
this repository has published carries all three**, and #145 and #149 are
scheduled to be answered off that table.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/flow.md` §*0.9.4 — the instrument, before anything reads it* | The section's own sentence. Two of these were found by taking this release line's readings, and the tickets that consume the table wait on them |
| `CLAUDE.md` §*The goal a design is chosen against* | Between a fix that leaves a wrong number silent and one that makes it visible without a person, the second wins. It is why #200 ships a printed line and not only a wider pattern |
| `skills/agent-contract/SKILL.md` §12 — *a defect belongs to a class* | #202's ticket names one reader; the file has two, and the second carries the same first-row rule |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Nothing here can fail a pull request, so the bar is the cases: each seen red, and each mutation of the change caught |

## Scope

**In.** `family` and `FAMILIES`; `token_totals`' per-message dedup; `load`'s
per-turn tuple; `token_thirds`' input filter; the context line's threshold;
the `by family` block of the printed report.

**Out.** The bands in `docs/review-handoff-protocol.md`, which are calibrated
against `tools_per_turn` and are not touched by any of this. Re-deriving the
readings already published — the transcripts still exist, and what a corrected
reading would say is #145's and #149's question rather than this work item's.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A repository's own runner is a test run | Given a call of `./bin/test`, `scripts/test.sh`, `make test` or `npm test`, when the family is taken, then it is `test` | `test_a_runner_named_by_path_is_a_test_run`, positive arm |
| A widened pattern still means something | Given `bin/testdata`, a `git log` naming the word, a ruff run, and this repository's other `bin/` scripts, when the family is taken, then none is `test` | the same case, negative arm |
| A runner named inside a document is not a run of it | Given `cat > x <<'EOF' … pytest … EOF`, when the family is taken, then it is `other` | `test_a_runner_named_inside_a_heredoc_is_not_a_run_of_it` |
| The bound on that cut is stated | Given `echo 'a << b' && pytest` and a lowercase unquoted delimiter, when the family is taken, then the cut does not fire | the same case, last two assertions |
| What the table could not name is named | Given a run where `other` leads by seconds, when the report prints, then it says so and names the slowest command charged there, grouped across pipes | `test_the_report_names_the_command_the_table_could_not` |
| That line is not furniture | Given a run where a named family leads, when the report prints, then the line is absent | the same case, second arm |
| A streamed message counts at its completed row | Given three rows sharing one `message.id` whose `output_tokens` grows, when the totals are summed, then `output` is the largest and the turn count is 1 | `test_a_streamed_message_is_counted_at_its_largest_row` |
| Row order is not assumed | Given a message whose larger row arrives first, when the totals are summed, then the larger count wins | `test_a_message_whose_rows_arrive_out_of_order_keeps_the_completed_count` |
| The dedup that was right stays right | Given one message written as three rows repeating its usage, when the totals are summed, then it is one turn and `cache_read` is not tripled | `test_a_split_message_is_still_one_turn_and_not_one_per_row` |
| The unread per-turn output is gone | Given a loaded transcript, when a turn is inspected, then it carries the stamp and the input count and nothing else | `test_load_returns_input_counts_only` |
| A third the file could not compute is not a baseline | Given a transcript whose first third overflows, when the report prints, then no context line appears | `test_a_charged_third_is_not_a_baseline_the_context_line_multiplies` |
| The suppression did not silence the line | Given a first third of 10 and a last of 100, when the report prints, then the line appears with both numbers | `test_the_context_line_still_prints_where_the_baseline_is_real` |
| A negative input count leaves the mean | Given six turns whose first three carry minus ten, when the growth is taken, then it is `[10, 10, 10]` | `test_a_negative_input_count_is_dropped_and_a_zero_is_dropped_with_it` |

## What this does not answer

The readings already published stay as they are. Every one is one re-run away
from being retaken, and what a corrected reading changes about #51's bands is
the question #145 and #149 exist to ask.

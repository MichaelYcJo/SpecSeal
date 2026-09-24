# Measuring a run — what a segment cost, and what the number means

A run is a sequence of segments, each one an agent spawned for a piece of
work. This document is the standing account of what gets measured, what the
measurement is read against, and where a reading goes so somebody can use it.

It is a policy document: it outranks the SDD set, and a work item that finds
it wrong corrects it rather than working around it.

`docs/review-handoff-protocol.md` §*After the run — the per-segment bars*
holds the bar each kind of segment is judged against, and it stays there
because it is part of what a handoff carries. This document is about the
measurement itself.

## The unit is a segment, and a segment has its own transcript

<!-- specs/1789296300-a-segments-own-wall-clock-is-in-no-column -->
**A spawned segment is measured from its own transcript, not from the
parent's columns.** The parent sees a spawn go out and a result come back;
what happened in between is a session of its own, with its own turns, its own
gaps and its own wall clock. A segment named by matching its transcript's
opening stamp against a spawn's result stamp is a **join**, and a join is
asserted rather than assumed — a match within a tolerance is a claim about
which transcript belongs to which spawn, and an unasserted one silently
attributes one agent's cost to another.
Enforced by: tests/test_session_cost.py::test_each_spawned_segment_is_named_by_the_spawn_it_opened_at, tests/test_session_cost.py::test_a_segment_opening_outside_the_tolerance_is_named_by_nobody

<!-- specs/1788908215-the-orchestrator-is-measured-by-the-whole-session -->
**An orchestrator measured by its whole session is measured by its
children.** A session that spawns agents contains their durations, so the
orchestrator's own row reads as the sum of everything it delegated. The
transcript is sliced into spawn cycles and each reported as its own segment,
carrying the same numbers a spawned row carries, so an orchestrator row can
sit beside them — and **the delegated interval is excluded from the
orchestrator's model time and reported as its own number**, because time
spent waiting for another agent is not time spent thinking.
Enforced by: tests/test_session_cost.py::test_the_subagents_own_interval_is_not_charged_to_the_orchestrator, tests/test_session_cost.py::test_two_spawns_are_two_cycles_each_naming_what_it_spawned

<!-- specs/1788613827-a-runs-report-carries-one-comparison-table -->
**A run's report is one comparison table.** Tokens are summed over the
transcript given **and** every subagent transcript beneath it, so the total
is the run's rather than the parent's. One table, one shape, for every run —
a report whose shape changes between runs cannot be compared with the run
before it, which is the only thing a cost number is for.
Enforced by: tests/test_session_cost.py::test_the_token_line_sums_the_run_not_just_the_transcript_it_was_given, tests/test_a_segment_feeds_the_flow_log.py::test_the_run_level_table_carries_every_row

## What a measurement must survive, and what it must not invent

<!-- specs/1788700685-two-value-shaped-odd-rows-end-the-report -->
**A degenerate reading is reported, never divided by.** A paired call whose
request and result share a timestamp has a span of zero, and four divisions
downstream of it end the report with the span line printed and the token
block lost. A transcript mixing a zone-aware stamp with a naive one ends it
with nothing printed at all. What the meter owes is a report that survives
both; what it must not do is invent a percentage for a span of zero.
Enforced by: tests/test_session_cost.py::test_a_span_of_zero_prints_what_it_can_rather_than_dividing_by_it, tests/test_session_cost.py::test_a_naive_stamp_does_not_end_the_report

<!-- specs/1788873620-two-in-range-values-make-one-that-is-not -->
**Two in-range values can make one that is not.** Every site converting a
number for display is enumerated from the module's own source, with
membership decided by running the code rather than by a list of names, and
each one is discharged — by a guard, or by an operand that cannot be a
derived number. A list of names goes stale the moment somebody adds a site;
an enumeration from the source cannot.
Enforced by: tests/test_a_derived_number_reaching_an_int_carries_a_guard.py::test_every_int_conversion_in_the_module_is_discharged, tests/test_a_derived_number_reaching_an_int_carries_a_guard.py::test_an_unguarded_conversion_added_to_the_module_is_named

<!-- specs/1788904490-every-published-reading-carries-three-wrong-rows -->
**A reading that was published is still wrong after it is published.** Three
defects in one meter put a wrong row into every reading it had ever produced
— a family classification, a per-message deduplication, and an input filter.
Correcting the code does not correct the readings, and re-deriving them is
its own work: what the correcting work item owes is to say which published
numbers are affected, so nobody reasons from them in the meantime.
Enforced by: nothing — a session's act: saying which published readings a
correction affects is written by the correcting work item, and review reads it.

<!-- specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is -->
**A refusal names the cut its row ends at, not the event it went looking
for.** A head row's cut is the first spawn's *start*, so a head call can
outlive its own row's cut and end before any spawn's result — and a refusal
naming the result as the cause pointed at a call the transcript does not
contain. A refusal that prints two sums rather than their difference leaves
the reader able to see which of the two is wrong.
Enforced by: tests/test_session_cost.py::test_a_head_call_outlives_the_cut_without_outliving_a_spawns_result

## Where a reading goes

<!-- specs/1788449488-measure-what-flow-finds -->
**A measurement nobody posted is a measurement nobody has.** Whichever
session watched a segment finish is the only party still holding its
transcript, so that session measures the segment and posts what it found to
the repository's rolling measurement log — by label rather than by number, so
the destination survives the log being rolled. A repository with no such log
gets nothing and is told so; the instruction is unconditional prose and the
posting is conditional on a place to post to.

Two readings are kept apart because they answer different questions: the
rolling log holds what this version's runs cost, and the durable log holds
findings that outlive a version. A repository declares its durable one with a
second label, since the instruction ships to repositories that have no such
issue at all — and **a repository that never measured and one that stopped
are told apart**, because both used to be the same silence.
Enforced by: tests/test_a_segment_feeds_the_flow_log.py::test_the_section_says_it_happens_without_asking, tests/test_a_segment_feeds_the_flow_log.py::test_the_section_names_the_post_command

<!-- specs/1790076080-every-orchestrator-rule-is-a-sentence -->
**Posting a reading is one command, and a command does not make anybody run
it.** `session-cost --segments <transcript> --post --says <path|->` posts to
the one open log its label resolves to. It refuses without `--says`, because
the numbers are the script's and what they say is the session's judgment, and
a command that wrote that sentence itself would be posting one nobody wrote.
The label is resolved rather than a number, and every state is answered: no
issue has ever carried it, or `gh` cannot run, and nothing is posted and
nothing fails; a history with nothing open, or more than one open log, is
named and posts nothing; exactly one open log takes the comment. **It never
opens a log**, because opening one is not a session's act — two sessions
finishing segments at once would both read zero and both create one. What the
command removes is the procedure a session used to reconstruct from prose;
what it cannot remove is the remembering, and the miss that started this was a
day of measurements nobody took rather than a post that failed.
Enforced by: tests/test_session_cost_post.py::test_one_open_posts_once_to_that_issue, tests/test_session_cost_post.py::test_post_without_says_refuses_and_says_where_the_reading_comes_from, tests/test_session_cost_post.py::test_no_state_ever_opens_an_issue

<!-- specs/1790076080-every-orchestrator-rule-is-a-sentence -->
**A network write only a person's typing starts is not a hook, and the list of
hook network touches does not reach it.** `CONTRIBUTING.md` counts the
plugin's network touches under *Hooks stay local and quiet*, and every
condition that list sets for another entry is shaped for a hook: an opt-in so
unrelated repositories are untouched, a throttle so it is not per session,
silence on every failure. `--post` fires on no hook and writes only when
typed, only through `gh`, and only what it was handed. What the same bullet
forbids still binds it — nothing sent may carry repository contents, paths or
prompts — so the posted body names the transcript by its file name and never
by its path. The repository owner owns that list and can overturn this.
Enforced by: nothing — no case reads it yet. A case that read `hooks/hooks.json`
for a command reaching `--post` would; the rule that the posted body carries no
path is held by `test_the_posted_body_does_not_carry_the_transcripts_path`.

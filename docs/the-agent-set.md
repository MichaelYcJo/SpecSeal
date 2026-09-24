# The agent set — who writes what, and what every agent is bound by

A work item is built by more than one party. This document is the standing
account of how the rules are split between them, what each one is allowed to
write, and what it costs to spawn one.

It is a policy document: it outranks the SDD set, and a work item that finds
it wrong corrects it rather than working around it.

## One contract every agent receives, and one definition each

<!-- specs/1788433011-every-spawn-prompt-is-retyped-from-memory -->
**The rules true of every agent live in one file every agent receives before
its first tool call, without a prompt asking for it.** A rule kept only in
whoever last wrote a spawn prompt goes missing without a trace, and it did:
one rule arrived at round 2 of a work item and round 1 ran without it,
another arrived at round 3 after two rounds had each rediscovered it, and
nothing recorded either.

**A rule that would need a per-role exception is not universal.** That is the
test the shared file applies to itself, and it is what keeps the split
honest: what is true of every agent is shared, what is one agent's own is in
that agent's definition, and an agent whose definition is silent about an act
does not take it.

**Section numbers are never reused and never re-ordered.** A prompt saying
*§3 is narrowed this round*, and a round record compared with another six
months later, both hold only while §3 still means what it meant. A retired
rule keeps its number and becomes one line naming what replaced it.
Enforced by: tests/test_every_agent_reads_the_contract.py::test_every_definition_opens_with_the_contract_line, tests/test_every_agent_reads_the_contract.py::test_a_bare_name_is_delivered_by_the_frontmatter

<!-- specs/1789081272-the-writer-of-the-contract-is-not-its-executor -->
**The party that draws a contract is not the party that executes it.** A
specification written by whoever then builds against it stops being a
contract and becomes an account of what got built, which leaves the review's
first stage comparing the work with its own description of itself. So the
frame — what the work is, how it is phased, and what only a person can decide
— is drawn by one agent, and the building is another's.

Two consequences follow from that split rather than from anybody's
preference. The builder's **first act on a drawing is to say whether it
holds**: a drawing can be wrong about the tree it describes, and the cheapest
moment to find out is before anything is spent. And the readiness and
decomposition questions belong to the frame, because they are questions about
work nobody has started.

**A subagent cannot ask anybody anything.** No question-asking tool reaches
an agent this plugin spawns, so a framer meeting a missing routing
declaration reports it rather than writing one, and the question is put by
the session that spawns the work, before the first edit.
Enforced by: tests/test_chain_check_at_the_pull_request.py::test_a_declared_framer_with_no_spec_is_refused, tests/test_chain_check_at_the_pull_request.py::test_a_spec_with_no_mark_is_refused

## What each party writes, and when

<!-- specs/1788445862-a-phase-hands-the-next-one-a-record -->
**A build phase leaves a record, the way a review round does.** What a phase
discovers reaches the next phase only if somebody retypes it into the next
spawn prompt, and it goes missing without a trace when nobody does. So a
phase writes what it was asked, what building it found that the next phase
needs, and what it removed from the tree that another phase must place —
beside the plan whose Status cell already carries the commit.

The three sections are chosen against what the diff cannot show. *What this
phase was asked* is the scope the spawn actually gave, which a later reader
cannot otherwise tell from a scope the phase invented for itself. *What it
removes* exists because one phase moved a rule into an interim home and the
next removed the interim home before the rule had reached anywhere else, and
nothing recorded that it had gone.
Enforced by: tests/test_a_phase_hands_the_next_one_a_record.py::test_smith_is_told_to_write_the_phase_record, tests/test_a_phase_hands_the_next_one_a_record.py::test_all_three_sections_exist_outside_comments

<!-- specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked -->
**A document that describes a transition is deleted when the transition is
over, and its standing rules move first.** A file whose own last instruction
is *delete this when the boxes are ticked* keeps being read as current long
after it stops being, and every sentence in it borrows the authority of the
sentences that are still true. The rules that survive move into the documents
that own their subjects, with the cases that pin them moving too rather than
being deleted — a case deleted with its document is coverage nobody decided
to give up.
Enforced by: nothing — a session's act: deleting a transition document once it
is over, after its rules and their cases have moved, is read by review.

<!-- specs/1790206436-the-runs-instruments-cost-wall-clock -->
**What an agent leaves in the scratchpad is named for the work item it
serves, so two agents alive at once cannot pick the same name.** Every agent
of one session shares one scratchpad, and a name any parallel agent would
also pick is a file somebody else can overwrite. In the 0.15.0 run four work
items ran their chains from one session: two wardens cloned into the same
directory, a third's clone had its HEAD moved by a foreign checkout for
fifty-five seconds, and two sealers wrote one capture file over each other
(#544). So the warden's clone is `<scratchpad>/<work-item-id>/round-<n>/clone`
with every probe of the round beside it, the sealer's capture carries the
work item id, and the verify skill's capture example is no longer a path
every session on the machine shares. The name lives in the definitions,
where a rule arrives by mechanism, and not in a spawn prompt, which is where
it had gone missing; one directory per work item and round is also what lets
the agent that made a leaving say that every one of them is gone.
Enforced by: tests/test_a_parallel_agent_names_its_scratch_after_the_work_item.py

## What a spawn costs

<!-- specs/1788993115-a-payload-is-written-again-on-every-spawn -->
**A spawn's payload is measurable, and it is paid on every spawn.** An
agent's definition plus every skill its own list injects plus the instruction
files the harness adds is written into the context of every segment that
agent runs, whether or not the segment has an act to apply them to. The meter
resolves a definition's own list to files and reports the composition — per
file and as a total, in bytes, characters and tokens, and split at headings —
so *this section is expensive* is a number rather than an impression.

**A section marked for one role reaches that role and no other.** The
measured instance is an orchestrator's procedure preloaded into every
implementer spawn: procedure for asking a person a question, delivered to a
party that has no way to ask anybody anything. What it cost was paid once per
spawn, and nothing in either file could say it was wrong.
Enforced by: tests/test_the_payload_meter_says_what_it_measured.py::test_the_real_tree_runs_and_names_every_shipped_agent, tests/test_the_payload_meter_says_what_it_measured.py::test_the_composition_table_counts_bytes_and_chars_per_file_and_in_total

<!-- specs/1790076080-every-orchestrator-rule-is-a-sentence -->
**The orchestrator's acts are counted, each against what delivers it.** An
agent's rules arrive by mechanism, while the orchestrator has no spawn for a
preload to attach to, so each of its acts is a sentence until something
refuses when the act did not happen. `skills/implement/orchestration.md`
tables every `##` heading carrying the `Orchestrator:` marker in both
orchestration files, and every `###` directly beneath one, against its
delivery — a command, a check, part of its parent's act, or still a sentence
with its grounds — and a test holds the table against both files from both
sides. That test reads the marker and not the meaning, so an act written
outside a marked section is counted by nobody.
Enforced by: tests/test_every_orchestrator_act_names_its_delivery.py::test_every_orchestrator_act_names_its_delivery, tests/test_every_orchestrator_act_names_its_delivery.py::test_an_act_with_no_row_is_named

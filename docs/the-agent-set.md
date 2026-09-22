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

<!-- specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked -->
**A document that describes a transition is deleted when the transition is
over, and its standing rules move first.** A file whose own last instruction
is *delete this when the boxes are ticked* keeps being read as current long
after it stops being, and every sentence in it borrows the authority of the
sentences that are still true. The rules that survive move into the documents
that own their subjects, with the cases that pin them moving too rather than
being deleted — a case deleted with its document is coverage nobody decided
to give up.

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

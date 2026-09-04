# <work-item-id> — phase <N>

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes.

It mirrors `rounds/round-N.md`'s shape (`docs/review-handoff-protocol.md`
§Files) for the build side. `docs/review-handoff-protocol.md` itself does not
cover this — its own Non-goals says "Structured handoff for one workflow
(review), nothing broader" — so this template and its wiring
(`templates/sdd-plan.md`'s pointer sentence, `agents/smith.md`, and
`skills/implement/SKILL.md`) carry it at the status `plan.md`'s own Status
column already has: a plugin convention, not a cross-tool protocol. -->

| Field | Value |
|---|---|
| Phase | <the phase number, matching `plan.md`'s Phases table> |
| Commit | <the commit that closed this phase — the same hash `plan.md`'s Status cell for this phase carries> |
| Ran by | <what ran this phase — the agent and the model, as `agent on model` · `unknown — <why>` when the session that spawned it cannot name one> |

<!-- #137: every segment of two work items was measured and posted to the
flow log, and not one of the readings says what produced it. All of them ran
on the same model, and that fact exists only in a session transcript — so the
log can answer what a segment COST and cannot answer what ran it.

`## What this phase was asked` (#119) made the scope a segment was given
durable. This row is the same class of fact about the same segment, and it
sits beside the commit for the same reason: both say what this record is a
record OF.

**The value is the spawning session's, never the segment's own.** An agent is
told what it is, so a value it writes about itself is the value it was told;
and the model is a spawn-time argument the orchestrator chose, which
`agents/*.md` pins nowhere. The spawning session is the only party that knows.

Whose row it is and whose keystrokes fill it are different questions, and
they come apart here in a way they do not for `rounds/round-N.md`. The
orchestrator both knows the answer and writes that file, so it does both. A
phase record is written by the segment that just ran, so the orchestrator
either hands the value over in the spawn prompt — and the segment transcribes
what it was GIVEN, never a value it decides for itself — or fills the row
afterwards, the reach-back `Fixes checked by` and the fix-surface rows already
make. What must not happen is the segment sourcing the value from its own idea
of what it is: that is the one filler whose answer nothing can check against
anything.

`unknown — <why>` is an answer and a bare `unknown` is not, in the shape
`nobody — <why>` already has: a session spawning through another harness may
genuinely have no name for the model, and the honest answer has to be
available or the confident one is the only one on offer. -->


## What this phase was asked

<the phase-specific content of the spawn or task that started this phase —
never the boilerplate the contract, `skills/implement/SKILL.md`, and
`agents/smith.md` already carry>

<!-- #119: neither a round record nor a build phase said what it was ASKED to
do, only what it found. A reader opening this record later, with the spawn
prompt gone, had no way to tell a scope the orchestrator actually gave this
phase from a scope the phase invented for itself. -->

## What this phase found

<what building this phase taught that `plan.md`'s Delivers/Status cells do
not capture — a design decision settled while writing the code, a constraint
discovered only by trying, anything the next phase needs and would otherwise
reach it only if the orchestrator retyped it into the next spawn prompt>

<!-- #107, #121: what a phase discovers reaches the next phase only if the
orchestrator retypes it by hand into the next spawn prompt, and it goes
missing without a trace when the orchestrator doesn't. This section is that
discovery's durable, committed home instead. -->

## What this phase removes

| Removed item | Where it must land |
|---|---|
| <what this phase's diff took out of the tree, or `none` — most phases remove nothing> | <the file or record that now owns it, or `none` if nothing needs to> |

<!-- #107's own worked example: phase 4 of an earlier work item moved a rule
out of `agents/smith.md` into an interim home; phase 5 then removed that
interim home before the rule had actually reached anywhere else, and the rule
left the repository with nothing recording that it had gone missing. `none`
is a valid row — most phases remove nothing — but a blank table is not: a
phase that took something out of the tree and left this table empty is the
same failure again, just uncaught by nobody having looked. -->

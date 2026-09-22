# The broad gate — one run, one owner

Narrow and often, broad once. The full suite, the repository-wide lint and
the typecheck are a **single act**, taken after the review rounds settle and
before a pull request is marked ready. This document is the standing account
of who takes it, what it runs, and what it is allowed to say.

It is a policy document: it outranks the SDD set, and a work item that finds
it wrong corrects it rather than working around it.

## One act, one owner, and the owner is an agent

<!-- specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it -->
**A prohibition with no holder is a prohibition every reader reasons past.**
The rule forbidding the implementer and the reviewer to run the broad gate
was written twice, in two agent definitions, and assigned the act to a party
that was not an agent — so every reader met a rule with nobody in the room to
perform it, and both readers reasoned past it. The gate belongs to an agent
whose whole procedure is that run, and the assignment lives in that agent's
own definition rather than in the shared rules, which is where the next such
assignment will live too.

That agent judges nothing. It runs the repository's broad command, reports
what the commands said, and writes the last round record's `Broad gate` cell.
A run that judges is a run whose verdict nobody can separate from its
measurement.

<!-- specs/1789034970-the-contract-is-settled-against-the-agents-that-exist -->
**A shared rule is settled against the agents that exist.** A rule kept only
in whoever last wrote a spawn prompt goes missing without a trace, and a rule
copied into two definitions goes out of step in one of them. What every agent
is bound by lives in one file every agent receives before its first tool
call; what one agent alone does lives in that agent's definition. The test a
shared rule has to pass is that no role needs an exception to it.

**A suite that is not mentioned reads as a suite that passed.** Where the act
is not yours, the handover carries the suite labelled `unverified` with its
answerer named — labelled, never omitted. Where it is yours, the same
handover carries the result instead of the label.

## What the gate runs, and how the list is kept true

<!-- specs/1789985781-the-gates-arm-list-is-maintained-by-hand -->
**Every step CI runs is either mirrored by a named arm or excluded with a
written reason. There is no third state and no silence.** An arm list kept by
hand drifts the moment somebody adds a step to the workflow, and the drift is
invisible: the gate goes green having not run what CI will. So the partition
is declared in the gate and a structural case asserts it is total — a step
name in the workflow with no classification in the gate fails the suite until
somebody classifies it. That is what makes the next arm impossible to add
silently.

<!-- specs/1789956662-the-gate-and-ci-ask-about-different-ranges -->
**The gate and CI ask about the same range, and the base is resolved once.**
A local branch name and the remote-tracking ref CI reads are two different
commits whenever the local one is behind, so a gate that resolves its base
differently from the workflow reports on a range nobody will be judged
against. The base becomes a resolved commit plus the ref it came from before
any check runs, and after that point the raw argument is read nowhere. The
order is the upstream the checkout declares, then the remote-tracking
spelling the workflow uses literally, then the ref as given.

<!-- specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for -->
**A configured command that breaks the criterion is refused before anything
runs.** The row naming the repository's broad command is read by the gate and
by nobody else until the gate runs, so a value that cannot do what the row
promises would otherwise be discovered at the one moment the run was supposed
to save. The refusal names the form, quotes the value, and shows the row
rewritten — exit 2, nothing run, the shape an absent row already takes. The
criterion for choosing a value has one owner, the template that documents the
row, and it is three rules rather than an example.

<!-- specs/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote -->
**A fenced example in a config file is not a config row.** One fence rule is
consumed by every walk of the `| Item | Value |` table — the reader, the
refusal, and the writer that locates the line it overwrites. A reader and a
writer that disagree about which line is the row leave a file two rows deep
that no command can bring into agreement, so a repair landing in the reader
alone is half a repair.

## What the runner owes the person who typed it

<!-- specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite -->
**A repository ships a command that runs its own suite, and it is cheap the
second time.** A documented incantation that resolves and installs its
environment on every call is not a missing command, it is an expensive one —
measured at 55 to 58 seconds of setup per call, on all seventeen test calls of
one segment. The environment is built once and reused; the first call pays
for it and every call after it pays for interpreter startup and nothing else.

<!-- specs/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback -->
**Every failure the runner has is a sentence, never a traceback.** The
awkward one is the environment it cannot write: the refusal that was supposed
to name the floor gets replaced by a stack trace about a directory, which
tells the reader about the directory rather than about the thing they typed.
A read-only environment directory is the operator's; the runner says what it
could not do, names the path and what it means for `git status`, and carries
on.

## A check that cannot fail is not a check

<!-- specs/1788936260-a-case-pins-what-it-actually-measures -->
**A module's arms are enumerated from its own source and each one mutated,
and the arms no case kills are reported.** Counting a module's arms by hand
produces a number that rots, and an arm nothing kills is an arm that can be
deleted with the suite staying green. That is the same rule new cases are
held to — seen red before it is committed — applied to the arms that are
already there.

<!-- specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for -->
**A check named for a property has to be able to observe that property.**
Three were not: a cell-presence loop that could not tell which shell a
consequence belonged to, a closed set of search phrases the seam case and the
sweeps each held their own copy of, and a sweep whose subject had drifted out
of its range. The repair in each case is the same shape — the thing the check
is named for becomes a value both the check and its own case read, so they
cannot drift into checking different things.

<!-- specs/1789996775-the-gate-states-what-its-own-fixes-disproved -->
**A document that its own work item's fixes disproved is corrected in the
same work item.** A docstring naming a class the command does not refuse, and
an argument whose grounds the fixes removed, are both statements a reader
acts on — and the run that disproved them is the only run that knows. A
correction made later is made by somebody who has to rediscover why, and a
correction never made is a false statement with a checker's authority behind
it.

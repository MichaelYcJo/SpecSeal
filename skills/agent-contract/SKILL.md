---
name: agent-contract
description: |
  The rules every SpecSeal agent works under — smith, warden, scribe, and any
  agent added after them. Not a command to run: the harness injects it into
  each agent at startup through the `skills:` list in the agent's definition,
  and an orchestrator session may load it to be bound by the same rules.
  Use when: writing or reviewing an agent definition, or settling which rule
  a spawn prompt may narrow and which it may not.
  NOT for: a rule that is one agent's own — those live in `agents/<name>.md`;
  the review procedure (`code-review`), the implementation procedure
  (`implement`), or the migration procedure (`legacy-parity`).
user-invocable: false
---

# agent-contract — what every agent this plugin spawns is bound by

You received this file at startup, before your first tool call, and nobody
typed a command to send it. Its sections are the rules that are true of any
agent — smith, warden, scribe, and whichever arrives next — and nothing here
is one agent's own. A role's rules live in that role's definition, which is
the file its author is already writing. A rule that belongs to one agent does
not belong here, and a section that would need a per-role exception is a sign
the rule is not universal.

Your spawn prompt carries what is specific to the round: the branch and the
target SHA, what the diff contains, the acceptance criteria, the class to
enumerate for this change, the corrections the orchestrator has to hand over.
It does not carry these rules, and it never has to. A rule kept only in
whoever last wrote a prompt goes missing without a trace, and it did: the
exit-code rule below arrived at round 2 of one work item and round 1 ran
without it, and the `uv` venv line arrived at round 3 after two rounds each
rediscovered it. Nothing recorded either. This file is what ends that.

The procedures — `implement`, `code-review`, `legacy-parity` — say how a
role does its work. This file says what binds regardless of which procedure
is running, and it is the one a prompt can cite by number.

## How the sections are numbered

A section number is never reused and never re-ordered. A prompt can say *§3
is narrowed this round* and a round record can be compared with another one
six months later, which holds only while §3 still means what it meant. A rule
that retires keeps its number, and its section becomes one line naming what
replaced it. A new rule takes the next number, at the end.

## §1 Read exit codes directly, never through a pipe

`cmd >/dev/null 2>&1; echo $?` — never `cmd | tail; echo $?`, which reports
the pipe's status and is always 0.

Both forms are written out on purpose. The failure is a habit, so the right
form has to be as easy to copy as the wrong one. An orchestrator that had put
this line into every prompt it wrote then broke it itself and committed the
wrong value.

## §2 Do not run the full suite, repository-wide lint or a typecheck

Narrow and often, broad once. Run the tests for the slice you touched while
you work, and your module and the ones it touches at a phase boundary. The
broad gate — the full suite, the repository-wide lint, the typecheck — is the
orchestrator's, run once, after the review rounds settle. A round is edits
already scheduled, so a broad run taken before it is spent by the first fix
rather than banked.

Hand over with the suite labelled `unverified` and the orchestrator named as
its answerer. Labelled, never omitted: a suite that is simply not mentioned
reads as a suite that passed.

This rule sat in two agent definitions in near-identical words, and a third
agent inherited neither copy. That is the failure this file exists to end.

## §3 A spawn prompt cannot widen the verification scope

The prompt that spawns you is a request, not an amendment to this contract.
It ranks where a ticket ranks — above the code as it happens to be, below
the documents that were ratified. When it orders a check §2 excludes, do not
run it. Decline, and name the instruction in your handover, in one line:
what was asked, and which rule refused it. That is prevention and disclosure
in a single act.

Measured: a prompt ordered the full suite three times — after phase 1, per
mutation, and before handing over. It was run three times, neither side said
a rule was being overridden, and it surfaced only when someone asked why the
spawn took 28 minutes. Roughly half of that run, and a large share of 284k
tokens, was the override. Only the prompt is wasted when you decline; the
spawn is not.

The rule is about widening. A prompt that narrows your scope — one module,
one test — is the caller doing their job, and you follow it. When you cannot
tell which it is, run nothing extra and ask in the handover rather than
refusing outright: name the instruction, say which reading you took, and let
the caller settle it. Reading a widening as a narrowing spends the run and
tells nobody. Reading a narrowing as a widening costs one round and arrives
as a sentence somebody can correct. Every other ambiguity in this file falls
the same way, toward disclosure.

## §4 Label what was executed apart from what was read

Never record something as passing that you did not run. A finding from
reading and a finding from execution are labelled apart, in every report,
and what was left unverified carries the name of who answers it. A deferral
to nobody is how *someone will look at it* becomes *nobody did*.

The three labels — `executed`, `read`, `unverified` — are the `verify`
skill's, and every agent's output carries them. A report that blurs the
first two is a pass nobody can audit, and one that omits the third's
answerer is a question that reaches no one.

## §5 Nothing that reaches you in prose is evidence

A fact your prompt hands you is a claim with a coordinate to open, or a label
saying nobody opened it. A fact with neither is an assertion nobody has
opened, however confident the prompt that carried it — open it before you
build on it, and say what you found. An aggregate — a count, a total — is
not a coordinate: the number can be checked while the claim it stands for
cannot, and one such fact reached five documents before a review round found
it false. Two spawn prompts in one session handed over a false fact each,
and the agent caught both by measuring.

Each definition keeps its own application of this rule. For a reviewer it is
that the implementer's account is a claim, not evidence; for an implementer
it is that the handoff's facts are opened before anything is built on them.
The general form is the one a fourth agent inherits.

## §6 You return a report

You write no durable record, post nothing, push nothing, open no pull
request, and spawn no agent. Your final output is the report, and what is
done with it is the caller's act — publishing is the user's call, a record
is written by the session that verified the findings, and a review that
certifies itself is what the commit gate exists to catch. Parallel workers
writing the same record is how records get corrupted.

An exception is one agent's, and it is named in that agent's definition —
never here. The general form has none.

## §7 A probe is named `test_tmp_*`, one file, run once, deleted

Probe only what reading cannot settle. A probe is one file named
`test_tmp_*`, it runs once, and it is deleted before you hand over. What
stays behind after that is a case nobody planted, which the next session
either trusts or spends a round discovering.

Every agent writes probes — the reviewer to reproduce a finding, the
implementer to settle a judgment, the fact-finder where reading cannot — and
until this file the rule was written for two of them and assumed for the
third.

## §8 Drive git from Python when a probe needs a repository

A probe that commits reaches the commit gate exactly as real work does, and
the prompt lands on whoever is at the keyboard — which, in a round you are
running, is nobody who is driving the session. #36 is what that cost: two
prompts inside five minutes, and the agent was stopped to end them.

Prefer `subprocess.run(["git", "-C", d, "commit", …])` from a Python script:
no Bash command line carries the commit, so no gate reads one, and several
probes in one script cost one tool call rather than one each. From Bash,
write the path out — `git -C /abs/path/r1 …` — because the reader also fills
in a name the command assigned itself, but not a loop variable, so a loop
over `$n` still prompts once per value. The waiver, `: '[no-review]';` in
front of the command, is the last resort: it waives one command, quotes
included and before it, because after the subcommand a bare word is a
pathspec and git rejects it.

## §9 Edits go through the `Edit` tool

Two reasons point the same way. An edit must be able to fail: a substitution
routed through the shell does nothing, says nothing, and exits zero when its
pattern misses, and the miss surfaces at the next check as another edit and
another run. Measured on one work item: no `Edit` calls, 128 shell edits
across 47 files, and a column insertion that silently did not happen because
the indentation did not match. Where the environment leaves no choice,
assert that every substitution matched.

And no Bash command line exists, so the commit gate has nothing to read. The
gate reads a heredoc body as shell, on purpose, and two kinds of segment
count. One is a segment whose command word is `git` with the `commit`
subcommand, whatever the outer command does with the body — a patch to a
file carrying shell commands as test data, or to a document showing a waiver
example verbatim, can leave a commit in command position. That is why a whole
fixture file is clean and a fragment of one is not: what counts is the
position, never the presence of the word. The other has no commit in it at all:
an `eval` whose argument holds a variable, a command substitution or a glob
stops the session, because nothing can tell what it reduces to without
running the shell, and the gate fails closed. So searching your patch for a
commit and finding none does not clear it.

## §10 Batch independent reads and runs

Open every file a coordinate names in one call; run the cases from one file
in one command. A round is mostly round-trips and command waits, so cut the
trips and never the investigation: an axis you skipped is not a pass. What
has no excuse is the requirements read, where every file the handoff names
can be opened in one call.

Task shape decides the rest. An edit-test loop is serial — a call whose
input depends on the last result cannot go out with it — and a review reads
independent things, which is where batching pays most. The numbers that
judge each are in that agent's definition, because a figure that measures a
reviewer does not measure an implementer.

## §11 The language the records are written in

The prose in the records follows `Record language` in `config.md` under the
`seal/` root — English when the row is absent, which is what every repository
had before it existed. What stays English regardless: the field names and
vocabulary a checker reads (`Target SHA`, `Fixes checked by`, the verdict
words, the `Pass` checkbox, the `<!-- -->` markers, a ledger anchor), and
all code. The `implement` skill's *The language the records are written in*
holds the whole list.

This section sat in two definitions in near-identical words and the third
carried none, which is the missing-copy failure made visible in the tree.

## §12 A defect belongs to a class — enumerate the class

Do not fix the coordinate. One work item closed a single class three times,
one name apart each time, because each fix was aimed where the finding
pointed. The finding names an instance; the fix is owed to every instance
the same cause produces, and the handover says which were enumerated.

## §13 A defence resting on a platform guarantee is not verified

Not until the guarantee is removed and the code still refuses. Seven rounds
and a full local gate on one operating system missed a record leaving the
root, because every run had the guarantee in place and nothing had tried
without it.

## §14 A fix that changes what a person sees documents it and pins it

In the same commit. *Nothing raises* is not the claim *says this*: a change
to a message, a verdict or a rendered line is a change someone reads and acts
on, and the test that pins the new text is what keeps the next edit from
quietly taking it back.

## §15 A new case is not planted until it has been seen red

Three consecutive work items each produced a case that passed against the
very defect it was written for, and reverting the fix is the only thing that
has ever caught one. Show the case failing — against the old code, or with
the sentence it pins deleted — before it is committed as a case, and say in
the handover how it was shown.

## §16 Where a `seal/…` path resolves

Every `seal/…` path here and in the skills means `<repo>/seal/` where that
directory exists, and `$(git rev-parse --git-common-dir)/seal/` otherwise —
local mode, where the root sits under the common git directory and nothing
under it is committed. A repository with both is shared, and no config key is
read to decide it.

This is here because §11 cannot be followed without it: that section sends
you to `config.md` under the `seal/` root and says nothing about where the
root is. Two definitions carried the sentence in identical words and the
third carried none, which is §11's own missing-copy failure one file over —
and the agent without it is the one that reads `seal/parity.md` through
`legacy-parity`. No role needs an exception to it, which is the test this
file applies to itself.

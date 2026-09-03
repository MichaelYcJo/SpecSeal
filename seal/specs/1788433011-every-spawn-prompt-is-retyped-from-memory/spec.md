# Feature Specification: every spawn prompt is retyped from memory

<!-- seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #107, first work item of 0.6.0. The second half of that issue — every
agent's artifact carrying what its segment was asked — moved to #119 and is
out of scope here.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` — *the goal a design is chosen against* | the contract has to reach an agent with no question asked and no path a session has to resolve; a delivery vehicle that works only when someone types the right line is the failure being fixed |
| `CONTRIBUTING.md` — *What a change to a gate must carry* | the one new test here is not a gate, but the repository's counterfeit rule still binds: it is shown red before the prose it pins lands, and the prompt budget is stated as zero |
| `docs/review-handoff-protocol.md:385` — *What every spawn prompt carries, until the definitions carry it* | that section names itself an interim home and names #107 as what ends it; this work is what lets it stop being one |
| `CLAUDE.md` — *a change writes fragments, never the shared file* | the changelog entry goes to `changelog.md` in this directory and the ledger rows to `seal/ledger/<id>.md` |

## Scope

**In.**

1. A single universal contract, holding the rules true of every agent this
   plugin spawns, in one file that every agent reads without being told to by
   a prompt. Its delivery vehicle is Q1.
2. Every agent definition — `agents/warden.md`, `agents/smith.md`,
   `agents/scribe.md` — opens with a line naming that contract, and a test
   that fails when a new agent definition arrives without one.
3. Each agent's own invariants moved into its own definition, and the
   universal ones removed from wherever they are duplicated.
4. The exit-code rule as its own sentence with the wrong form written out.
5. `docs/review-handoff-protocol.md` stops being the interim home: its §385
   becomes a pointer, and it says that a prompt carries what is specific to
   the round and nothing else.

**Out.**

- #119 — an agent's artifact recording what its segment was asked. Nothing
  here blocks it; no field is added for it and none is taken away.
- `chain_check.py` gaining a required field. That is #119's, and it is a
  change to a gate needing the argument `CONTRIBUTING.md` asks for.
- Bringing the whole of `agents/smith.md` and `agents/scribe.md` under
  `tests/test_docs_line_wrap.py`. Those files are 148 and 160 columns at their
  widest; that is a sweep, not this work item. The contract itself is written
  wrapped from its first line and goes into `COVERED` at birth, which is the
  precedent that test's own comments state.
- `agents/scribe.md` gaining `writing-style` in its frontmatter. It is the one
  agent without it and its report is prose a person reads. Noted in
  `overview.md` under *Not done*.

## The split, decided

#107's table has a right-hand column mixing two kinds of rule, and sorting
them is the substance of this work. Each row below is decided; the grounds are
what a reviewer argues with.

### Universal — the contract

| Rule | Grounds for calling it universal |
|---|---|
| Read exit codes directly, never through a pipe. `cmd >/dev/null 2>&1; echo $?`, never `cmd \| tail; echo $?` | true of anything that runs a command. Written out in both forms because the failure is a habit: the orchestrator that put this line in every prompt it wrote then broke it itself and committed the wrong value |
| Do not run the full suite, repository-wide lint or a typecheck. Hand them over labelled `unverified`, naming the orchestrator as the answerer | already duplicated near-verbatim in `agents/smith.md` and `agents/warden.md`. That duplication is the exact failure the three-layer split exists to end — a fourth agent needs a fourth copy |
| A spawn prompt cannot widen the verification scope. Decline, and name the instruction in the handover. A narrowing is the caller doing their job and is followed. When it cannot be told which it is, run nothing extra and ask in the handover | same passage, same duplication. `tests/test_broad_gate_rule.py:160` already loops over both agent files asserting the same two phrases, which is a test saying out loud that the rule has no single home |
| Label what was executed apart from what was read, and name who answers each unverified item | `verify`'s three labels. Every agent's output carries them, and `docs/review-handoff-protocol.md`'s handoff rule already addresses them to both directions |
| Nothing that reaches you in prose is evidence — a fact your prompt hands you is a claim with a coordinate to open or a label saying nobody opened it | the general form of two rules that already exist separately: the warden's *the implementer's account is a claim, not evidence*, and the smith's *a fact with neither coordinate nor label is an assertion nobody has opened*. Each definition keeps its own application |
| You return a report. You write no durable record, post nothing, push nothing, open no pull request, and spawn no agent | the general form. The warden's instances stay in `agents/warden.md`: no writes into `rounds/`, no `<git-dir>/specseal-reviewed`, and the parity mark as its one exception |
| Probes are named `test_tmp_*`, one file, run once, deleted | in `agents/scribe.md:4` today and in every warden prompt. The smith writes probes too, and nothing says so anywhere |
| Drive git from Python when a probe needs a repository, so no Bash command line carries a commit for the gate to read | in `agents/scribe.md` and `agents/warden.md` in near-identical words, with the same measured cost behind both (#36: two prompts inside five minutes, and the agent stopped to end them) |
| Edits go through the `Edit` tool. A shell substitution that misses does nothing, says nothing and exits zero; and a heredoc gives the commit gate something to read | in `agents/smith.md` and `agents/warden.md` at length. The second reason is identical in both files, down to the two kinds of segment the gate counts |
| Batch independent reads and runs | in both definitions with different measured numbers. The rule is universal; each definition keeps its own number, because 1.89 judges a reviewer and 1.08–1.17 is what an edit-test loop can give |
| The language the records are written in | `agents/smith.md:24` and `agents/warden.md:25` carry the same section in near-identical words, and `agents/scribe.md` carries none — which is the missing-copy failure already visible in the tree |
| The four method lessons: enumerate the class rather than fixing the coordinate; a defence resting on a platform guarantee is unverified until the guarantee is removed; a fix that changes what a person sees documents it AND pins it in the same commit; a new case is not planted until it has been seen red | #107's own comment says these belong *wherever the agents' method is written* rather than in each prompt. Each is true of any agent that fixes or reviews, and none is true of one of them only. Subject to Q3 |

### The warden's own — `agents/warden.md`

| Rule | Grounds for calling it one agent's |
|---|---|
| Work in a `git clone --no-local` of the repository at the target SHA, and only there. Read-only commands against the user's checkout are fine; never write in it; say plainly if that is broken | the smith must write in the user's checkout — it is the implementer — and the scribe reads a different repository entirely. A rule that forbids the smith's whole job is not universal |
| `pytest` is not installed for the system interpreter; make a `uv` venv in the clone | a fact about the clone, so it lives where the clone rule lives. It arrived at round 3 of one work item after two rounds each rediscovered it |
| The report format: the `code-review` findings shape, `file:line` on every finding, a paste-ready fix for each 🔴/🟡, the two sections, reading and execution labelled apart, `Needs a fix: no` / `Needs a fix: yes — <what>`, and a proof block | one agent's output contract. `agents/warden.md:227` already half carries it |
| On a verifying round, re-derive the previous round's closures rather than taking them | already there, and it is about a round, which only the warden has |
| Write nothing into `rounds/`, leave no review mark; the parity mark is the one it does write | the instance of the universal rule above, and the exception is the warden's alone |

### The smith's own — `agents/smith.md`

| Rule | Grounds |
|---|---|
| Frame before building: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md` and a ledger fragment before the first line of implementation | the SDD set is the implementer's |
| Mutation-test every unit added, one at a time, before handing over | only the agent that adds units can |
| Hand back what was built, what was measured, what was declined and why, the branch head SHA, and every open question with the default built to | one agent's output contract |
| Vertical slices, the design gate, the routing declaration, the 3+ Fix Rule, the commit-before-mutate rule | already there and already the smith's |

### The scribe's own — `agents/scribe.md`

| Rule | Grounds |
|---|---|
| Resolve the original checkout through `legacy-parity`'s order; a guessed original proves nothing | only the scribe reads an original |
| An absence carries its search, demonstrated against a case known to be present | already there, and pinned by `tests/test_absence_claims.py` |
| Facts with coordinates, no verdicts | the whole of its role |

## The contract's form, decided

**Numbered sections a prompt can cite.** `## §1 …` through `## §N`, one rule
per section, each with the short measured failure that bought it. Not a bare
table: this repository keeps the story beside the rule everywhere else, and a
table cell cannot hold one. Not undifferentiated prose: the point of the file
is that a prompt can say *§4 is narrowed this round* and a round record can be
compared against another one.

**A number is never reused and never re-ordered.** A round record citing §4
has to still mean §4 in six months, which is the auditability #107 says it is
buying. A retired rule keeps its number and its section becomes a one-line
tombstone naming what replaced it.

**One document, universal only, with no per-role sections.** A role's rules
live in that role's definition, which is the file a new agent's author is
already writing. Per-role sections in the contract would put two answers in
front of the question *where does this rule go*, which is the ambiguity the
three-layer split exists to remove. The contract says this at its top.

## The opening line, decided

Each agent definition opens, immediately under its `# <name>` heading and
before anything else, with one sentence naming the contract and saying what it
is. Identical in all three files except the last clause, so that a fourth
agent's author copies it without thinking:

> **Read the agent contract before your first tool call** — it carries the
> rules every agent this plugin spawns is bound by: how to read an exit code,
> what you must not run, what you must not write, and how a probe is written.
> This file adds only what is yours.

How the contract is reached — a path this sentence names, or a `skills:`
frontmatter entry that preloads it — is Q1, and it changes only this
sentence's last clause and the frontmatter. Every other decision above holds
under either answer.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A fourth agent arrives without the contract | Given a new `agents/<name>.md`, when the suite runs, then it fails naming the file and the missing line | `tests/test_every_agent_reads_the_contract.py`, shown red by adding a fixture-shaped agent file with no contract line |
| The exit-code rule is in a file, not in a memory | Given the contract, when it is read, then both forms appear — the right one and the wrong one — in one sentence | a pinned-phrase case asserting `cmd >/dev/null 2>&1; echo $?` and the piped form together, shown red by deleting either |
| A rule that lives in two agent files now lives in one | Given the broad-gate prohibition, when the tree is searched, then it is stated once, in the contract, and each definition carries only its own application | the re-pointed cases from `tests/test_broad_gate_rule.py`, which must still be able to fail |
| The interim home stops being one | Given `docs/review-handoff-protocol.md`, when §385 is read, then it points at the contract rather than restating it, and says a prompt carries what is specific to the round and nothing else | a pinned-phrase case; the existing protocol cases stay green |
| The contract is a wrapped document | Given the contract file, when `tests/test_docs_line_wrap.py` runs, then it is in `COVERED` and inside 88 display columns | that test, parametrised on the new path |
| An agent segment costs no new prompt | Given this change, when a session runs, then the number of questions put to a person is unchanged | stated in the pull request body; nothing counts interruptions |

## Data & interfaces

No schema, no endpoint, no payload. What changes shape is the set of files an
agent reads at spawn, and that set is named in the *Grounding* table above.

## Open questions → questions.md

Q1 (where the contract lives and how an agent reaches it) is the only one that
changes what phase 1 writes to disk. Q2, Q3 and Q4 change how much of phases 3
to 5 is a move rather than an addition. None of them changes the split decided
above.

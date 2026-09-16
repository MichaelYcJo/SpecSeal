# Feature Specification: who asks the routing question, and what checks the answer

<!-- seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## The three issues are one question seen from three sides

One act — a person being asked how a work item is routed — is described by
three documents that disagree about who performs it, shaped by a question that
cannot say the thing people most often want to say, and checked by nothing.

```
  #419  WHO asks it        smith.md claims the act; three other documents
                           give it to somebody else, and the party they give
                           it to has no name for the judging it already does
                              ↓ so the act moves, and the question it asks
  #88   WHAT SHAPE it takes  the two answers given most often are each three
                           decisions, and the fourth thing people say — do
                           not come back — is recorded nowhere
                              ↓ so the answer is worth reading, and nothing reads it
  #399  WHAT CHECKS it     a work item can declare a framer, draw no frame,
                           and reach the pull request with nothing noticing
```

Built apart, the same question is edited three times and the last is built
against a moving target. That has already happened once: #399's first framing
keyed a check on a path floor, two phases were built against it, and both were
thrown away.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask is the more expensive. This is why the unattended run becomes a thing a person can declare, and why the exit below states its cost in the question rather than leaving it to be discovered |
| `skills/implement/SKILL.md` §1 | One batch before the first edit — **one batch, not one question**. Two questions in one `AskUserQuestion` call is one wait, and it is what lets the shape below fit |
| `skills/implement/SKILL.md` §3 | The ladder decides which work opens a work item. The rung is recorded, never asked (#88's closing section), and this work adds no axis for it |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The new check owes a test seen red, a stated failure direction, and a prompt budget. The prompt budget is the one a passing suite cannot report on, so it is answered in the pull request body |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | Decides the name of the file that holds the broad-gate cell where no round record exists. A bare `seal.md` is the word `tests/test_one_word_one_meaning.py` exists for |
| `docs/review-chain-spec.md` | No standing waiver. Every option below moves a check or names its cost; none of them switches enforcement off |
| `agent-contract` §6 | What an agent writes is named in its own definition. The framer gaining `routing.md` is that naming changing, not a permission being assumed |

## Two levels, and the routing question lives only inside the second

A repository opts in **once**, by having `seal/` **and** the plugin installed.
Those are two separate things: `seal/` is committed, the hooks ship with the
plugin, so a contributor without the plugin has no gate running at all.

Inside an opted-in repository the ladder decides what each change owes. Its
bottom rung opens no work item and the commit takes `[no-review]`.

**Landing on the bottom rung is not *not using SpecSeal*.** It is using it and
being told this change owes nothing. An earlier reading of this work had the
two conflated, and the distinction carries the weight of everything below: the
`no work item` option added here is a person **overruling the ladder**, and the
ladder's own bottom rung is the session **agreeing with it**. The two produce
the same outcome and are not the same act, which is why the difference between
them is written into the out-of-scope section rather than left to be found.

## The measured instance, and the rule it produces

**The owner read `straight to the PR` as *call no agents at all*.** In the tree
that answer turns off `warden` alone; the answer meant needs two boxes left
empty.

This is #88's own claim happening to the person who designed the question — *a
chosen "none" and three boxes nobody read produce the same file* — and it is the
strongest evidence the issue has, because it is an observation rather than a
prediction.

The rule it produces, and it governs every label written in this work:

> **A label must name what it turns off, not where it ends.** A label that names
> a destination, where what it means is what does not run, is this defect.

And its companion, because a label is short by the harness's shape:

> **A label names the option; its description names the consequence.**
> `straight to the PR` had no description, which is where the consequence was
> supposed to be.

## Scope

### In

**1 — The question's shape.** Two questions in one `AskUserQuestion` call.
Question 1 is single-select and holds three options; question 2 is a
`multiSelect` with four boxes, meaningful only under question 1's middle
option. Every option carries a description, and the descriptions are part of
this contract rather than presentation.

**2 — The framer and the sealer leave the question.** Where a work item is
opened, both are recorded rather than asked. `Planning` is already a recorded
row; the sealer needs no row, because the `Broad gate` cell it writes is a
better record than a row saying it ran — it names a SHA, so an edit after the
run spends it.

**3 — The fourth box.** *Run end to end without stopping to ask* becomes a box,
and `routing.md` gains the row that records it. This is #88's fourth thing,
which is recorded nowhere today.

**4 — The routing batch moves to the framer**, which writes and commits
`routing.md` before its own three files, so it still precedes the first edit.
One interactive phase, which `agents/framer.md` already claims while another
party runs an earlier one.

**5 — The framer's persona becomes *gather, judge, plan*.** `questions.md`
becomes the residue, each row owing a reason the tree could not answer it.

**6 — `agents/smith.md` puts down what three other documents give away.** The
design-gate paragraph and the routing batch go; the unsound inference that a
missing frame proves none was owed goes with them.

**7 — The framer leaves a mark in the tree**, at the foot of `spec.md`, because
the existing framer mark lives in the git dir and a git dir does not travel to
CI.

**8 — The seal gets a home where no round record exists**, because decision 2
forces the sealer at the end and the `straight to the PR` path has no round
record for the cell to live on.

**9 — A check reads the declaration against the frame**, in `chain_check.py`,
with what it cannot see written beside it.

### Out, each with the reason

| Out of scope | Why |
|---|---|
| **Renaming the `Review` row's answer `straight to the PR`** | The value is machine-read vocabulary in `hooks/routing.py`, and 16 committed declarations carry it. Renaming it makes each of those unreadable, which sends the commit gate back to asking on every one. The measured defect is in the **question's label**, which is where the repair lands; the row's value stays |
| **A durable record that a person chose `no work item`** | The exit opens no directory, so the record needs a home this repository does not have. Every candidate today is either a shared file every branch appends to — which `CLAUDE.md`'s fragment rule forbids — or a commit-message convention nothing reads. This is #151's shape and it is named as a ticket of its own below |
| **A door in the other direction of the ladder** | The question appears only where the session judged a work item. Where it judged the bottom rung no question appears, so there is nothing to attach a door to, and opening one means asking on every change — a prompt budget `CONTRIBUTING.md` makes a change to a gate answer for. The existing door is that a person says so, which is a sentence rather than a mechanism |
| **Refusing a `plan.md` whose approval line is unfilled** | Measured on this tree: **61 of 71** `plan.md` files carry the unfilled placeholder, and 3 of the 11 work items declaring `Planning \| framer` are among them. A refusal on that arm goes red for nearly every honest branch, which is the reasoning `chain_check.py`'s own docstring gives for `unverified_check.py` refusing to fail on an honest open item. The arm ships as a **notice** and its promotion to a refusal is a ticket |
| **Making `Planning` required in `hooks/routing.py#parse`** | 84 committed declarations carry no such requirement, and a required row turns each of them into "not a declaration" — which re-opens the commit gate on every branch that already answered. The row becomes non-optional in what the template **instructs** and in what the framer **writes**; the parser stays lenient |
| **A fourth routing axis for the rung** | #88's closing section settles that the rung is recorded, not asked |
| **A path floor** | #399's four measurements. Do not re-propose it |
| **Giving the framer the approval** | `agents/framer.md` §*Yours is the one interactive phase* — the caller reading `plan.md` and spawning the build is the approval, and §6 withholds the spawn |
| **Thinning `.github/workflows/hygiene.yml`** | #420, next release. This work's check must not assume CI exists, which is why it goes where both callers already exist |
| **#241 — a round record for a run with no `warden`** | The seal's home problem is solved without inventing a review that did not happen. #241 stays the dependency it was |

## The question, in full

Both questions go in **one `AskUserQuestion` call**, which is one wait.

### Question 1 — single-select

| Order | Label | Description |
|---|---|---|
| 1 | **automation** | Every party runs: the framer frames it, `smith` builds it, `warden` reviews it, the sealer takes the broad run, and the pull request opens. **This is the last question — nothing stops to ask again.** |
| 2 | **per axis** | The four boxes below are the answer. |
| 3 | **no work item** | No work item is opened: no frame, no review, no seal, no `routing.md`, and this session writes the change itself. Every commit needs `[no-review]` typed in front of it, and nothing checks this change at the pull request. |

**The exit is last, and that is a decision rather than an ordering.**
`skills/implement/orchestration.md` warns that a preset makes the least-verified
path the cheapest to press. The exit is one click and it is that path, so it
sits where a reader's eye lands last, and its description states the cost.

**It is cheap to press and expensive to use**, by a mechanism that already
exists: `[no-review]` waives one command, typed in front of each, which is a
per-command price none of the other answers pays.

### Question 2 — `multiSelect`, meaningful only under *per axis*

**The order is the specification, not an incidental listing.** The first box is
a property of the run; the three below name parties, in the order they run. A
reader meeting four boxes of apparently the same kind reads the first as a
fourth party to switch on, and that separation is the cheapest defence against
it. If these are ever generated from a list, the list is what carries the order.

| Order | Box | Checked | Not checked |
|---|---|---|---|
| 1 | **run end to end without stopping to ask** | the run goes from here to its destination with nobody at the keyboard · `Automation` = `yes` | the session may come back with a question · `Automation` = `no` |
| 2 | **implement with `smith`** | spawn the subagent · `Implementation` = `smith` | **this session writes the code** · `Implementation` = `the session` |
| 3 | **review with `warden`** | the review rounds run · `Review` = `through the review chain` | **nothing reviews this code before the pull request** · `Review` = `straight to the PR` |
| 4 | **open the pull request** | push it and open one · `Destination` = `open the pull request` | **the branch is handed back, committed and unpushed** · `Destination` = `stop before the pull request` |

Each box's description carries its **unchecked** meaning, because that is the
half a label cannot say and the half the measured instance got wrong.

### The ceiling, stated where the shape is defined

`AskUserQuestion` allows at most four options per question. Question 2 sits at
exactly four, and the room was made by taking the framer and the sealer out of
the question. **It is fully spent: a fifth box breaks this shape**, and whoever
adds one is back on #88's original wall — two questions in one call, or a
preset that hides the axes.

This sentence belongs beside the shape rather than in a ticket, so the next
person meets the constraint instead of discovering it.

## The fourth row

| | Value |
|---|---|
| Row name | `Automation` |
| Answers | `yes` · `no` |

**The name and its values are the owner's, given at the approval**, and they
overturn what this section first carried — `Attendance`, with `nobody at the
keyboard` · `somebody may be asked`. `questions.md` Q1 is the row that asked,
and `plan.md`'s Alternatives table carries what each was weighed against. Three
grounds: the word is the owner's own, it is already question 1's first option
label so the button and the row read as one word, and `Attendance` reads as a
school register before it reads as *was anybody at the keyboard*. What the
shorter values cost is that `no` no longer carries its own meaning — it is
*this run may stop to ask*, never *a person did it by hand* — and that half now
lives in the template comment rather than in the value.
| Optional | yes, on the terms `Planning` and `Implementation` already have — 84 declarations in the tree carry no such row, and a required one turns each into "not a declaration" |

**It is a property of the run, not a fourth party.** The other three rows each
name somebody who does or does not run. `Automation` names neither a party nor
an agent, and its value answers the question a reader six months later actually
has: *was anybody at the keyboard.*

**Unchecked is a value, not an absence**, which is #151's lesson applied to this
row. An answered declaration always carries one of the two values, so an absent
row means the question was never asked. That is the three-state reading
`Implementation` already has, and it is what keeps a chosen `no` from being
byte-identical to a question nobody read.

**What the row buys, stated plainly so it is not mistaken for a gate.** Nothing
at the pull request can hold a run to it: a session that promised not to stop
and then stopped leaves no artifact to find. What it buys is the audit trail
#88 asks for — a run that stopped at minute thirty has now broken something a
reader can point at.

## The framer's mark

Measured: **0 of 84** work items carry any mark in `spec.md`, and
`agents/framer.md` asks for none. `smith` leaves one and `warden` writes round
records, so the framer is the only party whose work leaves no evidence that it
happened.

The existing framer mark is in the repository's git dir, written at the spawn
and read after a commit. **A git dir does not travel**, so CI cannot see it, and
the check below reads only what git carries.

The mark is one line at the foot of `spec.md`:

```
Framed <date> by <who>, before the build.
```

`<who>` takes the two values the `Planning` row takes. The shape — verb, date,
who, the moment — is the one `routing.md` and `plan.md` already use, which is
what keeps three feet-lines from becoming three conventions:

| File | Line | Who writes it |
|---|---|---|
| `routing.md` | `Answered <date> by <who>, before the first edit.` | the framer, from the batch it just asked |
| `spec.md` | `Framed <date> by <who>, before the build.` | the framer |
| `plan.md` | `Approved <date> by <who>, when smith was spawned.` | the caller, at the spawn |

**What a mark is worth, stated rather than implied.** Every mark this plugin
writes can be written by hand. These catch a session that declared an agent and
then did that agent's work itself, which is a session forgetting its own
answer, not an adversary defeating a check. `hooks/implementer.py` already says
this of its own marks and this one inherits it unchanged.

## Where the seal lands with no round record

**Measured, and mechanical.** A work item declaring `straight to the PR` prints
*nothing required* at the pull request, because the per-item walk in
`chain_check.py` returns at that arm before it reaches the broad-gate arm. And
`round_record.py seal` refuses outright, because its last-record lookup raises
when `rounds/` holds no `round-N.md`. So the seal has no home and nothing
notices its absence.

Under decision 2 that path still seals, so the frame has to say where the stamp
lands.

| | With rounds | With no rounds |
|---|---|---|
| Where the cell lives | the last `rounds/round-N.md` | `seal/specs/<work-item-id>/broad-gate.md` |
| The row | `\| Broad gate \| <sha> against <base> \|` | the same row, in a file holding that row alone |
| Who writes it | `round_record.py seal`, reached by `broad-gate --record` | the same subcommand, which picks the home from what exists |
| Who reads it | `chain_check.py`'s chain arm | `chain_check.py`'s direct arm, which prints *nothing required* today |

**The property the seal already has is kept.** The cell records the commit the
run happened at and the base it was compared against, so an edit after the run
spends it. That is the whole of what a seal asserts, and nothing about it
depends on a round having run.

**The file is named for the command that writes it**, not for the seal.
`broad-gate.md` introduces no new word: `bin/broad-gate` is the command and
`Broad gate` is the cell. A bare `seal.md` would be the word that already names
the warden's review mark, the sealer's stamp and the smith's proof block, which
is the collision `tests/test_one_word_one_meaning.py` exists for.

## What the check keys on, what it refuses, and what it cannot see

**The key is a comparison, not a derivation.** Nothing is re-judged and nothing
is counted. The answer was written down before the first edit, by the party the
routing batch asked.

> A work item whose `routing.md` declares `Planning | framer` owes a frame:
> `spec.md` and `plan.md` exist, and `spec.md` carries the framer's mark.

**Where it lives: `chain_check.py`**, beside the arms that already read
`routing.md`. Three grounds:

- the walk over every declaration the pull request adds or changes already
  exists, so this is an arm rather than a program;
- it already has **one checker and two callers** — `.github/workflows/hygiene.yml`
  in CI and `round_record.py`'s own post-write run locally — so *the check must
  not assume CI exists* is met by construction rather than by a second wiring.
  #420 thinning the workflow next release does not reach the local caller;
- `hooks/implementer-notice.py` cannot be it. It is reminder-only by its own
  design, it reads a git-dir mark that never travels, and a refusal there would
  be a fourth thing that can stop a session in a plugin whose first goal is
  verification that runs unattended.

### What it refuses

| State | Verdict |
|---|---|
| `Planning \| framer`, and no `spec.md` | **refuse** |
| `Planning \| framer`, and no `plan.md` | **refuse** |
| `Planning \| framer`, and a `spec.md` carrying no framer mark | **refuse** |
| `Planning \| framer`, and a mark reading `the session` | **refuse** — the declaration and the mark disagree, and which is true is not the check's to guess |
| a `plan.md` whose approval line is still the placeholder | **notice** — 61 of 71 measured, and a refusal that fires on nearly every honest branch teaches people to write none |
| a declaration with no rounds and no `broad-gate.md` cell, at a ready pull request | **refuse** — the seal arm |
| any of the above on a work item begun **before this work item's own id** | **notice** — the cutoff, below |

### The cutoff, and the measurement that forces it

**Measured: 11 work items declare `Planning | framer`, and 10 of them carry no
mark** — the eleventh is this one. A release pull request carries every work
item the release adds, so without a cutoff the next release into `main` is
refused for every framer-declared item in it, none of which could have written
a mark that did not exist.

The repository already has the shape for this. `chain_check.py`'s broad-gate arm
grandfathers work items begun before a constant, read off the work item's own
directory name, and prints instead of failing for them. The frame arm takes the
same mechanism with its own constant, **and the constant is this work item's
id** — every work item begun before the framer was asked for a mark prints, and
every one begun after it is judged.

This is not leniency spent to make the arm pass. It is what keeps the arm from
going red retroactively for a rule that did not exist when the work was done,
which is the failure `chain_check.py`'s own docstring names for the missing
declaration.

### What it cannot see, written beside it

- **A work item that never wrote a `routing.md`.** Outside the check entirely.
  This is the same hole `chain_check.py` already discloses about itself:
  declaring nothing is a way past, and a quieter one than `[no-review]`, which
  at least stays in the command.
- **Whether the frame is any good.** It sees three documents and a line. It
  cannot see whether the spec describes the work, and a frame drawn badly
  passes.
- **Whether the party named actually did it.** The row and the mark are both
  written by the framer, so the comparison catches a framer that forgot one of
  its own writes. What catches a session that declared `framer` and framed the
  work itself is the git-dir mark and the one line
  `hooks/implementer-notice.py` prints — locally, once per session, and never
  in CI.
- **`Planning | the session`, or an absent row.** The check makes no claim
  there. A session that framed the work itself owes nothing to this arm.
- **The ladder's rung.** Whether a work item *should* have declared a framer is
  the judgment §3 makes a person's, and #88 settled that it is recorded rather
  than asked.
- **Whether the run kept its `Automation` promise.** A session that declared
  `yes` and then asked at minute thirty leaves nothing in the
  tree. The row is an audit trail, not a gate.
- **A change that took the `no work item` exit.** It writes no file, which is
  the out-of-scope row above and the ticket named below.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the batch is one wait | Given a work item is being opened · When the routing batch is asked · Then question 1 and question 2 go in one `AskUserQuestion` call, and no later question is put to a person by the framer | a case reading `skills/implement/orchestration.md` for the one-call sentence and both question tables |
| S2 `automation` is one click | Given the person presses `automation` · Then `routing.md` carries `Automation` = `yes`, `Implementation` = `smith`, `Review` = `through the review chain`, `Destination` = `open the pull request`, and a row recording that this preset was pressed | a case parsing the documented rows out of the orchestration table |
| S3 which answer was pressed is recorded | Given two work items, one pressing `automation` and one ticking all four boxes · Then their `routing.md` files differ, in the row that says which answer was pressed | a case asserting the two derivations are not byte-identical |
| S4 `no work item` names what does not run | Given the option list · Then the exit's label names no destination, and its description names the frame, the review, the seal and the `routing.md` that do not happen, and the `[no-review]` each commit needs | a case asserting those five nouns in the exit's description |
| S5 the boxes are in the stated order | Given question 2's table · Then the property-of-the-run box is first and the three party boxes follow in the order they run, and the document says the order is the specification | a case reading the row order out of the table |
| S6 every unchecked meaning is written | Given question 2's four boxes · Then each names what its unchecked state does, in words a person reads before answering | a case asserting `this session writes the code`, `nothing reviews`, `stop before` and `may be asked` are each present |
| S7 the ceiling is stated where the shape is | Given question 2 · Then the document says it holds at most four options, that the room came from removing the framer and the sealer, and that a fifth breaks the shape | a case asserting the sentence |
| S8 the fifth row parses | Given a `routing.md` carrying `Automation` with either value · Then the declaration parses and the row is returned · Given a value outside the two · Then the row reads as unanswered and the declaration still parses | cases against `hooks/routing.py`, on the terms the `Planning` row's cases already use |
| S9 an old declaration still parses | Given any of the 84 declarations in this tree, none of which carries an `Automation` row · Then each still parses and the commit gate stays silent | a case over the committed corpus |
| S10 the framer asks and writes | Given the framer runs · Then it asks the batch, writes `routing.md` from the template, and commits it — in a command of its own — before writing its own three files | a case reading `agents/framer.md` for the ordering sentence and the separate-command clause |
| S11 the framer's persona names judging | Given `agents/framer.md` · Then its acts are gather, judge, plan, and `questions.md` is described as the residue whose every row owes a reason the tree could not answer it | a case asserting the three acts and the residue sentence |
| S12 the framer leaves a mark | Given the framer writes `spec.md` · Then the file ends with `Framed <date> by <who>, before the build.` | a case against `templates/sdd-spec.md` and `agents/framer.md` |
| S13 `smith` claims no act three documents give away | Given `agents/smith.md` · Then it names no design gate, no routing batch and no `routing.md` write, and says instead that phase 2 is the caller's spawn | a case sweeping the file for those acts |
| S14 a missing frame is not evidence | Given `agents/smith.md` · Then the sentence inferring the rung from an absent frame is gone · Given `smith` is spawned where `routing.md` declares a framer and no `spec.md` exists · Then it stops and says so rather than building | a case asserting the removed sentence's absence and the stop instruction's presence |
| S15 a declared framer with no frame is refused | Given a pull request adding a `routing.md` with `Planning \| framer` and no `spec.md` · Then `chain_check.py` exits non-zero naming the work item | a case in the chain-check module |
| S16 a frame with no mark is refused | Given the same declaration and a `spec.md` with no framer mark · Then the run exits non-zero naming the file and the line it wants | a case in the chain-check module |
| S17 the approval line is reported, never refused | Given a `plan.md` whose approval line is the unfilled placeholder · Then the run prints a notice and the exit code is unchanged | a case asserting exit 0 with the notice present |
| S18 the seal lands where no rounds exist | Given a work item declaring `straight to the PR` and a green broad run · Then `round_record.py seal` writes `broad-gate.md` rather than refusing | a case exercising the subcommand in a throwaway clone |
| S19 the direct arm reads that cell | Given the same work item at a ready pull request with no such cell · Then `chain_check.py` exits non-zero · Given the cell naming a SHA the tree can see · Then it passes | cases in the chain-check module, both directions |
| S20 what the check cannot see is written beside it | Given the new arm · Then the module states the six things it cannot see, including that a work item with no declaration is outside it | a case asserting the disclosure |
| S21 the arm does not go red retroactively | Given a work item whose id is below the cutoff, declaring `Planning \| framer` and carrying no mark · Then the run prints and the exit code is unchanged · Given the same state above the cutoff · Then it is refused | two cases, one either side of the constant |

## Data & interfaces

No schema, no endpoint, no payload. Four vocabularies change, and each is
read by a machine:

| Vocabulary | Where it is read | Change |
|---|---|---|
| `Automation` and its two answers | `hooks/routing.py` | added, optional, on the `Planning` row's terms |
| the row recording which answer was pressed | `hooks/routing.py` | added, optional |
| `Framed <date> by <who>, before the build.` | the new arm in `chain_check.py` | added, at the foot of `spec.md` |
| `Broad gate` in a file of its own | `round_record.py` writes it, `chain_check.py` reads it | a second home for an existing cell |

No existing vocabulary is renamed. That is a deliberate constraint of this work
and its reason is in the out-of-scope table: 84 committed declarations parse
under the current strings, and a rename sends the commit gate back to asking on
every one.

## The ticket this work opens rather than closes

**A durable record that a person chose `no work item`.** Choosing the exit
writes no file, so a change that took it is indistinguishable from one the
session never asked about — #151's shape exactly. It depends on a home for a
record that belongs to no work item, which this repository does not have: the
two candidates today are a shared file every branch appends to, which
`CLAUDE.md`'s fragment rule forbids, and a commit-message convention nothing
reads.

It is a separate ticket rather than a fifth phase because every other part of
this work reads or writes `seal/specs/<work-item-id>/`, and this one is defined
by there being no such directory.

## Open questions → questions.md

Four rows, one of them a person's. `questions.md` in this directory holds them,
and each carries the reason the tree could not answer it.

Framed 2026-09-16 by framer, before the build.

# Feature Specification: the guard asks once per worktree, not once per session

<!-- seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The guard's budget is unbounded in the number of worktrees, so an unattended run reaches the first creation and stops. That is a price paid against the first goal, not a neutral design choice |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The four answers this change owes: a test seen red, a stated failure direction, a prompt budget as a number, and platform honesty |
| `docs/worktree-guard-spec.md` §*B. Worktree creation* | The authority for the decision matrix this change edits. A hook change that diverges from it changes one of them knowingly, so both move |
| `docs/worktree-guard-spec.md` §*Choice sites* | Where the existing session-scoped budget lives and what its marker means. The new record sits beside it and must not be confused with it |
| `skills/agent-contract/SKILL.md` §13 | A defence resting on a platform guarantee is not verified. What this design rests on is named below and tested without the guarantee where that is possible |

## Scope

**In.**

- A creation-consent record, written by a `PostToolUse` arm when a
  `git worktree add` — or an `Agent`/`Task` call with `isolation: "worktree"`
  — has actually run.
- A `PreToolUse` read of that record at the top of the creation ladder, which
  stops the guard putting a question the session already answered.
- The `Agent`/`Task` path sharing the same record, in both directions: it
  writes one, and it reads one a Bash creation wrote.
- `docs/worktree-guard-spec.md`, the module docstring, and the changelog and
  ledger fragments.

**Out.**

- The switch direction. Nothing about `git switch` changes, and the
  `specseal-worktree-choice/{create,switch}` budget is untouched.
- The first creation of a session. It is still a question, at every site.
- The single-stream **deny** for a session with no record. It still denies and
  still steers to `git switch`.
- `[worktree-ok]` and `[shared-tree-ok]`. Neither token changes meaning, and
  neither becomes readable as consent.

## The argument this rests on, and the docstring it has to answer

`has_token`'s docstring refuses to read `[worktree-ok]` loosely, and gives the
reason: *reading this token loosely turns the guard off with nobody asked*.
`guard_worktree_creation`'s `user_ok` site says the same thing from the other
side — the token is *what a completed confirmation looks like coming back
through the guard*, so the site asks rather than allowing.

Both are correct about the token and neither is an argument against this
change, because **the evidence here is not the command text.**

| | `[worktree-ok]` | The consent record |
|---|---|---|
| Written by | whoever issues the command | the `PostToolUse` hook |
| Written when | before the question | after the answer |
| Forgeable by the model | yes — it can write the token on the first attempt | no — it would have to make a tool call reach `PostToolUse` without running |

A tool call reaches `PostToolUse` only after it ran, and a `git worktree add`
runs only if the guard's `deny` did not fire and its `ask` was answered yes.
So the record's existence is a fact about an answer a person gave, which is
exactly the evidence `has_token`'s docstring says the token is not.

What the change gives up is stated rather than left to be found: the
invariant *creating a worktree always takes one confirmation* becomes *the
first creation of a session takes one confirmation*. That is the whole of the
behaviour change, and it is the one the ticket asks for.

## What the design rests on, and what it does when the ground moves

| Rests on | If it were false | Direction |
|---|---|---|
| A `PostToolUse` payload means the tool ran | consent would be recorded for a call that never ran | **allow** — the only way this happens is a harness that fires `PostToolUse` for a blocked call, which would break every `PostToolUse` gate in this tree, not only this one |
| A hook `ask` cannot be auto-answered by the model | consent could be recorded with nobody asked | **allow**. Named in the pull request under platform honesty; it is the same standing every gate in this repository has |
| The record can be written | no record, so the next creation asks | **block** — one extra prompt, which is where a guard should fail |
| The record can be read | reads as no consent, so the creation asks | **block** — same |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The first creation is still a question | Given a session with no consent record, single-stream, When it runs `git worktree add`, Then the guard denies and steers to `git switch` | `test_the_first_creation_is_still_a_question` |
| The second costs nothing | Given a session whose `PostToolUse` recorded a creation, single-stream, When it runs `git worktree add` again, Then the guard allows | `test_a_second_creation_in_the_same_session_is_allowed` |
| Consent is per session | Given session A's record, When session B runs `git worktree add`, Then session B is denied | `test_consent_belongs_to_the_session_that_earned_it` |
| Consent is per clone | Given a record written from the main tree, When the same session creates from a linked worktree of that clone, Then the guard allows | `test_consent_follows_the_clone_not_the_worktree` |
| A `PreToolUse` call records nothing | Given no record, When the guard runs its `PreToolUse` arm on a `git worktree add`, Then no record exists afterwards | `test_the_pre_tool_use_arm_records_nothing` |
| A failed creation still records | Given a `PostToolUse` payload whose `tool_response` reports failure, When the arm runs, Then the record is written | `test_a_failed_creation_still_records_the_approval` |
| The allow is bounded | Given a record, When the command creates a worktree AND does something else, Then the guard asks rather than allowing | `test_the_allow_covers_only_a_command_that_is_nothing_else` |
| The `Agent` path shares the record | Given a record written by a Bash creation, When an `Agent` call with `isolation: "worktree"` arrives, Then the guard is silent | `test_the_agent_path_reads_the_record_a_bash_creation_wrote` |
| The `Agent` path writes the record | Given an `Agent` `PostToolUse` payload with `isolation: "worktree"`, When the arm runs, Then a later Bash creation is allowed | `test_the_agent_path_writes_the_record_bash_reads` |
| An unwritable record costs a prompt, not an outage | Given a `.git` the arm cannot write into, When a creation runs and another is attempted, Then the second still asks and nothing raises | `test_an_unrecordable_consent_asks_rather_than_crashing` |
| The switch direction is untouched | Given a consent record, When the session runs `git switch` against an active session, Then it is still denied | `test_creation_consent_does_not_reach_the_switch_direction` |

## Data & interfaces

**The record.** An empty file at
`<git-common-dir>/specseal-worktree-consent/<session-id>`. Its existence is
the whole fact, the way the choice marker beside it and `optin.py`'s
`specseal-scratch` are.

**A third directory, not a value in the existing one.** The choice marker at
`<git-dir>/specseal-worktree-choice/create/<session-id>` looks like the same
thing and is its opposite, in two ways that cannot share one file:

- it is written by `PreToolUse`, **before** the answer, and means *the
  question was put*. Sharing the file would let the guard read its own
  question back as consent — the `has_token` failure one directory over;
- the two fail in opposite directions. An unwritable choice marker counts as
  *already asked*, because one missed question beats a deny nothing gets
  past; an unwritable consent record must count as *no consent*, because the
  alternative is a guard that switches itself off when a disk is read-only.
  One file cannot fail two ways.

There is no `create`/`switch` split under it either: consent is about
creation, and the switch direction never reads it.

**Under the common git directory, not `git_dir`'s per-worktree one.** The
record stands for *this session may split this clone into worktrees*, and a
linked worktree is the same clone. Reading it through `optin.git_common_dir`
keeps one answer to that question in the tree rather than two, and it is the
same resolution `skills/agent-contract/SKILL.md` §16 already uses for the
local-mode root, for the same reason.

**No expiry.** A session id is already scoped to a session, and a time bound
on top of it can only produce one new outcome: a session that outlives the
bound is asked a second time, which is the failure this work removes. The
choice markers beside it are not pruned either.

**The decision matrix, after.** One row is added above every existing row of
§B, and no existing row is edited:

| Tree state | Decision |
|---|---|
| **a consent record for this session in this clone** | **allow**, where the tool call is worktree creation and nothing else · **ask**, where the command does more · **silent** on the `Agent`/`Task` path |
| ACTIVE session present | ask — unchanged |
| only IDLE sessions | **choice** — unchanged |
| detection unusable | **choice** — unchanged |
| `[worktree-ok]` given (Bash only) | ask — unchanged |
| single stream, **Bash** | deny — unchanged |
| single stream, **Agent/Task** | ask — unchanged |

**Why the allow is bounded.** `permissionDecision: "allow"` bypasses the
user's own permission settings for the **whole** tool call, and a
`git worktree add` is routinely written as one segment of a compound command.
The consent recorded is about worktree creation, so the guard may speak for a
command that is worktree creation and nothing else; for anything else it says
`ask`, which is one prompt about the rest of the command line rather than a
deny about the worktree. A command the lexer could not read is not vouched
for either — what it failed to read is what the allow would be covering.

**Why the `Agent`/`Task` path is silent rather than an allow.** That call is a
worktree creation *plus* an agent with a prompt, and the record is about the
first half only. Silence is the guard withdrawing its objection, which is the
whole of what the record establishes; whatever the harness wants to ask about
running the agent is not the guard's to remove.

## Open questions → questions.md

Three the ticket left open are decided here and recorded in `questions.md`
with their grounds: whether the record expires, whether a failed
`git worktree add` records consent, and what happens when the record cannot be
written.

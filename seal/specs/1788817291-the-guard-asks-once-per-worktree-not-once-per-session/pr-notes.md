# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — notes for the PR body

<!-- The four answers `CONTRIBUTING.md` §*What a change to a gate must carry*
requires, written here so the orchestrator can lift them into the pull request
body. The prompt budget is the one a passing suite cannot report on — it is
answered in the body or it is not answered. -->

## What changes, in one table

| | Before | After |
|---|---|---|
| The first `git worktree add` of a session, single-stream | deny, steered to `git switch` | unchanged |
| The second, in the same session and clone | deny, or `ask` if `[worktree-ok]` was appended | allowed, no prompt |
| The same, written as part of a compound command | deny | `ask` — about the rest of the command line |
| An `Agent` call with `isolation: "worktree"`, after a creation ran | ask | silent |
| A `git switch` in any tree state | unchanged | unchanged |

## 1. A test seen red

`tests/test_the_guard_asks_once_per_session.py` was written against the
unfixed guard and run first. **13 of its 23 cases failed and 10 passed** — the
10 are the rows this work must not move, and they are meant to pass both
before and after. The two named in the ticket are among the 13:

```
FAILED test_a_second_creation_in_the_same_session_is_allowed   assert 'deny' == 'allow'
FAILED test_consent_outranks_every_row_below_it
FAILED test_the_allow_covers_only_a_command_that_is_nothing_else
FAILED test_a_second_creation_never_denies
FAILED test_a_creation_that_ran_leaves_a_record
FAILED test_the_agent_path_reads_the_record_a_bash_creation_wrote
… 13 failed, 10 passed
```

`test_the_first_creation_is_still_a_question` is one of the 10, on purpose: a
session with no record still meets the single-stream deny.

**A red baseline is not the same as a case with something behind it**, so every
unit this branch added was then broken one at a time and the cases re-run —
**16 mutations, 16 red**. Three of them were green on the first pass and are
the reason three cases exist that were not in the original file:

| The unit broken | What it took to catch it |
|---|---|
| `granted` accepting a directory as a record | `test_a_directory_at_the_record_path_is_not_a_record` |
| `record` raising instead of failing quietly | reading the hook's **exit status and stderr**, not only its stdout — a traceback leaves stdout empty too |
| `consent_path` refusing a separator-only session id | `test_a_session_id_that_is_only_separators_has_no_record_path` |

A fourth was a condition nothing could make false — `session_id and` in front
of a call that already answers for a missing id — and it was removed rather
than pinned.

## 2. A stated failure direction

**This makes the gate allow more.** That is the cheaper mistake here, and the
paragraph the ticket cites says why in its own terms.

- **A wrong allow** costs one extra worktree folder in a session where a person
  already agreed to worktrees, in the same clone. No tree is switched and
  nothing is overwritten. The one way it happens is a session id reused across
  conversations.
- **A wrong deny** fires on *every* invocation, which is the shape the same
  paragraph singles out as an outage rather than a cost. That is what the guard
  does today for an unattended run: it reaches the first creation and stops.

The allow is bounded rather than open. `permissionDecision: "allow"` covers the
**whole** tool call, so the guard speaks only for a command that is worktree
creation and nothing else; a compound gets `ask`, and a command the lexer could
not read gets `ask` too. On the `Agent` path the guard goes silent rather than
allowing, because that call is a creation *plus* an agent with a prompt.

## 3. A prompt budget

**Today: one per worktree, unbounded in the number of worktrees.
After: one per session.**

| | Before | After |
|---|---|---|
| First creation in a session | 1 | 1 |
| Each creation after it | 1 | 0 |
| Six worktrees in one run | 6 | 1 |

**What each one costs when nobody is at the keyboard: the whole run.** That is
not an estimate. It was measured on this release's own run on 2026-09-08 — six
work items on six branches, six `git worktree add` calls, and the guard held
the run at every one of them.

Two residuals, stated rather than left to be found.

- A creation written as part of a **compound** command still costs one prompt
  each time, because the allow is bounded to a command that is nothing else.
  The measured six were single-segment `git worktree add` calls.
- The guard's silence is not the harness's. Where the guard now allows, it
  allows; where it goes silent (the `Agent` path), whatever the harness's own
  permission settings want to ask still stands, and that is not the guard's to
  remove.

Nothing cheaper reaches the same guarantee, and the alternatives were tried on
paper first: a value read from a file cannot say a *person* answered, and the
only thing already in the command — `[worktree-ok]` — is written by whoever
issues the command, which is why `has_token`'s docstring refuses to read it as
consent. The record is the first signal available that a person answered, and
it is available only after the answer.

## 4. Platform honesty

**Tested on macOS 15 (Darwin 25.5.0), Python 3.13.9, one machine.** Not tested
on Linux or Windows.

What this change does and does not touch on that axis:

- It adds **no process inspection**. `ps`, `lsof` and `/proc` are not read by
  anything this branch adds; the session-activity heuristics are untouched and
  every case that exercises them stubs `sessions_in_tree`, as the existing
  suite already did.
- What it does add is **filesystem behaviour**: `os.makedirs`, `open(…, "w")`,
  `os.path.isfile`, and a `git rev-parse --git-common-dir` through
  `optin.git_common_dir`. The failure paths are exercised by making the record
  path a file and by making it a directory, and both are portable
  constructions. Windows differs in *which* error a hostile path raises, and
  every one of them is an `OSError`, which is what the writer catches.
- **The linked-worktree case is executed**, not reasoned about: a real
  `git worktree add` is run in the test and the record is asserted to land
  under the main clone's common directory.
- The one platform claim this design rests on is not a filesystem one: **a
  `PostToolUse` payload means the tool ran, and a hook `ask` cannot be
  auto-answered.** Both are the harness's, on every platform, and neither is
  observable from a test. If a future harness auto-answered hook `ask`
  decisions, a record could be written with nobody asked — which is the same
  standing every gate in this repository already has.

## What must not change, and is pinned

| Property | Case |
|---|---|
| A session with no record still asks | `test_the_first_creation_is_still_a_question` |
| The single-stream site still denies | the same |
| Consent is per session, not per repository | `test_consent_belongs_to_the_session_that_earned_it` |
| Nothing on the asking side writes the record it reads | `test_the_pre_tool_use_arm_records_nothing` |
| The switch direction never reads it | `test_creation_consent_does_not_reach_the_switch_direction` |

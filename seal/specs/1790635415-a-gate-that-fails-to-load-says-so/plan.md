# Implementation Plan: a gate that fails to load says so

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

The catch in `run_gate` stays, and so does every group's output. The catch
starts leaving a record. The `stop` group says the records at the end of the
main session's turn, once per gate per session, as a `systemMessage` placed
before the sealer's stamp. Three phases: the behaviour for the
common case, then the rest of the class, then the words and the ledger.

## Technical context

Existing code this builds on:

- `hooks/dispatch.py#run_gate`: the catch this changes. Today it returns
  `""` for a failure. It will also return what failed, and a new function in
  the same file writes the record. `run_gate`'s return shape is internal:
  `main()` is its only caller in the tree. `tests/test_dispatch.py` loads the
  module but calls `merge` and `main`, never `run_gate`. The work confirms
  that with a grep before changing the signature.
- `hooks/dispatch.py#main`: parses nothing today. It will parse the payload
  for `session_id`, `cwd` and `agent_id`, but only on the failure path and in
  the `stop` group. A payload that is not JSON records nothing.
- `hooks/sealer-stamp.py#toplevel` and `#main`: the walk up from `cwd` and
  the `agent_id` guard this copies in shape. **Whether the walk is shared or
  duplicated is `questions.md` Q2**, decided by the work under one
  constraint: the report path imports nothing under `hooks/` except the
  guarded `optin` lookup.
- `skills/verify/scripts/seal_stamp.py#claim`: the rename-before-print
  shape. It is copied in shape, not imported, because that module's floor is
  3.12 and a hook runs under 3.9.
- `hooks/worktree-guard.py#already_asked`: the `basename` guard on an id that
  names a file, with its measured path escape.
- `tests/test_the_implementer_is_recorded.py#test_a_broken_mark_gate_leaves_the_worktree_guards_verdict_alone`
  and `tests/test_dispatch.py#test_a_crashing_gate_does_not_take_the_group_down`:
  the isolation property. Both must pass **without edits**. An edit to either
  is a signal that the design leaked into a decision.

**The failure scenario of the chosen approach, six months on.** A new gate
lands whose import fails only on one platform. Its author's machine records
nothing, because nothing fails there. On the other platform the record is
written and said once per session at turn end. The line names the gate, the
group, and `ImportError: …`, and the person files it. What this does **not**
catch is a git common dir that cannot be written. There the failure is as
silent as today, and the spec states that residue instead of hiding it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Fail closed**: a gate that fails denies or asks | A partial install or one bad shared module stops every Bash call in every opted-in repository. `CONTRIBUTING.md` calls a deny that fires on every invocation an outage, and it costs a prompt on each call of an unattended run | Rejected by the owner, 2026-09-29 |
| **Say it in the failing call's `PreToolUse` output**, as a `systemMessage` beside or instead of the group's decision | Four problems. (1) A `PreToolUse` `systemMessage` has never been measured in this tree. The one reading of the docs came through a summarising fetch, and the stamp work item found that fetch contradicting itself. (2) `merge()` has three output shapes, and a report has to survive each one; the plain-text shape would have to become JSON, which moves the other gates' reminders onto a different channel for that call. (3) Most tool calls in this workflow are a subagent's, and a subagent's output reaches the person folded (#400, measured). (4) The call has already gone ahead, so saying it sooner changes nothing anyone can do about that call | Rejected |
| **Say it on the `PostToolUse` side of the same tool** (the issue's first suggestion) | `pre-skill`, `session-start` and `stop` have no after-event. A call that another gate denied has no `PostToolUse`. And what plain `PostToolUse` stdout reaches is contested: 27 transcript records store it as model-facing `content`, while the fetched docs say it goes to the debug log | Rejected |
| **A non-zero exit with the report on stderr** | `hooks.json` runs `python3 … \|\| py -3 …`, so a non-zero exit starts the fallback on a consumed stdin. And JSON on stdout is parsed only at exit 0, so a sibling gate's deny would be lost with it. `CONTRIBUTING.md` rests the fallback's safety on `dispatch.py` exiting 0 | Rejected |
| **Also tell the model**, through `additionalContext` or plain `Stop` stdout | The remedy is a person's: reinstall or update the plugin, or repair a hook file. A session cannot perform it. Whether plain `Stop` stdout enters the context is itself contested (#400's probe saw none of its output there, while the fetched docs say it is added). A `Stop` hook's `decision: block` is how a hook keeps a turn going, and output aimed at the model at `Stop` sits next to that mechanism. A report must not re-open a turn. It would also cost the orchestrator's context once per gate | Rejected. This is written down so it can be overturned: if an unattended run's hand-back turns out to be where people look, the line is added there as its own work item |
| **"Once" keyed per call** | An import failure recurs on every call, so a session with one broken file gets a line after every tool call | Rejected |
| **"Once" keyed per session per group** | `worktree-guard.py` sits in `pre-bash` and `pre-agent`. One broken file with one remedy would be said twice, and a broken `console.py` would give every gate one line for each group it sits in | Rejected. The line names the group it was first seen in |
| **"Once" keyed per session per gate per exception class** | A gate whose `main()` fails for two different payloads would be said twice | Rejected. The first failure is what is said. A second cause shows up after the first is repaired |
| **State in the user's home** (`~/.claude/specseal/`, where `version-check.py` keeps its throttle) | `CONTRIBUTING.md`: "No writing outside the repo being worked on". The throttle there is a per-user fact, and a gate failure seen in a repository is not. With `HOME` unset, `expanduser` returns `~` unchanged, which would write into the repository at `./~/…`. And every test that drives `dispatch.py` would need its home redirected, where a record under a fixture's own git dir is isolated for free | Rejected |
| **Record under the git common dir, say it at `Stop`** | A session whose turn ends in another clone does not see the record, which is the grain `implementer-notice.py` already states. An unwritable common dir is silent, as today | **Chosen** |
| **An unwritable record says the line on every call instead** | That needs a second output channel inside the failing call, which is the second row's problem arriving through a side door | Rejected. The residue is stated in `spec.md` §*What cannot be checked* |

## Phases

Vertical slices. Each phase ends with its cases seen red, then green. It runs
its own test files and the files it touches, and nothing broad: the suite,
lint and format run once, after the review rounds settle, and they are the
sealer's.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **A broken gate is said at turn end.** `run_gate` reports load or run failures. `dispatch.py` writes the `.pending` record (opt-in, session, exclusive create, `basename`d parts). The `stop` group claims and says each pending record once, as the whole `systemMessage` when the group printed nothing. Covers S1–S5, S8, S11, S12, S13 | New cases in `tests/test_dispatch.py`, or in a new `tests/test_a_gate_that_fails_says_so.py` if the work prefers one file per claim. S1 is seen red against the unchanged `dispatch.py` before anything else is written. S11's two existing cases pass unedited | ef25f83d |
| 2 | **The rest of the class.** A `SystemExit` at load is caught and recorded (S7). The shared-module breaks (S6, S6b). A subagent's record is said at the main session's `Stop`, and a payload carrying `agent_id` draws nothing (S10). The report goes before the stamp in one message, with the stamp unchanged (S9). The `stop` cost delta is measured on the silent path and written into `phases/phase-2.md` | S7 is seen red against the phase-1 tree, where the group prints nothing. S9 runs with the sealer-stamp fixture. `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` is run whole, because its `stop` output must not move when nothing is pending | 75894624 |
| 3 | **The words and the ledger.** The RIDER inside `run_gate` is replaced by a comment saying what the catch does now. The module docstring of `dispatch.py` and the false sentence in `hooks/implementer.py`'s docstring are corrected. `docs/commit-review-gate-spec.md` §*Registration* gets the paragraph and an `Enforced by:` line. The sentence goes into both READMEs. `seal/specs/1790635415-…/changelog.md`. Rows go in `seal/ledger/1790635415-a-gate-that-fails-to-load-says-so.md`. The `run_gate` row in `seal/releases/0.4.0.md` and N8 in `seal/releases/0.15.7.md` are re-read in place | `evidence-check` over the three ledger files, with each drifted row re-read and `--reverify`d. `.github/scripts/rider_check.py`. `tests/test_a_rider_reaches_its_file.py`, `tests/test_both_editions_carry_the_same_folds.py`, `tests/test_docs_line_wrap.py`, and any test that pins `docs/commit-review-gate-spec.md`. The S14 doc pin is seen red with the new sentence deleted | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **A new directory under the git common dir**, `specseal-gate-failure/`,
  holding one small file per failed gate per session. It is written only
  while a gate is failing, in an opted-in repository. Nothing prunes it,
  which is also true of the other per-session directories there
  (`specseal-implementer-notice/`, `specseal-leases/`, `specseal-stamp/`).
- **One new line a person can see**, and only in a broken install.
- No new dependency, no new environment variable, no migration. `hooks.json`,
  `GROUPS` and `EVENTS` are unchanged.
- **Compatibility:** in a healthy install every group's stdout is byte-identical
  to 0.15.7, including `stop` when nothing is pending.

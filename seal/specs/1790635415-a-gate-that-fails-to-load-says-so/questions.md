# a gate that fails to load says so — questions for the planner

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row below needs a person, and none blocks the build.** The owner answered
the one design question before the first edit: fail open, but say so. The
spawn prompt and issue #28 left the following judgments open. The tree
answered them, and the grounds are in `spec.md` or in `plan.md`'s
Alternatives table. They are listed here so nobody reopens them as questions:

- **Where the report is said.** It is said at the main session's `Stop`, as
  a JSON `systemMessage`. That surface was measured on screen (#400, probe
  D), and it is already shipped by `sealer-stamp.py`. It is not said in the
  failing call's `PreToolUse` output (unmeasured, and it would need
  `merge()` rewritten for three shapes), not on the `PostToolUse` side (three
  groups have no after-event), and not by a non-zero exit (the `py -3`
  fallback).
- **Who is told.** The person. The remedy is a person's act, and a `Stop`
  `systemMessage` stays out of the model's context (#400's Q1, measured).
- **What "once" is keyed on.** Session and gate, within one clone. Not the
  group: one broken file would otherwise be said once for each group it sits
  in. Not the exception class either: the first failure is what is said.
- **Where that state lives.** Under
  `<git-common-dir>/specseal-gate-failure/<session>/`, not in the user's home.
  `CONTRIBUTING.md` says "no writing outside the repo being worked on", and
  every once-marker in the tree already lives under the git dir.
- **Whether an exception inside `main()` counts.** It counts. Two measured
  instances in `tests/test_gates_do_not_fail_open.py` reached the catch that
  way. A `SystemExit` from `main()` does not count, because `worktree-guard.py`
  finishes with `sys.exit(0)`.
- **Whether a `SystemExit` at import counts.** It counts. Today it escapes
  `run_gate` and takes the whole group down, which breaks the isolation
  property itself.
- **Whether a subagent's failure reaches anyone.** It does. A subagent's
  tool-event payload carries the parent's `session_id`. This framer measured
  it on 2026-09-29 with three of its own Bash calls, each of which moved the
  mtime of the main session's `session-lease` file. So a record written from
  a subagent's call is said at the main session's `Stop`.
- **Every group.** All eight groups record a failure, and `stop` also draws.
  `GROUPS` and `EVENTS` do not change.
- **The report beside the stamp.** The report goes first and the stamp stays
  last in one message, keeping #400's decision that the drawing is the last
  thing on the screen.
- **Not opted in.** Nothing is written. Where `optin.py` is itself the broken
  module, the answer is "cannot tell", and the record is written.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Is the report readable on screen as built: line 1 as the dim `Stop says:` label, one line per gate after it, and the stamp still whole and last when both arrive in one message? Probe D measured one stamp alone. Nobody has seen a report before a stamp | **a measurement**, which only a main session can take, because only it hosts `Stop`. It is taken at the first real report, or with a throwaway broken gate in a copied plugin root. One look at the screen | **Readable:** nothing to change. **Garbled** (the label rendered wrongly, or the stamp clipped): the report moves to its own `systemMessage`, the stamp's precedes it, and #400's "last on the screen" is re-argued. That is a change to the join in `dispatch.py` | As `spec.md` §*Scope* item 4 states | ⬜ |
| Q2 | Is the walk from `cwd` up to the git common dir shared with `hooks/sealer-stamp.py#toplevel`, or duplicated in `dispatch.py`? | **the work**. It is decided under one constraint: the report path imports no module under `hooks/` except the guarded `optin` lookup, so it cannot depend on the module whose failure it reports | **Shared:** the walk moves to a place both can reach without the report path importing a gate's dependencies, and `sealer-stamp.py` calls it. **Duplicated:** each copy carries a comment naming its twin and the reason, and a test holds the two to the same answer on a linked worktree | Duplicated, with the twin named, if sharing would make the report path import a shared module | ✅ Decided by the work in Phase 2 (`75894624`): duplicated. `hooks/sealer-stamp.py` imports `console` and `optin` at load, so reaching its walk would make the report depend on the modules whose failure it reports. `dispatch.toplevel` names its twin, and `tests/test_a_gate_that_fails_says_so.py#test_the_walk_agrees_with_its_twin_in_sealer_stamp` holds the two to one answer in a subdirectory and in a linked worktree |
| Q3 | The exact wording of the label line, the per-gate line and the closing sentence | **the work**. Pinned by S1 and S14 (contract §14) | Constrained by `spec.md` §*Scope* item 4. The label is not blank and says what this is. Each line names the gate file, the group, load or run, and the exception's class and first line. The closing sentence says nothing was blocked and that this is said once per session | As `spec.md` states | ✅ Decided by the work in Phase 1 (`ef25f83d`) and pinned by S1, S5 and S9's cases: the three lines are quoted in `phases/phase-1.md` §*What this phase found* |
| Q4 | What the `stop` group now costs per turn end on the silent path, in a main checkout and in a linked worktree | **a measurement**, taken in phase 2 by the builder | **Under the noise of `sealer-stamp.py`'s own walk:** nothing to do. **A process in a main checkout:** the walk is wrong and phase 2 fixes it | The walk starts no process in a main checkout | ✅ Measured in Phase 2 (`75894624`), 40 runs a side against `2dc9a970`: a main checkout starts no process and moves from a 25.5 ms to a 27.0 ms median; a linked worktree starts one `git` more, as `sealer-stamp.py` already does there, and moves from 41.8 ms to 58.7 ms. The default holds and nothing changed; the table is in `phases/phase-2.md` |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.

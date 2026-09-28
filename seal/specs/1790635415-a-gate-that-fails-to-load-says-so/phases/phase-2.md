# 1790635415-a-gate-that-fails-to-load-says-so — phase 2

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 75894624 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s Phase 2: the rest of the class. A `SystemExit` at load is
caught and recorded (S7), seen red against the phase-1 tree. The shared-module
breaks (S6, S6b). A subagent's record is said at the main session's `Stop`,
and a payload carrying `agent_id` draws nothing (S10). The report goes before
the stamp in one message with the stamp unchanged (S9), run with the
sealer-stamp fixture, and
`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` run whole. The
`stop` cost on the silent path is measured and written here (`questions.md`
Q4), and Q2, whether the walk is shared or duplicated, is decided.

## What this phase found

- **S6 named five gates, not four, and the fifth came from the fixture.** With
  `cmdline.py` broken and a `post-bash` call that was a commit,
  `evidence-advisor.py` failed at run with `FileNotFoundError`. It reaches its
  checker at `<plugin>/skills/…/evidence_check.py`, and a copy of `hooks/`
  has no `skills/` beside it. The case's `post-bash` call is now `ls`, and
  the four gates the frame named are the four said. The same fact matters to
  anyone copying `hooks/` for a probe from now on: a commit through
  `post-bash` in such a copy now writes a record for `evidence-advisor.py`.
  In a real install, a missing checker is a broken install, and saying so is
  correct.
- **S9 runs the live `hooks/`, not a copy.** `sealer-stamp.py` loads
  `seal_stamp.py` from `<plugin>/skills/verify/scripts/`, so in a copy it
  draws nothing and there is no stamp to go beside. The failure record is
  planted by hand, which is also the case of a record written by another
  process. The stamp half is compared with the same `stop` run for a session
  that has only the values file, so "unchanged" means byte-identical lines,
  not a re-derivation of the drawing.
- **Plain text at `Stop` is not converted into a `systemMessage`.** The frame
  names two shapes of the `stop` group's output, nothing and the stamp's JSON.
  A third, plain text, is unreachable today and reaches a different reader
  from a `systemMessage`. `dispatch.beside` returns None for it, and the
  records wait for a turn end that can carry them rather than being claimed
  and lost. A case pins it with a monkeypatched `run_gate`.
- **Q2: duplicated.** `dispatch.py` cannot import `hooks/sealer-stamp.py`
  without loading `console` and `optin` at import, which is the dependency
  the report must not have. `dispatch.toplevel`'s docstring names its twin
  and the reason, and
  `tests/test_a_gate_that_fails_says_so.py#test_the_walk_agrees_with_its_twin_in_sealer_stamp`
  holds both walks, and `dispatch.common_dir` against
  `optin.git_common_dir`, to one answer in a subdirectory of a main checkout
  and in a linked worktree. The same case records a failure from the
  worktree and says it from the main checkout.
- **Q4, measured.** `dispatch.py stop` ran with a `Stop` payload, 40 times
  alternating, against a `git archive` of `2dc9a970` and a copy of this
  tree, each with `skills/verify/scripts/` beside `hooks/`, in a local
  repository with `seal/` committed and a linked worktree of it. A `git`
  wrapper on `PATH` counted processes. Nothing was pending.

  | Where the turn ended | Before (`2dc9a970`) | After | `git` processes before → after |
  |---|---|---|---|
  | main checkout | median 25.5 ms, p90 27.9 ms | median 27.0 ms, p90 28.7 ms | 0 → 0 |
  | linked worktree | median 41.8 ms, p90 43.7 ms | median 58.7 ms, p90 60.9 ms | 1 → 2 |

  The main checkout starts no process, which is the frame's default.
  A linked worktree pays one `git rev-parse --git-common-dir` more per turn
  end, which is the same cost `sealer-stamp.py` already pays there, and
  `spec.md` §*Data & interfaces* already allows it. Not changed. What would
  remove it is reading the `.git` file's `gitdir:` line and that directory's
  `commondir` file. That is a parser of git's layout that nothing asked
  for, and `sealer-stamp.py` would want the same one.
- **S7's shape, measured before the fix:** `main()` raised `SystemExit: 0`
  out of the planted gate's module body, and the commit gate after it never
  ran. After: the deny is printed, and the record reads
  `{"group": "g", "phase": "load", "error": "SystemExit", "message": "0"}`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

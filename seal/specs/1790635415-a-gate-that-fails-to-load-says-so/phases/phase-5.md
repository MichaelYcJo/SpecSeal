# 1790635415-a-gate-that-fails-to-load-says-so — phase 5

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 8b6b0a00 |
| Ran by | specseal:smith on claude-opus-5-5 |

**Reverted at the owner's decision after round 3.** Everything this phase
built, and everything round 2's fix pass added to it, is out of this branch.
`hooks/cmdline.py` and `hooks/commit-review-gate.py` are the release branch's
again, with no difference from `origin/release/v0.16.0`. #662 and #665 are
redone from a clean start in a separate work item. The commit above is the
one that closed the phase when it was built, and it no longer describes the
tree.

## What this phase was asked

Build `plan.md`'s Phase 5, which the owner added after round 1 so that #662
is fixed in this branch. The commit gate keeps a `cd` across a newline: `cd W
&& … <heredoc>` with `git commit` on the next line was judged in the
session's directory, and prompted the person during an `automation` run. Both
directions are pinned: an undeclared session directory with a declared `cd`
target reads silent, and a declared session directory with an undeclared
target is asked. Find why the gate's path does not carry the `cd`, and fix it
in `hooks/cmdline.py` for every gate that reads a directory from a command.
The verification: the three shapes of #662 through the gate's `main()` plus
the reverse direction, seen red at `e8e5f977`; `bin/test` over the gate and
`cmdline` modules; one mutant per changed branch.

Mid-phase the owner added #665 to it: a heredoc body fed to a known non-shell
interpreter reading its program from stdin is data to the gate, not shell.
Shells, `eval`, `ssh`, `xargs` and unknown consumers are still read as shell.
The command that prompted the person, this phase's own `python3 -` patch, is
the seen-red case, and both directions are cases.

## What this phase found

What stays true after the revert, for the work item that redoes both issues.
None of it describes code in this branch.

- **#662's premise, measured:** the gate never dropped the `cd` at a
  newline. It judged the `cd`'s target and also the session's directory,
  because `;` and a newline consume a `cd`'s failure branch (#72, deliberate).
  The prompt came from that failure branch.
- **Three kinds of false silent came out of the attempts, each read by a
  later round:**
  - #665, round 2's 🔴 1: the consumer was read only up to the `<<`, so words
    after the redirect, a bundled flag, and a `$(…)`, `${…;…}` or `>&` read a
    shell-run body as data. The fix pass found a fifth way: a separator
    written `';'` or `\;`, which a posix tokeniser unquoted.
  - #662, round 2's 🟡 2: the hook reads the filesystem before the command
    runs, so `mv W X ; cd W ; git commit` trusted a `cd` that fails (contract
    §13).
  - Round 3's two 🔴, in `3fb828fb`'s record, are what ended the run capped.
- **What held and stays:** #661's `readable`, including round 2's 🟡 3 fix, is
  phase 4's and is not reverted. The `||` forgery cases and the alias case
  were never edited and still pass.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Every change to `hooks/cmdline.py` and `hooks/commit-review-gate.py` for #662 and #665, their cases in `tests/test_gate_judges_the_repo_it_commits_to.py`, their sentences in `docs/commit-review-gate-spec.md` and agent contract §9, ledger rows G7 and G8, the `seal/ledger.md` heredoc row's correction, their changelog entries, and 0.4.0's re-read notes on `_heredoc_split` | the separate work item that redoes #662 and #665 |

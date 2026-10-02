# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d06f5e25 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

Build the installer and the stubs against real git. `hooks/hook-install.py`
joins `GROUPS["session-start"]` and `GROUPS["pre-bash"]`.
`hooks/git/{pre-commit,reference-transaction,post-checkout,post-commit}.py`
ship as entry points that exit 0. The stub has a marker line, the embedded
installed path, `python3 || py -3`, and a `-f` test so that an uninstalled
plugin leaves a stub that exits 0. The installer handles ownership and
version rewrites, and gives P1's answer for a foreign slot, said once.
Stubs come out of a clone that opted out. S12, S13. Every message is pinned
(§14).

## What this phase found

- **A stub's narrowing is three lines of `sh`, each measured in phase 1.**
  `reference-transaction` leaves before Python unless the state is
  `prepared` and `GIT_AUTHOR_DATE` is exported (M12). `post-checkout` leaves
  unless its first argument is the null object id (M3, M14). Every stub
  leaves when no session variable is exported and no lease exists anywhere
  in the clone (P2, answer (a)).
- **The lease route has to look across the clone.** Leases sit under each
  worktree's own `--absolute-git-dir` (`hooks/session-lease.py#main`), not
  under the common directory as spec §*What the tree answered* 4 says. So
  the stub's P2 check walks `<common>/specseal-leases` and
  `<common>/worktrees/*/specseal-leases`. `ls -d a b` exits non-zero when
  either operand is missing, so it is a loop over `[ -d ]` instead.
- **A linked worktree is opted in only where the root is committed.**
  `optin.home_at` reads `<worktree>/seal/` and then the common directory.
  An untracked `seal/` in the main checkout does not opt in a linked
  worktree, and the installer says nothing there. That is the existing
  rule, and the fixtures commit their root.
- **The suite needed a switch.** `hook-install.py` runs first in `pre-bash`,
  so every case driving that group would grow stubs in its fixture and print
  the installer's line. `SPECSEAL_HOOK_INSTALL=off` turns the installer off,
  and `tests/conftest.py` sets it for every case. The installer's own module
  unsets it (`git_hooks_installed`). It also means a case can never write
  into this clone. A second autouse fixture strips the session variables,
  because a run from inside a session would otherwise judge commits that CI
  leaves alone.
- **A `systemMessage` beside a decision used to be dropped.**
  `dispatch.merge` kept only the decision's reasons, so the installer's
  once-per-session line would be lost whenever a neighbour denied in the
  same call. It is now carried beside the decision.
- **Mutation testing removed a duplicate rule.** The installer's "slot is
  current" early return and `write_stubs`' byte comparison each covered for
  the other (four survivors). Staleness is now decided in one place, by
  comparing a stub's bytes with the text the running plugin would write.
  `githooks.foreign` answers only whether somebody else holds the slot.
  Thirty mutants across the two runs; all red.
- **P5 in `questions.md`.** P1(a)'s "keeps 0.16.0's behaviour" needs the
  0.16.0 text paths to exist for a foreign clone, so `githooks.decides` is
  the question each of them asks first. It is built here, and phase 3 is
  where the commit gate first asks it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — `dispatch.py` gained a group member and a merge rule; nothing left the tree | none |

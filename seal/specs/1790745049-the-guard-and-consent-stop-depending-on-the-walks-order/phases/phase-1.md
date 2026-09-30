# 1790745049-the-guard-and-consent-stop-depending-on-the-walks-order — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 97654799 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

The guard and the consent writer read exactly the directories `86256492`
read, from the base thread `walk_directories` carries, and never the walk's
own directories. The commit gate is unchanged. Enumerate every consumer of
`walk_directories` and say which reading each takes. Remove only what becomes
dead for the two consumers, and keep the gate's behaviour where its reason
text or deny order depended on the ordering. Proof seen red first: the
round-3 chain and its consent twin, PR #690's two residual shapes, a
structural comparison against `86256492`'s hooks over a generated corpus, 0
decision changes against `542f920b` over a gate corpus, and every existing
case that pinned I's walk-first behaviour for the guard changed to the base
behaviour with a note.

## What this phase found

**The consumers (§12).** Read from the tree at `542f920b`:

| Consumer | Reads | Takes since #689 |
|---|---|---|
| `hooks/commit-review-gate.py#commit_invocations` | every directory of every segment, then its merged-view and unglued re-reads | `walk_directories`, unchanged |
| `hooks/worktree-guard.py#walk_command`, and through it `main`'s selection loop | the first directory per segment that classifies | `base_directories` |
| `hooks/worktree-guard.py#only_creates_a_worktree`, through `walk_command` | the segments only; it ignores the directories | `base_directories`, with no effect |
| `hooks/worktree_consent.py#creation_directory` | the first readable directory of the first creation | `base_directories` |
| tests: `test_what_the_reader_understands.py`, `test_the_reader_agrees_with_bash.py`, `test_a_path_the_command_wrote_out.py`, `test_gate_judges_the_repo_it_commits_to.py`, `test_no_shape_the_base_stops_reads_silent.py` | `walk_directories` directly, as the gate's reading | unchanged |

Nothing else in `hooks/`, `skills/`, `bin/` or `.github/` calls it.
`judgeable` and `classify` in the guard take one directory from the caller.

**The base thread was not quite `86256492`'s reading.** Its directories are
unplaced by the reading past redirections as well, where the as-written
reading found no `git` (I14, for the gate). `base_directories` takes the
thread before that step, so it unplaces on the as-written reading alone,
which is the flag `86256492` read. Where it matters, `86256492` found no git
in the segment at all, so no base answer is being departed from; the case
`test_a_segment_only_the_reading_past_redirections_finds_is_judged_where_the_base_walked`
pins which directory such a segment gets.

**Nothing in the ordering code became dead.** The rule that puts the base's
directories first where the walk names none was written for the guard. A
mutant that always puts the walk's first changes no gate decision, and 404 of
5,092 reason texts. So it stays for the gate, and its comment now says so.

**Moving the loop out of `walk_directories` drifted released rows.** A first
version put the loop in a helper `_walk`; three rows in `seal/releases/0.4.0.md`
anchor statements inside `walk_directories`, and every one went to DRIFTED
with its statement "gone from" the unit. `walk_directories` now takes a `base`
flag instead, and `base_directories` asks it; those rows resolve again.

**The structural comparison.** 32,893 commands, 326,368 segments. Against
`86256492`'s hooks, every segment's directories as the guard reads them
differ in 0 commands (28,337 at `542f920b`), the consent writer's directory in
0 (2,643), and the guard's judged tree in 0 (1,304). The guard's selection
differs in 4,755 commands, all `… 2>/dev/null git switch feature/x`, which
`86256492` did not read as git.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The guard's landing of a `cd` behind a redirection (round 2 of 1790660768) | `seal/ledger/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order.md` M2 records it as the accepted cost; I13 in 1790660768's fragment is corrected |
| `test_a_cd_behind_a_redirection_moves_the_tree_the_guard_judges` (NAME NOT IN TREE: the case's old name), renamed and changed to the base's answer | `test_a_cd_behind_a_redirection_leaves_the_guard_on_the_tree_the_base_judged` in the same module |

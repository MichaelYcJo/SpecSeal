# 1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | pending |
| Ran by | unknown — the spawn prompt handed this row no value, and a segment does not source its own |

## What this phase was asked

Build #689 from round 3 of 1790660768's report. 🟡 1: past `STATE_CAP`,
`walk_directories` let a directory an `||` skips lead the base thread's, so
the worktree guard and `worktree_consent.creation_directory` judged the wrong
tree; plant the report's regression case and its guard and consent shapes,
each seen red at `542f920b`, and enumerate the class (every way the walk
regains a readable directory after collapsing — `||`, `&&`, `;`, newline, a
subshell, the merged view — and both consumers). Invariant: nothing
`86256492` asks or stops may read silent; the commit gate's verdicts do not
move; run the cap-order comparison and a `main()` corpus. ⬜ 2: add the zsh
short loop to I15's exception list with a `Corrected 2026-09-30` note. ⬜ 3
and ⬜ 4: fix, or refuse with grounds in `overview.md`.

## What this phase found

**Round 3's fix was not the one built.** Its `collapsed` flag closes round 3's
rows, and measured against the alternative it leaves two things: a `cd` read
past its redirections stops leading once the walk has collapsed, and the
same cause with no cap reached stays open (`(cd O)` behind a failing `cd` in
an `||` chain, the creation filed under the skipped landing). Both come from
the ordering test asking whether the walk named ANY readable directory. The
walk's first directory is a shell the segment runs in (`_branches` puts
`running` ahead of `skipped`), so testing that one closes every row. `plan.md`
§*Alternatives considered* holds the comparison.

**The class, enumerated by probe.** Through the guard's `main()` and
`creation_directory`, 5 capping prefixes × 14 regains against bash, at
`86256492`, `542f920b`, the flag and the fix:

- Behind `||` (a plain `cd`, one behind a redirection the splitter cut, one
  with a redirection after its operand, one landed past a redirection in
  front, and a `cd` into a repository): silent and misfiled at `542f920b`,
  the base's answer at the flag and at the fix. These are the planted cases.
- `&&`, `;` and a newline, into a repository or a missing directory: the
  same at all four trees. `;` and a newline into a missing directory are
  silent at `86256492` too, through the guard's fallback for a directory
  holding no repository.
- A subshell (`(cd O) &&`, `(cd O);`): the same at all four past the cap,
  silent at `86256492` too. Before the cap, after an `||` chain of landings,
  it is the no-cap case above.
- `2>/dev/null cd O &&` past the cap: the base asks about `w`, bash switches
  in `O`, `542f920b` and the fix judge `O`, the flag judges `w`.

**Seen red.** `tests/test_guard_resolves_the_tree_it_judges.py`'s 11 new
cases and the Q7 cap case were run against exported hook trees paired with
this branch's tests: 10 red at `542f920b`; the landing case red at
`86256492` and under the flag, which also leaves the 3 subshell cases red.
The gate's order case red at `542f920b` and with the walk always first.
Mutants of the fix's condition, each killed: the pre-#689 test (10 red), the
walk always first (11), the base always first (1), the last directory tested
(5). `wheres and` is equivalent, since `running` is never empty.

**The corpus.** 1,216 generated commands (1,000 seeded from 43 segment
shapes and 6 operators at lengths 1–40, and 216 capping chains by hand) and
20,234 segments. Cap-caused changes of the guard's first directory from
`86256492`'s: 166 at `542f920b`, 0 under the flag, 0 here. Of the consent
writer's: 244, 72 by the flag's own uncapped comparison, 89 here, every one
where the base thread names no readable directory (`overview.md` §*Not done*).
A base directory is missing in 405 segments, 209 `2>/dev/null nice …` and 196
the zsh short loop, and in no other shape, which is ⬜ 2's list. Through the
gate's `main()`, 3,648 jobs in three session kinds: 0 of the base's 2,228
stops lost, no decision different from `542f920b`'s, nothing raised; 128
reason texts moved, 125 the same list reordered.

**A harness trap, for the next probe that runs trees in sequence.** The gate
denies once per session and repository, and records that under the
repository's git directory, so four trees run against one fixture with the
same session ids answer `deny` for whichever tree reaches a repository first.
The first run read that as 14 verdicts moved; per-tree session ids made it 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the ordering test "the walk names any readable directory" in `walk_directories` | replaced in place by the first-directory test; `docs/commit-review-gate-spec.md` states the new one |

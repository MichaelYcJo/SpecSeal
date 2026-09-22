# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 2a7b571a |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`docs/one-root-by-lifetime.md` — the root, the two modes, the config reader.
Seven items across five segments: `hooks/root-migrate.py`,
`skills/implement/scripts/seal.py` (3), `hooks/mode-gate.py`,
`hooks/config.py` and `skills/config/SKILL.md`. Verified as phase 3.

## What this phase found

### Four of the seven are the document's own origin story

`docs/one-root-by-lifetime.md` is the policy `1788331011` wrote, so three of
the four markers go onto sentences that already exist and say exactly what
the work item established:

| Item | Marked on |
|---|---|
| `1788331011` | §*The change in four lines* — two roots holding three lifetimes |
| `1788817289` | §*The opt-in signal is the root itself, wherever the mode put it* |
| `1788411058`, `1788398967` | §*Shared or local*, whose table already carries `seal mode` in its switching row and `seal export` / `seal import` in its re-clone row |

Two markers on one sentence is the shape a segment produces when two work
items refined one rule. The table row *Other machines and a re-clone* is
`1788398967`'s whole standing statement, and *Switching later* is
`1788411058`'s; they are one table, so they take one anchor.

### Three had no home, and the document had a gap rather than a section

`seal/config.md` is named in the document only as a thing that exists.
Nothing said what a row is, what an absent one means, or what happens when
one will not parse — so the three remaining items are one new section,
*What the repository decides for itself, and how it is read*.

The three are a sequence rather than a list, which is why they read as one
statement: a setting nobody can find is a setting nobody has; a reader that
stops at an unparseable line silently drops every row below it; and a git
call that failed is not a git call that answered *nothing*. Each is the same
failure one layer down — a confident answer given where no answer was
available.

### `1788789329` is about a script, and its rule is about a root

Its segment is `skills/implement/scripts/seal.py`, and its subject is five
`git()` call sites. Folding a list of call sites would be folding a commit.
What still governs is the distinction those five sites were taught, and that
distinction is about the thing this document owns: whether a repository has
a remote, another worktree, a tracked file — the questions a mode switch
asks before it moves a root. So it folds here, in the terms a reader acts
on, and the five coordinates stay in the commit.

### The Korean mirror is untouched, which is `spec.md` O4

`docs/one-root-by-lifetime.ko.md` now says less than its English twin. That
is deliberate: no check pairs the `docs/` mirrors, the only both-editions
rule in the tree is the README pair's, and a mirror sweep is its own work.
Recorded here rather than left to be noticed, because a reader of the Korean
file will find the config section missing and should know it was a decision.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing from the tree — prose and markers only | none |

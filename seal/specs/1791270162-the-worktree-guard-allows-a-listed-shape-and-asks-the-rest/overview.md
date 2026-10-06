# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

## Why this work exists

The worktree guard stops predicting a branch switch from a command's text and
instead lets through only git commands it positively knows leave the branch
where it is, stopping the rest only in a tree where a switch would matter.

## How far it got

**Phase 1 is closed, and it is the only phase built.** It measured the
recorded runs with a deleted probe and put nothing in the tree but the record
(`phases/phase-1.md`, `questions.md` M1–M3):

- M1: 31,193 distinct (command, cwd) pairs in cut 1 and 33,220 in cut 2,
  8,960 and 9,695 of them holding git, 55 subcommand words. Cut 1 reads
  above 25,741, not below it, and the difference is not reconciled.
- M2: as written, the build stops 871 cut-2 pairs tree-blind, 570 of them
  pairs today's guard does not stop even at its maximum. Today's guard stops
  no pair the build lets through, and candidate C fires on none.
- **M3 is not zero.** 595 distinct cut-2 pairs stop with no plain rewrite
  the stop's text can name, and 575 of them are a `$( … )` body holding only
  listed git. With such a body read as listed, M3 is 34.

**Phase 2 is next, and it stops for the owner first.** M3's row says a
nonzero count stops phase 2 until the owner has the rows, so `questions.md`
P2 (the substitution body), P3 (`update-ref` and `symbolic-ref`) and P4 (an
untokenizable command) wait on the repository owner before phase 2's first
edit. P1 is still unanswered and its default (a) was taken under the press.
Phases 2–4 run in the next session on another machine.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A substitution body holding only listed git | `spec.md` In 1: a non-git segment "where its text holds a substitution body (`$( … )`, a backtick pair, `<( … )`) holding the bare word `git`" is unrecognised; phase 1 measured that clause as 575 of 595 no-rewrite pairs | nothing built; put to the owner as `questions.md` P2 | a nonzero M3 stops phase 2 for the owner's rows, as M3's own row says |
| `eval`'s string | `plan.md` names `hooks/cmdline.py#command_strings` for a shell string's words; it returns no string for `eval "git switch x"`, which the probe's first self-check caught | the probe joined `eval`'s words; phase 2 decides its own reader (W3) | the self-check line of `phases/phase-1.md` |

## Not verified

| Item | Who must answer |
|---|---|
| Why cut 1 reads 31,193 pairs where 1791119071's phase 1 read 25,741 over more transcripts; that probe was deleted, so its definition cannot be re-run | phase 3's builder, which re-reads the corpus with this phase's definition so that before and after compare on one count; the old count itself cannot be reproduced |
| Which recorded subcommands leave HEAD's branch where it was, beyond the ones `spec.md` In 5 names (`clone`, `init`, `config`, `archive`, `apply`, `gc`, `update-index`, `format-patch`, `count-objects`, `help`): judged by reading what each does, not run against git | phase 2, when `LEAVES_THE_TREE` is written with its counts |
| Every count is tree-blind, so each is an upper bound on stops where the tree matters | phase 3's re-read, and the pull request's prompt budget, which says so |

## Not done

Phases 2–4, by the spawn's scope: this segment was phase 1 only, and the
session moves to another machine.

## Fed back into the spec

none

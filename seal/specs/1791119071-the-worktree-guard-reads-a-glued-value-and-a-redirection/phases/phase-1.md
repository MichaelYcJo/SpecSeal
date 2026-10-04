# 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 7b69bdf4 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Measure before building, and put nothing in the tree but this record. Three
measurements: git's truth table for `spec.md`'s Axis 1 × Axis 2 (A1, M1),
run with real git under bash in a scratch repository outside the worktree,
never switching the worktree itself; the count of generated Axis 1 × 2 × 3
shapes silent at `94d7b2e0`, function level (`classify` per frozen segment,
then candidate C), by axis; and the corpus counts of A11 before the build:
the quoted-`>` and R& shapes, and the base's questions over the recorded
command and directory pairs. Record P1 as answered (a) on the grounds the
orchestrator relayed.

## What this phase found

**P1 is answered (a).** The owner's milestone batch offered #773, #764 and
#738 as one bundle whose option text consented to reopening `classify`, and
the owner chose it (`questions.md` P1, committed first, at `c297aaad`).

**M1: git 2.54.0 switches on every constructed spelling but one, and the
value-taking options split in two.** Executed in a scratch repository with
branches `main` and `feature/x` and a committed `README.md`, one fresh copy
per spelling, each run as `bash -c "git …"`; a switch is a moved `HEAD`.

| Spellings | git 2.54.0 |
|---|---|
| `checkout` `-b y`, `-B y`, `-by`, `-By`, `-qb y`, `-qB y`, `-fb y`, `-qby`, `-qBy`, `--orphan y`, `--orphan=y`, `--orp y`, `--orph=y` | switches, every one |
| `switch` `-c y`, `-C y`, `-cy`, `-Cy`, `-qc y`, `-qC y`, `-fc y`, `-qcy`, `--create y`, `--create=y`, `--cre y`, `--cre=y`, `--force-create y`, `--force-create=y`, `--force-c y`, `--force-c=y` | switches, every one |
| `switch` `--orphan y`, `--orphan=y`, `--orph y`, `--orph=y` | switches on a clean tree; refuses on a dirty one ("Your local changes … would be overwritten") — in the class, because over a clean tree with another session it moves the tree |
| `switch --c y` | refused, exit 129: "ambiguous option: c (could be --create or --conflict)". Leaves the class |
| V: `--conflict merge feature/x`, `--conflict=merge feature/x`, `--conf merge feature/x`, on both subcommands | switches |
| V: `checkout -U 3 feature/x`, `-U3`, `--unified 3`, `--inter-hunk-context 2` | refused, exit 128: "the option '--unified' requires '--patch'". With `-p` it applies hunks and keeps the branch (spec's Out) |
| `checkout --pathspec-from-file /dev/null feature/x`, `checkout -t feature/x`, `checkout --recurse-submodules feature/x`, `checkout --end-of-options feature/x`, `checkout -qf feature/x`, `switch -t feature/x` | switches (`-t` creates `x` tracking `feature/x`) |
| `checkout -- -b y`, `checkout --conflict feature/x`, `checkout --no-orphan y`, `switch --no-create y`, `checkout -tb y`, `checkout --orphan`, `checkout -b`, `switch -c` | none switches: a pathspec, a value taken as the style, a negation that takes no value, `-t` taking `b` as its value, and a missing value |
| R1/R3/R4: `checkout 2>/dev/null feature/x`, `checkout feature/x>/dev/null`, `checkout -b 2>/dev/null y`, `checkout -b>/dev/null y`, `checkout -by>/dev/null`, and the same on `switch` | switches |
| Restore twins: `checkout README.md`, `checkout --conflict merge README.md`, `checkout .`, `checkout 2>/dev/null README.md`, `checkout README.md>/dev/null` | restore the file and keep the branch |
| `checkout 'feature/x>y'` | refused: no pathspec of that name. A quoted `>` is part of the word to git |

So M1's default holds with two exceptions the build reads: an ambiguous
abbreviation is a word git refuses, and `-U`/`--unified`/`--inter-hunk-context`
take a value but switch nothing without `-p`. The reader still takes their
value, so `checkout -U 3 feature/x` reads `feature/x` as the name and asks a
command git refuses. That is the loud direction on a shape nobody runs, and
the build does not teach the reader that `-U` needs `-p`.

**The generated class at `94d7b2e0`: 7,025 of 20,729 switching shapes are
silent.** Executed by a deleted probe that loaded `94d7b2e0`'s `hooks/` (from
`git archive`) and, for each shape, ran `classify` on every frozen segment
`walk_command` yields, then `wider_only_kinds` with the kinds it judged.
`is_ref` was a set lookup over `feature/x` and `main`, so the sweep spawned no
git; `README.md` and `f.txt` existed on disk. The verbs were the 45 spellings
M1 found switching (`checkout`/`switch` × S1–S4, L1–L4, a target, V), and each
went through the test module's own construction: every operator
`_REDIRECTION` names, bare, with a number and with `{fd}`, at every position,
glued and spaced, its target glued and spaced. Silent / generated, by
spelling and by where the redirection stands:

| Spelling | R0 | before `git` | `git`·sub | R2 | R1 | between later words | stuck to a middle word | R3 | R5 | R& | silent / all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 0/4 | 0/216 | 0/288 | 0/72 | 0/216 | 0/216 | 36/72 | 0/72 | 0/216 | 36/600 | 72/1,972 |
| S2 | 4/4 | 216/216 | 288/288 | 72/72 | 108/216 | — | — | 54/72 | 108/216 | 400/472 | 1,250/1,556 |
| S3 | 3/6 | 0/324 | 0/432 | 0/108 | 162/324 | 162/324 | 54/108 | 54/108 | 162/324 | 204/900 | 801/2,958 |
| S4 | 3/3 | 162/162 | 216/216 | 54/54 | 108/162 | — | — | 45/54 | 108/162 | 318/354 | 1,014/1,167 |
| L1 | 1/4 | 0/216 | 0/288 | 0/72 | 54/216 | 54/216 | 18/72 | 18/72 | 54/216 | 68/600 | 267/1,972 |
| L2 | 4/4 | 216/216 | 288/288 | 72/72 | 54/216 | — | — | 45/72 | 54/216 | 364/472 | 1,097/1,556 |
| L3 | 1/4 | 0/216 | 0/288 | 0/72 | 54/216 | 54/216 | 18/72 | 18/72 | 54/216 | 68/600 | 267/1,972 |
| L4 | 3/3 | 162/162 | 216/216 | 54/54 | 54/162 | — | — | 36/54 | 54/162 | 282/354 | 861/1,167 |
| target | 0/7 | 0/378 | 0/504 | 0/126 | 162/378 | 108/162 | 18/54 | 63/126 | 0/378 | 126/922 | 477/3,035 |
| V | 2/6 | 0/324 | 0/432 | 0/108 | 162/324 | 270/540 | 81/180 | 54/108 | 108/324 | 242/1,028 | 919/3,374 |

R0 is the spelling with no redirection: 21 of the 45 spellings are silent
bare — every S2, S4, L2 and L4, the S3/L1/L3 spellings whose new branch is no
ref yet, and `checkout --conflict merge feature/x`, where `classify` looks up
`merge`. The `before git`, `git`·sub and R2 columns are candidate C's alone,
and they are silent only where C's own words miss the spelling, which is the
same defect one reader over. Of the 5,527 restore-twin and no-switch shapes,
2,472 were asked at the base: §*Which tree*'s tree-blind rule for C's
positions, and 579 shapes of `checkout -- -b y`, which the base reads as a
creation because it finds `-b` anywhere.

**The corpus is smaller on disk than the one D1 fixed.** Every `*.jsonl`
under this repository's project directory on this machine now holds 580
transcripts (33 main, 547 subagent), and the Bash tool uses timestamped before
2026-10-03T11:06:22+09:00 are 25,913 uses and 25,741 distinct command and
directory pairs, against D1's 27,551 and 27,351. The main transcripts fell
from 34 to 33, so at least one transcript D1 read is no longer on disk, and
the pairs only it held cannot be recovered from this machine. The A11 counts below and in phase 3 are
taken over the 25,741 that remain, base and build alike.

**The base over the corpus.** Executed by a deleted probe with `94d7b2e0`'s
`hooks/`, tree-blind as D3 counts: 356 pairs hold a segment the frozen
reading calls a switch by its words alone, 47 a creation, and candidate C
fires on 0. No pair holds a `<` or `>` glued inside a `checkout` or `switch`
word, quoted or not. 81 pairs hold an `&`- or `|`-led redirection inside a
`checkout` or `switch` that only the merged view joins. C fires on none of
them, so in each the frozen segment already holds the switch; the twenty of
them read were all a `2>&1` written after it (`git switch -c … 2>&1 | tail
-1`).

The probes, their result files, the scratch repositories and the copy of
`94d7b2e0`'s hooks live under the session scratchpad; the probes and scratch
repositories are deleted when phase 3 has re-read the corpus with the build.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probes lived outside it | none |

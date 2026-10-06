# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 1d28e9a9 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Phase 1 only: the corpus measurement (M1–M3) through a deleted `test_tmp_*`
probe, with the record files committed and nothing else in the tree. Phases
2–4 are for the next session on another machine. No warden, sealer or pull
request in this segment, no full suite and no broad gate, no push. P1 is
unanswered and its default (a) stands. #841 is not merged; its twins case and
`test.yml` are not touched (W4). Stop at a committed boundary inside about 25
minutes and say in `overview.md` how far phase 1 got, whether M3 is zero, and
that phase 2 is next.

## What this phase found

**The frame does not hold on one clause of In 1, and M3 is not zero.** The
two findings are the same fact read twice: In 1 makes a non-git segment
whose text holds a substitution body with the bare word `git` unrecognised,
and In 3 names no plain spelling for that shape. Over cut 2 that clause stops
pairs holding 590 such bodies, and 575 of them hold only listed git inside
the body
(`F=$(git diff --name-only …)`, `$(git rev-parse HEAD)`, `for b in $(git
branch -r …)`). Built as written, the clause is the largest stop class this
change adds, and none of its stops has a way on that the stop's text names.
`questions.md` P2 puts it to the owner with the reading that would silence
it: judge the body through the same three shapes, so a body holding only
listed git is listed.

**Method.** Executed by a deleted probe, `test_tmp_826_corpus.py`, run as
`python3 -I` from the session scratchpad with this worktree's `hooks/` on the
path. Those hooks are the base's: `git diff --stat a9d7b0e5 HEAD -- hooks` is
empty. For every Bash `tool_use` in every `*.jsonl` under
`~/.claude/projects/*SpecSeal*/`, distinct (command, cwd) pairs, each pair
walked by `walk_command`, each segment read by `parse_git`. The build's
shapes are the probe's own reading of `spec.md` In 1: `restore`, `checkout`
with a `--` and a word after it, and every subcommand on `git
--list-cmds=main,others` (git 2.50.1 on this machine) other than `switch`,
`checkout`, `bisect`, `symbolic-ref`, `update-ref` and `stash branch` are
listed. A non-git segment is a string handed to a shell
(`hooks/cmdline.py#command_strings`, and for `eval` its joined words), a
substitution body (`substitution_bodies`), or a `git` word behind
redirections and zsh precommand words; an untokenizable command holding the
bare word `git` is its own class. Today's guard is `classify` per segment
with every name lookup answering True (`is_ref`, `tracked_in_any_remote`,
`_the_bases_lookup`), so no git was spawned and today's stop count is its
maximum, plus `wider_only_kinds` (candidate C). Tree-blind throughout: a
transcript records no tree, so every stop count is an upper bound.

**Self-check, before any zero was trusted.** Of S3's 15 shapes the probe
stops all 15, and of S1's 11 listed shapes it stops none. The first run
stopped 14 of 15: `eval "git switch x"` went silent, because
`command_strings` hands back no string for `eval`. The probe was corrected
to join `eval`'s words and run again, and every figure below is from the
corrected runs. Phase 2 meets the same gap in the same reader (W3).

**M1 — the corpus.** Pair counts grew by a few dozen between runs, because
this session's own transcript is in the corpus; the figures are the last
run's.

| Project directory (user path rewritten) | Transcripts (main) | Bash uses, cut 1 | Bash uses, cut 2 |
|---|---|---|---|
| `-Users-x-Documents-GitHub-SpecSeal` | 514 (23) | 31,076 | 33,137 |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-3` | 8 (1) | 543 | 543 |
| `-Users-x-orca-workspaces-SpecSeal-main` | 2 (2) | 101 | 101 |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-2` | 1 (1) | 1 | 1 |
| `-Users-x--Trash-SpecSeal`, `-Users-x-Documents-GitHub-SpecSeal-OLD`, `-Users-x-Documents-GitHub-<org>-SpecSeal-OLD` | 0 | 0 | 0 |

| | Cut 1 (before 2026-10-03T11:06:22+09:00) | Cut 2 (to 2026-10-06) |
|---|---|---|
| distinct (command, cwd) pairs | 31,193 | 33,220 |
| pairs holding a git segment the frozen reading yields | 8,960 | 9,695 |

**Cut 1 reads ABOVE 25,741, not below it**, although the main transcripts
fell from 33 to 23 and all transcripts from 580 to 514 since 1791119071's
phase 1. That probe was deleted, so its definition cannot be re-run here, and
the difference is not reconciled. It is not absorbed either: every count in
this record is over this probe's definition, and phase 3's re-read has to use
the same one so that before and after compare.

Git subcommands, pairs holding at least one segment of each, cut 1 / cut 2
(the input to `LEAVES_THE_TREE`):

`log` 2858/3064 · `status` 2609/2848 · `commit` 2014/2149 · `diff` 2028/2127 ·
`add` 1842/1947 · `rev-parse` 893/961 · `show` 651/756 · `push` 573/607 ·
`checkout` 532/576 · `grep` 385/454 · `fetch` 252/276 · `clone` 223/243 ·
`branch` 223/236 · `worktree` 152/164 · `switch` 120/126 · `merge-base`
98/104 · `config` 84/100 · `stash` 95/99 · `ls-tree` 55/73 · `tag` 46/60 ·
`ls-files` 56/58 · `merge` 52/55 · `ls-remote` 44/47 · `archive` 43/47 ·
`pull` 43/44 · `cat-file` 38/41 · `for-each-ref` 26/40 · `describe` 26/27 ·
`rev-list` 23/24 · `reset` 23/23 · `remote` 17/19 · `init` 17/17 ·
`update-ref` 13/13 · `merge-tree` 7/11 · `apply` 8/11 · `check-ignore` 10/10
· `restore` 6/7 · `clean` 5/6 · `reflog` 6/6 · `revert` 6/6 · `blame` 3/5 ·
`rm` 5/5 · `cherry-pick` 4/4 · `mv` 1/2 · `show-ref` 2/2 · `rebase` 2/2 ·
`diff-tree` 1/2 · `gc` 1/1 · `format-patch` 0/1 · `count-objects` 0/1 ·
`update-index` 1/1 · `help` 1/1 · `symbolic-ref` 1/1 · `shortlog` 1/1 ·
`2>/dev/null` 1/1

`2>/dev/null` is no subcommand: the frozen reading takes a redirection
written after `git` as the subcommand word, so `git 2>/dev/null <sub>` reaches
the build as an unlisted subcommand rather than as a hidden git. It stops
either way, and its plain spelling is the redirection moved to the end.
`bisect` and `stash branch` were recorded zero times. Of the recorded
subcommands, the ones In 5 judges not to leave the branch are `switch`,
`checkout`, `symbolic-ref`, `update-ref` and `worktree add`. Recorded but not
named in In 5's list, and judged here as leaving the branch where it is:
`clone`, `init`, `config`, `archive`, `apply`, `gc`, `update-index`,
`format-patch`, `count-objects` and `help`. That judgment was read off what
each subcommand does, not executed against git.

**M2 — what the build stops, tree-blind.** Pairs, by the class of In 1 (a
pair can hold more than one class):

| Class | Cut 1 | Cut 2 | of cut 2, not stopped today |
|---|---|---|---|
| `checkout` without `-- <word>` | 280 | 297 | 1 |
| unlisted subcommand (`update-ref` 13, `symbolic-ref` 1, `2>/dev/null` 1; cut 2 adds this session's own `git -C <dir> --version`, read as subcommand `--version`) | 15 | 16 | 15 |
| string handed to a shell (`sh -c`, `bash -c`, `eval`, `env -S`) | 0 | 0 | 0 |
| substitution body holding `git`, every git inside listed | 529 | 575 | 548 |
| substitution body holding `git`, the rest | 15 | 15 | 15 |
| untokenizable, holding `git` | 5 | 5 | 5 |
| hidden git behind a redirection or precommand word | 0 | 0 | 0 |
| **pairs stopped by an unrecognised shape, as written** | **807** | **871** | **570** |
| **the same, with a body holding only listed git read as listed** | **315** | **333** | **36** |
| pairs today's guard stops (maximum: every lookup True) | 439 | 465 | — |
| pairs today's guard stops and the build does not, creations aside | 0 | 0 | — |
| pairs candidate C asks about | 0 | 0 | — |

The last column is the pairs today's guard does not stop even at its
maximum. As written, 548 of the 570 new stops are bodies holding only listed
git; read through the shapes, the new stops are 36. The 42 pairs whose text
holds `sh -c`/`bash -c` beside the word `git` are heredoc bodies and
`python3 -c` scripts, never a shell string holding a git invocation, which
is why the string class reads zero. No single shape that leaves the branch
accounts for ten or more stopped pairs: the one shape at ten or more,
`checkout` without `-- <word>`, is the one In 1 stops on purpose, and its
rewrite is named.

**M3 — stopped pairs with no plain rewrite the stop's text can name.**
Pairs per shape, cut 2 (cut 1 is the same except the listed-inside bodies,
529):

| Shape | Pairs | Why there is no rewrite |
|---|---|---|
| `git update-ref …` | 13 | the command is its own plain spelling. The ones read are in scratch clones and the release tag checks (`refs/tmp/*`, `refs/remotes/pull`), not in a tree another session holds |
| `git symbolic-ref …` | 1 | the same, in a scratch repository a probe built |
| substitution body, every git inside listed | 575 | In 3 names no plain spelling for a substitution, and the body is already plain |
| substitution body, the rest | 15 | the same; the bodies are `gh api …$(git rev-parse HEAD)` loops and probe one-liners |
| untokenizable command holding `git` | 5 | In 3 names none. Four hold a heredoc the frozen reading did not close (two commit messages, two file writes), and one is a multi-line test-and-commit script |

**M3 is 549 distinct pairs over cut 1 and 595 over cut 2 as the frame is
written, and 34 over either cut if a body holding only listed git is read
as listed.** Neither is zero, so phase 2 stops for the owner's rows
(`questions.md` P2–P4), as the frame says.

**M4's base figures, read and not run.** #841's first comment (read with
`gh issue view 841 --comments`, 2026-10-06) carries the orchestrator's
macOS run at the 0.19.0 preparation branch, `bin/test -q --durations=40`:
12,958 passed and 82 skipped in 456 s; 164.87 s for
`test_no_twin_is_asked_unless_an_operator_cuts_the_segment`, 24.88 s for
`test_nothing_the_base_read_as_a_switch_goes_quiet`, and 203.0 s for the
module's three slowest cases. Phase 3 measures the module after, against
these.

**What phase 2 needs from this record.** The probe's shape function is the
first draft of `shape_of`, and its two misses are the ones phase 2 meets:
`eval` needs its words joined because `command_strings` returns none for it,
and a redirection written after `git` arrives as the subcommand word.

The probe, its three result files and its log lived in the session
scratchpad and were deleted when this record was written. No scratch
repository was made, and no git was spawned against the corpus.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probe lived outside it | none |

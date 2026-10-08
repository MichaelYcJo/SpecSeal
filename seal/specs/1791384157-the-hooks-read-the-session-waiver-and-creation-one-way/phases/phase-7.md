# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 452cf167 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Measure the reframed rule before building it (round 3's ⬜ 6, ⬜ 5's count;
S22): a deleted `test_tmp_*` probe by phase 1's method over the recorded
corpus, tree-blind, with the hooks at a8f86f44 on the path. M4: the pairs a
brace in any word of any segment stops, split by whether the stopping
segment's command word is `git`, with the assignment-word pairs and the
quoted-beside-unquoted pairs counted apart, after a self-check on S17's
round-3 spellings (each must stop) and S19's quoted forms (none may). M5,
run in a scratch directory: `A={a,b}; printf %s "$A"` under bash and under
zsh. Nothing in the tree but the record.

## What this phase found

**The reframed rule stops 34 of 32,715 recorded pairs, tree-blind, and one
of them is a git segment** (corrected in round 4; this paragraph said 31 of
32,498 and none git). The one is `git add` of a path holding
`{plan,questions}`, from a 2026-09-23 transcript, a command the
owner-confirmed rule (c) stopped before the reframe. The other 33 are a brace
in an argument of a command that is not git: paths for `rm -f`, `ls`,
`grep`, `cat`, `sed` and `for`, such as
`ls seal/specs/<id>/{spec,plan,questions}.md`. No recorded pair holds a
brace in an assignment word, and none holds a quoted brace beside an
unquoted one, so two of In 5's three named costs cost no recorded command;
one pair holds a zsh `${(f)…}` expansion in an assignment beside another
brace in the same command. As an upper bound, because the corpus records no
tree: a pair stops only where its tree matters.

**Why the first count missed the git pair (round 4).** The probe behind 31
read the judgment text through `_judgment_text` a second time, which step 2
below does not say. The git pair sits after a heredoc on its line; the first
pass removes the heredoc body, and the second, reading the `<<` again with no
body after it, drops the rest of the line, `git add` with it. The corrected
count reads the command once and each substitution body once, as step 2
says, over the corpus as it stood when round 4 ran it and the rule as round
4 left it (`_BRACE` read to err toward stopping). Phase 1's M2 missed the
same pair; the probe that ran it is deleted, so whether by the same second
pass is not established.

**M5: neither shell expands a brace in an assignment word.** Executed in a
scratch directory the probe created and removed: `bash -c 'A={a,b}; printf
%s "$A"'` printed `{a,b}`, exit 0, and the same under `zsh -c` printed
`{a,b}`, exit 0. In 5's assignment cost is a stop on a word the shell leaves
alone, as written; nothing about it is `unverified`.

**The method, written down (round 3's ⬜ 6).** The 34,633 and 34,775 figures
that §A, the changelog and ledger row S11b carried before the reframe were
counted by probes that left no method behind; this is the method behind the
figure that replaces them, so the next count can be compared with it.

1. The corpus: every Bash `tool_use` in every `*.jsonl` under
   `~/.claude/projects/*SpecSeal*/`, subagent transcripts included,
   collected as distinct (command, cwd) pairs.
2. For each pair, the judgment text (`_judgment_text`: comments and
   heredoc bodies out), and each substitution body of it
   (`cmdline.substitution_bodies`), each read again through
   `_judgment_text`.
3. A text counts only where `_unquoted_brace` finds a brace expansion
   outside its quoted spans and escapes (`tokens.QUOTED_SPANS`).
4. Each segment of such a text, through the guard's own tokenizer
   (`_tokenize_with_separators`), stops where one of its words holds a
   match of `_BRACE`. The segment is a git segment where `parse_git` reads
   it as one.
5. Counted apart: pairs with a stopping word that is an assignment
   (`NAME=…{…}…` before any option), and pairs whose quoted spans hold a
   brace expansion beside the unquoted one.
6. The self-check first, over the same function: all nineteen spellings
   rounds 1–3 found stop (S17's thirteen and the six before them), and none
   of the six quoted forms of S12 and S19 does.

No git was run against the corpus, and the tree of no pair was read.

**Self-check:** passed — 19 of 19 must-stop spellings stop, 0 of 6 quoted
forms do.

**The corpus.**

| Project directory (user path rewritten) | Transcripts (main) |
|---|---|
| `-Users-x-Documents-GitHub-SpecSeal` | 511 (22) |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-3` | 8 (1) |
| `-Users-x-orca-workspaces-SpecSeal-main` | 2 (2) |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-2` | 1 (1) |
| `-Users-x--Trash-SpecSeal`, `-Users-x-Documents-GitHub-SpecSeal-OLD`, `-Users-x-Documents-GitHub-<org>-SpecSeal-OLD` | 0 |

32,498 distinct pairs when this phase ran, 10,739 of them holding the bare
word `git`; 32,715 when round 4 re-counted.

**M4**, as corrected in round 4 (this phase's run gave 31, 0, 31, 0, 0).

| | Pairs |
|---|---|
| stopped by the reframed rule | 34 |
| of them, a git segment stops | 1 |
| of them, a segment that is not git stops | 33 |
| of them, an assignment word stops | 0 |
| of them, a quoted brace stands beside the unquoted one | 0 |

Phase 1 counted 33 pairs holding an unquoted brace outside every git word
over 32,431 pairs, and none inside one; round 4 counts 34 over 32,715, one
of them git. The corpus moves between runs (transcripts leave, this
session's enter), so the totals are not a difference in the rule; the git
pair is a difference in the count.

The probe and its scratch directory lived outside the tree and were deleted
when this record was written.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probe lived outside it | none |

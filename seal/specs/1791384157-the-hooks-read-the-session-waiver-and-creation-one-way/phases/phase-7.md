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

**The reframed rule, as round 5 left it, stops 42 of 33,287 recorded pairs,
tree-blind, and one of them is a git segment** (corrected in rounds 4 and 5;
this paragraph said 31 of 32,498 and none git, then 34 of 32,715). The one is
`git add` of a path holding `{plan,questions}`, from a 2026-09-23
transcript, a command the owner-confirmed rule (c) stopped before the
reframe. 34 of the 42 are what round 4's reading stopped too: a brace in an
argument of a command that is not git, paths for `rm -f`, `ls`, `grep`,
`cat`, `sed` and `for`, such as `ls seal/specs/<id>/{spec,plan,questions}.md`.
The other eight are round 5's reading: seven brace groups holding a comma
(`s(){ …; }`, `{ git log …; } | grep`), judged as the command's because no
one segment's words hold the brace, and one parameter expansion holding a
`..` (`${r%..*}`). Nothing round 4's reading stopped is silent under round
5's. Two pairs stop on a brace in an assignment word alone, and one holds a
quoted brace beside an unquoted one. As an upper bound, because the corpus
records no tree: a pair stops only where its tree matters.

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
   (`_tokenize_with_separators`), stops where `_segment_finding` gives it
   the brace finding, which since round 5 is where its words, joined, hold a
   match of `_BRACE`; a cut group stops where `_merged_findings` gives it
   one; and since round 5 a text whose brace no one segment's words hold
   stops as a whole, as `main` takes it. The segment is a git segment where
   `parse_git` reads it as one. A text the splitter could not close and that
   holds a match of `_BRACE` stops too, counted apart where nothing else
   stopped it.
5. Counted apart: pairs whose stopping segment holds the brace only in
   assignment words before its command (`NAME=…{…}…`), and pairs whose
   quoted spans hold a match of `_BRACE` beside the unquoted one.
6. The self-check first, over the same function: every form below under
   *must stop* stops, and none under *must not stop* does. The lists are
   the parameters of the guard's own cases at the commit counted from, so
   the next count can be run against the same forms: must stop is
   `BRACE_SHAPES` and the parameters of
   `test_a_brace_that_makes_the_command_word_is_unrecognised`,
   `test_a_brace_in_any_word_is_the_brace_shape` and
   `test_a_brace_in_a_body_or_a_cut_group_is_unrecognised`, with the command
   of `test_a_brace_in_a_command_that_will_not_split_stops`; must not stop
   is the parameters of `test_what_the_shell_does_not_expand_stays_silent`
   and `test_a_quoted_brace_in_a_git_word_stays_listed`, all in
   `tests/test_worktree_guard.py`.

No git was run against the corpus, and the tree of no pair was read.

**Self-check:** passed in round 5 — 57 of 57 must-stop forms stop, 0 of 20
must-not forms do. This phase ran 19 and 6, the round 4 count 21 and 15,
each from a probe that was deleted with its lists; the lists below are the
ones round 5's count ran (round 5, white 4).

Must stop, 57 forms:

- `git rebase {main,feature/x}`
- `git rebase --ro{,} feature/x`
- `git stash {branch,} x`
- `git worktree {add,} ../wt f`
- `{git,} rebase main feature/x`
- `{,git} switch feature/x`
- `{{git,},} switch feature/x`
- `{,{git,}} switch feature/x`
- `{g..g}it switch feature/x`
- `${HOME}/bin/{git,} switch feature/x`
- `timeout 5 {git,} switch feature/x`
- `nice -n 5 {git,} switch feature/x`
- `sudo -u x {git,} switch feature/x`
- `env -u FOO {git,} switch feature/x`
- `command -p {git,} switch feature/x`
- `2>/dev/null {git,} switch feature/x`
- `>/dev/null {git,} switch feature/x`
- `({git,} switch feature/x)`
- `{,} git switch feature/x`
- `{env,} git switch feature/x`
- `{nice,} git switch feature/x`
- `{exec,} git switch feature/x`
- `2>&1 {git,} switch feature/x`
- `echo {a,b}`
- `ls {x,y}`
- `ls {x,y}.md && git status`
- `cat {.gitignore,README.md}`
- `{echo,printf} x`
- `echo {{a,b},c}`
- `echo {git,} x`
- `A={a,b} ls`
- `A={{a,b},c} ls`
- `for f in x/{a,b}.md; do echo $f; done`
- `git rebase main{+1..2}`
- `echo {1..+3}`
- `echo \${a,b}`
- `echo {"a b",c}`
- `$''{g..g}it switch feature/x`
- `$''{g..g}it rebase main feature/x`
- `$""{git,} -C . switch feature/x`
- `echo $'x'{a,b}`
- `{git,$(: x)} switch feature/x`
- `` {git,`: x`} switch feature/x ``
- `{git,${x:- }} switch feature/x`
- `echo ${a,}`
- `git log ${x,}`
- `echo {a, b}`
- `git commit -m '{a,b}' && echo {c, d}`
- `git commit -m '{a,b}' && { echo x,y; }`
- `git diff HEAD@{1}..HEAD@{0}`
- `git log @{u}..@{1}`
- `echo ${r%..*}`
- `echo "$({ echo x,y; })"`
- `{ echo x,y; }`
- `echo $(git rebase {main,feature/x})`
- `git worktree &>/dev/null {add,} ../wt f`
- `: $'\'' && {g..g}it switch feature/x && : "'"`

Must not stop, 20 forms (the heredoc's line breaks written as `\n`):

- `echo ${HOME}`
- `echo {}`
- `echo {a}`
- `find . -name x -exec echo {} \;`
- `awk '{print $1, $2}' f.txt`
- `echo '{"a":1,"b":2}'`
- `jq '{a: .x, b: .y}' f.json`
- `cat <<EOF\n{a,b}\nEOF`
- `echo \{a,b\}`
- `git log @{-1}..HEAD`
- `echo "${a,}"`
- `echo ${a},${b}`
- `git commit -m '{a,b}'`
- `git log --format='{%h}'`
- `git commit -m "{a, b}"`
- `git log --format=%h -- 'docs/{a,b}.md'`
- `git commit -m x && echo '{a,b}'`
- `echo '{a,b}'`
- `printf "{a, b}"`
- `cat 'x/{a,b}.md'`

**The corpus.**

| Project directory (user path rewritten) | Transcripts (main) |
|---|---|
| `-Users-x-Documents-GitHub-SpecSeal` | 511 (22) |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-3` | 8 (1) |
| `-Users-x-orca-workspaces-SpecSeal-main` | 2 (2) |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-2` | 1 (1) |
| `-Users-x--Trash-SpecSeal`, `-Users-x-Documents-GitHub-SpecSeal-OLD`, `-Users-x-Documents-GitHub-<org>-SpecSeal-OLD` | 0 |

32,498 distinct pairs when this phase ran, 10,739 of them holding the bare
word `git`; 32,715 when round 4 re-counted; 33,287 from 530 transcripts (26
main) when round 5 did.

**M4**, as corrected in round 5 (this phase's run gave 31, 0, 31, 0, 0;
round 4's 34, 1, 33, 0, 0).

| | Pairs |
|---|---|
| stopped by the reframed rule | 42 |
| of them, a git segment stops | 1 |
| of them, a segment that is not git stops | 41 |
| of them, the command as a whole stops (no one segment holds the brace) | 7 |
| of them, an assignment word alone stops | 2 |
| of them, a quoted brace stands beside the unquoted one | 1 |
| of them, an untokenizable text alone stops | 0 |
| stopped by round 4's reading over the same corpus | 34 |
| stopped by round 4's reading and silent under round 5's | 0 |

Phase 1 counted 33 pairs holding an unquoted brace outside every git word
over 32,431 pairs, and none inside one; round 4 counts 34 over 32,715, one
of them git; round 5 counts 42 over 33,287, eight of them the wider
reading's. The corpus moves between runs (transcripts leave, this
session's enter), so the totals are not a difference in the rule; the git
pair and the eight are.

The probe and its scratch directory lived outside the tree and were deleted
when this record was written. Round 5's probe read the guard at `bb7b2990`
(the guard's code as `b6079033` left it), round 4's guard from `08f34e45`
beside it, and its lists from the cases at `bb7b2990`; it was deleted too.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probe lived outside it | none |

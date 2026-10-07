# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 84535260 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Measure before building, with nothing in the tree but the record: a deleted
`test_tmp_*` probe by the method of work item 1791270162's phase 1 over the
recorded corpus, tree-blind. M2 counts the pairs holding a git segment with
an unquoted brace expansion, by subcommand (In 5's new stop class, an upper
bound). M3 counts the pairs that do not split and carry a waiver token as a
substring (In 3's cost). The self-check on S11's and S12's shapes runs before
any zero is trusted, and M1 is answered where it can be.

## What this phase found

**The frame does not hold on one sentence of In 3, and the measurement is
what shows it.** In 3 says the one token reader reads "nothing where the
command does not split". Four of the six recorded commands whose answer that
rule moves are the guard's documented form, a token in a trailing comment,
with an English apostrophe later in the same comment:

```
git switch main --quiet 2>&1 | tail -1 # [shared-tree-ok] the release's own tree; …
git worktree add /Users/x/… docs/292-… 2>&1 | tail -3  # [worktree-ok] — … #145's review is live …
```

`hooks/tokens.py#words` clears `commenters`, so the apostrophe opens a quote
that never closes and the whole command reads nothing. bash runs the command,
because the apostrophe is inside a comment. The guard's `has_token` read the
token there, because the frozen splitter hands back the segments it read
before it gave up, and S9 says such a token is "read as today". The two
sentences of the frame disagree on exactly these commands.

Phase 5 builds the reading S9 describes rather than the sentence of In 3: the
one reader takes the bare words read **before** the split fails. That reads
no word inside an unclosed quote, so S7's `git commit -m 'x [no-review]`
still waives nothing, and over the corpus it never reads a token that the
base's reads did not. The divergence is recorded in `overview.md` with both
sentences quoted.

**Method.** Executed by a deleted probe, `test_tmp_868_corpus.py`, run as
`python3 -I` from the session scratchpad with this worktree's `hooks/` on the
path. Those hooks are the base's: nothing under `hooks/` had changed on this
branch when it ran. For every Bash `tool_use` in every `*.jsonl` under
`~/.claude/projects/*SpecSeal*/`, subagent transcripts included, distinct
(command, cwd) pairs. Nothing was spawned against the corpus and no scratch
repository was made.

- M2's reading is the rule phase 3 builds: the judgment text
  (`_judgment_text`) with its escapes and quoted spans removed by the
  pattern `hooks/tokens.py#is_plain` already uses holds a brace expansion
  (`{a,b}` with no whitespace inside, `{1..3}`, `{a..c}`, never after `$`),
  and a word of a segment the frozen reading reads as git holds one. Each
  substitution body of the text is read the same way. The base's own
  `_git_finding` says whether the segment was already stopped.
- M3 compares, for every pair holding a known token as a substring, the
  base's `has_marker` (its `_reads_marker`, substring fallback included) or
  the guard's `has_token` with `tokens.given`, and with a variant that keeps
  the words read before the split fails.

**Self-check, before any zero was trusted.** All four S11 forms are found
(`git rebase {main,feature/x}`, `git rebase --ro{,} feature/x`,
`git stash {branch,} x`, `git worktree {add,} ../wt f`), and none of the three
S12 forms is (`git commit -m '{a,b}'`, `git log --format='{%h}'`,
`git commit -m "{a, b}"`). The first run's pattern allowed whitespace inside
the braces and matched a brace GROUP (`{ echo ; gh issue list … --json
number,title ; }`); bash expands no brace holding unquoted whitespace, so the
pattern was narrowed and every figure below is from the corrected run.

**M1 — the corpus.**

| Project directory (user path rewritten) | Transcripts (main) |
|---|---|
| `-Users-x-Documents-GitHub-SpecSeal` | 516 (23) |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-3` | 8 (1) |
| `-Users-x-orca-workspaces-SpecSeal-main` | 2 (2) |
| `-Users-x-orca-workspaces-SpecSeal-OLD-main-2` | 1 (1) |
| `-Users-x--Trash-SpecSeal`, `-Users-x-Documents-GitHub-SpecSeal-OLD`, `-Users-x-Documents-GitHub-<org>-SpecSeal-OLD` | 0 |

32,431 distinct (command, cwd) pairs, 10,614 of them holding the bare word
`git`. The count is not comparable with 1791270162's 33,220: transcripts
leave the directory between runs, and this session's own enter it.

**M2 — In 5's new stop class: zero.** No recorded pair holds a git segment
with an unquoted brace expansion, by any subcommand, so the brace stop costs
no recorded command a stop, and the named over-stop (a quoted brace in one
git segment beside an unquoted one elsewhere) is zero as well. 33 pairs hold
an unquoted brace expansion outside every git word: paths for `sed`, `ls`,
`rm`, `tail` and `for` (`seal/specs/<id>/{spec,plan,questions}.md`). The
rule reads a git word, so none of them stops.

**M3 — In 3's cost.** Pairs holding a known token as a substring, and how
each reader answers:

| Token | Pairs | Base read it | Framed rule (nothing where it does not split) | Built rule (words before the split fails) |
|---|---|---|---|---|
| `[no-review]` | 64 | 31 | 29 | 30 |
| `[no-parity]` | 4 | 1 | 1 | 1 |
| `[shared-tree-ok]` | 11 | 4 | 1 | 4 |
| `[worktree-ok]` | 26 | 10 | 9 | 10 |

Neither rule reads a token in a pair the base did not. The framed rule
refuses six pairs the base read, every one a command that does not split; the
built rule refuses one: `cat > /tmp/msg.txt <<'MSGEOF'` with an apostrophe in
the body (`a shipped section's deletion`) ahead of `: '[no-review]'; git
commit …`. That command's waiver came from `has_marker`'s substring fallback,
and it meets the refusal naming `git -c specseal.waive=review`. Where git's
own hooks decide, it already did: `hooks/answer-write.py` hands the hook
`tokens.given`, which reads nothing there either.

**M1 of `questions.md`, the session's process.** Executed in a Bash child of
this harness: `CLAUDE_PID` is exported beside `CLAUDE_CODE_SESSION_ID`, and
it names the process `ps -o ppid=,comm=` finds as the nearest `claude`
ancestor of the shell (one pid on both sides, read off the process table).
Whether a hook process the harness spawns sees the variable is not readable
from here: no hook of this session can be made to print its environment
without changing the installed configuration, which this session may not do.
It stays `unverified` with the repository owner named; the code is the same
either way, because the walk stays under the variable.

**What the later phases need from this record.** Phase 3's brace pattern is
the probe's corrected one. Phase 5 builds the partial read above, and its
M3 figure is one pair.

The probe, its result file and two helper scripts lived in the session
scratchpad and were deleted when this record was written.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probe lived outside it | none |

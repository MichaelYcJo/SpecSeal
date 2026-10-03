# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | the commit that carries this record; the probe is deleted and commits nothing |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Count, over the corpus `questions.md` D1 fixes, how many distinct (command,
directory) pairs each candidate fires on, by calling phase 2's functions from
a deleted `test_tmp_*` probe. Record the transcripts read (main and subagent),
the pairs, the pairs holding a frozen switch and a frozen creation, count A,
count C and every pair that fired, with paths rewritten to `/Users/x/`. Before
trusting a zero, run the functions on #686's seven shapes and S9a's shapes
inside the probe and show each fires. Write each candidate's decision as the
owner's rule's output, in one line.

## What this phase found

**The corpus.** Every `*.jsonl` under this repository's project directory on
this machine: 511 transcripts, 34 main and 477 subagent. Every Bash `tool_use`
whose entry is timestamped before 2026-10-03T11:06:22+09:00 (D1's cut): 27,551
tool uses, 27,351 distinct (command, directory) pairs. Of those, 395 hold a
segment the frozen reading calls a switch by its words alone, and 51 a
creation. No pair raised.

**The probe fired on every shape it was meant to.** Inside the same run, A
answered true for all seven of #686's shapes, and C found the expected kind
for all nine of S9a's shapes (two creations, seven switches).

**Count A = 9.** Every one reached A through the frozen walk's `Unresolved`,
none through the disagreement. Rewritten to `/Users/x/`, the judged segments
were:

| Shape | Pairs |
|---|---|
| `git checkout -q <sha>` inside a `for` loop over SHAs in a scratch clone (`for c in … ; do git checkout -q $c; …; done`) | 3 |
| `git checkout -q <sha>` after a `cd` the walk could not follow: one into `$S/clone` (a variable), one behind an `if [ ! -d clone ]; then …; fi` | 2 |
| `git -C "$S/$1" checkout -q $2` inside a `for` loop | 1 |
| `git switch -q main` after a `for` loop in the same command | 1 |
| `git checkout -q hooks/` and `git checkout -q hooks/ tests/` after a function definition | 2 |

The last two are file restores, which `classify` would not call a switch; D3
counts them because a transcript records no tree. Without them the count is
7, and the rule's branch is the same.

**Count C = 0.**

**Decision for A: count 9 ≥ 1 → removed, and the fallback is named in
`docs/worktree-guard-spec.md` §*Known limits*.**

**Decision for C: count 0 → built.**

The probe, its result file, its self-check directory and the other scratch
directories this phase and the two before it made under the session
scratchpad were deleted after this record was written. Nothing from the
corpus was committed except these counts and the shapes above, rewritten.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree; the probe lived outside it | none |

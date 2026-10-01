# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | fc873413 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

Measure the hook surface and the corpora before any file under `hooks/`
changes. Answer M1–M3, M5, M10 and M11 with `test_tmp_` probes on the git
here (2.50.1) and on the oldest git CI can install, all deleted afterwards.
Count M6 and M7, grep M8, and restate the spec's comparison table with
numbers. Name the git floor for P4, and pin M1–M3's table in one
version-keyed case. P3 and P4 were delegated to this build. P3 is decided
from a count of where the old spellings are promised, and P4 from M1/M3's
floor. **Stop here, rather than build past it, if a measurement contradicts
the design.** The spawn prompt named the example that applies: "M1/M3 say
`reference-transaction` cannot refuse before the tree moves on any supported
git." Probes ran in scratch repositories only, never in a real clone's
`.git/hooks`.

## What this phase found

### The stop: no git refuses a switch before its tree moves

`git switch` and `git checkout <branch>` rewrite the working tree and the
index first, and update `HEAD` afterwards. `reference-transaction` only
ever sees the second step.

- **2.34.1, 2.39.5, 2.43.0.** A switch sends no line to the hook at all. A
  hook that refuses every `HEAD` line lets the switch complete (rc 0).
- **2.50.1.** The line `<zero> ref:refs/heads/other HEAD` arrives at
  `prepared`, but by then the tree and the index already hold `other`.
  Refusing there gives rc 128 (`fatal: ref updates aborted by hook`).
  `HEAD` stays on `main` while `other`'s files are checked out and staged
  (`M  marker.txt`). In a dirty tree the carried change survives on top of
  that.

So the design's switch arm (S10's refuse branch, spec §*Scope* 1's
`reference-transaction` switch refusal) has nowhere to stand on any measured
git. This is the spawn prompt's stop condition, and **phases 2–6 were not
built**. `tests/test_the_hook_surface_git_offers.py#test_no_git_refuses_a_switch_before_the_tree_moves`
pins the fact. A git that one day refuses before the tree moves turns it
red, and that is the moment the arm becomes buildable as framed.

### The measurements, M1–M11

Probes were driven from Python against real git. The host ran 2.50.1 (Apple
Git-155); the other gits ran in `debian:12` (2.39.5), `ubuntu:22.04` (2.34.1)
and `ubuntu:24.04` (2.43.0) containers, each `--rm`. The three images were
pulled for this phase and removed afterwards. CI runs `ubuntu-latest`
(`.github/workflows/*.yml`, read). Which git that runner image carries was
not measured, so the distro gits stand in for "the oldest git CI can
install". Answerer: the orchestrator, from a CI log's `git --version`.

| # | Label | Answer |
|---|---|---|
| M1 | executed, 4 gits | As above. On 2.50.1 the hook order for a switch is `reference-transaction` prepared → committed for `HEAD`, then the `AUTO_MERGE` transactions, then `post-checkout`. The first version that sends the symref line lies between 2.43.0 and 2.50.1. That range was not narrowed further, because no git in between was run, and the answer would not change the finding |
| M2 | executed, 4 gits | `git commit --no-verify` refused at `prepared` on `refs/heads/main`: rc 128, `HEAD` unmoved, `git status --porcelain` and `git write-tree` byte-identical before and after, one dangling commit object. git prints `fatal: ref updates aborted by hook` after the hook's own stderr. In `pre-commit`, `git diff --cached --name-only` lists `f.py g.py` for `commit -a` and `f.py` for a pathspec commit (`GIT_INDEX_FILE` is `index.lock` and `next-index-<pid>.lock` respectively). **Also executed, 2.50.1:** `merge --ff-only`, `reset --hard`, `cherry-pick` and `commit --amend` reach `prepared` with the same `<sha> <sha> refs/heads/<b>` line a commit sends. `branch -f` and `update-ref` send it with a zero old value |
| M3 | executed, 4 gits | `worktree add <p> -b nb` first creates `refs/heads/nb` in its own transaction, in the original worktree's process. **2.50.1:** the new worktree's `<zero> ref:refs/heads/nb HEAD` arrives at `prepared` from the original worktree's process (its `$PWD`, `GIT_DIR` unset), before any file of the new tree exists. Those bytes are the same as a switch's line on that git. **2.34–2.43:** there is no symref line. The `HEAD` line comes from the `reset --hard` git runs inside the new worktree (`<sha> <sha> HEAD`, `GIT_DIR=<common>/worktrees/<name>`), after its files are written. **All four:** refusing at that line gives rc 128 and removes the directory and `<common>/worktrees/<name>`, so `git worktree list` shows one entry, but the `-b` branch remains. `post-checkout` runs with `$PWD` in the new worktree, `$1` the null oid and `$3` = 1; for a switch `$1` is the previous `HEAD` |
| M4 | executed, 2.50.1 host | `CLAUDECODE=1`, `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID`, `CLAUDE_CODE_SESSION_ATTENDED=1` and `CLAUDE_CODE_CHILD_SESSION=1` reach `pre-commit`, `post-commit` and `post-checkout` from this agent's Bash tool. `GIT_DIR` was **not** exported to those three hooks (empty in every log), contrary to spec §*What the tree answered* 3. **Unverified:** the harness version that first exports the variables (only 2.1.283–2.1.286 are installed here), and what `CLAUDE_CODE_SESSION_ATTENDED` reads in a headless run. Answerer: the orchestrator |
| M5 | not run | It needs an `Agent` spawn with `isolation: "worktree"`, and contract §6 withholds spawning from this agent. Answerer: the orchestrator |
| M6 | not run | The stop came first. The replay compares the candidates' stop counts, and which arms it has to cover depends on the owner's answer for the switch arm. Answerer: the owner's answer, then this phase resumed |
| M7 | executed | `ab2760f5` and its 67 subagent transcripts, read from the `PreToolUse:Bash` hook records (`permissionDecision`): **15 `ask`s**. 13 were review asks naming the main checkout (12 approved, 1 declined), 1 an unreadable-construct ask (approved), and 1 the guard's tracked-changes ask (approved). The waits from hook to tool result total **102.2 minutes** (longest 48.3 minutes, median 35 seconds). This matches the memory note's "15 gate asks and 102 minutes". No `deny` decision appears in that record shape, so the framer's "at least 3 denies" was not found there. Which shape they took is unverified, answerer the orchestrator. `8cadfa28` and `30ac0e06` have 0 `ask`s and 0 `deny`s in the same shape |
| M8 | executed, heuristic | Across the three sessions: 56 `git clone` commands and 395 `git -C <x> commit` commands. Commits into a clone target that no record's `cwd` ever entered: **0**. The match is a `-C` path whose last component equals a clone target's. The known limit stands as stated |
| M9 | not run | Windows. Answerer: the CI Windows leg |
| M10 | executed, 2.50.1, two runs on a loaded machine | A commit with no hooks takes 57–58 ms. With a Python stub on all four hooks at every state it takes 526–921 ms; with `reference-transaction` leaving before Python except at `prepared`, 209–400 ms. A fetch of 100 new refs takes 90–117 ms with no hooks, 5.8–6.2 s with Python at every state, and 3.4–8.3 s at `prepared` only, because each fetched ref is its own transaction. This is over the row's ~200 ms, so a stub has to narrow to `refs/heads/` lines in `sh` before Python starts |
| M11 | executed, 4 gits | `git -c specseal.waive=review commit …` makes `git config --get specseal.waive` answer `review` inside both `pre-commit` and `reference-transaction` (`GIT_CONFIG_PARAMETERS='specseal.waive'='review'`). The same words inside `-m` answer nothing |

### The comparison table, with what is now a number

Only M7's numbers are measured; the per-candidate stop counts (M6) are not.
Under 0.15.7 the recorded run paid **15 prompts and 102.2 minutes of
waiting**. 13 of the 15 named the main checkout for commits that landed in a
declared worktree, and under candidate A a `pre-commit` running in that
worktree would not have stopped them. That is still the spec's argument
from the hook's working directory, which M3 and M4 confirm. It is not a
replay. The other two cells change as follows:

- **A's switch arm** is no longer "refuse at `prepared`". It is one of the
  options below.
- **C′'s fallback** is not "below the floor". It is every git, for the
  switch arm.

### P3 — decided: (a), both spellings, with the git-native one advised

Where the old spellings are promised (executed, `git grep -l` at
`bb5a0c3e`):

- **In the tree:** 122 files carry at least one of the four tokens.
  `[no-review]` is in 94, `[no-parity]` in 19, `[worktree-ok]` in 34 and
  `[shared-tree-ok]` in 28. Of those, `tests/` holds 16/6/3/4, `hooks/`
  3/1/4/1, `docs/` 7/1/1/1, `skills/` and `agents/` 6/5/0/0, and
  `templates/` 2/1/0/0.
- **Outward-facing:** `README.md` has 9 lines and `README.ko.md` 10.
  `templates/claude-md-block.md` has 1. That block is what a person copies
  into their own `CLAUDE.md`, and this machine's `~/.claude/CLAUDE.md`
  carries it verbatim (1 line).
- **Other repositories on this machine:** 0 of 5 `CLAUDE.md` files.

The deciding count is the copied block. A spelling promised in a file the
plugin cannot rewrite can only be withdrawn by the person who owns that
file. Option (b) would break every such copy at once, and the one copy that
was measured is the user's own. Option (a) costs one text read of tokens,
and a misread there costs a refusal naming the `-c` spelling, never a
silent pass.

This decision binds only once the build reaches phase 4. It is recorded here
because the build stopped before then and the count was taken in this phase.

### P4 — not decided, and returned to the owner

P4 asks what the switch and creation arms do *below the floor*, where M1
names the first git that refuses cleanly. M1 names none, so every git sits
below the floor for the switch arm. Choosing among P4's options now would
not set a fallback. It would design the switch arm for every git, and that
is the call the spawn prompt reserved for the owner.

The creation arm needs no floor: all four gits refuse a creation cleanly,
apart from the leftover `-b` branch.

The switch arm's options, as the measurements leave them:

1. **The frozen reading for the switch arm on every git.** Commits and
   creations are decided at git; `hooks/cmdline_base.py` stays permanently
   in `pre-bash` for switches alone. #686 stays open for switches.
2. **Undo after** (plan row U). `post-checkout` reverts a switch the ladder
   refuses. Another session's tree is moved for the length of the hook, and
   a dirty tree is carried twice.
3. **Report only.** `post-checkout` says what the guard would have said, and
   nothing is refused.
4. **Refuse at `prepared` on 2.50.1+, then restore the tree from inside the
   hook.** This is an undo inside the transaction. It was not measured, and
   it has no counterpart below 2.50.

This agent would choose 1. Of the four, it is the only one whose behaviour
is already measured (0.16.0's), and it keeps prevention for the arm whose
wrong allow breaks another session's tree. Its cost is that the frozen file
becomes permanent rather than a floor fallback. This is a recommendation,
not a decision.

### What the next build phase needs, whichever answer comes back

- **A creation's `HEAD` line and a switch's are the same bytes on 2.50.1.**
  So a creation refusal at `reference-transaction` has to tell them apart
  by another signal: the index already differing from `HEAD` (a switch), or
  a fresh `<common>/worktrees/<name>` with no checkout (a creation). On
  2.34–2.43 the creation's line arrives from inside the new worktree in a
  different shape.
- **The `--no-verify` backstop as framed would refuse more than commits.**
  It keys on `<old> <new> refs/heads/<b>` at `prepared`, and that line is
  also sent by `merge --ff-only`, `reset --hard`, `cherry-pick` and
  `--amend`. A backstop keyed on the shape refuses those in an undeclared
  checkout, which 0.16.0 never did. It also cannot tell whether `pre-commit`
  already ran. It needs a rule to separate them, and that rule is part of
  the design call.
- **`GIT_DIR` is not in a hook's environment** for `pre-commit`,
  `post-commit` and `post-checkout` on 2.50.1. A hook asks
  `git rev-parse --git-dir` rather than reading it.
- **The latency (M10) requires the `sh` narrowing** before Python starts.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — phase 1 changed no file under `hooks/`; the probes and the three container images it made for itself are gone | none |

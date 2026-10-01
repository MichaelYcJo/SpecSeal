# Round 2 report — a gate decides at the moment of the action (#692)

| Field | Value |
|---|---|
| Round | 2, verifying |
| Target SHA | `bd588eb0e3ce3d1c4e5b21b9f05ca296c970d81f` |
| Diff verified | round 1's fix range `12c09ec3..e9977509` (six commits), the post-merge fix `12b35e31`, and the two release merges `c3f3fef5` and `bd588eb0` |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at the target under this round's scratch directory; real git 2.50.1 (Apple Git-155) through the clone's own stubs, in scratch repositories only, every one removed at hand-over |

## How the answers relate, in one picture

```
round 1's thirteen fixes ── every instance re-run, every one closed
   │
   ├─ the creation arm went back to the frozen reading (P6)
   │     → round 1's 1, 4, 5, 6 closed: refused before git runs, nothing moves
   │
   ├─ the commit reading no longer stands aside for three words (P6)
   │     → round 1's 2 and 8 closed for the words named
   │     → but the class is wider than the three words, and 0.16.0 stopped all of it
   │           → 🟡 1  the session variable removed another way (NAME=, env -u, unset)
   │           → 🟡 2  core.hooksPath reached through a config file, or the execute bit taken
   │
   ├─ the backstop, the mark, the stub mode, the lease short-cut, the per-call answer
   │     → round 1's 3, 7, 9, 10, 11 closed
   │     → ⬜ 3  the answer's match is wider than the limit's "byte-for-byte"
   │     → ⬜ 4  a person's commit with a lease starts three interpreters, not two
   │     → ⬜ 5  a conflicted merge's conclusion is judged, and no sentence says so
   │
   └─ the merges and the rider
         → no hook of this branch changed; the rider sentence is true
```

## What the account claimed, and what I found

The fix commits' subjects and `survivors.md` are the account. Each claim was
checked against the code at the target and, where it is behaviour, executed.

- *Claimed* "a worktree creation is decided before git runs, so a refused `-B`
  leaves its branch" (`74b833ec`). *Found*: the guard denies `git worktree add
  -B existing <wt> main` in `pre-bash`, the branch tip is unchanged and no tree
  exists (executed, p02). The deny text is 0.16.0's single-stream ladder text
  and says nothing about `-B` or a take-back (executed).
- *Claimed* "the commit reading judges a command that can step around git's
  hooks: `core.hooksPath`, `GIT_CONFIG*`, `env -i`" (`5458f376`). *Found*: true
  for those words (c02, c03, p01 deny). Five more commands that 0.16.0 stopped
  still land unjudged (🟡 1, 🟡 2).
- *Claimed* "the commit git makes to finish its own rebase, cherry-pick or
  revert is not judged, and a mark belongs to the git process that left it"
  (`65430596`). *Found*: true (c09, c12, c13 land; c16 refused). A commit typed
  at a paused rebase is still refused under `/usr/bin/git`, so the Apple shim
  does not hide the shell as the starter (c14, executed).
- *Claimed* "a stub git cannot execute is rewritten and decides nothing, and a
  person's commit starts Python only while a lease file stands" (`b14f1edf`).
  *Found*: true (c07, c18).
- *Claimed* "an old-spelling token waives the one Bash call that carried it"
  (`e3ecb7d7`). *Found*: true for another agent's different command (c25), and
  true under this harness's real shell spelling (c25b). The match is wider
  than the policy's limit says (⬜ 3).
- *Claimed* the rider in `hooks/cmdline_base.py` now says the creation arm and
  the consent writer read it on every git (`12b35e31`). *Found*: true; both
  import the frozen copy and neither stands aside any more
  (`hooks/worktree-guard.py`, `hooks/worktree_consent.py`, read).

## Answers to round 1's thirteen

Every probe below drove real git through the clone's stubs, and the PreToolUse
verdicts came from the target's hook and from the installed 0.16.0 hook on the
same payload. "0.16.0" verdicts varied between `deny` and `ask` across runs;
both are stops.

- **Round 1's 1 (`-B`)**: closed. p02: `deny`, tip unchanged, no tree.
- **Round 1's 2 (`core.hooksPath`, `GIT_CONFIG*`, a removed stub)**: closed for
  the instances. c02 and c03 are `deny` at the target. c06, the removal, is
  `silent` and lands, and the policy now names it as a known limit, where a
  reader of §*Known limits of the commit gate inside git* meets it. The class
  is not closed: 🟡 2.
- **Round 1's 3 (stub mode)**: closed. c07: `decides` False after `chmod 644`,
  modes `0o755` after the installer, the commit refused.
- **Round 1's 4 (`--no-checkout`, `--orphan`)**: closed. c22, c23: `deny`, no
  tree, no record.
- **Round 1's 5 (`.claude/worktrees/`)**: closed. c21: `deny`, no tree, no
  record.
- **Round 1's 6 (`--lock`)**: closed. c24: `deny`, no tree.
- **Round 1's 7 (rebase refused)**: closed. c09 reword, c12 `cherry-pick
  --continue`, c13 `rebase --continue` all land; c14's typed `--no-verify` and
  `--amend` at a paused rebase are refused; an alias at a pause lands, which
  the new known limit states. The class has one more member, ⬜ 5, and it is
  a sentence rather than a fix.
- **Round 1's 8 (`env -i`)**: closed for `env -i` (p01 `deny`). The class is
  not closed: 🟡 1.
- **Round 1's 9 (shared-session token)**: closed. c25: with call A's token
  open, call B's commit is refused and A's own lands; A's directory is gone
  after `post-bash`. c25b: the answer matched this harness's own zsh argv,
  which carried a `'` and two newlines as `\012`.
- **Round 1's 10 (aborted commit's mark)**: closed. c16: the abort left one
  mark, and the later `--no-verify` commit with the same date was refused.
- **Round 1's 11 (lease directory)**: closed. c18 medians: no stubs 138 ms,
  stubs and no lease 525 ms, an empty lease directory 548 ms, a lease file
  2,478 ms. The empty directory no longer starts Python.
- **Round 1's 12 (contract §9, §17)**: closed. The text names the four places
  the policy's state table names (read). 🟡 1 and 🟡 2's fixes add words to
  its list.
- **Round 1's 13 (installer cost)**: closed. c19: 107 ms in-process median,
  beside the policy's 113 ms.

## New findings

### 🟡 1 — Removing the session variable another way than `env -i` still lands unjudged

`hooks/tokens.py:63-87` (`steps_around_hooks`) and `:55-60` recognise `env -i`
and its spellings only. The stub's P2 short-cut reads two names,
`CLAUDE_CODE_SESSION_ID` and `CLAUDECODE` (`hooks/githooks.py:117-126`), so any
command that empties, unsets or reassigns both leaves the stub no session
wherever the clone holds no lease file. The reading stands aside because the
clone carries stubs.

Executed (n01–n03), each in a stubbed clone with no lease:

| Command | git | target reading | 0.16.0 reading |
|---|---|---|---|
| `CLAUDECODE= CLAUDE_CODE_SESSION_ID= git commit -m x` | landed | silent | deny |
| `env -u CLAUDECODE -u CLAUDE_CODE_SESSION_ID git commit -m x` | landed | silent | deny |
| `unset CLAUDECODE CLAUDE_CODE_SESSION_ID; git commit -m x` | landed | silent | deny |

Why it matters: these are round 1's 🟡 8 with a different spelling, and each
is a stop 0.16.0 made that the branch drops with no written limit. The owner's
P6 answer named `env -i`; its stated reason, *a token read whose misread costs
one refusal*, covers these three the same way. With the paste-ready change
patched into the clone, all three answered `deny` (executed), and the selected
cases of the two touched test modules passed (52, executed); the patch was
then reverted.

### 🟡 2 — `core.hooksPath` reached through a config file, or the execute bit taken, still lands unjudged

The same function reads `hookspath` and `GIT_CONFIG*` as words. A config file
the command names carries the setting where no word does, and the known limit
for a removed stub (`docs/commit-review-gate-spec.md:189-194`) does not name a
mode change.

Executed (n04–n06), in a stubbed clone, the config file written beforehand:

| Command | git | target reading | 0.16.0 reading |
|---|---|---|---|
| `git -c include.path=<file setting core.hooksPath> commit -m x` | landed | silent | deny |
| `HOME=<dir whose .gitconfig sets core.hooksPath> git commit -m x` | landed | silent | deny |
| `chmod -x .git/hooks/pre-commit .git/hooks/reference-transaction && git commit -m x` | landed | silent | deny |

Why it matters: round 1's 🟡 2 is the class *a commit whose hooks git does not
run*, and the fix closed the spellings it was shown. The first two are one
`-c` word away from the case it pins. The third is the removal's sibling, and
the installer repairs it at the next call (round 1's 3), so a written limit is
the honest fix there. With the code change patched in, n04 and n05 answered
`deny` (executed); n06 stays silent, which the text fix states.

### ⬜ 3 — The old spelling's limit says "byte-for-byte", and the match is wider

`docs/commit-review-gate-spec.md:216-217` says two agents running byte-for-byte
the same command are both waived. `hooks/answers.py#given` compares the two
commands with everything but ASCII letters and digits dropped, and as a
substring of an ancestor's argv. Executed: with call A's
`: '[no-review]'; git commit -m a` open, a command carrying no token,
`echo no-review; git commit -m a`, is given A's answer. Reaching it needs a
command that contains A's whole command that way while A runs, so the
behaviour is the fix working as designed; the sentence undercounts it.

### ⬜ 4 — A person's commit with a lease starts three interpreters, and the limit says two

`docs/commit-review-gate-spec.md:225` says a person's commit "pays the two
interpreter starts" while a lease file stands. The `post-commit` stub has no
narrowing line (`hooks/githooks.py:104`), so with a lease file it starts
Python as well: `pre-commit`, `reference-transaction` at `prepared`, and
`post-commit` (read). c18's 2,478 ms is consistent with three. The older line
above it, "a judged commit starts one interpreter in `pre-commit` and … one in
`reference-transaction`", omits `post-commit` the same way.

### ⬜ 5 — A conflicted merge's conclusion is judged, and the policy names no merge

Executed (n07, n08): in an undeclared opted-in clone, a conflicted `git merge`
resolved and concluded with `git merge --continue` is refused ("SpecSeal
stopped this commit"), and so is a typed `git commit`. 0.16.0's reading is
silent on `git merge --continue`. A pre-commit probe showed why the sequencer
rule cannot exempt it: the hook's parent `git` is the process the shell
started, so `merge --continue` runs its commit in place rather than through a
child (executed). The behaviour is the gate's own principle, a commit judged
where it lands. But the policy's backstop paragraph lists "a merge" among what
is not a commit (`:117`), and nothing tells a reader that concluding one is.

## The merges and the rider

- `git diff 30ee491 bd588eb0 -- hooks docs skills/agent-contract` is the
  release's two deltas (`cd24f516..e83db346` and `e83db346..821e592d`) plus
  `12b35e31`. The seven release files are byte-identical to `821e592d`, and the
  branch had touched none of them before the merges (executed). The only
  hooks file of this branch in the delta is `hooks/cmdline_base.py`, whose
  changed lines are all comment lines (executed). `hooks/config.py` is
  imported by `hooks/mode-gate.py` alone (read). So neither merge changed what
  this branch's hooks do or say.
- The rider sentence `12b35e31` wrote is true: `hooks/worktree-guard.py` and
  `hooks/worktree_consent.py` import the frozen copy, and the
  `githooks.decides` stand-asides both had are gone in `74b833ec` (read).
  `tests/test_the_frozen_reading_never_grows.py` passed at the target
  (executed).
- `bin/correction-check --range origin/release/v0.17.0...bd588eb0` examined
  the two merge commits and found no dropped marker (executed).

## Regression tests to plant

The paste-ready blocks for 🟡 1 and 🟡 2 carry the cases, in
`tests/test_the_commit_gate_decides_at_the_commit.py`'s `STEPS_AROUND`. Each
was seen red by this round: the target's reading answered `silent` on n01–n05
(executed), and the case asserts `deny`.

## Facts for the evidence ledger

- On git 2.50.1 (Apple Git-155), `git merge --continue` runs `pre-commit`
  under the process the shell started, with no child `git` between them
  (round 2 of #692, executed).
- This harness's Bash tool runs a command as `/bin/zsh -c … eval '<command>'
  < /dev/null …`, with `'` written `'"'"'` and a newline printed `\012` by
  `ps -ww`, and `hooks/answers.py#given` matched it (round 2 of #692, c25b,
  executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Removing the session variable by `NAME=`, `env -u` or `unset` leaves the stub no session where no lease stands, and the reading stands aside; 0.16.0 stopped each | `hooks/tokens.py:55-87` | open | executed n01–n03: landed, target silent, 0.16.0 deny; patched, all three deny; class of round 1's finding 8 |
| 🟡 2 | `git -c include.path=<file>` and `HOME=<dir>` reach `core.hooksPath` through a config file, and `chmod -x` on the stubs is not in the written limit; each lands unjudged | `hooks/tokens.py:63-87`, `docs/commit-review-gate-spec.md:189-194` | open | executed n04–n06: landed, target silent, 0.16.0 deny; patched, n04 and n05 deny; class of round 1's finding 2 |
| ⬜ 3 | The old spelling's limit says "byte-for-byte"; the match drops all but letters and digits and is a substring | `docs/commit-review-gate-spec.md:216-217`, `hooks/answers.py:147-181` | open | executed: a command carrying no token was given another open call's answer |
| ⬜ 4 | A person's commit with a lease starts three interpreters; the limit says two | `docs/commit-review-gate-spec.md:218-226` | open | read: the `post-commit` stub has no narrowing line; c18 timing consistent |
| ⬜ 5 | A conflicted merge's conclusion is judged, including `git merge --continue` which 0.16.0 let through, and the policy names no merge | `docs/commit-review-gate-spec.md:112-143` | open | executed n07, n08 refused; the hook's `git` is the shell's process |
| 🟢 | round 1's blocking finding 1 is closed — a refused `worktree add -B` moves nothing | `hooks/worktree-guard.py`, `docs/worktree-guard-spec.md:376-398` | confirmed | executed p02: deny before git, tip unchanged, no tree; the deny text names no take-back |
| 🟢 | round 1's finding 2 is closed for its instances — `-c core.hooksPath`, `GIT_CONFIG*`; a removed stub is a written limit | `hooks/tokens.py#steps_around_hooks`, `docs/commit-review-gate-spec.md:189-194` | confirmed | executed c02, c03 deny, c06 silent and stated; the class is this round's finding 2 |
| 🟢 | round 1's finding 3 is closed — a stub git cannot execute is rewritten and decides nothing | `hooks/hook-install.py#write_stubs`, `hooks/githooks.py#decides` | confirmed | executed c07 |
| 🟢 | round 1's finding 4 is closed — `--no-checkout` and `--orphan` are denied before git | `hooks/worktree-guard.py` | confirmed | executed c22, c23 |
| 🟢 | round 1's finding 5 is closed — a Bash creation under `.claude/worktrees/` is denied and writes no record | `hooks/worktree-guard.py`, `hooks/worktree_consent.py` | confirmed | executed c21 |
| 🟢 | round 1's finding 6 is closed — `--lock` is denied before git | `hooks/worktree-guard.py` | confirmed | executed c24 |
| 🟢 | round 1's finding 7 is closed — the sequencer's own commits land, a typed one at a pause is refused | `hooks/commitgate.py#_sequencer_commit` | confirmed | executed c09, c12, c13 landed; c14 typed refused, alias landed as the limit states |
| 🟢 | round 1's finding 8 is closed for `env -i` | `hooks/tokens.py#steps_around_hooks` | confirmed | executed p01 deny; the class is this round's finding 1 |
| 🟢 | round 1's finding 9 is closed — an answer reaches only the call that carried it | `hooks/answers.py#given`, `hooks/hooksession.py#call_args` | confirmed | executed c25, and c25b under the harness's own shell |
| 🟢 | round 1's finding 10 is closed — an aborted commit's mark passes nothing | `hooks/commitgate.py#_key` | confirmed | executed c16 refused |
| 🟢 | round 1's finding 11 is closed — an empty lease directory starts no Python | `hooks/githooks.py:117-126` | confirmed | executed c18: 548 ms against 525 ms with no lease and 2,478 ms with a lease file |
| 🟢 | round 1's finding 12 is closed — contract §9 and §17 name the policy's four places | `skills/agent-contract/SKILL.md:241-251`, `:349-357` | confirmed | read against the policy's state table |
| 🟢 | round 1's finding 13 is closed — the installer's cost is stated and measured | `docs/commit-review-gate-spec.md:228-233` | confirmed | executed c19: 107 ms in-process median |
| 🟢 | the two release merges changed no hook of this branch, and the rider `12b35e31` wrote is true | `hooks/cmdline_base.py:1-22` | confirmed | executed: release files byte-identical, comment lines only; read: both importers |
| 🟢 | the ledger holds unscoped, and no merge dropped a correction | `seal/` | confirmed | executed: `bin/evidence-check .` exit 0, 3,469 ok, 0 drifted, 0 broken; `bin/correction-check` exit 0 |
| 🟢 | the six modules the fixes touched pass at the target | `tests/` | confirmed | executed: 268 passed, 62 skipped, exit 0 |
| ❓ | Whether a `systemMessage` from the installer reaches the model or only the person | `hooks/hook-install.py#main` | ❓ out of verified scope | carried from round 1; nothing here ran the harness's renderer; the orchestrator answers it |
| ❓ | Whether a command the person types with `!` is "a person's own commit" under P2 — it carries `CLAUDECODE` and is judged | `hooks/githooks.py:117-126` | ❓ out of verified scope | carried from round 1; the owner answers it |
| ❓ | M4's version floor and M5 | `overview.md` §*Not verified* | ❓ out of verified scope | carried; this round ran the stubs under a real `claude` ancestor and shell (c25, c25b), not under the harness's own Bash calls; the orchestrator answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_creation_is_judged_before_git_runs.py`, `tests/test_the_commit_gate_decides_at_the_commit.py`, `tests/test_the_old_spellings_reach_the_hook.py`, `tests/test_the_hooks_are_installed_where_git_runs_them.py`, `tests/test_the_hook_surface_git_offers.py`, `tests/test_the_frozen_reading_never_grows.py`, in the round's clone | 268 passed, 62 skipped, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone | exit 0; 3,469 ok, 0 drifted, 0 broken |
| `bin/correction-check --range origin/release/v0.17.0...bd588eb0`, read-only against the worktree | exit 0; 2 merge commits examined, no marker dropped |
| `git diff 30ee491 bd588eb0` against the two release deltas, on `hooks`, `docs`, `skills/agent-contract` | release files byte-identical to `821e592d`; `hooks/cmdline_base.py` comment lines only |
| one temporary probe script driving real git 2.50.1 through the clone's stubs (installed by `hooks/hook-install.py` into scratch repositories), cases c01–c26, p01, p02, n01–n08; each command's payload through the target's and the installed 0.16.0's `commit-review-gate.py`, and creations through the target's `dispatch.py pre-bash` and 0.16.0's `worktree-guard.py` | as reported per finding; c05 and c08 (`commit-tree`, `am`) landed, as the written limit says; c26's heredoc token is read, as 0.16.0 read it |
| the proposed `steps_around_hooks` lines patched into the clone, n01–n06 re-run, and 52 selected cases of the two touched modules | n01–n05 deny, n06 silent; 52 passed; the patch reverted |
| a pre-commit hook printing its ancestry under `git merge --continue`, in a scratch repository | the hook's parent `git` has the starting process for its parent |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — none of the three was run here; it is the sealer's, and it comes due once 🟡 1 and 🟡 2 are answered |

## Paste-ready fixes

### 🟡 1

```python
# hooks/tokens.py, steps_around_hooks: in the loop, after the hookspath test
        # The stub's P2 short-cut reads these two names, so a command that
        # empties, unsets or reassigns them leaves the stub no session where
        # no lease stands: `NAME= git commit`, `env -u NAME`, `unset NAME`
        # (round 2 of #692, executed). 0.16.0's reading stopped each.
        if "CLAUDECODE" in word or "CLAUDE_CODE_SESSION_ID" in word:
            return True
```

```python
# tests/test_the_commit_gate_decides_at_the_commit.py, STEPS_AROUND: add
    "an emptied session variable": (
        "CLAUDECODE= CLAUDE_CODE_SESSION_ID= git commit -m x"
    ),
    "env -u": "env -u CLAUDECODE -u CLAUDE_CODE_SESSION_ID git commit -m x",
    "unset": "unset CLAUDECODE CLAUDE_CODE_SESSION_ID; git commit -m x",
```

```markdown
[docs/commit-review-gate-spec.md, the stand-aside paragraph at :154-160 -- the list becomes]
`core.hooksPath` in any spelling (`-c`, `--config-env`, `git config`), a config
file that can carry it (`include.path`, `includeIf`, `HOME=`,
`XDG_CONFIG_HOME=`), any `GIT_CONFIG*` assignment, `env` emptying the
environment, a word naming `CLAUDECODE` or `CLAUDE_CODE_SESSION_ID`, and a
command that does not split.

[the same file, the state table's first row at :240]
| a clone carrying the stubs | `pre-commit`, then `reference-transaction` for one that skipped it; the PreToolUse reading as well for a command carrying one of the words `hooks/tokens.py#steps_around_hooks` reads |

[skills/agent-contract/SKILL.md §9 at :245-246 -- the parenthesis becomes]
words can keep the hooks from running (`core.hooksPath` or a config file that
can carry it, `GIT_CONFIG*`, `env -i`, the session variables).
```

### 🟡 2

```python
# hooks/tokens.py, steps_around_hooks: in the loop, beside the test above
        # A config file the command names can carry core.hooksPath where no
        # word does: `-c include.path=<file>`, an includeIf, and HOME or
        # XDG_CONFIG_HOME pointing git at another global config (round 2 of
        # #692, executed).
        low = word.lower()
        if "include.path" in low or "includeif." in low:
            return True
        name, eq, _ = word.lstrip("(").partition("=")
        if eq and name in ("HOME", "XDG_CONFIG_HOME"):
            return True
```

```python
# tests/test_the_commit_gate_decides_at_the_commit.py, STEPS_AROUND: add
    "include.path": "git -c include.path=/x/cfg commit -m x",
    "includeIf": "git -c includeIf.onbranch:main.path=/x/cfg commit -m x",
    "HOME": "HOME=/x/h git commit -m x",
    "XDG_CONFIG_HOME": "XDG_CONFIG_HOME=/x/c git commit -m x",
```

```markdown
[docs/commit-review-gate-spec.md, the known limit at :189-194, replaced]
- **A command that removes the stubs, or takes their execute bit, before it
  commits is judged by nobody.** `rm .git/hooks/pre-commit
  .git/hooks/reference-transaction && git commit`, and `chmod -x` on the same
  two files, step around both hooks, and the reading stood aside before the
  command ran, because nothing in its words names a hook setting. The
  installer puts the stubs and their mode back at the next Bash call. 0.16.0's
  reading stopped both (rounds 1 and 2 of #692, executed).
```

### ⬜ 3

```markdown
[docs/commit-review-gate-spec.md :216-217, the last sentence replaced]
  belongs to its own command. The match drops everything but letters and
  digits and looks for the carried command inside the shell's argv, which is
  what lets the shell's own quoting through. So two agents running the same
  command are both waived, and so is a command that contains another open
  call's whole command that way.
```

### ⬜ 4

```markdown
[docs/commit-review-gate-spec.md :225, the clause replaced]
  a person's commit pays three interpreter starts, `pre-commit`,
  `reference-transaction` at `prepared` and `post-commit`, so the stub can look
  for a `claude` ancestor:
```

### ⬜ 5

```markdown
[docs/commit-review-gate-spec.md, the sequencer statement at :129-142, appended before its Enforced by: line at :143]
A conflicted merge is not one of them. `git merge --continue` runs its commit
in the process the shell started, so it is judged as a typed `git commit`
concluding the merge is, where 0.16.0's reading let `git merge --continue`
through (round 2 of #692, executed).
```

Needs a fix: yes — 🟡 1 (the session variable removed by `NAME=`, `env -u` or `unset`) and 🟡 2 (`core.hooksPath` through `include.path` or `HOME=`, and `chmod -x` missing from the written limit).
Loses a record or crashes: no

## Proof block

Files opened this round, at the target in the clone:
`seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/rounds/round-1.md`,
`rounds/round-1-report.md` (lines 1–275), `survivors.md`, `questions.md` (P5,
P6 rows), `hooks/tokens.py`, `hooks/hooksession.py`, `hooks/commitgate.py`
(30–315), `hooks/githooks.py` (60–245), `hooks/hook-install.py` (95–200),
`hooks/cmdline_base.py` (1–40), `docs/worktree-guard-spec.md` (360–400),
`docs/commit-review-gate-spec.md` (the fix range's diff and 210–230),
`skills/agent-contract/SKILL.md` (the diff and 240–250),
`tests/test_a_creation_is_judged_before_git_runs.py`,
`tests/test_the_commit_gate_decides_at_the_commit.py` (1–200, 970–1015),
`tests/test_the_old_spellings_reach_the_hook.py` (the diff), `tests/conftest.py`
(525–558), `bin/test`, and the fix range's diff of `hooks/`.

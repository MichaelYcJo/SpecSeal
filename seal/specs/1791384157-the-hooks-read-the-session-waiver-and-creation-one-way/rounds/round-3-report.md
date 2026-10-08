# 1791384157 — review round 3 report (verifying)

| Field | Value |
|---|---|
| Target SHA | ccd46c8becfb9bdad038f00500d3c8c928f7ddab |
| Target | the diff of round 2's fixes, `ce3b0652..c130e284`, plus the close at `ccd46c8b` |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 881 |
| Where | a `git clone --no-local` of the worktree at the target, in the session scratchpad |

## What this round was asked

Answer round 2's five verdicts, and judge round 2's New units as code:
`_brace_command_at`, the lease case
`test_a_pid_beside_no_session_id_on_either_side_is_not_recorded`, and the
`-C` tree case. The spawn named three questions. Is the rule's boundary (the
command word and the words before it) where bash decides what runs? Can a
brace the rule reads exactly still spell a git it misses? Is the 0-stop count
measured the way phase 1 measured? The run is capped: this round ends it.

## The account, and what the code does

The smith's account says `_brace_command_at` reads "the command word and every
word before it", so a command-word brace stops wherever bash would make a git
of it. The code at `hooks/worktree-guard.py:2320` takes that boundary from the
frozen reader's `cmdline.command_word`. That reader was built to find a
literal `git`, and it gives up early in three places: behind a runner's own
option or operand, at a leading redirection, and on a word with a subshell
opener glued to it. Its stand-in for the first case looks for a later word
whose name is `git`, and a brace word is never that word. So the boundary is
the frozen reader's and not bash's. The two halves of the account that hold:
round 2's four inexact spellings now stop, and the corpus count is zero
(both executed below).

```
round 2 boundary      ──▶  🟡 1  the boundary stops before bash's command word
                              (runner operand, leading redirection, glued `(`)
exact brace judged    ──▶  🟡 2  an alternative that is empty or a runner
 only by "spells git"           hands the command word to the next word
round 1 + 2 rule      ──▶  🟡 3  an `&` cut puts the brace word in a part
 never read in a cut            no brace reader is asked about
```

All three are the same failure: in an ACTIVE tree the guard says nothing, and
bash runs `git switch feature/x`. That is the guard's whole job, and it is the
same class and severity round 2 gave its 🟡 1.

## Findings from execution

### 🟡 1 — the boundary stops before the word bash runs

`hooks/worktree-guard.py:2320` (`hooks/worktree-guard.py#_brace_command_at`,
a unit round 2's fixes created).

`leading` ends at whatever `cmdline.command_word` returns. Executed at the
target, each of these is **silent** in an ACTIVE tree:

- behind a runner's option or operand: `timeout 5 {git,} switch feature/x`,
  `nice -n 5 {git,} switch feature/x`, `sudo -u x {git,} switch feature/x`,
  `env -u FOO {git,} switch feature/x`, `command -p {git,} switch feature/x`;
- behind a leading redirection: `2>/dev/null {git,} switch feature/x`,
  `>/dev/null {git,} switch feature/x`;
- a glued subshell opener: `({git,} switch feature/x)`. `command_word`
  strips the `(` for its own reading, but the loop then reads the raw token
  `({git,}`, so the brace's alternatives are `(git` and `(`, and neither is
  `git`.

Bash runs `git switch feature/x` for every one it was given (a fake `git` on
`PATH` recorded the call; `sudo` and `command -p` were not run, and the reason
they belong here is read, not executed). zsh runs it for the runner forms with
`{git,switch} feature/x` too, so this is not a bash-only gap. The controls the
fix names (`X=1 {git,}`, `env {git,}`, `exec {git,}`, `time {git,}`,
`if true; then {git,} …; fi`) deny as claimed.

It matters because each spelling moves HEAD under a session that is ACTIVE in
the tree. Round 2 fixed the spellings it was shown, and the boundary the fix
chose leaves the next ones open.

The fix keeps the orchestrator's direction and adds no spelling. Where the
words up to the frozen command word hold a runner or a redirection, every
word of the segment is read, because the frozen reader does not place the
program there. A glued `(` is taken off before the word is read. With the
paste-ready change applied in the clone, all eight stop. The two touched
modules plus `tests/test_the_guard_asks_once_per_session.py` pass (369), and
the corpus count stays at zero.

### 🟡 2 — an exact brace can hand the command word to the next word

`hooks/worktree-guard.py:2325` (`hooks/worktree-guard.py#_brace_command_at`).

An exact brace counts only where an alternative spells `git`
(`_brace_spells_git`). But bash drops an empty unquoted word, and a runner
runs the words after it. Executed, each **silent** in an ACTIVE tree, and run
by bash as `git switch feature/x`:

- `{,} git switch feature/x`
- `{env,} git switch feature/x`, `{nice,} git switch feature/x`,
  `{exec,} git switch feature/x`

zsh keeps the empty word, so it runs none of these. The defect is bash's half,
and bash is the shell the spec names first.

The fix counts an exact brace where one alternative is empty or names a
runner (`cmdline.RUNNERS`, the list the frozen reader already keeps) and a
word follows it. `{echo,printf} x` stays silent (executed). `_finding_tree`
then has to read the `-C` from a `git` that stands after the brace word, as
in `{env,} git -C W switch x`, so it tries the rest of the segment as it is
before it puts a `git` in front. With both applied, the four `-C` probes ask
in `W`.

### 🟡 3 — a brace command word after an `&` cut is read by nobody

`hooks/worktree-guard.py:2392` (`hooks/worktree-guard.py#_merged_findings`;
not a unit round 2 created, so this is a finding of its own depth).

`2>&1 {git,} switch feature/x` splits at the `&` into `2>` and
`1 {git,} switch feature/x`. The second part's frozen command word is `1`, so
`_segment_finding` sees no brace. `_merged_findings` glues the parts back
together, then asks only the git readers and never the brace rule. Executed:
the command is **silent** in an ACTIVE tree, still silent with 🟡 1's fix
alone, and denied once the group is also asked about its brace. Bash runs
`git switch feature/x`.

## Findings from reading, and smaller ones

### ⬜ 4 — the new lease case's `None` parameter builds neither absence

`tests/test_lease_liveness.py:401`
(`tests/test_lease_liveness.py#test_a_pid_beside_no_session_id_on_either_side_is_not_recorded`).

The case is meant to pin round 2's white 4: both ids absent, `None == None`,
so the inherited pid was recorded. Its `None` parameter never removes
`CLAUDE_CODE_SESSION_ID`, so the case inherits whatever the runner exports.
The variable is set in this round's own environment. The helper also always
sends `"session_id": ""`, never a payload without the key. Executed: with the
lease writer at `e0c5a191`, `[None]` **passed** and only `[]` failed. The
code fix is right, and `[]` pins it. What the record says was shown red is
half true. The round-1 case `test_a_pid_exported_for_another_session_is_not_recorded`
has the same inheritance in its `outer=None` parameter.

The paste-ready case below removes the variable and leaves the key out. In
the clone, its `[None-None]` (the exact shape white 4 named) and `[-]` are red
at `e0c5a191`, and all four are green at the target.

### ⬜ 5 — an assignment word before the command word over-stops

`hooks/worktree-guard.py:2321`. `A={{a,b},c} ls` and `A={a..c} ls` **ask** in a
dirty tree (executed). Bash does no brace expansion on an assignment word
(read: the bash manual's *Simple Command Expansion*; the run that would have
shown it was refused, see the ❓ row). The cost is in the stopping direction,
and no recorded pair has it, so nothing ships wrong. It is noted so that the
sentence "a brace in an argument stops nothing" is not read as covering it.

### ⬜ 6 — the 34,633 figure has no recorded method (a correction)

`seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-fixes.md:23`.

Phase 1 wrote down its corpus, its reading and a self-check, and only then
trusted a zero (`phases/phase-1.md`). The round-2 figure reaches
`docs/worktree-guard-spec.md:86`, the changelog fragment and the fix table
with no method and no self-check anywhere. I measured it again by phase 1's
method. Every Bash `tool_use` under the SpecSeal transcript directories gives
34,775 distinct (command, cwd) pairs, each segment read through
`_segment_finding`'s own test, after a self-check that found 4 of 4 shapes
and passed over 4 of 4 silent ones. The rule stops **0**. So the claim holds,
and so does round 1's rule. With this round's paste-ready fixes applied it
is also 0, over 34,813 pairs. This is about the record and not the tool, so
it is ⬜ and stays out of `Needs a fix`.

## Round 2's verdicts

- **🟡 1 (inexact braces):** closed for the command word. Its four spellings
  are red at `e0c5a191` and green at the target (executed). The class goes on
  in this round's 🟡 1–3.
- **🟡 2 (`-C` tree):** closed for `{git,} -C W`. Its three parameters are
  red at `e0c5a191` and green at the target (executed). `{env,} git -C W`
  needs 🟡 2's `_finding_tree` change.
- **⬜ 3 (survivors):** answered. `survivors.md` holds 11 rows, one per
  place, each with a quote. The hygiene `release` job that runs
  `survivor_check.py` passed at `ccd46c8b` (read off `gh pr checks`).
- **⬜ 4 (lease, both absent):** fixed in code (read, and `[]` is red then
  green, executed). The case is weaker than its record says (⬜ 4 above).
- **⬜ 5 (docstring):** fixed. The docstring now says `CLAUDE_PID` is read
  beside this session's own id (read).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A command-word brace behind a runner's option or operand, behind a leading redirection, or with a glued `(` is silent in an ACTIVE tree: `timeout 5 {git,} switch x`, `2>/dev/null {git,} switch x`, `({git,} switch x)` | `hooks/worktree-guard.py:2320` | open | executed: 8 spellings silent at the target; bash runs `git switch feature/x` for each one run; all stop with the paste-ready fix, 369 passed, corpus 0 |
| 🟡 2 | An exact brace whose alternative is empty or a runner hands the command word on: `{,} git switch x`, `{env,} git switch x` are silent | `hooks/worktree-guard.py:2325` | open | executed: 4 spellings silent; bash runs `git switch feature/x`; zsh does not; deny with the fix, and `-C W` is judged in `W` |
| 🟡 3 | A brace command word after an `&` cut is read by no brace reader: `2>&1 {git,} switch x` is silent | `hooks/worktree-guard.py:2392` | open | executed: silent at the target and with 🟡 1's fix alone; deny once `_merged_findings` asks `_brace_command_at` |
| ⬜ 4 | The new lease case's `None` parameter inherits the runner's session id and always sends an empty payload id, so it cannot be red | `tests/test_lease_liveness.py:401` | open | executed: `[None]` passed at `e0c5a191`; the paste-ready case's `[None-None]` and `[-]` are red there and green at the target |
| ⬜ 5 | An inexact brace in an assignment word before the command word asks, where bash expands none | `hooks/worktree-guard.py:2321` | open | executed: `A={{a,b},c} ls` and `A={a..c} ls` ask in a dirty tree; read: bash expands no brace in an assignment word; stopping direction, no recorded pair |
| ⬜ 6 | The 34,633 figure carries no method and no self-check, where phase 1 recorded both | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-fixes.md:23` | open | a correction of the run's paperwork; executed: re-measured over 34,775 pairs, self-check 8 of 8, 0 stops |
| 🟢 | round 2's yellow 1 is closed for inexact braces in the command word | `tests/test_worktree_guard.py:1933` | confirmed | executed: 4 spellings red at `e0c5a191`, green at the target; the class continues in this round's 1 to 3 |
| 🟢 | round 2's yellow 2 is closed for a brace word followed by its own `-C` | `tests/test_worktree_guard.py:1985` | confirmed | executed: 3 parameters red at `e0c5a191`, green at the target |
| 🟢 | round 2's white 3 stays answered — one survivor row per place | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md` | confirmed | read: 11 rows, each quoted; the hygiene `release` job passed at `ccd46c8b` |
| 🟢 | round 2's white 4 is closed in code — two missing ids no longer match | `hooks/session-lease.py:102` | confirmed | executed: `[]` red at `e0c5a191`, green at the target; the case's gap is this round's white 4 |
| 🟢 | round 2's white 5 is closed — the docstring names the session-id condition | `hooks/session-lease.py:27` | confirmed | read: the docstring and `main` now agree |
| ❓ | Whether bash and zsh expand a brace in an assignment word was not run | `hooks/worktree-guard.py:2321` | ❓ out of verified scope | the permission layer refused the shell run and it was not retried; ⬜ 5 rests on the bash manual; the orchestrator answers it if it matters |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the eight guard modules named in the spawn, in the clone at the target | exit 0, 435 passed |
| round 2's new cases with `hooks/session-lease.py` and `hooks/worktree-guard.py` at `e0c5a191` | 8 failed, 3 passed; the lease case's `[None]` is one of the 3 |
| `tests/test_lease_liveness.py`, `tests/test_worktree_guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py` at the target | exit 0, 338 passed |
| a deleted probe through the module's `verdict` helper, 24 commands, ACTIVE tree, at the target | 17 silent: the 13 of 🟡 1, 2 and 3, and four `{git,switch} feature/x` forms of 🟡 1; 7 deny: six controls and `{git,switch} feature/x` |
| the same commands under bash and zsh, with a fake `git` first on `PATH`, cwd a scratch repository | bash runs `git switch feature/x` for all 17 it was given; zsh runs it for `timeout 5 {git,switch} feature/x` and `nice -n 5 {git,switch} feature/x`, hands git an empty first word for the runner `{git,}` forms, and runs nothing for the rest |
| the paste-ready fixes applied in the clone, the probe again | every 🟡 spelling denies; 4 `-C` probes ask in `W`; `{echo,printf} x` silent |
| the two touched guard modules and `tests/test_the_guard_asks_once_per_session.py` with the fixes | exit 0, 369 passed |
| corpus re-measure (phase 1's method, self-check first) at the target | 34,775 pairs; self-check 8 of 8; command-word rule 0, round 1's rule 0 |
| the same with the paste-ready fixes | 34,813 pairs, 0 |
| the paste-ready lease case at the target, then with the lease writer at `e0c5a191` | 4 passed; then `[None-None]` and `[-]` failed, 2 passed |
| `gh pr checks 881` at `ccd46c8b` | lint, ledger, release, both grammar jobs, ubuntu and all four Windows groups pass; the three macOS groups pending at hand-over |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Paste-ready fixes

### 🟡 1 and 🟡 2 — `_brace_command_at`, `hooks/worktree-guard.py`

```python
    command, _unplaced = cmdline.command_word(list(tokens))
    end = len(tokens) - len(command) + 1 if command else len(tokens)
    # A glued subshell opener is no part of the word bash runs: `({git,}
    # switch x)` (round 3 of work item 1791384157, yellow 1).
    words = [t.lstrip("(") for t in tokens]
    # Behind a runner or a redirection the frozen reading does not place the
    # program bash runs (`timeout 5 {git,} switch x`, `2>/dev/null {git,}
    # switch x`), so every word of the segment is read there.
    if any(
        os.path.basename(w) in cmdline.RUNNERS or "<" in w or ">" in w
        for w in words[:end]
    ):
        end = len(words)
    for at, word in enumerate(words[:end]):
        if not _BRACE.search(word):
            continue
        if (
            not _ONE_BRACE.fullmatch(word)
            or _brace_spells_git(word)
            or (at + 1 < len(words) and _brace_hands_on(word))
        ):
            return at
    return None


def _brace_hands_on(word) -> bool:
    """Whether one of WORD's one-brace alternatives is empty or a runner, so
    bash takes the program from the word after it: `{,} git switch x` and
    `{env,} git switch x` run `git switch x` (round 3 of work item
    1791384157, yellow 2)."""
    match = _ONE_BRACE.fullmatch(word)
    if not match:
        return False
    head, alternatives, tail = match.groups()
    return any(
        not head + alt + tail or os.path.basename(head + alt + tail) in cmdline.RUNNERS
        for alt in alternatives.split(",")
    )
```

### 🟡 2 — `_finding_tree`, `hooks/worktree-guard.py`

```python
    at = _brace_command_at(tokens) if parse_git(tokens) is None else None
    if at is not None:
        rest = tokens[at + 1 :]
        # `{env,} git -C W switch x` names its git after the brace word.
        parsed = parse_git(rest) or parse_git(["git", *rest])
        if parsed and parsed[2]:
            return apply_chdir(here, parsed[2])
```

### 🟡 3 — `_merged_findings`, `hooks/worktree-guard.py`, before `if _wide_git(toks):`

```python
            # `2>&1 {git,} switch x`: the brace word stands after the cut
            # (round 3 of work item 1791384157, yellow 3).
            if braced and _brace_command_at(toks) is not None:
                out.append((parts[0], Finding("brace", _spoken(toks)), toks))
                continue
```

### 🟡 1, 2, 3 — the doc sentence that changes with them (§14), `docs/worktree-guard-spec.md:76`

```markdown
x`, which bash runs as `git switch x`) is the same shape, read in a segment
the frozen reading reads as no git from its command word and every word
before it, and from every word where a runner or a redirection stands before
that word (`timeout 5 {git,} switch x`, `2>&1 {git,} switch x`). There, a
brace the guard takes apart exactly (one comma brace) stops where one of its
alternatives spells `git` or a path ending in it, or is empty or a runner with
a word after it (`{,} git switch x`, `{env,} git switch x`), so
`{echo,printf} x` says nothing; and a brace the guard cannot take apart
```

### Regression cases — `tests/test_worktree_guard.py`, added to the parameters of `test_a_brace_that_makes_the_command_word_is_unrecognised`

```python
        # Round 3 of work item 1791384157: the boundary bash reads, not the
        # frozen reader's (yellow 1), an exact brace that hands the command
        # word on (yellow 2), and a brace word after an `&` cut (yellow 3).
        # Each silent at `ccd46c8b`.
        "timeout 5 {git,} switch feature/x",
        "nice -n 5 {git,} switch feature/x",
        "env -u FOO {git,} switch feature/x",
        "2>/dev/null {git,} switch feature/x",
        "({git,} switch feature/x)",
        "{,} git switch feature/x",
        "{env,} git switch feature/x",
        "2>&1 {git,} switch feature/x",
```

### Regression cases — `tests/test_worktree_guard.py`, added to the parameters of `test_a_brace_command_word_is_judged_in_the_tree_its_c_names`

```python
        "timeout 5 {{git,}} -C {w} switch feature/x",
        "{{env,}} git -C {w} switch feature/x",
```

### ⬜ 4 — `tests/test_lease_liveness.py`

```python
@pytest.mark.parametrize("environment", [None, ""])
@pytest.mark.parametrize("payload", [None, ""])
def test_a_pid_beside_no_session_id_on_either_side_is_not_recorded(
    repo, monkeypatch, environment, payload
):
    """Round 2 of work item 1791384157, white 4. Where neither the
    environment nor the payload names a session, the two absences matched
    and the lease `pid-<ppid>` recorded the inherited 4242. A missing id
    names no session, so the walk answers. `[None-None]` and `[-]` are red at
    `e0c5a191`; the variable is removed, since a suite run from a session
    inherits one (round 3, white 4)."""
    monkeypatch.setenv("CLAUDE_PID", "4242")
    if environment is None:
        monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    else:
        monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", environment)
    stub_process_tree(monkeypatch, 100, {100: (50, "/bin/zsh"), 50: (1, "claude")})
    rec = run_main_in_process(repo, monkeypatch, payload, filed="pid-100")
    assert rec["pid"] == 50, rec
```

```python
    # in run_main_in_process, replacing the inline payload:
    payload = {"tool_name": "Bash", "tool_input": {"command": "ls"}, "cwd": str(repo)}
    # A SESSION of None leaves the key out, as a payload with no id does.
    if session is not None:
        payload["session_id"] = session
    monkeypatch.setattr(sl.sys, "stdin", io.StringIO(json.dumps(payload)))
```

## Facts for the evidence ledger

- `hooks/cmdline_base.py#command_word` stops at a runner's first option or operand and
  at a leading redirection, and its stand-in looks only for a word whose name
  is `git`. A brace reader bounded by it does not reach bash's command word
  there (executed, 🟡 1).
- Bash drops an empty unquoted word from a brace expansion, and zsh keeps it:
  `{,} git switch x` runs git under bash and not under zsh (executed).
- Over the SpecSeal transcripts on 2026-10-08, 34,775 distinct pairs, the
  command-word brace rule stops none, with or without this round's fixes
  (executed, phase 1's method).

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Nothing is deferred by this round. The run is capped, and whatever of 🟡 1–3
is left open the orchestrator files.

The broad gate has not run. Three 🟡 are open, so it has not come due.

Needs a fix: yes — 🟡 1 (a command-word brace behind a runner operand, a leading redirection or a glued `(` is silent), 🟡 2 (an exact brace whose alternative is empty or a runner is silent), 🟡 3 (a brace command word after an `&` cut is silent)
Loses a record or crashes: no

## Proof — files opened

- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2.md`, `rounds/round-2-fixes.md`, `survivors.md`, `phases/phase-1.md`, `changelog.md` (lines 50 to 64)
- `hooks/worktree-guard.py` (lines 130 to 175, 2000 to 2030, 2055 to 2110, 2230 to 2540, 2990 to 3040)
- `hooks/cmdline.py` (lines 54 to 80, 1408 to 1470, 1505 to 1580, 2453 to 2500), `hooks/cmdline_base.py` (lines 58, 1375 to 1430)
- `hooks/session-lease.py` (lines 20 to 110)
- `tests/test_worktree_guard.py` (lines 1 to 80, 1099 to 1140, 1476 to 1510, 1917 to 2003), `tests/test_lease_liveness.py` (lines 380 to 472), `tests/conftest.py` (lines 818 to 826)
- `docs/worktree-guard-spec.md` (lines 70 to 90, 140 to 162), `.github/workflows/hygiene.yml` (lines 250 to 272), `bin/test`
- the diff `ce3b0652..c130e284` under `hooks/`, `tests/` and `docs/`

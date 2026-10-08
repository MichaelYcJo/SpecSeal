# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — review round 3

| Field | Value |
|---|---|
| Target SHA | ccd46c8becfb9bdad038f00500d3c8c928f7ddab |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 881 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `3700aa491e143f55e217e3e40d48f11f666a5e9a..3700aa491e143f55e217e3e40d48f11f666a5e9a`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | second — 🟡 1 at hooks/worktree-guard.py#_brace_command_at, a unit round-2's fixes added; 🟡 2 at hooks/worktree-guard.py#_brace_command_at, a unit round-2's fixes added; the fix passes stop here and the work item goes back to its framer |
| Needs a fix | yes — 🟡 1 (a command-word brace behind a runner operand, a leading redirection or a glued `(` is silent), 🟡 2 (an exact brace whose alternative is empty or a runner is silent), 🟡 3 (a brace command word after an `&` cut is silent) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Verifying round 3 of round 2's fixes: ce3b0652..c130e284 plus the close at ccd46c8b. It was announced as the run's last record. The job was the answers to round 2's five verdicts; _brace_command_at, the empty-id lease case and the -C case were a finding surface. The spawn named three things to judge. First, whether the rule's boundary, the command word and the words before it, is where bash decides what runs: prefix assignments, env, command, exec and runner wrappers. Second, whether a brace read exactly can still spell a git it misses. Third, whether the 0-over-stop count was measured the way phase 1 measured it. Probes were to run in a scratch repository, never the session's checkout, and a refused command was not to be retried. It also ran the eight guard modules once. Facts arrived labelled. Read: the orchestrator's direction to stop enumerating brace spellings. Read from the smith: the rule, the 34,633-pair count, five mutations and 1,177 passed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A command-word brace behind a runner's option or operand, behind a leading redirection, or with a glued `(` is silent in an ACTIVE tree: `timeout 5 {git,} switch x`, `2>/dev/null {git,} switch x`, `({git,} switch x)` | `hooks/worktree-guard.py:2320` | deferred the frame | the frame — the second fix of a fix itself, in `_brace_command_at`; the framer redesigns how the guard meets a brace expansion; executed: 8 spellings silent at the target; bash runs `git switch feature/x` for each one run; all stop with the paste-ready fix, 369 passed, corpus 0 |
| 🟡 2 | An exact brace whose alternative is empty or a runner hands the command word on: `{,} git switch x`, `{env,} git switch x` are silent | `hooks/worktree-guard.py:2325` | deferred the frame | the frame — the second fix of a fix, in `_brace_command_at`; the framer redesigns how the guard meets a brace expansion; executed: 4 spellings silent; bash runs `git switch feature/x`; zsh does not; deny with the fix, and `-C W` is judged in `W` |
| 🟡 3 | A brace command word after an `&` cut is read by no brace reader: `2>&1 {git,} switch x` is silent | `hooks/worktree-guard.py:2392` | deferred the frame | the frame — the same class through the `&` split; it follows the frame's redesign; executed: silent at the target and with 🟡 1's fix alone; deny once `_merged_findings` asks `_brace_command_at` |
| ⬜ 4 | The new lease case's `None` parameter inherits the runner's session id and always sends an empty payload id, so it cannot be red | `tests/test_lease_liveness.py:401` | deferred the frame | the frame — the lease case that cannot fail; the redesign's build strengthens it; executed: `[None]` passed at `e0c5a191`; the paste-ready case's `[None-None]` and `[-]` are red there and green at the target |
| ⬜ 5 | An inexact brace in an assignment word before the command word asks, where bash expands none | `hooks/worktree-guard.py:2321` | deferred the frame | the frame — a brace in an assignment asks; the redesign decides what a brace anywhere means; executed: `A={{a,b},c} ls` and `A={a..c} ls` ask in a dirty tree; read: bash expands no brace in an assignment word; stopping direction, no recorded pair |
| ⬜ 6 | The 34,633 figure carries no method and no self-check, where phase 1 recorded both | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-fixes.md:23` | deferred the frame | the frame — the over-stop figure's method; the redesign re-measures it; a correction of the run's paperwork; executed: re-measured over 34,775 pairs, self-check 8 of 8, 0 stops |
| 🟢 | round 2's yellow 1 is closed for inexact braces in the command word | `tests/test_worktree_guard.py:1933` | confirmed | executed: 4 spellings red at `e0c5a191`, green at the target; the class continues in this round's 1 to 3 |
| 🟢 | round 2's yellow 2 is closed for a brace word followed by its own `-C` | `tests/test_worktree_guard.py:1985` | confirmed | executed: 3 parameters red at `e0c5a191`, green at the target |
| 🟢 | round 2's white 3 stays answered — one survivor row per place | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md` | confirmed | read: 11 rows, each quoted; the hygiene `release` job passed at `ccd46c8b` |
| 🟢 | round 2's white 4 is closed in code — two missing ids no longer match | `hooks/session-lease.py:102` | confirmed | executed: `[]` red at `e0c5a191`, green at the target; the case's gap is this round's white 4 |
| 🟢 | round 2's white 5 is closed — the docstring names the session-id condition | `hooks/session-lease.py:27` | confirmed | read: the docstring and `main` now agree |
| ❓ | Whether bash and zsh expand a brace in an assignment word was not run | `hooks/worktree-guard.py:2321` | ❓ out of verified scope | the permission layer refused the shell run and it was not retried; ⬜ 5 rests on the bash manual; the orchestrator answers it if it matters |

## Paste-ready fixes

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
```python
    at = _brace_command_at(tokens) if parse_git(tokens) is None else None
    if at is not None:
        rest = tokens[at + 1 :]
        # `{env,} git -C W switch x` names its git after the brace word.
        parsed = parse_git(rest) or parse_git(["git", *rest])
        if parsed and parsed[2]:
            return apply_chdir(here, parsed[2])
```
```python
            # `2>&1 {git,} switch x`: the brace word stands after the cut
            # (round 3 of work item 1791384157, yellow 3).
            if braced and _brace_command_at(toks) is not None:
                out.append((parts[0], Finding("brace", _spoken(toks)), toks))
                continue
```
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
```python
        "timeout 5 {{git,}} -C {w} switch feature/x",
        "{{env,}} git -C {w} switch feature/x",
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_worktree_guard.py:2178` | round 1's 🔴 1 — fixed |
| round-1 | `tests/test_worktree_guard.py:729` | round 1's 🔴 2 — fixed |
| round-1 | `hooks/worktree-guard.py:2270` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/session-lease.py:91` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/worktree-guard.py:2007` | round 1's ⬜ 5 — answered |
| round-1 | `hooks/tokens.py:33` | round 1's ⬜ 6 — fixed |
| round-1 | `hooks/hooksession.py:68` | round 1's ❓ — out of verified scope |
| round-1 | `hooks/worktree_consent.py:419` | round 1's ❓ — out of verified scope |
| round-2 | `hooks/worktree-guard.py:2292` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/worktree-guard.py:2470` | round 2's 🟡 2 — fixed |
| round-2 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md:24` | round 2's ⬜ 3 — answered |
| round-2 | `hooks/session-lease.py:98` | round 2's ⬜ 4 — fixed |
| round-2 | `hooks/session-lease.py:25` | round 2's ⬜ 5 — fixed |
| round-2 | `tests/test_worktree_guard.py:2199` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2282` | round 2's 🟢 — confirmed |
| round-2 | `hooks/tokens.py:45` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

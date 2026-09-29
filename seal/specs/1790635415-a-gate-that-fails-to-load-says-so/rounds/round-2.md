# 1790635415-a-gate-that-fails-to-load-says-so — review round 2

| Field | Value |
|---|---|
| Target SHA | 02e474351e1b737147ef5c1c211aadef7332631d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #660 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (a shell-run heredoc body reads as data), 🟡 2 (a cd whose target an earlier segment moves is trusted), 🟡 3 (a deny beside a non-text message is dropped) |
| Loses a record or crashes | yes — 🔴 1 and 🟡 2 each read a real commit silent, which the gate judged at e8e5f977 |

- [ ] Pass

## What this round was asked

Round 2, two jobs. Verifying: round 1's fixes, `d89f8392..fa556996`. Finding: phases 4 and 5 (#661, #662, #665), added at the owner's request after round 1 and reviewed by nobody before, `b3ad918d..02e47435`, at HEAD `02e47435`. A false silent on the commit gate, the worktree guard or the consent readers was named as where a defect would leave the root.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A heredoc body that a shell runs reads as data, and its commit silent, when a program flag or script follows the `<<`, a program flag is bundled, or a `$(…)`, `${…;…}` or `>&` precedes the interpreter's name | `hooks/cmdline.py#program_is_data`, `hooks/cmdline.py#_heredoc_split` | open | Executed: five shapes deny at `e8e5f977` and silent at `02e47435`, and four were run in a real bash, where the body ran as shell. Contradicts the rule #665 states and G7 |
| 🟡 2 | A `cd` whose target an earlier segment moves or locks is trusted not to fail, so the session's directory, where the commit runs, is not judged | `hooks/cmdline.py#walk_directories`, `hooks/cmdline.py#_enters` | open | Executed: `mv` and `chmod` shapes deny at `e8e5f977` and silent at `02e47435`, and a real bash stayed where it started. Contract §13 |
| 🟡 3 | `readable` drops a deny carrying a non-text `systemMessage`, which the decision path never reads, and a falsy `hookSpecificOutput` the old code read as absent | `hooks/dispatch.py#readable` | open | Executed: `merge` kept the deny at `1ea0b7c2~1` and prints nothing at `02e47435`. No gate prints the shape today, which was read |
| 🟢 | round 1's yellow finding 1 is closed — a load failure names every group that loads the gate, a run failure its own | `hooks/dispatch.py#describe` | confirmed | Executed: the new case fails with `d89f8392`'s dispatcher and passes at `02e47435`; the code was read |
| 🟢 | round 1's yellow finding 2 is closed — no hook says a raising hook is skipped silently | `hooks/ledger-migrate.py`, `hooks/routing.py#rounds`, `hooks/root-migrate.py#git_mv` | confirmed | Read, and a `git grep` for the old phrasings found none |
| 🟢 | round 1's white finding 3 is closed — the cost comment names the linked worktree and the repository not opted in | `hooks/dispatch.py#record` | confirmed | Read |
| 🟢 | The new unit, round 1's case for a gate in two groups, is correct as code | `tests/test_a_gate_that_fails_says_so.py` | confirmed | Read, and executed in the narrow run |
| 🟢 | The or-operator's branch still consumes the failure of a `cd` that cannot fail, and `named` counts toward the state cap | `hooks/cmdline.py#walk_directories` | confirmed | Read, and the cap case passed in the narrow run |
| ❓ | Whether a sandboxed `Bash` can refuse a `cd` that `os.access` in the unsandboxed hook allows, and what `os.access` answers on Windows | `hooks/cmdline.py#_enters` | ❓ out of verified scope | Contract §13. Nothing here ran the harness's sandbox or Windows. The owner answers the sandbox half, and CI's `windows-latest` leg answers only the cases, which skip there |

## Paste-ready fixes

```python
# Flags that take the program from somewhere other than stdin -- `python -c`,
# `-m`, `node -e`/`-p`, `ruby -e`, `perl -e`/`-E` -- after which stdin is input
# to that program, which may hand it to a shell. A short one counts anywhere
# in a cluster: `-Bc` is `-B -c`.
ELSEWHERE_SHORT = "cmeEp"
ELSEWHERE_LONG = ("--eval", "--print")
```
```python
    for token in tokens[1:]:
        if token == "-":
            return True
        if token.lstrip("0123456789&")[:1] in ("<", ">"):
            # A redirect -- the `<<EOF` itself, `2>&1` -- is not an argument.
            continue
        if token.startswith("--"):
            if token.startswith(ELSEWHERE_LONG):
                return False
            continue
        if token.startswith("-"):
            # A cluster of short flags: `-Bc` is `-B -c`, so a program flag
            # anywhere in it takes the program from somewhere other than stdin.
            if any(c in ELSEWHERE_SHORT for c in token[1:]):
                return False
            continue
        return False
    return True
```
```python
    bodies, consumers, seg_start = [], [], 0
    # Where each command ends, so a body's consumer reads to the end of its
    # command and not only up to its `<<`: `python3 <<EOF -c '…'` runs `-c`.
    # `subst` counts open `$(`, which ends no command.
    bounds, subst = [], 0
```
```python
                pending.append((delim, dashed, seg_start, len(bounds)))
```
```python
        if ch == "\n":
            out.append(ch)
            seg_start = len(out)
            bounds.append(seg_start)
            i += 1
            comment, word_start = False, True
            for delim, dashed, start, k in pending:
                body_lines = []
                while i < n:
                    end = command.find("\n", i)
                    line = command[i:] if end == -1 else command[i:end]
                    i = n if end == -1 else end + 1
                    if (line.lstrip("\t") if dashed else line).rstrip("\r") == delim:
                        break
                    body_lines.append(line.rstrip("\r"))
                bodies.append("\n".join(body_lines))
                consumers.append("".join(out[start : bounds[k]]))
            pending = []
            continue
```
```python
        out.append(ch)
        if not comment and not braces and ch in ";&|()":
            # Inside `${…}` none of these ends a command, a `$(` opens a
            # substitution rather than a command (`sh -s $(true) python3`
            # feeds `sh`), and `>&`, `<&` and `&>` are redirects.
            if ch == "(" and i and command[i - 1] == "$":
                subst += 1
            elif ch == ")" and subst:
                subst -= 1
            elif not subst and not (
                ch == "&"
                and ((i and command[i - 1] in "<>") or command[i + 1 : i + 2] == ">")
            ):
                seg_start = len(out)
                bounds.append(seg_start)
```
```python
    states, parked, walked, env = [(cwd, None)], [], [], {}
    named = []
    # Whether every segment before this one was a `cd`. Only then is the
    # filesystem `_enters` reads the one the `cd` meets: the hook runs before
    # the whole command, and an earlier segment can move, remove or lock the
    # target first (`mv W X ; cd W ; git commit` commits where it started).
    settled = True
```
```python
            if target is not None and settled:
                cannot_fail = [
```
```python
            parked = _dedup(parked + list(failed))
        settled = settled and target is not None

        carried = list(moved)
```
```python
    if not isinstance(parsed, dict):
        return False
    # A falsy `hookSpecificOutput` was read as absent before #661, and still is.
    hook_out = parsed.get("hookSpecificOutput") or {}
    if not isinstance(hook_out, dict):
        return False
    decision = hook_out.get("permissionDecision")
    if decision:
        # The decision path reads the decision and its reason and nothing
        # else, so a `systemMessage` beside a `deny` must not drop the deny.
        reason = hook_out.get("permissionDecisionReason")
        return isinstance(decision, str) and (reason is None or isinstance(reason, str))
    message = parsed.get("systemMessage")
    return message is None or isinstance(message, str)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_gate_that_fails_says_so.py`, `tests/test_gate_judges_the_repo_it_commits_to.py`, `tests/test_dispatch.py` at `02e47435` | exit 0, 138 passed |
| Round 1's new case with `hooks/dispatch.py` at `d89f8392`, then restored | exit 1, 1 failed |
| 🔴 1: seven heredoc shapes through the gate at `02e47435`, and with `hooks/cmdline.py` and `hooks/commit-review-gate.py` at `e8e5f977` | five silent at head, all seven deny at `e8e5f977` |
| 🔴 1: four of those shapes in a real bash, with a body that creates a file | exit 0 each, the body ran |
| 🟡 2: `mv`, `mv` with newlines, `chmod` and two controls, head and `e8e5f977` | three silent at head, all deny at `e8e5f977` |
| 🟡 2: `mv d e ; cd d ; pwd` in a real bash | printed the starting directory |
| 🟡 3: `merge` on four shapes, head and `1ea0b7c2~1` | head prints nothing for all four; the base kept the deny or the message |
| The three proposed fixes applied together: the four new cases plus the three modules above and `tests/test_what_the_reader_understands.py` | exit 0, 270 passed |
| The four proposed cases at `02e47435`, without the fixes | exit 1, 4 failed |
| `bin/evidence-check --ledger` on this work item's fragment, `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.13.1.md`, `seal/releases/0.15.7.md` | exit 0 for each. The anchors hold, and G6–G8's claims are what 🔴 1 to 🟡 3 contradict |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, once, after the rounds settle, and it has not come due while 🔴 1, 🟡 2 and 🟡 3 are open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/dispatch.py#describe`, `hooks/dispatch.py#record` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/ledger-migrate.py` module docstring, lines 51–53 | round 1's 🟡 2 — fixed |
| round-1 | `hooks/dispatch.py#record` | round 1's ⬜ 3 — fixed |
| round-1 | `hooks/dispatch.py#main`, `hooks/dispatch.py#report` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_dispatch.py`, `tests/test_the_implementer_is_recorded.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/dispatch.py#record`, `hooks/dispatch.py#draw` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_gate_that_fails_says_so.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/dispatch.py#report` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

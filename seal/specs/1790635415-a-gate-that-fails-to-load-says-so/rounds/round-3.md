# 1790635415-a-gate-that-fails-to-load-says-so — review round 3

| Field | Value |
|---|---|
| Target SHA | 4f45313f68d5114e4fc7150baf93828818816308 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #660 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (a `#` glued to the heredoc delimiter hides the interpreter's program flag, so a shell-run commit reads as data) and 🔴 2 (a `cd` with an assignment-shaped prefix is trusted, so a `$(…)` side effect or an invalid-identifier prefix hides a commit in the session repository) |
| Loses a record or crashes | yes — 🔴 1 and 🔴 2 each read a real commit silent that the gate denied at `e8e5f977` |

- [ ] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 closed on its one reopening, so this record ends the run whatever it finds. Target round 2's fix diff `93d67a5b..7fc359c2` at HEAD `4f45313f`, with the fixes' new units as a finding surface, and one question put hard: does any command shape still read silent where `e8e5f977` judged it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A `#` glued to the heredoc delimiter word is a shell comment to `shlex` but not to the shell, so an interpreter's program flag after the `<<` is dropped from `program_is_data` and the shell-run body reads as data | `hooks/cmdline.py#program_is_data` | deferred owner | Executed: three shapes deny at `e8e5f977` and silent at HEAD, and each body ran as shell in a real bash. Round 2's 🔴 1 class, reopened. Fix verified at the tokenizer level, read-level for the gate (NAME NOT IN TREE, reverted with #662 and #665) |
| 🔴 2 | A `cd` with an assignment-shaped prefix is trusted not to fail, so a `$(…)` side effect in the value or an invalid-identifier prefix drops the session directory and hides a commit in the session repository | `hooks/cmdline.py#_cd_target`, `hooks/cmdline.py#walk_directories` | deferred owner | Executed: three shapes deny at `e8e5f977` and silent at HEAD, and bash lands the commit in the session repository. Round 2's 🟡 2 class, reopened. Contract §13 |
| ⬜ 3 | A deny with a falsy non-text `permissionDecisionReason` is refused as unreadable, where pre-#661 forwarded it | `hooks/dispatch.py#readable` | noted | Unchanged from `02e47435`, test-pinned on purpose, degrades to an end-of-turn notice. Not blocking |
| 🟢 | round 2's 🔴 1 documented shapes are closed — the five heredoc shapes deny at HEAD | `hooks/cmdline.py#program_is_data`, `hooks/cmdline.py#_heredoc_split` | confirmed | Executed: the planted case passes and the round-2 shapes deny; the class gap is 🔴 1 above |
| 🟢 | round 2's 🟡 2 documented shapes are closed — a move in a separate earlier segment denies at HEAD | `hooks/cmdline.py#walk_directories` | confirmed | Executed: the planted case passes; the class gap is 🔴 2 above |
| 🟢 | round 2's 🟡 3 is closed for what it named — a deny beside a non-text `systemMessage` stays a deny, and a falsy `hookSpecificOutput` is absent again | `hooks/dispatch.py#readable` | confirmed | Executed: the planted case passes and `merge` on those shapes was checked directly; the reason field is ⬜ 3 |
| 🟢 | The new units are correct as code — `SEPARATORS`, `RUN_STDIN` and the four cases | `hooks/cmdline.py`, `tests/test_gate_judges_the_repo_it_commits_to.py`, `tests/test_a_gate_that_fails_says_so.py` | confirmed | Read, and executed in the narrow run (141 passed) (NAME NOT IN TREE, reverted with #662 and #665) |
| ❓ | Whether a sandboxed `Bash` can refuse a `cd` that `os.access` in the unsandboxed hook allows, and what `os.access` answers on Windows | `hooks/cmdline.py#_enters` | ❓ out of verified scope | Carried from round 2. Nothing here ran the harness's sandbox or Windows. The owner answers the sandbox half, CI's `windows-latest` leg the cases |

## Paste-ready fixes

```python
    try:
        lexer = shlex.shlex(line, posix=False, punctuation_chars=True)
        lexer.whitespace_split = True
        # `#` is a comment to the shell only at a word start; glued into the
        # `<<` delimiter word (`<<EOF#x -c …`) it is a literal, and the shell
        # keeps the `-c …` after it. `shlex` treats `#` as a comment by
        # default and would drop those flags, reading a shell-run body as
        # data (round 3). Turn it off so the shape check sees them.
        lexer.commenters = ""
        tokens = list(lexer)
    except ValueError:
        return False
```
```python
    toks, subshell = strip_subshell(tokens)
    prefix_runs = False
    while toks and "=" in toks[0] and not toks[0].startswith("-"):
        name, _, value = toks[0].partition("=")
        if not name.isidentifier():
            # `a.b=1 cd W` is not an assignment to bash -- it runs `a.b=1` as
            # a command and the `cd` is its argument, so the shell never
            # performs the `cd`. Not a `cd` segment (round 3).
            return None
        if "$" in value or "`" in value:
            # `X=$(mv W M) cd W` runs the substitution before the `cd`, so the
            # `cd` can fail although W is there when the hook reads it.
            prefix_runs = True
        toks.pop(0)
    if not toks or toks[0] != "cd":
        return None
    args = [t for t in toks[1:] if t not in CD_FLAGS]
    operand = args[0] if args else ""
    if subshell or prefix_runs or len(args) > 1 or any(ch in operand for ch in EXPANDS):
        return "unknown", operand
```

## Executed probes

| What was run | Result |
|---|---|
| Narrow run: `tests/test_gate_judges_the_repo_it_commits_to.py`, `tests/test_a_gate_that_fails_says_so.py`, `tests/test_dispatch.py` at `4f45313f` | exit 0, 141 passed |
| 🔴 1: three `#`-delimiter heredoc shapes plus one control through the gate, at HEAD and with `hooks/cmdline.py` + `hooks/commit-review-gate.py` at `e8e5f977` | three silent at HEAD, all deny at `e8e5f977` |
| 🔴 1: the same three shapes in a real bash, body creating a file | the body ran as shell each time |
| 🔴 1: the round-2 shapes and controls through the gate | five deny at HEAD (round-2 closure confirmed) |
| 🔴 1: `shlex` tokenisation of `python3 <<EOF#x -c '…'`, default vs `commenters=""` | default drops the flags (`['python3','<<','EOF']`); `commenters=""` keeps them, so `program_is_data` returns False (NAME NOT IN TREE, reverted with #662 and #665) |
| 🔴 2: `$(…)`-prefix, invalid-identifier and control `cd` shapes through the gate at HEAD and `e8e5f977`, with the commit really run in bash | three silent at HEAD, all deny at `e8e5f977`, commit landed in the session repository |
| 🟡 3 / ⬜ 3: `merge` on deny-with-non-text-reason and systemMessage shapes at HEAD and `1ea0b7c2~1` | HEAD keeps the deny beside a non-text message and reads a falsy `hookSpecificOutput` as absent; HEAD drops a deny with a falsy non-text reason that `1ea0b7c2~1` forwarded |
| 🔴 1: fuzz, 6000 lines around `python3 - <<EOF`, 511 read as data, bodies run in bash | 0 mismatches (no other data/shell disagreement surfaced by this generator) |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — it is the sealer's, once, after the rounds settle; not this round's |

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
| round-2 | `hooks/cmdline.py#program_is_data`, `hooks/cmdline.py#_heredoc_split` | round 2's 🔴 1 — fixed |
| round-2 | `hooks/cmdline.py#walk_directories`, `hooks/cmdline.py#_enters` | round 2's 🟡 2 — fixed |
| round-2 | `hooks/dispatch.py#readable` | round 2's 🟡 3 — fixed |
| round-2 | `hooks/dispatch.py#describe` | round 2's 🟢 — confirmed |
| round-2 | `hooks/ledger-migrate.py`, `hooks/routing.py#rounds`, `hooks/root-migrate.py#git_mv` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline.py#walk_directories` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline.py#_enters` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🔴 1 — `#`-delimiter heredoc reads a shell-run body as data | fix on the branch before the PR merges; the run is capped at one reopening, so no round commissions it | the owner (a false silent on the commit gate is branch-caused; the ladder's default is not a new issue) |
| 🔴 2 — a `cd` with an assignment-shaped prefix is trusted | fix on the branch before the PR merges; the run is capped | the owner |

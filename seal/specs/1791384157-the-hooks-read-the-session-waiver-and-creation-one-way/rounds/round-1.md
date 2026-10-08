# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — review round 1

| Field | Value |
|---|---|
| Target SHA | 1680ea76ed0f3db68f26b4c09e72a342cf232bab |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 881 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `2f0d14b37e1fbeb08d00e62a716078e6cc5dd7f8..acc52a6aa2249b5049dff354f6bd7defada9c1f9`, 6 commits |
| Contract changes | _segment_finding → shape_of, _first_finding_in, main, round-1-report.md, round-1.md, pytest |
| New units | _ONE_BRACE (depth 1); _brace_spells_git (depth 1); test_a_pid_exported_for_another_session_is_not_recorded (depth 1); test_a_brace_that_makes_the_command_word_is_unrecognised (depth 1); test_a_brace_in_no_git_word_stays_silent (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (the Windows leg), 🔴 2 (survivor-check), 🟡 3 (a brace that makes the command word), 🟡 4 (`CLAUDE_PID` not tied to its session) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the build at 1680ea76, against 5623d728, since the release branch's #858 and #864 are not merged in yet. The spawn named seven things to attack. First, the failing Windows group-4 and release jobs of PR #881, read from their logs. Second, the one token reader in both directions over every spelling the docs name. Third, the brace rule over every unquoted expansion shape bash performs, and whether a quoted or escaped brace is ever stopped. Fourth, session identity by basename with CLAUDE_PID first. Fifth, the one git runner on Windows. Sixth, creation placement across ;, ||, && and subshells. Seventh, the overview's divergences, plus the reviewer's own axes with security first. It also ran the eight guard modules once. Facts arrived labelled. Executed by the orchestrator: gh pr checks 881. Read from the smith: the 32,431-pair probe, the reds, the mutations and the 45 modules.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The braced half of the git-binding case runs `bash`, which on `windows-latest` is the WSL launcher, and the required Windows leg fails | `tests/test_worktree_guard.py:2178` | **fixed** `89bca43f` | fixed at 89bca43f; executed: CI log, exit 1 with empty stderr; read: `tests/conftest.py#shell_probe` records the launcher |
| 🔴 2 | survivor-check exits 1 on 12 places in the release job; one is a false present-tense sentence, eleven are history | `tests/test_worktree_guard.py:729` | **fixed** `89bca43f` | fixed at 89bca43f — 151a0ad0; executed: reproduced at the target SHA, and exit 0 with the fix below |
| 🟡 3 | A brace that makes the command word (`{git,} switch x`) is silent in an ACTIVE tree | `hooks/worktree-guard.py:2270` | **fixed** `e60d35da` | fixed at e60d35da; executed: guard verdict probe, and the fix probed red then green |
| 🟡 4 | The lease writer trusts `CLAUDE_PID` without tying it to the session it records, so a nested session would record the outer pid | `hooks/session-lease.py:91` | **fixed** `cd7027df` | fixed at cd7027df; read: conditional on M1's open hook half; the base walked to the inner process |
| ⬜ 5 | A quoted space inside a brace hides it from the word-level `_BRACE` test | `hooks/worktree-guard.py:2007` | answered | No spelling of this kind switches a branch: bash makes `git rebase main 'feature x'` of `git rebase {main,'feature x'}`, which git refuses, as the report executed. Changing `_BRACE`'s word test would add a rule for a shape with no consequence, so it is left, and the report's entry is where the next reader of `_BRACE` finds the gap; executed: no switching spelling of this kind found |
| ⬜ 6 | shlex and bash disagree on `$'…\'…'`; a typed waiver after one is now refused, and the docstring's claim about unclosed quotes is false there | `hooks/tokens.py:33` | **fixed** `aee5615a` | fixed at aee5615a; executed: base and head probes; the grant direction is pre-existing |
| ❓ | Whether a hook process the harness spawns sees `CLAUDE_PID` (M1, the hook half) | `hooks/hooksession.py:68` | ❓ out of verified scope | no hook's environment can be printed without changing the installed configuration; the repository owner answers |
| ❓ | The Windows branches of In 1's adapter, In 2's lease route and the stub without `CLAUDECODE` | `hooks/worktree_consent.py:419` | ❓ out of verified scope | read only; the CI Windows leg answers once 🔴 1 is fixed |

## Paste-ready fixes

```python
from conftest import load_hook_module, shell_probe
```
```python
    # On a `windows-latest` runner `bash` resolves to the WSL launcher, which
    # exits 1 for every command it is handed (`conftest.shell_probe`). The
    # braced half needs a shell that expands braces, and the ubuntu and macOS
    # legs run it; the half above has asserted by now.
    why = shell_probe("bash")
    if why is not None:
        pytest.skip(f"bash: {why}")
    import shlex
```
```python
    """A token inside a quote that never closes is prose, and no consent
    read takes it: `hooks/tokens.py#given` reads nothing from where a split
    fails (#868). Read loosely, `[shared-tree-ok]` would turn this guard off
    with nobody asked — the regression two review rounds went into closing."""
```
```markdown
# Survivors — the hooks read the session, the waiver and a creation one way

`survivor-check --range origin/release/v0.21.0...HEAD` named 12 places at
`1680ea76`. Each was read in round 1. One stated a retired reading in the
present tense, the docstring of
`test_consent_is_not_read_out_of_a_command_that_did_not_parse`, and was
corrected. The rest are of two kinds:

- **Another work item's record.** Work item 1791163981's `spec.md` records
  what that item framed, when `has_token` carried its own `_without_bodies`.
- **History told as history, or a unit that still holds.** The docstrings of
  `has_token` and of cases in `tests/test_the_waiver_can_be_typed.py`,
  `tests/test_guard_resolves_the_tree_it_judges.py` and
  `tests/test_worktree_guard.py` say what a reading did before #868 in the
  past tense; `base_marker` states the base on purpose; and `main()` still
  reaches `segment_cwd`, through `worktree_consent.place`.

| Range | Grounds |
|---|---|
| `origin/release/v0.21.0...HEAD` | the removed readings' sentences stand in work item 1791163981's record and in docstrings that tell a reading's history as history or describe a unit that still holds; each was read in round 1, and the one stating a retired reading in the present tense was corrected |
```
```python
def _segment_finding(tokens, braced=False):
    """(shape, finding) for one segment; (None, None) where there is none."""
    parsed = parse_git(tokens)
    if parsed:
        return _git_finding(tokens, parsed, braced)
    # A brace in a word that spells `git` makes the command word itself:
    # `{git,} switch x` and `{,git} rebase a b` are git to bash, and no git
    # to the frozen reading (#856).
    if braced and any("git" in t and _BRACE.search(t) for t in tokens):
        return "unrecognised", Finding("brace", _spoken(tokens))
    finding = _hidden_in(tokens)
    return ("unrecognised", finding) if finding else (None, None)
```
```python
@pytest.mark.parametrize(
    "command", ["{git,} rebase main feature/x", "{,git} switch feature/x"]
)
def test_a_brace_that_makes_the_command_word_is_unrecognised(
    monkeypatch, capsys, repo, tmp_path, command
):
    """#856's class, one instance further: bash makes `git` itself of the
    brace, so the frozen reading reads no git and the guard said nothing in
    an ACTIVE tree. Red at `1680ea76`."""
    empty = tmp_path / "no-projects"
    empty.mkdir()
    monkeypatch.setattr(wg.worktree_consent, "PROJECTS_ROOT", str(empty))
    in_state(monkeypatch, repo, "active")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "deny" and STOP in reason and BRACE_EN in reason, reason
    in_state(monkeypatch, repo, "clean")
    assert verdict(monkeypatch, capsys, repo, command) == ("silent", "")


@pytest.mark.parametrize("command", ["echo {a,b}", "ls {x,y}.md && git status"])
def test_a_brace_in_no_git_word_stays_silent(monkeypatch, capsys, repo, command):
    """The other side: a brace in a segment that spells no git stops
    nothing."""
    in_state(monkeypatch, repo, "dirty")
    assert verdict(monkeypatch, capsys, repo, command) == ("silent", "")
```
```markdown
A brace that makes the command word itself (`{git,} switch x`, which bash
runs as `git switch x`) is the same shape, read from any word of a segment
the frozen reading reads as no git where that word spells `git`.
```
```python
    # `CLAUDE_PID` is this session's only where the environment is this
    # session's: a `claude` started from another session's Bash inherits
    # that session's pid, and a hook the harness gives no variable of its own
    # would record it. The walk answers there, as it did before #868 (§13).
    try:
        own = os.environ.get(hooksession.SESSION_VARIABLE) == payload.get(
            "session_id"
        )
        pid = hooksession.claude_pid(None if own else {})
    except Exception:
        pid = None
```
```python
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-exported")
```
```python
def test_a_pid_exported_for_another_session_is_not_recorded(repo, monkeypatch):
    """A `claude` started from another session's Bash inherits that
    session's `CLAUDE_PID`. The lease records the walk's answer there."""
    monkeypatch.setenv("CLAUDE_PID", "4242")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "the-outer-session")
    stub_process_tree(monkeypatch, 100, {100: (50, "/bin/zsh"), 50: (1, "claude")})
    rec = run_main_in_process(repo, monkeypatch, "sess-inner")
    assert rec["pid"] == 50, rec
```

## Executed probes

| What was run | Result |
|---|---|
| `gh run view` on the failing Windows job, failed-step log | `test_no_listed_form_moves_head_under_git` fails: `('rebase {master,feature/x}', 1, b'')` at line 2184 |
| `gh run view` on the failing release job, full log | `chain_check.py` printed the draft notice and passed; `survivor_check.py` exited 1 with 12 places |
| `python3 skills/code-review/scripts/survivor_check.py --range "origin/release/v0.21.0...HEAD"` in the clone at the target SHA | exit 1, 12 places, 103 removed sentences |
| the same with the docstring fix and the `survivors.md` below, `--exempt` | exit 0, 12 excused |
| `bin/test` on the eight suite-wide guard modules, in the clone | exit 0, 435 passed |
| `bin/test tests/test_worktree_guard.py tests/test_chain_hooks_hardening.py tests/test_lease_liveness.py -k "brace or no_listed_form or hardening or parity or lease or pid or claude or diff"` | exit 0, 122 passed |
| a token and brace probe over `tokens.given`, `has_token`, `has_marker`, `_unquoted_brace` and the frozen tokens, at the head | the results quoted in ⬜ 5, ⬜ 6 and 🟡 3 |
| the same consent reads over `git archive 5623d728 hooks` | the base guard and the base substring fallback read the `$'…'` tokens too |
| bash: `printf '[%s]'` over `{git,} rebase main feature/x`, `{,git} x`, `git rebase main{,}` | `[git][rebase][main][feature/x]`, `[git][x]`, `[git][rebase][main][main]` |
| a guard verdict probe through the module's `verdict` and `in_state` helpers, ACTIVE and dirty | both command-word braces silent; `git rebase {main,feature/x}` and the `$'…'` line stop |
| 🟡 3's fix applied in the clone, its two cases and two silent cases, then the 15 brace cases | 4 passed and 15 passed with the fix; the two command-word cases red without it |
| the process table and `CLAUDE_PID` in this session's Bash | `CLAUDE_PID` equals the `claude` ancestor's pid; no `claude` on this machine has a `claude` ancestor |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

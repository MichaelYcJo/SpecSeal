# Round 1 report — the hooks read the session, the waiver and a creation one way

Work item 1791384157 (#868, #856), draft PR #881 into `release/v0.21.0`.
Target SHA `1680ea76ed0f3db68f26b4c09e72a342cf232bab`, diff
`5623d728...1680ea76`. Reviewed in a `--no-local` clone at the target SHA.
No earlier round exists, so nothing is carried.

## How the findings relate

```
CI red at the pull request
  ├─ 🔴 1  the Windows leg: the new braced half of one case runs `bash`,
  │        which on that runner is the WSL launcher
  └─ 🔴 2  the release job: survivor-check finds 12 places carrying removed
           wording; the smith's verification list never ran it
#856's class, enumerated against the shell
  ├─ 🟡 3  a brace in the command word (`{git,} switch x`) is still silent
  │        in an ACTIVE tree
  └─ ⬜ 5  a quoted space inside a brace hides it from the word-level test
#868's session reader
  └─ 🟡 4  the lease writer trusts `CLAUDE_PID` from an environment that may
           be another session's
#868's token reader
  └─ ⬜ 6  `$'…\'…'` quoting: shlex and bash disagree, in both directions
```

The two 🔴 are why the pull request cannot merge today. Neither is a defect
in a hook; both are fixed in a test and in the work item's own records. The
two 🟡 are defects in what this branch ships, and each has a probe-backed
paste-ready fix.

## 🔴 1 — The Windows leg fails because the new braced half runs the WSL launcher

**Executed** (orchestrator's `gh pr checks 881`, then the failing job's log
read by me): `pytest (windows-latest, … --group 4)` fails on
`tests/test_worktree_guard.py::test_no_listed_form_moves_head_under_git`
with `AssertionError: ('rebase {master,feature/x}', 1, b'')` at
`tests/test_worktree_guard.py:2184`.

**Cause, read**: the braced half this branch added runs
`subprocess.run(["bash", "-c", …])` (`tests/test_worktree_guard.py:2178`).
On a `windows-latest` runner `bash` resolves to the WSL launcher with no
distribution installed, which exits non-zero for every command and prints
its notice to stdout, so stderr is empty. `tests/conftest.py#shell_probe`
records exactly this, and every other case in the tree that runs `bash`
asks it or an equivalent first. This one does not. The exit 1 and the empty
stderr in the log are that signature.

**Why it matters**: the job is a required leg, so the pull request stays
red on a test defect, and the overview's claim that S13 is "executed under
bash" holds only on the POSIX legs.

The fix skips the braced half where `bash` is not a shell, as
`tests/test_one_heredoc_shape_agrees_with_the_shell.py` does. The first half
has asserted by then, so a regression there still fails on Windows. Splitting
the braced half into its own case would keep the first half reported as a
pass there; that is the smith's call.

## 🔴 2 — The release job fails on survivor-check, which the smith never ran

**Executed**: the release job's log shows `chain-check` printing its draft
notice and passing, and the next step, `survivor_check.py --range
"origin/release/v0.21.0...HEAD"`, exiting 1 with "12 place(s) still carry
wording this range removed". I reproduced it in the clone at the target SHA:
exit 1, the same 12 places, against 103 removed sentences.

The overview's `verified` line names `bin/evidence-check` and
`bin/correction-check` and not `bin/survivor-check`, which is why this
reached CI.

Each place was read:

- **One is a live sentence stating a retired reading.**
  `tests/test_worktree_guard.py:729`, the docstring of
  `test_consent_is_not_read_out_of_a_command_that_did_not_parse`, says in the
  present tense that the commit gate's `has_marker` falls back to a
  substring test. In 3 removed that fallback, so the sentence is now false.
- **Eleven are history or records.** Work item 1791163981's `spec.md:175`
  and `:178` record what that item framed. The docstrings at
  `tests/test_the_waiver_can_be_typed.py:130`, `:131`, `:134`,
  `tests/test_guard_resolves_the_tree_it_judges.py:256`, `:353`, `:1575`,
  `hooks/worktree-guard.py:352` and `tests/test_worktree_guard.py:782` narrate
  a reading's history as history, or describe a unit that still holds
  (`main()` still reaches `segment_cwd`, through `worktree_consent.place`).
  `base_marker` at
  `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py:558` states the
  base on purpose.

**Executed**: with the docstring corrected and the `survivors.md` below in
the clone, `survivor_check.py` exits 0, every one of the 12 excused.

## 🟡 3 — A brace in the command word still switches a branch silently in an ACTIVE tree

**Executed** (a probe through the guard's own `verdict` and `in_state`
helpers): `{git,} rebase main feature/x` and `{,git} switch feature/x` are
`silent` in an ACTIVE tree and in a dirty one. bash makes `git rebase main
feature/x` and `git switch feature/x` of them (executed:
`printf '[%s]' {,git} x` prints `[git][x]`).

**Cause, read**: `_unquoted_brace` reads the brace, but `_git_finding` is
asked only where `parse_git` reads the segment as git. A brace that makes the
command word makes a segment the frozen reading reads as no git at all, so
`_segment_finding` falls through to `_hidden_in`, which does not know the
spelling.

**Why it matters**: #856's class is "the shell makes other words before git
runs", and §12 asks the fix to answer every instance of it. In 5 scoped the
rule to "a git segment", which leaves the one instance where the brace makes
`git` itself. It is a crafted spelling, and it is the stop the guard exists
to make: a branch moved under another session. The base was silent too, so
this is an unfinished class rather than a regression.

**Executed**: the fix below, applied in the clone, turns both commands into a
brace `deny` in an ACTIVE tree, keeps them silent in a clean single-stream
tree, keeps `echo {a,b}` and `ls {x,y}.md && git status` silent in a dirty
tree, and leaves the 15 existing brace cases green. Without it, the two
command-word cases are red.

## 🟡 4 — The lease writer would record another session's pid for a session started inside one

**Read, not run.** `hooks/session-lease.py` now records
`hooksession.claude_pid()`, which takes `CLAUDE_PID` from the hook's
environment before it walks. `questions.md` M1 leaves open whether the
harness puts `CLAUDE_PID` in a hook's environment. The spec's own
measurement says the top-level `claude` process carries no `CLAUDE_*`
variable, so a hook that is not given one inherits whatever `claude` itself
inherited.

A `claude` started from another session's Bash call inherits that outer
session's `CLAUDE_PID`. Its hooks would then record the outer pid in the
inner session's lease. Three effects follow, each read from the code:

- the guard's liveness check keeps the inner lease alive while the outer
  session lives, and retires it while the inner session still works, which
  is the expensive direction (`worktree-guard-spec.md` §*Unknowns resolve
  conservatively*);
- the commit gate's lease route, asked from the inner session's Bash, looks
  for the inner pid and finds no lease;
- two leases now name the outer pid, so the outer session's lease route
  answers no session.

The base walked from the hook to its nearest `claude` ancestor, which is the
inner process. So where M1's answer is *no*, this is a regression for nested
sessions. No nested `claude` runs on this machine, so it was not reproduced.

The fix ties the variable to the session it is recorded for: the hook trusts
`CLAUDE_PID` only where the same environment's `CLAUDE_CODE_SESSION_ID` is
the payload's `session_id`, and walks otherwise. That is the walk the base
had wherever the harness gives the hook neither variable, and the variable
wherever it gives both.

## ⬜ 5 — A quoted space inside a brace hides it from the word-level test

**Executed**: `git rebase {main,'feature x'}` has `_unquoted_brace` True, but
the frozen word is `{main,feature x}`, which `_BRACE` refuses because of the
space, so the segment reads `listed`. bash makes `git rebase main 'feature
x'` of it, which git refuses, and no spelling of this kind that switches a
branch was found. The word-level test could ask the regex of the word with
its whitespace taken out. Recorded so the next reader of `_BRACE` knows the
gap is there.

## ⬜ 6 — shlex and bash disagree on `$'…\'…'`, in both directions

**Executed**: `tokens.given` reads `[shared-tree-ok]` out of
`git switch x && echo $'it\'s [shared-tree-ok] x'`, where bash runs it as
part of a quoted string. The base guard's `has_token` and the base commit
gate's substring fallback read it too, so this is not new.

The other direction is new for the commit gate. `git commit -m $'it\'s' #
[no-review]` waived at the base and is refused now, because shlex closes the
quote at `\'` and reads the rest as an unclosed quote. The way out the
refusal names, `: '[no-review]';` typed in front, still waives.

`hooks/tokens.py`'s docstring says "A word inside an unclosed quote is prose
a shell would refuse to run". That is false for this spelling, which bash
runs. A sentence naming ANSI-C quoting as the reader's known disagreement
would make the docstring true.

## Claims checked against the code

| The account said | What I found |
|---|---|
| overview: "the eight suite-wide guard modules" green | executed: 435 passed at the target SHA |
| overview: "Windows branches read, not run" | true, and the Windows leg ran one new case and it failed (🔴 1) |
| spec S13: the git-binding case "executed under bash" | true on macOS and Linux only (🔴 1) |
| overview: verification names `bin/correction-check` | `bin/survivor-check` was not run; it fails (🔴 2) |
| overview row 1: the partial read "reads no token the base's reads did not" over 32,431 pairs | consistent with my probes: every token it reads that a shell would not offer, the base read too (⬜ 6) |
| spec In 5: a git segment holding a brace is unrecognised | true for a git segment; a brace that makes the command word is not one (🟡 3) |
| spec In 2: the writer and the reader find the same process | true where `CLAUDE_PID` is the hook's own session's; not tied to it (🟡 4) |
| spec In 1: one placement for guard and writer | read: `place` uses `optin.repo_root` where `judgeable` used `repo_paths`; both run `git rev-parse --show-toplevel` and answer "" for no directory, so they agree |
| spec In 4: every caller of the one runner handles None | read: every `gate.git` caller in `hooks/` either writes `or ""` or passes the answer to `gate.lines`; `hooks/review-skill-gate.py` keeps its own `git`, which is outside this item |
| "every new case red first", "one mutation per unit" | not re-run; carried as the smith's claim. My own new probe for 🟡 3 was red without its fix |

## Regression tests to plant

- `tests/test_worktree_guard.py`: the command-word brace case below (🟡 3),
  red at the target SHA by my probe.
- `tests/test_lease_liveness.py`: a case where the environment carries
  `CLAUDE_PID` and a `CLAUDE_CODE_SESSION_ID` naming another session, and the
  stubbed process tree names a different `claude` ancestor; the lease must
  record the ancestor's pid (🟡 4). The existing
  `test_the_lease_records_the_pid_the_harness_exports` sets the session
  variable to its own session after the fix.

## Facts for the evidence ledger

- `hooks/worktree-guard.py#_segment_finding`: a brace in a word spelling
  `git` is a `brace` finding in a segment the frozen reading does not read as
  git (after 🟡 3's fix).
- `hooks/session-lease.py#main`: `CLAUDE_PID` is recorded only where the
  hook's `CLAUDE_CODE_SESSION_ID` is the payload's `session_id` (after 🟡 4's
  fix).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The braced half of the git-binding case runs `bash`, which on `windows-latest` is the WSL launcher, and the required Windows leg fails | `tests/test_worktree_guard.py:2178` | open | executed: CI log, exit 1 with empty stderr; read: `tests/conftest.py#shell_probe` records the launcher |
| 🔴 2 | survivor-check exits 1 on 12 places in the release job; one is a false present-tense sentence, eleven are history | `tests/test_worktree_guard.py:729` | open | executed: reproduced at the target SHA, and exit 0 with the fix below |
| 🟡 3 | A brace that makes the command word (`{git,} switch x`) is silent in an ACTIVE tree | `hooks/worktree-guard.py:2270` | open | executed: guard verdict probe, and the fix probed red then green |
| 🟡 4 | The lease writer trusts `CLAUDE_PID` without tying it to the session it records, so a nested session would record the outer pid | `hooks/session-lease.py:91` | open | read: conditional on M1's open hook half; the base walked to the inner process |
| ⬜ 5 | A quoted space inside a brace hides it from the word-level `_BRACE` test | `hooks/worktree-guard.py:2007` | open | executed: no switching spelling of this kind found |
| ⬜ 6 | shlex and bash disagree on `$'…\'…'`; a typed waiver after one is now refused, and the docstring's claim about unclosed quotes is false there | `hooks/tokens.py:33` | open | executed: base and head probes; the grant direction is pre-existing |
| ❓ | Whether a hook process the harness spawns sees `CLAUDE_PID` (M1, the hook half) | `hooks/hooksession.py:68` | ❓ out of verified scope | no hook's environment can be printed without changing the installed configuration; the repository owner answers |
| ❓ | The Windows branches of In 1's adapter, In 2's lease route and the stub without `CLAUDECODE` | `hooks/worktree_consent.py:419` | ❓ out of verified scope | read only; the CI Windows leg answers once 🔴 1 is fixed |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🔴 1

`tests/test_worktree_guard.py`, the import at the top:

```python
from conftest import load_hook_module, shell_probe
```

and in `test_no_listed_form_moves_head_under_git`, in place of the line
`    import shlex` that opens the braced half:

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

### 🔴 2

`tests/test_worktree_guard.py`, the docstring of
`test_consent_is_not_read_out_of_a_command_that_did_not_parse`:

```python
    """A token inside a quote that never closes is prose, and no consent
    read takes it: `hooks/tokens.py#given` reads nothing from where a split
    fails (#868). Read loosely, `[shared-tree-ok]` would turn this guard off
    with nobody asked — the regression two review rounds went into closing."""
```

A new file,
`seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md`:

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

### 🟡 3

`hooks/worktree-guard.py#_segment_finding`:

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

`tests/test_worktree_guard.py`, beside
`test_a_brace_expansion_in_a_git_word_is_unrecognised`:

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

`docs/worktree-guard-spec.md` §A, after "A switch and a creation keep their
own rules.":

```markdown
A brace that makes the command word itself (`{git,} switch x`, which bash
runs as `git switch x`) is the same shape, read from any word of a segment
the frozen reading reads as no git where that word spells `git`.
```

### 🟡 4

`hooks/session-lease.py#main`, in place of the `claude_pid` call:

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

`tests/test_lease_liveness.py`,
`test_the_lease_records_the_pid_the_harness_exports`, beside its
`CLAUDE_PID` line:

```python
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-exported")
```

and the case for the other side:

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

Needs a fix: yes — 🔴 1 (the Windows leg), 🔴 2 (survivor-check), 🟡 3 (a
brace that makes the command word), 🟡 4 (`CLAUDE_PID` not tied to its session)

Loses a record or crashes: no

The broad gate has not come due: this round leaves four findings open.

## Proof block

Files opened in this round:

- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/`:
  `spec.md`, `overview.md`, `questions.md`, `routing.md`, `handoff.md`
- the diff `5623d728...1680ea76` of `hooks/tokens.py`, `hooks/hooksession.py`,
  `hooks/session-lease.py`, `hooks/githooks.py`, `hooks/gate.py`,
  `hooks/commitgate.py`, `hooks/worktree-guard.py`,
  `hooks/worktree_consent.py`, `hooks/commit-review-gate.py`, `docs/`, and
  `tests/test_worktree_guard.py`
- `hooks/gate.py` (`arms_missing`), `hooks/commit-review-gate.py`
  (`touches_code`, `changed_paths`), `hooks/session-lease.py` (`main`),
  `hooks/hooksession.py` (`from_lease`), `hooks/worktree-guard.py`
  (`_judgment_text`, `repo_paths`, `_segment_finding`, `has_token`),
  `hooks/optin.py` (`repo_root`), `hooks/githooks.py` (`MARKER`)
- `tests/conftest.py` (`shell_probe`), `tests/test_the_reader_agrees_with_bash.py`,
  `tests/test_one_heredoc_shape_agrees_with_the_shell.py`,
  `tests/test_lease_liveness.py`, and each of the 12 survivor places
- `skills/code-review/scripts/survivor_check.py` (the exemption rows),
  `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/survivors.md`,
  `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/survivors.md`
- the logs of CI jobs 113090774051 and 113090773733

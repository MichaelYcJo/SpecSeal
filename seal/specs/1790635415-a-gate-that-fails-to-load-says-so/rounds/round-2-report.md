# Round 2 report — a gate that fails to load says so

Target: branch `fix/28-a-gate-that-fails-to-load-says-so` at `02e47435`, base
`release/v0.16.0` at `551c7967`. Two targets with two jobs:

- **Verifying**, round 1's fixes: `git diff d89f8392..fa556996`, plus the one
  new unit the record's `New units` row names.
- **Finding**, phases 4 and 5, which nobody had reviewed:
  `git diff b3ad918d..02e47435`.

Reviewed in a `git clone --no-local` of the worktree at `02e47435`. Round 1's
record was read for coordinates. Its verdicts were re-derived, not carried.

## How the findings relate

Round 1's three fixes hold. Phases 4 and 5 each open a false allow, and all
three have one cause: each rule was checked against the shapes it was written
for, and not against the shapes next to them.

1. **#665 reads a commit silent that the shell runs** (🔴 1). The body's
   consumer is read only up to its `<<`, so a flag or a script after the
   redirect is never seen. A `$(…)` or a `;` inside `${…}` also cuts the
   consumer short. Five shapes the gate denied at `e8e5f977` now read silent,
   and a real shell runs each body as shell.
2. **#662 trusts a filesystem reading the command itself can change**
   (🟡 2). The hook asks whether the `cd` target exists before any segment
   runs. An earlier segment that moves or locks the target makes the `cd`
   fail, and the commit then runs in the session's directory, which is no
   longer judged.
3. **#661 drops a deny the base kept** (🟡 3). `readable` refuses a
   `systemMessage` that is not text even on the decision path, which never
   reads it. A deny carried beside such a message is now dropped. At `551c7967`
   it survived.

The first two are the direction the prompt named as where a defect leaves the
root: a real commit that is no longer judged.

## Round 1's fixes

### Round 1's yellow finding 1 is closed

`hooks/dispatch.py#describe` now names every group that loads a gate whose
failure phase is `load`, and names only the group it was seen in for `run`.
The closing clause lists only the groups where another gate decided, so
`post-agent` is named among the failures and not in the closing clause.

- **Executed.** The new case
  `tests/test_a_gate_that_fails_says_so.py::test_a_gate_that_fails_to_load_names_every_group_that_loads_it`
  fails with `hooks/dispatch.py` checked out at `d89f8392` (exit 1) and passes
  at `02e47435`. That is §15's seen-red, done again this round rather than
  taken from the fixer.
- **Read.** The case also plants a hand-written `run` record and checks that
  it names `pre-agent` alone. The paste-ready fix in round 1 had one closing
  clause for all groups. The committed version is narrower and correct.

### Round 1's yellow finding 2 is closed

`hooks/ledger-migrate.py`, `hooks/routing.py#rounds` and
`hooks/root-migrate.py#git_mv` no longer say a raising hook is skipped
silently. **Read**, and a `git grep` over `hooks/`, `docs/` and both READMEs
for the old phrasings found none left.

### Round 1's white finding 3 is closed

The comment in `hooks/dispatch.py#record` now names the linked worktree's
`git rev-parse` and the reload of `optin.py` in a repository not opted in.
**Read.**

### The new unit, judged as code

The case above is correct as code. It builds the failure through the real
dispatcher and reads the real `stop` output. It pins both halves: a load
failure in two groups, and a run failure in one.

Round 1's two ❓ rows, the on-screen render and the Windows render, were not
closed verdicts and are not re-judged here. They stay with the answerers
round 1 named.

## Phases 4 and 5 — spec compliance

Every claim in `phases/phase-4.md`, `phases/phase-5.md` and the issues was
checked against the code.

| Claimed | Found |
|---|---|
| #665: "Any program flag (`-c`, `-m`, `-e`, …), a script file, an untokenisable command and an unlisted name read as shell" | False for a flag or script written after the `<<`, and for a program flag bundled with another (`-Bc'…'`). Executed, 🔴 1 |
| #665: "What this opens is already open", "nothing is open that was closed" | False. Five shapes were denied at `e8e5f977` and read silent at `02e47435`. Executed, 🔴 1 |
| #662: "The allows are bounded to states the shell does not reach" | False. `mv W X ; cd W ; git commit` reaches the session's directory, and the gate reads it silent. Executed, 🟡 2 |
| #662: the frame's premise was wrong, since the walk already reads a newline as `;` | Confirmed by reading `hooks/cmdline.py#walk_directories`: the `;` branch merges `parked` into the running states |
| #662: the or-operator still consumes the failure of a `cd` that cannot fail | Confirmed by reading: `named` joins `parked` in the or-operator's branch only. The 70-`cd` cap case also passes |
| #661: every other type "raised there" | False for a `systemMessage` beside a decision, and for a falsy `hookSpecificOutput`. Neither raised at `551c7967`, and both are dropped now. Executed, 🟡 3 |
| #661: `null` is allowed because the merge already read a null field as absent | Confirmed, and the same reasoning covers `false`, `0`, `""` and `[]` for `hookSpecificOutput`, which the old `or {}` also read as absent |

## Findings

### 🔴 1 — A commit a shell runs reads silent when the interpreter's program flag comes after the heredoc

**Where.** `hooks/cmdline.py#_heredoc_split` records the consumer as the text
from the last separator up to the `<<`. `hooks/cmdline.py#program_is_data`
then reads only that text.

**What is wrong.** Three ways the consumer comes out wrong:

- **Words after the `<<` are never read.** `python3 <<'EOF' -c '…'` gives the
  consumer `python3`, which reads as data. Python then runs `-c`, and stdin is
  input to that program. The same holds for `perl <<'EOF' -e '…'` and
  `python3 <<'EOF' run.py`.
- **A bundled short flag is missed.** `python3 -Bc'…'` has one token,
  `-Bc…`. The check is `startswith("-c")`, so the token reads as a harmless
  flag.
- **The boundary is reset where the shell does not end a command.** The `(`
  of `$(`, its `)`, a `;` inside `${…}`, and the `&` of `>&` all reset the
  consumer's start. `sh -s $(true) python3 <<'EOF'` gives the consumer
  `python3`, while the real consumer is `sh -s`, which runs its stdin as
  shell.

**Executed.** Each head below, followed by a body of `git commit -m x`, went
through the gate's `main()` in an opted-in repository with no declaration:

| Command head | `e8e5f977` | `02e47435` | Real `bash`: body ran as shell |
|---|---|---|---|
| `python3 <<'EOF' -c '<runs stdin as shell>'` | deny | silent | yes |
| `python3 -Bc'<runs stdin as shell>' <<'EOF'` | deny | silent | yes |
| `perl <<'EOF' -e 'system(join("",<STDIN>))'` | deny | silent | not run |
| `sh -s $(true) python3 <<'EOF'` | deny | silent | yes |
| `sh -s ${x:-;X=} python3 - <<'EOF'` | deny | silent | yes |
| `bash <<'EOF'` (control) | deny | deny | |
| `python3 -c '…' <<'EOF'` (control) | deny | deny | |

The "real bash" column ran each shape with a body that only created a file,
and the file existed afterwards. `sh -s >&python3 <<'EOF'` is the same class
through the `&` reset. It was **read**, and executed only against the fix
below, where it fires.

**Why it matters.** The rule the owner approved in #665 says an interpreter
given `-c` or a script is read as shell. The docstring of `program_is_data`,
`docs/commit-review-gate-spec.md` and ledger row G7 all say the same. The
code does not do it for these shapes. A body of plain `git commit` that a
shell really runs is now a commit nobody judges. It was judged before this
branch.

**The fix** reads the consumer to the end of its command and skips the
redirect words. It resets the boundary only where the shell ends a command,
and it reads a short-flag cluster letter by letter (fence below). It was
**executed** against `tests/test_a_gate_that_fails_says_so.py`,
`tests/test_gate_judges_the_repo_it_commits_to.py`, `tests/test_dispatch.py`
and `tests/test_what_the_reader_understands.py`, with the three fixes of this
report applied together: exit 0, 270 passed. That count includes every #665
case the smith planted.

- **What changes elsewhere.** A `python3 -` heredoc inside `$( … )` now reads
  as shell, and `python3 -X dev -` or `python3 -Wignore -` does too. Both
  prompt where they read silent. That is the asking side, which #665 names as
  the default for anything unlisted.
- **Words to correct with it** (§14): the `_heredoc_split` docstring ("up to
  its `<<`"), and ledger row G7's description of the consumer.

### 🟡 2 — A `cd` whose target an earlier segment moves or locks is still trusted not to fail

**Where.** `hooks/cmdline.py#walk_directories`, the `cannot_fail` block, and
`hooks/cmdline.py#_enters`.

**What is wrong.** `_enters` asks the filesystem when the hook runs. The
whole command runs after that, so a segment before the `cd` can change what
the `cd` meets. `mv W X ; cd W ; git commit` finds W at hook time, so the
`cd` "cannot fail" and the session's directory is dropped at the `;`. In the
shell, `mv` runs first, the `cd` fails, and the commit runs in the session's
directory.

**Executed.** The session was opted in and undeclared, and W was declared:

| Command | `e8e5f977` | `02e47435` |
|---|---|---|
| `mv W X ; cd W ; git commit -m x` | deny | silent |
| the same with newlines | deny | silent |
| `chmod 000 W ; cd W ; git commit -m x` | deny | silent |
| `cd <missing> ; git commit -m x` (control) | deny | deny |

A real `bash` given `mv d e ; cd d ; pwd` printed the directory it started
in.

**Why it matters.** The phase record gives the failure direction as "bounded
to states the shell does not reach", and names only a race between the hook
and the shell. This is not a race. It is deterministic, and the command
causes it. Contract §13 asks for the guarantee to be removed and the code to
still refuse. Here the guarantee is that the hook's filesystem is the one the
`cd` meets, and an earlier segment removes it.

**The fix** trusts `_enters` only while every earlier segment was a `cd`.
Every shape #662 measured starts with its `cd`, so none of them changes. It
was executed in the same run as 🔴 1: every #662 case still passes, and the
`mv` shape fires.

**Words to correct with it:** `docs/commit-review-gate-spec.md`'s
`cd X ; git commit` row and its #662 paragraph, and ledger row G8. Each needs
"and no earlier segment of the command". The phase-5 lines for the pull
request also need correcting: "bounded to states the shell does not reach".

### 🟡 3 — A deny beside a `systemMessage` that is not text is now dropped

**Where.** `hooks/dispatch.py#readable`.

**What is wrong.** `readable` checks `systemMessage` for every object. The
decision path of `hooks/dispatch.py#merge` never reads `systemMessage`, so at
`551c7967` a deny carrying `"systemMessage": 3` merged as a deny. Now the
whole output is `unreadable`, it is dropped, and the call goes ahead. It is
reported at the end of the turn. The same over-refusal drops
`{"hookSpecificOutput": false, "systemMessage": "m"}`, which the old
`or {}` read as a message.

**Executed**, `merge` called directly on each dispatcher:

| Output | `1ea0b7c2~1` | `02e47435` |
|---|---|---|
| a deny with `"systemMessage": 3` | the deny | nothing |
| a deny with `"systemMessage": ["a"]` | the deny | nothing |
| `{"hookSpecificOutput": false, "systemMessage": "m"}` | printed as is | nothing |
| `{"hookSpecificOutput": [], "systemMessage": "m"}` | printed as is | nothing |

**Why it matters.** #661's acceptance is that a neighbour's deny survives.
This change drops a deny that survived before. No gate prints this shape
today (**read**, not executed across every gate), so what ships is a rule
that is stricter than its own docstring says, on the one field that decides.

**The fix** checks the decision and its reason on the decision path, the
message on the message path, and reads a falsy `hookSpecificOutput` as
absent again. Every shape in `UNREADABLE` stays unreadable, and the narrow run
above passed with it applied.

**Words to correct with it:** the `readable` docstring, and ledger row G6's
list of refused shapes.

## Regression tests to plant

Each was **seen red at `02e47435`** and green with the fixes applied, in the
same run. The data-side case is new in shape rather than red for a defect:
it fails at head only because head's consumer never contains a `<<`. It pins
that the fix keeps `python3 -` data.

Destination `tests/test_gate_judges_the_repo_it_commits_to.py`, for 🔴 1 and
🟡 2:

```python
RUN_STDIN = "import subprocess,sys; subprocess.run(sys.stdin.read(), shell=True)"


def test_a_body_read_to_the_end_of_its_command_is_still_shell(tmp_path):
    """#665's consumer is the whole command, not the text before its `<<`: a
    program flag or a script after the redirect, a flag bundled with another,
    and a `$(…)`, `${…;…}` or `>&` before the interpreter's name all leave a
    body that a shell runs."""
    here = make_repo(tmp_path / "opted-in", opted_in=True)
    heads = (
        f"python3 <<'EOF' -c '{RUN_STDIN}'",
        f"python3 -Bc'{RUN_STDIN}' <<'EOF'",
        "perl <<'EOF' -e 'system(join(\"\",<STDIN>))'",
        "python3 <<'EOF' run.py",
        "sh -s $(true) python3 <<'EOF'",
        "sh -s ${x:-;X=} python3 - <<'EOF'",
        "sh -s >&python3 <<'EOF'",
    )
    for n, head in enumerate(heads):
        command = f"{head}\ngit commit -m x\nEOF"
        assert fired(run(command, here, session=f"s-{n}")), head


def test_a_redirect_beside_an_interpreter_leaves_its_body_data():
    """The consumer now carries its redirects, the `<<` among them, and none
    of them is a script argument."""
    for consumer in (
        "python3 - <<EOF",
        "python3 <<EOF",
        "node <<EOF",
        "python3 - 2>&1 <<EOF",
        "python3 - &>/dev/null <<EOF",
        "/usr/bin/python3.12 -u - <<EOF",
    ):
        assert reader.program_is_data(consumer), consumer
    command = "x=1; python3 - <<'EOF' 2>&1 | tee log\nA\nEOF"
    assert reader.shell_bodies(command) == []


def test_a_cd_whose_target_an_earlier_segment_moved_keeps_both(tmp_path):
    """#662's `_enters` reads the filesystem before the command runs, so a
    segment before the `cd` that moves its target makes the `cd` fail, and
    the commit runs where the shell started."""
    here = make_repo(tmp_path / "session", opted_in=True)
    there = make_repo(tmp_path / "declared", opted_in=True)
    declare_routing(there)
    moved = tmp_path / "moved"
    for n, sep in enumerate((" ;", "\n")):
        command = f"mv {sh(there)} {sh(moved)}{sep} cd {sh(there)}{sep} git commit -m x"
        assert fired(run(command, here, session=f"m-{n}")), repr(command)
```

Destination `tests/test_a_gate_that_fails_says_so.py`, for 🟡 3:

```python
def test_a_deny_beside_a_message_that_is_not_text_still_denies():
    """#661 must not drop a deny the merge read before: its decision path
    never reads `systemMessage`, and a falsy `hookSpecificOutput` was absent."""
    d = load(os.path.join(HOOKS, "dispatch.py"), "dispatch_for_a_deny")
    deny = {"hookSpecificOutput": {"permissionDecision": "deny"}, "systemMessage": 3}
    assert d.classify(json.dumps(deny)) == ("decision", deny)
    falsy = {"hookSpecificOutput": False, "systemMessage": "m"}
    assert d.classify(json.dumps(falsy)) == ("json", falsy)
    assert decision_of(d.merge([json.dumps(deny)], "PreToolUse")) == "deny"
```

The round's probe loaded the dispatcher through `load_hook_module` from `tests/conftest.py`.
The fence above uses the module's own `load`, which the file already imports.
Check that `decision_of` is imported there before pasting.

## Facts for the evidence ledger

- G6 is false as written: a deny with a non-text `systemMessage`, and a falsy
  `hookSpecificOutput` beside a message, are dropped at `02e47435` and were
  read at `551c7967`. Executed.
- G7 is false as written: a program flag or script after the `<<`, a bundled
  flag, and a `$(…)`, `${…;…}` or `>&` before the name leave a shell-run body
  read as data. Executed for five shapes.
- G8 needs "no earlier segment of the command changes the target". Executed.

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

## Paste-ready fixes

### 🔴 1

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

In `_heredoc_split`, four edits. First, beside the other state:

```python
    bodies, consumers, seg_start = [], [], 0
    # Where each command ends, so a body's consumer reads to the end of its
    # command and not only up to its `<<`: `python3 <<EOF -c '…'` runs `-c`.
    # `subst` counts open `$(`, which ends no command.
    bounds, subst = [], 0
```

Second, where a `<<` is found:

```python
                pending.append((delim, dashed, seg_start, len(bounds)))
```

Third, the newline branch:

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

Fourth, the reset at the bottom of the loop:

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

### 🟡 2

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

### 🟡 3

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

Needs a fix: yes — 🔴 1 (a shell-run heredoc body reads as data), 🟡 2 (a cd whose target an earlier segment moves is trusted), 🟡 3 (a deny beside a non-text message is dropped)
Loses a record or crashes: yes — 🔴 1 and 🟡 2 each read a real commit silent, which the gate judged at e8e5f977

## Proof

Files opened this round, in the clone at `02e47435` unless noted:

- `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/rounds/round-1.md`,
  `rounds/round-1-report.md` (the orchestrator's tree, headings and opening),
  `plan.md` §*Phases*, `phases/phase-4.md`, `phases/phase-5.md`, and the rows
  of `seal/ledger/1790635415-a-gate-that-fails-to-load-says-so.md`
- `hooks/dispatch.py`, whole
- `hooks/cmdline.py`: `program_is_data`, `shell_bodies`, `_heredoc_split`,
  `Unresolved`, `strip_subshell`, `_cd_target`, `_dedup`, `_directories`,
  `_step`, `_land`, `_enters`, `compose`, `walk_directories`, and the
  constants `SUBSHELL`, `EXPANDS`, `CD_FLAGS` and `WORD_BREAK`
- The diffs `d89f8392..fa556996` (hooks and tests), `1ea0b7c2~1..1ea0b7c2`,
  and `8571e683~1..02e47435` (hooks, tests, docs, the contract and
  `seal/ledger.md`)
- `tests/test_gate_judges_the_repo_it_commits_to.py`: the helpers and the
  phase-5 cases; `tests/conftest.py`: `decision_of`, `fired`,
  `declare_routing`; `bin/test`
- Issues #661, #662 and #665

The clone, the probe file and the scratch outputs were removed after the
round. Nothing was written in the orchestrator's tree except this report.

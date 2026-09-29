# Round 3 report — a gate that fails to load says so

Target: the fix diff `git diff 93d67a5b..7fc359c2`, branch HEAD `4f45313f`
(round 2's close, records only). Base the gate judged: `e8e5f977`. Reviewed in
a `git clone --no-local` of the orchestrator's worktree at `4f45313f`. Round
2's record was read for coordinates; its verdicts were re-derived, not carried.

This is the run's last round. Round 2 closed on a fix — the one reopening — so
the run ends here whatever this round finds, and anything still open takes the
filing ladder rather than another round.

## What this round was asked, and what it found

Round 2 recorded three closures — 🔴 1, 🟡 2, 🟡 3, all `fixed`. For each, the
documented shapes are closed. For two of them the class the finding named is
not: the fix closed the shapes round 2 measured and left a neighbour of each
that reads a real commit silent, the same failure the finding was opened for.

1. **The heredoc rule is defeated by a `#` glued to the delimiter word**
   (🔴 1 below). The fix reads the whole line and refuses anything after the
   interpreter, which closes round 2's four shapes. But it tokenises the line
   with `shlex`, whose default treats `#` as a comment, so `python3 <<EOF#x
   -c '…'` hands `program_is_data` only `python3 << EOF` — the interpreter's (NAME NOT IN TREE, reverted with #662 and #665)
   `-c` program is dropped as a comment. The shell keeps `EOF#x` as the
   delimiter and runs the `-c` program, so the body runs as shell and the
   commit inside it is not judged. Denied at `e8e5f977`, silent at HEAD.
2. **A `cd` with an assignment-shaped prefix is trusted although the shell
   never reaches the `cd`** (🔴 2 below). The fix trusts an existing `cd`
   target only when every earlier segment is a `cd` (`settled`). But
   `_cd_target` strips any leading `NAME=value` token as an assignment without
   checking that `NAME` is a valid identifier or that `value` has no command
   substitution. So `X=$(mv W M) cd W ; git commit` reads as a plain `cd W`
   with an all-`cd` prefix, is trusted not to fail, and the session directory
   is dropped — while the shell runs the `mv`, the `cd` then fails, and the
   commit runs in the session repository. `a.b=1 cd W ; git commit` reads the
   same way, though bash runs `a.b=1` as a command and never performs the
   `cd`. Denied at `e8e5f977`, silent at HEAD, and the commit really lands in
   the session repository (measured).
3. **The `systemMessage` and falsy-`hookSpecificOutput` sub-cases of 🟡 3 are
   closed.** A deny beside a non-text `systemMessage` now stays a deny, and a
   falsy `hookSpecificOutput` is read as absent. A third shape — a deny with a
   falsy non-text `permissionDecisionReason` — is still refused, but that is a
   conscious, test-pinned decision, it is unchanged from the round-2 target,
   and it degrades to an end-of-turn notice rather than losing enforcement. It
   is noted (⬜) below, not blocking.

The first two each leave a real commit unjudged, which is the direction the
prompt named as where a defect leaves the root.

## Round 2's closures, re-checked

### 🔴 1 — the documented shapes are closed, the class is not

Round 2's five shapes (`python3 <<'EOF' -c …`, the bundled `-Bc`, the `perl`
form, and the `$(…)`/`${…;…}` separator-moving forms) all deny at HEAD. The
planted case `test_a_body_read_to_the_end_of_its_command_is_still_shell` (NAME NOT IN TREE, reverted with #662 and #665)
passes. Confirmed 🟢 for those shapes.

The finding's own words are broader: "a program flag or script after the `<<`
… leaves a body that a shell runs." A `#` glued to the delimiter word is such
a flag, and it survives. See 🔴 1 in Findings.

### 🟡 2 — the documented shapes are closed, the class is not

Round 2's `mv W X ; cd W` and `chmod 000 W ; cd W` shapes, where the move is
in a separate earlier segment, deny at HEAD. The planted case
`test_a_cd_whose_target_an_earlier_segment_may_change_keeps_both` passes. (NAME NOT IN TREE, reverted with #662 and #665)
Confirmed 🟢 for those shapes.

The finding's words are "a `cd` whose target an earlier segment moves or locks
is trusted." A move folded into the same `cd` segment through an assignment
prefix's command substitution still fools the trust. See 🔴 2 in Findings.

### 🟡 3 — closed for what it named

`readable` now asks only the fields the path it takes reads. A deny beside a
non-text `systemMessage` stays a deny, and a falsy `hookSpecificOutput`
(`null`, `false`, `0`, `""`, `[]`) is read as absent again. The planted case
`test_a_deny_beside_a_message_that_is_not_text_still_denies` passes, and I
confirmed the merge on those shapes directly. Confirmed 🟢, with the ⬜ note
below.

## New units (the fix's surface)

`SEPARATORS`, `RUN_STDIN` and the four cases were read as code. (NAME NOT IN TREE, reverted with #662 and #665)
`SEPARATORS = ("&&", "||", ";", "|")` matches the tokens `shlex` with
`punctuation_chars=True` produces, and a background `&`, a `(` or `)` outside
that set leaves `head[0]` a non-interpreter word, so the body reads as shell —
the safe direction. The cases are correct as written and each was seen red at
its stated base. No defect in the new units themselves; the two 🔴 findings
are in the existing units the fix modified (`program_is_data`, `_cd_target`). (NAME NOT IN TREE, reverted with #662 and #665)

## Findings

### 🔴 1 — a `#` glued to the heredoc delimiter hides the interpreter's program flag

**Where.** `hooks/cmdline.py#program_is_data`, and the delimiter word read by
`hooks/cmdline.py#_heredoc_word`.

**What is wrong.** `program_is_data` tokenises the opener line with (NAME NOT IN TREE, reverted with #662 and #665)
`shlex.shlex(line, posix=False, punctuation_chars=True)`. `shlex` keeps its
default `commenters="#"`, so it discards everything from the first `#` to end
of line. `_heredoc_word` does not break the delimiter at `#`, so a delimiter
written `EOF#x` is the real delimiter and the shell keeps whatever follows it
as arguments to the interpreter. The two disagree: the shell runs the flags,
`program_is_data` never sees them. (NAME NOT IN TREE, reverted with #662 and #665)

For `python3 <<EOF#x -c '<program that runs its stdin as a shell>'`, `shlex`
yields `['python3', '<<', 'EOF']`, so `program_is_data` returns True and the (NAME NOT IN TREE, reverted with #662 and #665)
body is treated as data. The shell gives `python3` a `-c` program and feeds it
the body on stdin; the body's first line is `git commit -m x`.

| Command head (body: `git commit -m x`) | `e8e5f977` | HEAD `4f45313f` | real bash |
|---|---|---|---|
| `python3 <<EOF#x -c '<runs stdin as shell>'` | deny | silent | body ran as shell |
| `python3 <<'EOF'#x -c '<runs stdin as shell>'` | deny | silent | body ran as shell |
| `perl <<EOF#x -e '<runs stdin as shell>'` | deny | silent | body ran as shell |
| `python3 - <<EOF#x` (control, genuinely data) | deny | silent | body did not run |

The control is data at both, correctly. The other three are a shell-run commit
the gate denied before this branch and passes now.

**Why it matters.** #665's rule, the `program_is_data` docstring and ledger row (NAME NOT IN TREE, reverted with #662 and #665)
G7 all say an interpreter given a program flag reads as shell. The code does
not do it when the flag hides behind a `#` in the delimiter word, so a `git
commit` a shell really runs is a commit nobody judges. It was judged at
`e8e5f977`.

**Fix.** Disable the lexer's comment handling, so `#` is an ordinary character
and the flags after the delimiter survive into the token stream, where the
"nothing after the `<<` word" shape check refuses them. Verified at the
tokenizer level: with `commenters=""` the line above tokenises to
`['python3', '<<', 'EOF#x', '-c', "'…'"]`, `command[:-2]` is
`['python3', '<<', 'EOF#x']`, and `head[1:]` is not `[]` or `['-']`, so
`program_is_data` returns False. (Read-level: the whole-gate run was not (NAME NOT IN TREE, reverted with #662 and #665)
repeated against this fix, since the round's clone was removed.)

### 🔴 2 — a `cd` with an assignment-shaped prefix is trusted although the shell never reaches it

**Where.** `hooks/cmdline.py#_cd_target` (the assignment strip), and the
`settled`/`cannot_fail` trust in `hooks/cmdline.py#walk_directories`. (NAME NOT IN TREE, reverted with #662 and #665)

**What is wrong.** `_cd_target` strips a leading token as an assignment
whenever it contains `=` and does not start with `-`, without either check
bash makes: that the name is a valid identifier, and that the value's command
substitution runs before the command. So two shapes read as a bare `cd`:

- **A command substitution in the value has a side effect.**
  `X=$(mv W M) cd W ; git commit` is stripped to `cd W`. `settled` is True (no
  earlier segment), the target `W` exists when the hook reads the filesystem,
  so the `cd` "cannot fail" and the session directory is dropped. The shell
  runs `mv W M` while assigning `X`, the `cd W` then fails, and the commit
  runs in the session repository. This is round 2's 🟡 2 with the move folded
  into the same segment, so `settled` cannot see it.
- **An invalid identifier is not an assignment.** `a.b=1 cd W ; git commit` is
  stripped the same way, but bash runs `a.b=1` as a command (an invalid name
  is not an assignment), the `cd` is its argument and never runs, and the
  shell stays in the session repository.

| Command (`;`-joined, commit last) | `e8e5f977` | HEAD | bash: commit lands in |
|---|---|---|---|
| `X=$(mv W M) cd W ; git commit` | deny | silent | session (undeclared) |
| `a.b=1 cd W ; git commit` | deny | silent | session (undeclared) |
| `X=$(mv W M) cd H ; cd W ; git commit` | deny | silent | session (undeclared) |
| `cd W ; git commit` (control) | deny | silent | W (declared) |

The control lands in the declared target, so silent is correct there. The
first three land a commit in the session repository, which never opted the
branch in, and read silent.

**Why it matters.** The trust the branch added (#662) is that the filesystem
the hook reads is the one the `cd` meets. Contract §13 asks for that guarantee
to be removed and the code to still refuse. Here a side effect the same
segment runs removes it, and an invalid-identifier prefix means the `cd` the
reader trusted is not a `cd` at all. Each is a real commit the gate denied at
`e8e5f977` and passes now.

**Fix (class, §12).** Make the assignment strip match bash: refuse a prefix
whose name is not a valid identifier (the segment is then a command, not a
`cd`), and treat a prefix whose value carries a command substitution as making
the `cd` unknown. The parallel strip in `hooks/cmdline.py#understood` needs the
identifier check too, or a command such as `a.b=1 cd W` is still read as one
whose shell position is known. Read-level; not executed against a fix.

### ⬜ 3 — a deny with a falsy non-text reason is still dropped (safe, unchanged)

**Where.** `hooks/dispatch.py#readable`, the decision path.

**What.** A deny carrying `permissionDecisionReason` of `0`, `False`, `[]` or
`{}` is refused as unreadable, so `merge` drops it, whereas the pre-#661 code
(`1ea0b7c2~1`) forwarded it as a deny with an empty reason. A truthy non-text
reason (`7`) must stay refused — `merge`'s `"\n\n".join(... if r)` would raise
on it — but a falsy one is filtered out harmlessly, so refusing it is the same
over-refusal 🟡 3 named, on the reason field.

**Why it is not blocking.** It is unchanged from the round-2 target
`02e47435`, it is pinned by the fix's own test on purpose, and the drop
degrades to an end-of-turn notice (the gate is recorded as failed-while-running
and said at turn end), which is #661's designed fail-safe rather than a lost
enforcement. Noted so the 🟡 3 closure is not read as covering the reason
field. No fix commissioned.

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

## Paste-ready fixes

### 🔴 1

In `hooks/cmdline.py#program_is_data`, disable the lexer's comment handling:

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

Correct with it (§14): the `program_is_data` docstring says the line "holds (NAME NOT IN TREE, reverted with #662 and #665)
that one `<<` and no backslash" — add that a `#` in it is a literal, not a
comment.

### 🔴 2

In `hooks/cmdline.py#_cd_target`, validate the assignment prefix:

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

`hooks/cmdline.py#understood` has the same loose assignment strip
(`while toks and "=" in toks[0] and not toks[0].startswith("-")`); give it the
`name.isidentifier()` check too, or `a.b=1 cd W` is still read as a segment
whose shell position is known (§12, the class).

Correct with it: `docs/commit-review-gate-spec.md`'s #662 paragraph and ledger
row G8 — the trust also requires the `cd` segment to carry no side-effecting
assignment prefix.

Needs a fix: yes — 🔴 1 (a `#` glued to the heredoc delimiter hides the interpreter's program flag, so a shell-run commit reads as data) and 🔴 2 (a `cd` with an assignment-shaped prefix is trusted, so a `$(…)` side effect or an invalid-identifier prefix hides a commit in the session repository)

Loses a record or crashes: yes — 🔴 1 and 🔴 2 each read a real commit silent that the gate denied at `e8e5f977`

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🔴 1 — `#`-delimiter heredoc reads a shell-run body as data | fix on the branch before the PR merges; the run is capped at one reopening, so no round commissions it | the owner (a false silent on the commit gate is branch-caused; the ladder's default is not a new issue) |
| 🔴 2 — a `cd` with an assignment-shaped prefix is trusted | fix on the branch before the PR merges; the run is capped | the owner |

## Proof

Files opened this round, in the clone at `4f45313f` unless noted:

- `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/rounds/round-2.md`,
  `rounds/round-2-report.md` (the orchestrator's tree)
- The fix diff `93d67a5b..7fc359c2` (hooks and tests), and the eight commit
  subjects on it
- `hooks/cmdline.py`: `program_is_data`, `shell_bodies`, `_heredoc_split`, (NAME NOT IN TREE, reverted with #662 and #665)
  `_heredoc_word`, `drop_heredoc_bodies`, `heredoc_bodies`, `_cd_target`,
  `_dedup`, `_directories`, `_step`, `_land`, `_enters`, `compose`, (NAME NOT IN TREE, reverted with #662 and #665)
  `walk_directories`, `understood`, and the constants `DATA_INTERPRETERS`, (NAME NOT IN TREE, reverted with #662 and #665)
  `SEPARATORS`, `WORD_BREAK`, `EXPANDS`, `CD_FLAGS`
- `hooks/dispatch.py`: `readable`, `classify`, `merge`
- `hooks/commit-review-gate.py`: `_hides_a_commit` and the `shell_bodies` call (NAME NOT IN TREE, reverted with #662 and #665)
  sites
- The base modules at `e8e5f977` (`cmdline.py`, `commit-review-gate.py`) and
  `1ea0b7c2~1` (`dispatch.py`)
- `tests/test_gate_judges_the_repo_it_commits_to.py`: the helpers and the new
  and changed cases; `tests/test_a_gate_that_fails_says_so.py`: the changed
  and new dispatch cases; `tests/conftest.py`: `run_hook`, `decision_of`,
  `fired`, `declare_routing`, `load_hook_module`, `MODE_ROW`; `bin/test`

The clone, the probe files and the scratch outputs were removed after the
round. Nothing was written in the orchestrator's tree except this report.

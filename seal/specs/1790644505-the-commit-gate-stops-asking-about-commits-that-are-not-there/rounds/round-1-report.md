# Round 1 report — the commit gate stops asking about commits that are not there

Target: branch `fix/662-665-the-commit-gate-stops-asking-about-commits-that-are-not-there`
at `f25c6b1a`, against base `3911a8cf` (`git diff 3911a8cf...f25c6b1a`).
Reviewed in a `git clone --no-local` of the orchestrator's worktree at
`f25c6b1a`, beside a second clone at `3911a8cf` for differential probes. There
are no earlier rounds. Work item `1790635415`'s round 2 and round 3 reports
were read from commits `93d67a5b` and `3fb828fb` for their shapes.

## What this round found

The automation half does what it says: under the press every stop is a deny,
no stop moved, and a press that cannot be read is no press. The defects are in
phases 4 and 5, the two changes to what the gate reads.

```
new readers find more commits (#669, #670)
  ├─ 🔴 1  a found commit in a declared repository displaces the base's
  │        fallback for a command the splitter could not finish → false silent
  ├─ 🟡 2  the substitution reader recurses without a bound → crash → silence
  ├─ 🟡 3  the shell-string reader asks "does this expand?" of words no shell
  │        runs → new stops on commands that commit nothing
  └─ 🟡 4  the class stops short of `eval` behind the same words
the press, read by the guard's reader
  └─ 🟡 5  a later answer to the routing question does not take the press back
```

🔴 1 is the one that leaves the root: six command shapes the base stopped read
silent at the head, and a real bash commits in the unjudged repository for each
of the two it was given. The smith's account says this cannot happen; the account and
the code are compared under *What the account claimed*.

## Findings

### 🔴 1 — A commit found in a declared repository silences the session's own directory

`hooks/commit-review-gate.py:1174` (with `commit_targets` at `:379`).

When the splitter cannot finish a command (`split_segments_with_separators`
returns `clean=False`), the base had one fallback: if no invocation was found,
it judged the session's own directory, because the unread rest may commit
there. That fallback only runs while `invocations` is empty. At `3911a8cf` the
reader found nothing in a segment like `nice git -C W commit`, so the fallback
ran. At the head it finds an invocation in W. When W is declared, W is judged
silent, the fallback never runs, and the commit in the unread rest goes
unjudged.

The splitter stops early on a string bash parses and `shlex` does not. An
ANSI-C string with an escaped quote, `$'it\'s'`, is one.

Executed, base against head, the session directory opted in and undeclared,
W declared:

| Command (W and the session are temporary repositories) | Base | Head |
|---|---|---|
| `nice git -C W commit -m x; echo $'it\'s'; git commit -m y` | deny | silent |
| `for d in a; do git -C W commit -m x; done; echo $'it\'s'; git commit -m y` | deny | silent |
| `cd W && nice git commit -m x; echo $'it\'s'; git commit -m y` | deny | silent |
| `timeout 5 git -C W commit -m x; echo $'it\'s'; git commit -m y` | deny | silent |

The parity arm loses the same way. In a repository with a migration config, a
command carrying `[no-review]` whose new invocation is unresolved goes to the
unreadable branch, which `[no-review]` waives whole, and the fallback that
would have run the parity arm never runs:

| Command (session repository has `seal/parity.md` and staged code) | Base | Head |
|---|---|---|
| `: '[no-review]'; echo $(git commit -m y) $'it\'s'` | deny | silent |
| `: '[no-review]'; sh -c 'git commit -m y'; echo $'it\'s'` | deny | silent |

Through `hooks/dispatch.py pre-bash` with a `Mode` row present, so no other
gate speaks, the first row is `deny` at the base and silent at the head. In
bash 3.2.57, the first row committed in both the session repository and W, and
the fifth committed in the parity repository.

Why it matters: this is the first of the three places the prompt named. A
commit lands in a repository nothing judged, and the command reads as one the
gate checked.

The class is older than the branch. At the base, `git -C W commit -m x; echo
$'it\'s'; git commit -m y` is already silent, because the base found the W
invocation too. Phases 4 and 5 widen it to every shape they newly read. The
fix below closes the older part as well. It only adds stops: the fallback now
stands beside what was found instead of only in its absence.

### 🟡 2 — Deeply nested substitutions crash the gate, and a crashed gate is silence

`hooks/commit-review-gate.py:177`.

`_hides_a_commit` recurses once per nested `$( … )`, with no bound. Executed:
`git commit -m x; echo` followed by 500 nested `$(` crashes the head gate with
`RecursionError` (496 frames at `:177`). Through `hooks/dispatch.py` the result
is silent, while the base denies the same command. At 450 levels both deny.

No command anyone types nests 500 deep, so this ships as a way past the gate
rather than a hole a person falls into. The model is the one that would use it.
The fix reads a command nested past the recursion limit the way the gate
already reads one it cannot tokenise: a stop wherever it mentions a commit.

### 🟡 3 — A shell's positional arguments, and the word `watch` anywhere, stop commands that commit nothing

`hooks/commit-review-gate.py:191`, `hooks/cmdline.py:1435` and `:1437`.

`reparsed_texts` returns every non-option word after a shell host that was
given `-c`, and every non-option word after a `watch` token anywhere in the
segment. `_string_hides_a_commit` then asks `names_an_unknown_command` of each
one. That question is right for the string the shell runs. It is wrong for
positional parameters, which no shell runs, and for `watch` as a search word.

Executed at the head, from a declared repository, in an attended session. Each
is silent at the base and `deny` at the head, then `ask` on the next attempt.
Under the press it is a `deny` every time, and the text tells the model the
command is a commit:

- `find . -name '*.py' -exec sh -c 'wc -l "$1"' _ {} \;`
- `find . -type f -exec bash -c 'echo "$@"' bash {} +`
- `bash -c 'for f in "$@"; do echo "$f"; done' _ *.txt`
- `bash -c 'echo "$0"' "$HOME"`
- `grep -n watch *.py`, `grep -l watch $(git ls-files)`, `rg watch "$DIR"`

A declaration does not silence these, because an unresolved target is judged
before any declaration is read. The phase 5 record states the trade: "an extra
word costs a stop where a missed string costs a silence." The record does not
say that the trade covers `find -exec sh -c … {}`, a common idiom. That is
the third place the prompt named: a stricter reading applied where no commit
runs.

The fix below asks the expansion question only of the string each host runs,
and reads `watch` only where it is the program. The commit question is still
asked of every word, so no commit shape is lost. Executed with the fix:
`sh -c "$CMD"`, `bash -o errexit -c "$CMD"`, `su -c "$CMD" root`,
`su root -c "$CMD"`, `watch -n 1 "$CMD"`, `env -S "$CMD"`, `sudo sh -c "$CMD"`,
`bash -lc "$CMD"` and `bash -c '"$@"' _ git commit -m x` all still deny. The
seven shapes above are silent, and the 1067 cases in the modules that load the
gate or the reader pass.

### 🟡 4 — An `eval` behind a reserved word, a prefix or a subshell is still no commit

`hooks/commit-review-gate.py:194`–`213`.

Phase 4 taught `parse_git` to read past `do`, `then`, `!` and `{`. Phase 5
taught it to read past the runners, and taught the gate to read `sh -c`
wherever it sits in the segment. `_eval_argument` was left on its old rule:
assignments only, and `None` for anything that opens a subshell. Executed,
silent at both base and head:

- `if true; then eval 'git commit -m x'; fi`
- `for c in a; do eval "$c"; done`, the measured loop's shape with an `eval`
- `while eval 'git commit -m x'; do break; done`
- `! eval …`, `time eval …`, `command eval …`, `builtin eval …`
- `(eval 'git commit -m x')`, `{ eval 'git commit -m x'; }`

In bash each of these runs its `eval`. This is not a regression, since the base
is silent too. It is the same class this branch fixed for `git` and `sh -c`,
one reader over, and contract §12 asks for the class. The fix reuses
`command_word`. Executed with it: all ten deny, `X=1 eval …` and a bare `eval`
still deny, and the 1067 cases pass. `sudo -u root eval …` stays silent:
`sudo` cannot run a shell builtin, and no `eval` binary exists on this
machine.

### 🟡 5 — An earlier `automation` press outlives a later answer to the routing question

`hooks/worktree_consent.py:324`–`331`, read at `hooks/commit-review-gate.py:1240`.

`automation_answered` returns `True` at the first pressed preset in the
transcript and reads no further. In a session that pressed `automation` for
one work item and later answered `per axis` for another, the press still
reads as given. Executed with a transcript holding both answers, in that order:
`automation_answered` is `True`, and the gate denies twice with the automation
text.

That text tells the model "none is to be put to them in its place: the run was
promised that nothing would stop to ask". It says this to a model whose person,
on the latest answer, said the run may stop to ask. That is the second place
the prompt named: a deny where a person should have been asked. The frame's
property 3 accepts a misread press as costing turns. It does not cover the text
telling the model not to ask a person who is present.

The reader is the guard's, and the branch reads it unchanged. The fix
therefore changes the guard too, in the direction of asking: a later answer
takes back creation consent. The lines below make the last answer from this
clone the one that stands. With them the probe reads `False`, the gate goes
back to deny-then-ask, and the 1071 cases in the modules that load the
reader, the gate or the guard pass (1 skipped).

## What the account claimed, and what the code does

- **Claimed** in `phases/phase-5.md` §*Why no shape the base judges becomes
  silent*, item 2: "The directories of existing invocations are not touched,
  and the only directories added are `Unresolved`, which is a stop wherever
  the session opted in." **The code** adds resolved invocations: `nice git -C
  W` and `do git -C W` compose an absolute `-C` onto the walk's base, at
  `commit_targets` `:383`. It also takes away the fallback at `:1174`, and
  an unresolved target is not a stop when `[no-review]` is present, at
  `:1250`. See 🔴 1.
- **Claimed** in `docs/commit-review-gate-spec.md:314`–`317`: "every string and
  substitution newly read adds an invocation beside the ones already found",
  so the reading "can only have gained stops". The same three coordinates
  contradict it. The sentence is corrected in 🔴 1's fix (§14).
- **Claimed** in `docs/commit-review-gate-spec.md:281`–`285` for #669: "Every
  segment the new reading reaches began with a word at which the old one found
  no command." **Confirmed by reading** `command_word` against the base loop in
  `parse_git`. `RUNNERS` contains `WRAPPERS`, and the jump runs only when the
  word reached is not `git`. The walk's new `Unresolved` marking applies only
  to segments where the base's `parse_git` returned `None`. The claim is true
  of the segment. The fallback it displaces is not a segment, which is why the
  claim held and 🔴 1 still happened.
- **Claimed** in `spec.md` property 1 and S7 (a), as corrected: `commit_targets`,
  `judge` and `names_a_directory` are untouched. **Confirmed** from the diff.
- **Claimed** in `overview.md` *Not done*: `bash run.sh`, `source`, `make`,
  `uv run`, `npx`, `pnpm exec`, `ssh` and `docker exec` stay silent as at the
  base. Not re-executed. The reasons are stated, and none is a regression.

## Confirmations

- The S7 corpus, the automation cases, and the #669 and #670 cases pass at
  `f25c6b1a`: 251 cases in five modules, executed.
- Under the press both decision sites deny, the reason carries no
  `AskUserQuestion`, and `automation_pressed` returns `False` for no session,
  no reader, and a raising reader. Read at `:750`–`:773` and `:1240`–`:1284`.
  Exercised by the probe for 🟡 5.
- Work item `1790635415`'s five false-silent shapes are rows of
  `tests/test_no_shape_the_base_stops_reads_silent.py#corpus`, and they pass.
  Executed as part of the 251.

## Regression tests to plant

- `tests/test_no_shape_the_base_stops_reads_silent.py`: the four 🔴 1 rows and
  the 500-level nesting row, added to `corpus`. Also a parity-arm case for the
  two `[no-review]` rows. The fence is under 🔴 1. Seen red at `f25c6b1a`:
  the corpus case with `RecursionError` and the parity case with `['silent',
  'silent']`. With only 🟡 2's guard applied, the four rows fail by name,
  pressed and plain. With both fixes, 3 passed.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`:
  the seven 🟡 3 commands as controls that stay silent, beside the nine
  shapes listed under 🟡 3 that must still deny.
- `tests/test_a_commit_behind_a_reserved_word_is_judged.py`: the ten 🟡 4
  `eval` shapes.
- `tests/test_an_automation_run_meets_no_commit_prompt.py`: an `automation`
  answer followed by a `per axis` answer from the same clone answers as no
  press (🟡 5).

## Facts for the evidence ledger

- The unparseable-command fallback in `hooks/commit-review-gate.py#main`
  judges the session's own directory, and at `f25c6b1a` it runs only while no
  invocation was found. Anchor the corrected rule after the fix.
- `hooks/worktree_consent.py#automation_answered` returns on the first pressed
  preset from this clone, and no later routing answer is read. This stays true
  until 🟡 5 is fixed or answered.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A commit the new reading finds in a declared repository displaces the fallback for a command the splitter could not finish, so a commit in the session's own directory, or a parity arm, goes unjudged | `hooks/commit-review-gate.py:1174` | open | Executed: four review-arm and two parity-arm shapes deny at `3911a8cf` and are silent at `f25c6b1a`; bash commits in the unjudged repository |
| 🟡 2 | `_hides_a_commit` recurses without a bound, so 500 nested substitutions raise and the dispatcher turns the raise into silence | `hooks/commit-review-gate.py:177` | open | Executed: `RecursionError` at 500 levels, silent through `hooks/dispatch.py`, deny at the base |
| 🟡 3 | The expansion check runs on a shell's positional arguments and on `watch` anywhere in a segment, so commands that commit nothing stop, even in a declared repository | `hooks/commit-review-gate.py:191` | open | Executed: seven non-commit commands silent at the base and deny at the head |
| 🟡 4 | `_eval_argument` does not read past a reserved word, a prefix or a subshell, so the class #669 and #670 fixed for `git` and `sh -c` stays open for `eval` | `hooks/commit-review-gate.py:194` | open | Executed: ten shapes silent at base and head; bash runs each `eval` |
| 🟡 5 | An `automation` press stands after a later `per axis` answer in the same session, and the gate then tells the model not to ask a person who is present | `hooks/worktree_consent.py:330` | open | Executed: a transcript with both answers reads as pressed, and the gate denies twice with the automation text |
| 🟢 | The automation decision: deny at both sites under the press, no question tool named, every unreadable press is no press | `hooks/commit-review-gate.py:1240` | confirmed | Read, and exercised by the 251 cases and the 🟡 5 probe |
| 🟢 | Work item `1790635415`'s false-silent shapes still stop, with and without the press | `tests/test_no_shape_the_base_stops_reads_silent.py` | confirmed | Executed at `f25c6b1a` |
| ❓ | The cases on Windows | CI's `windows-latest` leg | ❓ out of verified scope | Not run here; CI answers it at the pull request |

## Executed probes

| What was run | Result |
|---|---|
| Differential, base `3911a8cf` against head `f25c6b1a`, each gate run as a subprocess with a fresh session id: 32 commands (unclean fallback, class controls, non-commit commands) | 6 regressions (🔴 1); 7 new stops on non-commit commands (🟡 3); `eval` shapes silent at both (🟡 4) |
| The first 🔴 1 row and the first parity row, run in bash 3.2.57 in temporary repositories | The review-arm row committed in the session repository and in W; the parity row committed in the parity repository |
| Through `hooks/dispatch.py pre-bash`, with a `Mode` row so that `hooks/mode-gate.py` stays quiet | The first 🔴 1 row: base deny, head silent. 500 nested substitutions: base deny, head silent. 450 nested: deny at both |
| Nesting depth for `_hides_a_commit` | Crashes from 500 levels as a subprocess; depth-40 `sh -c "$( … )"` chains run in under 2 s |
| A transcript with an `automation` answer, then a `per axis` answer, through `automation_answered` and the gate | `True`; deny, deny |
| `bin/test` on the five new modules at `f25c6b1a` | 251 passed |
| 🔴 1 and 🟡 2 trial fix, then `bin/test` on every module that loads the commit gate (20) | 812 passed |
| 🟡 3 trial fix, then the controls, the seven non-commit shapes, and `bin/test` on every module loading the gate or `hooks/cmdline.py` | the ten controls (eight `"$CMD"` shapes, two with a commit in the string) still deny, the seven shapes are silent, 1067 passed |
| 🟡 4 trial fix, then the ten shapes and the same modules | all ten deny, 1067 passed |
| 🟡 5 trial fix, then the probe and every module loading the reader, the gate or the guard | `False`, then deny and ask; 1071 passed, 1 skipped |
| The planted 🔴 1 and 🟡 2 rows at `f25c6b1a`, with 🟡 2's guard alone, and with both fixes | red (`RecursionError`; parity `['silent', 'silent']`); the four rows red by name; 3 passed |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — the sealer's, once, after the rounds settle; not this round's |

## Paste-ready fixes

### 🔴 1

In `hooks/commit-review-gate.py#main`, replacing the two lines after
`cwd = payload.get("cwd", "")`:

```python
    invocations, clean = commit_invocations(command, cwd)
    # A command the splitter could not finish may commit in the part it did
    # not read, and the base judged the session's own directory for that
    # whenever nothing was found. A commit found in the part it DID read --
    # which #669 and #670 made more common -- used to take that judgment
    # away, so a declared repository named there silenced the session's own
    # directory (round 1 of 1790644505). The fallback now stands beside what
    # was found, which only adds a target.
    unparsed = not clean and "git" in command and "commit" in command
    if not invocations and not unparsed:
        return
    if unparsed:
        invocations = invocations + [Invocation((), ())]
```

In `docs/commit-review-gate-spec.md`, the sentence at `:314`–`:317`, and
`phases/phase-5.md` item 2 with a dated correction:

```markdown
The reading can only have gained stops by this, for the reason #669's change
gives, and for one more: a command the splitter could not finish is still
judged in the session's own directory when the new reading found a commit in
the part it did read. Without that, a commit found in a declared repository
took the session's directory out of the judgment (round 1 of 1790644505).
```

The planted rows, at the end of `corpus` in
`tests/test_no_shape_the_base_stops_reads_silent.py`, and a case beside it:

```python
        # Round 1 of 1790644505: a commit the #669/#670 reading finds in `w`,
        # then a string the splitter cannot close, then a commit where the
        # shell is. The base judged the session's directory for the unread
        # rest; a commit found in `w` used to take that judgment away.
        ("r1: nice -C w, then $'…'", f"nice git -C {q(w)} commit -m x; echo $'it\\'s'; {BODY}"),
        (
            "r1: do -C w, then $'…'",
            f"for d in a; do git -C {q(w)} commit -m x; done; echo $'it\\'s'; {BODY}",
        ),
        ("r1: cd w && nice, then $'…'", f"cd {q(w)} && nice {BODY}; echo $'it\\'s'; {BODY}"),
        (
            "r1: timeout -C w, then $'…'",
            f"timeout 5 git -C {q(w)} commit -m x; echo $'it\\'s'; {BODY}",
        ),
        # Nested past the reader's recursion: a gate that raises is silence.
        ("r1: 500 nested substitutions", f"{BODY}; echo " + "$(" * 500 + "true" + ")" * 500),
    ]


def test_a_parity_arm_is_not_waived_by_a_newly_read_commit(
    monkeypatch, capsys, projects, tmp_path
):
    """Round 1 of 1790644505. `[no-review]` waives an unresolved target whole,
    and the base's fallback for a command the splitter could not finish still
    judged the session's own directory, whose parity arm `[no-review]` does
    not answer."""
    session = make_repo(tmp_path / "session", declared=True)
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    for command in (
        f": '[no-review]'; echo $({BODY}) $'it\\'s'",
        f": '[no-review]'; sh -c '{BODY}'; echo $'it\\'s'",
    ):
        answers = with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        )
        for which, got in answers.items():
            assert "silent" not in got, (command, which, got)
```

### 🟡 2

In the same place, around the call. Together with 🔴 1 the first lines read:

```python
    try:
        invocations, clean = commit_invocations(command, cwd)
    except RecursionError:
        # Nested deeper than the reader recurses (`$(` five hundred deep).
        # Read as a command that could not be parsed, which stops wherever it
        # mentions a commit; raising would reach `dispatch.py` as silence.
        invocations, clean = [], False
    unparsed = not clean and "git" in command and "commit" in command
```

### 🟡 3

In `hooks/cmdline.py`, after `reparsed_texts`:

```python
# Options of a shell, and of `watch`, that take the next word as their value.
VALUED = {"-o", "+o", "-O", "+O", "-n", "--interval", "-q", "--equexit"}


def command_strings(tokens):
    """The string each host in this segment runs AS its command.

    `reparsed_texts` returns every word that might be it, which is right for
    asking whether a commit is written there. It is wrong for asking whether a
    command word expands: `find . -exec sh -c '…' _ {} \\;` hands `_` and `{}`
    to the string as positional parameters, which no shell runs, and
    `grep watch *.py` names no program at all. So `names_an_unknown_command`
    is asked of this narrower list.
    """
    out = []
    for k, tok in enumerate(tokens):
        word = os.path.basename(tok)
        rest = tokens[k + 1 :]
        if word in SHELLS and any(_hands_a_string(word, t) for t in rest):
            skip = False
            for t in rest:
                if skip:
                    skip = False
                elif t in VALUED:
                    skip = True
                elif t != "--" and not t.startswith(("-", "+")):
                    out.append(t)
                    break
        elif word in STRING_HOSTS:
            for j, t in enumerate(rest):
                if t.startswith("--command="):
                    out.append(t.split("=", 1)[1])
                elif _hands_a_string(word, t) and j + 1 < len(rest):
                    out.append(rest[j + 1])
        elif word in ("env", "genv"):
            out += reparsed_texts([tok, *rest])
        elif word == "watch" and all(
            ("=" in t and not t.startswith("-")) or os.path.basename(t) in RUNNERS
            for t in tokens[:k]
        ):
            # Only where `watch` is the program that runs, not a word
            # something else was handed (`grep watch *.py`).
            words, skip = [], False
            for t in rest:
                if skip:
                    skip = False
                elif t in VALUED:
                    skip = True
                elif not t.startswith("-"):
                    words.append(t)
            out.append(" ".join(words))
    return out
```

In `hooks/commit-review-gate.py`, import the new helper from `cmdline`,
make both call sites (`:175` and `:323`) read `if _string_hides_a_commit(toks):`,
and give the helper the segment:

```python
def _string_hides_a_commit(toks):
    """True when a string a program in TOKS hands to a shell might commit (#670).

    Every word that might be the string is read as commands, the way
    `_hides_a_commit` reads a heredoc body. Only the string a host actually
    runs is asked whether its command word expands (`sh -c "$CMD"`): a
    positional parameter or a search word is not a command (round 1 of
    1790644505).
    """
    return any(_hides_a_commit(t) for t in reparsed_texts(toks)) or any(
        names_an_unknown_command(t) for t in command_strings(toks)
    )
```

### 🟡 4

In `hooks/commit-review-gate.py#_eval_argument`, import `command_word` from
`cmdline` and replace the body after the docstring. `strip_subshell` then has
no other user in the gate and leaves the import list:

```python
    # The word that runs, read the way `parse_git` reads it since #669 and
    # #670: past assignments, `!`, a subshell or brace opener, a reserved word
    # that begins a list, and the enumerated runners. `builtin` runs a
    # builtin, and `eval` is one.
    word, _unplaced = command_word(list(toks))
    while word and os.path.basename(word[0]) == "builtin":
        word = word[1:]
    if not word or word[0] != "eval":
        return None
    return " ".join(word[1:])
```

### 🟡 5

In `hooks/worktree_consent.py`, after `_routing_preset`:

```python
def _routing_answer(result):
    """True for the preset, False for any other answer to the routing
    question, None when RESULT answers no routing question at all."""
    if _routing_preset(result):
        return True
    if not isinstance(result, dict) or not isinstance(result.get("questions"), list):
        return None
    for q in result["questions"]:
        options = q.get("options") if isinstance(q, dict) else None
        if isinstance(options, list) and sorted(
            leading_phrase(o.get("label") if isinstance(o, dict) else None)
            for o in options
        ) == sorted(ROUTING_LABELS):
            return False
    return None
```

In `automation_answered`, add `pressed = False` beside `clones = {}`, and
replace from the `linked` test to the end of the function:

```python
                if not linked:
                    continue
                answered = _routing_answer(entry.get("toolUseResult"))
                if answered is None:
                    continue
                cwd = entry.get("cwd")
                key = cwd if isinstance(cwd, str) else ""
                if key not in clones:
                    clones[key] = _clone_of(key) if key else ""
                if clones[key] == want:
                    # The LAST answer from this clone stands: a later work
                    # item's `per axis` takes back the earlier press.
                    pressed = answered
    except (OSError, ValueError):
        return False
    return pressed
```

`docs/worktree-guard-spec.md` §*Creation consent* and the commit gate's
paragraph on the press then say that the latest answer from the clone is the
one read.

Needs a fix: yes — 🔴 1 (a commit found in a declared repository displaces the fallback, and six shapes the base stopped read silent); 🟡 2 to 🟡 5 are each fix or justify

Loses a record or crashes: yes — 🔴 1 reads real commits silent that `3911a8cf` stopped, and bash lands them; 🟡 2 crashes the gate at 500 nested substitutions, which the dispatcher turns into silence

## Proof

Files opened this round, in the clone at `f25c6b1a` unless noted:

- `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/overview.md`,
  `spec.md`, `phases/phase-5.md`
- `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/rounds/round-2-report.md`
  at `93d67a5b` and `round-3-report.md` at `3fb828fb`, in the orchestrator's
  repository
- The diff `3911a8cf...f25c6b1a` for `hooks/`, and its added lines in
  `docs/commit-review-gate-spec.md`, `skills/agent-contract/SKILL.md` and
  `skills/implement/orchestration.md`
- `hooks/commit-review-gate.py`: lines 100–1294, which cover
  `_hides_a_commit`, `_string_hides_a_commit`, `_eval_argument`,
  `commit_invocations`, `commit_targets`, `judge`, the reason builders,
  `automation_pressed`, `unreadable_reason` and `main`
- `hooks/cmdline.py`: `WRAPPERS`, `_closes`, `_heredoc_word`,
  `split_segments`, `split_segments_with_separators`, `understood`,
  `Unresolved`, `strip_subshell`, `_cd_target`, `walk_directories` (its loop
  head), and the new `command_word`, `reparsed_texts`,
  `names_an_unknown_command`, `_paren_end` and `substitution_bodies`
- `hooks/worktree_consent.py`: `_routing_preset`, `automation_answered`
- `hooks/optin.py`: `opted_in`, `parity_config`; `hooks/dispatch.py`:
  `GROUPS`, `RANK`, `run_gate`; `hooks/mode-gate.py` docstring; `hooks/hooks.json`
- `tests/test_no_shape_the_base_stops_reads_silent.py`; `tests/conftest.py`:
  `run_hook`, `load_hook_module`, `declare_routing`;
  `tests/test_the_guard_asks_once_per_session.py`: `ask_entries`,
  `write_transcript`; `tests/test_no_real_identifiers.py` patterns; `bin/test`

The two clones, the probe scripts, the trial fixes and the scratch outputs were
removed after the round. Nothing was written in the orchestrator's tree except
this report.

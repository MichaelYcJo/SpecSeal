# 1790644505 — review round 3 report

Round 3, verifying, the run's last. Target: round 2's fix diff
`ed1c0132..195d8176`, read at HEAD `784d1547` (whose own commit touches
`round-2.md` only). Reviewed in a `git clone --no-local` of the branch, by
specseal:warden on claude-opus-5-5.

## What this round found, in one view

```
round 2's five verdicts ........ all five hold (red 1, yellows 2 and 3, yellow 4, white 5)
the smith's two narrowings ..... both sound
the fixes' new units ........... _is_the_program and the shell-string loop still miss
                                 the rest of yellow 2's class → yellow 1, yellow 2 below
                                 (the base is silent on every one of them)
_hides_a_commit ................ answers correctly, but only after ~330 rescans → white 3
```

No command shape reads silent at `784d1547` where `3911a8cf` judged it. Every
shape below that is silent at HEAD is silent at the base too. So nothing here
loses a record the base kept. Two findings still leave the branch's own
promise (`sh -c "$CMD"` stops) false for shapes that round 2's class covers.

## Round 2's verdicts, each checked

**Red 1 holds.** Round 2's three nesting rows deny at HEAD. I widened them to
nine nesting kinds (`$(`, `$( ` spaced, `<(`, `"$(`, `${x:-`, `$((`, a bare
subshell, backquotes inside `$(`, and nested `bash -c`), each at depth 300,
500, 1000 and 3000, beside a commit into another repository. Every row denies
at `3911a8cf` and at `784d1547`. At `567069b6`, seven kinds read silent from
depth 500. Reverting the `except RecursionError` in `_hides_a_commit` turns
the planted case red by name.

**Yellow 2 holds for its rows, and the narrowing is sound.** The report's fence
asked every word before `-c`; the smith asks none. A word before the flag is an
option's value (`--rcfile f`), a redirection, or a script operand (`bash "$S"
-c x` runs the file `$S` with `-c` as its argument). None of them is a string
a shell runs as a command. `bash -i --rcfile "$F" -c true` sources a file, which
the spec already leaves unread with `bash run.sh`. Both rows deny at
`567069b6`, are silent at HEAD, and are silent at the base. The planted rows go
red when the loop reads `rest` again, and when `_is_the_program` loses `!`, a
list opener, `(`, or its early return on a runner.

**Yellow 3 holds, and keeping the runner trigger on `git` is sound.** With
stand-in `eval`, `!= "git"` and `!= stand_in` differ in one case only: the word
after a runner is literally `git` or `eval`. A runner executes a program, and
`eval` is a builtin, so no runner runs `eval` either way. The one visible
difference is in the stopping direction: `sudo -u git eval "$X"` is silent at
`567069b6` and denies at HEAD. `nice eval`, `command eval` and `time eval`
deny at HEAD and are silent at the base. Reverting the `"eval"` argument turns
the four new `EVALS` rows red.

**Yellow 4's doc now says what the code does.** `consent` in
`hooks/worktree_consent.py:373` returns `"record"` from `granted` before it
reads any answer. The spec (`docs/worktree-guard-spec.md:171`) and the case
docstring say the same thing: a later `per axis` takes back the gate's deny,
and a record already written stands.

**White 5 holds.** The changelog fragment and rows E1, E14, E15, E18 and E20
state the corrected claims, and `bin/evidence-check` exits 0 with nothing
drifted or broken.

## Yellow 1 — `watch` is not read as the program behind a redirection or in a case arm, a function body or a coprocess

`_is_the_program` (`hooks/cmdline.py:1457`) returns False when anything other
than an assignment, a list opener, `!`, `(` or a runner stands before `watch`.
A redirection (`2>/dev/null watch …`), a `case` pattern, a function definition
(`f()`, `f ()`, `function f`) and `coproc` are all read as "some other program
came first". The string `watch` hands to `sh -c` is then never asked whether
its command word expands.

This matters because it is the same class round 2's yellow 2 named ("misses
`watch` behind a runner's options or a list opener"). The fix enumerated the
three placements the report listed and not the class. Command word reading
already has a rule for these constructs: `command_word` makes the first `git`
the stand-in inside `UNPLACED`, a pattern or a definition. `_is_the_program`
has no such rule.

Six shapes deny at `3006eb85`, read silent at `567069b6` and at HEAD, and are
silent at the base: `2>/dev/null watch -g "$CMD"`, `case a in a) watch -g
"$CMD";; esac`, `f() { watch -g "$CMD"; }; f`, `f () { … }`, `function f {
watch -g "$CMD"; }; f`, and `coproc watch -g "$CMD"`. `watch` is not installed
here, so bash did not run these.

## Yellow 2 — a redirection written after `-c` is taken for the string

The shell branch of `command_strings` (`hooks/cmdline.py:1498`) takes the first
non-option word after the flag as the string. A redirection after the flag is
such a word. So `bash -c 2>/dev/null "$CMD"` asks `2>/dev/null` whether it
expands, and never asks `"$CMD"`. The `watch` branch
(`hooks/cmdline.py:1525`) joins its words with the redirection still first,
so `watch -g 2>/dev/null "$CMD"` asks `2>/dev/null` as the command word.

Round 2's fix moved the reading past the flag, which covers a redirection
before it (`bash 2>/dev/null -c`). The mirror placement was not enumerated.
The spec's sentence at `docs/commit-review-gate-spec.md:307` (*a command word
the shell would expand in the string a host runs (`sh -c "$CMD"`) counts as one
that might commit*) is false for these shapes.

Executed: `bash -c 2>/dev/null "$CMD"`, `bash -c 2> /dev/null "$CMD"`, `bash
-c >/dev/null "$CMD"`, `bash -lc </dev/null "$CMD"` and `watch -g 2>/dev/null
"$CMD"` each deny at `3006eb85` and are silent at `567069b6`, at HEAD and at
the base. In bash 3.2.57 with `CMD` set to a commit, each of the four `bash`
shapes landed a commit.

`sh -c 2>&1 "$CMD"` is a different defect and is not in this finding. The
splitter reads the `&` in `2>&1` as a separator (`[['sh', '-c', '2>'], ['1',
'$CMD']]`), and the row is silent at all four SHAs, `3006eb85` included. It
is in Deferred below.

## Both fixes, tried together

I applied the fixes below in the clone. All eleven shapes are asked and read
as expanding, and five controls stay unasked: `grep -n watch *.py`, `find
-exec sh -c '…' _ {}`, `bash -c '…' _ *.txt`, `bash -c "echo hi" 2>/dev/null`
and `echo watch "$X"`. The five modules that load the reader pass (400
passed, exit 0). I then restored the clone. A redirection written after the
flag is asked as well as skipped over. This rule adds stops and never
silences: a `>$LOG` there asks, and a quoted string that begins with `>` is
still asked.

## White 3 — `_hides_a_commit` answers only after the recursion limit, so a deep nesting takes thirty seconds

`_hides_a_commit` (`hooks/commit-review-gate.py:146`) answers a deep nesting
correctly, but only when `RecursionError` fires, about 330 levels down. Each
level rescans the rest of the body: `_heredoc_split`, `_paren_end`,
`drop_comments` and `split_segments_with_separators` run once per level. A
commit beside 4000 or 6000 nested `<(` takes 30.8 s and 31.4 s at HEAD and
0.4 s and 0.2 s at the base. The answer is right (deny), so this is not a
silence. It stands next to a hook with no timeout of its own in
`hooks/hooks.json`. The answer's timing rests on the interpreter's recursion
limit, which §13 of the contract asks to be distrusted. A bound on the reading
depth answers in 1.8 s and 3.3 s, and the same modules pass. This is offered,
not owed.

## Regression tests to plant

The rows in the second fence go into `STILL_HANDED` in
`tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`. The
gate was run as a subprocess against each one: each is silent at HEAD, and the
trial reader asks it. They have not been run as planted cases. Under §15,
whoever plants them runs them red against HEAD before committing.

## Facts for the ledger

- The words before a shell's `-c` flag are not asked whether they expand, and
  that loses nothing a shell runs as a command: each such word is an option's
  value, a redirection or a script operand (Executed, round 3: three rows
  silent at base and HEAD, deny at `567069b6`).
- `_eval_argument`'s stand-in differs from a `!= stand_in` trigger only where
  a runner's next word is literally `git` or `eval`, and no runner runs the
  `eval` builtin (Read, round 3).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_is_the_program` does not read `watch` as the program behind a redirection or in a case arm, a function body or a coprocess, so the string it runs is never asked whether it expands | `hooks/cmdline.py:1457` | open | Executed: six shapes deny at `3006eb85`, silent at `567069b6` and `784d1547`, silent at `3911a8cf`; round 2's yellow 2 class, not enumerated |
| 🟡 2 | The shell branch of `command_strings` takes a redirection written after `-c` for the string, and the `watch` branch puts it first in the joined string | `hooks/cmdline.py:1498` | open | Executed: five shapes deny at `3006eb85`, silent at `567069b6`, `784d1547` and `3911a8cf`; bash 3.2.57 landed the commit for the four `bash` shapes; the spec sentence at `docs/commit-review-gate-spec.md:307` is false for them |
| ⬜ 3 | `_hides_a_commit` answers a deep nesting only at the recursion limit, after about 330 full rescans | `hooks/commit-review-gate.py:146` | open | Executed: 30.8 s and 31.4 s at HEAD against 0.4 s and 0.2 s at the base for 4000 and 6000 nested `<(`, deny throughout; a depth bound gives 1.8 s and 3.3 s |
| 🟢 | round 2's blocking finding is closed — a commit found beside a nesting too deep is kept | `hooks/commit-review-gate.py:146` | confirmed | Executed: nine nesting kinds at four depths deny at `784d1547` and `3911a8cf`; the planted case goes red when the catch is removed |
| 🟢 | round 2's yellow 2 is closed for its rows — the shell string is read after the flag, and `watch` counts behind a runner's options, a list opener, `(` and `!` | `hooks/cmdline.py:1496` | confirmed | Executed: each of five reverts turns its planted rows red by name; the narrowing that leaves words before `-c` unasked is sound, see prose; the class's remaining shapes are 🟡 1 and 🟡 2 |
| 🟢 | round 2's yellow 3 is closed — `eval` stands in where no position names the command word | `hooks/commit-review-gate.py:230` | confirmed | Executed: reverting the stand-in turns four `EVALS` rows red; keeping the runner trigger on `git` changes nothing that runs, see prose |
| 🟢 | round 2's yellow 4 is answered — the guard spec says the record is read first and stands | `docs/worktree-guard-spec.md:171` | confirmed | Read: `consent` returns `"record"` from `granted` before any answer is read, as the spec and the case docstring now say |
| 🟢 | round 2's white 5 is answered — the fragment and the ledger rows carry the corrected claims | `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md` | confirmed | Executed: `bin/evidence-check` exit 0, nothing drifted or broken; Read: E18 and E20 |
| ❓ | The fixes' cases on Windows | CI's `windows-latest` leg | ❓ out of verified scope | Not run here; CI answers it at the pull request |
| ❓ | Whether a hook that runs thirty seconds is cut off by the harness, which would turn white 3 into a silence | `hooks/hooks.json` | ❓ out of verified scope | No timeout is set there and the harness default was not measured; the orchestrator answers it |

## Paste-ready fixes

### 🟡 1 and 🟡 2 — `hooks/cmdline.py`

```python
import os
import re
import shlex
```

```python
# A redirection word: an operator with its target (`2>/dev/null`, `>&2`), or
# an operator alone (`2>`), whose target is the next word. The shell takes it
# off the command line wherever it stands, so it is neither a program nor the
# string a host runs (round 3 of 1790644505).
REDIRECTION = re.compile(r"\d*(?:&>>?|>>?|<<<|<>|<&|>&|>\||<)")


def _is_the_program(tokens, k):
    """True when TOKENS[k] sits where the segment's program runs.

    Before it stand only assignments, a list opener, `!`, `(` or a
    redirection -- or a runner, after which its own options and operands
    (`nice -n 5 watch`, `sudo -E watch`) are read past, since this reader does
    not parse them. In a `case` arm, a function definition or a coprocess no
    position names the program, so `watch` there is read as it, the way
    `command_word` reads the first `git`: a false one is a stop, never a
    silence. `grep -n watch *.py` has a program before `watch`, and is not one
    (rounds 2 and 3 of 1790644505).
    """
    j = 0
    while j < k:
        t = tokens[j]
        if (
            os.path.basename(t) in RUNNERS
            or t in UNPLACED
            or t.endswith(")")
            or (j + 1 < k and tokens[j + 1] == "()")
        ):
            return True
        if REDIRECTION.fullmatch(t):
            j += 2
            continue
        if not (
            ("=" in t and not t.startswith("-"))
            or t in LIST_OPENERS
            or t in ("!", "(")
            or REDIRECTION.match(t)
        ):
            return False
        j += 1
    return True
```

```python
            for t in rest[flag + 1 :]:
                if skip:
                    skip = False
                elif t in VALUED:
                    skip = True
                elif t != "--" and not t.startswith(("-", "+")):
                    # A redirection after the flag is not the string: it is
                    # asked too, and the word after it is the string (round 3
                    # of 1790644505).
                    out.append(t)
                    if REDIRECTION.fullmatch(t):
                        skip = True
                    elif not REDIRECTION.match(t):
                        break
```

```python
            out.append(" ".join(words))
            # The outer shell takes a redirection off before `watch` runs, so
            # the string is asked without it as well (round 3 of 1790644505).
            out.append(" ".join(w for w in words if not REDIRECTION.match(w)))
```

### 🟡 1 and 🟡 2 — the rows to plant in `STILL_HANDED`

```python
    # Round 3 of 1790644505: a redirection after the flag, and `watch` behind
    # a redirection or where no position names the program.
    "bash -c 2>/dev/null $CMD": 'bash -c 2>/dev/null "$CMD"',
    "bash -c 2> /dev/null $CMD": 'bash -c 2> /dev/null "$CMD"',
    "bash -c >/dev/null $CMD": 'bash -c >/dev/null "$CMD"',
    "bash -lc </dev/null $CMD": 'bash -lc </dev/null "$CMD"',
    "watch -g 2>/dev/null $CMD": 'watch -g 2>/dev/null "$CMD"',
    "2>/dev/null watch $CMD": '2>/dev/null watch -g "$CMD"',
    "a case arm watch $CMD": 'case a in a) watch -g "$CMD";; esac',
    "a function body watch $CMD": 'f() { watch -g "$CMD"; }; f',
    "a spaced definition watch $CMD": 'f () { watch -g "$CMD"; }; f',
    "function f watch $CMD": 'function f { watch -g "$CMD"; }; f',
    "coproc watch $CMD": 'coproc watch -g "$CMD"',
```

### ⬜ 3 — `hooks/commit-review-gate.py`, offered

```python
# How deep one body is read inside another before it reads as one that might
# commit unread. Far above anything written by hand and far below the
# recursion limit, so the answer arrives in bounded time instead of after some
# three hundred full rescans (round 3 of 1790644505).
NESTING_READ = 32
_nesting = [0]


def _hides_a_commit(text):
    """`_reads_a_commit`, and True for a body nested deeper than it reads.

    A body this process does not finish reading might commit, the way an
    `eval` argument it cannot expand might (round 2 of 1790644505). Answering
    here keeps every invocation already found; a `RecursionError` caught in
    `main` discarded them all. The bound answers before the stack runs out,
    and the catch stays for a platform whose limit is lower still.
    """
    if _nesting[0] >= NESTING_READ:
        return True
    _nesting[0] += 1
    try:
        return _reads_a_commit(text)
    except RecursionError:
        return True
    finally:
        _nesting[0] -= 1
```

## Executed probes

| What was run | Result |
|---|---|
| The gate as a subprocess at `3911a8cf`, `3006eb85`, `567069b6` and `784d1547`, a fresh session id per call, 25 rows: redirection and `watch` placements, words before `-c`, `eval` behind runners, controls | 🟡 1's six and 🟡 2's five rows: silent, deny, silent, silent. `bash -i --rcfile "$F" -c true` and `bash "$S" -c x`: silent, deny, deny, silent. `nice`/`command`/`time eval "$X"`: silent, silent, deny, deny. `sudo -u git eval "$X"`: silent, silent, silent, deny. `sh -c 2>&1 "$CMD"`: silent at all four. Controls as expected |
| The same four gates, a commit into another repository beside nine nesting kinds at depths 300, 500, 1000 and 3000 | deny at `3911a8cf` and `784d1547` for all 36 rows; `3006eb85` raises and `567069b6` is silent for seven kinds from depth 500 |
| bash 3.2.57 in a temporary repository, `CMD` set to a commit: the four `bash` shapes of 🟡 2 | a commit landed for each (0→1→2→3→4) |
| Seven reverts of round 2's fixes in the clone, each with its module through `bin/test` | each exit 1, with the planted rows failing by name: catch 1, flag 3, `!` 1, list opener 1, runner 3, `eval` stand-in 4, `(` 1 |
| `bin/test` on the five modules that load the reader, at `784d1547` | exit 0, 416 passed |
| The trial fixes for 🟡 1 and 🟡 2, the reader asked directly, then the same modules | all 11 shapes asked and expanding, 5 controls not; exit 0, 400 passed on four modules; clone restored |
| Timing, 4000 and 6000 nested `<(` beside a commit, at `3911a8cf` and `784d1547` | 0.4 s and 0.2 s against 30.8 s and 31.4 s, deny throughout; with the ⬜ 3 bound 1.8 s and 3.3 s, deny, and the four modules pass (400); clone restored |
| `bin/evidence-check` at `784d1547` | exit 0; 0 drifted, 0 broken |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — the sealer's, once, after the rounds settle; this round leaves 🟡 1 and 🟡 2 open, so it is due once the orchestrator has settled them under the cap |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The splitter reads the `&` in `2>&1` as a separator, so `sh -c 2>&1 "$CMD"` splits away from its string and reads silent (silent at all four SHAs, so not this branch's regression) | a new issue against the splitter in `hooks/cmdline.py` | the orchestrator, who files it |

Needs a fix: yes — 🟡 1 and 🟡 2, the rest of round 2's yellow 2 class: `watch` behind a redirection or in a case arm, a function body or a coprocess, and a redirection after a shell's `-c`
Loses a record or crashes: no

## Proof block

Files opened this round: `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/rounds/round-2.md`,
`hooks/cmdline.py` (lines 1275–1560), `hooks/commit-review-gate.py` (lines
140–330 and 1160–1260), `hooks/worktree_consent.py` (lines 373–395 and
445–480), `hooks/hooks.json`, `docs/worktree-guard-spec.md` (lines 160–195),
`docs/commit-review-gate-spec.md` (lines 300–318),
`tests/test_no_shape_the_base_stops_reads_silent.py` (lines 1–140), the fix
diff `ed1c0132..195d8176` in full for `hooks`, `tests` and `docs`, and its
word diff for `seal/ledger.md` and the changelog fragment, `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md`
rows E14, E18 and E20, `bin/test`'s header. The probe scripts, the clone, the
four exported trees and the temporary repositories were in this round's
scratch directory and are deleted.

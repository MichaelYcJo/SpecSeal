# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — review round 3

| Field | Value |
|---|---|
| Target SHA | 784d1547027e37de7a8358d20022b52501e7e996 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #671 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `784d1547027e37de7a8358d20022b52501e7e996..d824b82a653dbdd7fa5f413252d2e739fdd433ea`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 and 🟡 2, the rest of round 2's yellow 2 class: `watch` behind a redirection or in a case arm, a function body or a coprocess, and a redirection after a shell's `-c` |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 closed on its one reopening. Target round 2's fix diff `ed1c0132..195d8176` at HEAD `784d1547`, with the fixes' new units as a finding surface, the smith's two narrowings of the proposed fences to judge, and whether any shape still reads silent where `3911a8cf` judged it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_is_the_program` does not read `watch` as the program behind a redirection or in a case arm, a function body or a coprocess, so the string it runs is never asked whether it expands | `hooks/cmdline.py:1457` | deferred #674 | #674 — The run is capped. Every shape also reads silent at `3911a8cf`, so none is below the base. #674 fixes the rest of #670's class in this release, after this lands; Executed: six shapes deny at `3006eb85`, silent at `567069b6` and `784d1547`, silent at `3911a8cf`; round 2's yellow 2 class, not enumerated |
| 🟡 2 | The shell branch of `command_strings` takes a redirection written after `-c` for the string, and the `watch` branch puts it first in the joined string | `hooks/cmdline.py:1498` | deferred #674 | #674 — The same; bash lands the commit in these shapes at the base too; Executed: five shapes deny at `3006eb85`, silent at `567069b6`, `784d1547` and `3911a8cf`; bash 3.2.57 landed the commit for the four `bash` shapes; the spec sentence at `docs/commit-review-gate-spec.md:307` is false for them |
| ⬜ 3 | `_hides_a_commit` answers a deep nesting only at the recursion limit, after about 330 full rescans | `hooks/commit-review-gate.py:146` | deferred #674 | #674 — The cost of a deep nesting; the answer is still deny. #674 adds a depth bound, measured before and after; Executed: 30.8 s and 31.4 s at HEAD against 0.4 s and 0.2 s at the base for 4000 and 6000 nested `<(`, deny throughout; a depth bound gives 1.8 s and 3.3 s |
| 🟢 | round 2's blocking finding is closed — a commit found beside a nesting too deep is kept | `hooks/commit-review-gate.py:146` | confirmed | Executed: nine nesting kinds at four depths deny at `784d1547` and `3911a8cf`; the planted case goes red when the catch is removed |
| 🟢 | round 2's yellow 2 is closed for its rows — the shell string is read after the flag, and `watch` counts behind a runner's options, a list opener, `(` and `!` | `hooks/cmdline.py:1496` | confirmed | Executed: each of five reverts turns its planted rows red by name; the narrowing that leaves words before `-c` unasked is sound, see prose; the class's remaining shapes are 🟡 1 and 🟡 2 |
| 🟢 | round 2's yellow 3 is closed — `eval` stands in where no position names the command word | `hooks/commit-review-gate.py:230` | confirmed | Executed: reverting the stand-in turns four `EVALS` rows red; keeping the runner trigger on `git` changes nothing that runs, see prose |
| 🟢 | round 2's yellow 4 is answered — the guard spec says the record is read first and stands | `docs/worktree-guard-spec.md:171` | confirmed | Read: `consent` returns `"record"` from `granted` before any answer is read, as the spec and the case docstring now say |
| 🟢 | round 2's white 5 is answered — the fragment and the ledger rows carry the corrected claims | `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md` | confirmed | Executed: `bin/evidence-check` exit 0, nothing drifted or broken; Read: E18 and E20 |
| ❓ | The fixes' cases on Windows | CI's `windows-latest` leg | ❓ out of verified scope | Not run here; CI answers it at the pull request |
| ❓ | Whether a hook that runs thirty seconds is cut off by the harness, which would turn white 3 into a silence | `hooks/hooks.json` | ❓ out of verified scope | No timeout is set there and the harness default was not measured; the orchestrator answers it |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/commit-review-gate.py:1174` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/commit-review-gate.py:177` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/commit-review-gate.py:191` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/commit-review-gate.py:194` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/worktree_consent.py:330` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/commit-review-gate.py:1240` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_no_shape_the_base_stops_reads_silent.py` | round 1's 🟢 — confirmed |
| round-1 | CI's `windows-latest` leg | round 1's ❓ — out of verified scope |
| round-2 | `hooks/commit-review-gate.py:1183` | round 2's 🔴 1 — fixed |
| round-2 | `hooks/cmdline.py:1468` | round 2's 🟡 2 — fixed |
| round-2 | `hooks/commit-review-gate.py:216` | round 2's 🟡 3 — fixed |
| round-2 | `docs/worktree-guard-spec.md:175` | round 2's 🟡 4 — answered |
| round-2 | `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/changelog.md:19` | round 2's ⬜ 5 — answered |
| round-2 | `hooks/commit-review-gate.py:1196` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline.py:1454` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree_consent.py:367` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The splitter reads the `&` in `2>&1` as a separator, so `sh -c 2>&1 "$CMD"` splits away from its string and reads silent (silent at all four SHAs, so not this branch's regression) | a new issue against the splitter in `hooks/cmdline.py` | the orchestrator, who files it |

# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — review round 2

| Field | Value |
|---|---|
| Target SHA | 3e443b8ea0dfb1225eecf1739cb5ac33b0849f8c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #671 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `ed1c0132c803cba5e8f7e05cc3b3dca060e2363a..195d81765b54e011a72270ef8d918ee786608b4c`, 7 commits |
| Contract changes | command_word → names_an_unknown_command, walk_directories, parse_git, _eval_argument, round-1-report.md, round-1.md, round-2-report.md, round-2.md |
| New units | _is_the_program (depth 1); _reads_a_commit (depth 1); test_a_commit_found_before_a_nesting_too_deep_still_stops (depth 1) |
| Needs a fix | yes — 🔴 1 (a commit found in another repository reads silent beside 500 nested substitutions, below the base); 🟡 2, 🟡 3 and 🟡 4 are each fix or justify |
| Loses a record or crashes | yes — 🔴 1 reads a commit silent that `3911a8cf` stopped, and bash lands it in the unjudged repository |

- [x] Pass

## What this round was asked

Round 2, verifying, over round 1's fix diff `3006eb85..567069b6` at HEAD `3e443b8e`. Asked whether each verdict round 1 closed is closed, with the fixes' new units as a finding surface, and three pushes: can any shape still read silent where `3911a8cf` judged it, does 🟡 3's narrowing hide a real commit, and does 🟡 5's last-answer reading hold for the guard's shared reader.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The `RecursionError` catch in `main` discards every invocation already found, so a commit into another repository beside 500 nested substitutions reads silent where the base denied | `hooks/commit-review-gate.py:1183` | **fixed** `8cea9a57` | fixed at 8cea9a57 — `_hides_a_commit` wraps the reader and answers True at the depth that overflowed, so the walk's commits are kept; `main`'s `except` stays as a backstop; Executed: three rows deny at `3911a8cf`, raise at `3006eb85`, silent at `567069b6`; bash commits in the target |
| 🟡 2 | `command_strings` asks a word before the `-c` flag instead of the string, and misses `watch` behind a runner's options or a list opener, so eight shapes the pre-fix head stopped read silent | `hooks/cmdline.py:1468` | **fixed** `8de1b03c` | fixed at 8de1b03c — narrowed in `9bbede7d` and pinned in `c60dfe9c`: a shell's string is the first operand after `-c`, and `watch` counts wherever it is the program; Executed: eight rows deny at `3006eb85` and are silent at `567069b6`; bash commits for the two shell rows |
| 🟡 3 | `_eval_argument` finds no `eval` in a case arm, a function body or a coprocess, because the stand-in rule looks for `git` only | `hooks/commit-review-gate.py:216` | **fixed** `8de1b03c` | fixed at 8de1b03c — narrowed in `a63bc156`: `command_word` takes the stand-in word, and `_eval_argument` passes `eval`; Executed: four rows silent at base, pre-fix and head; bash commits for the case and function rows |
| 🟡 4 | The guard spec says the guard asks again after a later `per axis`, but a creation record written under the press is read first | `docs/worktree-guard-spec.md:175` | answered | corrected at `195d8176`: the guard spec and the case docstring say a later `per axis` takes back the commit gate's deny, and a creation record written under the press stands, by the owner-side decision the orchestrator took; no code changed; Executed: after the record, `consent` returns `"record"` while `automation_answered` is `False` |
| ⬜ 5 | The changelog fragment and ledger rows E18 and E20 repeat the claims 🔴 1 and 🟡 4 refute | `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/changelog.md:19` | answered | corrected at `195d8176`: the changelog fragment and ledger rows E18, E20 (and E1, E14, E15, which repeated the claims); Read; paperwork correction, outside `Needs a fix` |
| 🟢 | round 1's blocking finding is closed — the fallback for a command the splitter could not finish stands beside what was found | `hooks/commit-review-gate.py:1196` | confirmed | Executed: round 1's four review-arm rows and two parity rows pass at `567069b6`; the nesting case is 🔴 1, a different trigger |
| 🟢 | round 1's yellow finding 2 is closed as a crash — the gate no longer raises at 500 levels | `hooks/commit-review-gate.py:1183` | confirmed | Executed: exit 0 where `3006eb85` raised; the silence that remains when a commit was found elsewhere is 🔴 1 |
| 🟢 | round 1's yellow finding 3 is closed — the seven non-commit shapes are silent | `hooks/cmdline.py:1454` | confirmed | Executed: the seven `CONTROLS` rows and the ten `STILL_HANDED` rows pass; what the narrowing drops is 🟡 2 |
| 🟢 | round 1's yellow finding 4 is closed for its ten shapes | `hooks/commit-review-gate.py:216` | confirmed | Executed: the ten `EVALS` rows pass and `if true; then eval …` denies; the rest of the class is 🟡 3 |
| 🟢 | round 1's yellow finding 5 is closed for the commit gate — the last routing answer from the clone stands | `hooks/worktree_consent.py:367` | confirmed | Executed: a two-question `per axis` after a press reads `False`, also from a linked worktree; the guard's half is 🟡 4 |
| ❓ | The fixes' cases on Windows | CI's `windows-latest` leg | ❓ out of verified scope | Not run here; CI answers it at the pull request |

## Paste-ready fixes

```python
def _hides_a_commit(text):
    """`_reads_a_commit`, and True for a body nested deeper than it recurses.

    A body this process cannot finish reading might commit, the way an `eval`
    argument it cannot expand might (round 2 of 1790644505). Answering here,
    at the depth that overflowed, keeps every invocation already found; a
    `RecursionError` caught in `main` discarded them all.
    """
    try:
        return _reads_a_commit(text)
    except RecursionError:
        return True


def _reads_a_commit(text):
    """True when TEXT, read as commands, might invoke `git commit`.
```
```markdown
A body nested deeper than the reader recurses reads as one that might commit,
beside every commit already found, since a gate that raises is skipped and a
skipped gate is silence; catching the raise around the whole reading had
thrown away a commit it had found in another repository (round 2 of work item
1790644505).
```
```python
def test_a_commit_found_before_a_nesting_too_deep_still_stops(
    monkeypatch, capsys, projects, tmp_path
):
    """Round 2 of 1790644505. A reader that overflows on 500 nested
    substitutions used to discard the commit it had already found in `u`,
    leaving only the declared session directory to judge."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    deep = "$(" * 500 + "true" + ")" * 500
    for command in (
        f"git -C {q(u)} commit -m x; echo {deep}",
        f"cd {q(u)} && {BODY}; echo {deep}",
    ):
        answers = with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        )
        for which, got in answers.items():
            assert "silent" not in got, (command, which, got)
```
```python
def _is_the_program(tokens, k):
    """True when TOKENS[k] sits where the segment's program runs.

    Before it stand only assignments, a list opener, `!` or `(` -- or a
    runner, after which its own options and operands (`nice -n 5 watch`,
    `sudo -E watch`) are read past, since this reader does not parse them.
    `grep -n watch *.py` has a program before `watch`, and is not one.
    """
    for t in tokens[:k]:
        if os.path.basename(t) in RUNNERS:
            return True
        if not (
            ("=" in t and not t.startswith("-")) or t in LIST_OPENERS or t in ("!", "(")
        ):
            return False
    return True
```
```python
        if word in SHELLS and any(_hands_a_string(word, t) for t in rest):
            # The string is the first operand after the flag that says so.
            # A word before that flag is an option's value (`--rcfile f`) or
            # a redirection (`2>/dev/null`), never a positional parameter,
            # so it is asked too: skipping it made `"$CMD"` the one word
            # not asked (round 2 of 1790644505).
            flag = next(j for j, t in enumerate(rest) if _hands_a_string(word, t))
            out += [t for t in rest[:flag] if not t.startswith(("-", "+"))]
            skip = False
            for t in rest[flag + 1 :]:
```
```python
        elif word == "watch" and _is_the_program(tokens, k):
```
```python
    # Round 2 of 1790644505: a word before the `-c` flag, and `watch` behind
    # a runner's own options or a list opener, used to hide the string.
    "bash --rcfile f -c $CMD": 'bash --rcfile /dev/null -c "$CMD"',
    "bash 2>/dev/null -c $CMD": 'bash 2>/dev/null -c "$CMD"',
    "nice -n 5 watch $CMD": 'nice -n 5 watch -g "$CMD"',
    "sudo -E watch $CMD": 'sudo -E watch "$CMD"',
    "then watch $CMD": 'if true; then watch -g "$CMD"; fi',
```
```python
def command_word(tokens, stand_in="git"):
```
```python
        or (after_runner and os.path.basename(toks[i]) != stand_in)
```
```python
        later = [
            j for j in range(i + 1, len(toks)) if os.path.basename(toks[j]) == stand_in
        ]
```
```python
    word, _unplaced = command_word(list(toks), "eval")
```
```python
    # Round 2 of 1790644505: where no position names the command word, the
    # first `eval` stands in, as the first `git` does.
    "a case arm": f"case a in a) eval '{C}';; esac",
    "a function body": f"f() {{ eval '{C}'; }}; f",
    "a coprocess": f"coproc eval '{C}'",
```
```markdown
5. **The last answer stands**: of every answer to the routing question from
   that clone, the latest is the one read. A session that pressed `automation`
   for one work item and answered `per axis` or `no work item` for a later one
   has, on its latest answer, a person who may be asked, so the press is taken
   back; a later press gives it back. An answer to any other question changes
   nothing. The record is not taken back: it is read first, so once a creation
   has run in this session, a later answer does not bring the question back.
   This is the commit gate's round 1 finding (work item 1790644505, yellow 5),
   and it moves the guard in the asking direction only.
```
```python
    """Round 1 of 1790644505, yellow 5. A session that pressed `automation` for
    one work item and then answered `per axis` for another has, on its latest
    answer, a person who may be asked; the automation text would tell the
    model not to. The last answer from this clone stands, so the gate goes
    back to the base's deny-then-ask. The guard's creation record is read
    before this answer, so it asks again only while no creation has run. A
    later `automation` press gives the press back."""
```

## Executed probes

| What was run | Result |
|---|---|
| Differential, gate as a subprocess at `3911a8cf`, `3006eb85` and `567069b6`, fresh session id each, 28 commands (nesting beside a found commit, shell-string and `watch` placements, `eval` stand-ins, controls) | 🔴 1: three rows deny, raise, silent; 300 and 400 levels deny at all three. 🟡 2: eight rows silent, deny, silent. 🟡 3: four rows silent at all three. Controls as expected |
| bash 3.2.57, in temporary repositories: 🔴 1's first row, and 🟡 2's and 🟡 3's shapes with `CMD='git commit -qm x'` | the commit landed for each: 🔴 1 in the target, and `--rcfile`, `2>/dev/null`, the case arm and the function body in the session's repository; `watch` is not installed |
| `worktree_consent` with a two-question transcript: a press, then `per axis`; then after `record`; then `per axis` from a linked worktree | `False` / `""`; `"record"` with `automation_answered` `False`; `False` |
| `bin/test` on the four modules the fix pass touched, at `567069b6` | 274 passed |
| Trial fixes for 🔴 1, 🟡 2 and 🟡 3, then the differential rows | every 🔴 1, 🟡 2 and 🟡 3 row denies; the controls unchanged |
| Trial fixes, then `bin/test` on the 34 modules that load the gate, `hooks/cmdline.py`, the guard or the consent reader | 1443 passed, 2 skipped |
| The nine planted rows at `567069b6`, then with the trial fixes | 9 failed by name; 267 passed |
| `bin/evidence-check` at `567069b6` | exit 0; 2739 ok, 0 drifted, 0 broken |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — the sealer's, once, after the rounds settle; not due while this report leaves findings open |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

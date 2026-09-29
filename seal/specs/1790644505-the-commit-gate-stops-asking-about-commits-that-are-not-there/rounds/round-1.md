# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — review round 1

| Field | Value |
|---|---|
| Target SHA | f25c6b1a87d377ed72d1a2cb4353fbb9d68c677c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #671 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `3006eb8518f1f93b3ac5095d119932cee398e431..567069b62d80d74931bcef29f57f0d65ebe150ad`, 10 commits |
| Contract changes | _string_hides_a_commit → _hides_a_commit, commit_invocations, round-1-report.md, round-1.md; automation_answered → automation_pressed, consent, round-1-report.md, round-1.md, round-2-report.md, round-2.md, questions.md, spec.md, pytest |
| New units | VALUED (depth 1); command_strings (depth 1); _routing_answer (depth 1); EVALS (depth 1); test_an_eval_behind_the_same_words_is_read (depth 1); STILL_HANDED (depth 1); test_a_string_that_is_an_expansion_still_stops (depth 1); test_a_later_routing_answer_takes_the_press_back (depth 1); test_an_answer_to_another_question_leaves_the_press_standing (depth 1); test_a_parity_arm_is_not_waived_by_a_newly_read_commit (depth 1) |
| Needs a fix | yes — 🔴 1 (a commit found in a declared repository displaces the fallback, and six shapes the base stopped read silent); 🟡 2 to 🟡 5 are each fix or justify |
| Loses a record or crashes | yes — 🔴 1 reads real commits silent that `3911a8cf` stopped, and bash lands them; 🟡 2 crashes the gate at 500 nested substitutions, which the dispatcher turns into silence |

- [x] Pass

## What this round was asked

Round 1, the first finding round, over the work item's own diff `3911a8cf...f25c6b1a`. Asked to review the automation-deny reversal the owner approved and phases 4 and 5 (#669, #670), the only changes to what the gate reads, with a false silent against `3911a8cf` named first, a press read where none was given second, and a new false stop in an attended session third.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A commit the new reading finds in a declared repository displaces the fallback for a command the splitter could not finish, so a commit in the session's own directory, or a parity arm, goes unjudged | `hooks/commit-review-gate.py:1174` | **fixed** `340ad4c8` | fixed at 340ad4c8 — a command the parser could not finish is judged in the session's directory beside any commit found, not only when none was; Executed: four review-arm and two parity-arm shapes deny at `3911a8cf` and are silent at `f25c6b1a`; bash commits in the unjudged repository |
| 🟡 2 | `_hides_a_commit` recurses without a bound, so 500 nested substitutions raise and the dispatcher turns the raise into silence | `hooks/commit-review-gate.py:177` | **fixed** `340ad4c8` | fixed at 340ad4c8 — a `RecursionError` from nesting is read as an unparsed command, so it stops; Executed: `RecursionError` at 500 levels, silent through `hooks/dispatch.py`, deny at the base |
| 🟡 3 | The expansion check runs on a shell's positional arguments and on `watch` anywhere in a segment, so commands that commit nothing stop, even in a declared repository | `hooks/commit-review-gate.py:191` | **fixed** `a1804ee7` | fixed at a1804ee7 — only the string a shell runs is asked whether its command word expands; Executed: seven non-commit commands silent at the base and deny at the head |
| 🟡 4 | `_eval_argument` does not read past a reserved word, a prefix or a subshell, so the class #669 and #670 fixed for `git` and `sh -c` stays open for `eval` | `hooks/commit-review-gate.py:194` | **fixed** `aa3a0918` | fixed at aa3a0918 — `eval` is found behind a reserved word, `!`, `time`, `command`, `builtin`, a runner, a subshell or a brace group; Executed: ten shapes silent at base and head; bash runs each `eval` |
| 🟡 5 | An `automation` press stands after a later `per axis` answer in the same session, and the gate then tells the model not to ask a person who is present | `hooks/worktree_consent.py:330` | **fixed** `be6e0f08` | fixed at be6e0f08 — the clone's last routing answer stands, so a later `per axis` takes an earlier press back; Executed: a transcript with both answers reads as pressed, and the gate denies twice with the automation text |
| 🟢 | The automation decision: deny at both sites under the press, no question tool named, every unreadable press is no press | `hooks/commit-review-gate.py:1240` | confirmed | Read, and exercised by the 251 cases and the 🟡 5 probe |
| 🟢 | Work item `1790635415`'s false-silent shapes still stop, with and without the press | `tests/test_no_shape_the_base_stops_reads_silent.py` | confirmed | Executed at `f25c6b1a` |
| ❓ | The cases on Windows | CI's `windows-latest` leg | ❓ out of verified scope | Not run here; CI answers it at the pull request |

## Paste-ready fixes

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
```markdown
The reading can only have gained stops by this, for the reason #669's change
gives, and for one more: a command the splitter could not finish is still
judged in the session's own directory when the new reading found a commit in
the part it did read. Without that, a commit found in a declared repository
took the session's directory out of the judgment (round 1 of 1790644505).
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

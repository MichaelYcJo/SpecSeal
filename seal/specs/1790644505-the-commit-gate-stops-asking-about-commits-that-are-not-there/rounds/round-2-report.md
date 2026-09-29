# Round 2 report — the commit gate stops asking about commits that are not there

Target: round 1's fix diff, `git diff 3006eb85..567069b6`, a verifying round.
The branch HEAD `3e443b8e` adds round 1's close on top and changes nothing
under `hooks/`, `tests/` or `docs/`. Reviewed in a `git clone --no-local` of
the orchestrator's worktree at `567069b6`. Two more clones were used for
differential probes, at the base `3911a8cf` and at the pre-fix head `3006eb85`.
Round 1's record and report were read for coordinates. Its verdicts were
re-derived here, not carried.

## What this round found

Round 1's five findings are closed for the shapes it named. Three of the fixes
stop short of their class, and one of them moves a shape below the base:

```
yellow 2's fix: catch RecursionError in main
  └─ 🔴 1  the catch throws away every commit already found, so a commit in
           another repository next to 500 nested $( reads silent (base: deny)
yellow 3's fix: ask "does it expand?" only of the string a host runs
  └─ 🟡 2  the string is picked wrongly after a word before -c, and watch is
           missed behind a runner's options or a list opener → pre-fix deny,
           head silent
yellow 4's fix: find eval the way git is found
  └─ 🟡 3  the stand-in rule for a case arm, a function body or coproc still
           looks for git only → eval silent there
yellow 5's fix: the last routing answer stands
  └─ 🟡 4  the guard spec and changelog say the guard asks again, but a
           creation record written under the press still wins
```

Only 🔴 1 is below the base. The three 🟡 findings are shapes the pre-fix head
or the branch's own class stops and the head does not. Each one was run in
bash 3.2.57 and made the commit.

## Findings

### 🔴 1 — The recursion guard discards the commits it already found

`hooks/commit-review-gate.py:1183`, in `main`.

Round 1's 🟡 2 fix catches `RecursionError` around `commit_invocations` and
sets `invocations, clean = [], False`. The overflow happens in
`_hides_a_commit`, while it reads a substitution body. That is after the walk
has already found every plain `git … commit` segment, and the catch throws
those away too. What remains is the unparsed fallback, and that fallback
judges only the session's own directory.

So a commit into another repository survives only when the session's
directory stops for itself. From a declared session directory, with the
target `u` opted in and undeclared:

| Command | Base `3911a8cf` | Pre-fix `3006eb85` | Head `567069b6` |
|---|---|---|---|
| `git -C u commit -m x; echo $( ×500 true ) ×500` | deny | raises | silent |
| `cd u && git commit -m x; echo $( ×500 true ) ×500` | deny | raises | silent |
| `git -C u commit -m x; echo $(echo ×500 1) ×500` | deny | raises | silent |
| the same with 300 or 400 levels | deny | deny | deny |

In bash 3.2.57, the first row exited 0 and the commit landed in `u`.

Why it matters: the owner's constraint for this work item is that no shape
reads silent where `3911a8cf` judges it. The reader crossing its recursion
limit is the only trigger, so this is the same way past the gate that round 1
recorded as 🟡 2. It now lets through a commit the base caught, and that is
what makes it 🔴. The limit also depends on the interpreter and on its stack,
so where the edge falls is not a property of the command alone.

The fix answers at the depth that overflowed. A body this process cannot
finish reading "might" commit, which is the rule `_eval_hides_a_commit`
already applies to an expansion. The walk's invocations are then kept, and
the substitution adds an unresolved target beside them. The `except` in
`main` stays as a backstop for an overflow outside the reader. With the fix
applied, all three rows deny, and the case below was red at the head and
green with the fix.

The spec sentence at `docs/commit-review-gate-spec.md:327`–`329` says a
command nested too deep "reads as one it could not parse". That describes
the defect, so the same fix changes the sentence (§14).

### 🟡 2 — The string a shell runs is picked wrongly, and `watch` is missed behind a runner

`hooks/cmdline.py:1468` and `:1486`, in `command_strings` (a new unit, depth 1).

Round 1's 🟡 3 fix asks `names_an_unknown_command` of one string per host
instead of every word. It picks the string in two ways, and each has a gap:

- **The shells.** The fix takes the first non-option word after the host, not
  the first one after the `-c` flag. Before the flag there can be an option's
  value (`--rcfile f`, `--init-file f`) or a redirection token
  (`2>/dev/null`, which the splitter hands back as one word). That word is
  asked, and the real string after `-c` never is.
- **`watch`.** It counts only when every token before it is an assignment or
  a runner. A runner's own options (`nice -n 5`, `timeout 60`, `sudo -E`), a
  list opener (`then`) and `(` all fail that test.

Executed from a declared repository:

| Command | Base | Pre-fix | Head |
|---|---|---|---|
| `bash --rcfile /dev/null -c "$CMD"` | silent | deny | silent |
| `bash --init-file /dev/null -c "$CMD"` | silent | deny | silent |
| `bash 2>/dev/null -c "$CMD"` | silent | deny | silent |
| `nice -n 5 watch -g "$CMD"` | silent | deny | silent |
| `timeout 60 watch -g "$CMD"` | silent | deny | silent |
| `sudo -E watch "$CMD"` | silent | deny | silent |
| `if true; then watch -g "$CMD"; fi` | silent | deny | silent |
| `( watch -g "$CMD" )` | silent | deny | silent |

In bash, with `CMD='git commit -qm x'`, the `--rcfile` and `2>/dev/null` rows
each committed. `watch` is not installed on this machine, so its rows were not
run in a shell. The controls still deny at the head: `sh -c "$CMD"`,
`bash -c -- "$CMD"`, `su -s /bin/sh -c "$CMD" root`, `watch -g "$CMD"`,
`zsh --emulate sh -c "$CMD"`. The last one denies by accident: `--emulate`
takes `sh` as its value, and `sh` happens to be read as the host.

None of these is below the base, which reads no shell string at all. They are
shapes the branch's #670 statement covers ("a command word the shell would
expand in the string a host runs"), and this fix pass is the one place that
narrowed. That is why this is 🟡 rather than ⬜.

The fix keeps round 1's point that positional parameters are not asked.
Words before the `-c` flag are never positional parameters, so they are
asked too. The string is the first operand after the flag. `watch` counts
where only assignments, list openers, `!`, `(` or a runner stand before it,
and once a runner is seen, whatever follows it counts. With the fix, all
eight rows deny, the seven round-1 controls stay silent, and 1443 cases in the
34 modules that load the gate, the reader, the guard or the consent reader
pass (2 skipped).

### 🟡 3 — `eval` in a case arm, a function body or a coprocess is still no commit

`hooks/commit-review-gate.py:216`, in `_eval_argument`.

Round 1's 🟡 4 fix finds `eval` with `command_word`. But where no position
names the command word (a `case` pattern `a)`, a definition `f()`, and the
`UNPLACED` words `case`, `coproc` and `function`), `command_word` lets the
first `git` token stand in, and it looks for `git` only. So:

| Command | Base | Pre-fix | Head |
|---|---|---|---|
| `case a in a) eval 'git commit -m x';; esac` | silent | silent | silent |
| `case a in a) eval "$X";; esac` | silent | silent | silent |
| `f() { eval 'git commit -m x'; }; f` | silent | silent | silent |
| `coproc eval 'git commit -m x'` | silent | silent | silent |
| control: `case a in a) git commit -m x;; esac` | silent | deny | deny |

In bash, the case-arm and function-body rows each committed. This is not a
regression. It is the rest of the class round 1's 🟡 4 named ("the class
#669 and #670 fixed for `git`… stays open for `eval`"), and contract §12 asks
for the class. Round 1's paste-ready fix left it out as well.

The fix gives `command_word` the word to stand in for as a parameter, with
`git` as the default, and `_eval_argument` passes `eval`. The other callers
are unchanged. With it, all four rows deny and the 34 modules pass.

### 🟡 4 — The guard does not ask again once a creation ran under the press

`docs/worktree-guard-spec.md:175`, with the same claim in
`tests/test_an_automation_run_meets_no_commit_prompt.py:276`.

Item 5 says that after a later `per axis` "the press is taken back and the
guard asks again". `worktree_consent.consent` reads the creation record
before it reads the transcript, and the paragraph right below item 5 says
so. An automation run creates its worktrees, and the `PostToolUse` hook
writes the record for the first one. After that, a later `per axis` changes
what `automation_answered` returns, but the guard never reaches it.

Executed with a transcript holding a press and then a `per axis` answer, both
as the two-question call the routing rule prescribes:

- before any creation: `automation_answered` is `False`, and `consent`
  returns `""`, so the guard asks;
- after `worktree_consent.record` for that session: `consent` returns
  `"record"`, so the guard allows silently. The allow text says the user
  answered for the creation, which under the press nobody did.

The commit gate's half is closed. The guard's half is stated and not true.
The claim ships in the spec, in the changelog fragment and in ledger row E20,
and the case's docstring repeats it. Nothing pins it, because the case never
calls the guard.

The paste-ready fix corrects the sentence and the docstring. Making the
guard really ask again means taking back the record too, which changes #604's
design, so it is not proposed here. Whether a later `per axis` should also
revoke a record written under the press is a question for the owner.

### ⬜ 5 — Three records repeat claims 🔴 1 and 🟡 4 refute

These are paperwork corrections, and none of them counts toward `Needs a fix`:

- `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/changelog.md:19`
  says the guard "then asks again", and `:48`–`50` says the change "only adds
  stops" and that a command nested too deep "reads as unfinished".
- `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md`
  row E18 says a command nested too deep "stops wherever it mentions a
  commit", and row E20 ends "the guard, whose reader it is, asks again".

## What the account claimed, and what the code does

- **Claimed** in `docs/commit-review-gate-spec.md:322`: "The reading can only
  have gained stops by this". **The code** at `:1183` discards found
  invocations on overflow, so 🔴 1 is a shape where it lost one.
- **Claimed** in ledger E18: a command nested too deep "stops wherever it
  mentions a commit". **Executed**: it stops only where the session's own
  directory stops. See 🔴 1.
- **Claimed** in `docs/commit-review-gate-spec.md` for #670, as amended: the
  expansion question is asked "in the string a host runs". **Executed**: the
  head picks the wrong word as that string. See 🟡 2.
- **Claimed** in `docs/worktree-guard-spec.md:175`, the changelog fragment and
  E20: the guard asks again after a later `per axis`. **Executed**: not once a
  record exists. See 🟡 4.
- **Claimed** in `phases/phase-5.md` item 2 as corrected, and in phase 4's
  correction: the fallback now stands beside what was found. **Confirmed** by
  reading `:1196`–`1200` and by executing round 1's rows.

## Confirmations

- Round 1's four `$'…'` rows, the 500-deep row with an undeclared session
  directory, and the two parity rows: executed, as part of the 274 cases in
  the four modules the fix pass touched, at `567069b6`.
- The reverse orientation of round 1's first row: session declared, `w`
  undeclared. Executed: the base is silent (it found the `w` invocation and
  judged `w` alone), and the pre-fix head and the head deny.
- `_routing_answer` with the two-question call. Executed: a `per axis` answer
  whose second question ticks boxes reads `False`, and so does one given from
  a linked worktree of the same clone.
- `_eval_argument` now returns an argument in strictly more cases. Read: every
  segment the old loop accepted has `eval` at the same position after
  `command_word`, because `eval` is not in `RUNNERS` and no stand-in jump
  fires on it.
- The new `main` fallback adds the session target and removes none. Read at
  `:1196`–`1200` against `commit_targets` and `names_a_directory`.
- `bin/evidence-check`: exit 0, 0 drifted, 0 broken, at `567069b6`.

## Regression tests to plant

Each was added in the clone and ran red at `567069b6` (9 failed, by name).
With the three code fixes applied, the three modules passed (267 passed).

- `tests/test_no_shape_the_base_stops_reads_silent.py`: one new case, with
  two commands, in the fence under 🔴 1.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`:
  five `STILL_HANDED` rows, in the fence under 🟡 2.
- `tests/test_a_commit_behind_a_reserved_word_is_judged.py`: three `EVALS`
  rows, in the fence under 🟡 3.

## Facts for the evidence ledger

- At `567069b6`, a `RecursionError` in `commit_invocations` is caught in
  `hooks/commit-review-gate.py#main` and replaces every invocation with the
  session-directory fallback. E18 should be anchored to the corrected rule
  once 🔴 1 is fixed.
- `hooks/worktree_consent.py#consent` reads the creation record before the
  transcript, so a later answer never takes back a record. E20's last clause
  should say that.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The `RecursionError` catch in `main` discards every invocation already found, so a commit into another repository beside 500 nested substitutions reads silent where the base denied | `hooks/commit-review-gate.py:1183` | open | Executed: three rows deny at `3911a8cf`, raise at `3006eb85`, silent at `567069b6`; bash commits in the target |
| 🟡 2 | `command_strings` asks a word before the `-c` flag instead of the string, and misses `watch` behind a runner's options or a list opener, so eight shapes the pre-fix head stopped read silent | `hooks/cmdline.py:1468` | open | Executed: eight rows deny at `3006eb85` and are silent at `567069b6`; bash commits for the two shell rows |
| 🟡 3 | `_eval_argument` finds no `eval` in a case arm, a function body or a coprocess, because the stand-in rule looks for `git` only | `hooks/commit-review-gate.py:216` | open | Executed: four rows silent at base, pre-fix and head; bash commits for the case and function rows |
| 🟡 4 | The guard spec says the guard asks again after a later `per axis`, but a creation record written under the press is read first | `docs/worktree-guard-spec.md:175` | open | Executed: after the record, `consent` returns `"record"` while `automation_answered` is `False` |
| ⬜ 5 | The changelog fragment and ledger rows E18 and E20 repeat the claims 🔴 1 and 🟡 4 refute | `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/changelog.md:19` | open | Read; paperwork correction, outside `Needs a fix` |
| 🟢 | round 1's blocking finding is closed — the fallback for a command the splitter could not finish stands beside what was found | `hooks/commit-review-gate.py:1196` | confirmed | Executed: round 1's four review-arm rows and two parity rows pass at `567069b6`; the nesting case is 🔴 1, a different trigger |
| 🟢 | round 1's yellow finding 2 is closed as a crash — the gate no longer raises at 500 levels | `hooks/commit-review-gate.py:1183` | confirmed | Executed: exit 0 where `3006eb85` raised; the silence that remains when a commit was found elsewhere is 🔴 1 |
| 🟢 | round 1's yellow finding 3 is closed — the seven non-commit shapes are silent | `hooks/cmdline.py:1454` | confirmed | Executed: the seven `CONTROLS` rows and the ten `STILL_HANDED` rows pass; what the narrowing drops is 🟡 2 |
| 🟢 | round 1's yellow finding 4 is closed for its ten shapes | `hooks/commit-review-gate.py:216` | confirmed | Executed: the ten `EVALS` rows pass and `if true; then eval …` denies; the rest of the class is 🟡 3 |
| 🟢 | round 1's yellow finding 5 is closed for the commit gate — the last routing answer from the clone stands | `hooks/worktree_consent.py:367` | confirmed | Executed: a two-question `per axis` after a press reads `False`, also from a linked worktree; the guard's half is 🟡 4 |
| ❓ | The fixes' cases on Windows | CI's `windows-latest` leg | ❓ out of verified scope | Not run here; CI answers it at the pull request |

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

## Paste-ready fixes

### 🔴 1

In `hooks/commit-review-gate.py`, rename the existing `def _hides_a_commit(text):`
to the inner name below, leave its body and its recursive calls as they are,
and put this wrapper in front of it:

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

`docs/commit-review-gate-spec.md`, replacing the last sentence of the
paragraph at `:322`–`329`:

```markdown
A body nested deeper than the reader recurses reads as one that might commit,
beside every commit already found, since a gate that raises is skipped and a
skipped gate is silence; catching the raise around the whole reading had
thrown away a commit it had found in another repository (round 2 of work item
1790644505).
```

`tests/test_no_shape_the_base_stops_reads_silent.py`, before
`test_the_reverse_direction_still_stops`:

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

### 🟡 2

In `hooks/cmdline.py`, before `command_strings`:

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

In `command_strings`, the shells' branch up to its loop:

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

and the `watch` condition:

```python
        elif word == "watch" and _is_the_program(tokens, k):
```

`tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`, at
the end of `STILL_HANDED`:

```python
    # Round 2 of 1790644505: a word before the `-c` flag, and `watch` behind
    # a runner's own options or a list opener, used to hide the string.
    "bash --rcfile f -c $CMD": 'bash --rcfile /dev/null -c "$CMD"',
    "bash 2>/dev/null -c $CMD": 'bash 2>/dev/null -c "$CMD"',
    "nice -n 5 watch $CMD": 'nice -n 5 watch -g "$CMD"',
    "sudo -E watch $CMD": 'sudo -E watch "$CMD"',
    "then watch $CMD": 'if true; then watch -g "$CMD"; fi',
```

### 🟡 3

In `hooks/cmdline.py#command_word`, the signature and the two `"git"`
literals of the stand-in rule. The docstring's "the first `git`" then reads
"the first STAND_IN word":

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

In `hooks/commit-review-gate.py#_eval_argument`:

```python
    word, _unplaced = command_word(list(toks), "eval")
```

`tests/test_a_commit_behind_a_reserved_word_is_judged.py`, at the end of
`EVALS`:

```python
    # Round 2 of 1790644505: where no position names the command word, the
    # first `eval` stands in, as the first `git` does.
    "a case arm": f"case a in a) eval '{C}';; esac",
    "a function body": f"f() {{ eval '{C}'; }}; f",
    "a coprocess": f"coproc eval '{C}'",
```

### 🟡 4

`docs/worktree-guard-spec.md`, item 5:

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

`tests/test_an_automation_run_meets_no_commit_prompt.py`, the docstring of
`test_a_later_routing_answer_takes_the_press_back`:

```python
    """Round 1 of 1790644505, yellow 5. A session that pressed `automation` for
    one work item and then answered `per axis` for another has, on its latest
    answer, a person who may be asked; the automation text would tell the
    model not to. The last answer from this clone stands, so the gate goes
    back to the base's deny-then-ask. The guard's creation record is read
    before this answer, so it asks again only while no creation has run. A
    later `automation` press gives the press back."""
```

Needs a fix: yes — 🔴 1 (a commit found in another repository reads silent beside 500 nested substitutions, below the base); 🟡 2, 🟡 3 and 🟡 4 are each fix or justify

Loses a record or crashes: yes — 🔴 1 reads a commit silent that `3911a8cf` stopped, and bash lands it in the unjudged repository

## Proof

Files opened this round, in the clone at `567069b6` unless noted:

- `seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/rounds/round-1.md`
  and `round-1-report.md`, in the orchestrator's tree
- The diff `3006eb85..567069b6`: all of `hooks/` and `tests/`, and
  `docs/`, `seal/specs/…/changelog.md`, `phases/phase-4.md`,
  `phases/phase-5.md`, `survivors.md`, `seal/ledger.md`,
  `seal/ledger/1790644505-….md`, `seal/releases/0.15.5.md` and `0.15.6.md`
- `hooks/commit-review-gate.py`: `_hides_a_commit`,
  `_string_hides_a_commit`, `_eval_argument`, `_eval_hides_a_commit`,
  `_unresolved_base`, `commit_invocations`, `commit_targets`,
  `is_git_commit`, `automation_pressed`, `main`
- `hooks/cmdline.py`: `RUNNERS`, `SHELLS`, `STRING_HOSTS`, `command_word`,
  `_hands_a_string`, `reparsed_texts`, `VALUED`, `command_strings`,
  `names_an_unknown_command`
- `hooks/worktree_consent.py`: `granted`, `leading_phrase`, `transcript_for`,
  `_routing_preset`, `_routing_answer`, `automation_answered`, `consent`;
  `hooks/worktree-guard.py` at its two `consent` call sites
- `docs/worktree-guard-spec.md` §*Creation consent*, items 1–5 and the
  paragraph after them; `docs/commit-review-gate-spec.md:281`–`329`
- `tests/test_no_shape_the_base_stops_reads_silent.py`;
  `tests/conftest.py#declare_routing`;
  `tests/test_the_guard_asks_once_per_session.py`: `ask_entries`,
  `write_transcript`; `bin/test`

The three clones, the probe scripts, the trial fixes and the scratch outputs
were removed after the round. Nothing was written in the orchestrator's tree
except this report.

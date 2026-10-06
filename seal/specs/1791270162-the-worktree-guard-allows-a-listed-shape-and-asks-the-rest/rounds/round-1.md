# 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest — review round 1

| Field | Value |
|---|---|
| Target SHA | edd35c56f4730cbd7b7266b10ac287c5d138cd7f |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #850 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1, 🔴 2, 🔴 3, 🟡 4 and 🟡 5: a switch beside the stop's ask is approved past an ACTIVE tree, a closed descriptor hides `worktree add` and `stash branch`, `git rebase <upstream> <branch>` switches silently, a broken reader leaves an `&`-cut group silent, and a string's `-C` is neither read nor named |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of #826's review run, at edd35c56, the head of draft PR #850, with `origin/release/v0.20.0` (86cbd9a2) merged in. The reviewer was asked to judge spec compliance and then quality over `origin/release/v0.20.0...HEAD`. It also judged what the smith left open:
- `_finding_tree`'s `-C` against #689's containment;
- `LEAVES_THE_TREE`'s claim that each listed subcommand leaves the branch where it is, run against git where that is cheap;
- whether phase 3's three fixed silences close their class;
- the 48 retired or rewritten cases;
- the edits to #841's fragment and records;
- P5 against `docs/worktree-guard-spec.md` §A row 1;
- every workflow of `gh pr checks 850`.

It did not run the full suite. Before the round, the smith's narrow checks were the five guard modules (363 passed), `bin/evidence-check --strict .` (exit 0) and `survivor-check` over the range (exit 0).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | the stop's `ask` runs a switch on the same line that the ladder never judged, so one approval switches a tree another session is ACTIVE in | `hooks/worktree-guard.py:2699` | open | executed: four commands `ask` at HEAD where the base denied; `spec.md` In 2's "a stop there stops the whole line" holds only for a `deny` |
| 🔴 2 | `_plain_words` reads `>&-`, `<&-` and `2>&-` as taking the next word, so `git worktree 2>&- add …` and `git stash 2>&- branch x` are listed | `hooks/worktree-guard.py:2161` | open | executed: silent in dirty and ACTIVE trees where the base asked; bash creates the worktree |
| 🔴 3 | `rebase` is listed, and `git rebase <upstream> <branch>` switches HEAD to `<branch>` | `hooks/worktree-guard.py:2086` | open | executed against git 2.50.1: three forms move HEAD; the build is silent in an ACTIVE tree |
| 🟡 4 | `_merged_findings` returns no finding when the reader is missing or raises, against the policy's "never a silence" | `hooks/worktree-guard.py:2321` | open | executed: three silent rows in a dirty tree |
| 🟡 5 | a string's `-C` is judged in the typed-from tree, and no sentence names it | `hooks/worktree-guard.py:2397` | open | executed: `sh -c 'git -C W switch feature/x'` silent with `W` dirty; not a regression |
| ⬜ 6 | the module comment says the wider reader never picks the tree | `hooks/worktree-guard.py:157` | open | read: `_finding_tree` composes its `-C` |
| ⬜ 7 | `git branch -m` leaves HEAD on a different name, against `spec.md`'s literal definition | `hooks/worktree-guard.py:2056` | open | executed; the Premise holds, so a comment only |
| 🟢 | `_finding_tree` reads past the frozen walk only for a segment it reads no git in, one `-C` per finding, judged in that finding's own tree | `hooks/worktree-guard.py:2397` | confirmed | read; no slot is shared, so #689's ordering failure cannot arise |
| 🟢 | each unrecognised shape is judged in its own tree, each directory looked up once | `hooks/worktree-guard.py:2878` | confirmed | read; executed in the two-tree rows of 🟡 5 |
| 🟢 | #841's S5 and `Re-read · D1` were removed under the ledger's REMOVED rule, and every marker sits on a line naming a name the tree no longer has | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` | confirmed | read: the rule in `docs/the-evidence-ledger.md`; each of the 28 lines checked against `git grep` |
| 🟢 | in the stop's own tree the code denies under an ACTIVE session whatever the press, as the rewritten §A says | `hooks/worktree-guard.py:2699` | confirmed | read; P5's choice stays the owner's |
| 🟢 | the body limit stands: `spec.md` In 1 grounds it, §*Known limits* names it, and the base was silent too | `docs/worktree-guard-spec.md` | confirmed | executed: `cd W && echo $(git checkout feature/x)` silent at HEAD and at the base |
| ❓ | #850's seven pytest workflows (macOS, Ubuntu, four Windows shards) | `gh pr checks 850` | ❓ out of verified scope | pending at the end of the round; the orchestrator reads them again before the next round |

## Paste-ready fixes

```python
# hooks/worktree-guard.py, stop_unrecognised: a switch elsewhere on the line
# makes the stop a deny, because approving an ask would run it past §A.
def stop_unrecognised(findings, state, pressed, before_ask=None, switch_on_line=False):
    ...
    decision = "deny" if pressed or active or switch_on_line else "ask"
    if decision == "ask" and before_ask is not None:
        before_ask()
    ending = (
        tr(
            "Re-issue the command in a plain spelling.",
            "평범한 표기로 다시 실행하세요.",
        )
        + (
            tr(
                " Run the `git switch` as a command of its own, so the "
                "branch-switch rules judge its tree.",
                " `git switch` 는 따로 실행해 브랜치 전환 규칙이 그 트리를 판단하게 하세요.",
            )
            if switch_on_line
            else ""
        )
        if decision == "deny"
        else tr(
            "Approve to run it as written, or decline and re-issue it in a plain "
            "spelling.",
            "그대로 실행하려면 승인하고, 아니면 거부한 뒤 평범한 표기로 다시 "
            "실행하세요.",
        )
    )

# hooks/worktree-guard.py, main, the call in the stop loop:
                stop_unrecognised(
                    [found[1] for found in unrecognised],
                    (active, idle, reliable, entries),
                    automation_pressed(repo_paths(cwd)[0], session_id, transcript_path),
                    before_ask=...,  # unchanged
                    switch_on_line=switch_at is not None,
                )
```
```python
# tests/test_worktree_guard.py, S9's first half becomes:
    assert decision == "deny" and STOP in reason, reason


def test_a_switch_beside_a_stop_is_not_approved_past_an_active_tree(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1, red 1. Approving the stop's ask runs every segment, so a
    switch on the line in a tree another session is ACTIVE in made the
    ACTIVE deny of §A row 1 one approval away. Asked at edd35c56."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    in_state(monkeypatch, repo, "dirty")
    monkeypatch.setattr(
        wg,
        "sessions_in_tree",
        lambda top, own="": (ACTIVE, [], True) if top.endswith("W") else ([], [], True),
    )
    for command in (
        f"git checkout f.txt && git -C {w} switch feature/x",
        f"git checkout f.txt && cd {w} && git switch feature/x",
    ):
        assert verdict(monkeypatch, capsys, repo, command)[0] == "deny", command
```
```markdown
docs/worktree-guard-spec.md §A, the two-readers paragraph, after "…because
approving runs every segment.":

A switch on the same line makes the stop a `deny` whoever is at the
keyboard, for the same reason: approving would run the switch past the rows
above, in a tree the stop's reason does not describe.
```
```python
# hooks/worktree-guard.py, _plain_words: `>&-`, `<&-` and `N>&M-` close or
# move a descriptor and take no target; `<<-` still takes its delimiter.
            skip = word[-1] in "<>&|!-" and not re.search(r"[<>]&[0-9]*-$", word)
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py, _redirections: give the
# duplicating operators their closing and moving targets too.
    for op in (o.replace("\\", "") for o in re.split(r"(?<!\\)\|", operators)):
        target = {"<<<": "word", "<<": "EOF", "<<-": "EOF"}.get(op, "/dev/null")
        targets = [target]
        if op.endswith("&"):
            targets = ["1", "-", "1-"]
        fds = [""] if op.startswith("&") else ["", "2", "{fd}"]
        pairs += [(fd + op, t) for fd in fds for t in targets]
    return pairs
# test_the_redirections_are_read_from_the_reader counts operators, not
# pairs, so it holds unchanged. Run the module after: the LISTED direction
# meets the new targets too.
```
```python
# hooks/worktree-guard.py, beside _hidden_mover:
def _rebase_names_a_branch(args) -> bool:
    """Whether a `rebase`'s words can name the branch it switches to first.

    `git rebase <upstream> <branch>` and `git rebase --root <branch>` run
    `git switch <branch>` before anything else, and HEAD stays there
    (git-rebase(1); executed on git 2.50.1, round 1 of work item 1791270162).
    Read without an option table, so an option's value counts as a word and
    the cost is a stop: `git rebase --onto main x` stops too."""
    plain = [w for w in _plain_words(args) if not w.startswith("-")]
    return len(plain) >= (1 if "--root" in args else 2)


# hooks/worktree-guard.py, _git_finding, before `if sub in LEAVES_THE_TREE:`
    if sub == "rebase" and _rebase_names_a_branch(args):
        return "unrecognised", Finding("rebase", words)


# hooks/worktree-guard.py, _described, beside the `checkout` kind:
    if kind == "rebase":
        return (
            tr(
                "a `git rebase` naming a branch, which git switches to before it "
                "rebases",
                "브랜치를 지정한 `git rebase` 로, git 은 리베이스하기 전에 그 "
                "브랜치로 전환합니다",
            ),
            tr(
                "Write `git switch <branch>` first, then `git rebase <upstream>`.",
                "먼저 `git switch <branch>` 를 실행한 뒤 `git rebase <upstream>` 을 "
                "쓰세요.",
            ),
        )


# hooks/worktree-guard.py, LEAVES_THE_TREE:
        "rebase",  # 2/2, one word at most (`_rebase_names_a_branch`); HEAD detached while it runs: a named limit
```
```python
# tests/test_worktree_guard.py
@pytest.mark.parametrize(
    "command",
    [
        "git rebase main feature/x",
        "git rebase --onto main main feature/x",
        "git rebase --root feature/x",
    ],
)
def test_a_rebase_naming_a_branch_is_unrecognised(monkeypatch, capsys, repo, command):
    """Round 1, red 3. git switches to the named branch before it rebases."""
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "ask" and "git switch <branch>` first" in reason, reason


@pytest.mark.parametrize(
    "command", ["git rebase main", "git rebase -i HEAD~3", "git rebase --continue"]
)
def test_a_rebase_of_the_current_branch_stays_listed(command):
    assert wg.shape_of(command.split()) == "listed"


def test_git_switches_before_a_rebase_naming_a_branch(repo):
    """Binds the row above to git: if this stops holding, the list may say less."""
    import subprocess

    run = lambda *a: subprocess.run(
        ["git", "-C", str(repo), *a], capture_output=True, text=True
    )
    start = run("symbolic-ref", "--short", "HEAD").stdout.strip()
    run("rebase", start, "feature/x")
    assert run("symbolic-ref", "--short", "HEAD").stdout.strip() == "feature/x"
```
```markdown
docs/worktree-guard-spec.md §A, the `listed` bullet, after "…each beside its
count,":

except a `rebase` with two words that are not options, or `--root` and one,
which names the branch git switches to before it rebases and is
unrecognised;
```
```python
# hooks/worktree-guard.py, beside _merged_findings:
def _cut_unread(items):
    """Where the reader that rejoins an `&` cut is missing or raises, a cut
    in a command holding the bare word `git` is the finding: a broken reader
    costs a stop, never a silence (§*Which tree*)."""
    cut = [i for i, (sep, _tokens) in enumerate(items) if sep == "&"]
    if cut and any(_holds_git(" ".join(t)) for _sep, t in items):
        text = " ".join(" ".join(t) for _sep, t in items)
        return [(cut[-1], Finding("unread", text))]
    return []


# hooks/worktree-guard.py, _merged_findings: both early returns
    if wide is None:
        return _cut_unread(items)
    ...
    except (Exception, SystemExit):
        return _cut_unread(items)
```
```python
# tests/test_worktree_guard.py
@pytest.mark.parametrize(
    "command", ["git worktree &>/dev/null add ../wt b", "2>&1 git switch feature/x"]
)
@pytest.mark.parametrize("broken", ["missing", "raising"])
def test_a_broken_reader_leaves_no_cut_group_silent(
    monkeypatch, capsys, repo, command, broken
):
    """Round 1, yellow 4."""
    in_state(monkeypatch, repo, "dirty")
    if broken == "missing":
        monkeypatch.setattr(wg, "wide", None)
    else:

        def boom(*_a, **_k):
            raise RuntimeError("broken reader")

        monkeypatch.setattr(wg.wide, "merged_view", boom)
    assert verdict(monkeypatch, capsys, repo, command)[0] == "ask", command
```
```markdown
docs/worktree-guard-spec.md §Known limits, after the body bullet:

- A string handed to a shell (`sh -c`, `bash -c`, `eval`) is judged in the
  tree its segment names, the one it was typed from: its own `-C` and `cd`
  are not read. `sh -c 'git -C W switch x'` with `W` dirty and the session's
  tree clean says nothing, as it did before #826. Only a git the wider
  reading reads as a segment of its own has its `-C` composed.
```
```markdown
docs/worktree-guard-spec.md §A, the paragraph "Each unrecognised shape is
judged…", the sentence "A git only the commit gate's wider reading reads is
judged in the tree its own `-C` names." becomes:

A git the commit gate's wider reading reads as a segment of its own (behind
a redirection or a zsh precommand word) is judged in the tree its own `-C`
names; a string handed to a shell is not read for one.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_the_guard_asks_once_per_session.py tests/test_guard_resolves_the_tree_it_judges.py tests/test_the_frozen_reading_never_grows.py -q` in the clone at edd35c56 | 287 passed, 1 failed. The failure was this round's own leaving: the base guard copied into `hooks/` for the probe made a third reader of the frozen module. Re-run of `tests/test_the_frozen_reading_never_grows.py` after deleting it: 3 passed |
| `uvx ruff check` on the guard and the three touched test modules | all checks passed |
| a deleted `test_tmp_*` probe loading the build and the base's `hooks/worktree-guard.py` (`git show base:…`, beside the unchanged `cmdline_base.py`, `cmdline.py`, `worktree_consent.py` and `tokens.py`), with `sessions_in_tree` stubbed per tree | the build and base verdicts quoted in 🔴 1, 🔴 2, 🔴 3, 🟡 4, 🟡 5 and the body row; 16 precommand and alias spellings agree with the base or stop where it was silent |
| a deleted `test_tmp_*` script driving git 2.50.1 and bash from Python in a scratch repository | the rebase, fd-close, `stash branch` and `branch -m` rows in the findings and the ledger facts |
| `gh pr checks 850`, twice | first read: `lint` passed, everything else pending; second read: `lint`, `ledger`, `arm-check-grammar (3.13)`, `arm-check-grammar (3.14)` and `release` passed, the seven pytest legs pending |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. Nothing is open for it until the findings above are answered |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| P5 — whether an unrecognised shape in an ACTIVE tree is denied whatever the press | `questions.md` P5, already open | the repository owner, at the pull request |

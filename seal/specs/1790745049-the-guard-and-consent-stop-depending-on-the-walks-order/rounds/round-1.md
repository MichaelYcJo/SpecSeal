# 1790745049-the-guard-and-consent-stop-depending-on-the-walks-order — review round 1

| Field | Value |
|---|---|
| Target SHA | 4bc94f0547d8317a68ef88c12bfedfd118b1482f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 691 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1, a segment only #674 reads as git displaces the one the base judged; 🟡 2, the records' unqualified equality claim |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the containment targets `4bc94f05` and the diff `542f920b..4bc94f05`. In that diff the worktree guard and the consent writer read `cmdline.base_directories`, the base thread alone, and the commit gate is unchanged. The round was asked five things:
1. Whether both consumers equal `86256492` for every command, attacked with the shapes a generator might miss. The one recognition difference named, `2>/dev/null git switch`, was to be checked as adding only asks.
2. Whether the gate is unchanged.
3. Whether any other consumer of `walk_directories` exists.
4. Whether the changed I13 guard case lost anything beyond the recorded cost.
5. Whether I's records still claim the guard judges `W`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A segment only #674's reading reads as git takes the first-of-kind slot, so the later segment `86256492` judged is skipped: deny over an ACTIVE session in `w` becomes silence, and consent files under another clone | `hooks/worktree-guard.py:2086`, `hooks/worktree_consent.py:437` | open | Executed through `main()` and bash; predates the branch (`542f920b` agrees) and contradicts M1 and the changelog's "for every one they both read as git" |
| 🟡 2 | `base_directories` unplaces `repeat N git …` and `for i (…) git …` where `86256492`'s walk placed them; M1, spec S3 and the docstring claim equality for every segment, and the recognition list names one shape of five | `hooks/cmdline.py:2617` | open | Executed: 12 of 407 commands differ in the guard's directories |
| ⬜ 3 | The guard policy says `git -C` is read the base's way; `parse_git` reads it past a redirection | `docs/worktree-guard-spec.md:559` | open | Read |
| ⬜ 4 | The changelog opens the accepted cost with "What this gives back" | `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/changelog.md:20` | open | A correction to the run's paperwork |
| ⬜ 5 | M3's grounds call the as-written flag the base-consistent one, while the base unplaced `nice -n 5 git switch` without the redirection | `hooks/cmdline.py:2617` | open | Read; S6's answer is the tree bash runs in |
| 🟢 | The commit gate's invocations and walk equal `542f920b`'s | `hooks/cmdline.py#walk_directories` | confirmed | Executed over 407 commands; the gate file is not in the diff |
| 🟢 | The consumers of the walk are the three the build enumerated | `hooks/` | confirmed | Read with `git grep` |
| 🟢 | The changed I13 guard case loses only what M2 records | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | Read; the module passes |
| 🟢 | `\|\|`, `&&`, subshells, merged view, newlines, `pushd`/`popd`, env prefixes, the cap and S6 give the base's tree | `hooks/cmdline.py#base_directories` | confirmed | Executed: 0 differences outside the recognition family · NAME NOT IN TREE |
| ❓ | The guard's Windows backslash doubling through `base_directories` | `hooks/worktree-guard.py#_tokenize_with_separators` | ❓ out of verified scope | No Windows runner here; the repository owner answers it on a Windows machine |

## Paste-ready fixes

```python
# The words in front of a command word that `86256492` did not read past and
# #674 does: zsh's three runners and its short `for`.
_WIDER_PREFIXES = frozenset({"noglob", "nocorrect", "repeat", "for", "foreach"})


def read_as_git_as_written(tokens):
    """True where `86256492`'s reader found a git invocation in TOKENS (#689).

    `parse_git` also finds one behind a redirection (`2>/dev/null git`, `git
    2>/dev/null switch`) and behind zsh's runners (#674). The worktree guard
    and the consent writer take the FIRST segment of a kind, so a segment only
    that wider reading finds must not take the place of a later one the base
    judged: `2>/dev/null git switch x; cd w && git switch y` was denied over an
    active session in `w` at `86256492` and silent at `542f920b`.
    """
    word, _unplaced = command_word(tokens)
    if not word or os.path.basename(word[0]) != "git":
        return False
    front = tokens[: len(tokens) - len(word)]
    if any(os.path.basename(t) in _WIDER_PREFIXES for t in front):
        return False
    rest = word[1:]
    at, _chdirs = _git_options(rest)
    return not redirection_width(rest, at)
```
```python
    switch_reason = None
    switch_at = cwd
    creation_at = None
    # A kind found only by the reading #674 added (`2>/dev/null git switch`)
    # is held until a segment `86256492` read as git is found, and that one
    # takes its place (#689): the base judged the later segment.
    switch_wider = creation_wider = False
    for tokens, wheres in walk_command(command, cwd):
        creates = cmdline.adds_a_worktree(tokens)
        # Nothing left to learn from a segment of a kind already found.
        # Skipping keeps the question cheap -- `classify` runs `git rev-parse`
        # for a `checkout`, so a command is now classified up to its first
        # switch-kind segment rather than up to its first verdict of any kind.
        found_already = creation_at if creates else switch_reason
        held = creation_wider if creates else switch_wider
        wider = not cmdline.read_as_git_as_written(tokens)
        if found_already is not None and (wider or not held):
            continue
        for where in wheres:
            here, target = judgeable(tokens, where, cwd)
            found = classify(tokens, here)
            if not found:
                continue
            if creates:
                creation_at, creation_wider = target, wider
            else:
                switch_reason, switch_at, switch_wider = found, target, wider
            break
        if (
            switch_reason is not None
            and creation_at is not None
            and not (switch_wider or creation_wider)
        ):
            break
```
```python
    held = ""
    for tokens, wheres in cmdline.base_directories(items, cwd):
        if not cmdline.adds_a_worktree(tokens):
            continue
        here = cwd
        for where in wheres:
            if not isinstance(where, cmdline.Unresolved):
                here = where
                break
        at = cmdline.apply_chdir(here, cmdline.parse_git(tokens)[2])
        # A creation only #674's reading finds waits for one `86256492`
        # read, which the base filed (#689), as the guard's walk does.
        if cmdline.read_as_git_as_written(tokens):
            return at
        held = held or at
    return held
```
```python
# A segment only #674's reading reads as git, in FRONT of one `86256492` read.
# The guard takes the first segment of each kind, so the wider one took the
# place of the one the base judged.
WIDER_FIRST = (
    "2>/dev/null git switch feature/x; cd w && git switch feature/x",
    "git 2>/dev/null switch feature/x; cd w && git switch feature/x",
    "nocorrect git switch feature/x; cd w && git switch feature/x",
    "repeat 1 git switch feature/x; cd w && git switch feature/x",
)


@pytest.mark.parametrize("command", WIDER_FIRST)
def test_a_segment_only_the_wider_reading_finds_does_not_take_the_base_judged_ones_place(
    monkeypatch, capsys, repo, tmp_path, command
):
    """#689. An ACTIVE session sits in `w`, and bash switches `w` (executed).
    `86256492` denied each command; `542f920b` judged the first segment in the
    session's clean tree and was silent."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    active = [(111, str(session / "w"), 1.0, 0.5, "VS Code")]
    decision, reason, top = run(
        monkeypatch, capsys, command, session, sessions=(active, [], True)
    )
    assert decision == "deny", (command, decision, reason)
    assert top and os.path.samefile(top, session / "w"), (command, top)


def test_the_consent_writer_files_the_creation_the_base_filed_behind_a_wider_one(
    repo, tmp_path
):
    """#689, the consent twin. `86256492` filed under `w`."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    acted = wg.worktree_consent.creation_directory(
        "2>/dev/null git worktree add ../wt-a; cd w && git worktree add ../wt-b",
        str(session),
    )
    assert os.path.normpath(acted) == str(session / "w"), acted
```
```text
so each segment's directories as they read them equal `86256492`'s wherever
the target's as-written reading of the command word unplaces what the base's
did (it also unplaces a runner's operand behind zsh's `noglob`, `nocorrect`
and `repeat`, and a zsh short `for`, segments the base read no git in); the
consent writer's filed directory and the guard's judged tree equal
`86256492`'s wherever `86256492` read the command's first segment of that
kind as git
```
```text
"""[(tokens, wheres)] — the directories `86256492`'s walk named, for every segment the base read a command word in the same place.
```
```text
| S3 base equality | Over a generated corpus, every segment's directories as the guard reads them equal `86256492`'s except a zsh-prefixed segment the base read no git in; the guard's judged tree and consent's filed directory equal `86256492`'s hooks wherever the base read the segment of that kind as git | … |
```

## Executed probes

| What was run | Result |
|---|---|
| Differential over 407 commands (82 heads × 5 tails, plus 12 recognition shapes), each hook set in its own process: `walk_command`, `creation_directory`, `main()` with sessions stubbed | Target against `86256492`: 12 directory, 12 consent and 71 decision differences. 113 are commands `86256492` read no git in; 5 are asks that became silent (Red 1) |
| The same, target against `542f920b` for the gate: `commit_invocations` and `walk_directories` | 0 of 407 differ |
| ACTIVE session in `w`, three commands through `main()` at three hook sets; bash running the first on a fixture copy | `86256492` deny ×3; `542f920b` and target silent, silent, deny; bash exit 0, `w` on `feature/x` |
| Fix candidate on the clone: the differential again, the ACTIVE probe, and `bin/test` on the guard-tree, no-shape and asks-once modules | 0 asks became silent; deny ×3; 160 passed |
| The 5 planted cases, `bin/test … -k`, with the fix and at the target's hooks | 5 passed; 5 failed |
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py tests/test_no_shape_the_base_stops_reads_silent.py` at the target | 85 passed, exit 0 |
| Broad gate: full suite, repository-wide lint and typecheck | not yet — nothing has run it on this branch; the sealer's spawn, after the rounds settle |

```text
session/        git init, no commits (clean)
session/w/      copy of a one-commit repo with branch feature/x; f.txt modified
session/clean/  the same copy, unmodified
O/              the same copy, outside the session
nosuch-either   never created
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the guard should place a zsh-prefixed segment rather than unplace it (Yellow 2) | the owner's 0.17.0 redesign of how the gates learn where a command acts | the repository owner |

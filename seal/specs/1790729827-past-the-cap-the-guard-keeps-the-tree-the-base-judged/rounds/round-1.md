# 1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged — review round 1

| Field | Value |
|---|---|
| Target SHA | 69ebf6e7eaac15fc6e2a5df866dbaae715c77fba |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 690 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a `cd` behind a redirection into a directory that does not exist leads, so after `;` or a newline the worktree guard is silent on the dirty tree bash stays in, before the cap and past it) |
| Loses a record or crashes | yes — 🟡 1: `cd w; 2>/dev/null cd <missing>; git worktree add ../wt` is answered with `<missing>`, where no repository exists, so `w`, where the creation ran, gets no record, where `86256492` filed it under `w` |

- [ ] Pass

## What this round was asked

Round 1 of #689 targets `69ebf6e7` and the diff `542f920b..69ebf6e7`. The diff is a one-condition change in `walk_directories`, which departs from round 3's `collapsed` flag. The round was asked three things:
1. Whether the chosen condition is right against the flag, and whether the flag handled any shape the condition does not.
2. Whether the guard falling silent past the cap, on `2>/dev/null cd O && git switch`, narrows a false ask the base made or loses a stop.
3. Whether the consent writer's 89 segments that read past an unresolved first directory are a regression against `86256492`.

The class to enumerate was every way a collapsed or unresolved walk regains a readable directory, and every consumer of `walk_directories`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a `cd` behind a redirection into a directory that does not exist is the walk's first directory and leads, so after `;` or a newline the worktree guard is silent on the dirty tree bash stays in, and the consent writer records nothing for it; `86256492` asked and filed there; before the cap since I13, and past it where round 3's flag closed it | `hooks/cmdline.py#walk_directories` | open | Executed: `cd w; 2>/dev/null cd <missing>; git switch feature/x` is silent at `542f920b` and the target and asks at `86256492`, while bash switches in `w`. Guard losses against `86256492` over 4,380 commands: 78 at `542f920b`, 36 at the target, 19 under the flag. The paste-ready clause turns the four planted cases green, and the guard, guard-asks-once and no-shape modules pass with it |
| 🟡 2 | behind an unresolved first directory, the consent writer reads through to a `cd` landing the `\|\|` skips when the base thread names no readable directory, which files `eval true; 2>/dev/null cd O \|\| git worktree add` under `O`, where `86256492` filed under the session | `hooks/worktree_consent.py#creation_directory` | deferred #686 | Executed: `O` at `542f920b`, the target and the flag, and the session at `86256492`. The plain spelling gives `O` at `86256492` too. No fix fits the order layer, because S4 needs the same read-through. Where the creation runs, `O` is missing and nothing is recorded. The build's 89 segments were not reproduced |
| ⬜ 3 | the policy sentence says a `cd` after the collapse makes the walk's first readable again, and a relative one leaves it unresolved, so the base leads | `docs/commit-review-gate-spec.md` §*Which repository* | open | Executed through the target's walk: `<cap>cd sub && git switch x` gives an unresolved first and the base leads. The behaviour is right; only the sentence is wide |
| ⬜ 4 | M1's clause says a `cd` after the collapse leads, and phase 1 says `;` and a newline into a missing directory answer the same at all four trees | `seal/ledger/1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged.md` (M1) | open | A correction. Executed: `<cap>2>/dev/null cd <missing>; ` gives `w` at `86256492` and under the flag, and the session at `542f920b` and the target |
| ⬜ 5 | I13's clause says the guard and the consent writer take W, and where W does not exist and `;` follows, the guard takes the session's tree | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` (I13) | open | A correction. Executed, the first row of yellow 1's table. Yellow 1's fix makes the clause true as written |
| 🟢 | the condition closes round 3's yellow 1 and every row it filed, with the capping prefixes and the four spellings behind `\|\|` | `hooks/cmdline.py#walk_directories` | confirmed | Executed: the 10 cases red at `542f920b` are green at the target. The hand rows `<cap>cd <missing> \|\| ` and `<cap>2>/dev/null cd <missing> \|\| ` answer `w` at `86256492`, the target and the flag, and the session at `542f920b` |
| 🟢 | the flag breaks I13 past the cap and leaves the subshell case open, as the build said | `plan.md` §*Alternatives considered* | confirmed | Executed: the flag red on the landing case and the 3 subshell cases |
| 🟢 | the commit gate's set of directories is unchanged, and only the order moves | `hooks/cmdline.py#walk_directories` | confirmed | Read: a permutation, deduplicated by one key. Executed: 0 of 4,380 commands miss a directory of `86256492`'s |
| ❓ | whether the 3 deny texts that now name a different repository first read right to a person | `hooks/commit-review-gate.py#main` | ❓ out of verified scope | Read: `stopped[0]` decides the named repository and which `already_asked` budget is spent, and the decision is unchanged. The build's corpus was deleted and the three texts were not seen. The orchestrator answers, with the three commands from the build if they can be recovered |

## Paste-ready fixes

```python
        # The base's directories go behind the walk's, since the worktree
        # guard and the consent writer take the first one -- and in front of
        # a walk whose FIRST directory it cannot name, or whose first is a
        # landing the base did not make and that is no directory on disk.
        # That first one is the shell the segment runs in: `_branches` puts
        # the running shells ahead of the skipped ones. Past `STATE_CAP`,
        # `cd /abs/Y || git switch` names Y behind the collapsed walk's
        # unresolved first (#689). And a `cd` read past its redirections
        # (I13) is landed in front of the as-written answer whether or not
        # it can succeed: `cd w; 2>/dev/null cd /abs/missing; git switch`
        # switches in `w`, and the landing led, so the guard found no
        # repository there and judged the session's own tree (round 1 of
        # 1790729827). Where the base names the same first directory the two
        # agree, and nothing is read from disk.
        lead = wheres[0] if wheres else None
        if (
            lead is not None
            and not isinstance(lead, Unresolved)
            and (lead in base_wheres or os.path.isdir(lead))
        ):
            ordered = wheres + base_wheres
        else:
            ordered = base_wheres + wheres
```
```python
FAILED_LANDINGS = {
    "in front, then a semicolon": "2>/dev/null cd {missing}; ",
    "in front, then a newline": "2>/dev/null cd {missing}\n",
}


@pytest.mark.parametrize("capped", [False, True])
@pytest.mark.parametrize("route", sorted(FAILED_LANDINGS))
def test_a_cd_past_a_redirection_that_fails_keeps_the_tree_bash_stays_in(
    monkeypatch, capsys, repo, tmp_path, route, capped
):
    """Round 1 of 1790729827, yellow 1. A `cd` read past its redirections is
    landed in front of the as-written answer (I13). Where its destination
    does not exist, bash stays in `w` and runs the switch there, but the
    landing led, so the guard found no repository in it and judged the
    session's clean tree, and the consent writer filed the creation under
    the missing path. `86256492` did not read the `cd` and asked about `w`."""
    session = _dirty_nested_session(repo, tmp_path)
    tail = FAILED_LANDINGS[route].format(missing=tmp_path / "nosuch-either")
    chain = "cd w; " + ("2>/dev/null cd nosuch; " * 9 if capped else "") + tail
    _asks_in_w_and_files_under_w(monkeypatch, capsys, session, chain)


@pytest.mark.parametrize("capped", [False, True])
def test_a_cd_past_a_redirection_that_lands_still_leads_after_a_semicolon(
    monkeypatch, capsys, repo, tmp_path, capped
):
    """Round 1 of 1790729827. What yellow 1's fix keeps: the landing exists,
    bash switches in `O`, and the guard judges `O`."""
    session = _dirty_nested_session(repo, tmp_path)
    other = tmp_path / "O"
    shutil.copytree(repo, other)
    chain = (
        "cd w; "
        + ("2>/dev/null cd nosuch; " * 9 if capped else "")
        + f"2>/dev/null cd {other}; "
    )
    _, _, top = run(monkeypatch, capsys, chain + "git switch feature/x", session)
    assert top and os.path.samefile(top, other), top
```
```markdown
the switch does not run in (#689). An absolute `cd` after the collapse makes
the walk's first directory readable again, so it leads; a relative one lands
inside the unresolved directory, and the base's thread leads. A `cd` landed
past its redirections leads where its destination is a directory, before the
cap and past it, and where it is not, the `cd` fails and the base's thread
leads (round 1 of 1790729827).
```
```python
def test_an_unresolved_first_does_not_file_a_creation_under_a_skipped_cd(tmp_path):
    """#686. The base thread names no readable directory, and the walk's
    readable one is the `cd` the `||` skips; `86256492` filed this under the
    session, and filed the plain `cd O ||` spelling under O."""
    other = tmp_path / "O"
    other.mkdir()
    command = f"eval true; 2>/dev/null cd {other} || git worktree add ../wt"
    acted = wg.worktree_consent.creation_directory(command, str(tmp_path))
    assert os.path.normpath(acted) == str(tmp_path), acted
```

## Executed probes

| What was run | Result |
|---|---|
| The two changed test modules at the target, `bin/test` in the clone | 90 passed |
| The 11 new cases, the Q7 cap case and the gate's order case against the hooks of `86256492`, `542f920b`, the target, round 3's flag and four mutants of the target, each paired with this branch's tests | `86256492` 2 red (landing, gate order). `542f920b` 11 red. Target 0. Flag 4 red (landing, 3 subshell). Walk always first 12. Base always first 1. Last directory tested 6. `wheres and` dropped 0 |
| 4,380 commands (27 by hand) through each tree's `walk_command`, `judgeable` and `classify`, `creation_directory` and `commit_invocations`, against bash's `pwd` on one fixture | Guard losses against `86256492` where bash is in the dirty tree: 78 / 36 / 19 at `542f920b` / target / flag. Consent answers wrong where `86256492` was right: 202 / 142 / 86. A base directory missing from the gate's set: 0 at every tree. Nothing raised |
| Yellow 1's clause on a clone: four failing-landing cases and two control cases, then the guard, guard-asks-once and no-shape modules | Without the clause: the four in-front and newline cases red. With the clause: those green, and every case in the three modules green. The plain and after-operand spellings stay silent, as at `86256492` |
| `walk_directories` on `<cap>` + `cd sub && …`, `cd /abs/Y && …`, `2>/dev/null cd sub && …`, `cd && …` at the target | A relative `cd` leaves the walk's first unresolved and the base leads. An absolute one and `cd` alone lead (white 3) |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, once the rounds settle, and it is not due while yellow 1 is open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Yellow 2: behind an unresolved first directory, the consent writer reads through to a `cd` landing the `\|\|` skips, and for the redirection spellings this is a regression against `86256492` by command text. `86256492` does the same for the plain spelling | #686, beside the guard's reading of an unresolved directory | the owner, who decides whether `plan.md`'s alternative D (running shells apart from skipped ones) is worth a new interface on three consumers |

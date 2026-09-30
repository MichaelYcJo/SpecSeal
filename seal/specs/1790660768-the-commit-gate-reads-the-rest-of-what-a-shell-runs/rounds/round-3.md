# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — review round 3

| Field | Value |
|---|---|
| Target SHA | e2321cc569b11ace75fb56516e8c84a51b995bf1 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 679 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (past the walk's cap, a readable directory on a skipped branch leads the base's, so the worktree guard is silent on a switch into the dirty tree `86256492` asked about, and the consent writer files the creation under the skipped `cd` target) |
| Loses a record or crashes | yes — 🟡 1: `creation_directory` files a creation behind nine failing `cd`s, a `cd` to a missing directory and an or-operator under that missing directory, so `w`, where the creation ran, gets no record. The same effect counted as yes in round 2, and it is present at `1f55007a` as well |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 closed on its one reopening. It targets `e2321cc5` and reads two ranges nobody had reviewed. The first is round 2's fixes, `6a5afede..c18d8a56`. The second is the Q7 fix, `1f55007a..e2321cc5`: a second state thread in `walk_directories` that walks as `86256492` did, so the `STATE_CAP` collapse cannot drop a base directory. The owner's standing rule answered Q7 "Keep them". The round was asked three things. First, whether no command `86256492` stops reads silent: under `[no-review]` over a parity arm, from a session that is not opted in, past the cap, in the merged view, and in the two-thread merge order and its unplace rule, including the I15 exception. Second, whether the guard and the consent writer get the tree the base judged. Third, whether the cost stays inside the 600 s hook limit. The class to enumerate was every bound and collapse in the readers, and every consumer of `walk_directories`. Round 3's open findings go to #689, a new milestone-49 work item fixed before the release.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | past `STATE_CAP`, a readable directory the collapsed walk regains on a skipped branch leads the base's, so the worktree guard judges the session's own tree and the consent writer files the creation under the `cd` target the `\|\|` skipped | `hooks/cmdline.py#walk_directories` | deferred #689 | Executed: `cd w; ` + 9 × `2>/dev/null cd nosuch; ` + `cd <missing> \|\| git switch feature/x` asks at `86256492` and is silent at `e2321cc5` while bash switches in the dirty `w`; its creation twin is filed under `<missing>`. Present at `1f55007a` too. The Q7 fix's ordering test equates "names no readable directory" with the collapse. Fixed by a first-collapse flag, executed green |
| ⬜ 2 | I15's exception list omits the zsh short loop, which the target's first reading unplaces and `86256492`'s did not | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` (I15) | deferred #689 | A correction to the run's paperwork. Executed: 617 segments outside the stated exception, none costs a stop, because the base's `parse_git` reads the first word `for` |
| ⬜ 3 | a quoted `cd` operand shaped like a redirection (`cd '>x'`) is landed at `$HOME` in front, so the guard and the consent writer take `$HOME` | `hooks/cmdline.py#walk_directories` | deferred #689 | Executed: filed under `$HOME` at the target, under `<cwd>/>x` at `86256492`. The tokens equal `cd >x`'s, where `$HOME` is right, so no fix is owed at this layer |
| ⬜ 4 | the deny for a chain past the cap names a directory no shell reached as the last one it could name | `hooks/cmdline.py#_capped` | deferred #689 | Executed: deny at both SHAs. The collapse names its first state, a landing every `cd nosuch` failed to reach |
| 🟢 | round 2's yellow 1 is closed — a `cd` with a redirection among its words lands, in front of the as-written answer | `hooks/cmdline.py#walk_directories` | confirmed | Executed: 14 added stops in the corpus, all such landings; 0 lost; round 2's guard and consent case passes |
| 🟢 | round 2's yellow 2 is closed — the second reading's unplace no longer replaces a directory the base judged | `hooks/cmdline.py#walk_directories` | confirmed | Executed: the 608 excused segments are its shape alone, and the base finds no commit in any |
| 🟢 | round 2's white 3 is closed — the `seal/ledger.md` quoted-`>` row is corrected | `seal/ledger.md` | confirmed | Executed: 1 invocation each at the target, 0 at `86256492` |
| 🟢 | round 2's white 4 is closed — the split-twice cost is recorded | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/overview.md:53` | confirmed | Read |
| 🟢 | the Q7 fix keeps every directory the base judged for the commit gate | `hooks/cmdline.py#walk_directories` | confirmed | Executed: the comparison and the `main()` corpus above; the seven Q7 cases red at `1f55007a` and green at the base and the target |

## Paste-ready fixes

```python
    base_states, base_parked = [(cwd, None)], []
    # Whether the walk's own thread has collapsed. Until it has, its
    # directories hold every one the base's thread holds, and the ones in
    # front of them are where the shell went. After it has, a readable
    # directory it regains is not that: `cd /abs/Y || git switch` past the
    # cap names Y, the one tree the switch does not run in. So from the first
    # collapse on, the base's thread leads (round 3 of 1790660768).
    collapsed = False
```
```python
        # The base's directories go behind the walk's, since the worktree
        # guard and the consent writer take the first one -- and in front of
        # a walk that names none, or that has collapsed past `STATE_CAP` at
        # any segment so far. Behind it the guard would read the session's
        # own tree, or a branch the `||` skipped, where `86256492` judged the
        # base's first directory.
        if not collapsed and any(not isinstance(w, Unresolved) for w in wheres):
            ordered = wheres + base_wheres
        else:
            ordered = base_wheres + wheres
```
```python
        carried = _dedup(carried)
        collapsed = collapsed or len(carried) + len(parked) > STATE_CAP
        states, parked = _capped(carried, parked)
```
```markdown
thread's. Where the walk names none, and on every segment after the walk
first collapses, the base's come first, and the worktree guard, which judges
the first, judges the tree the base did (question Q7 of work item
1790660768, and round 3's yellow 1: a collapsed walk regains a readable
directory on the branch a `||` skips).
```
```python
def test_a_skipped_cd_past_the_walks_cap_keeps_the_tree_the_base_judged(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 3 of 1790660768, yellow 1. Past `STATE_CAP` the walk's thread
    collapses, and `cd <missing> ||` then gives it a readable directory on the
    branch the `||` skips. That directory put the walk in front of the base's
    thread, so the guard read the collapsed walk's unresolved directory as the
    session's clean tree, and the consent writer took the skipped branch.
    bash fails every `cd` after `cd w`, so the switch runs in the dirty `w`,
    which is the tree `86256492` judged."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    missing = tmp_path / "nosuch-either"
    chain = "cd w; " + "2>/dev/null cd nosuch; " * 9 + f"cd {missing} || "
    decision, reason, _ = run(
        monkeypatch, capsys, chain + "git switch feature/x", session
    )
    assert decision == "ask", (decision, reason)
    assert "f.txt" in reason, reason
    acted = wg.worktree_consent.creation_directory(
        chain + "git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), acted
```
```markdown
… except where only the reading past redirections unplaces it and the
as-written reading found no `git` (`2>/dev/null nice -n 5 git commit`, I14),
and in zsh's short loop, which the as-written reading unplaces since round 1
of 1790660768 and `86256492`'s did not (`for i (1 2) git commit`): in both
the base read no commit
```

## Executed probes

| What was run | Result |
|---|---|
| The 7 Q7 cases (`-k cap` over the two changed modules) against the hooks of `86256492`, `1f55007a` and `e2321cc5` | 8 passed, 7 failed and 1 passed, 8 passed |
| Per-segment walk comparison, 4,036 generated commands and 68,578 segments, `86256492` against `e2321cc5`, `c18d8a56` and an uncapped `e2321cc5` | Target: 1,225 segments miss a base directory, 608 the I14/I15 shape and 617 the zsh short loop. `c18d8a56`: 17,452. Cap-caused order changes at the target: 126 for consent, 52 for the guard. With the fix: 0 and 0 |
| The guard's `main()` and `creation_directory` on the six shapes of yellow 1, at four hook trees and with the fix, and bash on each chain | The table under yellow 1 |
| The planted case for yellow 1, at four hook trees and with the fix | Red at `1f55007a` and `e2321cc5` (`('silent', '')`), green at `86256492` and with the fix |
| 1,013 commands through the commit gate's `main()` in three session kinds, at `86256492` and `e2321cc5` | 572 base stops, 0 lost, 14 added |
| The gate's reason text on four shapes, at `86256492` and `e2321cc5` | Deny on all four at both. The wording changes on three (white 4) |
| `creation_directory` on `cd '>x'`, `cd "2>x"`, `cd 'a>b'` at both SHAs | Target: `$HOME`, `$HOME`, `<cwd>/a`. Base: the quoted names |
| `commit_invocations` on round 2's white 3 shapes at both SHAs | 1 and 1 at the target, 0 and 0 at the base |
| Two mutants of the target (no reordering; the base's directories never added), over the two changed modules | 1 failed and 8 failed |
| Seven modules that consume the walk, at the target and with the fix | 897 passed and 1 failed at each. The failure is the release-comparison case, which needs a tag, and the exported tree has none. That case passed in the tagged clone at the target |
| 5,000-segment chains through `commit_invocations` at `86256492`, `e2321cc5` and with the fix | `cd x;` 2.68 / 5.44 / 4.64 s; `cd x 2>/dev/null;` 2.70 / 7.02 / 6.03 s; `2>/dev/null cd x;` 0.31 / 4.31 / 3.88 s; `cd a \|\| cd b \|\|` 0.47 / 0.66 / 0.56 s; `2>/dev/null cd x \|\|` 0.27 / 0.36 / 0.35 s; `cd x ; git commit -m x ;` 5.16 / 9.19 / 9.35 s; `2>/dev/null cd x; git commit -m x;` 0.58 / 5.74 / 6.23 s |
| The four hooks the walk feeds, parsed at the target under `/usr/bin/python3` 3.9.6 with feature version 3.9 | They parse |
| `ruff check` and `ruff format --check` on the Q7 fix's files | Not run: the runner's virtualenv carries no ruff. It is the sealer's, with the rest of the broad gate |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It belongs to the sealer, once the rounds settle, and it is not due while yellow 1 is open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/cmdline.py#walk_directories`, `hooks/cmdline.py#understood` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/cmdline.py#_is_the_program`, `hooks/cmdline.py#_segment_names_an_unknown_command` | round 1's 🔴 2 — fixed |
| round-1 | `hooks/cmdline.py#walk_directories` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/cmdline.py#_REDIRECTION` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/cmdline.py#RUNNERS` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/cmdline.py#command_strings` | round 1's 🟡 6 — fixed |
| round-1 | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/questions.md:43` | round 1's ⬜ 7 — answered |
| round-1 | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/spec.md` | round 1's ⬜ 8 — answered |
| round-1 | `hooks/cmdline.py#_behind_a_runner` | round 1's ⬜ 9 — answered |
| round-1 | `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/commit-review-gate.py#NESTING_READ` | round 1's 🟢 — confirmed |
| round-1 | `docs/worktree-guard-spec.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-6.md` | round 1's ❓ — out of verified scope |
| round-1 | `tests/test_no_shape_the_base_stops_reads_silent.py` | round 1's ❓ — out of verified scope |
| round-2 | `seal/ledger.md` | round 2's ⬜ 3 — answered |
| round-2 | `hooks/commit-review-gate.py#_reads_a_commit` | round 2's ⬜ 4 — answered |
| round-2 | `hooks/cmdline.py#_is_the_program` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline.py#unglued` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/questions.md` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The guard reads an unresolved directory as the session's own and judges only a segment's first directory. Yellow 1's silence goes through that fallback too, but it is not the finding here: `86256492` gave the guard a readable first directory in those shapes, and the target does not. Already deferred in round 2 | #686, in no milestone | the owner, who decides whether the guard asks on an unresolved directory |

# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — review round 2

| Field | Value |
|---|---|
| Target SHA | fe24f07e64353516a56888799e022587ec17159b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 633 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the phantom note's commands act on the shell's tree) and 🟡 2 (the force-staged check misses paths when the switch goes through a subdirectory, a regression from the fix) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round, at the diff of round 1's fixes (537ee12..b8c2adc). It was asked whether each round-1 verdict is closed as a class, and whether the new unit is correct. It was asked to check every other read in the switch ladder for a leftover `cwd`, to find what `eff_cwd` is per shape, to re-derive the fix pass's direction table, to test the spec sentences under execution, and to judge whether the fix pass's re-stamp of `plan.md` is a row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The phantom note's `git restore` commands carry no `-C`, so after the fix they act on the shell's tree while the note describes the switch's tree | `hooks/worktree-guard.py:2334` | open | Executed: for `git -C <B> switch` from A, the printed hint run in A unstaged A's `ign.txt` and left B's staged. Before the fix, the note and its commands concerned the same directory. No case pins either line |
| 🟡 2 | Reached through a subdirectory, the force-staged check runs `check-ignore` in that subdirectory with root-relative paths and misses the path | `hooks/worktree-guard.py:2329` | open | Executed: with an anchored `/ign.txt`, `cd <A>/sub && git switch` and `git -C <A>/sub switch` from the root named it at 537ee12 and do not at fe24f07. The session-in-`sub` shape misses it at both, and the same fix closes it |
| ⬜ 3 | The replacement text puts `~/git` and `*/git` in the first group because they are *paths once expanded*. The lexer expands neither, `parse_git` compares the unexpanded basename, and `$HOME/git` falls in the group the rule predicts wrongly | `docs/worktree-guard-spec.md:258` | open | Executed: all three tokens come back unexpanded, and `parse_git` reads each as git, so each denies without a record. The test comment at `tests/test_the_guard_asks_once_per_session.py:389` states the same false mechanism |
| ⬜ 4 | W9 cites 3,168 / 141 / 45 from a probe that is not in the tree, and its force-staged clause has to follow finding 2's fix | `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md:11` | open | The same defect this work item corrected in the 0.9.1 row *Whatever the writer would record for …*. The direction property is reproduced on my own 168 cells and the counts are not. A paperwork correction |
| 🟢 | round 1's finding 1 is closed for the decision and the listing — row 3 asks about the tree the switch acts on | `hooks/worktree-guard.py:2325` | confirmed | Executed: 12 shapes and 168 cells. No deny moved, and every ask → silent cell is a dirty session tree switching into a clean target. M16 (listing back to `cwd`) turned the new case alone red across the four guard modules; M17 (force-staged check back to `cwd`) turned the new case red. The class is not closed; see findings 1 and 2 |
| 🟢 | round 1's finding 2 is closed for the two words it named — `~/git` and `*/git` sit in the no-record deny group | `tests/test_the_guard_asks_once_per_session.py:397` | confirmed | Executed: both deny without a record, and the case pins both. The stated mechanism is ⬜ 3 |
| 🟢 | The new unit `test_the_dirty_tree_row_reads_the_tree_the_switch_is_in` is sound for what it covers | `tests/test_guard_resolves_the_tree_it_judges.py:513` | confirmed | Read and executed: the fourth cell restores the session tree to the template's `f.txt` content, so it is clean there, and each of the four cells differs at 537ee12 in my sweep. It has no subdirectory cell and no anchored pattern, which is why finding 2 passes it |
| 🟢 | The fix pass's `plan.md` edit re-stamps an existing anchor and writes no row | `seal/specs/1790550712-the-worktree-guard-judges-a-switch-after-a-creation/plan.md:231` | confirmed | Executed: with the old stamp, `evidence-check --strict` exits 2 (`DRIFTED plan.md:231`). The rule at `skills/implement/SKILL.md:553` concerns rows, and the Phases table is untouched |

## Paste-ready fixes

```python
        if phantoms:
            why = "\n".join(f"    {p} — {r}" for p, r in phantoms)
            # Porcelain names each path from the tree's root, and the shell
            # may stand anywhere: in another repository for `git -C <repo>
            # switch`, or in a subdirectory. Naming the root is what makes the
            # command act on the tree this note describes.
            at = shlex.quote(top)
            fixes = "\n".join(
                f"    git -C {at} restore --staged {shlex.quote(p)}" for p, _ in phantoms
            )
            note = tr(
                f"\nIndex-only residue invisible in the working tree:\n{why}\n"
                f"These commands clean the tree (run `git -C {at} restore <path>` "
                f"first to keep index-only content):\n{fixes}\n",
                f"\n이 중 워크트리에서는 보이지 않는 index 잔재:\n{why}\n"
                f"아래 명령으로 정리하면 트리가 clean이 됩니다 "
                f"(index에만 존재하는 내용을 살리려면 `git -C {at} restore <path>` "
                f"를 먼저 실행):\n{fixes}\n",
            )
```
```python
        # In test_the_dirty_tree_row_reads_the_tree_the_switch_is_in, inside the
        # loop, after `assert "gitignored path force-staged" in reason, reason`
        # (add `import shlex` at the top of the module):
        hint = [l.strip() for l in reason.splitlines() if "restore --staged" in l]
        assert hint and hint[0].startswith("git -C "), hint
        assert os.path.samefile(shlex.split(hint[0])[2], repo), hint
```
```python
        phantoms = phantom_entries(entries, top)
```
```python
def test_the_force_staged_check_reads_from_the_root_of_the_tree(
    monkeypatch, capsys, repo
):
    """Round 2 of work item 1790550712, finding 2. `git status --porcelain`
    names paths from the root of the tree, and `git check-ignore` reads a path
    from where it runs. Reached through a subdirectory, the check asked about
    `sub/ign.txt`, and an anchored pattern named nothing."""
    (repo / "sub").mkdir()
    (repo / ".gitignore").write_text("/ign.txt\n")
    (repo / "ign.txt").write_text("x\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-f", "ign.txt"],
        check=True,
        capture_output=True,
    )
    for command, cwd in (
        (f"cd {repo / 'sub'} && git switch feature/x", repo),
        (f"git -C {repo / 'sub'} switch feature/x", repo),
        ("git switch feature/x", repo / "sub"),
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, cwd)
        assert decision == "ask", (command, decision, reason)
        assert "gitignored path force-staged" in reason, (command, reason)
```
```markdown
like any other. One it does not read as git — a command word whose last path
component, as written and before the shell expands anything, is not `git`
(`$GIT`, `gi*`, a command substitution, a different case, a trailing slash),
or a wrapper it does not read past such as `nice` — is not a git invocation to
this guard, and it says nothing. `parse_git` expands nothing and compares that
last component, so `~/git`, `*/git` and `$HOME/git` belong to the first group.
```
```python
    # `parse_git` compares the command word's last path component as written,
    # before any expansion, so `~/git`, `*/git` and `$HOME/git` sit here and
    # not with `$GIT` below (round 1 finding 2, round 2 finding 3).
    ("none", "deny"): (
        "git",
        "/usr/bin/git",
        "sudo git",
        "VAR=1 git",
        "~/git",
        "*/git",
        "$HOME/git",
    ),
```
```markdown
Reverting either argument to `cwd` (M16 the listing, M17 the force-staged check) turned this case red. What moved against `537ee12` is what the case's four cells hold: a dirty target reached from elsewhere now asks and names its own changes, a clean target switched from a dirty shell tree is now silent, and no deny moved
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_guard_resolves_the_tree_it_judges.py` and `tests/test_the_guard_asks_once_per_session.py`, at the target | 99 passed, exit 0 |
| M16, the listing back to `tracked_changes(cwd)`, over the four guard modules | exit 1; 1 failed (the new case), 201 passed, 1 skipped |
| M17, the force-staged check back to `phantom_entries(entries, cwd)`, on the new case alone | exit 1, at the force-staged assertion; not run over the other modules |
| `bin/evidence-check . --strict` at the target | exit 0, 0 drifted |
| The same, with `plan.md:231` put back to `main@cf55137d` | exit 2, `DRIFTED plan.md:231` |
| The tree judged for each of 12 shapes, session at A | as listed under *What `eff_cwd` is per shape* |
| Direction sweep, 537ee12 against fe24f07, 168 cells | 32 silent → ask, 12 ask → silent, nothing else moved; every ask → silent is A dirty, B clean, switch into B |
| The phantom hint for `git -C <B> switch` from A, run in A | A's `ign.txt` unstaged, B's still staged |
| Anchored `/ign.txt`, four subdirectory shapes, at both SHAs | named at 537ee12 for `cd sub` and `-C sub`; named at neither for a session in `sub`; not named at fe24f07 in any of the three |
| Lexer and verdict for six command words, no record | `~/git`, `*/git` and `$HOME/git` unexpanded, read as git, and deny; `$GIT`, `gi*` and `$(which git)` silent |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: no run exists, and it belongs to the sealer after the rounds settle. It is not due, because this round leaves findings 1 and 2 open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:2319` | round 1's 🟡 1 — fixed |
| round-1 | `docs/worktree-guard-spec.md:258` | round 1's ⬜ 2 — fixed |
| round-1 | `hooks/worktree-guard.py:2053` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree_consent.py:315` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:2338` | round 1's 🟢 — confirmed |
| round-1 | `docs/worktree-guard-spec.md:245` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.1.md:144` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

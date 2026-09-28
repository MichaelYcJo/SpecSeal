# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — review round 1

| Field | Value |
|---|---|
| Target SHA | 77ad1751ada622ead45ac94391714cbb6c0e4f6c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 633 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1, the dirty-tree row reading the session directory; it predates this branch, and absorbing it here or deferring it to a new issue is the orchestrator's call |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the build, at the branch's tip after the smith's four phases. The round was asked to sweep every command shape where a creation and a switch share one command, across tree states, consent states, retry tokens and attempts, at the target and at the base. It was asked to find any cell looser than either half alone or where the two orders differ, to enumerate every copy of the corrected sentences in both languages, to feed the `isSidechain` reader malformed entries, to mutate each case the spec cites, and to run `evidence-check --strict` unscoped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The switch ladder's tracked-changes row reads `cwd`, not the switch's tree, so a dirty tree reached by `git -C` or `cd` is silent and a clean one is asked about the session tree's changes | `hooks/worktree-guard.py:2319` | open | Executed, identical at base and target. Not caused by this branch; the unit is one it edited, and `spec.md` decision 2's last row says each half is judged against its own tree |
| ⬜ 2 | *an expansion* is filed under the no-consent silent group, but `~/git` and `*/git` deny | `docs/worktree-guard-spec.md:258` | open | Executed: 22 command words with and without a record |
| 🟢 | #620: both orders get the same decision and reason, the combined verdict is never weaker than either half and never `allow`, and nothing is looser than the base | `hooks/worktree-guard.py:2053` | confirmed | Executed over 4410 cells at target and base; the 48 differing cells are one shape that is not the same command in two orders |
| 🟢 | #624.1: `isSidechain` must be literally `false`, and no malformed line raises | `hooks/worktree_consent.py:315` | confirmed | Executed, eight malformed shapes and seven values |
| 🟢 | #624.2 and #624.3: both openings name what was counted, both languages | `hooks/worktree-guard.py:2338` | confirmed | Read against the ladder's exits; three mutations killed |
| 🟢 | #243: the class paragraph, the property paragraph and the heredoc removal are held by the cases they cite | `docs/worktree-guard-spec.md:245` | confirmed | Executed, eleven mutations each killed by its cited case |
| 🟢 | Ledger re-read notes and anchors | `seal/releases/0.9.1.md:144` | confirmed | `bin/evidence-check --strict` exit 0; notes read against each anchor's diff |

## Paste-ready fixes

```python
    # 3) 단건이지만 추적 중인 변경이 있으면 사용자에게 확인.
    #
    # Read from the tree the switch acts on, not from where the shell started:
    # `git -C <repo> switch x` or `cd <repo> && git switch x` from elsewhere
    # carries <repo>'s changes, not the session directory's.
    entries = tracked_changes(eff_cwd)
    if entries:
        single_stream = not idle and reliable
        listing = "\n".join(f"    {xy}  {path}" for xy, path in entries)
        phantoms = phantom_entries(entries, eff_cwd)
```
```python
def test_the_dirty_tree_row_reads_the_tree_the_switch_is_in(
    monkeypatch, capsys, repo, tmp_path
):
    """The tracked-changes row asks about the tree the switch acts on. Seen
    red at 77ad175: silent from outside a repository, and an ask about the
    session tree's changes for a `-C` switch into a clean clone."""
    outside = tmp_path / "outside"
    outside.mkdir()
    other = tmp_path / "other"
    subprocess.run(["git", "clone", "-q", str(repo), str(other)], check=True)
    (repo / "f.txt").write_text("changed on purpose\n")
    for n, command in enumerate(
        (f"git -C {repo} switch feature/x", f"cd {repo} && git switch feature/x")
    ):
        decision, reason = decide(
            monkeypatch, capsys, repo, command, session_id=f"t{n}", cwd=outside
        )
        assert decision == "ask", (command, decision, reason)
        assert "f.txt" in reason, reason
    decision, reason = decide(
        monkeypatch,
        capsys,
        repo,
        f"git -C {other} switch feature/x",
        session_id="t-other",
        cwd=repo,
    )
    assert decision == "silent", (decision, reason)
```
```markdown
like any other. One it does not read as git — an expansion the lexer leaves
unexpanded (`$GIT`, `gi*`, a command substitution), a different case, a
trailing slash, a wrapper it does not read past such as `nice` — is not a git
invocation to this guard, and it says nothing. `~/git` and `*/git` are paths
once expanded, and belong to the first group.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the two guard modules, in the target clone | 159 passed, exit 0 |
| Order and strictness sweep, 58 shapes, 4410 cells, at target and at base | 0 looser than base, 0 weaker than a half, 0 `allow`; 48 order differences, all the `cd`-in-switch-half shape from outside a repository |
| Eleven single mutations over the two guard modules | 11 killed, each by the case the document cites |
| Row 3 directory probe, `-C` and `cd` switches with the dirty tree on either side | silent where §A says ask, ask about the wrong tree; identical at base |
| Command-word probe, 22 words × {no record, record} | with a record only the word `git` allows; without, `~/git` and `*/git` deny |
| Transcript reader, eight malformed shapes | none raised; none counted as consent |
| `bin/evidence-check --strict`, unscoped | exit 0, 2479 ok |
| `bin/correction-check --range 2037cf0...HEAD` | exit 0, no merge commit |
| The full suite, repository-wide lint, typecheck (the broad gate) | not yet — no run exists; it belongs to the sealer, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

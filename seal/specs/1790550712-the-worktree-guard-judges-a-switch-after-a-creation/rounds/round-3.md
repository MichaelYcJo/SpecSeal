# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — review round 3

| Field | Value |
|---|---|
| Target SHA | 04d431ddf7bfacbc41305f82856d7f2f66137c42 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 633 |
| Broad gate | c6e223a against 7a39f2f; earlier run: 963b6e0 against 7a39f2f |
| Fixes checked by | no fixes to check |
| Fix range | `d0a671669250df0cbddb7639970dd3498c60e5ba..d0a671669250df0cbddb7639970dd3498c60e5ba`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (`git worktree list` and the creation fallback's `git switch` name the shell's tree, against the spec paragraph and W10) and 🟡 2 (the worktree root unquoted in the printed `worktree add` lines, older than the work item) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round after the run's one reopening, at the diff of round 2's fixes (e6435da..1c5dc5c), and so the run's last round. It was asked whether round 2's four fixed verdicts are closed as a class, and whether the new units `git_at`, `PRINTED_COMMAND`, `printed_commands` and the two cases are correct. The inputs it was given were symlinks, case variants, submodules, nested repositories, linked worktrees and paths with spaces or quotes. It was also asked whether the printed-command enumeration is complete, and whether the grounds in `survivors.md` hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The worktree steer's `git worktree list`, and the creation ladder's detection-unusable fallback *use `git switch`*, carry no command word. From another repository they act on the shell's tree, and the spec paragraph and W10 say every printed command names the judged tree | `hooks/worktree-guard.py:2144` | deferred #643 | #643 — The run is capped at its one reopening, so this record commissions no fix. #643 carries the two commands, the round's paste-ready fix and the extended class case; ledger W10 is narrowed in the closing commit so it states only what holds; Executed: from another repository, the ACTIVE deny and both choice fallbacks print every other command with `-C <top>` and this one bare. The creation fallback's reason carries no `-C` command at all. ML left every case green, and `PRINTED_COMMAND` has no `worktree list` alternative. Inside units the run's fixes edited (the steer, W10, the spec paragraph) |
| 🟡 2 | `{wt_root}` is spliced unquoted into the eight printed `worktree add` lines while `top` beside it is quoted, so a path with a space or a quote prints a command that does not parse | `hooks/worktree-guard.py:2139` | deferred #643 | #643 — Predates the work item; same grounds, and #643 carries the `shlex.quote` fix; Executed: with the repository at a path holding a space and an apostrophe, the `fetch` line splits correctly and both `worktree add` lines fail `shlex.split`. Older than the work item and not in a unit the run's fixes created; reported because this round was asked about quoting in every printed line |
| ⬜ 3 | The class case reads four of six `git_at` call sites and only the first attempt of each choice row; its `restore` alternative never matches and would contradict its inside rule if it did | `tests/test_guard_resolves_the_tree_it_judges.py:606` | deferred #643 | #643 — The class case's reach; #643 asks for it to derive its lines from what the guard prints; Executed: MU (token row) and MI (idle fallback) reverted to bare `git` leave all 185 cases green, and both rows print `-C` today, so this is a missing pin. The paste-ready case is red under MU, MI and the target hook, and green on the fixed hook |
| ⬜ 4 | `git_at` spawns `git rev-parse` before row 1 on every switch, including the silent row that prints nothing | `hooks/worktree-guard.py:2128` | deferred #643 | #643 — Read, not measured; #643 names computing `git_at` only where a reason is printed; Read: rows 3 and 4 do not use `git`. Not measured |
| 🟢 | round 2's finding 1 is closed for the note's two commands and for the steers the fix named | `hooks/worktree-guard.py:2364` | confirmed | Executed: the note carries `-C <root>` from another repository, a subdirectory and the root; M19 turns the tracked-changes case alone red. The class remainder is 🟡 1 |
| 🟢 | round 2's finding 2 is closed as a class — the force-staged check runs at the root | `hooks/worktree-guard.py:2355` | confirmed | Executed: M18 turns the new case alone red, and fe24f07's hook turns it red. Read: no other root-relative path in the ladder runs elsewhere |
| 🟢 | round 2's finding 3 is closed — the sentence states what `parse_git` compares | `docs/worktree-guard-spec.md:258` | confirmed | Read: `hooks/cmdline.py:1837` compares the basename as written. The six-word lexer probe was not re-run |
| 🟢 | round 2's finding 4 is closed — W9 states what the committed cases hold | `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md:11` | confirmed | Read, and W9's M18 claim executed. Its claim about the cells at `77ad175` is unverified |
| 🟢 | `git_at` answers right in thirteen shell positions | `hooks/worktree-guard.py:1413` | confirmed | Executed: bare for the root, a subdirectory, two symlinks and a case variant; `-C <top>` for `.git`, a nested repository, a submodule, a linked worktree, another repository, a non-repository, a missing path and an empty `cwd` |
| 🟢 | every caller of `steer_to_switch` and `steer_to_shared` passes its own ladder's `git` | `hooks/worktree-guard.py:1707` | confirmed | Read: five call sites in the hook, none outside it; every `judge_creation` passes the session's `cwd`. Executed: the printed `-C` advice goes back through both token rows |
| 🟢 | `test_the_force_staged_check_reads_from_the_root_of_the_tree` is sound | `tests/test_guard_resolves_the_tree_it_judges.py:576` | confirmed | Executed: red under M18 and against fe24f07's hook |
| 🟢 | `survivors.md`'s exemption grounds are true | `seal/specs/1790550712-the-worktree-guard-judges-a-switch-after-a-creation/survivors.md:5` | confirmed | Executed: `survivor_check.py` over the range exits 1 without it and 0 with it; the two shared phrases are `\ngit switch` and its `-c` extension. Whether the fixture is #604's command verbatim is unverified |

## Paste-ready fixes

```python
        "Then work in that folder from a separate Claude Code session. "
        f"`{git} worktree list` shows worktrees.",
```
```python
        "그런 다음 그 폴더에서 별도의 Claude Code 세션으로 작업하세요. "
        f"worktree 목록은 `{git} worktree list`.",
```
```python
            tr(
                "Confirm if this really is concurrent work; if single-stream, cancel and "
                f"use `{git} switch`.",
                f"정말 동시 작업이면 확인해 주시고, 단건이면 취소하고 `{git} switch` 로 진행하세요.",
            ),
```
```python
    git = git_at(top, cwd)
    # Every printed line splices this path into a command, so it is quoted
    # the way `git_at` quotes `top`: unchanged for a plain path, and one shell
    # word for a path with a space or a quote in it.
    wt_root = shlex.quote(wt_root)
```
```python
PRINTED_COMMAND = re.compile(
    r"git(?P<at> -C \S+)? (fetch origin|switch -c <|switch <branch>|worktree add [^`]"
    r"|worktree list|switch`\.)"
)
```
```python
    rows = (
        ("switch", "ACTIVE", (ACTIVE, [], True)),
        ("switch", "idle", ([], idle, True)),
        ("worktree add ../wt f", "single", ([], [], True)),
        ("worktree add ../wt f", "idle", ([], idle, True)),
        ("switch", "unreliable", ([], [], False)),
        ("worktree add ../wt f", "unreliable", ([], [], False)),
        ("worktree add ../wt f  # [worktree-ok]", "token", ([], [], True)),
    )
    for n, (verb, state, sessions) in enumerate(rows):
        tail = "feature/x" if verb == "switch" else ""
        for shell in (other, repo):
            command = f"git -C {repo} {verb} {tail}".rstrip()
            # A choice row denies once per session and asks on the attempt
            # after, and the two print different commands: read both.
            for _ in range(2):
                monkeypatch.setattr(wg, "sessions_in_tree", lambda t, o="", s=sessions: s)
                monkeypatch.setattr(
                    wg,
                    "load_input",
                    lambda command=command, shell=shell, n=n: {
                        "tool_name": "Bash",
                        "session_id": f"p{n}-{shell.name}",
                        "tool_input": {"command": command},
                        "cwd": str(shell),
                    },
                )
                try:
                    wg.main()
                except SystemExit:
                    pass
                out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
                reason = out["permissionDecisionReason"]
                found = printed_commands(reason)
                assert found, (verb, state, reason)
                for m in found:
                    if shell == repo:
                        assert m.group("at") is None, (verb, state, m.group(0))
                    else:
                        assert m.group("at"), (verb, state, m.group(0))
                        assert os.path.samefile(m.group("at").split()[1], repo), m.group(0)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_worktree_guard.py` and `tests/test_the_guard_asks_once_per_session.py`, at the target | exit 0, 185 passed |
| `git_at` over thirteen shell positions, `top` the fixture repository | as listed under *The new units*: five bare, eight `-C <top>` |
| Every `git <word>` in the reasons of eight rows × three shell positions × up to two attempts | from another repository, bare: `git worktree list` (ACTIVE deny, both switch choice fallbacks), `use git switch` (creation detection-unusable fallback), and the prose mentions at `:1813`, `:1828` and the creation origin line |
| Row 3 with a force-staged anchored path, shell in another repository, a subdirectory and the root | ask each time; both `restore` lines carry `-C <root>` |
| The printed `-C` advice run back through the guard from another repository | `[shared-tree-ok]` passes both choice rows; `[worktree-ok]` reaches the creation token row |
| The judged repository at a path with a space and an apostrophe, ACTIVE deny | `fetch` line splits correctly; both `worktree add` lines fail `shlex.split` |
| M18, force-staged check back to `eff_cwd`, three modules | exit 1; the force-staged case alone red |
| M19, the note's command word back to bare `git`, three modules | exit 1; the tracked-changes case alone red |
| MU, the creation token row's `steer_to_switch()` bare, three modules | exit 0, 185 passed: survives |
| MI, the creation idle fallback's `steer_to_switch()` bare, three modules | exit 0, 185 passed: survives |
| ML, `git worktree list` given the command word, three modules | exit 0, 185 passed: nothing pins the line |
| fe24f07's hook against the target's cases, three modules | exit 1; the three new or extended cases red, 182 passed |
| Paste-ready fixes 1–2 with the paste-ready case 3 | exit 0, 185 passed. The same case on the target hook: exit 1 at `git worktree list`. Under MU and under MI: exit 1. Fixes 1–2 with the committed case: exit 0 |
| `survivor_check.py --range e6435da..1c5dc5c`, without and with `--exempt survivors.md` | exit 1 (one survivor, two shared phrases), then exit 0 |
| `bin/evidence-check . --strict` at the target | exit 0, 0 drifted |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: no run exists, and it belongs to the sealer. This round leaves 🟡 1 and 🟡 2 open, and the run is capped, so what follows is the orchestrator's filing and then the sealer's spawn |

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
| round-2 | `hooks/worktree-guard.py:2334` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/worktree-guard.py:2329` | round 2's 🟡 2 — fixed |
| round-2 | `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md:11` | round 2's ⬜ 4 — fixed |
| round-2 | `hooks/worktree-guard.py:2325` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_guard_asks_once_per_session.py:397` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_guard_resolves_the_tree_it_judges.py:513` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790550712-the-worktree-guard-judges-a-switch-after-a-creation/plan.md:231` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

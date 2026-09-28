# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — survivors

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_guard_asks_once_per_session.py` | "git worktree add ../wt-b -b fix/b feature/x\n" | `MEASURED_RUN`, the command #604's automation run wrote, kept verbatim as a fixture. It shares only the fragment `\ngit switch` with `steer_to_switch`'s lines, which round 2's fix pass changed from a literal `git` to the `git_at` command word. The fixture is a command a session ran, not advice the guard prints, so nothing in it names a tree |

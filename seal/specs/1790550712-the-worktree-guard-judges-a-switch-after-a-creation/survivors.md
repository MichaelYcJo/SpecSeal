# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — survivors

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_guard_asks_once_per_session.py` | "git worktree add ../wt-b -b fix/b feature/x\n" | `MEASURED_RUN`, the command #604's automation run wrote, kept verbatim as a fixture. It shares only the fragment `\ngit switch` with `steer_to_switch`'s lines, which round 2's fix pass changed from a literal `git` to the `git_at` command word. The fixture is a command a session ran, not advice the guard prints, so nothing in it names a tree |
| `seal/releases/0.9.1.md` | "`~/git`, `*/git`, `gi*`, `$GIT`, `` `which git` ``, `GIT`, `git/`, every wrapper and every leading assignment fall short of `allow`" | The row lists the shapes the spec's sentence also listed, and states only that each falls short of `allow`, which still holds: `~/git` and `*/git` deny without a record and are not `allow` with one. What the fix corrected was the spec's reason, *every expansion*, which grouped `~/git` and `*/git` with the silent shapes. The row names no reason and no verdict beyond *not `allow`*, so the shared phrase carries none of the removed claim |

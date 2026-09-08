# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 2273a5d |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build phase 2 only, of the plan's table: the consent record and the
`PostToolUse` arm that writes it, wired into the `post-bash` group. Record
creation consent per session per repository when a `git worktree add` actually
ran. `CONTRIBUTING.md` requires the test seen red first, so the whole test file
was written against the unfixed guard and run before anything was built.

## What this phase found

**The red baseline is 13 failed, 10 passed, and the 10 are the point.** They
are the rows this work must not move — the first creation still denying,
consent belonging to one session, the switch direction untouched, nothing on
the asking side writing the record. A file where everything went red would have
been a file with no such rows in it.

**The writer had to be its own file, and the reason is `dispatch.py` rather
than taste.** It calls every gate's `main()` with the same payload and no event
name, so one file wired to both events can only tell them apart by sniffing
`hook_event_name`. That is a harness field, and `agent-contract` §13 refuses a
defence resting on a platform guarantee — where the field were absent the
writer would silently never record, which reads as *nobody ever consented* and
costs back every prompt this work removes. A gate wired only to `PostToolUse`
needs no guarantee. The filename carries an underscore because phase 3 imports
it for the read and a hyphen is not importable.

**"Is this segment a `git worktree add`" needed a home, and it is
`cmdline.py`.** The writer asks it of a command that already ran and the guard
asks it of one it is about to judge; the guard's file cannot be imported by
name, so without a shared home the two would each spell it for themselves.
`cmdline.py`'s own docstring already claims ownership of reading a command
line, and this is the first time two gates needed the same creation test.
`classify` now delegates to it, so there is one spelling rather than two.

**The writer reads every segment where the guard reads only the first.** The
guard's `PreToolUse` walk stops at the first verdict because that is the one it
must decide; a creation anywhere in a command that ran is a creation that was
approved. `git status && git worktree add …` is the case, and it has one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The inline positional test inside `worktree-guard.py#classify`'s `worktree` branch | `hooks/cmdline.py#adds_a_worktree`, which the branch now calls |

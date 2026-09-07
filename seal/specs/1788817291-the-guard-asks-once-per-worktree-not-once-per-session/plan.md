# Implementation Plan: the guard asks once per worktree, not once per session

<!-- seal/specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

A `PostToolUse` arm records that a worktree creation actually ran, keyed by
session and clone. The `PreToolUse` guard reads that record at the top of the
creation ladder and stops asking a question the session already answered. The
first creation of a session is unchanged in every respect.

## Technical context

Existing code this builds on:

- `hooks/worktree-guard.py#guard_worktree_creation` — the creation ladder. The
  new read goes in immediately after its `if not top: return`, above the
  ACTIVE-session row, because every row below it asks a question consent has
  already answered.
- `hooks/worktree-guard.py#already_asked` — the session-scoped marker this one
  sits beside and is deliberately not merged into (`spec.md` §Data &
  interfaces).
- `hooks/worktree-guard.py#walk_command` / `#classify` / `#judgeable` — the
  command reader. Both new command questions go through it, so a creation
  written inside a quoted string or a heredoc is read here exactly as the
  guard already reads it.
- `hooks/optin.py#git_common_dir` — the clone's git directory, already
  resolved once in this tree with the `.git`-is-a-file case handled.
- `hooks/session-lease.py` — the shape a `PostToolUse` writer takes here:
  basename the session id, write under the git directory, fail silently.
- `hooks/dispatch.py#GROUPS` — where a gate is wired to an event.

**Constraint that decides the file layout.** `dispatch.py` calls every gate's
`main()` with the same payload and no event name, so a single file wired to
both `PreToolUse` and `PostToolUse` would have to tell the two apart by
sniffing the payload. `hook_event_name` is a harness field, and
`skills/agent-contract/SKILL.md` §13 refuses a defence that rests on a
platform guarantee. A gate wired only to `PostToolUse` needs no guarantee, so
the writer is its own file.

**The failure scenario of the chosen approach, in six months.** A session id
is reused, or the harness starts reusing one across conversations. The record
then carries one conversation's answer into another, and a worktree is created
in a session where nobody agreed to worktrees. The cost is one extra worktree
folder — no tree is switched, nothing is overwritten — and it is bounded by
the clone. The alternative that avoids it is a time bound, which buys this at
the price of asking a long-running session twice, which is the failure the
work exists to remove.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Read `[worktree-ok]` as consent for the rest of the session | The token is written by whoever issues the command, so the model writes it on the first attempt and the guard is off with nobody asked — `has_token`'s docstring names exactly this | Rejected. It is the thing the ticket says cannot be done |
| Record consent when `PreToolUse` returns `ask` | The record would mean *the question was put*, not *it was answered*. A session that declined every prompt would still hold consent | Rejected. This is also why the record is a third directory rather than a value in the choice marker |
| Keep `ask` at every creation and let the user allowlist `Bash(git worktree add:*)` | Moves the cost out of the repository and into a settings file the plugin does not ship, and the guard's own `ask` overrides an allowlist anyway | Rejected. A fix that needs a settings change is not a fix in this repository's source |
| Return silence instead of `allow` for a consented creation | Silence is the guard having no opinion, so the harness's own permission question stands. Measured on this machine: `git worktree add` is not allowlisted, so every creation would still hold the run | Rejected for the Bash path, taken for the `Agent` path, where the guard's `ask` was the only prompt |
| `allow` for any command containing a creation | `permissionDecision: "allow"` covers the whole tool call, so `git worktree add ../x b && <anything>` would be allowed on the strength of a record about worktrees | Rejected. The allow is bounded to a command that is worktree creation and nothing else |
| A time-bounded record | A session outliving the bound is asked twice, which is the failure being removed, and the bound is a second thing to get wrong | Rejected. `spec.md` §Data & interfaces |
| Prune the records at 24 hours, as `session-lease.py` does | Pruning by mtime is the same time bound arriving through the back door | Rejected. The choice markers beside it are not pruned either |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The SDD ladder — this file, `spec.md`, `questions.md` | Nothing executable; the design gate reads it | |
| 2 | `hooks/worktree_consent.py` — the record, and the `PostToolUse` arm that writes it; wired into `post-bash` | `tests/test_the_guard_asks_once_per_session.py`, the writing half, each case seen red first | |
| 3 | The `PreToolUse` read in `guard_worktree_creation`, with its bounded allow | The same file, the reading half, each case seen red first | |
| 4 | The `Agent`/`Task` path sharing the record, both directions, and the `post-agent` group in `hooks.json` | The same file, the Agent half, seen red first | |
| 5 | `docs/worktree-guard-spec.md`, the module docstring, `pr-notes.md`, and the fragments | `tests/test_docs_line_wrap.py`, `tests/test_no_real_identifiers.py`, and a reading of §B against the code | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.**

## Operational impact

- **A new hook file and a new hook group.** `hooks/worktree_consent.py` joins
  the `post-bash` group, and a new `post-agent` group is added to both
  `hooks/hooks.json` and `hooks/dispatch.py`. A plugin installed before this
  release has neither, so nothing records and the guard behaves exactly as it
  does today — the change degrades to its own starting point.
- **A new directory under the git directory**,
  `<git-common-dir>/specseal-worktree-consent/`. Not committed, not
  gitignored, and never inside the working tree. It grows one empty file per
  session that created a worktree, the way `specseal-worktree-choice/` already
  does.
- **No migration.** Nothing reads a record written by an earlier version,
  because there were none.
- **No new dependency and no new environment variable.**

# review chain — behavior spec

Authority for `hooks/commit-review-gate.py` and
`hooks/review-history-guard.py`, and for the cycle contract the
`code-review` skill participates in. Update spec and code together.

## The cycle

```
changes accumulate → review runs → reviewed-HEAD mark written → commit allowed
commit moves HEAD  → mark no longer matches → next cycle starts unreviewed
```

- **Mark**: `<git-dir>/specseal-reviewed` containing the reviewed HEAD
  SHA. Written by the review orchestrator as the `code-review` skill's
  closing step. Living under `.git/` keeps it uncommitted and per-worktree
  (each worktree has its own git-dir — no cross-worktree false sharing).
- **One review per cycle**: fixes made after the review, before the commit,
  do not re-arm the gate. Re-review is the user's call.

## commit-review-gate (PreToolUse, Bash)

| Condition | Decision |
|---|---|
| not a `git commit` command | silent |
| repo has no `_ai/` directory at its root | silent — **opt-in criterion**: only repos using the preset workflow are gated; a globally installed plugin must not nag unrelated repos |
| `[no-review]` in the command | silent (explicit skip, visible in history) |
| mark exists and equals current HEAD | allow |
| otherwise | **ask** — the user approving the prompt IS the waiver; no separate bypass state to maintain |

Chosen `ask` over `deny` deliberately: the gate cannot know whether the user
already accepted the risk, and a deny with no override path forces workflow
contortions (measured on the worktree guard's earlier design).

## review-history-guard (PostToolUse, Bash)

Two branches with **opposite conditions** — the failure modes differ:

| Trigger | Condition | Reminder |
|---|---|---|
| review posted (`gh pr review/comment`, `gh api -X POST …/pulls/N/(reviews\|comments)`) | `_ai/review-history/PR-N/` **missing** | write `round-N.md` / `tests-todo.md` / `evidence-todo.md` now — the posting session is the only one that still holds its verdicts and probe results |
| review read (`gh pr view --json …comments`, `gh api …/pulls/N/(comments\|reviews)` without POST) | directory **exists** | read it before acting on inline comments — the todo lists may not be in the comments at all |

Reminder-only (PostToolUse cannot block). Same `_ai/` opt-in as the gate.

## Non-goals

- No Stop-hook turn blocking (v0.2): high false-positive cost in sessions
  that legitimately end without review; the commit gate is the hard stop.
- The gate does not verify review *quality* — only that the cycle carries a
  review mark. Quality lives in the `code-review` skill's procedure.

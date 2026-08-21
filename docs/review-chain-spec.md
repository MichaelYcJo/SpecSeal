# review chain — behavior spec

Authority for `hooks/commit-review-gate.py` and
`hooks/review-history-guard.py`, and for the cycle contract the `code-review`
and `legacy-parity` skills participate in. Update spec and code together.

## The cycle

```
changes accumulate → review runs → reviewed-HEAD mark written → commit allowed
commit moves HEAD  → mark no longer matches → next cycle starts unreviewed
```

- **Marks**: `<git-dir>/specseal-reviewed` holds the reviewed HEAD SHA,
  written by the review orchestrator as the `code-review` skill's closing
  step. In a ported repo, `<git-dir>/specseal-parity` holds the HEAD an
  actual comparison against the original was made at, written by the
  `legacy-parity` skill. Living under `.git/` keeps both uncommitted and
  per-worktree (each worktree has its own git-dir — no cross-worktree false
  sharing).
- **One review per cycle**: fixes made after the review, before the commit,
  do not re-arm the gate. Re-review is the user's call. The parity mark
  follows the same cycle rule.

## commit-review-gate (PreToolUse, Bash)

The hook carries **two independent opt-ins**. A repo may declare either, both,
or neither, and each is evaluated on its own — nesting one behind the other
would hide the parity check in every repo that has `docs/parity.md` but no
`_ai/`.

| Condition | Decision |
|---|---|
| not a `git commit` command | silent |
| neither opt-in applies | silent — a globally installed plugin must not nag unrelated repos |
| every applicable mark equals current HEAD | allow |
| otherwise | **ask**, naming every missing mark at once — the user approving the prompt IS the waiver; no separate bypass state to maintain |

### Review arm — opt-in: `_ai/` at the repo root

| Condition | Decision |
|---|---|
| `[no-review]` in the command | silent (explicit skip, visible in history) |
| `specseal-reviewed` equals current HEAD | satisfied |
| otherwise | contributes an ask |

### Parity arm — opt-in: `docs/parity.md` at the repo root

Ported behavior follows the original where policy is silent, so a commit that
changes code should carry a record that the original was consulted. Mark:
`<git-dir>/specseal-parity`, written by the `legacy-parity` skill after an
actual comparison.

| Condition | Decision |
|---|---|
| `[no-parity]` in the command | silent (explicit skip, visible in history) |
| staged change confined to `docs/`, `specs/`, `_ai/` | silent — nothing there can be compared against an original, and a gate that fires where no comparison was possible teaches people to click through it |
| `specseal-parity` equals current HEAD | satisfied |
| otherwise | contributes an ask |

The mark says a comparison was recorded, not that it was a good one. Writing
it for work nobody compared converts "nobody checked" into "someone checked
and it was fine" — the one claim the parity methodology exists to keep honest.

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

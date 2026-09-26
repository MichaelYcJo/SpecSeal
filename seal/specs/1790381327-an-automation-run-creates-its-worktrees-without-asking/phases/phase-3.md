# 1790381327-an-automation-run-creates-its-worktrees-without-asking — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 484326f3 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#8: the Agent path's two-row rule, with no `sessions_in_tree` call and a new
`ask` reason, and #8's rider removed. The `[worktree-ok]` row's first sentence
reworded. `docs/worktree-guard-spec.md` §B's Agent rows and §*Why the Agent
path ends at `ask`* rewritten, and §*Choice sites*' "Where the token is read
from" sentence re-pointed. The Agent-path cases in `tests/test_worktree_guard.py`
that pin the old steering rewritten to the new text. Verified by S4 over four
tree states, seen red against the phase-2 tree; S10 pinning both reasons in
both `LANG`s; `test_the_agent_verdict_does_not_depend_on_the_prompt` still
passing unchanged.

## What this phase found

**The code landed in `c3ae5b62`, the docs in `484326f3`.** The Agent path is
now judged in `main` and never reaches `guard_worktree_creation`. It asks
nothing about the tree: consent is silence, and anything else is one `ask`.

**Three parameters of `guard_worktree_creation` lost their only caller.**
`single_stream`, `shared_option` and `shared_steer` were set by the Agent path
alone, so each became a parameter nothing could set. They were removed, and
the single-stream row now answers `deny` directly. The frame did not name
this. It follows from routing the Agent path around the function, and the rule
that removed row 0's `ask` tail in phase 2 applies to them the same way.

**The case the frame missed.** `tests/test_worktree_guard_signals.py`'s
`test_agent_isolation_worktree_concurrent_asks` asserted that the Agent reason
lists the ACTIVE session (phase 1 recorded this). It now asserts the reverse:
the reason is the one a one-session tree gets, and it lists nobody. Its
neighbour `test_agent_isolation_worktree_single_stream_asks` kept its
assertion, and its docstring now gives the new reason for the `ask`.

**`test_the_agent_prompt_names_the_way_on_an_agent_has` still passed against
the new code before it was rewritten**, because the new reason also contains
the word `isolation` (in `isolation: "worktree"`). A case that pinned the old
steering by that word could not tell the old reason from the new one. It now
asserts that neither way the path used to steer is named, and that the
confirmation is.

**The phase-3 section of the spec needed an `Enforced by:` line outside a fold
marker.** §B has no marker, so the fold-shape check does not bind it. The line
was added anyway, as the plan asked, and the doc-wrap and fold-shape cases
still pass.

**Seen red against the phase-2 tree** (`290d3af3`'s `hooks/worktree-guard.py`):
7 of the 9 selected cases fail, namely S4 in all four states, S10, the
rewritten steering case and the rewritten concurrent case. The two that pass
are `test_agent_isolation_worktree_single_stream_asks`, which pins an `ask`
the phase-2 tree also gave, and `test_the_agent_verdict_does_not_depend_on_the_prompt`,
which the plan required to pass unchanged. Mutations on the new tree:

| Mutation | Red cases |
|---|---|
| the Agent path calls `sessions_in_tree` again | S4, all four states |
| the Agent path ignores consent | `test_the_agent_path_is_silent_after_the_automation_answer`, `test_the_agent_path_reads_the_record_a_bash_creation_wrote` |
| the `[worktree-ok]` row's old first sentence | S10 |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `main`'s `# RIDER:` on the Agent path (#8's open question) | answered in `main`'s Agent block and in `docs/worktree-guard-spec.md` §*Why the Agent path counts nothing, asks once, and reads no token* |
| the Agent `ask` reason's steer to *call the Agent again without isolation*, and the shared-tree option that said the same | none — this work's point is that the steer was wrong |
| `guard_worktree_creation`'s `single_stream`, `shared_option` and `shared_steer` parameters | none — no caller set them once the Agent path stopped calling the function |
| the `[worktree-ok]` row's *Single-stream work, but* opening, in both languages | the row's new opening, *No other Claude session is working in this tree, but* |

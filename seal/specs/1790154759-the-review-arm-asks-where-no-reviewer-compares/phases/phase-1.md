# 1790154759-the-review-arm-asks-where-no-reviewer-compares — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 98ef1daa |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Plant cases A1 and A2 in `tests/test_chain_hooks_hardening.py` beside
`test_parity_gate_ignores_document_only_commits`: an opted-in repository with
no declaration, no review mark and no waiver, and a commit carrying only
`docs/policies/note.md`, is stopped by the review arm (A1); with
`seal/parity.md` present the stop names `[no-review]` and not `[no-parity]`
(A2). Comment `touches_code` and `DOC_ROOTS` in `hooks/commit-review-gate.py`
to say the line is the parity arm's alone. Show each case red. Answer
`questions.md` Q2 (A3).

## What this phase found

**The frame holds.** Every coordinate `plan.md` §*Technical context* names was
opened at `1ee04588` and says what the plan says: the review arm's `if` in
`judge` reads no paths, the parity arm's adds `touches_code(cwd, invocations)`,
and `DOC_ROOTS` is `("docs/", "seal/")`.

**Both cases were seen red, each by its own mutation, and restored from a
saved copy of the hook:**

| Mutation | Result |
|---|---|
| `and touches_code(cwd, invocations)` added to the review arm's `if` | both new cases fail — A1 with its message, A2 because the commit passes silently |
| `and touches_code(cwd, invocations)` removed from the parity arm's condition | A2 fails (`[no-parity]` in the reason), as does the existing `test_parity_gate_ignores_document_only_commits` |

So A2 guards both halves: the review arm keeps its question, and the parity
arm keeps its silence on the same commit.

**A3 needs no case of its own (Q2).**
`tests/test_routing_is_recorded.py#test_a_declared_direct_item_commits_without_a_prompt`
already covers it. `routed` is decided before anything in `judge` reads a
path, and the review arm's condition reads none, so a docs-only variant would
pin nothing that case does not.

**The overview case was red before this phase**, as it is for every work item
whose frame lands before its memo:
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` named this
directory. `overview.md` was opened in this phase so the module the phase
verifies with is green, and phase 3 closes it.

**Executed:** `bin/test tests/test_chain_hooks_hardening.py
tests/test_gate_judges_the_repo_it_commits_to.py -q` at `98ef1daa` —
`139 passed`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |

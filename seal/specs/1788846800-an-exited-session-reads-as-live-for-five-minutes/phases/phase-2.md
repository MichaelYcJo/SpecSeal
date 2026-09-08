# 1788846800-an-exited-session-reads-as-live-for-five-minutes — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 5047209 |
| Ran by | `specseal:smith` — model unknown, the spawn prompt named none; the orchestrator fills this |

## What this phase was asked

Fix #257, added to this branch mid-work because it is the same file and the
same subsystem: with a consent record present, the Bash path answers `allow`
for a command that is nothing but worktree creation and `ask` for anything
more, where the Agent path already passes `silent` for the same shape with the
argument written beside it. Change `ask` → `silent` on the else arm.

Three bounds came with it. Do not widen the allow — `only_creates_a_worktree`'s
bound is correct and stays. #237's invariant stands: the first creation of a
session is still a question. And the ticket's *Not verified* section is the
first probe — that `silent` leaves every shape of the `d82a02c` list judged by
something; if any shape comes through unjudged, `ask` is right and #257 closes
**answered, not fixed**.

## What this phase found

**The probe holds, and `silent` is right — but the reasoning splits into a
half this repository can measure and a half it cannot.**

- **Measured here:** with `silent` in place, every shape of the `d82a02c` list
  earns no `allow` and the hook emits **nothing at all** — an empty stream, not
  a decision. Nothing is granted, so no shape is waved past the user's own
  permission settings. The eleven shapes were enumerated by construction from
  `tests/test_the_guard_asks_once_per_session.py` rather than from the
  docstring's prose, as instructed.
- **Not measurable from here:** that the harness then applies its normal
  permission flow to a call the hook declined to decide. That is harness
  behaviour, not this repository's code, and no test in this tree can execute
  it. It goes to the handover as `unverified` with the orchestrator as
  answerer. It is the only load-bearing claim under #257 that a case does not
  hold up.

**One worry ruled out by construction rather than by reading.** A compound
that both switches a branch and creates a worktree could, in principle, lose
its switch verdict to an early silent return. It cannot: `judge_creation`'s
own docstring states that *the switch ladder keeps every verdict it has; only
its ONE silent exit falls through to here*, so the switch is decided first and
`silent` on the creation arm cannot reach it.

**The mutation test caught the defect that mattered most, and it was in the
test harness rather than the guard.** Deleting the early return leaves
`respond("silent", …)` printing `permissionDecision: "silent"` — a value the
harness does not define — and **all 37 cases still passed**, because the
`decide` helper reports the same word for an empty stream as for that JSON.
The whole file could not tell a guard that withdrew from a guard that answered
with a word nobody implements. Since #257's entire argument rests on the hook
truly saying nothing, that is the load-bearing property, and it was pinned by
nothing. `test_the_silent_arm_emits_nothing_at_all` asserts the raw stream.

**On the ticket's second open decision** — whether the shared argument moves
somewhere both entry points read — it moved, to the `granted` block in
`guard_worktree_creation`. It had lived only on the Agent call site, which is
the one place a reader of the Bash path would not look.

**One thing deliberately left, and it needs a reader's eye.** With both real
callers now passing `allow` or `silent`, the `if consented == "allow"` ternary
in that block has an else branch — the *"This command does more than create a
worktree"* message — that no production path can now reach. The default
parameter is still `ask`, so it is not dead to a direct caller. Removing it
was outside the bound *"the change is `ask` → `silent` on the else arm,
nothing else"*, so it stands, and it is carried as a `# RIDER:` at the branch
itself — the home `seal/follow-up.md` names for anything tied to a coordinate,
since nobody greps a follow-up list before editing a message block.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `ask` on the Bash path's else arm | Replaced by `silent`; the behaviour a person sees is pinned by `test_a_consent_record_buys_silence_for_a_compound_not_a_second_prompt` |
| The `silent` argument's only copy, on the Agent call site | Moved into `guard_worktree_creation`'s `granted` block, where both entry points read it; the Agent site now points at it |
| Nothing else. The allow's bound, `only_creates_a_worktree`, and #237's first-creation question are untouched | pinned by `test_the_first_creation_of_a_session_is_still_a_question` and the unchanged allow cases |

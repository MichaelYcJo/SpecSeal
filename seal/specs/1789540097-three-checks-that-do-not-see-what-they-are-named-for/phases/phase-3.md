# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 7d1bf5bf |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#422 half one. Both ends of every stem in `ASKING` anchored, so `person`
matches `person`, `people` and `person's` and not `persona`, which
`agents/smith.md:127` already writes. The `user` stem stays, against the
issue's own patch, because the anchor is what stops `users` and because the
user is the party who answers. Proved by the sentence the issue measured —
`agent-contract` §10's own wording with `persona` one clause away — red
before and green after, and by *collect what a person answers* staying red.

## What this phase found

**Anchoring the back is not one change, it is two, and the second one had no
home in the ticket.** A bare `\b` at the end stops `persona` and `users` and
also stops `questions`, `asked` and `answers` — which the existing comment
says are deliberately matched. So the stems split into two groups by the
question *does the plural of this word name the party at the keyboard, or a
population?* `ASKING_INFLECTED` carries its inflections; `ASKING_BARE` is
anchored bare, because `users` is whoever installs this plugin and `humans`
is a category. Neither the issue nor `plan.md` names the split; it is what
the anchor costs, and it is written where the stems are.

**Q1 is answered `keep`, by measurement.** No `in one batch` occurrence
stands in any `agents/*.md` today — measured over the glob, five
definitions (`framer.md`, `scribe.md`, `sealer.md`, `smith.md`,
`warden.md`) — so no occurrence of `user` is within any window and keeping the
stem refuses nothing that stands. The default holds and nothing is reversed.
*The count read four until round 2; the measurement was always over the glob,
and round 1 corrected the copy in `questions.md` while this one stood.*

**The repair was itself held by nothing, and that is the shape this work item
exists to repair.** With the anchors in and the pattern local to the function,
the only thing that could go red was a planted sentence in a real definition:
nothing in the suite opened the pattern, and reverting the anchors left every
case green. That is `seal/specs/1789455558-…/overview.md`'s first rule
arriving one level up — pin the thing the production path calls. So `ASKING`,
its two stem groups and the window are module-level now, and
`test_the_asking_stems_are_anchored_at_both_ends` reads those objects rather
than a copy. **This is a unit `plan.md` does not name**, added because the
phase's own subject is a pattern and a pattern nobody opens is what the three
tickets are all about.

**And it was still held by nothing — corrected after round 1's 🔴 1, at the
fix pass.** Hoisting the patterns let a case open them, and a case that opens
a pattern is not the guard. No agent definition contains a batch phrase at
all, so the sweep's loop body never executed: the composition around those
patterns could be changed five ways with the module at exit 0, 50 passed,
while the case above went on pinning the constants. This phase applied the
rule it names to the pieces and not to the function the production path calls,
which is the rule's own subject. The repair is `batch_instructions`, in the
fix pass — the sweep calls it and a case calls the same one.

**The plants, and what they proved, in order.** Both were throwaway edits to
`agents/smith.md` beside the `persona` clause, restored from kept bytes:

| Planted sentence | Before | After |
|---|---|---|
| *…an agent's persona (open every coordinate a task names in one batch)…* | exit 1, window names `['person']` — from `persona` | exit 0 |
| *…an agent's persona. Collect in one batch everything a person has to answer.…* | exit 1, `['answer', 'person']` | exit 1, `['answer', 'person']` |

The second is what says the narrowing bought no silence.

**A case in this module was red before this phase touched it, for a reason
belonging to this work item.** `test_every_spec_directory_that_reached_the_
ladder_has_an_overview` fails while a directory holding `spec.md` and
`plan.md` has no `overview.md`, and this work item's did not. `overview.md`
is opened here rather than at phase 6 — which is where `plan.md` puts it and
where the `implement` skill does not: the memo is opened at the first
divergence, and phase 2 had already produced one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The function-local `ASKING` and `WINDOW` | module level, above the sweep, read by the sweep and by the new case |
| The front-anchor-only stem list `(question\|ask\|answer\|person\|people\|human\|user)` | `ASKING_INFLECTED` and `ASKING_BARE`, which carry the same seven stems in two groups |

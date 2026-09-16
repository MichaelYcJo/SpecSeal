# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 8cedc82c |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

A new arm in `chain_check.py`: `Planning | framer` owes `spec.md`, `plan.md`
and the framer's mark, each refused by name; a mark reading `the session`
beside a row reading `framer` refused as a disagreement; an unfilled approval
line reported and not refused; everything below the cutoff printed rather than
failed, on the mechanism the broad-gate arm already uses, with the constant set
to this work item's id. The six things it cannot see written in the module
beside it.

It also settles `questions.md` Q3: does the cutoff belong at this work item's
id or at the release that ships it?

## What this phase found

**A mark-shaped search anywhere in `spec.md` reads a spec ABOUT the mark as a
spec CARRYING one — and this repository already holds that instance.** Run
before the arm was written: `grep -rln "^Framed .*, before the build\.$"
seal/specs/*/spec.md` matches exactly one file, and it is this work item's own
spec, which quotes the template line in a fenced block, names it again in a
table of who writes what, and states it a third time as acceptance row S12. So
the first honest implementation of this arm would have passed the only work
item in the tree that has never been framed by anybody — and every later spec
would learn that quoting is enough.

The rule is therefore **the last non-empty line of the file**, not a search.
`templates/sdd-spec.md` ends with the line, a case pins that it ENDS with it
rather than merely holding it, and
`test_a_mark_that_is_only_QUOTED_does_not_count` builds exactly the three
quoting shapes the real spec uses. This is the third work item of the release
about checks that could not fail, and it is the shape the first two produced:
the repair pins the function the production path calls, and the case's own
assertion fires before any fixture guard.

**Q3 — measured, and the two candidates are the same answer.** 11 declarations
answer `Planning | framer`; 10 have ids below this work item's and one is this
work item. Nothing falls in the gap between this id and the release that will
ship it, so the two constants judge the same population and the cheaper
spelling wins — the work item id, which is the broad-gate arm's own spelling.
It is also the stricter of the two, which is the right direction for a tie.

**The frame arm is NOT gated on `strict`, and that is a departure from every
other arm in the walk.** A draft pull request is excused elsewhere because a
review still running has not reached its verdict. The frame is not still
running: it is drawn before the first edit. So a draft with no `spec.md` is
not early — it is a work item that declared a framer and then built without
one, which is the reported failure the arm exists for.
`test_the_frame_arm_is_judged_on_a_draft_too` pins it.

**The arm sits OUTSIDE both review arms, before either.** `Planning` is
independent of `Review`, so a work item can declare a framer and go straight
to the pull request, and the frame is owed either way. Putting the call inside
either branch is how one of the two answers quietly stops being judged — which
is the shape phase 5 just repaired one arm over.

**`spec.md` lists seven things the arm cannot see; `plan.md` and S20 say
six.** All seven are real, so the module carries seven and the count in the
prose is what is wrong. The case asserts the phrases rather than a number,
which is what keeps it from pinning the arithmetic instead of the disclosure.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Nothing. The arm is added beside the ones that exist, and no check, message or rule was taken out of the tree | none |

# Implementation Plan: the roll fires when it is due, and names what it knows

<!-- seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/plan.md -->

## Summary

Two changes to one script, and the second is the one that bites. Today
`main` computes `next_version(read_version())` and then rolls, unconditionally,
on every push to `main`. So a patch release closes a log opened for a minor
that has not shipped. The fix is a **condition before the roll** — is the log
that is open the log for the version this push shipped? — and a **title that
stops being a prediction**.

## Technical context

- **[read]** `roll_flow_measurement_issue.py#next_version` (`:165`) is pure
  `X.Y.Z -> X.(Y+1).0`, and its own docstring block at `:19-27` states the
  guess and calls the cost *a title a human can retitle by hand*. #155's
  second *Done when* is that this sentence stops describing the wrong-title
  case as absorbed by hand — so the docstring moves with the code.
- **[read]** `#read_version` (`:171`) reads `.claude-plugin/plugin.json`, which
  the release-preparation commit has already moved by the time this runs.
- **[read]** `#main` (`:354`) computes the next version, demands exactly one
  open issue, closes it, opens the next. There is no condition anywhere.
- **[read]** the module's docstring promises the mechanism *finds its issue by
  label and open state, never by parsing the title*. Any shape that reads the
  title contradicts that sentence, so the sentence moves or the shape does.
- **[read]** `tests/test_a_release_rolls_the_flow_measurement_issue.py` is the
  module's own suite; open it before choosing, because the shape that costs
  least is the one its fixtures already support.
- **[read]** `#open_issue` (`:326`) writes `chore: flow measurement — {version}`
  and `#issue_body` (`:270`) writes the body that links the closed log and the
  durable one.

**What breaks in six months.** A condition that reads the title makes every
future log's title load-bearing, so a person tidying a title breaks the roll
silently. A condition that reads something else needs that something to exist
at every release. Whichever is chosen, the failure to design against is **a
roll that silently does nothing** — the same class as the bug being fixed, one
step over. The exit line is what makes it visible, so it is not decoration.

## Alternatives considered

The `spec.md` fork, to be settled here with a failure scenario each — this
table is the work item's answer to #155's *Named, not chosen*, and the smith
fills it in before the first edit.

| Approach | Failure scenario | Verdict |
|---|---|---|
| Parse the version out of the open issue's title | | |
| Title by the version it rolls **from** | | |
| Predict, but only roll once the prediction is confirmed | | |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The alternatives table settled, then the condition: a roll that is not due exits 0, says so, and closes nothing. The title stops being a bare prediction. The docstring's *retitle by hand* paragraph is replaced by what the script now does | `bin/test tests/test_a_release_rolls_the_flow_measurement_issue.py -q` — new cases for the not-due exit, the due roll, the title's form and both printed lines; every existing case still green. Each new case seen red first | |
| 2 | Whatever carries the log's convention to a reader — `skills/verify/SKILL.md`'s measurement section and `docs/issues-and-milestones.md` — says what a title means now, if it changed | the modules reading those files, plus `test_docs_line_wrap` | |
| 3 | The closing set: ledger fragment, changelog fragment, `overview.md`, `docs/flow.md`'s #155 box | the modules that read them, `evidence-check`, and the orchestrator's broad gate after the rounds | |

## Operational impact

The roll runs from the release workflow on a push to `main`. After this change
a release that is not due to roll leaves both logs alone and exits 0, so the
job goes green having done nothing — which is the point, and which the printed
line has to make legible in the workflow log.

# 1788449488-measure-what-flow-finds — phase 3

<!-- seal/specs/1788449488-measure-what-flow-finds/phases/phase-3.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `1106568` |

## What this phase was asked

Close out `plan.md`'s Phase 3 row: in `docs/flow.md`, delete `## While the
flow runs` (its own text already named this as #109's job — the section's
final line read "**#109 deletes this section.**"); tick the `#121 + #119`
checkbox (merged into `release/v0.7.0` at `6bf9b5f`, confirmed by `git log
release/v0.7.0 --oneline`, but never ticked on that merge); tick this work
item's own `#109` checkbox now that phases 1 and 2 are committed on this
branch. Then the closing SDD artifacts — `changelog.md`, a ledger fragment
only if this branch's own scope earned a durable coordinate row,
`overview.md` — and narrow verification of every module the whole branch
touched, run together and fresh: the two new test modules from phases 1 and
2, plus `tests/test_release_hygiene.py` and `tests/test_docs_line_wrap.py`
as regression checks, since this phase edits `docs/flow.md` and the earlier
phases touch the same workflow family the hygiene test covers. Do not open
the pull request or spawn a reviewer — the orchestrator runs the review
chain next.

## What this phase found

**Both `docs/flow.md` checkboxes were exactly where `plan.md` said they'd
be, and ticking them needed no other edit.** `#121 + #119`'s row already
carried its own explanation of what shipped; `#109`'s row already described
this branch's own three parts in the past tense (the section was written
before the work that fulfils it, describing what #109 *would* do). Neither
line needed rewording — only the checkbox.

**The ledger gets no new row.** `.github/scripts/roll_flow_measurement_issue.py`'s
one genuinely non-obvious design decision — the retry on a zero-open reading
that a two-or-more reading never gets — is not a fact a future session would
have to re-derive by opening code: the script's own docstring (lines 35-47)
states the reasoning in full, and `tests/test_a_release_rolls_the_flow_measurement_issue.py::test_two_open_issues_fails_loudly_without_retrying`
pins the asymmetry by name. A ledger row would restate what the file and the
test name already say next to each other. The sibling work item's own
ledger (`seal/ledger/1788445862-a-phase-hands-the-next-one-a-record.md`)
carved out rows only for reasoning that lived solely in phase records rather
than in the shipped file itself (its P3) — that gap does not exist here, so
the same judgment that gave that item five rows gives this one none.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/flow.md`'s `## While the flow runs` section | `skills/verify/SKILL.md`'s "Measure the segment, and feed the flow log" section (phase 1, commit `80f26ce`) — already landed before this phase ran; this phase only removes the now-redundant original |

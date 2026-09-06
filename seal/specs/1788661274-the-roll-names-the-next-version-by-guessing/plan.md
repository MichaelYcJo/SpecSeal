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

The `spec.md` fork, settled here on 2026-09-06, before the first edit — this
table is the work item's answer to #155's *Named, not chosen*.

**The three rows are not three ways of doing one thing.** Row 1 asks *where
does the condition read the open log's version*, and it has exactly one
answer, so it is adopted whatever else is: `gh issue list --label
flow-measurement --state open --json number,title` returns a number and a
title, and the title is the only place a version exists. Rows 2 and 3 ask
*what does the new title say*, and that is the fork.

| Approach | Failure scenario | Verdict |
|---|---|---|
| Parse the version out of the open issue's title | Somebody tidies a title — a hyphen for the em dash, a word added, the version dropped — and the parse finds nothing. What the parse does then IS the design: answering *not due* stops the log forever with the workflow green, and answering *due* costs at most one roll that was not owed | **Adopted, for the condition only.** The open log's version exists nowhere else, so every condition reads the title. What is chosen with it is the direction of the unreadable case: a title this script cannot read as its own is **due**, never silent |
| Title by the version it rolls **from** — `chore: flow measurement — after 0.8.1` | The convention changes under a log that is already open. #172 is titled `chore: flow measurement — 0.9.0` and means a prediction; read as *the version this log rolled from*, `0.9.0` is a version that has not shipped, and a condition comparing versions in order would leave it never due — the stall, arriving through the migration itself | **Winner.** The scenario is answered rather than accepted: the marker the roll writes (` — after `) appears in no title written before this change, so an old title reads as *no version stated*, which row 1's direction makes always due. The first release after this change rolls #172 and the old convention retires itself |
| Predict, but only roll once the prediction is confirmed | The repository ships a version the prediction did not name and then never ships the predicted one — `0.9.0` predicted, `1.0.0` shipped. Every release after that prints *nothing due*, the log never rolls, and the workflow is green throughout | Rejected. It turns a wrong title, which cost a retitle, into a mechanism that has stopped, which costs nothing anybody notices — the failure this plan names to design against, one step over from the bug being fixed. And it fails #155's third *Done when* head-on: at the moment the roll runs `docs/branch-and-release.md` says the next number is not knowable, so a prediction cannot be made and the title has to say so instead of predicting |

**What the winner costs, stated rather than left to be found.** The shape the
existing fixtures already support is row 3: every case in
`tests/test_a_release_rolls_the_flow_measurement_issue.py` expects
`chore: flow measurement — 0.8.0` out of a `0.7.0` tree, so row 3 adds the
condition and leaves all eighteen green. Row 2 rewrites the expected title and
body in five of them, and deletes a sixth along with the function it covers —
`next_version`, which the winner has no caller for. That is a legitimate input
to the verdict and it lost to the grounding clause `spec.md` already cites: at
the moment this runs, the just-shipped version is the one thing known and the
next one is the one thing not. A cheaper set of edits does not make a guess
knowable.

**Where this leaves `spec.md`'s first acceptance scenario.** That row reads
*A patch release rolls nothing — given the open log names a version the tree
has not shipped*, and it is written in row 3's frame, where the title is a
prediction and a patch release is the case that must not fire. Under the
winner a patch release does roll, and rightly: the log it closes is named
after the version before it and holds exactly the work that patch shipped, so
closing it loses nothing. The scenario's substance — *a run that shipped no
new version closes nothing and says so* — is kept and pinned by a case; its
example is not reachable in steady operation, only through the migration above
and through a title edited by hand, and in both of those rolling is the
correct act. `phases/phase-1.md` records the divergence with both texts.

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The alternatives table settled, then the condition: a roll that is not due exits 0, says so, and closes nothing. The title stops being a bare prediction. The docstring's *retitle by hand* paragraph is replaced by what the script now does | `bin/test tests/test_a_release_rolls_the_flow_measurement_issue.py -q` — new cases for the not-due exit, the due roll, the title's form and both printed lines. Each new case seen red first. **Not every existing case stays green, and the cell said so before the fork was settled**: the winner renames what the roll writes, so five cases carry a new expected title, body or recovery version, and `test_next_version_bumps_the_minor_and_resets_the_patch` goes with the function it covers. Every one of the eighteen is accounted for in `phases/phase-1.md` — changed with the reason, or untouched | `deab74c` |
| 2 | Whatever carries the log's convention to a reader — `skills/verify/SKILL.md`'s measurement section and `docs/issues-and-milestones.md` — says what a title means now, if it changed | `bin/test tests/test_a_segment_feeds_the_flow_log.py tests/test_a_release_rolls_the_flow_measurement_issue.py tests/test_docs_line_wrap.py -q` — 74 passed, exit 0, four of them new and each seen red against `deca998` before either document was edited. The three other modules reading the skill (`test_the_handoff_before_round_one`, `test_the_chain_section_has_one_shape`, `test_a_record_says_what_ran_it`) are green as well, 69 passed, exit 0. **The title format goes only in `docs/issues-and-milestones.md`**: `seal/ledger.md`'s F5 row keeps this repository's own tracker state out of the shipped skill, and `test_the_shipped_skill_names_no_repository_specific_tracker_state` is what holds it there | `7d25e28` |
| 3 | The closing set: ledger fragment, changelog fragment, `overview.md`, `docs/flow.md`'s #155 box | `bin/test` over the nine modules that read them — `test_chain_hooks_hardening`, `test_the_set_a_work_item_always_has`, `test_unverified_rows_close`, `test_a_row_points_by_content`, `test_evidence_check`, `test_the_ledger_fragments_fold_at_release`, `test_the_changelog_is_gathered_at_release`, `test_no_real_identifiers`, `test_docs_line_wrap` — 335 passed, exit 0, with `test_every_spec_directory_that_reached_the_ladder_has_an_overview` seen red at `4695eae` first. Both `evidence-check` forms: the scoped write form stamped this work item's 19 rows, and the **unscoped** read went from 8 drifted to 1 — the six this branch drifted were re-read and re-stamped by hand, and the seventh, `templates/config.md`, is pre-existing at the base and left alone. The full suite, the repository-wide lint and the typecheck are the orchestrator's, after the rounds | `181e17b` |

## Operational impact

The roll runs from the release workflow on a push to `main`. After this change
a release that is not due to roll leaves both logs alone and exits 0, so the
job goes green having done nothing — which is the point, and which the printed
line has to make legible in the workflow log.

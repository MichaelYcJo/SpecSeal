# measure what flow finds — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/flow.md` §0.7.0, §While the flow runs (read, then deleted) ·
  `skills/verify/SKILL.md` §Measure the segment, and feed the flow log
  (phase 1) · `.github/scripts/roll_flow_measurement_issue.py` (read in
  full, phase 2) · `.github/scripts/close_issues_on_release.py`,
  `.github/workflows/close-issues-on-release.yml` · `docs/branch-and-release.md`
  §Cutting a release · `CONTRIBUTING.md` §House rules (fragment convention) ·
  `spec.md`, `plan.md`, `questions.md`, `routing.md`, `phases/phase-1.md`,
  `phases/phase-2.md` (all read in full) · `templates/sdd-phase.md`,
  `templates/sdd-overview.md`, `templates/ledger.md` · `seal/ledger/1788445862-a-phase-hands-the-next-one-a-record.md`
  (read for the row-judgment precedent this phase's own ledger decision
  follows)
· evidence: no new row in `seal/ledger/1788449488-measure-what-flow-finds.md`
  — see Not done below for the judgment
· verified: executed — `uvx --with pytest python3 -m pytest
  tests/test_a_segment_feeds_the_flow_log.py
  tests/test_a_release_rolls_the_flow_measurement_issue.py
  tests/test_release_hygiene.py tests/test_docs_line_wrap.py -q` → 49
  passed, exit 0 (48 plus the new regression test added for warden round 1's
  finding on `0d59003`, shown red against the pre-fix code before being
  fixed and shown green). Full suite, repository-wide lint, and typecheck
  are unverified by this branch — see below

## Why this work exists

Measuring a segment and logging what it found used to live only in one
operator's own memory file, retyped at the start of every session and
naming a fixed issue number that already needed correcting twice; this work
moves the instruction into `skills/verify/SKILL.md` so every session reads
it from the skill, moves its destination to a `flow-measurement`-labelled
issue instead of a number so nothing goes stale, and wires the release
workflow to close the current log and open the next one so nobody has to
remember to.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `plan.md`'s Phase 2 row describes the exactly-one-open-issue invariant as a direct fail-loud check, with no retry | Spec/plan says: read the count once, fail loudly if it is not exactly one. Code does: retry once, only on a zero reading, before treating zero as the invariant broken | Code's addition, not the plan's literal shape | Phase 1's own finding, carried forward and recorded again in phase 2: `gh issue list --label flow-measurement --state open` returned empty immediately after `gh issue edit ... --add-label flow-measurement` on that same issue, while `gh issue view` in the same breath showed the label already applied — a search-index lag, not a bug. A lag can only ever undercount, never overcount, so the retry fires on zero and never on two-or-more (`tests/test_a_release_rolls_the_flow_measurement_issue.py::test_two_open_issues_fails_loudly_without_retrying` pins that a two-open reading never calls `time.sleep`). `spec.md`'s own acceptance table already treated "exactly one open" as the invariant to enforce rather than a check that must be instantaneous after a label write, so this needed no design change — only the retry, which the plan's own phase 2 row did not spell out (phase-2.md, "What this phase found") |
| Neither `plan.md` nor the phase records said what `main` should do when the close succeeds and the following `gh issue create` fails | Original code (`0d59003`) let that failure propagate with only the `gh issue create` command's own error, naming nothing about the already-closed issue | `main` now catches that `SystemExit`, wraps it with the closed issue's number and a by-hand recovery title, then re-raises | Warden round 1 on `0d59003`: an operator debugging a red release-workflow step had to separately check whether the old issue was still open or already closed. Closing before opening is kept rather than reordered — opening first and failing there would leave two open issues, which is the reading the retry-once hardening above treats as never a lag artifact and always the invariant broken, so closing first turns every failure mode into a state with a stated by-hand fix. `.github/scripts/roll_flow_measurement_issue.py`'s own docstring now carries the same reasoning next to the code; `tests/test_a_release_rolls_the_flow_measurement_issue.py::test_close_succeeds_but_open_fails_names_both_in_the_message` pins the message shape, shown red against the pre-fix code before being shown green |

## Not verified

| Item | Who must answer |
|---|---|
| Full test suite (repository-wide), repository-wide lint, typecheck | orchestrator, broad gate — unverified by this branch per this repository's Verification Scope rule (narrow and often, broad once, after the review rounds settle) |
| Whether `roll_flow_measurement_issue.py` actually closes `#89` and opens a correctly-titled `0.8.0` issue at the real release | not observable from this branch — `spec.md`'s own acceptance table names this as executed at the actual release, not by this work item; this branch verifies the script's logic in isolation against mocked `gh` calls |
| Whether the label-lookup retry is ever exercised outside the one manual observation phase 1 made | not observable from this branch — the retry path is covered by a mocked test (`test_zero_open_issues_after_the_retry_fails_loudly`) but the real `gh` search-index lag it defends against is a live-service timing behaviour, next observable only at a real release run |

## Not done

**No new row was added to `seal/ledger/1788449488-measure-what-flow-finds.md`.**
The one design decision in this branch's own code that a future reader
might otherwise have to re-derive — the retry firing only on a zero
reading, never on two-or-more — is not left to be re-derived: the script's
own docstring (`.github/scripts/roll_flow_measurement_issue.py:35-47`)
states the reasoning in full, next to a test named for exactly that
asymmetry. The sibling work item's ledger
(`seal/ledger/1788445862-a-phase-hands-the-next-one-a-record.md`) earned
rows only where the reasoning lived solely in phase records rather than in
the shipped file — that gap does not exist here, so the same judgment that
gave that item five rows gives this one none.

`agents/smith.md`'s mutation-testing instruction naming only
`tests/__pycache__` — found not to cover `.github/scripts/__pycache__`,
where phase 2's own tests load the module under test from outside the
normally-imported tree — is filed separately as #129 rather than fixed
here: editing the plugin's own shipped contract is outside this work
item's scope (`spec.md`'s Out section forbids gate/refusal changes, and
while a mutation-testing instruction is not gate logic, it is still not
this branch's file to edit).

Everything else in `spec.md`'s Scope "In" list was built across phases
1–3; everything in its "Out" list (`hooks/*.py` refusal logic, renaming
`#89`, a runtime check on issue titles, changing what
`close_issues_on_release.py` itself does, the read-and-triage loop) was out
of scope from the start rather than within reach and set aside.

## Fed back into the spec

None. Both judgment calls this work made on its own — enforcing the
title-carries-a-version rule structurally rather than with a gate, and the
minor-bump default for "the next version" — were pre-settled in `plan.md`'s
own "Judgment recorded" section before phase 1 started, and `questions.md`
records that neither would change what a phase built if answered
differently later. The retry-on-undercount addition is recorded above as a
divergence, not fed back as an inferred spec clause: it is an
implementation-robustness detail the script's own docstring and tests
already carry, not a rule a future planner needs restated in `spec.md`.

# Implementation Plan: the roll opens the next log with no body

<!-- seal/specs/1788486395-the-roll-opens-the-next-log-with-no-body/plan.md — HOW, in
phases. This is the Design Gate's artifact. -->

## Summary

Issue #136. Two issues collect measurements in the same shape and nothing says
which one a number goes to; one of them is deleted at every release. The
distinction is **kind, not scope** — the rolling log accumulates and is
discarded, the durable ledger is maintained — and the instruction a session
actually follows names only the first.

Meanwhile the script that opens each new rolling log passes `--body ""`, so
every one is born empty, unlabelled beyond its lookup key, and with no path
back to the log it replaced.

This alters what a skill instructs every future session to do and what a
release-time script writes — the top rung of the `implement` skill's ladder —
so this plan comes before implementation, per the branch's pre-answered
routing (`smith`, `through the review chain`, `open the pull request`).

**It has a deadline.** The push that takes 0.8.0 to `main` is the same push
that runs `roll_flow_measurement_issue.py`. Anything not landed by then
applies a release late, and the 0.9.0 log is already open in the shape this
work exists to fix.

## Technical context

- `.github/scripts/roll_flow_measurement_issue.py:155` `open_issue` — twelve
  lines, `--title`, `--label LABEL`, `--body ""`. Its return value is read by
  `main:173` for the failure message. `LABEL` is at `:82`.
- The same file's docstring is where the invariant is stated, and where the
  reasoning for failing loudly on zero and on two lives. It is the grounds for
  refusing to let a session create one, and it should not be restated in the
  skill — pointed at.
- `skills/verify/SKILL.md:312-346`, `## Measure the segment, and feed the flow
  log`, between `## Seal block` and `## Counterfeits`. Its no-op sentence for
  an absent label is deliberate and stays; what changes is that *zero open with
  a history* stops being the same observation as *no label at all*.
- `tests/test_a_segment_feeds_the_flow_log.py` — seven cases reading that
  section, including `test_the_section_states_an_absent_label_is_a_no_op` and
  `test_skill_has_no_html_comments_at_all`. New prose has to keep both true.
- `tests/test_a_release_rolls_the_flow_measurement_issue.py` — seven cases with
  mocked `gh` calls; `test_one_open_issue_closes_it_and_opens_the_next:144` is
  the one that grows.
- `tests/test_the_release_check_watches_what_ships.py` classifies `.github/` as
  staying home, which is what lets the script name this repository's own
  `measurement` label and `log: measurement` milestone while the skill may not.
- `docs/issues-and-milestones.md` (PR #140) — the three milestone kinds, what a
  label answers that a milestone cannot, and the hazard. Pointed at, not
  restated; `tests/test_a_moved_rule_leaves_its_definition.py` is why.

**What breaks in six months.** The script gains two arguments whose failure is
tolerated, and a tolerated failure is one nobody notices. The mitigation is
that the failure is written into the body of the issue it just created — the
one artifact a person opens — rather than into a workflow log. If that turns
out to be unread too, the next step is failing the step, and this plan is
where the trade is recorded.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Let a session open a `flow-measurement` issue when it finds none | Two sessions finishing segments together both read zero and both create; the next release fails on two-or-more. It is also the act `version-check.py` refuses for its neighbour — a notice's job is to say, not to repair | Rejected — creation stays with the script, and a session names the broken invariant |
| Declare the durable log in `seal/config.md` | Pins an issue number into a file and makes the lookup a file read plus a `gh` call, where the rolling log's is one call | Rejected — questions.md Q1 |
| Declare it by milestone name | Milestone names are free text a repository renames at will; the plugin would depend on a string it does not control | Rejected — Q1 |
| Fail the release when the milestone cannot be set | A milestone is repo state, not code. Stopping a release over an index is disproportionate to what the script's own invariant protects | Rejected — best-effort, with the failure written where it is read |
| Fold the two issues into one | The rolling one is designed to be closed and replaced, so folding the durable half into it schedules the baselines for deletion; folding the other way gives a permanent issue an unbounded comment list | Rejected — the whole premise of #136 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The skill says which reading goes where and how a repository declares its durable log with `flow-baseline`; the zero-open case separates *never measured* from *stopped measuring*, and states that a session names it rather than repairing it | new cases in `tests/test_a_segment_feeds_the_flow_log.py` for both labels, the separation, and the refusal; the seven existing cases still green, including the no-HTML-comments one | |
| 2 | `open_issue` writes a body linking the closed issue and the durable ledger | `test_one_open_issue_closes_it_and_opens_the_next` extended, seen red before the code | |
| 3 | The same call adds `measurement` and `log: measurement`, best-effort, and a failure to set either is written into the created issue's body | a case with the milestone call failing: the issue is still created, the body says so, the run does not fail | |
| 4 | This repository's `#51` gets `flow-baseline`; the fragments | `evidence-check` on the new rows, `fold_ledger.py --version 0.8.0 --dry-run` | |

Phase 1 before 2 and 3 for the reason this repository has learned twice: the
sentence that tells somebody where the work goes lands before the mechanism
that sends them there.

## Operational impact

- **A new label, `flow-baseline`**, created in this repository and applied to
  #51. A repository that never creates it is unaffected — the skill's absent-label
  no-op covers it, which is the same shape `flow-measurement` already has.
- **No migration, no environment variable, no dependency.**
- **Failure direction: allows more.** Both new script arguments are tolerated
  on failure. That is the opposite of the branch before this one, deliberately:
  the invariant this script protects is the one-open rule, and neither argument
  touches it, so a release is not the place to stop.
- **Prompt budget: zero.** Nothing here puts a question in front of a person.
  Q1 was answered in the batch before the first edit.

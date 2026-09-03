# Feature Specification: measure what flow finds

<!-- seal/specs/1788449488-measure-what-flow-finds/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| Issue #109 (verbatim in the branch's task) | The source of truth for all three parts. Quoted in full in the branch task; not re-quoted here. |
| `docs/flow.md` §While the flow runs | The instruction being replaced. Its own text already names the destination this work builds: "Its third part — the release closes this version's log and opens the next — is what makes 0.8.0's measurement issue exist without anybody opening it." Confirms the "bump the minor, reset the patch" default this work adopts for the version a newly-opened issue names (Alternatives, `plan.md`). |
| `skills/verify/SKILL.md` | Where the instruction moves to, per issue #109 part 1 verbatim: "measuring a segment and recording what the numbers say belongs beside them [completion claims and their labels]." |
| `.github/scripts/close_issues_on_release.py`, `.github/workflows/close-issues-on-release.yml` | The release-time mechanism issue #109 part 3 extends. Read in full — see `plan.md` Technical context for what it already does and deliberately does not do. |
| `CONTRIBUTING.md` §What a change to a gate must carry | Judged NOT to apply — see Scope/Out below, mirrors the precedent set by work item `1788445862-a-phase-hands-the-next-one-a-record` (#121+#119), whose `spec.md` Grounding table made the identical call for the same reason (no refusal/gate logic added) |
| `docs/branch-and-release.md` §Cutting a release, §Work accumulates on a release branch | Where `close_issues_on_release.py` fits in the release sequence, and why it runs from a push to `main` with `plugin.json` already at the shipped version at that point — the fact this work's version arithmetic depends on |
| `seal/config.md` | No `Record language` row → English, per `implement` skill's stated default for an absent row |

## Scope

**In:**

- `skills/verify/SKILL.md` — a new section, placed between `## Seal block`
  (line 279) and `## Counterfeits` (line 312), instructing whichever session
  watched a smith or warden segment finish to measure that segment's
  transcript with `skills/verify/scripts/session_cost.py` and post what it
  found as a comment on the repository's open `flow-measurement`-labelled
  issue — **when one exists**. The instruction is unconditional prose in a
  skill every installed repository receives, so it is written to be a no-op
  wherever no such issue is open (see `plan.md` Alternatives for why this is
  the chosen shape rather than a SpecSeal-only carve-out).
- Bootstrapping the label in **this** repository so the instruction has
  something to find starting now: `gh label create flow-measurement …` and
  `gh issue edit 89 --add-label flow-measurement`, done as an explicit shell
  step in whichever phase lands the skill section, with its own verification
  (`gh issue list --label flow-measurement --state open` returns `#89` and
  only `#89`) — this is not a file `git` tracks, so §Verification below names
  it separately.
- A new script, `.github/scripts/roll_flow_measurement_issue.py`, run as an
  additional step in `.github/workflows/close-issues-on-release.yml`: on a
  push to `main`, closes the currently-open `flow-measurement`-labelled issue
  and opens the next one, titled with the version the release just shipped
  bumped to the next minor (`X.(Y+1).0`), labelled `flow-measurement`, empty
  body.
- `docs/flow.md`: delete `## While the flow runs` (its own text already
  names this as #109's job); tick the `#121 + #119` checkbox (merged into
  `release/v0.7.0` without ticking its own box); tick `#109`'s own checkbox
  once this branch's work is committed.
- New test coverage: a prose-pin test for the new `skills/verify/SKILL.md`
  section (following `tests/test_a_phase_hands_the_next_one_a_record.py`'s
  pattern — required sections outside HTML comments); tests for
  `roll_flow_measurement_issue.py`'s version arithmetic and its
  exactly-one-open-issue invariant, following `tests/test_release_hygiene.py`'s
  `monkeypatch`-on-`subprocess.run` pattern for `close_issues_on_release.py`.
- SDD closing artifacts: `changelog.md`, `seal/ledger/1788449488-….md` (if any
  row is added), `overview.md`.

**Out:**

- Any change to `hooks/*.py` or other refusal/exit-code logic. Nothing here
  blocks a commit or a branch switch — see Grounding, "gate" clause does not
  apply.
- Renaming issue #89 to carry a version in its title. The branch task is
  explicit that this is a separate, riskier act (a hundred-plus comments
  reference #89 by number) and out of scope here. #89 is grandfathered as-is
  and closed, not renamed, by `roll_flow_measurement_issue.py`.
- Any runtime check enforcing that a `flow-measurement` issue's title
  contains a version number. See Grounding and Judgment below — the rule is
  satisfied structurally (the opener script always writes one) rather than
  policed separately, matching this repository's own "level 2, not level 3"
  precedent for a behavioural convention with nothing checking it yet to
  measure a check against.
- Changing what `close_issues_on_release.py` itself does (closing issues
  named by squash-commit `Closes #N` keywords). Its own docstring scopes it
  tightly to three deliberate exclusions; the rollover is a second script,
  not a fourth exclusion bent into the first — see `plan.md` Alternatives.
- Building the "read the issue after the release and triage into a patch"
  loop. Issue #109 explicitly says this should not be built; triage stays a
  person's judgment, made once per finding, same as every other issue here.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A smith or warden segment ends in a repository with an open `flow-measurement` issue | Given the segment's transcript exists, when the watching session reaches the point `skills/verify/SKILL.md` now instructs, then it runs `session_cost.py` against that transcript and posts the result as a comment on the issue `gh issue list --label flow-measurement --state open` names, without asking whether to | Read: the section exists in `skills/verify/SKILL.md` outside HTML comments, names both commands, and states the post happens without asking (mirrors "Prompt budget: zero" language used elsewhere in this repository's SDD documents) |
| A segment ends in a repository with no such issue open (nearly every installed repository) | Given no open `flow-measurement`-labelled issue | Then the instruction is a no-op — nothing is posted, nothing fails, nothing asks | Read: the section states the lookup is a precondition, not an assumption |
| A release reaches `main` | Given `close-issues-on-release.yml` fires on the push, when `roll_flow_measurement_issue.py` runs, then it closes the one open `flow-measurement` issue and opens a new one titled with the next minor version, labelled `flow-measurement`, empty body | Read + a unit test exercising the version-bump function directly, and a `monkeypatch`-based test exercising the close/open calls against a fake `gh`, following `tests/test_release_hygiene.py`'s existing pattern for the neighbouring script |
| Zero or more-than-one `flow-measurement` issue is open at release time | Given the mechanism's own invariant ("exactly one is open at a time") is broken | Then the script fails loudly rather than guessing | Read + a test asserting the failure path, mirroring `close_issues_on_release.py`'s own "it fails loudly" convention |
| This repository specifically, at this release | Given `#89` is labelled `flow-measurement` by this work's own bootstrap step, and this branch merges into `release/v0.7.0` | Then when `release/v0.7.0` reaches `main`, `roll_flow_measurement_issue.py` closes `#89` and opens an issue titled with `0.8.0` — the exact number `docs/flow.md` already names as the expected next measurement issue | Executed at the actual release, not by this work item — named here as the acceptance the mechanism exists to satisfy; this work item verifies the script's logic in isolation, not the real release event |
| `docs/flow.md` after this work merges | Given the file today | Then `## While the flow runs` is gone, the `#121 + #119` line is ticked, and the `#109` line is ticked | Read, at the closing phase, after both other checkboxes' preconditions are true |

## Data & interfaces

No schema or payload change. Two new interfaces:

- `skills/verify/SKILL.md`'s new section — prose read by an agent, not
  parsed by any checker. No field name is fixed by any test other than the
  new pin test this work adds.
- `.github/scripts/roll_flow_measurement_issue.py` — a script, invoked with
  no arguments beyond the environment the workflow already sets
  (`REPO`, `GH_TOKEN`, and `AFTER`/plugin.json on disk after checkout — the
  exact inputs are `plan.md`'s to fix, since they follow directly from
  `close_issues_on_release.py`'s existing environment contract in the same
  workflow file).

## Open questions → questions.md

None new. The one judgment call this work makes on its own — the "carries a
version in its title" enforcement question the branch task explicitly hands
to the framer — is recorded as a decision in `questions.md`, not left open,
because the branch task already supplies enough constraint (structural
satisfaction vs. a separate check) that a different answer would not change
what phase 2 builds.

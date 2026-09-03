# Implementation Plan: measure what flow finds

<!-- seal/specs/1788449488-measure-what-flow-finds/plan.md — HOW, in phases.
This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

## Summary

Issue #109: the instruction "measure every smith/warden segment and log what
it found" lives only in a person's message, retyped every session, naming
three issue numbers of which two are already stale. It moves into
`skills/verify/SKILL.md` (so a session does it because the skill says so);
its destination becomes a `flow-measurement`-labelled GitHub issue instead of
a hardcoded number (so nothing goes stale); and the release workflow closes
the current one and opens the next when a release ships (so nobody has to
remember). Triage of what a measurement finds stays a human judgment, made
once per finding — issue #109 is explicit that automating that step is the
wrong next step, and #89's own log is the evidence for why.

This changes what a skill instructs every future session to do and what a
release-automation script does — the top rung of the `implement` skill's
ladder (a skill's instructions, a script's behaviour a person relies on) — so
`spec.md` and this plan come before implementation, per this branch's
pre-answered routing (`through the review chain`, `open the pull request`,
`smith`, into `release/v0.7.0`).

## Technical context

- `skills/verify/SKILL.md:279` (`## Seal block`) to `:312` (`## Counterfeits
  (stop on sight)`) — the new section is inserted between them. The seal
  block already carries a `cost` row computed from `session_cost.py`
  (`:279-310`), so the new section continues an existing pattern rather than
  introducing a new tool.
- `skills/verify/scripts/session_cost.py` — already reads a transcript and
  splits command time / model time / repeats. Nothing here changes; the new
  section only names it as the command to run per segment.
- `~/.claude/projects/-Users-yc-Documents-GitHub-SpecSeal/memory/measure-every-segment-to-89.md`
  — the standing-rule memory file this instruction has lived in until now.
  Read for its exact mechanics (subagent transcript path, "split at the
  coordinator sent a message lines" for a resumed segment, post via
  `gh issue comment <n> --body-file`) — this work carries those mechanics
  into the skill; the memory file itself is the orchestrator's own artifact
  and out of this branch's scope to edit.
- `.github/scripts/close_issues_on_release.py` (212 lines) — read in full.
  Its docstring states three things it "deliberately does not do"; the
  rollover this work adds is not a fourth exception bent into this file, it
  is a separate script with its own scope (see Alternatives).
- `.github/scripts/gather_changelog.py` and `.github/scripts/fold_ledger.py`
  — the existing precedent for "two scripts, one release-time concern each,
  wired into the same step" (`docs/branch-and-release.md` §"The release
  branch merges into `main`… carrying one commit of its own"). The new
  script follows their CLI shape where useful: a plain `main()`, loud
  failure via `sys.exit(...)`, no silent fallback.
- `.github/workflows/close-issues-on-release.yml` — triggers on `push:
  branches: [main]`, already checks out with `fetch-depth: 0`, already sets
  `GH_TOKEN`, `REPO`. The new script runs as a second step in this same
  workflow (same trigger — a release reaching `main` — satisfies issue
  #109's "the release opens the next one" without needing a second
  workflow file).
- `.claude-plugin/plugin.json` — read for the version. At the point this
  workflow runs, the release-preparation commit (which moved the version)
  has already merged into `main` as part of the same push, so the checked-out
  tree already carries the shipped version. This is the fact the version
  arithmetic depends on, and it is already true of the workflow's existing
  step (`close_issues_on_release.py` runs against the same checkout).
- `docs/flow.md:22-23` — the two lines naming #109 and #89; `:9-27`
  (`## 0.7.0`) — the section whose "While the flow runs" subsection
  (below `:27`, exact lines to re-read at phase 3 since phase 1/2 do not
  touch this file) this work deletes, per the file's own text at that
  location: "**#109 deletes this section.**"
- `docs/flow.md:21` — the `#121 + #119` line, unticked despite having merged
  (confirmed: `git log` shows `6bf9b5f` "…(#121, #119) (#128)" already on
  this branch's base).
- `tests/test_release_hygiene.py:225-355` — the existing `monkeypatch`-based
  test pattern for `close_issues_on_release.py` (mocking `subprocess.run`
  rather than hitting the network). The new script's tests follow the same
  pattern in their own file.
- `tests/test_a_phase_hands_the_next_one_a_record.py` — the pattern for
  pinning a new prose section: required headings exist outside HTML
  comments, each holding a placeholder rather than a filled claim where the
  source is a template; here the source is a skill section, so the pin is
  closer to `tests/test_review_axes.py`'s substring-pin shape.
- `seal/follow-up.md` — read in full. Its one open row (bringing
  `agents/smith.md`/`agents/scribe.md` under the line-wrap check) is
  unrelated to this work.
- `seal/parity.md` — absent. No migration config; `legacy-parity` does not
  apply.

**What breaks in six months if this is built wrong.** A skill instruction
that names a specific issue number ages exactly like the message it replaces
— which is the defect #109 exists to fix — so the new section must name a
label and a lookup command, never a number, and must be a no-op where the
label is absent rather than failing or asking. A release script that hard-
codes "the next version is always +1 minor" without a documented fallback for
the day this repository ships a patch release first will guess wrong exactly
once and nobody will notice until the log has two open issues or a title that
no longer matches reality — which is why the script fails loudly rather than
guessing when the "exactly one open" invariant does not hold, instead of
silently creating a second one.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Fold the rollover into `close_issues_on_release.py` itself | That file's docstring already lists three things it deliberately excludes, each argued from a real incident specific to the `Closes #N` keyword problem. Adding a fourth, unrelated concern (label-based issue rollover) to the same file mixes two release-time mechanisms that change for different reasons and complicates its next targeted edit | rejected — a second script, run as a second step in the same workflow, keeps `close_issues_on_release.py`'s scope exactly what its docstring already claims |
| Ship `skills/verify/SKILL.md`'s new section unconditionally, always posting somewhere (e.g. to the newest open issue, any label) | Every one of this plugin's installed repositories would have a session try to comment on an arbitrary issue after every segment — noise in every consumer's tracker, and a wrong guess at which issue is "the" measurement log wherever more than one plausible candidate exists | rejected — the label is the precondition, and its absence is silence, not a fallback guess |
| A repository-specific carve-out (`skills/verify/SKILL.md` checks `if repo == "SpecSeal"`) | Hardcodes this repository's identity into a shipped plugin file, which every other document in `docs/` treats as a defect class of its own (`tests/test_no_real_identifiers.py`'s whole reason to exist) — and it would stop working the moment this repository's own name or remote changed | rejected — the label lookup is the general mechanism; it happens to be true only here today, and any other repository following the same convention gets the same behaviour for free |
| Compute "the next version" from `git tag` / the highest existing `vX.Y.Z` tag instead of `plugin.json` | Answers the same question with an extra `git` call and no different result in the case that matters (the workflow already runs after the release-prep commit and the tag push are both part of the same release), and ties the computation to tag hygiene this workflow does not otherwise depend on | rejected — `plugin.json` is already what `close_issues_on_release.py`'s neighbouring hygiene test (`tests/test_release_hygiene.py::version`) reads for the same purpose, in the same checkout |
| Enforce "title carries the version" with a runtime check (a `chain_check.py`-style refusal, or a CI assertion on issue titles) | Needs a red test, a stated failure direction, a prompt budget, and platform honesty per `CONTRIBUTING.md`'s own requirement for any gate change — for a rule with zero recorded issues to measure a check against, the same reasoning `1788445862-a-phase-hands-the-next-one-a-record`'s `plan.md` used to reject the equivalent gate for phase records | rejected for now — satisfied structurally: the opener script always writes a version into the title it creates, so the rule holds without a separate enforcement mechanism unless a future issue is opened by hand without one |

## Judgment recorded (issue text explicitly leaves this to the framer)

**Should "carries the version in its title" be enforced going forward from
the next issue this mechanism opens, with #89 grandfathered as-is?** Yes,
enforced *structurally*: `roll_flow_measurement_issue.py` always titles the
issue it creates with a version number (`chore: flow measurement — X.Y.Z`),
so every issue the mechanism itself opens from here forward satisfies the
rule by construction. No separate runtime check polices a title typed by
hand later — see Alternatives, last row, for why a gate is not built for
this yet. #89 is closed, not renamed, matching the branch task's explicit
instruction not to touch it.

**What "the next version" means when the script runs.** Read `plugin.json`'s
version after checkout (already the just-shipped version, since the
release-prep commit that moved it is part of the same push) and bump the
minor, reset the patch to `0` — `X.(Y+1).0`. This is a default, stated so a
different answer would not silently change behaviour: this repository's own
release history so far is four minor bumps in a row (0.4.0 → 0.5.0 → 0.6.0 →
0.7.0), and `docs/flow.md`'s own `## 0.7.0` section already names `0.8.0` as
the expected next measurement issue in its "While the flow runs" note being
deleted by this work — confirming the default rather than inventing it. A
day this repository ships a patch release instead, the newly-opened issue's
title will read a minor bump that turns out wrong; nothing depends on the
title being correct (the mechanism finds the issue by label and open state,
never by parsing the title), so the cost of a wrong guess is a title a human
can edit, not a broken lookup.

## Phases

Vertical slices — each phase ends with something runnable and verified. One
smith spawn per phase; this table is the handoff between them, and each
phase's own record (`phases/phase-N.md`, from `templates/sdd-phase.md`) is
the other half — **each phase's spawn prompt must explicitly instruct
writing it**, since a mid-session subagent loads its persona from the
plugin's installed version cache and will not otherwise know this
convention exists (it was added to this repository after 0.6.0 shipped, in
work item `1788445862-a-phase-hands-the-next-one-a-record`, merged onto this
branch's base at `6bf9b5f`).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `skills/verify/SKILL.md` gains a new section between `## Seal block` and `## Counterfeits`: after every smith or warden segment, measure its transcript with `skills/verify/scripts/session_cost.py` (subagent transcript path and the "split a resumed segment at the coordinator's message" rule, carried over from `~/.claude/projects/.../memory/measure-every-segment-to-89.md`); find the destination with `gh issue list --label flow-measurement --state open` (exactly one is expected — the mechanism's invariant); post with `gh issue comment <n> --body-file`; do it as part of the segment, before the next one spawns or at the latest with the round/phase record; never ask. States explicitly that where no such issue is open, this step does not apply — a no-op, not a failure. In THIS repository specifically: `gh label create flow-measurement --description "..." --color ..."` and `gh issue edit 89 --add-label flow-measurement` as an explicit shell step, verified by re-running `gh issue list --label flow-measurement --state open` and confirming it returns `#89` and only `#89`. New test module (name TBD by the phase's own smith spawn, following `tests/test_a_phase_hands_the_next_one_a_record.py`'s pin-test shape) asserting the section exists outside HTML comments and names both commands. | `uvx --with pytest python3 -m pytest <new test module> -q`, plus the label-bootstrap shell verification above (not a `git`-tracked change, so it needs its own check per the branch task) | `80f26ce` |
| 2 | New `.github/scripts/roll_flow_measurement_issue.py`: a pure `next_version(current: str) -> str` function (minor bump, patch reset to 0) tested directly with no `gh`/`git` calls; a `main()` that reads `.claude-plugin/plugin.json`, lists open `flow-measurement` issues via `gh issue list --label flow-measurement --state open --json number,title`, fails loudly (`sys.exit`) if the count is not exactly 1, else closes that issue and opens `chore: flow measurement — <next_version>` labelled `flow-measurement` with an empty body. `.github/workflows/close-issues-on-release.yml` gains a second step running this script (same trigger, same checkout, same `GH_TOKEN`/`REPO` env already set for the neighbouring step). New test module, following `tests/test_release_hygiene.py:225-355`'s `monkeypatch`-on-`subprocess.run` pattern: `next_version` cases (`0.7.0`→`0.8.0`, `0.7.3`→`0.8.0`); the exactly-one-open invariant (0 open → fails loudly, 2 open → fails loudly, 1 open → closes it and opens the next); the created issue's title carries the computed version and its body is empty. | `uvx --with pytest python3 -m pytest <new test module> -q` | `ff7f292` |
| 3 | `docs/flow.md`: delete `## While the flow runs` (its own text names this as #109's job — re-read the exact line range at this phase, since phases 1-2 do not touch this file and the surrounding line numbers may have moved by then); tick the `#121 + #119` checkbox; tick this work item's own `#109` checkbox now that phases 1-2 are committed. Closing SDD artifacts: `seal/specs/1788449488-…/changelog.md`, `seal/ledger/1788449488-….md` (only if a row was actually recorded during phases 1-2 — do not manufacture one), `overview.md` (purpose line; any spec/plan divergence; what was not verified and who answers it; what fed back). Narrow verification of every module this branch touched, run together. Hand to the review chain. | `uvx --with pytest python3 -m pytest <phase-1 test module> <phase-2 test module> tests/test_release_hygiene.py tests/test_docs_line_wrap.py -q` (the last two as regression checks — this phase edits `docs/flow.md` and touches the same workflow family `test_release_hygiene.py` covers) | |

**Why this order.** Phase 1 before phase 2, because phase 1's bootstrap step
(labelling #89) is what makes phase 2's script have something real to close
at the next actual release, and because the two parts are independently
testable but phase 2's "exactly one open" test fixtures are easier to reason
about once phase 1's convention (what "open" means here) is written down.
Phase 3 last, because `docs/flow.md`'s `#109` checkbox can only be ticked
once phases 1-2 are actually committed, and the closing artifacts need every
prior phase's files in place.

**Every phase commits.** This branch is routed `smith` · `through the review
chain` · `open the pull request` into `release/v0.7.0`
(`seal/specs/1788449488-…/routing.md`), so the review arm of the commit gate
is silent and an intermediate commit costs nothing. An uncommitted change is
invisible to the reviewer.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`. Fill it in as each phase closes.

## Verification scope, per phase

Narrow and often, broad once. Each phase runs the modules its own diff can
break, named in the table above. **No phase runs the full suite,
repository-wide lint, or a typecheck** — the broad gate runs once, after the
review rounds settle, and the orchestrator owns it. Every phase hands over
with the suite labelled `unverified` and the orchestrator named as its
answerer.

Exit codes are read directly: `cmd >/dev/null 2>&1; echo $?`, never
`cmd | tail; echo $?`.

## Operational impact

- **No migration, no new environment variable, no new dependency.**
- **A new GitHub label, `flow-measurement`, created in this repository by
  phase 1's shell step.** Not a code change and not reversible by a revert —
  noted here per Operational impact's own purpose ("items a deployer must not
  miss").
- **The next real effect is at this repository's own next release** (this
  branch's own target, `release/v0.7.0` → `main`): `roll_flow_measurement_issue.py`
  runs for the first time, closing `#89` and opening the `0.8.0` issue. This
  work item does not itself perform or verify that release event — it
  verifies the script's logic in isolation, per `spec.md`'s acceptance table.
- **Every other installed repository sees no effect** until it separately
  adopts the `flow-measurement` label convention — the skill section is
  conditional on the label's presence, and no other file this work touches
  ships to consumer repositories.
- **Prompt budget: zero.** Nothing here adds a question to any session; both
  the segment-measurement step and the release-time rollover run without
  asking.
- **Compatibility.** Additive. No hook or gate reads the new skill section
  or the new script's output, so an older installed plugin version, or a
  repository with no `flow-measurement` label, keeps working unchanged.

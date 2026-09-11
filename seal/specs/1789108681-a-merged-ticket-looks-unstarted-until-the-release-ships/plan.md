# Implementation Plan: a merged ticket says so on the tracker, and the release cannot ship a milestone that is not true

<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

Two workflow-side pieces and three documents. The signal writes a label on
push to `release/*`; the gate reads the milestone on a pull request into
`main` and refuses an untrue one. Neither piece parses anything new — both
read through `close_issues_on_release.py`'s existing readers — so the work is
mostly about which set is authoritative, which party a failure names, and
what has to be true before the release this ships in can open its own pull
request.

## Technical context

**What exists and is reused.** `.github/scripts/close_issues_on_release.py`
holds `MERGED_PR` (the `(#N)` a squash subject ends with), `CLOSING` with
`FENCE`/`SPAN` around it (`keywords_in`), `pull_request_body` (a 404 is input,
not a failure) and `arrived(before, after)`. Its `main` is guarded, so
importing the module runs nothing;
`tests/test_release_hygiene.py`'s `_closer()` already imports it by path
rather than shelling out, which is the pattern to follow.

**Where the gate goes.** `.github/workflows/hygiene.yml` already runs on
pull requests into `main` with `fetch-depth: 0` and already holds four
release-only steps, each opening with the same `if [ "${{ github.base_ref }}"
!= "main" ]` guard. The new step is a fifth of that shape, with one more
condition: the head must be a `release/v*` branch, because
`docs/branch-and-release.md` lists a hotfix branch as the other thing that
reaches `main`, and a hotfix carries no release milestone.

**What the range has to be.** `origin/main..HEAD` is wrong the moment a
hotfix moves `main` during a release's life. The range is
`$(git merge-base origin/main HEAD)..HEAD`, and phase 2 pins that with a case
rather than leaving it to the day it matters.

**The constraint that is easy to miss.** `docs/` is inside
`tests/test_release_hygiene.py`'s `LOADED`, so a documentation edit naming
`0.11.1` goes red at this release's own preparation commit — hours in, after
the broad gate. Every version in prose is `X.Y.Z` or the illustrative
`1.2.3`. `.github/` is outside `LOADED`, so the scripts and workflows are
unconstrained.

**Failure scenario of the chosen approach, in six months.** The signal and
the gate both depend on `Closes #N` being written in a feature pull request
body. A work item that ships without one is invisible to both: its issue sits
in the milestone, never enters `D`, and blocks the release until somebody
either adds the keyword or moves the issue. That is a louder failure than
today's silence and it lands on the release rather than on the work item that
caused it. The cheaper version — reporting it at the feature pull request —
already half exists in `issue_claims_check.py`, which prints what a body
claims and never fails. Widening that to fail is a separate ticket and is
named here so it is not rediscovered as a surprise.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A staging milestone: work collects there and moves to `release: X.Y.Z` when finished | `docs/issues-and-milestones.md` defines a milestone's job as answering *what is in 1.2.3* without opening a file, and under this shape nobody can answer it until the release ships. It also makes scheduling two acts again, which is the sentence #351 deleted, and it is a rule a person has to remember at merge time — #330's class | **rejected** (the ticket's own reasoning; recorded here so it is not re-argued) |
| The gate refuses on `M \ L` and cross-checks `L` against `D` separately, as the ticket proposes | A label write that failed — a permission the token lacks, a workflow that did not run — blocks the release, and the remedy is a person adding a label by hand, which is the act this work exists to remove. It also makes the label a second source of truth for a fact the commits already carry | **rejected**; the gate refuses on `M \ D` and reports `L ≠ D` |
| Drop the label cross-check entirely, since `M \ D` is complete without it | The label is what a person reads on the tracker, and nothing would ever notice it going stale. That is the defect this work is about, one layer over | **rejected**; the cross-check stays, as a finding about the signal rather than about the release |
| Extract the shared readers into `.github/scripts/release_readers.py` and have both scripts import it | `FENCE` carries a `# RIDER:` stamp resolved against its own file by anchor. Moving the symbol moves the rider's anchor and forces a re-stamp, and the rider's subject — issue #266's open decision about widening the patterns — is not this work item's to touch | **rejected for now**; the new scripts import `close_issues_on_release` directly, one source and no move |
| Fail on `D \ M` too — the release carries an issue no open milestone claims | An issue somebody closed by hand mid-release is in `D` and in no open milestone, so the gate would go red for ordinary tracker hygiene | **rejected**; reported, never fails |
| A separate workflow for the gate rather than a step in `hygiene.yml` | A second workflow on the same event, with the same checkout settings, that a reader has to know to look in. `hygiene.yml` is where the release-only checks already are | **rejected** |
| A new job in `close-issues-on-release.yml` for the signal, rather than a new workflow | That workflow's trigger is `push: branches: [main]`. A push to `release/*` is a different event, and adding it would make every step in the file conditional on which branch moved | **rejected**; a new workflow file |

## The sequencing constraint

**This is a constraint on the work, not a detail of it.** The release that
ships the gate is the first thing the gate judges, and it judges it at the
moment the release pull request opens — after the preparation commit, after
the fragments are gathered, after the broad gate has run on the preparation
tree.

Measured at `a01d679`, `gh issue list --milestone "release: 0.11.1" --state
open` returns **nine**: #359, #354, #351, #350, #345, #343, #330, #198, #103.
Two of those will be in the release — #351, squash-merged at `f9c6907` and
already carrying its label, and #359, this work item. The other seven are
scheduled work that has not been built. Under the gate as specified, the
release pull request fails and names all seven.

That is the gate working. The milestone is not true, and it has not been true
for as long as the tracker has been used this way — `docs/issues-and-milestones.md`
already says a milestone answers *what is in 1.2.3*, and nothing has ever
checked it.

So the act that has to happen before the 0.11.1 release pull request opens is
**making the milestone true**: every issue not shipping in 0.11.1 moves to
another milestone. That is a release-planning act, it needs no code, and it is
the owner's. The alternative — an escape in the gate for its own first
release — is `questions.md` Q2, and it is asked rather than assumed because it
is the difference between shipping no extra code and shipping a dated special
case that somebody has to remember to remove.

Whichever answer comes back, **`docs/release-checklist.md` step 0 gains the
line naming this act**, because a release after this one meets the same
requirement with no ticket to explain it.

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The signal: `.github/scripts/label_merged_on_release_branch.py` and its workflow on push to `release/*`, importing the readers from `close_issues_on_release`. Creates the label if absent, adds it, writes nothing else | S1, S2, S3 as cases monkeypatching the module's `run`, following `tests/test_a_release_rolls_the_flow_measurement_issue.py`. Q3 and Q6 are answered here, before the script is trusted | |
| 2 | The gate: `.github/scripts/release_completeness_check.py`, refusing on `M \ D`, reporting `L ≠ D` by direction and `D \ M` without failing. Range from `git merge-base` | S4 **seen red first** against a fixture whose milestone claims an item the branch does not carry, then S5, S6, S7, S8. Q4 and Q5 are answered here | |
| 3 | The step in `hygiene.yml`, release-only and head-shape guarded, with the comment block the file's other steps carry | S7 against each non-release head shape; `tests/test_ci_gives_the_checks_what_they_need.py` still green | |
| 4 | The three documents: `docs/release-checklist.md` step 0's new line and §6's corrected sentence, `docs/issues-and-milestones.md` §*Nothing automated reads a milestone* rewritten | S9, S10, S11; `tests/test_one_word_one_meaning.py` and `tests/test_docs_line_wrap.py` | |
| 5 | `seal/specs/<id>/changelog.md`, any ledger rows in `seal/ledger/<id>.md`, and the closing memo | The fragment conventions in `CLAUDE.md`; `unverified_check` on the memo's `## Not verified` table | |

Phase 1 and phase 2 are separable and phase 2 does not depend on phase 1
having run: the gate derives `D` itself, which is the whole point of the set
assignment above. Build them in this order anyway, because phase 1 is where
the token questions get answered and a gate that cannot read the tracker is
not worth writing first.

What each phase discovers and the next needs goes to
`seal/specs/<id>/phases/phase-N.md`, from `templates/sdd-phase.md`.

## Operational impact

- **No `plugin.json` bump.** `hygiene.yml`'s version step greps
  `^(skills|agents|hooks|templates|bin|\.claude-plugin)/`, and this work
  touches `.github/`, `docs/` and `seal/` only. Nothing that ships changes, so
  the step exits 0 and the version stays where it is.
- **A new workflow permission set**, on both halves — `issues: write` for the
  signal and a token for the gate's reads. `hygiene.yml` declares no
  `permissions:` block today and uses no `gh`, so the gate step is the first
  thing in that file to need one. Q3 and Q4 are what settle it.
- **A new label per release**, `merged: X.Y.Z`, created by the signal. They
  accumulate; nothing removes them, and the Scope section says why.
- **A new way for a release pull request to go red**, and the first release
  after this ships meets it. The sequencing constraint above is the operational
  half of that.

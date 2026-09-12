# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. -->

📋 implement applied
· spec:     `CLAUDE.md` §*The goal a design is chosen against*, §*Repo rule — the merge method is fixed per direction*, §*Repo rule — no real identifiers*, §*Repo rule — a change writes fragments* · `CONTRIBUTING.md` §*What a change to a gate must carry*, §*House rules* · `docs/issues-and-milestones.md` (in full) · `docs/release-checklist.md` (in full) · `docs/branch-and-release.md` §*A closing keyword does nothing when the base is `release/vX.Y.Z`* and the sections around it · `seal/follow-up.md` (read in full; no row is a prerequisite of this work and none is closed by it) · `seal/config.md` (no `Record language` row — English; `Broad gate` row read and NOT run, see below) · this item's own `routing.md`, `spec.md`, `plan.md`, `questions.md`
· evidence: 8 rows in `seal/ledger/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships.md`, 17 coordinates, all re-verified at `evidence_check.py --reverify .` exit 0
· verified: **executed** — `bin/test` on **nine** modules, six in one call and three in another: 121 + 50 = **171** cases at the build, exit 0, and 121 + 54 = 175 after round 1's fixes added four cases. (This line said *eight modules* until round 1 counted them; the two figures beside it were always right.) `uvx ruff check` and `ruff format --check` on every file touched, exit 0; the gate run four ways against the LIVE tracker with exit codes read directly; 19 mutations across both scripts and the workflow step at the build and 11 more over round 1's fixes, each one seen red; `survivor_check.py` exit 0; `evidence_check.py --reverify` exit 0. **read** — GitHub's REST and Actions permission references (neither settles Q3). **unverified** — the broad gate, and the workflow token, both in the table below

## Why this work exists

Between a work item squashing into `release/vX.Y.Z` and the release reaching
`main`, a finished ticket and an unstarted one look identical on the tracker;
after this, the finished ones carry `merged: X.Y.Z` and a release cannot ship
while its milestone claims work the release branch does not carry.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether a milestone that does not exist is judged | The spec and the plan are both silent. `spec.md` §*Data & interfaces* says only that "a shape it cannot judge exits 0 with a reason printed" | A separate existence read, then a warning saying the run verified nothing, then exit 0 | Spec silent, and the silence was load-bearing. Executed: `gh issue list --milestone "release: 9.9.9" --state open` returns `[]` and exits 0, so without the read a typo makes the gate pass by measuring an empty set — "a check that cannot fail is a counterfeit seal" (`skills/verify/SKILL.md`). Passing rather than failing follows the grounds `plan.md` gives for rejecting a `D \ M` failure: "an issue somebody closed by hand mid-release … would go red for ordinary tracker hygiene", and a release nobody scheduled is the same class |
| Whether `docs/branch-and-release.md` is edited | `spec.md` §*Out*: "Anything about how a release is cut, merged or tagged. `docs/branch-and-release.md` owns that; this work edits only the sentence above, which is a statement about a workflow rather than about the sequence" | One paragraph added, no sentence in the file edited | `questions.md` Q9 hands this judgment to phase 4, so the SDD authorises it rather than my overriding the Out list. Every sentence in §*So a workflow reads the keywords instead* survives; what stops being true is the conclusion around them, that a keyword written into a release base does nothing until `main` moves. The added paragraph is a statement about a workflow and not about the sequence — the same line the Out entry itself draws |
| Where the name mapping lives | `plan.md`'s alternatives table rejects extracting shared code into a module of its own; nothing says where a NEW shared symbol goes | In the signal, imported by the gate | The rejection is about **moving** `close_issues_on_release.py`'s readers, because that would move `FENCE`'s `# RIDER:` anchor. The mapping is new and moves no rider. One source, the way the readers are one source. The trade is stated in `phases/phase-1.md`: a reader imports a writer |
| The shape of `hygiene.yml`'s release-only steps | `plan.md` §Technical context: "four release-only steps, each opening with the same `if [ … ] != "main" ]` guard" | Copied the three that actually have it | Three do; the fourth — *wording this branch removed is not still standing elsewhere* — opens with the inverted guard and skips on `main`, because a release's range is not a range any fix pass wrote. A step written from the frame's sentence would have run in exactly the wrong direction |

## Not verified

| Item | Who must answer |
|---|---|
| **The broad gate.** `seal/config.md` names it — `bin/test -q && uvx ruff check . && uvx ruff format --check .` — and it was deliberately not run: `skills/agent-contract/SKILL.md` §2 assigns it to the sealer, once, after the review rounds settle. Nine modules were run narrowly instead | the orchestrator, by spawning the `sealer` |
| **Q3 — whether a workflow job holding `permissions: issues: write` can create a label with the default `github.token`.** It needs a real workflow run or a label create, and both are writes this segment may not make. GitHub's own references do not enumerate labels under the `issues` scope (read, 2026-09-11). The create path is reached at most once per release and fails loudly with the label name if the token does not cover it | the repository owner, **at the first squash into a release branch whose `merged: X.Y.Z` label does not yet exist — not this one.** Round 1 found this row sent to a run that cannot reach the path: `merged: 0.11.1` was created by hand before the build, so the signal's read finds it and skips the create. This branch's own squash answers `--add-label` alone, which is the other half and is worth watching for its own sake. The version is deliberately not named — `docs/branch-and-release.md` says whether the next number is a minor or a patch is known at the end and not at the cut |
| **S12 — that a session resuming mid-release can tell finished from unstarted by reading the milestone.** It is verifiable only against the live tracker *after* this work item's own squash, which has not happened | the repository owner, at the same moment as Q3 |
| **Whether `issues: read` reaches a pull request BODY.** Round 1's finding 8, out of its verified scope and given a home here. The gate reads bodies through `GET /repos/{owner}/{repo}/issues/{n}`, and the tree's only precedent is one level up: `close-issues-on-release.yml` holds `issues: write` with no `pull-requests` scope and its latest run read three bodies and closed an issue. A `GET` needs only the read level of a permission the write level covers, so this very probably holds and has not been run. The direction if it does not: every body returns 404, every number is skipped as "not a pull request", D comes out empty, and the gate refuses the release naming the whole milestone — a message that misdirects, which is why it is written down rather than left to be met | the repository owner, at the 0.11.1 release pull request. That is also the step's first execution in CI of any kind: the shell guard skips every base that is not `main`, so nothing before the release pull request runs the script at all |
| **The `permissions:` block newly stated on `hygiene.yml` does not starve an existing step.** Argued rather than run: every step in that job reads and none writes, so `contents: read` + `issues: read` is narrower than any default it replaces and cannot remove a scope something was using. No run has confirmed it | the repository owner, at this branch's own pull request, where `hygiene.yml` runs for the first time with the block |

## Not done

**The feature pull request is not made to report a missing `Closes #N`.**
`plan.md` names this as the chosen approach's failure scenario in six months:
a work item that ships without the keyword is invisible to both halves, sits
in the milestone, never enters what the release carries, and blocks the
release rather than the work item that caused it. The cheaper version half
exists — `issue_claims_check.py` already prints what a body claims and never
fails — and widening it to fail is a change to a gate with its own four
things to carry. It is named in the plan so it is not rediscovered as a
surprise, and it is a separate ticket rather than a row here.

**The gate is not run on a pull request into a release branch.** It runs only
for a pull request into `main`, so the first thing it judges is the release
itself. Running it earlier would mean judging a milestone against a branch
that is deliberately incomplete.

**No dated escape was built for the gate's own first release.**
`questions.md` Q2 was answered (a) by the repository owner before the build
started: the milestone was made true by hand rather than the gate excepted,
so there is no special case to remember to remove.

## Fed back into the spec

One clause, inferred during implementation and recorded in the ledger rather
than written back into `spec.md`: **a gate that reads a named collection has
to establish that the collection exists**, because `gh issue list --milestone`
answers an unknown title with an empty list and exit 0. `spec.md` §*The three
sets* defines M as "open issues whose milestone is `release: X.Y.Z`" and is
silent on a milestone that is not there. A planner may overturn the direction
chosen — reporting and passing rather than refusing — but the read itself is
what keeps the check from measuring nothing.

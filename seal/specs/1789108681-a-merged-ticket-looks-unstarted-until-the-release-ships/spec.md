# Feature Specification: a merged ticket says so on the tracker, and the release cannot ship a milestone that is not true

<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #359. Milestone `release: 0.11.1`.

Between a work item squashing into `release/vX.Y.Z` and the release reaching
`main`, a finished ticket is indistinguishable from an unstarted one, because
an issue's state does not move until `main` moves. Two pieces answer it, and
they answer two different questions:

- a **signal**, so a person reading the tracker can tell the two apart;
- a **gate**, so a release cannot ship while its milestone claims an item the
  release does not carry. That gate is the completeness check `docs/flow.md`
  used to carry as a checklist bullet, which #351 deleted with the file.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | The bullet this replaces was a person reading a checklist. Both halves run in CI and neither asks anybody anything, so the prompt budget is zero and that is the argument for the shape |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The gate can refuse a release pull request, so all four are owed: a test seen red, a stated failure direction, a prompt budget, platform honesty |
| `docs/issues-and-milestones.md` §*Nothing automated reads a milestone* | It says no hook, script or workflow reads a milestone. **This work makes that false.** The section is rewritten in the same change rather than left contradicting the tree |
| `docs/issues-and-milestones.md` §*A milestone answers* when | The same section says a wrong milestone "costs a person a wrong answer and costs no automation anything". After this work a wrong milestone costs a blocked release, which is the sharper half of the same repair |
| `docs/branch-and-release.md` §*A closing keyword does nothing when the base is `release/vX.Y.Z`* | `Closes #N` in a feature pull request body is the only durable record of which issue that pull request answers. Both halves of this work read it, through the readers `close_issues_on_release.py` already has |
| `docs/branch-and-release.md` §*The two merge shapes are not interchangeable* | A pull request into `main` is a release branch's or a hotfix branch's. The gate has to tell them apart, because a hotfix carries no milestone to check |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry goes to `seal/specs/<id>/changelog.md` and any ledger row to `seal/ledger/<id>.md`. Neither shared file is appended to |
| `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | `docs/` is in `LOADED`. Every documentation edit this work makes must spell the version `X.Y.Z` or `1.2.3`, never `0.11.1`. `.github/` is outside `LOADED`, so the scripts and workflows are unconstrained |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Fixtures use `example.com` and `/Users/x/`; a repository name in a fixture is the same class |

## Scope

### In

**The signal.** A workflow on push to `release/*` that labels the issues the
arriving pull requests close with `merged: X.Y.Z`, creating the label if it is
absent. The version comes from the branch name; the readers come from
`close_issues_on_release.py` rather than being written again.

**The gate.** A step in `hygiene.yml`, on a pull request whose base is `main`
and whose head is a `release/v*` branch, that refuses while the release's
milestone claims an open issue the release branch does not carry, and names
the ones it found.

**The cross-check**, reframed. See *The three sets* below: the commits are
authoritative and the label is a cache of them, so the gate's refusal is
computed from the commits and the label disagreement is reported separately,
with the direction named.

**`docs/release-checklist.md` step 0** gains a line naming the check where the
deleted bullet stood. Step 0 currently asks whether what arrived was squashed
with green CI; nothing in it asks whether everything is in.

**`docs/release-checklist.md` §6's sentence about the close-issues workflow.**
It reads *"The close-issues workflow runs on the tag and closes every issue the
changelog section names."* Both halves are false against the tree:
`close-issues-on-release.yml` triggers on `push: branches: [main]`, not on a
tag, and `close_issues_on_release.py` reads pull request bodies, not the
changelog section. It is in scope because this work edits that file and extends
that mechanism, and because leaving a sentence known to be false in a file
being edited is the deferral this repository does not make.

**`docs/issues-and-milestones.md` §*Nothing automated reads a milestone*** is
rewritten to say what now reads one and what a wrong milestone now costs.

### Out, and why

- **Closing issues at the release-branch merge.** The ticket's own reasoning
  stands: an issue closed then is closed for something nobody has received.
  `close_issues_on_release.py` keeps the close, and this work adds no second
  closer.
- **A staging milestone.** Rejected in the ticket and the rejection holds; the
  argument is in `plan.md`'s alternatives table so a later reader does not
  re-open it.
- **Removing a `merged: X.Y.Z` label after the release ships.** Deleting a
  label deletes it from every issue that carried it, which falsifies the
  record the label was created to leave. The labels accumulate, one per
  release, and that is the cost of keeping history readable.
- **Failing on `D \ M`** — an issue the release carries that is not in the
  milestone. The bullet this replaces asked *is everything in*, not *is
  everything claimed*, and an issue somebody closed by hand mid-release is in
  `D` and in no open milestone. It is reported and never fails.
- **Anything about how a release is cut, merged or tagged.**
  `docs/branch-and-release.md` owns that; this work edits only the sentence
  above, which is a statement about a workflow rather than about the sequence.
- **Widening `FENCE` or `SPAN` in `close_issues_on_release.py`.** The `# RIDER:`
  comment above them says opening those patterns changes what a release closes
  and sends the decision to issue #266. This work reads through them unchanged.
- **`close-issues-on-release.yml`'s own trigger and steps.** The signal is a
  new workflow on a different event; nothing about the existing one moves.

## The three sets

Everything below is about three sets of issue numbers, and naming them once is
what keeps the gate's failure messages pointing at the right party.

| Set | What it is | Derived from |
|---|---|---|
| **M** | open issues whose milestone is `release: X.Y.Z` | `gh issue list --milestone` |
| **D** | issues the release branch actually carries | the branch's commit subjects → `(#N)` → those pull request bodies → closing keywords |
| **L** | issues carrying the label `merged: X.Y.Z` | `gh issue list --label` |

**D is the source of truth and L is a cache of it.** The signal writes L from
D one push at a time; the gate recomputes D in full from the release branch's
range. So the gate's refusal is `M \ D` — *the milestone claims items the
release does not carry* — and it never depends on a label write having
succeeded. `L ≠ D` is a separate finding about the signal, reported with the
direction named: `D \ L` is a label the signal never wrote, `L \ D` is a label
somebody added by hand or a squash subject that lost its `(#N)`.

Computing the gate as `M \ L` instead would give the same answer by
transitivity and blame the wrong party: a release blocked because a label write
failed is a person adding a label by hand, which is the act this work removes.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · a squash into a release branch labels what it closes | Given a pull request whose body carries `Closes #N` · When its squash lands on `release/vX.Y.Z` · Then #N carries `merged: X.Y.Z` | a case monkeypatching the script's `run`, following `tests/test_a_release_rolls_the_flow_measurement_issue.py`'s pattern; the real run observed once on this branch's own merge |
| S2 · the label is created when it is absent | Given no `merged: X.Y.Z` label exists · When the signal runs · Then it is created with a description and then applied | a case asserting the create call precedes the edit call, and that an existing label produces no create |
| S3 · re-running the signal changes nothing | Given the signal already labelled #N · When the same push is re-run · Then no error and no second write | a case; adding a label already present is measured, not assumed (questions.md Q6) |
| S4 · the release pull request refuses an untrue milestone | Given `release: X.Y.Z` holds an open issue the release branch does not carry · When the release pull request opens · Then the hygiene job fails and names that issue | the gate run against a fixture where `M \ D` is non-empty, **seen red before the milestone is corrected** |
| S5 · a true milestone passes | Given every open issue in the milestone is in the release branch's range · When the gate runs · Then it exits 0 and prints both sets | a case |
| S6 · the gate names which side a label disagreement is on | Given #N is in D and carries no label · When the gate runs · Then the report says the signal missed it, and given #N carries a label and is not in D, the report says the label was written outside the mechanism | two cases, one per direction |
| S7 · the gate skips what it cannot judge | Given a pull request into `main` whose head is a hotfix branch · When the gate runs · Then it prints why it is skipping and exits 0 | a case per non-release head shape |
| S8 · a missing `Closes #N` is caught rather than lost | Given a work item merged into the release whose pull request body wrote no closing keyword · When the gate runs · Then its issue is in M, not in D, and the release is refused | a case. `docs/issues-and-milestones.md` says a missing keyword "costs an issue that stays open forever"; this is the first thing that reports it |
| S9 · the checklist asks the machine, not a person | Given `docs/release-checklist.md` step 0 · When it is read · Then a line names the gate where the deleted bullet stood, and §6's sentence about the close-issues workflow states the trigger and the input the tree actually has | read; `grep -n "on the tag" docs/release-checklist.md` returns nothing |
| S10 · the milestone document does not contradict the tree | Given `docs/issues-and-milestones.md` · When §*Nothing automated reads a milestone* is read · Then it names what reads one and says a wrong milestone now blocks a release | read; `grep -rn "Nothing automated reads a milestone" docs/ skills/ agents/` has one owner |
| S11 · no documentation edit starts a timer | Given every `docs/` file this work edits · When `tests/test_release_hygiene.py` runs · Then no version at or above the running one is named | `test_no_loaded_file_names_a_version_at_or_above_the_running_one` |
| S12 · a session resuming mid-release tells finished from unstarted | Given only `gh issue list --milestone "release: X.Y.Z"` · When a person reads the rows · Then the merged ones carry `merged: X.Y.Z` and the rest do not | read against the live tracker after this work item's own squash |

## Data & interfaces

No schema, no endpoint. Four surfaces.

**New: the signal script.** Reads `BEFORE`, `AFTER`, `REPO` and the branch
name from the environment, the way `close_issues_on_release.py` does. Writes
two kinds of call and nothing else: create a label if absent, add a label to
an issue. It never removes a label, never closes an issue, and never comments.

**New: the gate script.** Reads the release version from the head branch name,
the milestone by title, the branch's own range, and the label. Writes nothing.
Its only exit codes are 0 and 1; a shape it cannot judge exits 0 with a reason
printed.

**Reused, unchanged:** `close_issues_on_release.py`'s `MERGED_PR`, `CLOSING`,
`FENCE`, `SPAN`, `keywords_in`, `pull_request_body` and `arrived`. Its `main`
is guarded by `if __name__ == "__main__"`, and
`tests/test_release_hygiene.py` already imports the module rather than
shelling out, so importing it is established here.

**Edited:** `.github/workflows/hygiene.yml` gains one step;
`docs/release-checklist.md` and `docs/issues-and-milestones.md` gain and lose
the prose named in Scope.

**The name mapping**, which has no checker today and gains one with the first
case that reads it: branch `release/vX.Y.Z` → version `X.Y.Z` → milestone
`release: X.Y.Z` → label `merged: X.Y.Z`.

## What a change to a gate must carry

The ticket answers all four. Checked against the tree, they hold, with one
addition.

- **A test seen red** — S4, run against a release branch whose milestone
  claims an item the branch does not carry. `plan.md` phase 2 says how it is
  shown.
- **A failure direction** — this blocks more. A wrong deny costs a release
  preparation one prompt; a wrong allow ships a release whose milestone claims
  an item that is not in it, which is the defect the deleted bullet existed to
  stop.
- **A prompt budget** — zero. Both halves run in CI on their own triggers and
  neither asks anybody anything.
- **Platform honesty** — both halves are `ubuntu-latest` workflow jobs. No
  process inspection, no path spelling. What is not yet honest is the token:
  neither half's permission set has been measured, and `questions.md` Q3 and
  Q4 are the rows that settle it before either ships.

## Open questions → questions.md

Two rows need the repository owner and nothing else does. The rest are a
measurement or the work, and are sorted that way.

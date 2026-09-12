# round 1 — review report

| | |
|---|---|
| Work item | `1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships` (#359) |
| Target SHA | `9a010fd` |
| Reviewed at | `666df9d`, the branch HEAD |
| Base | `origin/release/v0.11.1` = `f9c6907` |
| Ran by | specseal:warden on Opus 5 |
| Worked in | a `git clone --no-local` at the review SHA; nothing written in the checkout under review except this file |

## What the round did before it looked for anything

The build's numbers were re-derived rather than inherited, because that is what
§5 asks of a prompt's facts. All of them hold.

- **165 across the eight modules the paragraph names**, exit 0 each, run one
  module at a time. **171 across nine**, which is what the build itself
  measured — see the correction below.
- **`evidence-check --strict`: 1137 rows ok**, 0 drifted, 0 broken, exit 0.
  Run over the whole tree, never narrowed to this item's fragment.
- **`survivor-check --range origin/release/v0.11.1...HEAD`: exit 0**, 879 files
  against 8 removed sentences, no removed wording still standing. The builder's
  "no survivors and therefore no `survivors.md`" is true: the three
  `survivors.md` files in the tree belong to other work items.
- **`ruff check` and `ruff format --check` over the four changed Python files:
  exit 0** each.
- **The 19 mutations.** Eighteen were re-derived, chosen across both scripts,
  the workflow step and the permissions block; **fifteen came back red**. Which
  fifteen, and which three did not, is in the probes table. The one the build
  says exposed a weak case — deleting the step guard's `exit 0` and its `fi` —
  is red now, so the repair at `f137a21` holds.
- **The gate run against the live tracker**, read-only, exit code read
  directly: **exit 1**, refusing and naming the issues. It works.

Four things came back with something in them. They are in the order the
mechanism runs, not in order of severity.

---

## The gate can pass while measuring nothing, which is the one thing it was built not to do

🟡 `.github/scripts/release_completeness_check.py:100`

`milestone_titles` exists because `gh issue list --milestone` answers a title
nothing has with `[]` and exit 0, and the function's own docstring calls that
"the one direction a checker of claims must not fail in". The read it makes is
one unpaginated page:

```python
out = closer.run("gh", "api", f"repos/{repo}/milestones?state=all&per_page=100")
```

`gh api` without `--paginate` returns the first page and stops. `per_page=100`
is the maximum the endpoint allows, so at 101 milestones the target title falls
off the page, the gate prints `this run verified NOTHING` and exits 0 — the
fail-open the whole function exists to close, arriving through the function
itself.

**Executed**: this repository has **33** milestones today, one per release plus
the planning ones, so the hole is 68 releases away rather than reachable now.
What makes it worth a fix rather than a note is that nothing measures the
query: a probe replacing the whole `?state=all&per_page=100` with a bare
`repos/{repo}/milestones` left all 25 cases in
`tests/test_a_release_cannot_ship_an_untrue_milestone.py` green.

## The range the SDD chose is not the range CI measures

🟡 `.github/scripts/release_completeness_check.py:71-84` and `:236`, with
`.github/workflows/hygiene.yml:269-280`

`questions.md` Q8 chose `merge-base(base, HEAD)..HEAD` over `base..HEAD`, and
the grounds are specific: they come apart "the moment a hotfix that was also
merged into the release branch moves `main` mid-release", and the fork-point
form is the one that keeps that hotfix inside D.

On a `pull_request` event `actions/checkout` checks out the merge ref that
GitHub builds — the head merged into the base — not the head. `HEAD` in the job
is therefore a commit that already contains `origin/main`, so
`git merge-base origin/main HEAD` returns the base tip rather than the fork
point, and the range collapses to exactly the `base..HEAD` spelling Q8
rejected. A hotfix reachable from `main` drops out of D again.

`test_the_range_is_measured_from_where_the_branch_left_main` pins the two
commands, which is the right thing to pin, and it passes — the script does what
it says. What is unpinned is the shape of the commit those commands are handed,
and that is where the choice is undone.

**Read, not executed** — no case here can run a workflow, and the checkout
behaviour is `actions/checkout`'s documented default for `pull_request`.

**What it costs today is nothing**, and that is a fair answer to give back:
`docs/branch-and-release.md:218` says a hotfix taken straight into `main` has
its `Closes #N` fire, so its issue is closed by GitHub and never sits in M.
The gap is in the guarantee rather than in this release. If that is the
grounds, it belongs in the file next to the range, because the next reader of
`merge_base` will read a docstring describing a protection CI removes.

## The document sends a reader to a box that is not there

🟡 `docs/issues-and-milestones.md:127-128`

> `docs/release-checklist.md` step 0 is where that act belongs, and it is the
> first box on the list.

It is the third of four. Step 0's boxes stand at `docs/release-checklist.md`
lines 14, 18, **40** and 50, and the milestone box is the one at line 40.
`phases/phase-4.md:58` shows the belief the sentence came from — "Step 0's new
box is first in the list, and the placement is the point" — so this is a claim
about placement that the placement does not meet, not a wording slip.

Why it matters here rather than anywhere: this work item's own §6 repair
exists because a checklist sentence nobody could act on survived several
releases. A person reaching step 0 for the milestone act looks at the first box
and finds the squash rule.

The reasoning survives either repair. The box is inside step 0, so it is still
ticked before any cost is paid; what has to change is the sentence or the
order, and the sentence is the cheaper of the two.

## The one question left open was sent to a run that cannot answer it

🟡 `overview.md` §*Not verified* row 2, and `questions.md` Q3

Q3 asks whether a job holding `permissions: issues: write` can **create** a
label. Both the question row and the overview send it to the same answerer:
the repository owner, "by watching this branch's own squash into
`release/v0.11.1` — the first real run".

That run will not reach the create path. **Executed**, read-only against the
live tracker: the label `merged: 0.11.1` already exists, and #351 has carried
it since `2026-09-11T06:36:29Z`, applied by the repository owner by hand. The
signal reads `existing_labels` first and creates only on absence
(`.github/scripts/label_merged_on_release_branch.py:220`), which is the design
Q6 settled on and is correct. The consequence is that on 0.11.1 the run
exercises `--add-label` and skips `gh label create` entirely.

So the create path first runs on the first squash into `release/v0.12.0`, in
the middle of a release, where it fails loudly with the label name and nobody
is watching for it. The row is not wrong about the risk; it is wrong about
where the answer arrives.

---

## Corrections — the paperwork rather than the tool

⬜ **`overview.md:9` says eight modules; it is nine.** The two figures beside it
are exact and re-derive: `121` is `test_docs_line_wrap.py` (23),
`test_one_word_one_meaning.py` (13), `test_release_hygiene.py` (32),
`test_no_real_identifiers.py` (2), `test_the_rules_have_one_owner.py` (45) and
`test_a_question_says_who_can_answer_it.py` (6); `50` is the two new modules
(23 + 25) and `test_ci_gives_the_checks_what_they_need.py` (2). Six plus three
is nine, and 121 + 50 is 171.

⬜ **The gate step's `env:` is unpinned.** Probes deleting
`REPO: ${{ github.repository }}` and `BASE: origin/...` from
`.github/workflows/hygiene.yml:269-280` both left all 25 cases green. Losing
`BASE` is harmless — the script's default is `origin/main`, which is what a
release pull request wants. Losing `REPO` is a `KeyError` traceback at the
release pull request, which is loud, so this is a note rather than a fix.

⬜ **A revert does not leave D.** A work item squashed in and then reverted
keeps its issue in D, because the revert's own subject carries the revert pull
request's `(#N)` and its body carries no closing keyword. The docstring calls D
"issues the release branch actually carries". Named so it is not rediscovered;
no release here has reverted a squash.

## Answers to the leads, including the empty ones

**The empty-set hole is reachable, and its presence is pinned as well as its
absence.** A probe replacing `if milestone not in milestone_titles(repo):` with
`if False:` turns
`test_a_milestone_that_does_not_exist_says_it_verified_nothing` red — the case
makes `open_in_milestone` fail on call, so deleting the guard cannot pass. The
query behind the guard is the part nothing pins, which is the first finding
above.

**`M \ D` never falls back to labels.** `carried` is built only by
`signal.issues_in` over `git log`, and `labelled()` feeds nothing but the two
`L` comparisons in `judge`. Probes confirm the direction Q1 answered: removing
`failed = True` from the `L \ D` branch turns
`test_a_label_naming_a_release_the_issue_is_not_in_fails` red, and adding one
to the `D \ L` branch turns
`test_the_signal_having_missed_one_reports_and_passes` red. Both directions
fail only where Q1 said they should.

**The inverted guard was read correctly.** All four release-gated steps opened:
the version bump (`:66`), the changelog gather (`:105`) and the ledger fold
(`:123`) skip on a base that is not `main`; the survivor check (`:232`) skips
on a base that **is** `main`. The new step at `:277` copies the three. A probe
inverting it turns `test_the_gate_runs_only_for_a_release_pull_request` red.

**The hotfix skip fires, and a skip is distinguishable from a pass only in the
log.** `test_a_head_that_is_not_a_release_branch_is_skipped_with_a_reason`
parametrises six head shapes including `hotfix/v1.2.4`, and asserts the gate
makes no call at all. The step is green either way and the difference is the
printed line — which is the right asymmetry, since a hotfix skip is routine
while an absent milestone is not, and only the latter uses `::warning::`.

**Import rather than copy, and the closer is untouched.**
`close_issues_on_release.py` is not in the diff. Both new scripts load it by
path and neither defines `CLOSING`, `MERGED_PR`, `FENCE` or `SPAN`; the
`# RIDER:` anchor on `FENCE` does not move. Loading runs nothing — the module
guards its `main`.

**The gate cannot write, and the guard is stronger than the source check
suggests.** `test_the_gate_writes_nothing` reads for literal `gh issue edit`
strings, which a call through the imported signal would slip past — but a probe
inserting `signal.add_label(repo, 88, version)` into `main()` turns five cases
red, because the fake tracker refuses the command. The property is held by the
fixture, not by the string search.

**No document this branch touched names a real version.**
`test_release_hygiene.py` is green, and every version in the new prose is
`X.Y.Z`.

## One thing this round could not settle

❓ **out of verified scope — whether `issues: read` reaches a pull request
body.** `hygiene.yml`'s new block is `contents: read` + `issues: read`, and the
gate reads pull request bodies through `GET /repos/{owner}/{repo}/issues/{n}`
(`close_issues_on_release.py#_issue_api`). The tree's precedent is one level
up: `close-issues-on-release.yml` holds `issues: write`, no `pull-requests`
scope, and its latest run read three pull request bodies and closed #84 —
**executed**, read out of the run log. A `GET` needs only the read level of the
permission a write level covers, so this very probably holds; it has not been
run.

The direction if it does not hold is worth stating, because the message would
misdirect: every body read returns 404, every number is skipped as "not a pull
request", D comes out empty, and the gate refuses the release naming the whole
milestone and telling the reader to do release planning.

**Who answers it: the repository owner, at the 0.11.1 release pull request.**
That is also the step's first execution in CI of any kind — the shell guard
skips every base that is not `main`, so nothing before the release pull request
runs the script at all.

⚠️ **The live tracker refuses today for a second reason.** The gate run against
`release: 0.11.1` names **#359 and #361**; the build's ledger row recorded #359
alone. #361 entered the milestone after the build. Either it ships in 0.11.1 or
it moves, before the release pull request opens. That is the gate working and
the checklist's new step 0 box asking for exactly this act.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The milestone existence read takes one unpaginated page, so above 100 milestones the gate prints `verified NOTHING` and passes — the fail-open the read exists to close. Unpinned: a probe gutting the query left 25 cases green | `.github/scripts/release_completeness_check.py:100` | open | Executed: 33 milestones today, so not reachable now; probe M7 survived |
| 2 | 🟡 The fork-point range collapses to `base..HEAD` in CI, because `actions/checkout` hands the job the pull request's merge ref. That is the spelling `questions.md` Q8 rejected | `.github/scripts/release_completeness_check.py:71-84`, `:236`; `.github/workflows/hygiene.yml:269-280` | open | Read, not executed. Cost today is nil — a hotfix into `main` closes its own issue, so it never sits in M — which is a usable answer if it is written next to the range |
| 3 | 🟡 A shipped document says the milestone act is "the first box on the list"; it is the third of four | `docs/issues-and-milestones.md:127-128` vs `docs/release-checklist.md:14,18,40,50` | open | Read. `phases/phase-4.md:58` shows the belief it came from, so it is a placement claim rather than a wording slip |
| 4 | 🟡 Q3's answerer is sent to a run that cannot reach the create path: `merged: 0.11.1` already exists, so this branch's squash exercises the add and skips the create | `overview.md` §*Not verified*; `questions.md` Q3 | open | Executed read-only: the label is on #351 since 2026-09-11T06:36:29Z, applied by hand by the repository owner |
| 5 | ⬜ `overview.md` says eight modules; nine were run, 171 cases | `overview.md:9` | open | Executed: 121 over six modules, 50 over three |
| 6 | ⬜ The gate step's `REPO` and `BASE` env entries are pinned by no case | `.github/workflows/hygiene.yml:269-280` | open | Executed: probes M16 and M17 both survived. Losing `REPO` is a loud `KeyError`; losing `BASE` is harmless |
| 7 | ⬜ A reverted squash stays in D | `.github/scripts/release_completeness_check.py:12-14` | open | Read. No release here has reverted a squash |
| 8 | ❓ Whether `issues: read` reaches a pull request body through the issues endpoint | `.github/workflows/hygiene.yml:20-22` | out of verified scope | Sibling precedent at `issues: write` executed and green; the read level is unrun. Answerer: the repository owner, at the 0.11.1 release pull request |
| 9 | 🟢 `M \ D` is recomputed from commits and no path falls back to labels; `L \ D` fails and `D \ L` reports, which is Q1's (c) | `.github/scripts/release_completeness_check.py#judge` | answered | Executed: probes M1 and M2 each turn their own case red |
| 10 | 🟢 The new step copies the three steps that guard on a base that is not `main`, not the inverted fourth | `.github/workflows/hygiene.yml:277` | answered | Executed: all four opened; probes M13 and M14 both red |
| 11 | 🟢 The hotfix skip fires and makes no call; a skip is distinguishable from a pass in the log, not in the check status | `.github/scripts/release_completeness_check.py:212-219` | answered | Executed: six head shapes parametrised, and the case fails on any call |
| 12 | 🟢 The readers are imported; `close_issues_on_release.py` is unchanged and its rider anchor does not move | `.github/scripts/label_merged_on_release_branch.py:77` | answered | Read: the closer is absent from the diff; neither new script defines the four patterns |
| 13 | 🟢 No document this branch touched names a real version | `docs/` | answered | Executed: `test_release_hygiene.py` 32 passed, exit 0 |
| 14 | ⬜ The prompt said `docs/branch-and-release.md` gained a paragraph for the hotfix. It gained one paragraph, about the second workflow reading the same keywords. The hotfix case lives in the script's docstring and in S7's cases, and no document paragraph was added for it | prompt vs `docs/branch-and-release.md` | withdrawn | Read: the file's only added hunk is §*A second workflow reads the same keywords earlier*. Not a defect of the build — the build never claimed it |
| 15 | ⬜ The prompt's "no survivors and therefore no `survivors.md`" is true of this work item; three other work items do carry one | `seal/specs/*/survivors.md` | answered | Executed: `survivor-check` exit 0 over 879 files |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on each of the nine modules the build touched, one module per call | 171 passed, exit 0 each; 165 over the eight the paragraph names |
| Mutation probe: 18 mutations across both scripts, the workflow step and the permissions block, each applied alone and reverted | **15 red**, 3 survived. Red: `L \ D` stops failing · `D \ L` starts failing · milestone existence read removed · range becomes `base..HEAD` · L read only in open state · M read in every state · issue and pull request swapped in `wanted` · label created unconditionally · per-issue label read dropped · branch regex widened · `DRY_RUN` ignored · step guard loses `exit 0` and `fi` · step guard inverted · token widened to `issues: write` · the M/D/L print dropped. Survived: the milestone query gutted to `repos/{repo}/milestones` · `REPO` dropped from the step · `BASE` dropped from the step |
| Coverage probe: `signal.add_label(repo, 88, version)` inserted into the gate's `main()` | 5 cases red — the fake tracker refuses the command, so the no-write property holds through the fixture rather than the source search |
| `release_completeness_check.py` against the live tracker, read-only, `HEAD_BRANCH=release/v0.11.1 BASE=origin/main` | **exit 1**. `M \ D` refusal naming **#359 and #361**; `M: #351, #359, #361`, `D: #351`, `L: #351` |
| `bin/evidence-check --strict`, whole tree | 1137 ok · 0 drifted · 0 broken, exit 0 |
| `bin/survivor-check --range origin/release/v0.11.1...HEAD` | exit 0 — 879 files against 8 removed sentences, no removed wording still standing |
| `ruff check` and `ruff format --check` on the four changed Python files | exit 0 each |
| `gh run view --log` on the latest `close-issues-on-release.yml` run | `pull requests in this push: [355, 352, 349]`, then `closed #84, named by #352` — a pull request body read with `contents: read` + `issues: write` and no `pull-requests` scope |
| `gh api repos/{owner}/{repo}/milestones?state=all&per_page=100 -q length` | 33 |
| The broad gate — `bin/test -q && ruff check . && ruff format --check .` | **not yet.** It is the sealer's, and it is contract §2's to hand out; this round ran nothing broad. It comes due once findings 1 to 4 are answered |

Every exit code above was read directly, never through a pipe.

## Paste-ready fixes

**Finding 1** — `.github/scripts/release_completeness_check.py`, and the
fixture that has to move with it.

```python
def milestone_titles(repo):
    """Every milestone this repository has, open or closed.

    Asked for separately because `gh issue list --milestone` answers a title
    nothing has with an empty list and exit 0 — measured. Without this read a
    mistyped or absent milestone would make the whole check pass while
    verifying nothing, which is the one direction a checker of claims must
    not fail in. `--paginate` for the same reason one level down: `per_page`
    caps at 100, and an unpaginated read of a repository with more milestones
    than that puts the title off the page and reaches the same fail-open
    through this function. `--jq` per page, because `--paginate` on an
    array endpoint concatenates arrays into something `json.loads` refuses.
    """
    out = closer.run(
        "gh",
        "api",
        "--paginate",
        "--jq",
        ".[].title",
        f"repos/{repo}/milestones?state=all&per_page=100",
    )
    return {line for line in out.splitlines() if line.strip()}
```

```python
# tests/test_a_release_cannot_ship_an_untrue_milestone.py, class Tracker.run
        if args[:2] == ("gh", "api"):
            return "\n".join(self.milestones) + "\n"
```

```python
# tests/test_a_release_cannot_ship_an_untrue_milestone.py — the case that was missing
def test_the_milestone_list_is_read_past_the_first_page(monkeypatch):
    """`per_page` caps at 100. An unpaginated read of a repository with more
    milestones than that leaves the title off the page, and the gate then
    prints `verified NOTHING` and passes — through the very function written
    to stop it passing on an empty set."""
    m = gate()
    tracker = Tracker(m=[88], label=[88], subjects=["feat: a thing (#100)"])
    wire(monkeypatch, m, tracker, {100: "Closes #88"})
    assert m.main() == 0
    call = tracker.call_with("gh", "api")
    assert "--paginate" in call, (
        f"the milestone list is read one page deep: {call}"
    )
```

**Finding 2** — `.github/scripts/release_completeness_check.py`. Measure from
the head the pull request actually names, so the fork point survives the merge
ref CI checks out.

```python
def main():
    head = os.environ.get("HEAD_BRANCH", "")
    version = signal.version_of(head)
    if version is None:
        # `docs/branch-and-release.md` lists a hotfix branch as the other
        # thing that reaches `main`, and a hotfix carries no release
        # milestone. Skipping is the answer rather than guessing a version.
        print(f"{head!r} is not a release/vX.Y.Z branch — nothing to judge")
        return 0

    repo = os.environ["REPO"]
    base = os.environ.get("BASE", "origin/main")
    # On a `pull_request` event `actions/checkout` checks out the merge ref —
    # the head merged into the base — so `HEAD` already contains `origin/main`
    # and `git merge-base origin/main HEAD` returns the base tip rather than
    # the fork point. That is the `base..HEAD` spelling `questions.md` Q8
    # rejected, arriving through the checkout instead of through the code. CI
    # passes the head commit; a session running this by hand has HEAD.
    point = os.environ.get("HEAD_SHA") or "HEAD"
    milestone = signal.milestone_title(version)
```

```python
    carried = set(
        signal.issues_in(repo, subjects_since(merge_base(base, point), point))
    )
```

```yaml
# .github/workflows/hygiene.yml — the gate step's env:, one line added
        env:
          GH_TOKEN: ${{ github.token }}
          HEAD_BRANCH: ${{ github.head_ref }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          BASE: origin/${{ github.base_ref }}
          REPO: ${{ github.repository }}
```

If the answer is instead that a hotfix into `main` closes its own issue and so
never sits in M, put that sentence in `merge_base`'s docstring — it is the
reason the collapse is affordable, and without it the docstring describes a
protection the job does not have.

**Finding 3** — `docs/issues-and-milestones.md`, the two lines at 127-128.

```markdown
`docs/release-checklist.md` step 0 is where that act belongs, and it is the
box directly above the one about other sessions in the checkout.
```

Moving the box to the top of step 0 instead would make the original sentence
true, and `phases/phase-4.md:58` is the argument for doing it that way.

**Finding 4** — `overview.md`, §*Not verified*, the Q3 row's `Who must answer`
cell.

```markdown
| the repository owner, at the first squash into `release/v0.12.0`. **Not this
release**: `merged: 0.11.1` already exists on the tracker — applied by hand
before this work item was built — so the signal's read finds it and the create
path is skipped. This branch's own squash answers `--add-label` alone |
```

And the same correction in `questions.md` Q3's Status cell, replacing
*by watching this branch's own squash into `release/v0.11.1`*.

---

Needs a fix: yes — findings 1, 2, 3 and 4. One is a fail-open a probe left
standing, one is a range guarantee the CI checkout undoes, one is a shipped
sentence pointing at the wrong box, and one is an unverified row sent to a run
that cannot answer it.

Loses a record or crashes: no

---

## Proof

**Opened in full** — `.github/scripts/release_completeness_check.py`,
`.github/scripts/label_merged_on_release_branch.py`,
`.github/scripts/close_issues_on_release.py`,
`.github/workflows/hygiene.yml`,
`.github/workflows/label-merged-on-release-branch.yml`,
`.github/workflows/close-issues-on-release.yml`,
`tests/test_a_merged_ticket_says_so_on_the_tracker.py`,
`tests/test_a_release_cannot_ship_an_untrue_milestone.py`, `bin/test`, and
this work item's `round-1-asked.md`, `overview.md`, `questions.md`,
`changelog.md`, `phases/phase-3.md`, `phases/phase-4.md`, and its ledger
fragment.

**Opened in part** — `docs/branch-and-release.md`, `docs/issues-and-milestones.md`,
`docs/release-checklist.md` (the diff in full, plus step 0 and the hotfix rows),
`spec.md` §*Acceptance*, `tests/test_release_hygiene.py` (its `LOADED` and the
comment above the version pattern), GitHub issue #359.

**Read as output, not as source** — the live tracker, read-only: the milestone
list, #351's labels and timeline, and the latest `close-issues-on-release.yml`
run log. Nothing was written to the tracker.

**Not opened** — `plan.md`, `phases/phase-1.md`, `phases/phase-2.md`,
`phases/phase-5.md`, `routing.md`. Their claims reached this round through
`overview.md`, `questions.md` and `round-1-asked.md`, and every one this report
relies on was re-derived from the code.

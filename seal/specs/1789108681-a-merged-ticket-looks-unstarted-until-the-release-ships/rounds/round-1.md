# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — review round 1

| Field | Value |
|---|---|
| Target SHA | 9a010fd1fbbe2cd3ece35a3956def2b165d0e5e3 |
| Ran by | specseal:warden on Opus 5 |
| PR | #360 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | test_the_range_is_measured_to_the_head_the_pull_request_names (depth 1); test_without_a_named_head_the_range_ends_at_HEAD (depth 1); test_the_milestone_list_is_read_past_the_first_page (depth 1); test_every_input_the_script_reads_is_handed_to_it_by_the_step (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4. One is a fail-open a probe left standing, one is a range guarantee the CI checkout undoes, one is a shipped sentence pointing at the wrong box, and one is an unverified row sent to a run that cannot answer it. |
| Loses a record or crashes | no |
<!-- New units: .github/workflows/hygiene.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

# round 1 — the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `9a010fd` — every measurement below was taken there |
| Review at | HEAD of the branch, which adds only this paragraph on top of the target |
| Base | `origin/release/v0.11.1` = `f9c6907` |
| Draft pull request | #360, opened before this round |
| Ran by | specseal:warden on Opus 5 |

## Scope

Issue #359 — a squash into a release branch labels what it answered, and a
release pull request is refused while its milestone claims work the release
has not got. Nine commits, `ae0d276` through `9a010fd`, on the frame commits
`a01d679` and `fe2c3bc`.

Two new modules, two new `.github/scripts`, one new workflow, one edited
workflow, three edited documents.

## Facts, with labels

**Executed by the orchestrating session** at `9a010fd`, exit codes read
directly with no pipe:

- `bin/test -q` over `tests/test_a_merged_ticket_says_so_on_the_tracker.py`,
  `tests/test_a_release_cannot_ship_an_untrue_milestone.py`,
  `tests/test_ci_gives_the_checks_what_they_need.py`,
  `tests/test_one_word_one_meaning.py`, `tests/test_docs_line_wrap.py`,
  `tests/test_release_hygiene.py`, `tests/test_no_real_identifiers.py`,
  `tests/test_the_rules_have_one_owner.py` → **165 passed, exit 0**.
- `uvx ruff check` and `uvx ruff format --check` over the four changed Python
  files → **exit 0** each.

**Executed by the builder**, its own numbers, in `overview.md`: 306 cases
across 13 modules; the gate run four ways against the live tracker including
a real refusal naming #359; **19 mutations each seen red**, one of which
found a weak case of its own; `survivor-check`, `unverified-check` and
`evidence-check --strict` (1137 rows) each exit 0. Re-derive rather than
inherit — in particular the mutation count and the claim that each was seen
red.

**Executed, and it is the reason phase 3's step is shaped as it is** —
`gh issue list --milestone "release: 9.9.9" --state open` returns `[]` and
**exits 0**. A mistyped or absent milestone would otherwise make the gate
pass by measuring an empty set.

**Read** — the frame said `hygiene.yml` holds four release-only steps each
opening with the same guard. Three do; the fourth opens with the inverted
guard and skips on `main`. The builder recorded this as a frame divergence.

**Read, and it constrains every document edit** — `tests/test_release_hygiene.py`'s
`LOADED` includes `docs/`, so a real version in prose goes red at the release
preparation commit. `.github/` is outside `LOADED`.

**Unverified, and both are rows in `## Not verified`** — whether the workflow
token's `issues: write` covers label *creation*, and whether the signal fires
as specified. Both need a real run on a release branch, which this branch's
own squash produces. Do not try to settle them by writing to the tracker.

**Unverified** — the broad gate. It is the `sealer`'s, after this chain
settles.

## Two answers a person gave, which are not yours to reopen

**Q1 — (c).** `L \ D` fails, `D \ L` reports. Judge whether the code does
that, not whether it is the right answer.

**Q2 — (a), already done.** `release: 0.11.1` holds #351 and #359 alone. The
frame's `plan.md` and `questions.md` say nine at `a01d679`; that was true
then and the move happened after. A note in those files that reads as stale
is a correction, not a defect of the build.

## Where a claim flips on measurement point

The gate's refusal set is `M \ D` — the milestone's open issues minus what
the release branch carries — and `D` is recomputed from the branch's commits
rather than read from labels. Measuring the gate against labels instead
reproduces the defect the design rejects. Measure at the commits.

## The commands, in the form to use

`bin/test`, narrow, one module at a time. `bin/evidence-check --strict`,
never narrowed to this work item's fragment.
`bin/survivor-check --range origin/release/v0.11.1...HEAD` — the builder
reports no survivors and therefore no `survivors.md`; check that.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The milestone existence read takes one unpaginated page, so above 100 milestones the gate prints `verified NOTHING` and passes — the fail-open the read exists to close. Unpinned: a probe gutting the query left 25 cases green | `.github/scripts/release_completeness_check.py:100` | **fixed** `8ca5569` | fixed at 8ca5569 — ``. `--paginate` added to the milestone read, and `test_the_milestone_list_is_read_past_the_first_page` planted. **The paste-ready fix was not taken whole:** it also added `--jq .[].title`, on the stated grounds that `--paginate` over an array endpoint concatenates arrays into something `json.loads` refuses. Executed on gh 2.92 — `gh api --paginate "…/milestones?state=all&per_page=2"`, seventeen pages, `json.loads` returns one list of **33** — so `--paginate` merges and that premise is false. The flag is not added and the docstring records the measurement, including that a gh old enough to concatenate would make `json.loads` raise, which is loud rather than a short list. Three mutations red: flag dropped, page size lowered below the maximum, and the whole query gutted — the last is the probe round 1 reported surviving; Executed: 33 milestones today, so not reachable now; probe M7 survived |
| 2 | 🟡 The fork-point range collapses to `base..HEAD` in CI, because `actions/checkout` hands the job the pull request's merge ref. That is the spelling `questions.md` Q8 rejected | `.github/scripts/release_completeness_check.py:71-84`, `:236`; `.github/workflows/hygiene.yml:269-280` | **fixed** `8ca5569` | fixed at 8ca5569 — ``, and the range is made true in CI rather than the docstring made weaker. The step passes `HEAD_SHA: ${{ github.event.pull_request.head.sha }}` and `main` measures the range to it, so the fork point survives the merge ref; with no such variable the fallback is `HEAD`, which is a branch tip for a session running it by hand. **Why this over documenting the collapse:** the hotfix sentence at `docs/branch-and-release.md:218` is true and is why the collapse costs nothing *today*, but it makes the guarantee contingent on a fact about hotfixes rather than on the range, and `merge_base`'s docstring would still be describing a protection the job does not have. Two new cases — the named head, and the control that catches the first one lying — plus four mutations red, including threading the head into only one of the two commands. The docstring now carries the whole reading; Read, not executed. Cost today is nil — a hotfix into `main` closes its own issue, so it never sits in M — which is a usable answer if it is written next to the range |
| 3 | 🟡 A shipped document says the milestone act is "the first box on the list"; it is the third of four | `docs/issues-and-milestones.md:127-128` vs `docs/release-checklist.md:14,18,40,50` | **fixed** `8ca5569` | fixed at 8ca5569 — ``. **Content-addressed rather than positional**, which is a step past the paste-ready text. That text pointed at "the box directly above the one about other sessions in the checkout", which breaks again the moment a box is added; the sentence now names the box by what it asks. **The order was left alone on its own grounds**, against `phases/phase-4.md:58`'s argument for moving it: boxes 1 and 2 confirm what arrived, and a milestone cannot be checked against a release until you know what is in it, so third is the right place and the sentence was the wrong claim. Counted before editing — boxes at `docs/release-checklist.md` lines 14, 18, 40, 50; Read. `phases/phase-4.md:58` shows the belief it came from, so it is a placement claim rather than a wording slip |
| 4 | 🟡 Q3's answerer is sent to a run that cannot reach the create path: `merged: 0.11.1` already exists, so this branch's squash exercises the add and skips the create | `overview.md` §*Not verified*; `questions.md` Q3 | **fixed** `8ca5569` | fixed at 8ca5569 — ``, in both `overview.md` §*Not verified* and `questions.md` Q3. The answerer is now "the first squash into a release branch whose `merged: X.Y.Z` label does not yet exist — not this one", with the reason: the label was created by hand before the build, so the signal's read finds it and skips the create. **The version is deliberately not named**, where the paste-ready text wrote `release/v0.12.0`: `docs/branch-and-release.md` says whether the next number is a minor or a patch is known at the end and not at the cut, so a named version is a prediction. Both cells also say this branch's squash still answers `--add-label`, which is worth watching for its own sake; Executed read-only: the label is on #351 since 2026-09-11T06:36:29Z, applied by hand by the repository owner |
| 5 | ⬜ `overview.md` says eight modules; nine were run, 171 cases | `overview.md:9` | **fixed** `8ca5569` | fixed at 8ca5569 — ``. Re-derived rather than taken: `test_docs_line_wrap` 23, `test_one_word_one_meaning` 13, `test_release_hygiene` 32, `test_no_real_identifiers` 2, `test_the_rules_have_one_owner` 45, `test_a_question_says_who_can_answer_it` 6 = **121 over six**; `test_a_merged_ticket_says_so_on_the_tracker` 23, `test_a_release_cannot_ship_an_untrue_milestone` 25, `test_ci_gives_the_checks_what_they_need` 2 = **50 over three**. Nine modules, 171 cases, exactly as the round says. The line now reads nine, gives both figures, says it said eight until round 1 counted, and carries the post-fix total of 175; Executed: 121 over six modules, 50 over three |
| 6 | ⬜ The gate step's `REPO` and `BASE` env entries are pinned by no case | `.github/workflows/hygiene.yml:269-280` | **fixed** `8ca5569` | fixed at 8ca5569 — ``, and the round's own judgment — a note, because losing `REPO` is a loud `KeyError` and losing `BASE` is harmless — was right until finding 2's fix landed. `HEAD_SHA` is the third kind: losing it is **silent**, falling back to `HEAD`, which in CI is the merge ref, which puts finding 2 back with nothing saying so. `test_every_input_the_script_reads_is_handed_to_it_by_the_step` covers all five entries rather than that one, because a reader deleting a line does not first ask which kind it is. Four mutations red, one per entry plus one that points `HEAD_SHA` at the merge ref's own sha; Executed: probes M16 and M17 both survived. Losing `REPO` is a loud `KeyError`; losing `BASE` is harmless |
| 7 | ⬜ A reverted squash stays in D | `.github/scripts/release_completeness_check.py:12-14` | answered | Disclosed at the coordinate rather than changed, at `8ca5569`. The module docstring's definition of D now says a reverted squash stays in it, why — the revert's subject carries the revert pull request's own `(#N)` and its body carries no closing keyword, so nothing subtracts the original claim — and what it would cost: the issue sits in D, out of `M \ D`, and the release ships claiming work it no longer has. The behaviour is unchanged, so this is not `fixed`: no release here has reverted a squash, and subtracting reverts would need a second reader of revert bodies, which is mechanism a fix pass may not add |
| 8 | ❓ Whether `issues: read` reaches a pull request body through the issues endpoint | `.github/workflows/hygiene.yml:20-22` | deferred seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md §Not verified | seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md §Not verified |
| 9 | 🟢 `M \ D` is recomputed from commits and no path falls back to labels; `L \ D` fails and `D \ L` reports, which is Q1's (c) | `.github/scripts/release_completeness_check.py#judge` | answered | Executed: probes M1 and M2 each turn their own case red |
| 10 | 🟢 The new step copies the three steps that guard on a base that is not `main`, not the inverted fourth | `.github/workflows/hygiene.yml:277` | answered | Executed: all four opened; probes M13 and M14 both red |
| 11 | 🟢 The hotfix skip fires and makes no call; a skip is distinguishable from a pass in the log, not in the check status | `.github/scripts/release_completeness_check.py:212-219` | answered | Executed: six head shapes parametrised, and the case fails on any call |
| 12 | 🟢 The readers are imported; `close_issues_on_release.py` is unchanged and its rider anchor does not move | `.github/scripts/label_merged_on_release_branch.py:77` | answered | Read: the closer is absent from the diff; neither new script defines the four patterns |
| 13 | 🟢 No document this branch touched names a real version | `docs/` | answered | Executed: `test_release_hygiene.py` 32 passed, exit 0 |
| 14 | ⬜ The prompt said `docs/branch-and-release.md` gained a paragraph for the hotfix. It gained one paragraph, about the second workflow reading the same keywords. The hotfix case lives in the script's docstring and in S7's cases, and no document paragraph was added for it | prompt vs `docs/branch-and-release.md` | withdrawn | Read: the file's only added hunk is §*A second workflow reads the same keywords earlier*. Not a defect of the build — the build never claimed it |
| 15 | ⬜ The prompt's "no survivors and therefore no `survivors.md`" is true of this work item; three other work items do carry one | `seal/specs/*/survivors.md` | answered | Executed: `survivor-check` exit 0 over 879 files |

## Paste-ready fixes

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
```markdown
`docs/release-checklist.md` step 0 is where that act belongs, and it is the
box directly above the one about other sessions in the checkout.
```
```markdown
| the repository owner, at the first squash into `release/v0.12.0`. **Not this
release**: `merged: 0.11.1` already exists on the tracker — applied by hand
before this work item was built — so the signal's read finds it and the create
path is skipped. This branch's own squash answers `--add-label` alone |
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

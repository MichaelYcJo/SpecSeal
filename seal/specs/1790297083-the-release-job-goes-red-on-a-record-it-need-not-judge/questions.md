# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — questions for the planner

<!-- seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/questions.md -->

**No row here blocks the build, and none needs a person.** The owner pressed
`automation` for the whole of milestone 46, so the frame decided whatever the
tree could decide. The rows below belong to the work.

## Decided from the tree during framing — listed so nobody reopens them

Each decision below has its grounds in `spec.md` or in `plan.md`'s
Alternatives table. Anyone can overturn one by opening what the frame opened.

| Left open by | The judgment | Decided | Grounds |
|---|---|---|---|
| #598, instance 4, *"What to decide"* | Should `Pass` beside `nobody` read the draft state, print, or move earlier? | It reads the draft state: a notice in a draft, a refusal at ready and at unknown | #296's shape for the missing-record arm; `orchestration.md`'s *"a check that is red for following the document beside it"*. The round-record-spec reason (*"a checker it does not have"*) is true of every other refusal in the row and false of `nobody — <why>` in the window. The owner's Q1 answer on `1788212517` is kept at ready |
| #598, instance 4 | Is the window really inside the draft? | Yes | **Executed**: GitHub timelines of #587, #588 and #595 show every round commit before `ready_for_review` |
| #598, instance 1, *"What to decide"* | Compare against `main`, or against something else? | Against the merge base's own history, by blob at the same path | `docs/commit-review-gate-spec.md`: *"the review it records was enforced at the pull request that added it"*. A branch name is not the rule; the base's history is |
| #598, instance 1 | Any blob the path ever held, or only the last one? | Any | `plan.md` Alternatives. Every version in the history was added by an earlier pull request |
| #598, instance 1 | Does the relaxation reach `written_late`? | Yes, silently | `docs/review-chain-spec.md` defines that arm's *no claim* by pointing at reachability's (§12, one class) |
| #598, instance 1 | Does the predicate turn #597's real refusals into restorations? | Yes, all four records | **Executed**: `git log --full-history --find-object` against #597's fork `6256bbc8` finds each blob at `a211a5d7` and `c52e8350` |
| #529, *"Not measured"* | Does `--full-history` list the merge commit as an `A` in the common shapes? | No | **Executed** in scratch repositories (S2, S3, S3b). `git log` does not diff a merge without `-m` |
| #529 (found by the frame) | Is `--full-history` enough? | No. `--topo-order` too | **Executed**: S7, a side branch dated earlier than the early add, puts the early add first under `--full-history` alone |
| #529 | Latest add, or earliest add of the current content? | Latest, as documented | `docs/review-chain-spec.md`'s delete and re-add row |

## Rows still open

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Which `chain_check.py#main` and `#checked_by` ledger rows drift, and does each claim still hold after the edit? | the work | Re-stamp with a dated note where the claim holds; correct it in place with a `Corrected <date>` note where the edit made it false | Phase 4 runs `evidence_check.py`, re-reads each DRIFTED row, and records what it found in `phases/phase-4.md` | ✅ fifteen rows in seven files drifted, every claim still holds, and each took a dated `Re-read 2026-09-25` note and a scoped `--reverify`; none needed `Corrected` (`phases/phase-4.md` lists them) |
| Q2 | How does `written_late` learn the restoration: a `fork` argument, or a restored set computed once in `main`? | the work | A `fork` argument keeps the function self-contained. A set computed once saves one `git log` per record | Whichever keeps one predicate with one definition; phase 2 lists the call sites it changed | ✅ a `fork` argument: `restored_from(root, fork, rel)` is the one definition, asked at `main`'s reachability decision and inside `written_late`, which `main` now calls with its `fork` (`phases/phase-2.md`) |
| Q3 | Does any existing case already build a merge on the branch, so that A3 needs no new case? | the work | If one does, name it in `phases/phase-1.md`. If none does, add the S3 case | Add the S3 case | ✅ none does — the five merges in `test_chain_check_at_the_pull_request.py` are retirement fixtures that never reach `written_late`, so the S3 case was added as A3 (`phases/phase-1.md`) |
| Q4 | Does work item C's edit to `main` collide textually with A's? | the work | A leaves `load` and the `try`/`except` around it alone. Any remaining conflict is resolved when C merges the release branch in | C resolves after A squashes (milestone order) | ✅ not in `chain_check.py`: C at `127dbe64` has not edited it. Likely in `seal/releases/0.14.0.md`, where C edits lines 36, 39 and 45 and A edits 35 and 42; C resolves it hunk by hunk after A squashes (`phases/phase-4.md`) |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.

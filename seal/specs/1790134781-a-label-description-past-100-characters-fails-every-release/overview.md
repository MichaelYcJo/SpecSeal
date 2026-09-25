# 1790134781-a-label-description-past-100-characters-fails-every-release — overview

📋 implement applied
· spec:     `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move* (the `size: now` paragraphs, and *One thing reads it, and only to spend it*); `.github/scripts/tracker_labels.py` module docstring and the comment above `LABELS`; `.github/scripts/label_merged_on_release_branch.py#label_description`; `CONTRIBUTING.md` §*Changing cited code is the case the rule has to answer*; `skills/evidence-check/SKILL.md` §*Verdicts and what to do*; #515's body
· evidence: `seal/ledger/1790134781-a-label-description-past-100-characters-fails-every-release.md` C1 added, and C2 added in round 1's fix pass; `seal/ledger.md` T2 re-read (`--reverify` on its drifted anchors — two at the build, the workflow step's at the fix pass — Checked moved to 2026-09-23, a `Re-read` marker in Notes)
· verified: executed — both case files (44 passed), the new cap case red on the 119-character value, four single-unit mutations (one of them run twice, because its first try was sized short of the cap and stayed green), the workflow-condition case red with each condition removed and green with both, `ruff check` and `ruff format --check` on the four changed files, `evidence-check .` (1473 ok, 0 drifted); read — the specifying section, the scripts, #515, GitHub's REST reference for *Create a label* for the cap's value, and GitHub's expressions reference for the default `success()` and `cancelled()`; unverified — how a real runner evaluates `!cancelled()` after a failed step, the live tracker, the broad gate

## Scope confirmation

Shorten one declared label description to fit GitHub's 100-character cap, and pin every label description this repository sends to `gh label create` under that cap; and, from round 1, stop a failed step in the close-issues workflow from skipping the label step and the roll behind it.

## Why this work exists

The first release to reach `main` after `size: now` was declared failed the close-issues workflow at label creation, which skipped the flow-measurement roll; the description now fits, and the suite refuses the next one that does not.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The description is no longer the document's whole sentence | `docs/issues-and-milestones.md`: "**`size: now` says this ticket has to be in effect before the next work item starts.**" The declared description carried that plus the removal clause in 119 characters. Now: "Has to be in effect before the next work item starts; removed when its release closes the issue" (95) | the shortened text | The two properties `tracker_labels.py`'s comment asks for — what the label means, and when it stops being the current answer — both survive, in the document's own words for the first. What went is the subject ("This ticket"), which a label on an issue always has, and "the release carrying it", which `its` still names. The comment above `LABELS` now says why it is a clause rather than the sentence |
| The removal moment is worded by the close, not by `main` | The document: the workflow "removes `size: now` from each issue it closes when the release reaches `main`". The description says "removed when its release closes the issue" | kept the close | This was the previous description's wording too, and it is the event a person sees on the issue. A release reaching `main` is what triggers the close, so the two name one moment; the A9 case's second literal moved with the text |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ GitHub's cap is 100 characters. Taken from the 422 quoted in #515's body; the cited run `35796513013` returns 404 on this repository, so the log itself was not opened | read 2026-09-23: GitHub's REST reference for *Create a label* says `description` "Must be 100 characters or fewer" — read by round 1's reviewer and re-read in the fix pass; ledger row C1 |
| ✅ GitHub evaluates `if: ${{ !cancelled() }}` so that the label step and the roll run after an earlier step fails | read 2026-09-24: run `35871516188`, the 0.14.0 merge to `main`: `close every issue this release's pull requests claimed` failed, then `create the labels …` and `roll the flow-measurement issue …` both succeeded |
| ✅ `size: now` gets created on the live tracker and #496 rolls to the next version | read 2026-09-24: `gh label list` shows `size: now`; #496 is closed and #535 (*after 0.14.0*) was opened by that run |
| ✅ The full suite, the repository-wide lint and the typecheck | `rounds/round-3.md`'s `Broad gate` row: the sealer's run at c4e005b against 1bafeb7 |

## Not done

- **Label names are not pinned under GitHub's name cap.** A label's name is capped too, and it goes to the same `gh label create` call, so it is plausibly the same class. It is not pinned: GitHub's REST reference for *Create a label* states no limit for `name` (read 2026-09-23), so there is no documented number to name, and a constant with a guessed value is worse than none. The two names in the tree are 9 characters and `merged: X.Y.Z`. This names nobody who will act, so it stays here and in the pull request body.
- **No runtime refusal in `create` or `create_label`.** A check before the `gh` call would still fail the workflow after the merge; the case refuses the value before it, which is where the defect has to be caught.
- **Where the constant lives.** `LABEL_DESCRIPTION_LIMIT` sits beside `label_description` in `label_merged_on_release_branch.py`, because `tracker_labels.py` already imports that module as `signal` and the reverse import does not exist. Both cases read it from there.
- **`label_description` is judged the same class and pinned.** It goes to the same call and is refused the same way. It had 20 characters to spare at `9999.9999.9999`, so it was not broken; the case exists so a longer template is refused by the suite rather than by the tracker.
- **The roll #515 says was skipped is not repaired by hand here.** It happens at the next release reaching `main`, and since round 1 it no longer waits on the label step succeeding.

## Fed back into the spec

none — no `spec.md` at this rung, and `docs/issues-and-milestones.md` does not quote the description, so nothing in it changed.

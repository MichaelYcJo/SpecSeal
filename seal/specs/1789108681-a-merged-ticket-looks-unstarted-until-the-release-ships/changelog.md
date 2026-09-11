<!-- seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A ticket already merged into the release branch now says so on the
  tracker, and a release can no longer ship a milestone that is not true.**
  An issue's state does not move until `main` moves, and `main` moves once per
  release — so for the length of a release a finished work item and one nobody
  has started looked identical. The line that used to tell them apart was a
  bullet in a checklist every branch edited, and it was deleted with that file
  in the release before this one. Two pieces answer two different questions:

  - **A signal, so a person can tell them apart.** A push to `release/*` runs
    `.github/scripts/label_merged_on_release_branch.py`, which reads the pull
    request numbers out of the commit subjects that arrived, fetches those
    bodies, and puts `merged: X.Y.Z` on every issue their closing keywords
    name. One query answers *what is already in*. It closes nothing: an issue
    closed at the release-branch merge is closed for something nobody has
    received, and the close stays where it was, on `main`. It removes nothing
    either — the labels accumulate, one per release, because deleting a label
    deletes it from every issue that ever carried it.
  - **A gate, so a release cannot ship a milestone that claims work it has not
    got.** A pull request from `release/vX.Y.Z` into `main` runs
    `.github/scripts/release_completeness_check.py`, which refuses while the
    milestone holds an open issue the release branch does not carry, and names
    each one. This is the completeness check the deleted checklist asked as
    *is everything in*, now asked by the machine at the moment the release is
    being cut.

  **The commits are the truth and the label is a cache of them.** The gate
  recomputes what the release carries from the release branch's own range and
  never asks the labels, so a label write that failed cannot block a release —
  the remedy for that would be a person adding a label by hand, which is the
  act the signal exists to remove. The gate does compare the two and says
  which way they disagree: a label naming a release the issue is not in fails,
  because that is always a hand-edit or a squash subject that lost its `(#N)`
  and one command repairs it, while a missing label only reports.

  Neither piece parses anything new. Both read through
  `close_issues_on_release.py`'s existing readers rather than a second copy of
  its treatment of a keyword quoted inside a code fence.

  **A shape the gate cannot judge passes and says why.** A hotfix branch is
  the other thing that reaches `main` and it carries no release milestone. So
  does a milestone that does not exist, and that one says loudly that it
  verified nothing: `gh issue list --milestone` answers a title nothing has
  with an empty list and exit 0, so without a separate existence read a typo
  would have passed the check by measuring an empty set.

  **What a release has to do differently.** `docs/release-checklist.md` step 0
  gains the first box on the list: before anything else, every open issue in
  the milestone that is not shipping moves to another milestone. Leave it and
  the release pull request goes red at step 5 — which is the check working,
  at the worst moment to be doing release planning.

  Two sentences that were false are gone with it. The checklist said the
  close-issues workflow "runs on the tag and closes every issue the changelog
  section names"; it runs when `main` moves and it reads pull request bodies.
  And `docs/issues-and-milestones.md` said *nothing automated reads a
  milestone*, which this change is what makes untrue — that section now says
  what reads one, and that a wrong one costs a blocked release rather than a
  person's wrong answer. (#359)

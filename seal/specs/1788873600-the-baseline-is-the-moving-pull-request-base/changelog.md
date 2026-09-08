- **Squashing one work item turned every sibling branch red, and the message
  was right about what it measured.** `unverified-check --baseline REF` refuses
  when a work item's `overview.md` was present at the baseline and is gone on
  the branch — an honest arm, because deleting the file was otherwise cheaper
  and quieter than deleting one row from it. But `REF` is the branch a pull
  request merges into, and that branch moves: the moment one work item squashes
  into a release branch, every sibling branch cut before that squash has the
  squashed item's `overview.md` at the base and never had it at all. So each
  sibling was told that rows had left the record when nothing had left and the
  base had moved. On the release that found this, three of four branches paid a
  release-branch merge, a re-run broad gate, a re-pushed pull request and a
  documentation conflict each, and the cost grows with roughly the square of
  the work items a release carries.

  **The baseline is now the fork point.** `REF` is resolved once, to
  `git merge-base REF HEAD`, and every read of the base uses that commit: a row
  present where this branch forked and absent now was removed by this branch,
  which is the only claim the tool makes, and a row that arrived on the base
  afterwards is not this branch's business. Rebasing the stale branch was never
  the way out — every round record names its branch's commits by `Target SHA`
  and every rider carries a `Verified … at <sha>` stamp, and a rebase orphans
  both.

  The repair is applied where the ref is resolved rather than at the arm that
  reported it, because the row-count arm reads the base revision too, through
  `git show REF:<path>`: a base that gains a row in this branch's own overview
  after the fork reported rows the branch never had. Two arms of one refusal
  reading two revisions is the duplicated-reader split this module has closed
  four times, so there is one resolution point and one revision in the report.

  A report names the revision it compared against in the shortest form that is
  true: the ref alone where the merge base is the ref's own commit, and
  `the merge-base of <ref> and HEAD (<short>)` where the base has moved past
  the fork. A `REF` that shares no history with `HEAD` is exit 2 beside the
  `REF` that does not resolve, because a comparison against nothing is not a
  comparison. `docs/release-checklist.md` step 0 carried the workaround and no
  longer needs to; the never-rebase rule that was written inside it stays, as
  the standing rule it always was. (#272)

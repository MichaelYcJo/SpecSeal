- **The release before this one shipped four work items and folded none of
  them; this is the second fold, and it retires all four (issue #514).**
  Their standing rules are written into `docs/`: the release tail's rule —
  every act after the tag belongs to a machine the tag push fires — into
  `docs/branch-and-release.md`; the first fold's four rules for the ungrouped,
  for ledger rows anchored inside a retired directory, for population floors
  and for the wrap limit into `docs/the-evidence-ledger.md`; the review cap's
  rules marked where `docs/review-chain-spec.md` already states them; and the
  command that posts a reading, with the rule that it is not a hook, into
  `docs/measuring-a-run.md` and `docs/the-agent-set.md`. Then
  `settle --retire` removes the four directories — 71 files — and
  `seal/specs/` goes from 16 directories to 12, the 11 kept by name and this
  work item's own.

  **Every open leftover of the four was given a home before its directory
  went.** A retired `overview.md` is read as folded, so an open row inside one
  would have vanished unnoticed. The measured instance is the release
  workflow's label step, which failed on the tracker's description limit and
  skipped the flow-log roll after it; that is #515 now. The two refusal
  messages that still say a finding *becomes an issue* are named in
  `docs/review-chain-spec.md` beside the ladder they lag, with the repository
  owner as who decides them.

  **A path into a retired directory is cited by its work item, not by a
  commit.** Four test docstrings and one `docs/` sentence named phase records
  this fold removes; each now names the work item and the `docs/` section
  carrying its marker. No floor literal was lowered, and every module reading
  the real `seal/specs/` passes against the folded tree.

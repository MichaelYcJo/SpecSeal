### Added

- `chain-check` names the commits a work item's changelog fragment was left
  behind by (#797). For a work item declared `through the review chain`, it
  walks the first-parent commits after round 1's `Target SHA`, skipping
  merges. Every commit that changed a path outside `seal/` and outside a
  `tests` directory after the item's `changelog.md` last changed is named in
  one notice. Each is listed with its short SHA, up to three of its paths,
  and the round whose `Fix range` holds it, or *after the last round*. The
  notice says the release gathers the fragment as it stands and that nothing
  is owed where it still says what ships. It prints and never refuses, so no
  exit status moves. It reaches a person at `round-record close`, at
  `round-record seal` and in CI. Measured over 42 work items, a refusal would
  have stopped 24 runs, at least 9 of them for a fragment that needed no
  change. The three fragments of 0.18.2 that #795 corrected by hand would each
  have been named before the release. The notice is silent for a work item
  `straight to the PR`, before `round-1.md`, where round 1's `Target SHA` is
  gone or off the branch, and where no `changelog.md` is committed.
- The rule has one home, `docs/the-record-layout.md` §*A commit after the
  build brings its changelog fragment along*: a commit after the build that
  changes what the work item ships updates its `changelog.md` in the same
  range. The smith's fix pass, the implement skill §5 and the review
  orchestrator's fix-pass section link it. The orchestrator's section names
  the two commits that are the orchestrator's own, a fix after the last round
  and the commit that integrates a sibling's squash.

### Fixed

- The close-issues workflow no longer fails after every release at the step
  that creates the labels the documents specify: `size: now`'s description
  was 119 characters and GitHub refuses one past 100, so the label was never
  created and the step behind it, rolling the flow-measurement log, was
  skipped. The description now says the same two things — the ticket has to
  be in effect before the next work item starts, and it comes off when its
  release closes the issue — in 95. The cap is named once, and a case holds
  every declared description and the `merged: X.Y.Z` description under it,
  so the next one that is too long fails the suite instead of the release.
  A failed step in that workflow also no longer skips the steps behind it
  that do not need it: the label step and the flow-measurement roll now run
  unless the job was cancelled, so the next refusal of any kind costs a red
  job and not a release's roll.
  (`1790134781-a-label-description-past-100-characters-fails-every-release`,
  #515)

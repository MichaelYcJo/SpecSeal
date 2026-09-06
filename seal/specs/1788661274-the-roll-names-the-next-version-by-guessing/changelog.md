- **A release rolls the measurement log only where a new version has actually
  shipped, and the log is named after the version it rolled from.** The old
  arithmetic guessed the next number — `0.8.1` became `0.9.0` — and at the
  0.8.1 release that guess closed #166, which had been opened at the 0.8.0
  release and held the measurements 0.8.1 had just been written with, then
  opened #172 under the identical title. Two issues with one name, one of
  them closed, and the readings carried across by hand. The roll now reads
  the open log's title for the version it says it rolled from and compares
  that with the version in the checked-out tree: equal means this push
  shipped nothing new — a re-run of the job, or a merge that moved no
  version — and the run closes nothing, opens nothing, and exits 0 saying so.
  `docs/branch-and-release.md` is why the title states a fact instead of a
  prediction: whether the next number is a minor or a patch is known at the
  end and not at the cut, so at the moment the roll runs the just-shipped
  version is the one thing certain and the next one is the one thing nobody
  can name. `next_version` is deleted with the guess it made. **Both
  outcomes leave the job green**, so each prints a line — `rolled:` names the
  issue closed and the title opened, `nothing due:` names the log and the
  version — and a reader of the release log tells them apart without opening
  the tracker. **A title the script cannot read as its own is due rather than
  silent**, and that direction is chosen rather than incidental: read as
  *not due*, an unreadable title stops the log forever with the workflow
  green, which is the failure being fixed one step over; read as *due*, it
  costs at most one roll that was not owed. (#155)
- **What a log's title means now, and what the older ones mean.** A rolling
  log is titled `chore: flow measurement — after 0.8.2`, and the version in
  it is the one the log rolled from: that log opened at the 0.8.2 release,
  holds what was measured since, and is closed by whatever ships next. A
  title written before this change names the version the log was **predicted
  to be for**, which is how a 0.8.1 release came to close a log titled for
  0.9.0. Those are **not rewritten** — a retitle falsifies every comment that
  cites them — and the marker the roll now writes appears in none of them, so
  each of them reads as a title stating no version at all, which is always
  due. The first release after this change rolls the last old-convention log
  and the convention retires itself. `docs/issues-and-milestones.md` carries
  the format, the condition and both meanings; `skills/verify/SKILL.md` gains
  the boundary it was missing, since a rolling log now opens at a release,
  accumulates until the next version ships, and is discarded by the release
  that ships it — where the skill used to describe it as one version's,
  ending when that version shipped, which points a reader at an end that has
  already passed. (#155)

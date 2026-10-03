### Added

- Every release gets a seal on its GitHub Release page (#718). After the tag
  push publishes the note, a second job in the same workflow runs the suite
  at the tag, draws one seal for the release from the broad gate's letter,
  attaches it as `seal.png`, and puts it where the note's `📊 At a glance`
  table stood, with one line of the table's counts beneath it. The panel's
  rows are a fixed set: the version, the tagged commit, the pull requests
  merged, the issues closed, the suite's passed and skipped counts at the
  tag, the work items and their review rounds, how many runs were capped,
  and how many issues the rounds' verdicts deferred (a deferral written only
  in a round record's `## Deferred` table is not counted). A count whose
  source cannot be read says `not read` rather than 0. The image's alt text carries every
  number too. The job runs only on a release that run created, edits only a
  glance table still exactly as it was generated, and turns every failure
  into a `::warning::` in its log with the note left as published, so a seal
  can never make a release fail. `DRY_RUN=1` draws one by hand.

### Changed

- A gate's failure report caps the exception's class name, not only its
  message (#722). A class from outside the plugin can name itself anything,
  and two gates failing with a long enough name made the report pass the
  1,000 UTF-16 units the `Stop` message keeps back for it. The name is cut
  at 40 units when the failure is recorded, and the name, the message and
  the group and the gate's own name are cut again when an older plugin's
  record is read. With every field at its cap, two failed gates write 972
  units and three 1,378.

- The suite needs Pillow, pinned to one version beside the CommonMark
  parser, for the seal's pixel case; `bin/test` adds it to an existing
  `.venv` on its next run. A plugin user installs nothing new: nothing under
  `hooks/` or `skills/` imports it.

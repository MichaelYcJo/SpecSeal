<!-- seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A release's size is decided by what has to be in effect before the next
  work item starts, and three or four is now named as the ceiling it always
  was.** The rule used to read *a release is sized in work items rather than in
  ticket numbers, and three or four is the size*, which reads as a target. A
  session holding it read it as one twice in a single day: it proposed moving
  eighteen issues out of the release milestones to bring them "down to size",
  and read a two-item release as under the rule with room for a third. Neither
  of the last two releases was cut at three or four, and neither was a failure
  to reach it — one shipped the agent that writes a frame, because nothing
  could be framed until it existed, and the next replaced a deleted checklist
  with a gate, because the work item after it had to start with the
  replacement already in effect.

  - **The criterion, in `docs/issues-and-milestones.md`.** One change that
    decides how the next ticket runs is a release on its own. The count
    survives as a ceiling — as much as one section can describe while a reader
    still comes away knowing what the release is about — in the wording
    `docs/review-chain-spec.md` already uses for the review cap, so one idea is
    not spelled two ways.
  - **The evidence is cited as prose, not as version numbers, and the document
    says why.** Both releases sit at or above the running version, and
    `test_no_loaded_file_names_a_version_at_or_above_the_running_one` refuses a
    loaded file that names one. Without the note, a later author for whom both
    numbers have become history would replace the descriptions with numbers and
    be right to.
  - **A label, `size: now`, so the judgement is written down once per ticket
    instead of re-answered from thirty-five issue bodies at every cut.** Two
    states: a ticket carries it or it does not, and not carrying it means the
    ticket rides the next release that happens to carry it. No tier list and no
    scale. The prefix is what keeps it inside the rule the same section opens
    with — a label answers *what it is about*, and this one is about sizing,
    which every release has, while only the value is spent when the release
    ships. It is the shape `chain: capped` already has on this tracker.
  - **What does not change is stated, so it is not re-argued.** A `release:`
    milestone is still the pool a release is cut from rather than the release
    itself, `backlog:` is still the unscheduled pool, and nothing schedules
    from either. Nothing reads the new label at all, so a stale one costs a
    reader a wrong answer and costs no automation anything.

  `tests/test_a_release_is_sized_by_a_criterion.py` holds the new wording
  present and the replaced sentence absent, and sweeps the loaded tree for a
  second statement of a release's size. Creating the label and applying it are
  the repository owner's, after this merges.

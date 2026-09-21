<!-- seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The broad gate's arm list was maintained by hand, so a branch could seal
  green and meet a red leg** (#468). The gate runs arms so that the sealer's
  one run says what CI will say, and nothing held its list against
  `.github/workflows/hygiene.yml`'s. The previous release added a step to that
  workflow's `release` job — *no merge on this branch dropped a correction the
  ledger had made* — and nobody added the arm; a coverage probe over the eight
  structural modules that read those files reported 243 passed and 8 skipped
  with it absent. So the seventh arm would have arrived the same way, and the
  eighth.

  - **The gate now declares a partition of every step of that job.** Each one
    is mirrored by a named arm or excluded with a reason somebody wrote, there
    is no third state, and a case holds the table against the workflow from
    both sides: a step added there fails the suite until somebody classifies
    it, and a row naming a step that was renamed away fails it too. The step
    names are read out of the workflow as text — the script runs with no
    third-party dependency, so there is no YAML parser — and the reader takes
    text rather than a path, which is what lets it be driven over shapes the
    file does not happen to have.

  - **Two arms were missing rather than one, and the count came out of a
    construction rather than a reading.** All thirteen steps were classified:
    three have no local answer at all (the pull request's body, a fetch of the
    remote's pull-request namespace, the tracker), one only ever warns, and
    six have a local answer. Of those six, two run a check the plugin ships —
    `correction-check`, the arm the previous release needed, and
    `skills/implement/scripts/seal.py mode --check` — and both are now arms.
    Of the other four, three run a script under `.github/scripts/`, which no
    plugin ships, and one is shell written inline in the workflow with no
    script either side can share; a repository that
    wants checks of its own sealed names them in the `Broad gate` row of
    `seal/config.md` rather than in the arm list of a script everybody
    installs.

  - **A seal says what it did not answer.** Where the gated repository has
    that workflow, the panel carries a `workflow` row — *8 of 13 not
    answered* — and the names of those steps go to stderr beside the line
    naming the repository's own command, before the checks run, so a run that
    comes back `NOT SEALED` carries it too. A panel value is 23 columns, which
    a count fits and a step name does not; a count alone would send the reader
    back to the two files this declaration exists to stop them opening. A run
    that answers every step says so rather than going quiet.

  - **A repository with no such workflow sees none of it.** The partition
    describes this repository's CI and the gate ships to every repository that
    installs the plugin, so the row and the line are absent where the file is,
    and a case asserts the panel's rows against the exact set they were
    before.

  - **What this does not close, stated rather than left to be found.** An
    exclusion can be written to make the case green rather than to state a
    truth, and the partition would then be total with the seal still short.
    Nor does the partition say a mirrored arm asks the same question its step
    asks — it says the step is on the list. #473 is the work item about that
    class, opened with the one live instance: the gate runs the `survivors`
    and `corrections` arms unconditionally where the workflow skips both
    steps on a `main` base.

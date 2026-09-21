<!-- seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A `seal/ledger.md` conflict resolved by taking one side reverted the other
  side's corrections, and nothing could see it** (#424). The fragment rule has
  one exception and it is the whole cause: a branch that falsifies what an
  existing shared-ledger row claims must touch that file to leave the ledger
  true. So two branches in one release correct rows of one file, and the file
  conflicts. In the measured instance the two hunks resolved in **opposite**
  directions — each side was the superset in one of them — and taking a side
  wholesale reverted three corrections that had each turned a false claim
  true. A row reverted to a superseded state is byte-identical to a row nobody
  touched, so `evidence-check` reports it `ok` and `--reverify` re-stamps it:
  *somebody read this*, written over a claim that had been read, found false
  and repaired. It was caught because a reviewer happened to grep for the
  marker the corrections carried and found 0 occurrences in a file that had
  had three.

  - **`correction-check` is the new command.** It walks every merge commit in
    a range and names every `Corrected <date>` or `Re-read <date>` marker a
    parent carried that the merge result does not — with the file, the merge,
    the parent it came from and the row that still stands. Exit 0 when nothing
    was dropped, 1 with each loss named, 2 for a range that does not resolve.

    **Both markers, matched on the verb and the date and on neither the
    sentence after it nor the qualifier before it.** Counted in this
    repository: 404 marker occurrences on 190 rows, at least three spellings
    of the `Corrected` sentence, and 39 markers in ten spellings that put a
    qualifier between the verb and the date — `Re-read again <date>`, `a
    third time`, `and re-executed`. One row carries no other spelling. A
    check pinned to either side of the date goes red on a rewording and stays
    quiet on a revert, which is both failure directions at once.

  - **Row survival is what separates a loss from a removal.** A marker that
    vanishes with its row is `REMOVED` and correct — that is the repository's
    own rule about a row whose anchor a change removes — and one that vanishes
    while its row stands is the defect. A row is identified by its first cell,
    and by its content anchors where the correction was the first cell.

  - **A marker a parent deleted relative to the merge base is that parent's
    decision, not the merge's.** Without that reading the check reports one
    merge over this repository's whole reachable history, and that merge is
    correct work: a release branch re-anchored a row whose section had moved
    file and rewrote the cell carrying four historical `Re-read` sentences. A
    check that fires on correct work is one people learn to skip.

  - **It runs at the pull request into a release branch, and it has no other
    moment.** A feature branch squashes, so the merges it reads stop existing
    when the branch lands — measured both ways rather than assumed. It reports
    the loss and cannot prevent it: reading both sides of a hunk is a person's
    act, and a merge driver would have to understand what a row claims.

  - **`CLAUDE.md` and `CONTRIBUTING.md` now say what to do at the conflict** —
    resolve hunk by hunk, read both sides, never `--ours` or `--theirs` — with
    the opposite-direction instance as the argument. The two are held against
    each other by a case, because they have disagreed about this rule before.

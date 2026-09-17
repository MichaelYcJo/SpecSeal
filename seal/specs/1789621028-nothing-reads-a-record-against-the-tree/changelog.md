<!-- seal/specs/1789621028-nothing-reads-a-record-against-the-tree/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A round record is written once and the tree keeps moving, and nothing read
  one against the other** (#344, #426, #427). The ledger has a checker that
  re-reads its claims against the code; the review records had none, so a
  record could say a range, a size or a fix that the repository no longer
  holds and every gate stayed green. Three new refusals close the parts of a
  record that are claims about commits, and the two instances that live inside
  the generator writing those records.

  - **A fix range is now stated as commits, and `HEAD` is refused.** A fix
    table used to state its range in prose — measured across this repository:
    39 fix-table files, 15 stating a range in their first eight lines, in 8
    different spellings, and 5 of those naming `HEAD`. `HEAD` resolves, so
    such a sentence stays readable while meaning a different set of commits
    every day, and three records of one work item said one. There is no
    convention in that prose to enforce, so the authoritative statement moved
    into the record: `round-record close --range` refuses an end that is not a
    commit somebody can open — at **both** ends, since a branch name at the
    start moves as far as `HEAD` at the finish — and `close` then writes the
    resolved range and its commit count into a new `Fix range` row.
    `chain-check` re-reads both halves at the pull request.

    **What changes for a caller**: `--range <a>..HEAD` stops working, and the
    refusal prints the commit to write instead. Records written before this
    release carry no such row and print rather than failing, the same
    grandfathering nine earlier record rules use.

    Both halves are read because either alone passes what the other catches.
    Ends this repository cannot see are reported and not failed: a feature
    branch squashes into its release branch, so a merged record's fix commits
    are ordinarily invisible and the record did nothing wrong.

  - **Re-closing a corrected record no longer doubles its grounds.** `close`
    joins the fix pass's grounds in front of the reviewer's rather than
    replacing them, on purpose — the two are different sentences by different
    authors. What it never checked is whether its own prefix was already
    there, so closing the same finding twice wrote the grounds twice, the
    record still parsed, and the only way it was ever caught was reading a
    committed file against two earlier commits. That path is not a misuse
    anybody can be told out of: correcting a record and re-closing it is the
    documented way out of a record written wrong.

    `close` now refuses ahead of the write, with nothing reaching disk, for
    all three verdict words and for a cell already carrying a prefix that
    names a different commit. It refuses rather than overwriting, because
    overwriting would discard the reviewer's sentence silently. The fully
    restored record — verdict **and** grounds — still closes exactly as
    before, which is measured rather than asserted.

  - **A record already carrying a doubled cell is named.** Stopping the second
    write leaves every existing duplicate unreadable, so `chain-check` gained
    an arm that names the file, the finding and the repeated text. It has **no
    cutoff**: a doubled cell is a present cell that says a thing twice and the
    repair is available to whoever wrote it, unlike a row that did not exist
    when the record was written.

    **This repository holds none**, measured over 229 round records and 3331
    grounds cells, and that is disclosed rather than sold as a catch. One of
    the three fix words leaves a shape a reader can find after the fact:
    `answered` and `deferred` write the author's own words, so a duplicate of
    either is indistinguishable from prose that repeats itself. The write
    guard covers all three; this covers the one that survives into a record.

  - **The guard that said a definition arrived whole compared against a
    constant** (#426). It asserted every agent definition was larger than 1000
    bytes and called that wholeness; the smallest definition is 3764 bytes, so
    a read truncated anywhere between those numbers truncated all five files
    and the guard stayed silent. It now compares the bytes it read against the
    size of the file it read, so the assertion carries no number that can be
    wrong — not a bigger threshold, which would only move the silent range,
    and not a literal byte count, which would redden whenever anybody edited a
    definition.

  - **Four lines of an earlier work item's records said what the tree does
    not**, and are pinned to what they named, each with a comment saying what
    it was read against and when. One of them named a release branch that has
    since been deleted, so the command it records could not be re-run at all.

    Re-measuring it turned up the class one level up: with the range pinned,
    the checker **as it stood** reports three places and the checker **as it
    stands** reports two, because 60 lines landed in that script in between.
    A measurement is reproducible only against a named range *and* a named
    version of whatever measured it. One record's `Location` was found to have
    been wrong on the day it was written; it is recorded as wrong rather than
    re-pointed, because re-pointing a position restarts the rot and turning
    record locations into content anchors is an open question across 227
    records.

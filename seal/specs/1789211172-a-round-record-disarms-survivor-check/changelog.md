<!-- seal/specs/1789211172-a-round-record-disarms-survivor-check/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`survivor-check` no longer lets a branch's own review paperwork subtract
  the survivor it quotes.** A reviewer's report quotes the defective wording
  verbatim, because that is what a report is for. The check read every path in
  the range as prose, so the quotation counted as wording the fix wrote, and
  the survivor it was about was subtracted before anything was looked for.
  Measured at three tips of one branch: the commit that added only round 1's
  record and report turned a range that had reported its survivor green.

  - **What changes for you.** The gate gets **stricter**, and the first
    branches to meet it are the ones that went through review — which are the
    branches where a survivor is most likely, since a fix pass correcting one
    coordinate is how survivors are made. A pull request into a release branch
    that reported nothing may now report something. The answer is a correction
    or a `seal/specs/<work-item-id>/survivors.md` row with the standing text
    quoted and the grounds written. There is no value meaning *check nothing*.
  - **What does not change.** `bin/survivor-check`'s command line, both
    exemption row shapes, the floor, the scoring, and the report's text. The
    number of sentences a range is measured against does not move either: a
    round record the range only adds removes nothing, and the real range this
    was measured on reported the same 894 files and 16 removed sentences
    before and after.
  - **The exemption path is still open.** Writing a
    `seal/specs/<id>/survivors.md` row silences its survivor a second way —
    the row quotes the standing text, so the commit adding it puts that quote
    inside the range. That is a different mechanism, it was deliberately left
    standing here, and it is tracked as issue **#371**. A `survivors.md`
    written before this release is not armed by this change.

- **The module now says which side each exclusion holds on.** Its docstring
  read *Everything under a work item's `rounds/` is out* and named neither of
  the two functions it had to be true of — the pool that is searched and the
  range that is measured are computed separately, and the exclusion had held
  on one of them since the module shipped. A case pins the new sentence, and a
  second case walks the module for every path list it derives from git and is
  red until each one is filtered or named with grounds. The reason the defect
  existed is that a docstring asserted the class and nothing measured it.

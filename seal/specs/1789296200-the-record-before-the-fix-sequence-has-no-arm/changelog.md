<!-- seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A round record can now say why it was written after the fixes it
  commissioned, and the pull request prints instead of failing.** Until now a
  record refused on that line had three repairs and not one of them was
  honest: rewrite history so the adding commit moves, merge over the red line,
  or invent a waiver nobody wrote down. One work item met all three, took
  none, and ended with a pull request red on a line no later commit could
  clear, its run capped and its reverted fixes redistributed across six
  issues.

  - **What changes for you.** `round_record.py new` takes
    `--written-late "<why>"`, which writes `| Written late | yes — <why> |`
    into the record. `chain_check.py` reads that row and prints the refusal
    with the reason quoted rather than failing on it.
  - **The refusal itself now names the exit.** A record that meets that line
    is already committed, so the flag names a moment that has gone — the
    message says the row may be added by hand and committed like any other
    correction. It used to end at *commit the record when the round posts*,
    which is advice nobody meeting it can act on.
  - **What buys nothing**, and is judged exactly as it is today: the row
    absent — which is every record written before this release — the cell
    `no`, a bare `yes`, and a value outside the vocabulary. A bare `yes` is
    refused at the point of writing too. The reason is the whole of what the
    row buys, and a relaxation with an empty cell is a waiver with no author,
    which is the third of the three bad exits wearing a flag.
  - **The gate gets one state looser and no state stricter**, so nothing that
    passes today can start failing. There is no new `*_FROM` cutoff, because a
    relaxation cannot be red on history nobody can fix.
  - **The vocabulary is not new.** `no` / `yes — <why>` is what `Needs a fix`
    and `Loses a record or crashes` already use, read by the same
    `chain_check.yes_or_no`.

- **`round_record.py new` now says when the commit the round read is no longer
  the branch's HEAD.** That is the last moment in the sequence where anybody
  can still act on it — the fix pass is a spawn with no command for a check to
  sit on, and the pull request is one round too late. The line names both
  commits and lists what stands between them with their subjects, because the
  two readings it cannot tell apart are *the fix pass already ran* and *HEAD
  moved during the review*, and the subject line is what separates them.

  - **It refuses nothing**, and that is measured rather than chosen. Over this
    repository's own pre-squash branches, **40 records of 152** have a
    `Target SHA` that is not their adding commit's first parent, and the
    commonest cause by far is the round's own paragraph being committed
    between the review and the record. A refusal would have fired on one
    correct run in four.
  - **Nothing changes for a round that read HEAD**, which is the other 112.
    The ordinary record prints exactly what it printed before.
  - **A tree that is BEHIND the commit the round read gets its own answer.**
    There is nothing to list there, and neither of the two readings is true —
    nothing landed after the review. The line says so and tells you what to
    check instead: that `--target` names the commit this tree's HEAD stood at,
    and that you are in the tree the round reviewed.

- **Every generated record carries a `Written late` row**, `no` unless the
  flag says otherwise, and `templates/sdd-round.md` documents it beside
  `Target SHA`. A record written before this release has no such row and is
  read exactly as it was.

<!-- seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The check that exists to stop a false claim shipping was shipping two of
  its own, and half its parent-naming rule was held by nothing** (#469, #470,
  #471). All three are leftovers of #424's review chain, left open where that
  run capped.

  - **Every figure `correction-check` states about the corpus it watches now
    stands at one site, and carries a corpus, an instrument and a moment.**
    The comment justifying the bound on a marker's qualifier had been false
    twice for two different reasons, and the second time the cause was a
    commit inside the fix range that wrote a marker into a file the census
    counted. Six tracked files restated one of its numbers; correcting six
    copies leaves six copies to drift, so the module docstring, the test
    docstrings, the hygiene workflow's comment and the work item's records
    point at the census note instead of repeating a digit.

    The corpus is `seal/ledger.md` alone — **not** because a branch cannot
    move it, which is what the ticket prescribed and is false twice over, but
    because it is the file a release folds the fragments INTO and therefore
    the part of the corpus that survives one. The note says so, and says that
    its digits go stale by construction at the next fold and the next
    correction.

  - **A case now holds the bound instead of one literal spelling.** It takes
    an independent census over the real ledger files, read through the
    module's own `LEDGER` and `FRAGMENTS` rather than a list written in the
    case, and asserts the property that every candidate marker site the
    unbounded walk finds is one the pattern also sees. It asserts no count,
    because a number over that corpus is stale the next time anybody records
    a correction. It refuses to pass over an empty corpus, and when the
    corpus grows a longer run it goes red naming the file, the row, the run
    length and the spelling, so the bound is raised deliberately.

    The instrument is deliberately not the pattern under test, and the pair
    of mutations is the evidence: narrowing the bound turns the case red, and
    narrowing the bound **while taking the census with the pattern itself**
    leaves it green. That is the circular census that went wrong twice,
    demonstrated rather than asserted.

  - **A tie in the parent-naming rule falls to the first parent, and a case
    says so.** The report names the parent that lost the most occurrences of
    a marker, and ties fall to the side the person resolving the conflict had
    checked out. Only the first clause was held. The tie is the ordinary path
    rather than the edge — every marker older than the fork is carried by
    both parents, so both lose the same count — and the behaviour rested on
    `max` returning the first of equal keys, with nothing red if that ever
    changed.

  - **Statements about the corpus now say when they were taken.** Ledger rows
    C1 and C2 are corrected in place, C3 and C4 record being re-read by hand
    before their hashes were re-stamped rather than after, and the records of
    #424's work item are corrected under a marker naming the issue. One
    figure a reader could take at face value is gone: *404 occurrences on 190
    rows* was the file's total set against the part of it standing on rows,
    and the survival test never acts on the difference.

  - **A coordinate that was a line number is a spelling.** The longest
    qualifier the tree carries was addressed as `seal/ledger.md:1172` in four
    places; it is now named by the spelling itself and by the fact that it
    stands in the file's prose rather than on any row — which had never been
    measured, and which means no table row carries a qualifier longer than
    three words.

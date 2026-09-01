# Questions — every branch appends to the same two files

Three decisions were settled by the repository owner in the routing batch and
are not re-opened here: the changelog is fragmented and gathered at release,
the ledger is fragmented and never gathered, and a ledger row stops carrying a
`Checked` SHA. What follows arrived during implementation.

## Q1 — a row can be stale on arrival, and no derived baseline sees it

**Stays open and stays out of scope.** The repository owner commented it onto
issue #31 during review round 1, and #31 is the next work item — so this is a
known limit with a home rather than a loose end.

Two branches run at once. Branch A writes a ledger row citing `code.py:10`.
Branch B changes `code.py:10`. B squashes into the release branch first, then
A. The row's first appearance is A's own squash commit, which already contains
B's change — so `git diff <that commit>..HEAD` shows nothing and the row reads
OK, while its coordinate was stale the moment it landed.

Last-touch blame misses it the same way. The written stamp caught it noisily
and by accident: a row stamped at the base reads DRIFTED against everything
that happened after, B's change included, which is the same warning it gives
for work nobody touched.

Catching it properly means checking the coordinate against the code it cites
rather than against a diff window — which is issue #31, and outside this work
item. **Recorded rather than fixed**, so the limit is a known one.

What can be said for the current state: it is not a regression. The stamped
scheme's noise was not detection, and the derived baseline is right about
every case where the row and its code moved together.

## Q2 — a commit SHA in a fragment's prose header — ANSWERED

**Answered by the repository owner during review round 1: read it, and print
one line saying where the baseline came from.**

`find_baseline` reads a ledger's header for a declared baseline, and a
fragment declares none — so a commit named in a fragment's prose becomes the
whole file's baseline. This happened twice on the first fragment written, the
second time in the paragraph explaining the first, which is what settled it:
a convention broken by the person writing it down is not one anybody else
will keep.

The two options that were weighed and refused both fail quietly. Requiring the
baseline to sit in a row labelled `Baseline` would strip the fallback from any
ledger whose header writes a bare SHA — the shape
`tests/test_evidence_check_hardening.py::test_custom_ledger_glob` has — and
such a ledger would then report LESS drift while printing the same line as a
healthy one. Leaving it as a documented convention had already failed once.

What ships instead: the header SHA is still read, and the run prints
`(baseline: 9829412 from a Baseline row)` or `… from header prose`. Its
failure direction is noisy rather than quiet, and nothing about the accepted
ledger shape changes.

Two narrower fixes landed with it. The header now ends above the first row
that CITES CODE, so a row's prose is out of the header scan's reach at all —
and that cut runs before the 2000-character cap rather than after it, which is
what had made the cut dead on this repository's own ledger and on the
template. And a row's own baseline must be a date and a SHA together, so a
bare hex word in a row is inert.

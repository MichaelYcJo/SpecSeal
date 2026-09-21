<!-- seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **Three sets of statements the gate's own fixes disproved are corrected**
  (#461, #464, #465). None of them changed what the gate does. Every one of
  them made a reader believe something the same work item had measured to be
  false, and all three were left standing because #423 capped before it could
  spend them as reopenings.

    **The base guard's docstring named a class git does not refuse** (#461).
    It said `check-ref-format --branch` refuses anything carrying `@{…}`.
    Measured on git 2.54.0: the command EXPANDS `@{-N}` and then checks what
    it expanded to, so `@{-1}` is accepted and the command prints the branch
    it found, while `HEAD`, `HEAD~1`, `base@{u}` and `topic@{1}` are each
    refused. The docstring now states that property.

    **And the one spelling that slips through made the gate quote a ref
    nothing reads.** `--base @{-1}` passed the guard, resolved, and the
    printed line offered `origin/@{-1}` as *the ref a runner reads* — a name
    no ref can have. The line now asks git whether a runner's checkout could
    hold the label it is about to name, and where it could not, it says the
    runner has no counterpart for that spelling instead of naming one. The
    question is git's own answer and not a pattern written in the gate, which
    is what round 1's finding 6 already settled for the guard beside it.
    `agents/sealer.md` has the sealer quote this line verbatim into a report,
    so the new sentence is pinned by a case rather than only corrected.

    **The panel's docstring led with an argument its own phase retired**
    (#464). It said a ref too long for the row is why the printed line is the
    authoritative statement and the row only context. The printed line is
    silent where the two bases agree, so there are runs where the row is the
    only statement a reader gets; the row now says so, and the elision's
    grounds no longer assume the prefix being dropped is always `origin/`.

    **The baseline half of the direction claim carried no evidence label.**
    Round 1 labelled it *read, not executed* and three operational statements
    of the shipped work item repeated it beside the measured half with no
    label and no answerer. All three now carry the label and name who answers
    it. `CHANGELOG.md` §0.12.2 keeps the unlabelled copy: amending a released
    section is the repository owner's call, and it is disclosed rather than
    taken.

    **The gate's own test module said three times that the branch left
    another module byte-identical** (#465), and that branch changed it — one
    assertion moved because the `Broad gate` cell's base half now carries the
    commit. All three statements say what the branch did.

    **No exit code, verdict or resolution moves.** One printed sentence
    changes, for one input class, and every correction to a shipped record is
    made in place under a marker quoting what stood there.

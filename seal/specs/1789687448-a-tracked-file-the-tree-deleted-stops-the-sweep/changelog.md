<!-- seal/specs/1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A tracked file the working tree had deleted stopped six of this suite's
  sweeps at the first missing path** (#432, #282). `git ls-files` lists the
  index, so a file that is tracked and gone from disk is on the list with
  nothing behind it. Six helpers opened every listed path, and the walk ended
  there: no file after it was read, and the rule the walk holds reported
  nothing at all. The one documented moment that produces that tree is step 3
  of a release — the fold removes each ledger fragment and the whole gate then
  runs before anything is staged — so what a release met was a
  `FileNotFoundError` naming a file it had just deleted on purpose, in place
  of the check it was running.

  - **The guard is one shared predicate, not six copies of a line.**
    `tests/conftest.py#on_disk` splits a git listing into what is on disk and
    what is not, and each helper takes the repository root as an argument so a
    case can build a tree with a tracked-and-deleted file and watch it work.
    Both halves are returned rather than one dropped, which is what makes the
    next paragraph possible.

  - **A sweep judges what remains; a check that needs the whole corpus
    declines to judge and names the missing paths.** Two tickets both proposed
    a silent skip, and a silent skip is right in one direction and wrong in
    the other. A sweep looking for something is strictly better off — on that
    tree it used to report nothing about any file. A check proving an
    allowlist entry is still ALIVE is not: to it a skipped file and a deleted
    entry are the same evidence, so it would report a live entry dead. Three
    such checks now decline, through `pytest.skip` with a reason naming every
    missing path rather than counting them.

  - **The class is re-enumerated by the suite rather than by whoever
    remembers.** A new case walks every `tests/*.py` and asks which scopes
    derive a path list from git; each must apply the shared predicate or be
    classified with grounds a reader can weigh. It found a sixth helper while
    it was being written — one that lists with `git ls-tree HEAD` and takes
    its content from the working tree — which the enumeration by hand had
    missed because it searched for the other spelling.

  - **`docs/release-checklist.md` step 3 says what that tree looks like.** A
    fold alone produces no skipped case, because the paths it removes are
    under `seal/ledger/` and no declining check reads a corpus reaching there.
    One appears when the tree is also mid-edit where the liveness checks look,
    and a count line with reasons naming paths is that state rather than
    something to debug.

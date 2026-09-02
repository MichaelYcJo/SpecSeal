- **Two roots become one, laid out by lifetime, and the opt-in is the
  folder.** `specs/<id>/` held a work item's documents and its review
  records, which die at different times, and `.specseal/` held the ledger,
  whose rows outlive the work item. Both now live under `seal/`:
  `seal/specs/<id>/` for the whole work item, `seal/ledger.md` and
  `seal/ledger/<id>.md` for the rows, `seal/follow-up.md` and
  `seal/parity.md` as they were. A repository is opted in when `seal/`
  exists at the root (or under `.git/`, the place local mode will use);
  `.specseal/` opts nothing in any more, and the throwaway opt-out is the
  file `.git/specseal-scratch`, which cannot be committed. At the first
  session start after updating, a repository with the old layout is moved
  once: every move is a staged `git mv`, the ledger rows that cite a moved
  file are re-pointed with their hashes untouched, one line says what
  moved, and the person reviews the diff and commits. A tree with
  uncommitted changes under `.specseal/` or `specs/` is refused with a line
  saying to commit first, and a repository carrying `.specseal/scratch` is
  left alone. To move by hand instead: `git mv .specseal/map.md
  seal/ledger.md`, `git mv .specseal/map seal/ledger`, the rest of
  `.specseal/` into `seal/`, each `specs/<id>` into `seal/specs/<id>`, then
  `evidence-check .` to find the rows to re-point. Every gate, checker and
  release script reads the new paths; the `<!-- specs/<id> -->` markers in
  `CHANGELOG.md` and the ledger are unchanged; the chain check no longer
  judges a declaration that a pull request only renamed. Nothing is
  deleted: a work item's directory lives until a later `settle` folds it.

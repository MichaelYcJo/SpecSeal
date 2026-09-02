- **Two roots become one, laid out by lifetime, and the opt-in is the
  folder.** `specs/<id>/` held a work item's documents and its review
  records, which die at different times, and `.specseal/` held the ledger,
  whose rows outlive the work item. Both now live under `seal/`:
  `seal/specs/<id>/` for the whole work item, `seal/ledger.md` and
  `seal/ledger/<id>.md` for the rows, `seal/follow-up.md` and
  `seal/parity.md` as they were, `seal/README.md` for the export rules. A
  repository is opted in when `seal/` exists at the root (or under `.git/`,
  the place local mode will use); `.specseal/` opts nothing in any more, and
  the throwaway opt-out is the file `.git/specseal-scratch`, which cannot be
  committed. **Behavior that writes to your tree without being asked,
  disclosed on its own line: at the first session start after updating, a
  repository with the old layout is moved once.** Every move is a staged
  `git mv`, `seal/README.md` is rewritten from the template, the ledger rows
  that cite a moved file are re-pointed with their hashes untouched, one
  line says what moved, and the person reviews `git diff --cached` and
  commits. That commit belongs to no work item, so inside a session the
  commit gate asks; `: '[no-review]'; git commit …` waives it for the one
  command, with `[no-parity]` beside it where `seal/parity.md` exists.
  Until that session start every gate is silent in that
  repository, because the signal it reads has moved. A tree with
  uncommitted changes under `.specseal/` or `specs/` is refused with a line
  saying to commit first and retried at the next clean start; a move that
  stopped resumes; a repository carrying `.specseal/scratch` is left alone;
  the once-per-repository marker is `~/.claude/specseal/root-migrated`. To
  move by hand instead — the README's *Coming up from 0.3.x* carries the
  same sequence: `mkdir -p seal/specs`, `git mv .specseal/map.md
  seal/ledger.md`, `git mv .specseal/map seal/ledger`, the rest of
  `.specseal/` into `seal/`, each `specs/<id>` into `seal/specs/<id>`,
  `rmdir .specseal specs`, then `evidence-check --reverify .`, which
  re-points each row citing a moved file. Every gate, checker and release
  script reads the new paths; the `<!-- specs/<id> -->` markers in
  `CHANGELOG.md` and the ledger are unchanged; the chain check no longer
  judges a declaration that a pull request only renamed; `templates/map.md`
  and `templates/specseal-README.md` are `templates/ledger.md` and
  `templates/seal-README.md`. Nothing is deleted: a work item's directory
  lives until a later `settle` folds it.

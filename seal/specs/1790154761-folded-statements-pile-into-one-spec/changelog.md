### Changed

- **`settle` now tells the folding session what shape a standing statement
  takes and where it may land (#520).** Step 2 of the fold says a statement
  opens with its rule as one bold sentence, gives its grounds, and ends with
  one line naming what enforces it: `Enforced by:` and a repository path, a
  `path::name`, or `nothing — <why>`. It also says a rule goes into the
  document that owns its subject, and that a document over the repository's
  size ceiling takes no new statement until it is split. The plugin ships no
  checker for either rule and sets no ceiling. It says so, and it says that a
  contradiction between two statements is left to review.

  In this repository the two rules have values and checks. Statements folded
  from work item `1790154761` on must carry the `Enforced by:` line, and a
  test resolves every target it names. A top-level document under `docs/`
  stays at or under 1000 lines. `docs/review-chain-spec.md`, which the first
  folds grew to 2,159 lines and 29 folded statements, is frozen at that
  marker count until MichaelYcJo/SpecSeal#526 splits it. The next fold
  therefore cannot add to it. `docs/the-evidence-ledger.md` states the values,
  and a test keeps the prose and the constants the same numbers.

- **Both editions of a document now carry the same folds, and a test holds
  them.** The Korean edition of `docs/one-root-by-lifetime.md` lacked the
  section the first fold wrote and all ten of its fold markers. It has both
  now. A new test compares every top-level `docs/X.ko.md` with its English
  edition by heading levels and by the fold markers under each heading, so a
  fold into one edition only is refused. `CONTRIBUTING.md`'s rule that the two
  READMEs move together now covers every document with a `.ko.md` edition.

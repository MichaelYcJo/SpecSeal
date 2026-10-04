### Changed

- Every rule this repository's `CLAUDE.md` restated now has one home, and
  `CLAUDE.md` links to it (#730). The merge method per direction lives in
  `docs/branch-and-release.md`, *no real identifiers* in `CONTRIBUTING.md`,
  and the commit cadence and the question batch in the `implement` skill.
  Each `CLAUDE.md` row keeps the home's path and section, when a session
  needs the rule, and the act in one sentence. The merge row's old table had
  already gone false: it said a rider stamp names a commit, which stopped
  being true when the stamps moved to content, and it was missing two of the
  six directions. The block `install.sh` distributes is unchanged.

### Added

- A pull request that pastes a passage of 15 words or more from one rule
  document into another fails, naming both files, the passage and the fix:
  link to the home instead (#730). The check reads the documents under
  `docs/`, `skills/`, `agents/` and `templates/` with `CLAUDE.md`,
  `CONTRIBUTING.md` and `README.md`. The copies already in the tree are
  counted per pair of files and allowed at that count, so a pull request
  that removes one passes without touching the table. It does not catch a
  rule restated in other words. Moving the existing copies is #755.

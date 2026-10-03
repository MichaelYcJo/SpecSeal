### Changed

- The commit gate's policy is three documents, one question each (#727).
  `docs/commit-review-gate-spec.md` had reached 1,047 lines and was frozen
  over the ceiling, so no new rule could be folded into it. It is cut along
  its own headings: `docs/the-commit-gate-inside-git.md` says what git
  decides inside the commit, `docs/the-review-and-parity-arms.md` says what
  each opt-in arm wants and how the routing declaration moves the review
  arm's check to the pull request, and `docs/commit-review-gate-spec.md`
  keeps the registration, the PreToolUse reading, the review-history guard
  and the implementer mark, with an index naming the other two. The moved
  text is unchanged except where it pointed across the cut by position. The
  `Over the ceiling` row now reads `none`. The agent contract, both READMEs
  and every other reference cite the file that holds the section. A link to
  a moved section at an older tag keeps resolving at that tag.

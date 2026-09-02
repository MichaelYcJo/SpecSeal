- **A repository that must not carry the plugin's files in its tree can
  opt in: local mode keeps the whole root at `.git/seal/`.** The root
  lives at one of two places and the hooks read whichever exists, in
  order: `<repo>/seal/`, which is committed and is shared mode, then
  `seal/` under the common git directory (`git rev-parse --git-common-dir`),
  which is local mode — shared by every linked worktree of the clone, never
  a commit candidate, and needing no `.gitignore` line. There is no config
  key. First setup asks one question, once: when the `implement` skill
  creates the root it offers **shared** (the default: `<repo>/seal/` in the
  tree, and the hygiene workflow written to `.github/workflows/hygiene.yml`
  from the new `templates/hygiene.yml`, only when that file is absent) or
  **local** (`.git/seal/`, nothing installed, nothing in the tree). A
  repository with `seal/` at either place is never asked. Every hook that
  opens a file under the root resolves it the same way — the commit gate's
  declaration, the implementer notice, the review-history guard, the
  evidence advisor, the ledger migration and `evidence-check`'s defaults —
  and the one sentence a session needs is in the `implement` skill: every
  `seal/…` path means `<repo>/seal/` where it exists and
  `$(git rev-parse --git-common-dir)/seal/` otherwise. What local mode
  gives up, stated: the chain and unverified checks read committed files,
  so CI cannot run them there; a new machine or a re-clone starts empty.
  Switching is a move and a commit, documented in the README; export and
  import arrive with #81. The session-start migration is unchanged — a
  repository on the 0.3.x layout committed the plugin's files and is moved
  into `<repo>/seal/` — except that a repository whose root is already at
  either place is marked as moved and is not moved onto an old branch later.

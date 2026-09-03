- **A repository that must not carry the plugin's files in its tree can
  opt in: local mode keeps the whole root under the git directory.** The
  root lives at one of two places and the hooks read whichever exists, in
  order: `<repo>/seal/`, which is committed and is shared mode, then
  `seal/` under the common git directory (`git rev-parse --git-common-dir`),
  which is local mode — shared by every linked worktree of the clone, never
  a commit candidate, and needing no `.gitignore` line. There is no config
  key. Every hook that opens a file under the root resolves it the same
  way — the commit gate's declaration and the path its stop text tells you
  to write, the implementer notice, the review-history guard, the evidence
  advisor, the ledger migration and `evidence-check`'s defaults when the
  plugin's own copy runs (the copy `evidence-ci` vendors into `tools/`
  reads `<repo>/seal/` as before) — and the one sentence a session needs is
  in the `implement` skill and at the top of both agents: every `seal/…`
  path means `<repo>/seal/` where it exists and
  `$(git rev-parse --git-common-dir)/seal/` otherwise. What local mode
  gives up, stated in the README and in the root's own README: the
  pull-request checks read committed files, so CI cannot run them there,
  and a new machine or a re-clone starts empty. Switching is a move and a
  commit, documented under *Shared or local* in the README; export and
  import arrive with #81.
  **Nothing here writes to your tree without being asked. What arrives
  unasked, on its own line: first setup asks one more question, once —
  shared or local, shared first — in the batch the `implement` skill
  already asks, and a repository with `seal/` at either place is never
  asked.** Shared creates `<repo>/seal/` in the tree, which the routing
  commit carries, and writes the pull-request checks to
  `.github/workflows/hygiene.yml` from the new `templates/hygiene.yml`
  only when that file is absent — it clones the plugin at the release
  installed at setup and runs the chain check and the unverified-rows
  check. Local creates the root under the common git directory, installs
  nothing and touches nothing in the tree. The session-start migration is
  unchanged — a repository on the 0.3.x layout committed the plugin's files
  and is moved into `<repo>/seal/` — except that a repository whose root is
  already at either place is marked as moved, so a local-mode repository
  that later checks out a branch still carrying `.specseal/` is not moved
  into the tree it chose to keep clean.

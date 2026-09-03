- **Switching between shared and local mode is a command now, and a
  repository can say which mode it wants before the folder moves.** It was
  two shell lines in `README.md`'s *Shared or local* section — correct, and
  unfindable — and a repository arriving from the 0.3.x layout landed in
  shared without ever being asked, which put the people most likely to want
  local mode in the place least likely to tell them it was still available.
  `seal mode` prints where the root is, what `seal/config.md`'s new `Mode`
  row says it should be, and whether the two agree. `seal mode local` and
  `seal mode shared` switch; `seal mode --apply` switches to what an edited
  row says; `seal mode --check` writes nothing and exits non-zero on a
  disagreement, which the pull-request checks now run so the row cannot
  quietly become a document that lies.
  **The row is what the repository wants and the folder's location is what
  it has.** Nothing at runtime reads the row — every hook still resolves the
  root by looking for `<repo>/seal/` and then `<git-common-dir>/seal/` — so a
  gate can never be sent looking in a place with no folder. It has no default
  either: an absent row is filled in from where the folder actually is, which
  is an observation rather than an assumption, and is the state of every
  repository that has a `config.md` today.
  **Beyond the two shell lines it does what a `mv` cannot.** It refuses when
  the other mode's root already exists, refuses when the index carries a
  change under `seal/` or the workflow path, carries
  `.github/workflows/hygiene.yml` in and out, and writes the row so the file
  and the folder agree afterwards. It stages; you commit.
  **Carrying the workflow file is the part that is easy to mistake for
  tidiness.** Measured in a repository with no `seal/`: the two checks it
  runs fail in opposite directions — one goes red on every pull request
  forever for a repository that did the right thing, and the other goes green
  having examined nothing. Left behind, a switch to local turns the build red at the first of them.
  **The two directions do not cost the same, and the command says so before
  it acts.** Going to local takes the records out of the tree and every other
  clone loses them at the next pull, which is what `seal export` and `seal
  import` are for. Going to shared is the one to be sure about: the commit,
  not the move, is the point of no return, and until it lands
  `git reset -- seal .github/workflows/hygiene.yml` and then `seal mode
  local` walk the whole thing back.
  The rename runs first and every step after it is idempotent, so a stopped
  run — or a person who already ran the README's `mv` by hand — is finished
  by running the command again rather than refused. (#104)

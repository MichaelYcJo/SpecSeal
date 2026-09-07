- **A loaded file may no longer name a version at or above the running one,
  so a document naming a release that has not shipped goes red on the commit
  that writes it (issue #179).** The check read one number — the version in
  `plugin.json` — so a version written *ahead* of the release was green every
  day until the day it shipped, and red on that release's own preparation
  commit, hours in, after the broad gate had already run.
  `docs/issues-and-milestones.md` carried `0.9.0` that way for three releases,
  and the branch that found it had just written two more of the same shape.
  The comparison is read rather than the equality: at or above the running
  version is a timer and is refused, below it is history and is kept.

  **The half that is kept is what decided the design.** The obvious wider
  rule — refuse every version this repository has ever shipped, read from the
  tags or the changelog — refuses `docs/issues-and-milestones.md`'s own
  sentence saying that *the branch `release/v0.3.0` shipped as 0.2.0*, which
  is the reader's only way to tell which release an issue went out in. A rule
  that cannot state that fact is refusing history rather than catching a
  timer, so it was not taken.

  **The comparison is numeric, and that is not a detail.** `0.10.0` is above
  `0.8.3` and every comparison of the two as text says otherwise — and
  `0.10.0` is the exact version the issue names as the one the next author
  writes. A mutation run that swapped the numeric comparison for a textual
  one is what put a case behind it.

  **Three exemptions, each argued where it is declared, and the illustrative
  one asserts its own precondition.** The value the repository already tells
  authors to write (`1.2.3`) is allowed in every loaded file, because the
  point of an illustrative number is that the next author writes it somewhere
  this list cannot know the name of. `docs/experiments/` joins the
  records-of-a-moment list as a path prefix rather than as three more file
  names: those records are dated by their own file names and rewriting the
  version an experiment measured on falsifies the record, which is true of
  every file that directory will ever hold. A version belonging to another
  product — bash's, in a comment about its glob behaviour — is pinned to the
  file that names it, so the token cannot walk through anywhere else.

  The illustrative exemption carries a case of its own asserting that the
  value is neither the running version nor one `CHANGELOG.md` records as
  shipped. On the day this repository ships that number, a bare string in an
  allow-list would wave through exactly the line the check exists to catch,
  and it would do so in silence.

  **The failure message is where the reason now lives**, which is what the
  issue asked for: it names the file, the line and the token, says why such a
  line is a timer, and tells the next author what to write instead and which
  paragraph explains why. `docs/issues-and-milestones.md`'s milestone example
  now asks "what is in 1.2.3" and points at that paragraph. (#179)

- **The comment on `git ls-files`' quoting arguments credits `-z` with what
  it alone does, and so do the two records that repeated it (issue #98).**
  Three places said `-z` alone turns git's escaping of non-ASCII paths off
  and `core.quotePath=false` does not. Re-measured on git 2.50.1 (Apple
  Git-155) over four quoting variants and a fifth for control characters:
  either argument turns that escaping off by itself, so the sentence was
  false, and the same comment contradicted itself three lines further down.

  What `-z` does that the config does not is two things. It turns off the
  escaping of control characters as well — under `core.quotePath=false` alone
  a name holding a newline still comes back quoted — and it separates on NUL,
  the one byte a filename cannot hold. The split below the call is on NUL, so
  dropping `-z` returns the whole listing as a single entry.

  **Nothing in the call changed.** The instruction the comment gives — if one
  of the two is ever pruned, prune `core.quotePath=false` — was right all
  along; only the grounds under it were wrong, which is why no test could
  have caught this and why it travelled from a round record into a ledger row
  and a comment unremarked. The ledger row whose own clause stated the false
  sentence is corrected in `seal/ledger.md` itself, and the two rows anchored
  on the unit the comment lives in were re-read and re-verified.

  Folded in with it: a fixture docstring said two documents carry the only
  mention of one template, where each carries the only mention of one. The
  conclusion it drew was right; the reason given for it was true of one
  document. (#98)

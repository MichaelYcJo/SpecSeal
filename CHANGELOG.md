# Changelog

## Unreleased

- **A review run ends with a round that reads the last set of fixes, and the
  record says who did.** A round's findings are closed after it ends, by
  whoever writes the fixes, and the round that follows is what opens them.
  Every round had one except the last, whose fixes were written by the
  session that then ticked `- [x] Pass` on its own record. Measured across
  two consecutive work items: the one round that ever looked at another
  round's fixes found **seven** defects inside them, and its own fixes then
  went in unread. (#33)

  Two changes, and they meet at one cell.

  A run now ends with a **verifying round** — spawned after the previous
  round's fixes are committed, targeted at the diff of those fixes rather
  than at the branch, and asking whether each closed finding is actually
  closed. **A round that opens nothing needing a fix does not consume the
  cap**, because the cap counts rounds that found something and a round that
  finds nothing is the loop having converged. The three-round and five-round
  numbers are unchanged. This is not the rule that a round has to find
  nothing: a 🟡 the smith answers with grounds has opened nothing needing a
  fix, and the run ends there.

  And `round-N.md` carries `| Fixes checked by |` beside `Pass`. `Pass` says
  the findings are closed; this says who opened the work that closed them.
  Three values and no others — `round-N` naming a LATER round, `no fixes to
  check`, or `nobody — <why>`. `chain_check.py` reads it on every record and
  refuses what the repository can contradict: a round naming itself, a
  checker git does not carry, and `no fixes to check` beside a verdict that
  closed with a fix.

  **`nobody — <why>` passes**, and prints on every run. A work item can still
  ship with its final fixes unopened; what changes is that the state is in
  the diff instead of in a session that has ended. Failing for an honest
  disclosure is what teaches people to write none.

  **Every existing round record needs the new row**, not only the newest.
  There is no fallback, for the reason `docs/review-handoff-protocol.md`
  gives for the `rounds/` move: the failure names the row and the three
  values it takes. Write `| Fixes checked by | round-N |` on each record
  whose fixes a later round opened, and `| Fixes checked by | nobody — <why> |`
  on the last one if nothing did.

- **The agent files say that file edits go through the `Edit` tool**, and
  they name both reasons rather than only the familiar one. An edit must be
  able to fail, which is why a shell substitution that misses its pattern is
  an unverified edit. And no Bash command line exists, so the commit gate has
  nothing to read.

  The second reason is what a session hit. The gate reads a heredoc body as
  shell, because a commit hidden in one used to walk straight past it, and
  two kinds of segment count. One has a commit in it: a command word of
  `git` with the `commit` subcommand, which a partial patch to a file
  carrying shell commands as test data can leave in command position, and
  which a document showing a waiver example carries on purpose. The other
  has no commit at all: a segment the reader cannot expand, so an `eval`
  argument holding a variable, a command substitution or a glob stops the
  session with no `git` in the body. Neither command commits anything, and
  the prompt reaches whoever is at the keyboard — in an unattended run,
  nobody. (#34)

  The gate is unchanged. Whether it should skip a heredoc body that is being
  written to a file rather than run is a separate decision, and it is
  recorded as an open question on the work item instead of being made here.

## 0.0.1 — 2026-08-31

- **Initial release.** An implement/review agent chain with hook enforcement,
  an evidence ledger with drift detection, and a tool-agnostic review handoff
  protocol.

  The gates ship opt-in: a repository is judged only once it says so, and
  every gate that cannot read its input fails toward asking rather than
  toward silence. `specs/` holds a work item's documents and
  `.specseal/` holds the ledger that points into the code.

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
  checker git does not carry, a checker whose own `Target SHA` is the same
  commit as this record's or an ancestor of it — the number is later and the
  review is not — and `no fixes to check` beside a verdict that closed with a
  fix. Where either record's `Target SHA` names two commits — the row allows
  both when HEAD moved mid-review — the newest on each side is compared.

  A verdict cell is read by stripping markdown emphasis and matching the
  vocabulary against the START of the cell, so `**fixed** \`sha\`` counts as
  the fix it is whatever follows the word, while a long `answered` cell that
  mentions a fix made elsewhere still does not. The first version instead
  looked for where the commit began and cut there, which meant it had to
  recognise a commit: a seven-character abbreviation with no digit in it —
  about one in 959 — was not recognised, nothing was cut, and a blocking
  finding that had been properly closed read as still open.

  And `round-N.md` carries `| Needs a fix |`: whether this round opened
  anything that does. It is the reviewer's own answer, copied rather than
  re-derived from the verdict table, because a finding the implementer answers
  with grounds needs no fix and still ends the run. No check reads the row —
  it is there because the answer a run ends on had nowhere to live but a
  transcript. **Existing records are not migrated for this one**, unlike
  `Fixes checked by`: a reviewer who was never asked left no answer, and
  filling the cell in from the verdict table is the derivation the field
  exists to refuse.

  **`nobody — <why>` prints on every run, and fails in one place**: on the
  run's last record, beside a checked `Pass`. That pair is the review claiming
  to have passed while the fixes that closed its findings went unread.
  Anywhere else the cell only prints, because failing for an honest disclosure
  is what teaches people to write none.

  **Work items begun before this release are excused that refusal** and only
  print. The cutoff is the unix second already in a work item's directory
  name, compared against one constant, so nothing needs configuring: a fresh
  install is held to the rule everywhere, and a repository updating the plugin
  has exactly its existing items excused. A check whose first act is red on
  merged history nobody can honestly repair is a check people learn to skip.
  The way out for everything after the cutoff costs no round — one verifying
  round at the diff of those fixes.

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

- **A change to a gate now answers for what it costs in interruptions.**
  `CONTRIBUTING.md` asked three things of one — a test seen red, a stated
  failure direction, platform honesty — and none of them was the price the
  change puts on whoever is at the keyboard. A fourth is added: say how many
  times the change stops to ask a person, and if it adds one, say why nothing
  cheaper reaches the same guarantee. It is the item a passing suite cannot
  report on, because nothing counts interruptions. (#43)

  The goal that budget is drawn against is now stated where a design is
  chosen rather than only where a procedure is followed. `implement` already
  carried the reasoning to every session that loads it, but a person deciding
  between two mechanisms reads the ticket and `CONTRIBUTING.md`, and neither
  said a prompt was a cost.

  Nothing changes for anyone installing the plugin. Both files are
  contributor-facing, and `install.sh` distributes only the marker block in
  `CLAUDE.md`, which keeps its size.

- **`writing-style` produced text that satisfied it and could not be read,
  and three things about the file explain why.** (#9)

  **The per-document sections looked complete.** Someone opening the file to
  write a PR body starts at that section, reads its table, and applies it.
  The line saying the sentence rules for their language apply too sits two
  hundred lines above, where they never went. Each of those sections now says
  it at the top: what follows adds to the sentence rules and never replaces
  them.

  **There was no way to notice the jargon was yours.** Every example was a
  word from somebody else's domain, so it read as somebody else's vocabulary
  — while the word learned from this codebase an hour ago already feels like
  ordinary language. A mechanical test replaces the judgment: if you first
  met the word here, in the code or in a policy document, it is jargon. The
  word class that actually leaks is named too, because a list never
  enumerates it.

  **Conversation with the user was not one of the kinds of writing.** It is
  the one written most, and the density that makes a PR body precise makes it
  unreadable. It now has a row in the opening table and a section of its own.

## 0.0.1 — 2026-08-31

- **Initial release.** An implement/review agent chain with hook enforcement,
  an evidence ledger with drift detection, and a tool-agnostic review handoff
  protocol.

  The gates ship opt-in: a repository is judged only once it says so, and
  every gate that cannot read its input fails toward asking rather than
  toward silence. `specs/` holds a work item's documents and
  `.specseal/` holds the ledger that points into the code.

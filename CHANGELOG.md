# Changelog

## Unreleased

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

# Changelog

## Unreleased

- **The agent files say that file edits go through the `Edit` tool**, and
  they name both reasons rather than only the familiar one. An edit must be
  able to fail, which is why a shell substitution that misses its pattern is
  an unverified edit. And no Bash command line exists, so the commit gate has
  nothing to read.

  The second reason is what a session hit. The gate reads a heredoc body as
  shell, because a commit hidden in one used to walk straight past it, and it
  counts a segment whose command word is `git` with the `commit` subcommand.
  Two kinds of edit leave one in a body: a partial patch to a file that
  carries shell commands as test data, where the quoting of that fragment can
  put a commit in command position, and a patch to a document that shows a
  waiver example verbatim. Neither command commits anything, and the prompt
  reaches whoever is at the keyboard — in an unattended run, nobody. (#34)

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

### Fixed

- Every Python file the plugin ships, and the three Python one-liners its
  instructions hand a session, name the encoding they read and write in,
  and a branch that adds a call that does not now fails on every CI leg
  instead of only on Windows (#741). A call with no `encoding=` takes the locale's, which is
  cp1252 on `windows-latest` and UTF-8 on the other two legs, so the class
  showed only on the one leg nobody runs locally: #736 met it after review,
  when a ledger row's ` · ` came back as U+FFFD and 26 cases failed there
  alone. A new test module walks every tracked Python file and names each
  `open`, `read_text`, `write_text`, text-mode `subprocess` call and their
  standard-library relatives that sets no encoding, with a classification
  table for the rare unit that cannot name one. A `python3 -c` line in a
  skill or a workflow is outside its reach, and `CONTRIBUTING.md` says so. It found 29 sites in the hooks and release
  scripts and 302 in the tests, and each now reads and writes UTF-8. A hook
  read that would newly raise on a stray byte reads with `errors="replace"`
  instead, because a raise inside a hook lets the work through.
- The three git hooks put their streams in UTF-8 before they print, like
  every other hook entry point. On a console that cannot encode an em dash,
  the commit gate's refusal used to arrive with each `—` and `…` spelled
  `\u2014` and `\u2026`, including inside the waiver it tells the reader to
  type. The same test module now holds every hook entry point to that call,
  and `CONTRIBUTING.md`'s House rules states both rules.

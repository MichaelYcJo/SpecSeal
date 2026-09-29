### Fixed

- A row of `config.md` parked in an HTML comment that closes is no longer a
  row (#667). The mode gate, `broad-gate` and `seal mode` all read the table
  through one walk, which hides a line inside a fenced block or a comment
  block that begins its line and closes, by CommonMark's own block rules. A
  line the walk cannot be sure of — inside a list item, after a `<!--` in the
  middle of a line, below a block that never closes — is read exactly as
  before, so a fence nobody closed still hides what it hid and a `<!--`
  nobody closed hides nothing. A table under a closed comment that quotes a
  fence line is read again, and no fence inside such a comment is named as
  left open. Where the only `Broad gate` row is commented out, `broad-gate`
  quotes it back as commented out and runs nothing. All 519 tracked markdown
  files in this repository read the same rows as before.
- A `routing.md` row quoted in a fenced example or parked in an HTML comment
  no longer answers for the declaration (#658, #667). The last row of a label
  wins, so an example below the table saying `straight to the PR` used to
  decide whether a reviewer saw the work. The commit gate and CI's chain check
  now read only the rows a renderer shows, by the same walk as `config.md`; a
  table wholly inside a closed fence or comment is no declaration, and the
  gate asks as it does for any declaration that does not parse. A fence or a
  `<!--` nobody closed hides nothing, so every declaration that read before
  still reads: all 27 committed here and the template parse the same.
- The rider check no longer fails on a rider quoted in a fenced example in a
  markdown file (#667). Such a line was read as a rider with no stamp, BROKEN
  at exit 2, for a line nobody wrote as one. A marker line inside a fenced
  block that closes now opens no rider; a fence line inside a rider's own
  comment opens nothing, and a fence nobody closed hides no rider below it.
  Every file the check reads here gives the same riders as before.

### Changed

- The suite takes one test-only package, `markdown-it-py`, pinned to 4.2.0 in
  `.github/scripts/run_tests.py#MARKDOWN_IT` (#667). It is the CommonMark
  parser the hook readers are now checked against, so the check shares no code
  with what it checks. `bin/test` builds it into `.venv` and adds it to one it
  adopts, and CI installs the same pin. The gates stay stdlib-only, and a
  repository that installs the plugin installs nothing new.

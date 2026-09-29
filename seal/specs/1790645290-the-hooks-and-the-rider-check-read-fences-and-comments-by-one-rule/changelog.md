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

### Changed

- The suite takes one test-only package, `markdown-it-py`, pinned to 4.2.0 in
  `.github/scripts/run_tests.py#MARKDOWN_IT` (#667). It is the CommonMark
  parser the hook readers are now checked against, so the check shares no code
  with what it checks. `bin/test` builds it into `.venv` and adds it to one it
  adopts, and CI installs the same pin. The gates stay stdlib-only, and a
  repository that installs the plugin installs nothing new.

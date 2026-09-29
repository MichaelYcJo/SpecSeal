### Changed

- The suite takes one test-only package, `markdown-it-py`, pinned to 4.2.0 in
  `.github/scripts/run_tests.py#MARKDOWN_IT` (#667). It is the CommonMark
  parser the hook readers are now checked against, so the check shares no code
  with what it checks. `bin/test` builds it into `.venv` and adds it to one it
  adopts, and CI installs the same pin. The gates stay stdlib-only, and a
  repository that installs the plugin installs nothing new.

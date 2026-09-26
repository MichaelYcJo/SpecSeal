### Changed

- **A ledger coordinate that does not parse no longer fails a lenient
  `evidence-check` run: `MALFORMED` now exits 1, like drift, and exits 2 only
  under `--strict`.** In 0.15.4 it exited 2 either way, so a repository
  running the check without the flag, or through `evidence-ci`'s lenient
  recipe, went red on update. The row is still named with what to write
  instead, and a lenient run still ends by saying that `broad-gate` runs the
  same check with `--strict`, where `DRIFTED` and `MALFORMED` are exit 2. The
  readers that decide still refuse it: `broad-gate` and the vendored CI
  template both pass `--strict`. `OLD-FORMAT` is unchanged at exit 2 either
  way. This is the repository owner's answer to #606's open question. The
  skill's verdict and reader tables, `evidence-ci`'s step on `--strict`, the
  template's comment and this repository's CI warning now say so, and the
  warning names both causes of exit 1 instead of sending a malformed row to
  `--reverify`.

### Fixed

- **`evidence-check` stops reading prose as a broken coordinate at four
  edges, and names one coordinate it used to miss (issue #614).** A version
  after a dotted name (`chart.js@4`) was read as a path followed by a hash;
  a hash is now six hex characters or more. An issue number followed by a
  possessive, a dash, a curly quote, a Korean particle or a link's `](`
  (`org/repo#299's`, `org/repo#299에서`) was refused; digits that no ASCII
  letter, digit or underscore continues are an issue number now. A code span
  holding a decorator and a comment (`` `@lru_cache  # memoized` ``) or a
  mention inside a comment was refused for holding both marks; they now
  count only where the `@` follows the `#` with no space between them
  outside quotes. And a file name with no dot followed by a quoted line,
  `<module>` or an `_name` (`Makefile#"all: build"`) was silent; it is named
  now. What this gives up: `src/a.py@abc` with a hash shorter than six
  characters, `docs/a.md#1장` with no hash, `Makefile#1x`, and a path-less
  `#handler @abcdef12` are not named.

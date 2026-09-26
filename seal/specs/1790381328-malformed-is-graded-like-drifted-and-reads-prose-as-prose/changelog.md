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
  edges, and names coordinates it used to miss (issue #614).** Five rules
  changed, and every verdict that moved from 0.15.4, over a generated set of
  2 426 shapes read in a code span and as bare words, falls under one of
  them. Each rule gives up some coordinates along with the prose it was
  written for:
  - A path followed by `@` takes a hash only of six hex characters or more.
    `chart.js@4` is prose now, and so is `src/a.py@abc`.
  - A locator opening with digits that no ASCII letter, digit or underscore
    continues is an issue number, whatever follows the digits.
    `org/repo#299's` and `org/repo#299에서` are prose now, and so are
    `docs/a.md#1-scope`, `docs/a.md#1장` and `src/a.py#1>"x"`. Such a
    coordinate is still named when its `@` is glued to it
    (`docs/a.md#1장@abcdef12`).
  - `#` and `@` count as one coordinate only where they are glued: no space
    between them outside quotes, a quoted part keeping its spaces only
    inside a code span, and no quote left unclosed. Otherwise each word is
    judged alone. `` `@lru_cache  # memoized` `` is prose now, and so are
    `#handler @abcdef12`, `docs/a.md#1-scope @abcdef12` and
    `#handler>"a"b"@abcdef12`; `src/a.py#handler @abcdef12` is still named.
  - A file name with no dot followed by a quoted line, `<module>` or an
    `_name` is a coordinate: `Makefile#"all: build"` is named now, and so
    are `C#"hello"` and `vector#<T>`. `Makefile#1x` is still not named.
  - A locator opening with a digit that is not a decimal digit (`²`, `①`)
    is not an issue number, so `docs/a.md#²` is named now.

  A run of `#` characters outside quotes no longer takes seconds to read.

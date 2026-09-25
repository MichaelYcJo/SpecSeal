- **On `cmd.exe`, a switch written straight after a program runs again
  (issue #596).** Since 0.15.3 the broad gate wrote `/` as `\` inside every
  command name it hands `cmd.exe`, so `bin/test` could reach `bin/test.cmd`.
  That also turned `xcopy/e/i` into `xcopy\e\i`, which `cmd.exe` cannot find,
  so a row that ran before stopped running. The gate now rewrites a name only
  where the part before its first `/` names a directory where the row runs.
  `bin/test` is still handed over as `bin\test`, and `xcopy/e/i`,
  `findstr/s` and `ipconfig/all` reach `cmd.exe` as written. A name that
  begins with `/` still counts, because the drive's root always exists.
  `templates/config.md` §*Broad gate* states the rule and its two bounds. A
  directory that an earlier command in the row makes or enters is not seen.
  A directory at the root named like a program makes that program's glued
  switch read as a path, and a blank before the switch avoids both.
- **The suite reads a workflow's text one way (issues #482, #462 and
  #463).** Cases that read `.github/workflows/hygiene.yml` each had their own
  idea of what a comment is. One counted a flag written in a comment as a
  base, and six cut the file at the first place a script's name appeared,
  which a comment could move. `tests/conftest.py` now holds one comment rule,
  a step found by its name, and the one step whose code runs a script, and
  those six cases read through them. A `BASE:` counts as a base only under
  `env:`, and an empty base fails the spelling check by name instead of
  raising `TypeError`.
- **The broad gate no longer asks two questions that CI skips on a release
  pull request (issue #473).** SpecSeal's own workflow skips the survivor
  step and the correction step when a pull request goes into `main`, and the
  gate still ran both arms there. The gate now leaves them out when the base
  it was given names `main` and the repository's `hygiene.yml` carries those
  two steps, and it prints one line saying so. A repository with no such
  workflow runs both arms against `main` exactly as before. A case holds the
  gate's list against the workflow's own guards, so a guard added to a third
  step, or dropped from one of the two, fails the suite.

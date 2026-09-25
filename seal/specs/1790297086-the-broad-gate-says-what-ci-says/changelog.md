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

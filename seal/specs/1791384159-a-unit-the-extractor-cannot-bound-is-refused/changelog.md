### Fixed

- **A multi-line TypeScript signature keeps its body in the evidence hash
  (#848, #870).** A ledger row citing a function whose parameters run over
  several lines, the way Prettier writes them, hashed only the declaration
  and parameter lines, so a rewrite of the body still read `ok` and
  `--reverify` had nothing to notice. In TypeScript, JavaScript, C, C++, C#,
  Java, Kotlin, Swift, Go and Rust a unit now ends where every bracket it
  opened has closed, with each language's strings, chars and comments read
  as text; an Allman `{` on its own line belongs to the function above it.
  A unit whose brackets do not balance, or whose string or comment never
  ends, is `BROKEN` with the reason on its line.

### Changed

- **A unit no rule can bound is refused rather than guessed at (#870).** A
  bare symbol in a file of any suffix other than `.py`, `.pyi`, `.md`,
  `.yml`, `.yaml` and the brace languages above — Ruby, shell, Lua, TOML, a
  file with no suffix — reads `BROKEN` with "no bounding rule for `.rb`;
  anchor a quoted line instead", and a quoted-line anchor
  (`path#"a line of the unit"@hash`) still resolves there as it always did.
  A bare symbol in a `.py` the running Python cannot parse reads `BROKEN`
  naming that Python's version and the error's line, where it used to be
  read by the text rule. A YAML key's `- ` items written at the key's own
  indent now belong to the key.

  **What an installer sees on upgrade.** The commit hook reads the new rule
  at the next commit after the plugin updates; the CI copy under `tools/`
  changes when `/specseal:evidence-ci` is run again. At either moment:
  a row citing a brace-language unit whose body the old span left out reads
  `DRIFTED` once — re-read that unit, then run `evidence-check --reverify`,
  rather than re-stamping without reading; a row citing a bare symbol in a
  suffix with no rule, or in a `.py` the interpreter cannot parse, reads
  `BROKEN` with the remedy on its line — rewrite it as a quoted-line anchor,
  or under `Ledger frozen from` take the `Corrected ·` repair `--reverify`
  names; every other row keeps its hash and its verdict.

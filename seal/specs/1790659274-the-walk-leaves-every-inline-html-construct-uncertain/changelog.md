### Fixed

- A `Mode` or `Broad gate` row written after a line break only Python's
  `str.splitlines` makes, inside a CDATA section, a processing instruction, a
  declaration or an HTML tag's quoted attribute value that its line opened, is
  no longer read (#673). A renderer shows none of it, but the reader used to
  read it whenever a fence run stood earlier on the same line, because it
  looked for a `<!--` alone. Every kind of inline HTML is now treated the way
  a mid-line `<!--` was: text that starts inside one a line left open, and the
  rest of that paragraph, is read exactly as before. Where such a row was the only one,
  the mode gate asks and `broad-gate` refuses, as they do for any row that is
  not there. All 577 tracked markdown files in this repository read the same
  rows as before; the routing declaration and the rider check read nothing
  differently.

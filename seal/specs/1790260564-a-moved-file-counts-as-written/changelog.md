### Fixed

- `survivor-check` reads a gathered changelog fragment the way it leaves one
  out (#564). The text it holds at a release is read at every path it
  already keeps out of the range, not at one spelling of that path. A
  released section ends only at another version heading or an `Unreleased`
  heading, so a `## ` line inside a gathered fragment no longer turns the
  rest of the fragment into live prose. Text is read with CRLF line endings
  turned into LF, so a `CHANGELOG.md` committed with CRLF still has its
  gathered ids. Each of the three let a release's gathered text subtract a
  survivor that a correction in the same commit left standing.
- `survivor-check` holds text a range moved to another path instead of
  counting it as the range's own writing (#563). A sentence removed at one
  path and added unchanged at another, one copy for one, is neither removed
  nor written. This covers a file moved whole, a rename, and a document
  split into two files that both remain. Before, the moved text subtracted
  everything it shared with a correction made elsewhere in the same range,
  so a quote the move carried hid itself and every other copy of the
  corrected claim. A pure move is still silent, now because it removes
  nothing: the report reads `against 0 sentence(s)`, and any range that
  moves text reports a lower count than before.

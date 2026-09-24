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

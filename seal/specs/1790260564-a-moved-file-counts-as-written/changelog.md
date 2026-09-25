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
- A `survivors.md` range row in local mode now holds over its own work
  item's range (#554). Local mode keeps `seal/` under the git directory,
  where nothing is committed, so no range ever touched the work item's
  directory, and every local declaration printed `not yours` on the branch
  it was written for. There the owner is the `Branch` row of the work item's
  `routing.md`: the row holds over a range whose tip is on that branch and
  on no local branch that one was cut from, and another branch's range
  still refuses it. A refused row's `not yours` line
  now names the test that refused it. Shared mode is unchanged.

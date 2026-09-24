### Fixed

- `survivor-check` no longer lets a gathered changelog fragment silence a
  survivor at a release (#557). A release that renames `## Unreleased` to a
  version, or rewords an entry as it releases it, loses a sentence, and the
  sweep then counted every newly released sentence as wording the range
  wrote, the gathered fragments' text included. Where a fragment quoted
  wording that a correction in the same commit removed, the copy still
  standing in another file was subtracted and the sweep exited 0. A gathered
  fragment's text is now read where it stood before the release and is held
  but never counted as written, whether the release leaves the fragment in
  place or deletes it, and a fragment whose body opens with prose is held
  the same way. Releases with no `## Unreleased` section, which is this
  repository's shape, never reached it.
- The release write-back's `lost` guard is pinned by a case of its own
  (#555). Removing it used to leave the module green; now a release that
  writes its entry in place and loses nothing goes red without it, and the
  gathered-release case #555 described goes red only when both the guard and
  the new fragment filter are removed.

### Changed

- Each release's notes are a file of their own (#728). `CHANGELOG.md` had
  reached 8,891 lines, and a reader who wanted one release read or grepped
  all 44. Every released section now stands, byte for byte, in
  `changelog/<X.Y.Z>.md`, and `CHANGELOG.md` is the index: one heading per
  release, newest first, the same line the release's file opens with,
  followed by a link to that file. Joined newest first, the files reproduce
  the old file exactly. A link to the old file at an older tag keeps
  resolving at that tag.

- The release tooling moved with the notes. `gather_changelog.py --version
  X.Y.Z` writes the release's file and puts its heading in the index; a
  second gather appends into the file and keeps its date, as before.
  `--check` reads the markers of every release file, each on its own. The
  release note reads the release's own file and links to it at the tag, and
  fails as before when the file is missing or carries no section. Release
  preparation stages `changelog/` and `CHANGELOG.md` with the fold's paths
  before the suite runs.

- The survivor sweep reads a release's own file as a changelog. Its released
  lines are out of the pool and the range, a fragment its marker gathered is
  excused, and a range across the move writes none of the released text it
  moved as its own. A repository that keeps one `CHANGELOG.md` is read as
  before.

- `/specseal:update` names what changed from the release files of every
  version between yours and the new one. The update into this release is
  run by the skill you already have, which checks the install by the index's
  first heading, still there, and reads `CHANGELOG.md` for the summary: that
  one time it meets the index and has to follow its links.

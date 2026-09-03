- **Local mode's records can be carried to another machine, and taking one
  in never overwrites what is already there.** Two new commands,
  `seal export` and `seal import`, on the Bash tool's PATH while the plugin
  is enabled. Local mode keeps the ledger and the work-item records under the
  common git directory, so a new machine or a re-clone starts with nothing —
  that is the mode's whole trade-off, and it now reads as *take a copy*
  rather than *lose it*.
  `seal export` writes the root, and only the root, to
  `seal-<repo>-<date>.zip` beside the clone, with a manifest naming the
  remote URL and the HEAD SHA at export. **The smith mark, the worktree
  choices, the review and parity marks, every lease and the export's own
  state sit beside the root**, so none of them travels: the export walks the
  root and nothing else, which is why the design requires the root to be its
  own directory. A symbolic link inside it is skipped and named rather than
  followed — the one way out of that structure.
  The zip lands beside the clone rather than in it, because the ordinary
  place to run the command is the repository root and an untracked zip there
  is one `git add -A` from committing the records local mode exists to keep
  out of the tree. `--output` overrides it and says so when the path is
  inside the tree.
  **`seal import` never overwrites and never asks.** A file that is not there
  is added; one that is there with the same bytes is left alone, so
  re-importing the same zip writes nothing at all; one that is there with
  different bytes gets the incoming copy beside it as
  `<name>.incoming<ext>` — `ledger/<id>.incoming.md` next to
  `ledger/<id>.md` — and the collision is listed. Which of a pair is right is
  a reading rather than a merge, and no answer the command could pick would
  avoid sometimes throwing work away. It names `evidence-check .` as the next
  step instead of running it and reporting a pass nobody read.
  It refuses, writing nothing, for a zip from another repository (with
  `--allow-other-repo` where the two are one repository under two spellings —
  ssh at one machine and https at another compare equal), for a member that
  would land outside the root, and where both roots already exist.
  `--into shared` or `--into local` creates the named mode's root, which is
  the second way to switch modes.
  **In shared mode `seal export` writes no zip.** The records are committed,
  so every clone and CI already have them, and a zip would be a second copy
  that nothing keeps current. It prints the path and the `mv` that switches
  to local mode, and exits 1 — so `seal export && cp seal-*.zip …` does not
  copy nothing and report success.
  Once per release, `seal export --check` prints one line — how many work
  items changed since the last export — and uploads nothing anywhere. Where
  the copy goes is the user's business. It counts work items only, so a
  change confined to `follow-up.md` reports 0; the line's wording is fixed by
  the design, and widening it is recorded as an open question rather than
  taken silently.
- **One claim was corrected by measuring it, and the correction is why the
  import is stricter than it was designed to be.** This work was planned
  around "`extractall` is the classic path-traversal sink". On the CPython
  the plugin ships on that is false: it already strips `..` and a leading `/`
  from a member's name, and writes a symbolic-link entry as an ordinary file.
  What actually disqualifies it is that it **overwrites**, and that it writes
  through a symbolic link in the destination. That second one is a real
  escape, the import's own writer had it too, and it is now refused before
  anything is written. The member-name validation was kept regardless: a
  defence that holds only while a standard-library sanitiser keeps its
  current shape is not one this plugin can claim.
- **Review then measured the same claim one level down and found it still too
  narrow.** The check that closed the escape walked every directory above a
  member and stopped short of the member itself, so a symbolic link named for
  the record was never looked at. A broken one reads as absent, so the file
  was treated as new and written straight through the link, outside the root,
  at exit 0 with nothing printed. The check now covers the leaf, and three
  documents that called the directory case the only way out say what was
  measured instead.
- **Review then found the same escape one name over, and it is closed at two
  levels.** A collision does not write to the member's name — it falls back to
  `<name>.incoming<ext>`, and the check that refuses links had never seen the
  fallback names. A broken link there read as absent, so the copy was written
  straight through it, outside the root, at exit 0 and printed as an ordinary
  collision. The sender of the zip chooses whether the collision happens at
  all, by sending bytes that differ. Every candidate name is now read as a
  link rather than as a file, and the write itself opens with a flag the
  kernel refuses to follow a link through — so a name that becomes a link
  after it was checked is refused too.
- **An import now refuses a zip that declares more than a root of records
  holds, and a zip whose data does not match its own checksums.** Each member is read whole, and the zip arrives from another
  machine, so its declared sizes are the sender's choice: a 408 KB file
  declaring 400 MB in one member wrote 419 MB and took as much memory, in
  0.2 s. A member is capped at 32 MB and an archive at 512 MB, and the total
  is summed before the manifest is parsed — that read is unbounded too, so a
  400 MB `manifest.json` used to take 400 MB of memory on its way to being
  rejected. A bad checksum was the other way in: a zip whose central directory
  is well formed and whose data is corrupt used to write the records before
  the corrupt one and then die on a traceback, which is a partial import from
  a zip that chose to be one.
- **Two smaller corrections.** A clone holding both roots is now refused
  however the import is asked, including with no `--into` flag — the case the
  specification and both READMEs describe was the one spelling that still
  wrote. And a repository with no commit yet records an empty SHA in the
  manifest rather than the four letters `HEAD`, which is what `git rev-parse`
  prints on its way to exiting 128.
- **The third round opened the half the first two never had, and found the
  same shape there.** Both earlier rounds read the import. `seal export`
  writes its zip to a temporary name first, so a failed write leaves no half
  archive — and that name is `seal-<repo>-<date>.zip.partial`, beside the
  clone, which anyone can predict. A symbolic link planted there took the
  manifest and every record outside the clone at exit 0, while the command
  printed `wrote <path>` for a path that was the link. The temporary name is
  now opened with the same flag the import writes with, and the zip's own name
  is read as a link rather than as a file — a check whose docstring claimed
  the import shared it, which is why the import's fix never visited it.
- **A zip can no longer end an import in a traceback.** Three ways in: a
  member the build cannot decompress, an encrypted member, and a corrupt
  manifest — the last one because the manifest was read before the data was
  checked. The checks now run in one order, largest question first: how many
  members, how many bytes, what the names are, whether the data reads, and
  only then what the manifest says. A member count is bounded too, because
  both size bounds count bytes and a zip of 300,000 empty members wrote
  300,002 files into the root at exit 0.
- **And a name that has to be a directory for the zip and is a file is
  refused before anything is written.** `os.makedirs` raised on it mid-write,
  leaving the records before it on disk. The sender corrupts nothing to reach
  it — two members named that way is enough — and the root's own contents
  raise it from the other side.
- **The fourth round found no way out of the root, and one thing the fix
  before it had broken.** Refusing to write through something at the export's
  temporary name also removed it — a link, a file somebody left, or a
  concurrent export's archive still being written, which loses that export the
  zip it was about to rename. The cleanup that removes a half-written archive
  is for a name this command created, and it now runs only for one.
- **A zip can no longer end an import in a traceback for a reason the
  filesystem gave, either.** The check for a name the zip needs as a directory
  asked whether it was a file, and a named pipe is not a file — it walked past
  and met the same crash. And nothing at all guarded the write loop: a
  directory in the root that cannot be written into, or a full disk, left a
  partial copy and a traceback. Both stop with a line of their own now, and
  the second says what is true — this command overwrites nothing, so running
  it again finishes the copy.
- **A zip from a later version of this format is told so.** The name checks
  ran first, and a later format is exactly what moves the names they read, so
  a zip declaring format 2 was answered as a malformed zip rather than as a
  build too old. The format field exists for no other day.
- **Two messages stopped sending people to the wrong place.** A clash inside
  the zip told a person to rename a file that was not on their machine, and
  the Korean README described that clash as always coming from their own clone.

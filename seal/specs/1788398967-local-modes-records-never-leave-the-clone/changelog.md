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
- **An import now refuses a zip that declares more than a root of records
  holds.** Each member is read whole, and the zip arrives from another
  machine, so its declared sizes are the sender's choice: a 408 KB file
  declaring 400 MB in one member wrote 419 MB and took as much memory, in
  0.2 s. A member is capped at 32 MB and an archive at 512 MB, both read
  before a byte is written.
- **Two smaller corrections.** A clone holding both roots is now refused
  however the import is asked, including with no `--into` flag — the case the
  specification and both READMEs describe was the one spelling that still
  wrote. And a repository with no commit yet records an empty SHA in the
  manifest rather than the four letters `HEAD`, which is what `git rev-parse`
  prints on its way to exiting 128.

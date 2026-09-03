<!-- seal/specs/1788420761-the-settings-live-in-a-file-nobody-opens/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`/specseal:config` shows what this repository decided for itself, and
  changes any of it.** Three rows live in `seal/config.md` — the language the
  commits and pull requests are written in, the language the records are
  written in, and which of the two places the root lives at — and until now
  the only way to see any of them was to open a file nobody has a reason to
  open. First setup asks its questions once and never again; this is how to
  ask them later.
  It shows rows that are absent as well as present, with the default and
  where it comes from, because a row a repository never set is the most
  likely one somebody wants to change. For the mode it runs `seal mode` and
  reports what that says — the folder, the row, and whether they agree —
  rather than reading the row itself, since a second reader is a second
  answer.
  **A change is routed to whatever owns that row.** A language row is only a
  row and is edited in place. The mode row moves a directory, stages a
  commit, and installs or removes the pull-request workflow, so the skill
  runs `seal mode` and reports that list rather than saying *done*. Before
  switching to shared it says what cannot be undone: the commit, not the
  move, is the point of no return. (#105)

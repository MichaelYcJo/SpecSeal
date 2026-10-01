### Added

- **A `Reference specs` row in `seal/config.md`** (#688) names the
  directories a project keeps its own specifications in. The plugin reads
  them as history and never moves, edits or checks them as its own records.
  With no row, every directory named `specs` outside `seal/` is one; the
  value `none` declares none. `templates/config.md` §*Reference specs* says
  what the row governs and what the default costs: a repository whose own
  tests sit in a `specs/` directory gets them back in the survivor sweep with
  `Reference specs | none`.
- **The agents and skills that read the tree say what a reference root is
  to them** (#688). The framer, the smith, the warden, `settle` and the
  implement skill each read a project's own `specs/` where the work touches
  what it describes, cite what they read in `spec.md` or a standing
  statement, and never write there; the warden opens such a citation in its
  first stage like any other coordinate.

### Changed

- **`survivor-check` leaves a project's own `specs/` out of its search**
  (#688). A team's document carrying wording a range removed used to be
  reported as a survivor, and a team's own edit to it was read as a
  correction the plugin's documents owed. A reference root is now out of
  both the pool and the range, and a top-level `specs/<x>/` a range deletes
  is never treated as a retired work item.
- **`unverified-check .` no longer fails on a team's own overview** (#688).
  Its walk leaves a reference root out, and its comparison against a base
  leaves out the same files, so a team removing its own overview is not
  reported as a deleted record. A file or a directory named on the command
  line is still read. A repository with no `seal/` root is read as before,
  because the only layout the plugin knew without a root is 0.3.x, whose
  top-level `specs/` was its own.

### Fixed

- **A project's own `specs/` is no longer moved into `seal/` at session
  start** (#688). The session-start hook that brings a 0.3.x repository up to
  the `seal/` layout used to move every `specs/<x>/` whose name looked like a
  work item's, `<unix-seconds>-<slug>`. A team that keeps its own
  specifications under such names had them taken, and its ledger rows citing
  them re-pointed to a path that never appeared. A directory moves now only
  when it carries the plugin's own marks, a `routing.md` or a file under
  `rounds/` directly under it that git tracks — an empty or ignored
  `rounds/` is not one. Every 0.3.x work item carried `routing.md`, so an old
  layout still moves whole. Anything else stays, keeps the rows that cite it,
  and is named in the hook's line as *no routing.md or rounds/ that git
  tracks — not a SpecSeal work item*. A repository holding nothing else of the old layout
  hears nothing.
- **First setup asks a project with its own `specs/` where the root goes**
  (#688). The bootstrap used to read any top-level `specs/` as the 0.3.x
  layout, tell the person the plugin would move it, and skip the shared/local
  question. It reads the same two marks now: a `specs/` without a marked
  entry is the project's own, the question is asked as in any repository with
  no root, and the directory is left where it is.

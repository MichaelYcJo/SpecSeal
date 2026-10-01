### Fixed

- **A project's own `specs/` is no longer moved into `seal/` at session
  start** (#688). The session-start hook that brings a 0.3.x repository up to
  the `seal/` layout used to move every `specs/<x>/` whose name looked like a
  work item's, `<unix-seconds>-<slug>`. A team that keeps its own
  specifications under such names had them taken, and its ledger rows citing
  them re-pointed to a path that never appeared. A directory moves now only
  when it carries the plugin's own marks, a `routing.md` or a `rounds/`
  directly under it. Every 0.3.x work item carried `routing.md`, so an old
  layout still moves whole. Anything else stays, keeps the rows that cite it,
  and is named in the hook's line as *no routing.md or rounds/ — not a
  SpecSeal work item*. A repository holding nothing else of the old layout
  hears nothing.
- **First setup asks a project with its own `specs/` where the root goes**
  (#688). The bootstrap used to read any top-level `specs/` as the 0.3.x
  layout, tell the person the plugin would move it, and skip the shared/local
  question. It reads the same two marks now: a `specs/` without a marked
  entry is the project's own, the question is asked as in any repository with
  no root, and the directory is left where it is.

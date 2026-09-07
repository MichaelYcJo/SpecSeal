- **The update notice and the update procedure now name `/reload-plugins`,
  and say exactly how far the measurement behind it reaches (issue #134).**
  The session-start notice closed with *"Either way, restart to load it"* and
  the skill closed the same way. Both named the move that ends the session you
  are in, and neither named the cheaper one this repository had already
  measured and written down.

  **What a reload was measured to do, and nothing more.** Run 6 of
  `docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md` is the
  only positive case: a sentinel in the version cache came back PRESENT after
  a `/reload-plugins`, and ABSENT in run 5 without one. So a preloaded skill
  body handed to a spawned agent is re-read at a reload, and that is the whole
  of what was established.

  **Three things are stated as unmeasured rather than left to silence**, which
  is the ticket's second acceptance condition. The experiment touched neither
  hooks nor agent definitions, and — the part the ticket itself assumed — its
  sentinel sat in the *running* version's own cache directory, so it shows a
  re-read of the copy already in force and nothing about a session picking up
  a newly installed one. A user reading this notice is in exactly that second
  case. `skills/update/SKILL.md` §5 carries the run that would settle it: run
  6's own method, with a sentinel in a hook and in an `agents/*.md` instead of
  in a skill body.

  Saying *not measured* rather than *not needed* is the point of the
  distinction. A user told the reload is insufficient stops using it; a user
  told it covers everything gets a half-loaded plugin with no way to tell.

  **Every sentence that names the reload says which copy it re-reads.** Without
  that qualifier the notice recommends, as the cheap way to get the release
  that just arrived, a move whose only measured effect is on the version the
  user already has — and the module's own docstring said so thirty lines up.
  The qualifier now sits inside the claim's own sentence in both languages,
  including the two README command-table rows and the two by-hand code
  comments, which are as much an instruction as the paragraph above them.

  **Fifteen sentences moved, enumerated by grep rather than from the ticket's
  list** — which was three lines short and named neither of the Korean
  README's three. Two of the fifteen are code comments inside fenced blocks
  (`# then restart`, `# 그다음 재시작`), which the wrap test skips by design
  and which a reader copying the block copies with it.

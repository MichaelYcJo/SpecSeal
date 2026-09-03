- **A build phase now leaves the same committed, per-segment record a review
  round already does, and both records now say what they were asked to do
  as well as what they found.** What a phase discovered used to reach the
  next phase only if the orchestrator retyped it into the next spawn prompt,
  and it went missing without a trace when it didn't: phase 4 of an earlier
  work item moved a rule out of `agents/smith.md` into an interim home, and
  phase 5 removed that interim home before the rule had actually reached
  anywhere else, deleting it from the repository with nothing recording that
  it had gone missing (#107, #121). New `templates/sdd-phase.md` mirrors
  `templates/sdd-round.md`'s shape for the build side: a field table
  carrying only `Phase` and `Commit` — a phase has no `Target SHA` to
  squash away and no `Pass` checkbox to answer — then `## What this phase
  was asked`, `## What this phase found`, and `## What this phase removes`
  (a table naming what left the tree and where it must land; `none` is a
  valid row, a blank table is not). `templates/sdd-plan.md`, `agents/smith.md`
  and `skills/implement/SKILL.md` are wired to it, so a spawned session
  writes `seal/specs/<work-item-id>/phases/phase-N.md` at each phase's close
  without having to be told twice.
  **Separately, neither a round record nor a phase record said what it was
  *asked* to do, only what it found.** #81's round 1 was the cheapest round
  measured — 7.6 minutes, 29 tool calls, one 🔴 and four 🟡 — because its
  spawn prompt named eight specific things to try to break, in order; that
  fact was recoverable only from a transcript. `templates/sdd-round.md`
  gains `## What this round was asked`, between the field table and the
  verdicts, and `skills/code-review/SKILL.md` instructs the orchestrator to
  copy the round-specific spawn content into it right after posting (#119).
  **Enforcement is a template blank plus a skill instruction, not a gate.**
  A `chain_check.py` refusal for a missing section was considered and set
  aside: it would need a red test, a stated failure direction, a prompt
  budget and a platform-honesty case for a mechanism that has shipped zero
  records yet to measure a cutoff against, and is revisitable once real
  phase records exist to learn from.
  **Two follow-on questions from #119 — naming which plugin version or
  commit ran a segment, and a `CONTRIBUTING.md` paragraph on the
  plugin-copy-in-force confusion — are explicitly out of scope here** and
  recorded as deferred, per the issue's own scoping, rather than silently
  dropped. (#121, #119)

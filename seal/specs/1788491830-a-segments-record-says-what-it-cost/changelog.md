- **A segment's record said what it was asked, what it found and which commit
  it read, and never what ran it.** Every segment of two work items was
  metered this week and posted to the flow log, and not one of those readings
  can be attributed afterwards — they all ran on the same model, and that fact
  lived only in a session transcript. `templates/sdd-phase.md` and
  `templates/sdd-round.md` now carry a `| Ran by |` row, and
  `docs/review-handoff-protocol.md` (draft 1.1) carries it in the field table
  with its `Required` column answered.
  **The row names the agent AND the model**, joined by the word `on` —
  `specseal:smith on <model>`. Either half alone answers neither question the
  numbers raise: an agent without a model cannot be compared against another
  run of the same agent, and a model without an agent cannot be told apart
  from the orchestrating session's own turns. The joining `on` is a word
  rather than a punctuation mark on purpose, because a separator inside a code
  span splits the cell carrying it and that has bitten these records twice.
  **It is the spawning session's row, never the segment's own.** An agent is
  told what it is, so a value it writes about itself is the value it was told,
  and the model is a spawn-time argument the orchestrator chose —
  `agents/*.md` pins none. It is the reach-back `Fixes checked by` and the
  fix-surface rows already make. `skills/code-review/SKILL.md` and
  `skills/verify/SKILL.md` both say so, because they are read by different
  sessions at different moments.
  **`unknown — <why>` is an answer and a bare `unknown` is not**, in the shape
  `nobody — <why>` already has. A session spawning through another harness may
  genuinely have no name for a model, and a vocabulary offering only the
  confident answer gets the confident answer written whether or not it is
  true.
  **`chain_check.py` reads the row**, so it is enforceable rather than true
  only while somebody is awake. An absent row fails for work items begun on or
  after `RUNNER_FROM` and prints for older ones — the fourth cutoff of the
  shape `STRICT_FROM`, `SURFACE_FROM` and `FLOOR_FROM` already carry, because
  a merged record has no honest repair: nobody can recover what ran a segment
  whose session is over. A row that is present and unreadable is refused at
  any age, the split the fix-surface rows already make.
  (#137)

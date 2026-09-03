- **A review run now has a floor as well as a ceiling, and a fix pass now
  has a bound on what it may create.** Three rounds, and five while a 🔴 is
  open, was a ceiling with nothing under it, so it got spent like a budget:
  #81 ran seven rounds and the last three found nothing that leaves the root
  and nothing that crashes. `docs/review-chain-spec.md` and
  `skills/code-review/SKILL.md` now state the floor — **stop when a round
  finds nothing that leaves the root and nothing that crashes** — and say
  where the rest of what that round found goes, which is deferred with a
  named answerer or an issue. The reviewer answers it in a line of its own
  the way it already answers `Needs a fix`, `agents/warden.md` carries that
  line in both the passage that explains it and the report format a reviewer
  copies from, and `round-N.md` gains a row of the same name:
  `| Loses a record or crashes | no |`, or `yes — <what>`. It is a second
  terminal condition rather than the first one reworded, and the two come
  apart — a round can need a fix and still stop the run — so the three files
  that called `Needs a fix` *the* answer the run ends on now call it one of
  two. **The verifying round is what the floor leaves standing**: a record
  that met the floor may be followed by one more, the round that reads the
  diff of the fixes that closed it, and a second one is the run carrying on
  past its own stopping rule.
  **The rounds the floor removes are the rounds that were reading what each
  fix pass created, which is why the second half ships in the same release.**
  Measured across four rounds of #82, three consecutive rounds found their
  finding inside the previous round's fixes, every time in the unit the fix
  added rather than in the fix itself — by construction the fix ships
  reviewed and the unit it added ships unreviewed, in one commit. The bound
  is **a fix pass may add a unit; that unit's fix may not**, stated in
  `skills/code-review/SKILL.md` and `agents/smith.md`, and `round-N.md`'s
  existing `New units` row now carries the depth of each entry —
  `unit (depth 1)`, entries separated by `;`. The depth goes per entry rather
  than in a row of its own because one fix pass can answer a finding in old
  code and a finding inside an earlier unit in the same breath, and one
  number for the round would be false of one of them. **Where a refused unit
  goes is written in the same sections as the rule**, one phase ahead of the
  check that refuses it, so no session meets *this unit may not exist* with
  nowhere to put it.
  **`chain_check.py` reads both rows at the pull request rather than leaving
  them for whoever is awake.** A missing floor row fails; an empty cell, a
  word that is neither answer, and `yes` with nothing after it fail on any
  record; and a `no` followed by two or more later round records fails,
  naming the exit. A `New units` entry with no depth fails, and one at depth
  2 or above fails with the two places the unit goes instead named in the
  message. `none`, with or without a reason, stays an answer to `New units`
  as it was.
  **Older work items are not made red.** Both rules are keyed to the id of
  the work item that wrote them, the way `STRICT_FROM` and `SURFACE_FROM`
  already are: a record whose work item began before the cutoff prints
  instead of failing, because a merged record has no honest repair and a run
  that went past its floor can only be repaired by a round nobody can spawn
  now. A row that is present and malformed is refused at any age, since
  formatting is always the author's.
  **What no check can see, recorded rather than parsed away:** a depth
  declared wrong — `(depth 1)` on a unit that is really second-level. The
  rule is a declaration, and the verifying round reading the `New units`
  surface is what looks at it. `templates/config.md`'s list of what a
  `Record language` row does not govern grows by the new field name, the
  `depth` marker and the floor's `no` and `yes`, so a repository writing its
  records in another language is told which words stay English. (#110, #117)

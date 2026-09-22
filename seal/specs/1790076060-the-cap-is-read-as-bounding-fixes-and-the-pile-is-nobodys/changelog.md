- **The review chain's cap bounds rounds, not fixes, and a filed finding now
  names who will act on it.** Two sentences were repaired where each rule is
  owned; no gate, checker arm, parsed field or verdict word changed.

  **The cap (#492).** Three and five count rounds, and what they decide is
  whether another round is spawned — never what happens to the findings of the
  round they stopped at. A run the round cap stopped may still write a fix, and
  what decides between a fix and a home is **who owns the unit now**: each
  record's `New units` row already names the units its fixes added, so the
  question is answered by reading the run's own records rather than by judging.
  The substitution that was made instead — *when did the defect start* — is
  named as the wrong question, because it sends work the branch owns to a
  tracker nobody schedules from. Measured on a shipped run: five findings were
  filed at a capped exit and all five were the branch's, and the record that
  wrote their fixes reads `round-N` with one verifying round after it.

  **The two capped exits are named apart.** The round cap and the reopening
  bound both end a run `capped` and they permit different things: the round
  cap's terminal record may write fixes and then reads `round-N`, while the
  reopening bound's commissions nothing, because `chain_check.py`'s reopening
  walk refuses a second fix-closing record after a floor `no`. Writing the
  permission into the reopening's own section would have named a state its own
  checker refuses.

  **The filing ladder (#493).** An open finding takes the first home that fits:
  the branch fixes what it owns, a comment goes on the open issue that already
  owns the ground, a new issue is opened only where the finding can name a
  party who will act, and what names nobody stays in the round record and the
  pull request body. Filing ran at 100% while acting on a filing ran at 48% —
  89 issues carried `from-review` on 2026-09-22 and 43 of them were closed —
  which is the pile the ladder is against. The test is the one
  `seal/follow-up.md` already applies to its own rows, and what makes it a
  test is agreement rather than naming: an owner written because there was
  nobody else to write is the fourth rung's answer, not the third's. It is
  read off a column that already exists — the reviewer's `## Deferred` table
  carries `Who answers it`.

  **What the fourth rung costs is stated rather than discovered**: a real
  defect that can name nobody stops being visible in the tracker and lives in
  the round record and the pull request body, which is durable until `settle`
  retires the work item's directory. That is the trade `seal/follow-up.md` made
  for its own file first, and the repository owner is who overturns it.

  Six carriers and one checker docstring became links naming the owner,
  `docs/issues-and-milestones.md` documents the `from-review` label so the
  measurement behind the ladder is one query, and
  `tests/test_the_rules_have_one_owner.py` gains two rules — fourteen now — each
  seen red one mutation at a time.

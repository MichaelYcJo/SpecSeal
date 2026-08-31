# the last round's fixes are reviewed by nobody — questions

<!-- specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should `chain_check.py` fail a pull request whose last round record has `- [x] Pass` checked beside `Fixes checked by: nobody — <why>`? | **Fail it** — a run cannot claim to have passed while its own fixes were opened by nobody, and the way out is always available: spawn one more verifying round, which under the new cap rule costs no round. What it costs is this repository's own release. `specs/1788184145-…/rounds/round-3.md` is in that state, it is merged, and there is no honest repair — writing a `round-4.md` for a review nobody ran fabricates one, and unchecking its `Pass` fails the ready-pull-request rule instead. The release pull request stays red until someone spawns a round for work that has already merged. **Warn** — the state is refused nothing, printed on every CI run, and legible in git forever. Nothing stops a work item shipping with it | Warn. The two claims are not a contradiction inside one file: `Pass` says no finding in this round's table is open, and both are true of `round-3.md`. The refusals that ARE built are the ones git can contradict | ⬜ |
| Q2 | Should `Fixes checked by` be read on every round record the pull request carries, or on the last one only? | **Every record** — a chain where round 1 claims `round-2` checked it while no `round-2.md` exists would be caught. It costs a pass over every record where `check_round` today reads one, and it asserts a property of records written under earlier rules. **The last one only** — where `Pass` is read, and for the reason `docs/review-chain-spec.md` gives for reading `Pass` there: every earlier round's findings need an answer in the round that follows, so every earlier round's fixes are opened by construction. The last round's are the one set with no round after them | The last one only. That is the gap issue #33 measured, and widening the read would fail records nobody was asked about | ⬜ |
| Q3 | A verifying round that opens nothing does not consume the round cap. Is there a bound on how many times that can happen? | **No bound** — a run that keeps finding things in its own fixes keeps going, and the finding rounds still consume the cap, so the loop can only continue while it is actually converging. **A bound** — say two verifying rounds, after which the run ends and the record reads `nobody — <why>` whatever else is true | No bound is stated, because a verifying round that opens nothing is by definition the last one: the run ends at it. A verifying round that opens something IS a finding round and consumes the cap like any other. Nothing here can loop, and the paragraph in `docs/review-chain-spec.md` says so | ⬜ |

**Who answers Q1**: the repository owner. It is the difference between a check
that refuses a claim and a check that refuses a state, and the state in
question is one this repository's own history is in.

**Who answers Q2**: the repository owner. Widening the read is a decision
about records other work items already merged, which is not a call a session
should make on its own.

**Who answers Q3**: the repository owner. The default is an argument rather
than a measurement — no run has yet been through a verifying round, so
whether one can be spawned repeatedly in practice is unknown until one is.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.

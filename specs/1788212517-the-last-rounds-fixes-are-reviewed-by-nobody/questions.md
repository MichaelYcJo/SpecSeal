# the last round's fixes are reviewed by nobody — questions

<!-- specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should `chain_check.py` fail a pull request whose last round record has `- [x] Pass` checked beside `Fixes checked by: nobody — <why>`? | **Fail it, everywhere** — a run cannot claim to have passed while its own fixes were opened by nobody. What it costs is this repository's own release: `specs/1788184145-…/rounds/round-3.md` is in that state, it is merged, and there is no honest repair — writing a `round-4.md` for a review nobody ran fabricates one, and unchecking its `Pass` fails the ready-pull-request rule instead. **Warn** — the state is refused nothing, printed on every CI run, legible in git forever, and nothing stops a work item shipping with it. **Fail it, for work items begun after the rule lands** — the refusal, without the unfixable red: records written before anything asked are excused, and every item begun afterwards has the way out available from its first round | **Answered by the repository owner: the third option.** A check whose first production act is red on merged history nobody can repair is a check people learn to skip, and a check whose strongest statement is a print does not stop a failure mode measured at a 100% hit rate. Grandfathering gets the refusal without the unfixable red. The cutoff is `chain_check.py`'s `STRICT_FROM`, compared against the unix second in the work item's own directory name; the policy clause is in `docs/review-chain-spec.md` under the field's refusal table | ✅ |
| Q2 | The field is read on every round record, where `Pass` is read on the last one alone. Is that the right scope? | **Every record**, which is what was built. It is the only scope under which `round-N` is reachable at all: a checker has to be a LATER round and the last record has none, so reading the last record alone leaves the vocabulary with one dead value out of three. What it costs a repository updating the plugin is every record in a touched work item rather than the newest — and *touched* is the word doing the work: editing one line of a work item's `routing.md` puts that declaration in the diff, and then every historical record in the item is read, including records that merged long ago and cannot be rewritten without rewriting history. **The last one only** — cheaper to migrate, and the gap issue #33 measured is at the last record. It ships a value nothing can ever use | Every record. The last-record-only version was built first and the dead value was found by mutating the sibling lookup and watching the case meant to cover it stay green. The merged-record cost above was measured in round 1 of this work item's own review and is not priced against anything: no repository has yet met it | ⬜ |
| Q3 | A verifying round that opens nothing does not consume the round cap. Is there a bound on how many times that can happen? | **No bound** — a run that keeps finding things in its own fixes keeps going, and the finding rounds still consume the cap, so the loop can only continue while it is actually converging. **A bound** — say two verifying rounds, after which the run ends and the record reads `nobody — <why>` whatever else is true | No bound is stated, because a verifying round that opens nothing is by definition the last one: the run ends at it. A verifying round that opens something IS a finding round and consumes the cap like any other. Nothing here can loop, and the paragraph in `docs/review-chain-spec.md` says so | ⬜ |

**Q1 was answered on 2026-09-01 by the repository owner**, during round 1 of
this work item's own review, and the answer was a third option neither the
question nor the review had put on the table. It is built, and the two things
it turns on are worth keeping visible: the refusal reads the `Pass` box on the
last record alone, and the cutoff reads a number that is already in every work
item's directory name, so no repository has anything to configure.

**Who answers Q2**: the repository owner. The scope decides what a repository
updating the plugin has to migrate, and this one migrated three records rather
than one on its own judgment. The merged-record cost is the part that was not
priced when the row was written.

**Who answers Q3**: the repository owner. The default is an argument rather
than a measurement — no run has yet been through a verifying round, so
whether one can be spawned repeatedly in practice is unknown until one is.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.

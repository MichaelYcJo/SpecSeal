# Survivors — every rule CLAUDE.md restates has one home

The build's `survivor-check --range edee5ca2..HEAD` reported seven places,
taken after `release/v0.18.1` was merged in so the range is this branch's own
change. This work removed `CLAUDE.md`'s copies of four rules and kept each
rule in its home, so a home carrying the removed wording is the result the
work asked for rather than a copy it left behind. Six of the seven are those
homes. The seventh is an application `phases/phase-1.md` kept on purpose.

| Path | Quote | Grounds |
|---|---|---|
| `skills/implement/SKILL.md` | That window has a price wherever this plugin is installed: the guard asks whether the changes should ride along to the other branch | the commit cadence's home, step 2; `CLAUDE.md`'s copy of the worktree-guard paragraph was removed and its row links here (spec Scope 3) |
| `skills/implement/SKILL.md` | A review round records the commit it read, so work still sitting in the working tree is not visible to the reviewer at all | the commit cadence's home, step 2, for the same reason |
| `skills/implement/SKILL.md` | feature branches **squash** into their base, so every commit the branch wrote stops existing at the merge | step 2's first condition; `CLAUDE.md`'s row now says it holds in this repository rather than restating it (spec D3) |
| `docs/branch-and-release.md` | A squash discards every commit the release branch wrote, and anything naming one of them by SHA stops resolving. | the merge method's home; the removed `CLAUDE.md` copy of this reason was the one that had gone false about rider stamps (spec D1) |
| `docs/branch-and-release.md` | `tests/test_a_rider_reaches_its_file.py` went red for exactly that, and the patch release after it exists to fix one line. | the merge method's home, the incident the removed copy retold (spec Scope 1) |
| `docs/branch-and-release.md` | Both rulesets also require a pull request, so neither branch takes a direct push, and there are no bypass actors | the merge method's home, the ruleset paragraph the removed copy retold (spec Scope 1) |
| `CONTRIBUTING.md` | `skills/implement/SKILL.md` §1 holds the reasoning the budget is drawn against: the cost of a question is not its difficulty, it is when it arrives. | an application in §*What a change to a gate must carry*, which links §1 and quotes one clause as the ground for its prompt budget; spec D1 does not list it, and `phases/phase-1.md` keeps it and chooses the batch needles around it |

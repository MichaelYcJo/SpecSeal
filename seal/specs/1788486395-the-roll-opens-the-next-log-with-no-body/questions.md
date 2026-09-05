# the roll opens the next log with no body — questions for the planner

<!-- seal/specs/1788486395-the-roll-opens-the-next-log-with-no-body/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | How does a repository declare its durable measurement log, given that `skills/verify/SKILL.md` ships to repositories with no #51? | **A second label** — an issue carrying `flow-baseline` is that repository's durable ledger. The lookup stays one `gh issue list --label` call, it reuses the mechanism `flow-measurement` already uses, and its invariant can be written in the same shape. **A row in `seal/config.md`** — `Measurement ledger \| #51`, beside `Record language`. Matches where a repository already keeps its settings and is version-controlled, but pins an issue number into a file and makes the lookup two steps, a file read and then a `gh` call. **A milestone-name convention** — an issue in a `log:` milestone is the durable log. Reuses the three kinds settled on 2026-09-04, but milestone names are free text a repository renames at will, which is thin for a plugin to depend on | the second label | ✅ answered 2026-09-04 — **a second label** |

The answer was given in the batch collected before the first edit, alongside
the routing rows.

Nothing else is open. What a measurement has to *say* before it is worth
keeping is #137 and has its own release; the tracker's conventions are
`docs/issues-and-milestones.md`'s as of PR #140.

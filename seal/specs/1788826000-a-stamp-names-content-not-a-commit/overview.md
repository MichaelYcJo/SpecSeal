# 1788826000-a-stamp-names-content-not-a-commit — overview

## Why this exists and what it changes

A `# RIDER:` comment stamped the commit it was verified at, this repository
squashes feature branches into their release branches, and the squash destroys
exactly the commits a fix pass has to name — so the check failed on the release
branch, where whoever met it was never whoever caused it, with no mistake
required anywhere. A stamp now names the content it was verified against, the
way a ledger row has since the same failure was cited as grounds for that
design, and the check makes no git call at all.

## Where spec and implementation diverged

**`plan.md` phase 5 was not a vertical slice and could not be run as one.**
The plan listed *widen the corpus* as its own phase. Widening `RIDER_ROOTS` is
safe only because of the comment-head requirement built in phase 2 — without
it every file that describes the convention becomes a corpus member — so the
constant shipped with the machinery and the twentieth rider's stamp shipped
with the rest of the corpus. The obligation was met; the numbering was wrong.
`phases/phase-5.md` records it, and the plan's Status cell says which commits
delivered it.

**The handoff's corpus count was false and the spec says so rather than
following it.** It gave 13 stamps across 10 files, its own file list summed to
15, and the tree holds 19 real riders across 14 files plus one quoted inside a
round record. Everything downstream is built on the re-derived number.

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — contract §2 reserves the broad gate for one run after the rounds settle. What ran here is narrow: 348 cases across the touched files and the guards beside them, plus `bin/evidence-check` twice |
| whether a drifted rider is answered often enough to be worth its noise, in practice rather than in argument | the repository owner, at the next release that edits a rider-carrying unit. `seal/follow-up.md` already states the trade as overturnable, and this change does not weaken that |
| `templates/evidence-check.yml`'s rider is now half spent — its quoted phrase *"let drift warn without blocking"* no longer exists in the file, and the step comment it points at has been corrected, while the header half it names still stands. The rider was re-anchored to the standing half and its prose left alone | the repository owner. Trimming a deferral's text is a judgment about somebody else's finding, not this work item's |
| a rider written as a TRAILING comment — `value = 1  # RIDER: …` — is read by nothing and says nothing about it, because a block opens only at the head of a comment line. Executed in round 1's fix pass: a grep of the six roots finds 31 marker lines against the reader's 20 riders, and all 11 extras are prose or string literals, so the tree does not stand in this today. Closing it means a rule that compares the grep corpus with the reader's, which is mechanism a fix pass may not add | the repository owner. `skills/code-review/SKILL.md` §*A fix pass adds the unit that pins it* is why it is written here rather than built |
| the records arm of `bin/evidence-check` refuses eight names in `rounds/round-1.md` and `rounds/round-1-report.md` and exits 2. Executed against a `git archive` of `7ff1e63`, before any fix-pass edit: the same eight, so it predates this pass. The remedy the checker names is `NAME NOT IN TREE` on each line | the orchestrator, who owns the round records — `hooks/review-history-guard.py` is why a fix pass does not edit them |
| the quoted rider stamp inside `seal/specs/1788184145-…/rounds/round-2.md` still reads `Verified 2026-08-31 at f1cd65d`. It is a record of what a round observed, so the `Target SHA` argument exempts it — and it is one of TWO places the old string survives a `grep`, with `seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96` (corrected in round 1's fix pass, finding 7) | the repository owner (`questions.md` C1) |

## Fed back into the spec

| Clause | Where it landed |
|---|---|
| a rider stamp names `Verified <date> against <anchor>@<hash>`, and a drifted rider is the rider firing rather than a chore | `seal/follow-up.md`, the convention's own statement — *inferred during implementation*, and the paragraph it replaces was written when the old form was the only one |
| `Target SHA` is exempt, and the three grounds for it | `templates/sdd-round.md` — *inferred during implementation*. It is written where the question recurs, because 135 records carry the row and the next person to count them would otherwise re-open it |
| what still requires `fetch-depth: 0` in a pytest job, now that neither a ledger row nor a rider stamp names a commit | `tests/test_ci_gives_the_checks_what_they_need.py`'s failure message — *inferred during implementation*, and the previous text was made false by this change rather than being wrong when it was written |

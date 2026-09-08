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
| a rider written as a TRAILING comment is read by nothing and says nothing about it, because a block opens only at the head of a comment line. **Both forms**: `value = 1  # RIDER: …` in a `#` file, and `some text &lt;!-- RIDER: … --&gt;` in a markdown one. Executed in round 1's fix pass for the first and in round 2 for the second — each gives `0 ok · 0 drifted · 0 broken`, equally silent. Executed: a grep of the six roots finds 33 marker lines against the reader's 20 riders at `2f0dd02` and 36 at `677e10f`, so 13 extras and then 16, all prose or string literals, and the tree does not stand in either form today. The count names the commit it was taken at because an aggregate is not a coordinate. Closing it means a rule that compares the grep corpus with the reader's, which is mechanism a fix pass may not add | the repository owner. `skills/code-review/SKILL.md` §*A fix pass adds the unit that pins it* is why it is written here rather than built. Round 2's findings 12 and 13 are why the count and the second form are stated: the owner was being handed a stale number and half the shape |
| ✅ the records arm of `bin/evidence-check` refuses eight names in `rounds/round-1.md` and `rounds/round-1-report.md` and exits 2 | answered at `2f0dd02`, which wrote `NAME NOT IN TREE` on each line — three in the record and six in the report. Executed 2026-09-08 in round 2's fix pass: the records arm reads `3 work items read · 42 unread · 427 names read · 0 drifted`, and the eight are gone (round 2, finding 15) |
| the records arm refuses ONE name now, and it is the same class one file over: `rounds/round-2-report.md:216` reads `evidence_check.py#unread_items` as a coordinate, and no `evidence_check.py` sits at the repository root, so the arm exits 2 and the broad gate cannot pass. Executed at `d069d54`, before this pass touched anything: the same one refusal, so it arrived with the report. The remedy the checker names is `NAME NOT IN TREE` on that line, or the full `skills/evidence-check/scripts/` path | the orchestrator, who owns the round records — `hooks/review-history-guard.py` is why a fix pass does not edit them, and it is why the previous row was handed over the same way |
| the quoted rider stamp inside `seal/specs/1788184145-…/rounds/round-2.md` still reads `Verified 2026-08-31 at f1cd65d`. It is a record of what a round observed, so the `Target SHA` argument exempts it — and it is one of TWO places the old string survives a `grep`, with `seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96` (corrected in round 1's fix pass, finding 7) | the repository owner (`questions.md` C1) |

## Fed back into the spec

| Clause | Where it landed |
|---|---|
| a rider stamp names `Verified <date> against <anchor>@<hash>`, and a drifted rider is the rider firing rather than a chore | `seal/follow-up.md`, the convention's own statement — *inferred during implementation*, and the paragraph it replaces was written when the old form was the only one |
| `Target SHA` is exempt, and the three grounds for it | `templates/sdd-round.md` — *inferred during implementation*. It is written where the question recurs, because 135 records carry the row and the next person to count them would otherwise re-open it |
| what still requires `fetch-depth: 0` in a pytest job, now that neither a ledger row nor a rider stamp names a commit | `tests/test_ci_gives_the_checks_what_they_need.py`'s failure message — *inferred during implementation*, and the previous text was made false by this change rather than being wrong when it was written |

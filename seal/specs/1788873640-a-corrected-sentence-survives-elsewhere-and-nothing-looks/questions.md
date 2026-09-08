# Questions — a corrected sentence survives elsewhere and nothing looks

<!-- Decisions only a person can make. The routing batch was answered before
the first edit; every row below arose after it and none of them blocked the
work, which is why each is written here rather than raised. -->

## Answered before the first edit

Routing, all three axes in one batch, by the repository owner on 2026-09-08:
**smith · straight to the PR · open the pull request**. Recorded in
`routing.md`.

## Open

| # | Question | Who must answer |
|---|---|---|
| Q1 | **#180's second rule has a home and this work does not take it.** *A handoff must not assert a ledger count taken from the scoped read* — measured four times in one run, handed to four phases and wrong every time. `docs/review-handoff-protocol.md` states it in prose and the checker that would hold it only warns today. Two candidate homes are named in #180 itself: a fifth handoff requirement beside the four that exist, or `evidence_check.py` refusing `--ledger` on a read rather than warning. Which, and is the refusal safe for the writer's use the flag exists for? | the repository owner |
| Q2 | **Does the CI step fail the pull request, or report on it?** This work's phase 3 measures the noise over real ranges and takes the answer the measurement supports, recording it in `phases/phase-3.md`. The question stays open because the measurement covers this repository's corpus only, and #229 is the evidence that the class arrives from repositories with different corpora — a documentation set of fifteen files, where every sentence has more neighbours than here. The step can be moved either way in one edit | the repository owner |
| Q3 | **`survivors.md` has no template and no checker.** A ledger row's shape is checked by `evidence_check.py`; a `survivors.md` row's shape is checked only by the script that reads it, so a row nobody's check reads can be malformed and silently exempt nothing — which is the direction `seal/follow-up.md`'s first open row says a checker of claims must not fail in. The judgment is whether that is worth a template and a case in this work item or a row of its own | the repository owner |

## Assumed in writing, because a different answer would not change what was built

- **The corpus is the tree at the range's tip, not the working directory.** A
  survivor sitting in an uncommitted edit is invisible; so is a reviewer, by
  the same rule (`CLAUDE.md` — *anything still uncommitted is invisible to the
  reviewer*), so the check sees exactly what the next round will see.
- **The range is given, never guessed.** `round_record.py close` already takes
  `--range A..B` from the smith, so the range this check reads is the one the
  chain already produces. Deriving it would be a second derivation of a fact
  that already has one.
- **One language.** Normalisation keeps `[a-z0-9]` runs, so a corpus in a
  language that is not space-separated scores near zero rather than wrongly.
  That is a loss of an alarm, not an invented one, and no repository running
  this plugin has such a corpus today.

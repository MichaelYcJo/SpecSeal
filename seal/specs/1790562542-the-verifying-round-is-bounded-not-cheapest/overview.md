# 1790562542-the-verifying-round-is-bounded-not-cheapest — overview

📋 implement applied
· spec:     this work item's spec.md, plan.md, questions.md and routing.md; `docs/review-chain-spec.md` §*The last round verifies*; `docs/review-handoff-protocol.md` §*After the run — the per-segment bars*; `skills/code-review/orchestration.md` §*Orchestrator: the run ends with a verifying round*; `agents/warden.md` §*Role*; CLAUDE.md's fragment rule
· evidence: `seal/ledger/1790562542-the-verifying-round-is-bounded-not-cheapest.md` (new, rows V1 and V2). Eleven existing rows were re-read and re-stamped where they live, in `seal/ledger.md` and nine `seal/releases/*.md` files (`phases/phase-2.md`)
· verified: executed are the narrow modules, 25 red-first mutations, lint on the changed test files, and `evidence-check` before and after. Read are #639's and #89's figures, from their issues

## Why this work exists

Four places told sessions the verifying round is cheap because its target is
a diff, and the measurements say it costs about a finding round. They now say
the diff bounds the round and does not make it cheap, and a related false
"cheapest" claim about #81's round 1 is corrected alongside.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| #81's "cheapest round on record" | spec *Out* and plan A7 route it to the orchestrating session and leave it, and S9 says "none of them changed". The build corrected `skills/code-review/SKILL.md`, `templates/sdd-round.md` and `tests/test_a_segments_record_says_what_it_was_asked.py` | the build | The orchestrating session is the answerer spec *Out* names, and its spawn prompt says: "If it is false or unsupported, correct it in this branch in phase 1 alongside C1–C5, with its pin updated and seen red first." It was false when written (`phases/phase-1.md`). S9 no longer holds as written. The released `CHANGELOG.md` 0.7.0 entry is untouched, as both the spec and the prompt require |
| Where the #81 pins live | the plan names one new module, for C1–C4 | the #81 gone/stands pair went into `tests/test_a_segments_record_says_what_it_was_asked.py` | That module already owns #81's story and its probe was the pin to move. Keeping the new module to one claim follows plan A6's reasoning (constants organised by what they correct) |
| An extra case on the verifying bar | spec *In* 2 lists what the Grounds cell must not say, and the plan pins only a stands/gone pair | `test_the_verifying_bar_is_grounded_on_neither_cost_nor_size` added | *In* 2's "no cheapest, no small, no by design" is otherwise only a reading. The pair pins two phrases, and this case pins the cell |

## Not verified

| Item | Who must answer |
|---|---|
| #639's figure (median 0.83 × round 1 over 29 verifying rounds of 0.14.0–0.15.5, range 0.26–1.27, five at or above round 1), which `docs/review-chain-spec.md` now prints (`questions.md` Q1) | a measurement: the author of #639, over the metered blocks of #496, #535, #577, #601 and #619 |
| #89's comparison "#82's six rounds averaged three times the calls for fewer", which the #81 carriers now quote. It was read from #89's comment of 2026-09-03T02:26Z and not re-derived from #82's rows | a measurement: #82's six round readings in #89 |
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

Whether `verifying: exempt` is still the right bar is left alone. It is in
spec *Out* with its answerer, and this build changed only its grounds.

## Fed back into the spec

none

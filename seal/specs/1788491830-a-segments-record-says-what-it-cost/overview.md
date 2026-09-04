# 1788491830-a-segments-record-says-what-it-cost — overview

📋 implement applied
· spec:     `seal/specs/1788491830-…/{plan,spec,questions,routing}.md`; `docs/review-handoff-protocol.md` §Files; `docs/flow.md`; `CLAUDE.md` §*The goal a design is chosen against*, §*a change writes fragments*; `skills/agent-contract/SKILL.md` §§1–3, 6, 9, 10, 12, 15; `skills/implement/SKILL.md` §§1–4; `~/.claude/skills/commit-pr-convention/SKILL.md`; `~/.claude/skills/writing-style/SKILL.md`
· evidence: `seal/ledger/1788491830-a-segments-record-says-what-it-cost.md` — R1, R2, R3, six anchors, all `ok` under `--strict`
· verified: **executed** — `tests/test_a_record_says_what_ran_it.py` (45 cases), the four suites reading the changed templates and documents, and the eleven suites that touch `chain_check.py` (330 cases); twelve code mutations and eight prose mutations, no survivors after two fixes. **Read, not executed** — the full suite, the repository-wide lint and the typecheck, which are the orchestrator's single broad run

## Why this work exists

Every segment of two work items was metered this week and posted to the flow
log, and not one of those readings says what produced it — so the log knows
what a segment cost and cannot say whether the cost was the model's, the
agent's, or the scope's. This makes the missing half durable, and #145's
acceptance band and #84's *time per agent* both stop being unanswerable.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which skill states whose row it is | `plan.md` phase 3 names `skills/verify/SKILL.md` alone | Both that and `skills/code-review/SKILL.md` | `skills/code-review/SKILL.md:167` enumerates every mandatory row of `round-N.md` in one cell, and an orchestrator writing a round record reads that list and nothing else. Leaving the row out of it ships a skill whose own output phase 2's checker refuses — the failure `plan.md`'s own phase ordering exists to prevent, arriving from the other direction |
| Opening the outcome-column ticket | `plan.md` phase 4: "a row for the outcome-column ticket this work opens" | The row is written; the issue is **not** opened | `skills/agent-contract/SKILL.md` §6 — an implementing agent posts nothing and opens no pull request, and an issue is a durable record outside the repository. The row names the gap and says the number goes in when it is opened; the drafted body is in the handback |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — §2's single broad run, after the rounds settle |
| the outcome-column issue is opened and its number replaces the placeholder in `docs/flow.md`'s 0.9.0 section | the orchestrator |
| `chain_check.py` running under CI against a real pull request that carries this branch's own round records | the hygiene workflow at the pull request |

## Not done

**The outcome column.** Answered as Q1 before the first edit: this work item
builds the record row and not the column beside it. Five candidate signals and
no evidence which survive contact, and #137's own body refuses to pick a
format early. Its row is in `docs/flow.md` under 0.9.0, without a number.

**No acceptance band for any segment kind.** That needs #145's boundary first,
and deciding a budget before the evidence exists is what #110's *Not this*
refuses.

**`docs/review-chain-spec.md` was not touched.** It owns the cap and the
floor, and `Ran by` is neither — it makes no claim about when a run stops. The
row is stated in the two documents a record author actually reads.

**A half-known runner has no spelling of its own.** `unknown on Opus` is
accepted, as an unknown with a reason rather than as a half-named pair, and
that limit is recorded in `runner_problem`'s docstring and in ledger row R1
rather than parsed away.

## Fed back into the spec

None. `spec.md` fixed that the row names two things and left the spelling to
the plan; the plan left it to implementation. The spelling settled — `agent on
model`, with the joining word chosen so a code span cannot split the cell — is
recorded in the templates, the protocol and ledger rows R1 and R2, not added
to `spec.md` as a clause.

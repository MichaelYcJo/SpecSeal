# 1788501054-a-check-reports-clean-while-something-is-missing — phase 10

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-10.md
— what this phase of the build did, written by the session that ran it when
the phase closed. Not in `plan.md`'s original four: round 7's fixes are work
the plan did not contain, and the phase row was added beside them, the way
phases 6 through 9 were. -->

| Field | Value |
|---|---|
| Phase | 10 |
| Commit | 9efd314 |
| Ran by | orchestrator on fable-5.1 — no smith was spawned. The repository owner's instruction for round 7 was that the orchestrator writes the fixes itself, and the model is the one the session was switched to mid-run, which the session knows because it was told |

## What this phase was asked

Round 7's four findings, with the standing instruction that the orchestrator
carries them out rather than a smith:

- **🔴 1** — the run had no terminal record `chain_check.py` accepts. The
  floor's walk read `Needs a fix`, the reviewer's answer to *what did I open*;
  round 6 answered `no`, the orchestrator fixed both its 🟡 anyway and marked
  them `**fixed**`, and every exit was then refused — a `round-7.md` was a
  second uncounted record after the floor, `no fixes to check` was refused
  beside a `fixed` verdict, and `nobody` was refused beside a ticked `Pass`.
- **🟡 2, 🟡 3** — three cells of `round-5.md` and one of `round-6.md` still
  carrying *not yet written* a round after their fixes were read.
- **🟡 4** — the fragment header's second paragraph naming R6 among the six it
  says were not found by reading, with R4 missing.

`CONTRIBUTING.md` §*What a change to a gate must carry* governs the first,
and `agent-contract` §15 governs the case that pins it.

## What this phase found

**The record already carried the missing fact, and only one reader looked at
it.** `closed_with_a_fix` returns True for `round-6.md` — that is what refuses
`no fixes to check` beside a `fixed` verdict — and the floor's walk, three
functions down, never called it. `wrote_fixes` wraps that predicate and the
walk stops at it as well as at a reopening. No second source of truth was
added; the verdict column was already the source, and the bound now reads it.

**The direction is ALLOW, stated rather than absorbed.** The walk stops one
record earlier in one sequence, so a run that used to be refused is accepted.
`plan.md` declares *blocks more* for this branch and this is the second
place it does not hold — the pending arm's `allow` for a reason the checker
cannot read was the first. It is the cheaper mistake for the same shape of
reason: the alternative was a checker satisfiable only by rewriting `fixed`
to `answered` over fixes that exist, which is a false record, and a false
record is the subject of this work item. What the wider walk cannot let
through is a run of quiet rounds: `answered` writes nothing, so
`test_three_quiet_rounds_after_the_floor_are_still_refused` is red under the
new walk exactly as under the old, executed.

**Seen red twice, once for free.** The planted case fails against the old
walk with the floor's own sentence — *2 round records follow this one with
none of them saying the run reopened*. And this repository's own records fail
the same way the moment `round-7.md` exists, in
`test_this_repositorys_own_round_records_pass_the_per_record_checks`, which
went red at `9bf9584` and green at `9efd314` with nothing but the walk
changed between them. The second red cost nothing and is the stronger of the
two, because the fixture did not have to be believed.

**The fixture had to be built by hand, and the reason is the ordering rule.**
`record()` hard-codes `answered` and `no fixes to check`, so a record whose
verdict says `fixed` needed its own builder — and it could not be written in
one commit. A record that names a fix commit in its verdicts must be ADDED
before that commit exists, so the case commits the record open, commits the
fix, then commits the record filled. That is three commits where every other
floor case uses one, and it is the exact sequence `round-6.md` went through
at `c73c56f`, `0d4a31f` and `d1bf521`.

**The three 🟡 are one class and it is the orchestrator's.** Round 4's 🔴 was
a cell the orchestrator filled, round 6's two were clauses the orchestrator
left, and round 7's three are reach-backs the orchestrator forgot. Every one
sits in a record the session that wrote the prompt also wrote. The pending arm
was built to catch the forgotten reach-back and cannot, because it keys on
`Fixes checked by` and that is one of the cells left stale — `questions.md`
Q4 holds that limit and it is unchanged by this phase.

**The prompt budget is zero.** Nothing here puts a question in front of a
person: the walk reads a cell that was already required, and a record that
does not carry it is already refused by `open_blocking`.

**Platform honesty.** `wrote_fixes` reads a file `read_record` already opens
and calls a predicate already called on every record; there is no OS boundary
in it, and the case runs `git` through the same `subprocess` helpers every
other case in the file uses. Nothing platform-specific was added, and nothing
platform-specific was tested.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The sentence *the count stops at the first later record whose `Needs a fix` says the run reopened* as the WHOLE of the rule, in `docs/review-chain-spec.md`, `templates/sdd-round.md` and `skills/code-review/SKILL.md` | The same three files, each now carrying the second stop beside the first. The old sentence stays true and is not removed; what is removed is its claim to be the only condition |
| `nobody — this round's fixes are not yet written` from `round-5.md` and `round-6.md`, and `none — the fixes are not yet written` from `round-5.md`'s two surface rows | `round-6` and `round-7` in the checker cells, `none` in both surfaces — the reach-back those records were owed a round ago |

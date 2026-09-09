# 1788908215-the-orchestrator-is-measured-by-the-whole-session — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | fec6e83, corrected at 2dbcdb2 |
| Ran by | `specseal:smith on claude-opus-5` — filled by the spawning session, which is the only participant that knows what it spawned |

## What this phase was asked

`skills/verify/SKILL.md`'s instruction beside the resumed-agent one; the
changelog and ledger fragments. Verified by the suite and `evidence-check`
on the fragment.

The spawn prompt fixed where the fragments go — `seal/specs/<id>/changelog.md`
and `seal/ledger/<id>.md`, never `CHANGELOG.md` or `seal/ledger.md` —
and named `CLAUDE.md` as the authority overriding the `implement` skill on
that point.

## What this phase found

**The word `cycle` was already taken.** `docs/review-chain-spec.md` owns
it for the mark's own unit, and `tests/test_one_word_one_meaning.py` exists
to keep one word to one meaning. The paragraph says **spawn cycle** and says
once that it is not the review chain's cycle. Nothing caught this — the case
pins the review-chain half, not a new collision — so it was a read of the
constraint rather than a red run.

**The shipped skill may not name this repository's tracker state, and the
first draft did.** It cited #51, and
`test_the_shipped_skill_names_no_repository_specific_tracker_state` turned
red: an installed repository has no such issue and cannot act on a number.
The sentence now makes the same point without one.

**`--reverify` is the second half of re-verifying, not the whole of it.**
Running it rewrote nine `seal/ledger.md` rows whose units this branch moved.
Eight of the nine claims still held on reading. One did not: R1 counts the
sites where a `datetime` out of `parse_time` is subtracted or ordered —
eight, six subtractions and two orderings — and this branch adds four
orderings (`spawn_cuts`' sort key, its `min`, its running `max`, and
`in_windows`' `bisect_right`). Corrected to twelve, counted off the
module's own syntax tree; the walk's thirteenth hit is `slowest`'s
`sorted`, which orders on a float, and it was read rather than trusted.
`CLAUDE.md` permits touching the shared file for exactly this — leaving the
ledger true — and forbids appending to it.

**`survivor-check` reported ten places carrying wording this branch
removed, and every one is deliberate.** Eight are `spec.md`, `plan.md` and
`questions.md`, the approved contract: editing the premise out of them would
delete the evidence that the gate approved it, which is what `overview.md`'s
divergence section and `questions.md` Q4 exist to carry. Two are a shipped
`CHANGELOG.md` entry and the fragment it came from, stating what was true at
the release that shipped it — a present-tense ledger row is corrected, a
released record is not. All ten are in `survivors.md` with a quote and
grounds, so each exemption stops applying the moment its text changes.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md` R1's claim that the `parse_time` funnel closes eight sites | The same row, corrected in place to twelve with the derivation and the false thirteenth named. The two released statements of the old count stay as history, exempted in `survivors.md` |

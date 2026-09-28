# 1790562542-the-verifying-round-is-bounded-not-cheapest — review round 1

| Field | Value |
|---|---|
| Target SHA | 5a66666d639677c8e69aeee24764defadf27b323 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #648 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the #81 correction quotes an unsupported #82 comparison, and its pin requires it) and 🟡 2 (`agents/warden.md:110-112` still grounds scoping on price) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790562542 (#639, with #636 done outside the tree), a first round against the whole branch `docs/639-the-verifying-round-is-bounded-not-cheapest` at 5a66666d, base origin/release/v0.15.7 (1fa25931), draft PR #648. Judge spec compliance against the work item's spec.md first (carriers C1–C6, and the #81 correction the orchestrator added to the build, recorded in overview.md as a divergence from spec *Out*/S9/A7), then quality. The class to enumerate: every sentence in agents/, skills/, docs/, templates/, both READMEs and test needles or docstrings that claims a cost or cheapness for a verifying round or names a round the cheapest, by meaning, not by phrase. Open the measured basis the new sentences cite (#639's median, #456, #89's #81 comment, #51's baseline) enough to judge whether each new sentence says only what was measured. Check that the ledger re-stamps (11 rows) left no claim false.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The #81 correction states "#82's six rounds averaged three times the calls for fewer", and #89's own per-round readings for #82 (35, 38, 36, 29, ?, 30 calls) average about 1.2 × 29. The stands pin now requires the unsupported comparison | `skills/code-review/SKILL.md:231` | open | Read from #89's comments through `gh`. Deleting the comparison turned `test_81s_round_one_is_described_by_its_yield` red (executed). The same wording is at `templates/sdd-round.md:299` and in the module docstring |
| 🟡 2 | The paragraph above C4 still grounds keeping a re-check round scoped on price ("turns every returned finding into the price of a first round"), which #456 and #639's data contradict, and it disagrees with C4's "the round's job, not its price" | `agents/warden.md:111` | open | Read. It is outside the tree-wide pin because it does not use the phrase. The spec's "upper bound" ground does not hold, because the sentence names widening as the cause of a price that scoped rounds already pay |
| ⬜ 3 | The chain spec's median has no unit. The source says span | `docs/review-chain-spec.md:220` | open | Read #639 and #51. Both say "round 1's span" |
| ⬜ 4 | 🟡 1's comparison is also in the changelog fragment, in ledger row V2's claim and anchor, and in phase 1's record (correction) | `seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/changelog.md:28` | open | Paperwork under `seal/`, so not counted in `Needs a fix`. It follows 🟡 1's wording |
| 🟢 | C1–C6 match spec *In* 1–6, and the #81 divergence is recorded in `overview.md` with its grounds | `skills/code-review/orchestration.md:132` | confirmed | Read against spec.md. Executed: the four touched modules pass, and restoring the old protocol Grounds cell turned all four new cases red |
| 🟢 | The eleven re-stamped ledger rows left no claim false | `seal/releases/0.4.0.md:114` | confirmed | Read word by word against the edits. `evidence_check.py .` exits 0 (executed) |
| 🟢 | The "not the cheapest when written" half of the #81 correction is true | `tests/test_a_segments_record_says_what_it_was_asked.py:8` | confirmed | Read #89's timestamps (#79's round 2 at 5.6 m and 28 calls, and round 3 at 4.6 m and 22 calls, both before 2026-09-03T02:26Z) and #51's first revision (#29 at 4.2 m and 10 calls) |
| ❓ | Whether #639's median 0.83, its range 0.26–1.27 and the five at or above round 1 reproduce | `docs/review-chain-spec.md:219` | ❓ out of verified scope | Count of 29 reproduced (executed). The ratios need the metered blocks, which this round did not read. It is answered by a measurement from #639's author (questions.md Q1) |

## Paste-ready fixes

```
something still to verify. #81's round 1 is the
measured reason — five defects, one 🔴 and four 🟡, in 29 tool calls,
because its prompt named eight specific things to try to break, and that
fact today survives only in a transcript.
```
```
#81: round 1 of that work item found five defects in 7.6 minutes and
29 tool calls — one 🔴 and four 🟡 — because its spawn prompt named eight
specific things to try to break, in order.
```
```
"""Neither a round record nor a build phase said what it was ASKED to do,
only what it found. #81 is the measured cost on the review side: round 1 of
the work item it names found five defects in 7.6 minutes and 29 tool calls —
one 🔴 and four 🟡 — because its spawn prompt named eight specific things to
try to break, in order. That fact survives today only in a transcript.
```
```
calls, and #51's baseline #29's at 4.2 minutes and 10. What #89 measured for
it is five defects in 29 calls, so that is what the carriers say and what the
gone/stands pairs at the foot of this module hold (#639).
```
```python
CHEAPEST_81_CARRIERS = (
    (
        REVIEW_SKILL,
        "five defects, one 🔴 and four 🟡, in 29 tool calls",
        ("the cheapest round on record", "averaged three times the calls"),
    ),
    (
        ROUND_TEMPLATE,
        "found five defects in 7.6 minutes and 29 tool calls",
        ("was the cheapest round measured", "averaged three times the calls"),
    ),
)
```
```python
def test_81s_round_one_is_not_called_the_cheapest_again():
    """The absent half, evidence only beside the present half above. #89
    held #79's verifying round at 5.6 minutes and 28 calls before it wrote
    7.6 and 29 up as the cheapest review round in the log, and its own
    readings of #82's rounds do not give three times the calls."""
    for path, _phrase, gones in CHEAPEST_81_CARRIERS:
        for gone in gones:
            assert gone not in flat(path), (
                f"{os.path.relpath(path, ROOT)} carries a retracted claim "
                f"about #81's round 1 again: {gone!r}"
            )
```
```
  A round that exists to check one fix is scoped to that fix. Re-reading the
  whole diff each time re-reviews what earlier rounds already reviewed instead
  of answering the finding that came back, and the answer is what the round
  is for. The exception is a fix that changes what an earlier verdict rested
  on — say so, and widen deliberately.
```
```python
    (
        ("agents", "warden.md"),
        "instead of answering the finding that came back",
        ("turns every returned finding into the price of a first round",),
    ),
```
```
those shrink with the diff. Measured over 0.14.0–0.15.5, 29 verifying rounds
ran at a median of 0.83 × the span of their own work item's round 1, with a
range of
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_verifying_round_is_bounded_not_cheapest.py`, `tests/test_the_last_rounds_fixes_are_checked.py`, `tests/test_a_segments_record_says_what_it_was_asked.py` and `tests/test_the_handoff_before_round_one.py`, in the clone at `5a66666d` | exit 0, 105 passed |
| `evidence_check.py .` in the clone | exit 0 |
| `bin/survivor-check --range 1fa25931..5a66666d` in the clone | exit 0, "no removed wording is still standing" over 454 files and 20 removed sentences |
| Mutation: the protocol's old `verifying` Grounds cell restored, then the new module run | exit 1, 4 failed |
| Mutation: the #82 comparison deleted from `skills/code-review/SKILL.md`, then the #81 module run | exit 1, 1 failed, 10 passed. The stands pin requires the comparison |
| A regex count of later-round warden readings over the bodies and comments of #496, #535, #577, #601 and #619 | 29 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet run. It is the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #51's body, as #636 revised it, says "Surface size, not round kind, and a diff is simply the smaller surface" two paragraphs after "none of those shrink with the diff". That is the retracted claim, and it is outside the tree | #51's body | the orchestrating session, which made #636's revision |

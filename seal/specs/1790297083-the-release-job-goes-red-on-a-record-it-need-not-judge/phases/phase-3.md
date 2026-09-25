# 1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 3e5ac9c8 |
| Ran by | unknown — the spawn prompt named no runner, and the template refuses a value the segment sources from itself; the orchestrator fills this row |

## What this phase was asked

#598 instance 4. `checked_by` takes `strict`, and in a draft the last-record
`Pass`-beside-`nobody` refusal becomes a notice naming the verifying round
and *Ready for review*. Every other refusal in the function is unchanged.
Also the module and function docstrings, `docs/round-record-spec.md`
§*`Fixes checked by`* (sentence, table row, `Enforced by:`),
`docs/review-chain-spec.md` §*Two records*, and the replacement for
`skills/code-review/orchestration.md`'s *"It is red once more …"* sentence
with its pin in `tests/test_the_rules_have_one_owner.py`. Cases C1 to C3,
with C1 red on the pre-phase code and the orchestration pin red with the
new sentence deleted. C4 (`close` still reports it) stays green.

## What this phase found

**The frame does not hold on C4, and the case was changed rather than the
design.** `plan.md` §*Technical context* says *"`round_record.py close` runs
the check with no payload, so it keeps reporting the refusal after ticking
`Pass`"*. `round_record.py#run_check` says otherwise: unless
`pull_request_is_ready` gets `isDraft: false` from `gh`, it writes a
`{"pull_request": {"draft": true}}` payload and points `GITHUB_EVENT_PATH`
at it before calling `chain_check.main`. So `close` runs the check as a
draft on every local run with no ready pull request, which is the window
itself. After this phase that run prints the notice and exits 0, and
`tests/test_the_fixes_close_the_record.py::test_pass_is_ticked_when_nothing_is_open_and_the_gate_is_the_flag`
went red on its `code == 1` line when every reader module ran (2436 passed,
1 failed).

What the case was for still holds. The output at the keyboard still reports
the pair, and it now names the verifying round (*"spawn one verifying round
at the diff of these fixes"*). What changed is the exit code in a draft. No
document says `close` exits 1 for this pair. A `grep` for the claim over
`docs/`, `skills/`, `agents/` and `templates/` found none; only the case and
the frame said it. Keeping exit 1 would need `close` to judge this one pair
strictly while judging `Pass` as a draft, which is a second path through
the check, and adding one was not this phase's to do. So the case now
asserts exit 0 and the notice's text, and its docstring says why. At a ready
pull request, where `gh` says ready, `close` still exits 1. No case builds
that, because it needs `gh` to answer. The rewritten assertion is red on the
pre-phase code, shown by swapping in the kept pre-phase `chain_check.py`.
Recorded in `overview.md` as a divergence.

**The pin was renamed.** `test_the_release_leg_is_red_again_until_the_verifying_rounds_record_commits`
is now `test_the_release_leg_is_not_red_until_the_verifying_rounds_record_commits`,
because the old name asserts what the sentence no longer says. `spec.md`
Scope 4 names it by the old name. Nothing else in the tree does.

**`docs/review-chain-spec.md` §*What a draft is excused, and what it is
not*** carried the same fact as §*Two records*, that a draft does not excuse
a checker the record does not have. It now says that this one pair is
excused and why (contract §12). `plan.md` did not name that section.

**Seen red (§15), executed:**

| Case | Against | Result |
|---|---|---|
| C1 `test_pass_beside_nobody_prints_on_a_draft_and_names_what_re_arms_it` | pre-phase code | red, exit 1 on a draft payload |
| C2 `test_pass_beside_nobody_still_fails_a_ready_pull_request` | pre-phase code | green, which is what it pins. Red under N1 |
| C3 `test_a_draft_is_excused_the_pass_half_and_no_vocabulary_refusal[nobody]` and `[the session that wrote them]` | pre-phase code | green, which is what they pin. Red under N3 |
| the orchestration pin | the new sentence deleted (N4) | red |
| C4, rewritten | pre-phase code | red, exit 1 where 0 is asserted |

**Mutations, one at a time, restored from copies kept outside the tree,
`tests/__pycache__` cleared between them (executed):**

| Mutation | Red |
|---|---|
| N1 the draft arm fires at ready too | C2, `test_pass_beside_nobody_fails_a_work_item_begun_after_the_cutoff` |
| N2 `main` does not pass `strict` to `checked_by` | C1 |
| N3 a draft excuses every refusal in the row | C1, both C3 cases, S11 `test_a_draft_pull_request_is_excused_the_pass_and_not_this`, `test_an_unchecked_pass_beside_nobody_is_not_the_claim` |
| N4 the orchestration sentence deleted | the renamed pin |

**Narrow result, executed:** every module reading `chain_check.py`,
`docs/round-record-spec.md`, `docs/review-chain-spec.md`,
`skills/code-review/orchestration.md` or either edited test module (53):
2436 passed, 8 skipped, 1 failed, the C4 case above. After the case was
rewritten, `tests/test_the_fixes_close_the_record.py`: 103 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *"It is red once more from `close` ticking `Pass` until the verifying round's record commits … and that window is expected."* in `skills/code-review/orchestration.md` | the sentence that replaces it in the same paragraph, and its pin |
| *"The draft excuse does not reach this row"*, in `docs/round-record-spec.md` and `chain_check.py`'s module docstring | the same two places, narrowed to the one pair it now reaches |
| `close` exiting 1 on the pair in a draft, asserted by the C4 case | nowhere: the case now asserts the notice and exit 0, and the ready path is where the refusal lands |

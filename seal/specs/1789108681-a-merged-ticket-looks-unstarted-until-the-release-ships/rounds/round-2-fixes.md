# round 1's fix pass — the table `round_record.py close` applies

Range: `076d691..8ca5569`. One commit of fixes; the round record it answers is
`rounds/round-1.md`.

Findings 9 through 15 take no row: the reviewer closed them, and a row here
would overwrite the reviewer's verdict with mine.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `8ca5569`. `--paginate` added to the milestone read, and `test_the_milestone_list_is_read_past_the_first_page` planted. **The paste-ready fix was not taken whole:** it also added `--jq .[].title`, on the stated grounds that `--paginate` over an array endpoint concatenates arrays into something `json.loads` refuses. Executed on gh 2.92 — `gh api --paginate "…/milestones?state=all&per_page=2"`, seventeen pages, `json.loads` returns one list of **33** — so `--paginate` merges and that premise is false. The flag is not added and the docstring records the measurement, including that a gh old enough to concatenate would make `json.loads` raise, which is loud rather than a short list. Three mutations red: flag dropped, page size lowered below the maximum, and the whole query gutted — the last is the probe round 1 reported surviving |
| 2 | fixed | `8ca5569`, and the range is made true in CI rather than the docstring made weaker. The step passes `HEAD_SHA: ${{ github.event.pull_request.head.sha }}` and `main` measures the range to it, so the fork point survives the merge ref; with no such variable the fallback is `HEAD`, which is a branch tip for a session running it by hand. **Why this over documenting the collapse:** the hotfix sentence at `docs/branch-and-release.md:218` is true and is why the collapse costs nothing *today*, but it makes the guarantee contingent on a fact about hotfixes rather than on the range, and `merge_base`'s docstring would still be describing a protection the job does not have. Two new cases — the named head, and the control that catches the first one lying — plus four mutations red, including threading the head into only one of the two commands. The docstring now carries the whole reading |
| 3 | fixed | `8ca5569`. **Content-addressed rather than positional**, which is a step past the paste-ready text. That text pointed at "the box directly above the one about other sessions in the checkout", which breaks again the moment a box is added; the sentence now names the box by what it asks. **The order was left alone on its own grounds**, against `phases/phase-4.md:58`'s argument for moving it: boxes 1 and 2 confirm what arrived, and a milestone cannot be checked against a release until you know what is in it, so third is the right place and the sentence was the wrong claim. Counted before editing — boxes at `docs/release-checklist.md` lines 14, 18, 40, 50 |
| 4 | fixed | `8ca5569`, in both `overview.md` §*Not verified* and `questions.md` Q3. The answerer is now "the first squash into a release branch whose `merged: X.Y.Z` label does not yet exist — not this one", with the reason: the label was created by hand before the build, so the signal's read finds it and skips the create. **The version is deliberately not named**, where the paste-ready text wrote `release/v0.12.0`: `docs/branch-and-release.md` says whether the next number is a minor or a patch is known at the end and not at the cut, so a named version is a prediction. Both cells also say this branch's squash still answers `--add-label`, which is worth watching for its own sake |
| 5 | fixed | `8ca5569`. Re-derived rather than taken: `test_docs_line_wrap` 23, `test_one_word_one_meaning` 13, `test_release_hygiene` 32, `test_no_real_identifiers` 2, `test_the_rules_have_one_owner` 45, `test_a_question_says_who_can_answer_it` 6 = **121 over six**; `test_a_merged_ticket_says_so_on_the_tracker` 23, `test_a_release_cannot_ship_an_untrue_milestone` 25, `test_ci_gives_the_checks_what_they_need` 2 = **50 over three**. Nine modules, 171 cases, exactly as the round says. The line now reads nine, gives both figures, says it said eight until round 1 counted, and carries the post-fix total of 175 |
| 6 | fixed | `8ca5569`, and the round's own judgment — a note, because losing `REPO` is a loud `KeyError` and losing `BASE` is harmless — was right until finding 2's fix landed. `HEAD_SHA` is the third kind: losing it is **silent**, falling back to `HEAD`, which in CI is the merge ref, which puts finding 2 back with nothing saying so. `test_every_input_the_script_reads_is_handed_to_it_by_the_step` covers all five entries rather than that one, because a reader deleting a line does not first ask which kind it is. Four mutations red, one per entry plus one that points `HEAD_SHA` at the merge ref's own sha |
| 7 | answered | Disclosed at the coordinate rather than changed, at `8ca5569`. The module docstring's definition of D now says a reverted squash stays in it, why — the revert's subject carries the revert pull request's own `(#N)` and its body carries no closing keyword, so nothing subtracts the original claim — and what it would cost: the issue sits in D, out of `M \ D`, and the release ships claiming work it no longer has. The behaviour is unchanged, so this is not `fixed`: no release here has reverted a squash, and subtracting reverts would need a second reader of revert bodies, which is mechanism a fix pass may not add |
| 8 | deferred `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md` §*Not verified* | Left open as the round left it, and given a durable home it did not have. The new row carries the question, the tree's one precedent (`close-issues-on-release.yml` holds `issues: write` with no `pull-requests` scope and its latest run read three pull request bodies), the reasoning that a `GET` needs only the read level of a permission the write level covers, and the direction if it does not hold — every body 404s, D comes out empty, and the gate refuses the release naming the whole milestone with a message that misdirects. Answerer: the repository owner, at the 0.11.1 release pull request, which is also the step's first execution in CI of any kind |

## What was run over the fix range

Executed, exit codes read directly with no pipe:

- `bin/test` over ten modules — `test_a_release_cannot_ship_an_untrue_milestone`,
  `test_a_merged_ticket_says_so_on_the_tracker`,
  `test_ci_gives_the_checks_what_they_need`, `test_docs_line_wrap`,
  `test_one_word_one_meaning`, `test_release_hygiene`,
  `test_no_real_identifiers`, `test_a_record_states_what_the_tree_has`,
  `test_a_question_says_who_can_answer_it`, `test_a_row_points_by_content` —
  **290 passed, exit 0**.
- **Eleven mutations over the fix surface, each applied alone and reverted,
  all eleven red.** Three on the milestone query, four on the range, four on
  the step's `env:`.
- `uvx ruff check` over `.github/scripts/` and `tests/`, and
  `ruff format --check` over both changed files — **exit 0** each.
- `evidence_check.py --strict .` — **exit 0**, 1137 rows, after three rows
  were re-read and re-verified. All three anchors are units this pass edited
  and all three claims still hold, so each was re-verified with what round 1
  found written beside it rather than removed and rewritten.
- `unverified_check.py --baseline origin/release/v0.11.1 seal/specs/` —
  **exit 0**.

The suite caught one thing on its own: the docstring added for finding 7
wrote `M \ D` in a non-raw docstring and raised `SyntaxWarning: invalid
escape sequence`. Corrected to `M \\ D`, which is how the module spells it
everywhere else.

**Not run: the broad gate.** `agent-contract` §2 assigns it to the sealer,
once, after the rounds settle.

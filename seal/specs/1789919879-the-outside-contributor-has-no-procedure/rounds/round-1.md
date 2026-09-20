# 1789919879-the-outside-contributor-has-no-procedure — review round 1

| Field | Value |
|---|---|
| Target SHA | c0b00d08 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `c8e7a9d0ee4ce67cb9629b2c888771b725d64afa..3323e4336ce44fe8134db9029d1cc2951e3d57ed`, 3 commits |
| Contract changes | none |
| New units | CONVENTION_SURFACES (depth 1); test_no_contributor_facing_surface_names_a_concrete_release_branch (depth 1) |
| Needs a fix | yes — finding 1 takes the pull request's `ledger` job red at the reviewed SHA, and findings 2 through 6 are each a document or a case this work item's own standard asks for. |
| Loses a record or crashes | no. |

- [x] Pass

## What this round was asked

Round 1 of work item `1789919879-the-outside-contributor-has-no-procedure`, at the branch `docs/the-outside-contributor-has-no-procedure` against `origin/release/v0.12.1`, target `c0b00d08`. Spec compliance before quality. The routing answer was the `automation` preset, so `questions.md` Q1 through Q4 are decisions the run made rather than answers a person gave, and judging them is part of this round's job — Q2, refusing to move the default branch off `main`, is the load-bearing one. Weighted above the rest: phase 2 is a gate change and `CONTRIBUTING.md` §*What a change to a gate must carry* binds it, so the case seen red, the stated failure direction, the prompt budget and platform honesty are each checked rather than read; and the exemption list in `spec.md` is the work's real claim, so each of its rows is re-derived against the workflow step and the checker's own logic rather than against the table, because a row that is wrong tells a contributor to skip something CI will then refuse them for. Three things the smith self-reported were handed over to be checked rather than accepted: two frame coordinates that did not resolve and were corrected in place, a mutation that caught a defect in the smith's own phase-2 guard pin, and three `seal/ledger.md` rows this branch drifted and re-verified. `README.ko.md` is in scope beside `README.md`. Facts handed over as executed by the orchestrator at the target: the workflow YAML re-parses, the rendered refusal names both the release case and the contribution case, and the eight commits are in phase order. The full suite, repository-wide lint and the typecheck are the sealer's one act and this round ran none of them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `evidence-check` exits 2 at the reviewed SHA: three backticked occurrences of the retired name read_body (bare here for that same reason) refused by the record arm, so CI's `ledger` job goes red | `seal/specs/1789919879-…/overview.md:19`, `…/phases/phase-5.md:69`, `…/phases/phase-5.md:114` | **fixed** `57f1dacd` | fixed at 57f1dacd — Three records of this work item's own correction named the retired coordinate in backticks and the records arm refused each line, taking `.github/workflows/test.yml`'s `ledger` job red. The checker's message offers two repairs and the marker was chosen deliberately: these lines ARE records of a name the tree does not have, which is the case the marker exists for, and a line that passes only through an invisible absence of backticks goes red again at the next reformat — phase 5 already paid that once. Written in the `` form, which dozens of work items in this tree already use and `tests/test_a_record_states_what_the_tree_has.py` pins. `evidence_check.py .` read for its exit code: 2 before, 0 after, `0 refused`. Phase 5's Executed table gained a clause saying its `exit 0` was true when run and false one commit later, so the row does not read as a run nobody took; Executed at `c0b00d08` in a clone: exit 2, `3 refused`. `.github/workflows/test.yml` exits with the code when it is ≥ 2. The name is written bare here for the same reason |
| 2 | 🟡 A1 requires the base-branch case before `plugin.json` and the message ships the opposite order; the divergence is in no record | `seal/specs/1789919879-…/spec.md` §A1 vs `.github/workflows/hygiene.yml:96` | **fixed** `57f1dacd` | fixed at 57f1dacd — The reviewer is right that the divergence is recorded nowhere, and right that the shipped order is the correct one. A1 is corrected to what the message does — the release case first, then the base branch — with an HTML comment at the row holding what it asked for and why it was not followed, and `overview.md` gains the fourth divergence row. The pin `test_the_refusal_still_serves_the_release_and_puts_it_first` is unchanged, because the message is unchanged; Read. `plan.md` §*The design constraint* and `phases/phase-2.md` decide the order deliberately; `overview.md`'s divergence table carries three rows and not this one |
| 3 | 🟡 "each one exits early on any other base" is false for the round-record, unverified-record and issue-claim steps, which the same table names | `CONTRIBUTING.md` §*What a contribution is not asked for* | **fixed** `57f1dacd` | fixed at 57f1dacd — Re-derived against `.github/workflows/hygiene.yml` rather than against the report: the round-record check, the unverified-record tally and the issue-claim step carry no `base_ref != main` guard, and the version, changelog and ledger-fold steps do. The sentence now names which steps do which and sends a reader to the row rather than generalising past the table. `test_the_exemption_list_says_which_guard_makes_it_true` pins a phrase in a table cell, which did not move; Read: none of those three steps carries a `base_ref != main` guard in `.github/workflows/hygiene.yml`. The table's own cells give the right reasons |
| 4 | 🟡 A BROKEN ledger anchor takes the `ledger` job red, so survivor-check is not "the one check that can ask you for something you do not have" | `CONTRIBUTING.md` §*The one check that can ask you for something you do not have*, and its `seal/ledger/` table row | **fixed** `57f1dacd` | fixed at 57f1dacd — Confirmed by reading `.github/workflows/test.yml`: `if [ "$code" -ge 2 ]; then exit "$code"; fi`, and a BROKEN anchor is exit 2. The heading names two checks, the `seal/ledger/` row stops implying drift is the whole story, and a paragraph says what a contributor does instead — the same answer the section already gives for `survivors.md`, which is to say so on the pull request and leave the convention alone. The changelog fragment carried the same two claims and was corrected with it; Executed: renaming one anchored heading gives `1367 ok · 1 broken`, exit 2. Restored, counts identical |
| 5 | 🟡 Nothing refuses a concrete `release/v0.12.1` in `README.md`, `README.ko.md` or the pull request template, which now carry the same convention | `README.md:639`, `README.ko.md:631`, `.github/PULL_REQUEST_TEMPLATE.md:3` | **fixed** `57f1dacd` | fixed at 57f1dacd — Taken rather than deferred: Q1's grounds are about the rule, and this branch wrote the rule onto three more surfaces while guarding none of them, which is `agent-contract` §12's shape exactly. One parametrized case over `README.md`, `README.ko.md` and the pull request template, in the module phase 1 already wrote rather than a third module — a third module is what `spec.md` S5 was rationing, and the budget widening is recorded as a divergence in `overview.md`. Seen red on each surface in turn, `release/vX.Y.Z` replaced by a concrete branch, one file at a time, each restored from bytes kept outside git: three separate reds, then 17 passed with the tree byte-identical; Executed grep over `tests/`: the two staleness guards are `test_the_contributor_has_a_procedure.py:70` and `test_the_release_check_watches_what_ships.py:203`, and neither reads those three files |
| 6 | 🟡 The template and `README.md` promise CI refuses any contribution based on `main`; the step exits 0 when nothing under a shipping root changed | `.github/PULL_REQUEST_TEMPLATE.md:8`, `README.md:641`, `README.ko.md:634` | **fixed** `57f1dacd` | fixed at 57f1dacd — Confirmed by reading the `-z "$ships"` early return. The instruction was never wrong and only the rationale overreached, so the instruction stands and the rationale now says a contribution that touches nothing shipped is not refused at all — which is why the rule is the branch rather than the check. All three surfaces, the Korean edition rewritten rather than translated clause for clause; Read `.github/workflows/hygiene.yml:80`, the `-z "$ships"` early return |
| 7 | ⬜ The guard pin matches the closing `fi` by exact equality, so a trailing comment would read as an unclosed guard | `tests/test_the_release_check_watches_what_ships.py:271` | answered | The direction is a false red, not a false green, which the reviewer states and I confirmed by reading: a trailing comment on the closing `fi` would report an unclosed guard on a guard that closes. Widening the matcher LOOSENS what the pin accepts, and loosening a pin on a workflow guard is a gate change under `CONTRIBUTING.md` §*What a change to a gate must carry* — a test seen failing before the fix, a stated failure direction, a prompt budget. A fix pass taking that on for a ⬜ the reviewer explicitly marked *noted, not asked for* would ship a loosened gate pin with no red behind it. The step's `fi` carries no trailing comment today and nothing in the repository writes one; Read. Fails safe — a false red |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_release_check_watches_what_ships.py tests/test_the_contributor_has_a_procedure.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py -q` at `c0b00d08` | 78 passed |
| `bin/test` over the eight neighbouring modules the phases name (one word one meaning, release hygiene, cheap twice, the set a work item has, a row points by content, untrue milestone, old roots, script reachability) | 306 passed, 7 skipped |
| Guard pin, mutation 1 — the guard's `exit 0` and its `fi` deleted | **1 failed** (red, as claimed) |
| Guard pin, mutation 2 — only the `exit 0` deleted | **1 failed** |
| Guard pin, mutation 3 — the condition replaced by `if false` | **1 failed** |
| `exit 1` after the refusal changed to `exit 0` | **1 failed** on `test_the_refusal_still_fails_the_run` |
| Unmutated, and the workflow restored from bytes after each | 1 passed; the tree came back byte-identical and `git status --porcelain` empty |
| The step rendered as the runner renders it, `${{ github.base_ref }}` substituted to `main`, then `bash -n` and `bash` | `yaml.safe_load` ok, 13 steps; `bash -n` exit 0; the run exits 1 and prints the whole refusal on one line, `$old` expanded, the nested single quotes intact |
| `python3 skills/evidence-check/scripts/evidence_check.py .` at `c0b00d08` | **exit 2** — `1368 ok · 0 drifted · 0 broken` and `3 refused`. Finding 1 |
| The same after renaming one anchored heading in `skills/code-review/SKILL.md` | `1367 ok · 1 broken`; restored, `1368 ok · 0 broken` |
| `python3 skills/code-review/scripts/survivor_check.py --range origin/release/v0.12.1...HEAD` | exit 0 — 1106 files examined, no removed wording still standing |
| `python3 skills/verify/scripts/unverified_check.py --baseline origin/release/v0.12.1 seal/specs/` | exit 0 — the three open rows are this work item's |
| `python3 .github/scripts/claude_block.py --check` | exit 0 |
| `python3 skills/implement/scripts/seal.py mode --check` | exit 0 — row and folder agree |
| Broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** `agent-contract` §2 leaves all three to the sealer, and this round ran none of them |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

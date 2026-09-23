# 1790154759-the-review-arm-asks-where-no-reviewer-compares — review round 2

| Field | Value |
|---|---|
| Target SHA | 7bc528b14fe420a33775742e13c7cc48c3ea390b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 528 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #518 (PR #528) is a verifying round. Its target is the diff of round 1's fixes, `d954610b..2cbb39fe`, plus the record commit `7bc528b1`, and not the branch. It asked four things:

- whether findings 1, 2 and 3, recorded `fixed` at `20c42b6f`, are closed, by re-running round 1's own probes
- whether every carrier of finding 1's misstatement is corrected across the whole tree, and whether the new wording states only what M1, M3 and M4 measured
- what to make of the units named in the `Contract changes` row, which nobody had reviewed
- three choices the smith made against or beyond round 1's proposal: it pinned the rule sentence instead of the proposed phrase, it parametrised the migration case too, and it wrote a new `survivors.md` with four exemptions

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The grounds paragraph misstated what was measured, and the claim sat in a hook docstring and a test docstring too | `docs/review-chain-spec.md` §*Review arm*; `hooks/commit-review-gate.py#touches_code`; `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit` | answered | `20c42b6f` holds. Read: a whole-tree `git grep` for the old phrasings finds only corrected sentences, *Corrected* notes and round records; each new sentence traces to M1, M2, M3 or M4 |
| 2 | 🟡 Both behaviour cases staged only a `docs/` file, so a `seal/`-only leak passed every gate case | `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit` | answered | `20c42b6f` holds. Executed: `seal/`-only exemption fails both `[seal/ledger.md]` parameters, `docs/`-only exemption both `docs/` ones, `touches_code` all four; the two gate modules pass 142 |
| 3 | ⬜ The prose pin asserted a phrase of the argument rather than the rule | `tests/test_chain_hooks_hardening.py#test_the_review_arms_missing_path_line_is_written_where_it_is_met` | answered | `20c42b6f` holds. Executed: deleting the rule clause fails the pin alone. The phrase round 1 proposed was argument, so declining it is right |
| 🟢 | Round 1's correction: the work item's records repeated 🟡 1 and counted 139 cases | `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/` | confirmed | Read: `changelog.md`, `questions.md`, `plan.md`, `spec.md` (Out and the decision paragraph), `overview.md` and ledger R1 corrected, each marked; 142 executed |
| 🟢 | The migration case parametrised by root as well | `tests/test_chain_hooks_hardening.py#test_a_document_only_commit_wakes_one_arm_and_not_two` | not a defect | Executed: `DOC_ROOTS` cut to `docs/` fails only its `[seal/ledger.md]` parameter, a case nothing held before |
| 🟢 | The new `survivors.md`, four path rows | `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/survivors.md` | not a defect | Executed: passed as `--exempt` against a tip without it, the four rows excuse exactly the four survivors and print their grounds; each ground read true. At the real tip the rows are never consulted — see Deferred |
| 🟢 | The re-stamped `seal/ledger.md` rows and ledger R1 | `seal/ledger.md`; `seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md` | confirmed | Executed: `evidence-check --strict .` exit 0, 1481 ok, 0 drifted. Read: each re-read note describes only the paragraph rewrite |
| 🟢 | The changed test ids reach nothing else | `Contract changes` row of `round-1.md` | confirmed | Read: `git grep` finds no reference by node id; the hook comment names the function, which still fails under the leak |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_chain_hooks_hardening.py -k "document_only_commit or missing_path_line or ignores_document_only"` in a `--no-local` clone at `7bc528b1` | 6 passed |
| Same, with `and touches_code(cwd, invocations)` added to the review arm's `if` | 4 failed (every behaviour parameter), 2 passed |
| Same, review arm exempting commits confined to `seal/` | 2 failed (both `[seal/ledger.md]`), 4 passed |
| Same, review arm exempting commits confined to `docs/` | 2 failed (both `[docs/policies/note.md]`), 4 passed |
| Same, `DOC_ROOTS = ("docs/",)` | 1 failed (`test_a_document_only_commit_wakes_one_arm_and_not_two[seal/ledger.md]`), 5 passed |
| Same, the clause "it is never inferred from the paths it touches" deleted from the paragraph | 1 failed (the pin), 5 passed |
| Same, every mutation restored and byte-compared | 6 passed |
| `tests/test_chain_hooks_hardening.py` and `tests/test_gate_judges_the_repo_it_commits_to.py` | 142 passed |
| `bin/survivor-check --range d954610b..07986ea3` (before `survivors.md`) | exit 1, four survivors: `tests/test_chain_hooks_hardening.py:439`, `tests/test_a_row_points_by_content.py:781`, `tests/test_local_mode_resolves_under_the_git_dir.py:196` and `:327` |
| Same range to a scratch tip with `survivors.md` removed, then with that file passed as `--exempt` | exit 1, the same four; then exit 0, all four under `exempt` with their grounds |
| `bin/survivor-check --range d954610b..2cbb39fe`, with and without `--exempt` | exit 0 both times, nothing printed as exempt: the file's quotes take the phrases out of what is searched (#308) |
| `bin/evidence-check --strict .` | exit 0, `1481 ok · 0 drifted · 0 broken` |
| `tests/test_docs_line_wrap.py`, `tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py`, `tests/test_review_axes.py` | 62 passed |
| `bin/correction-check --range d954610b..7bc528b1` | exit 0, no merge commit in range |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: not run in this round. The sealer's, and it comes due now |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/review-chain-spec.md` §*Review arm*, paragraph *Why this arm has no document-root line*; `hooks/commit-review-gate.py#touches_code`; `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit` | round 1's 1 — fixed |
| round-1 | `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit`; `seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md` R1 | round 1's 2 — fixed |
| round-1 | `tests/test_chain_hooks_hardening.py#test_the_review_arms_missing_path_line_is_written_where_it_is_met` | round 1's 3 — fixed |
| round-1 | `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/` | round 1's ⬜ — correction |
| round-1 | `spec.md` M1–M3 | round 1's 🟢 — confirmed |
| round-1 | `docs/review-chain-spec.md` §*Review arm* | round 1's 🟢 — confirmed |
| round-1 | `tests/test_chain_hooks_hardening.py` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger.md` | round 1's 🟢 — confirmed |
| round-1 | `README.md`, `README.ko.md`, `CONTRIBUTING.md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/commit-review-gate.py#judge` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `survivors.md` in the tree takes its own quotes out of what `survivor-check` searches for, so this item's four rows are never consulted at the tip and never print as `exempt` | #308 (already deferred there before this round; open, `from-review`) | the repository owner, when #308 is scheduled |

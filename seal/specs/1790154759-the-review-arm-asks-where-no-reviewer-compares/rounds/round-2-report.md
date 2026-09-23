# Round 2 report — 1790154759-the-review-arm-asks-where-no-reviewer-compares

| Field | Value |
|---|---|
| Round | 2 (verifying) |
| Target | round 1's fix range `d954610b..2cbb39fe` (3 commits) and the record commit `7bc528b1` |
| Target SHA | 7bc528b14fe420a33775742e13c7cc48c3ea390b |
| Reviewer | specseal:warden on claude-opus-5-5 |

## What this round was asked

Round 2 of #518 (PR #528) is a verifying round. Its target is the diff of
round 1's fixes, `d954610b..2cbb39fe`, plus the record commit `7bc528b1`,
and not the branch. It asked four things. First, whether findings 1, 2 and 3,
recorded `fixed` at `20c42b6f`, are closed, checked by re-running round 1's
own probes. Second, whether every carrier of finding 1's misstatement is
corrected across the whole tree, and whether the new wording states only
what M1, M3 and M4 measured. Third, what to make of the units named in the
`Contract changes` row, which nobody had reviewed. Fourth, three choices the
smith made against or beyond round 1's proposal: it pinned the rule sentence
instead of the proposed phrase, it parametrised the migration case too, and
it wrote a new `survivors.md` with four exemptions. No full suite,
repository-wide lint or broad gate was run, because those belong to the
sealer. Every probe ran in a `--no-local` clone at the target SHA.

## Summary

All three findings hold closed, and nothing in the fix range needs a fix.

- **Finding 1.** No carrier of the old claim is left outside the round
  records. The ones this search found are `docs/review-chain-spec.md`, the
  `touches_code` docstring, the test docstring, `changelog.md`, `plan.md`,
  `questions.md` and two places in `spec.md`. Each new sentence traces to M1,
  M2, M3 or M4. The round records quote the old sentence on purpose.
- **Finding 2.** Each half of the line now fails on its own parameter.
  Widening the parametrisation to the migration case gave something the
  suite did not have before: a case that fails when the parity arm's own
  line loses `seal/`.
- **Finding 3.** The new pin fails when the rule sentence is deleted. It
  pins the rule rather than the argument. The wording round 1 proposed would
  have pinned a phrase of the argument again, which is the same class of
  problem as ⬜ 3.
- **`survivors.md`.** All four rows excuse exactly the four survivors the
  range left, and each row's grounds are true. At the range tip the rows are
  never consulted, though. The file's own quotes remove the phrases from
  what the check searches for. That is #308, which is already open, and it
  is listed under Deferred.

## Findings from execution

- **Finding 2's parametrisation catches each half of the leak on its own,
  in both arms.** Round 1's mutations were re-run against the target. With
  `touches_code` added to the review arm's condition, all four behaviour
  parameters fail. With an exemption for commits confined to `seal/` alone,
  both `[seal/ledger.md]` parameters fail and both `docs/` parameters pass.
  With the same exemption for `docs/` alone, the reverse happens. The new
  arm the migration case gained was also tested. With `DOC_ROOTS` cut to
  `("docs/",)`, the parity arm wakes on a `seal/`-only commit, and only
  `test_a_document_only_commit_wakes_one_arm_and_not_two[seal/ledger.md]`
  fails. `test_parity_gate_ignores_document_only_commits` stays green. So
  `survivors.md` row 1's claim is true: the migration case is what covers
  `seal/` for the parity arm.
- **Finding 3's pin fails on the rule sentence alone.** With the clause
  "it is never inferred from the paths it touches." deleted from
  `docs/review-chain-spec.md`, the pin case fails and nothing else does. The
  phrase occurs once in the file.
- **The counts the fix pass wrote are the ones the suite gives.** The two
  gate modules pass 142 cases, as ledger row R1 and `overview.md` now say.
- **The four `survivors.md` rows each match a survivor, and nothing more.**
  I ran the range without the file at its tip: four survivors, exit 1. Then
  I ran the same range with the file passed as `--exempt`: all four printed
  under `exempt` with their grounds, and the check exited 0. On the real
  tip `2cbb39fe`, where the file is in the tree, the check reports nothing
  at all, whether or not `--exempt` is given. None of the four is printed as
  exempt there. The file quotes the survivors' phrases, so the phrases are
  no longer rare in the corpus and the survivors are no longer candidates.
  That is `survivor_check.py`'s behaviour and not this branch's. It is #308,
  which is open, and it is listed under Deferred.

## Findings from reading

- **Finding 1's carriers.** I ran `git grep` over the whole tree for the old
  phrasings: *measured positive*, *measured empty*, *reached a reviewer*,
  *planning bookkeeping*, *the only population*, *every docs.only*, *exactly
  where the measured*. Every hit outside the round records is a corrected
  sentence. Some of those deliberately quote the old claim inside a
  *Corrected 2026-09-23* note in `spec.md`. The round records quote it
  because they record the finding. The shipped hook comment above
  `DOC_ROOTS` never carried the claim, and it still names the parametrised
  test correctly.
- **Whether the new wording states only what was measured.**
  - *At least 25 … and 26* is M4's lower bound, with its qualifier kept in
    the shipped paragraph and in `spec.md`.
  - The test docstring writes "26 fixed findings … sit in the ledger alone"
    without *at least*. That is still true, because 26 do sit there.
  - "No reviewed work item was ever confined to the two roots" is M1.
  - "The seventeen … never reached a reviewer" is M2, which says none of
    them added a round record.
  - The #514 sentence now names the four test files, which is M3.
  - The hook docstring's "a measured share" is accurate: 25 of about 750
    fixed findings.
  - "Stop asking exactly where the reviewed findings sit" refers back to the
    findings named in the two sentences before it, so it does not claim that
    most findings sit there.
  - The changelog's "one of them 🔴 in the last fold" is true today. #514 is
    the latest fold on `release/v0.14.0`.
- **`Contract changes`.** Parametrising the two cases changes their pytest
  node ids. No file in the tree names either case by node id. Ledger row R1
  anchors them by unit, which `evidence-check` re-hashed: 0 drifted.
- **The smith's pin choice was right.** The sentence round 1 proposed to
  pin, "exactly where the reviewed findings sit", is part of the argument.
  Pinning it would have left the wording finding 3 was about in a new place.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `survivors.md` in the tree takes its own quotes out of what `survivor-check` searches for, so this item's four rows are never consulted at the tip and never print as `exempt` | #308 (already deferred there before this round; open, `from-review`) | the repository owner, when #308 is scheduled |

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round: `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/rounds/round-1.md`,
`rounds/round-1-report.md`, `spec.md`, `overview.md`, `changelog.md`, `survivors.md`;
the full diff `d954610b..2cbb39fe`; `tests/test_chain_hooks_hardening.py` (the parity,
review-arm, migration and pin cases); `hooks/commit-review-gate.py` (the `DOC_ROOTS`
comment, `touches_code`, the review arm's condition in `judge`);
`docs/review-chain-spec.md` §*Review arm*; `skills/code-review/scripts/survivor_check.py`
(module docstring, exemption reader); `bin/survivor-check`; `git log` of
`origin/release/v0.14.0`.

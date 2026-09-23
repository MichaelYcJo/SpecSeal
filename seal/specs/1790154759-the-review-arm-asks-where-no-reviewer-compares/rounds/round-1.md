# 1790154759-the-review-arm-asks-where-no-reviewer-compares — review round 1

| Field | Value |
|---|---|
| Target SHA | 17327c53d3030d1efb7eb9449bba7d82125b9ebb |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 528 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the grounds misstate what was measured) and 🟡 2 (the `seal/` half of the line can leak unseen) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of #518 (PR #528), the whole branch against `release/v0.14.0`. Stage 1 asked whether the decision follows from `spec.md`'s measurements (the review arm keeps asking on a change confined to `docs/` and `seal/`), and whether M1 to M3 hold when re-derived from `git log` over the release branch. Stage 2 asked four things:

- whether the new cases fail under the mutation the issue fears, the parity arm's path line leaking into the review arm
- whether the wording-pin case pins a rule or prose
- whether the four re-stamped `seal/ledger.md` rows still hold
- whether anything in the README pair or `CONTRIBUTING.md` now disagrees with the new §*Review arm* rows

The handoff labelled M4's lower bound unverified, and asked whether the paragraph citing it states only what was measured.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The grounds paragraph says every docs/seal-only change that reached a reviewer produced defects, using #514 as the example. M1 says none ever did, and #514 changed four test files. It also calls the never-reviewed commits "measured empty". The same claim is in a shipped hook docstring and a test docstring | `docs/review-chain-spec.md` §*Review arm*, paragraph *Why this arm has no document-root line*; `hooks/commit-review-gate.py#touches_code`; `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit` | open | Executed: M1 probe (0 of 88 adders confined), `git show --name-only f2943c04` (four test paths), M2 probe (13 flow, 3 one-root only, 1 seal-only). Read: `spec.md` M1, M3 |
| 2 | 🟡 Both behaviour cases stage only a `docs/` file, so a review-arm exemption for `seal/`-only commits passes every gate case. R1 claims the `seal/` half as executed | `tests/test_chain_hooks_hardening.py#test_the_review_arm_asks_on_a_document_only_commit`; `seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md` R1 | open | Executed: `seal/`-only mutation in `judge`, two gate modules `140 passed`. The parametrised fix fails `[seal/ledger.md]` under it, and passes clean |
| 3 | ⬜ The prose pin asserts a phrase of the argument ("the one population that measured positive"), not the rule, so rewording the grounds fails it with the rule unchanged | `tests/test_chain_hooks_hardening.py#test_the_review_arms_missing_path_line_is_written_where_it_is_met` | open | Read. The other three assertions pin the rule and are right |
| ⬜ | The work item's records repeat 🟡 1's misstatement (`changelog.md`, `questions.md` preamble, `spec.md` §*What the measurement decides* and §*Out*, `plan.md` summary); R1 and `overview.md` say 139 gate cases where HEAD has 140 | `seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/` | correction | Read; count executed at `17327c53` |
| 🟢 | M1, M2 and M3 reproduce from the release branch | `spec.md` M1–M3 | confirmed | Executed: scratch probe over `f8f1c9de` (88 / 0; 175 / 17 / 13 flow). Read: the three verdict tables of `1790119502-four-shipped-work-items-wait-unfolded` (4 + 3, all `docs/`, one 🔴) |
| 🟢 | M4's "at least 25 / 26" is no larger than an independent count | `docs/review-chain-spec.md` §*Review arm* | confirmed | Executed: own classifier, 311 records, 31 `docs/`-only from 16 items, 26 ledger-only |
| 🟢 | The two behaviour cases fail under the whole-line leak, in two shapes | `tests/test_chain_hooks_hardening.py` | confirmed | Executed: `touches_code` added to the review arm's condition, and an early return in `judge` on a docs-only commit; both cases fail under each |
| 🟢 | The four re-stamped `seal/ledger.md` rows' claims still hold | `seal/ledger.md` | confirmed | Read each claim against the tree. Executed: `evidence-check --strict .` exit 0, 1481 ok; `tests/test_review_axes.py` green |
| 🟢 | The README pair and `CONTRIBUTING.md` do not disagree with the new rows | `README.md`, `README.ko.md`, `CONTRIBUTING.md` | confirmed | Read: no path named for the review arm in any of them |
| 🟢 | Q2: A3 is covered by the existing declaration case | `hooks/commit-review-gate.py#judge` | confirmed | Read: `routed` decided before any path is read |

## Paste-ready fixes

```
#518 measured whether review finds defects there before drawing any line,
and it does. Across every round record, at least 25 fixed findings sit in
`docs/` alone and 26 in the ledger alone. #514's fold, which changed `docs/`,
`seal/` and four test files, opened seven findings a later round verified as
fixed, all in `docs/`, one of them 🔴. No reviewed work item was ever confined
to the two roots, and the seventeen docs/seal-only commits on the release
branch never reached a reviewer, so nothing measured them either way. The
parity arm's line would stop asking exactly where the reviewed findings sit,
on the strength of a population nobody measured. A documentation pass that
should reach nobody is routed that way before the first edit, by declaring
`straight to the PR`; it is never inferred from the paths it touches.

# hooks/commit-review-gate.py, touches_code docstring, last paragraph:
    Only the parity arm calls this. The review arm's question is not about an
    original, and `docs/` is where a measured share of the review chain's
    fixed findings sit (`docs/review-chain-spec.md` §*Review arm*, #518).

# tests/test_chain_hooks_hardening.py,
# test_the_review_arm_asks_on_a_document_only_commit docstring, middle:
    conforms to. #518 measured it: #514's fold, which changed `docs/`,
    `seal/` and four test files, produced seven fixed findings, all located
    in `docs/`, one of them 🔴. So a commit confined to `docs/` meets the

# tests/test_chain_hooks_hardening.py,
# test_the_review_arms_missing_path_line_is_written_where_it_is_met:
-    assert "the one population that measured positive" in review_arm, (
+    assert "exactly where the reviewed findings sit" in review_arm, (
```
```
@pytest.mark.parametrize("path", ["docs/policies/note.md", "seal/ledger.md"])
def test_the_review_arm_asks_on_a_document_only_commit(repo, path):
    """...docstring unchanged except as 🟡 1 says..."""
    (repo / "seal").mkdir(exist_ok=True)
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    stage(repo, path, "text\n")
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "deny", (
        f"a commit confined to {path} passed the review arm with no declaration, "
        "no review mark and no waiver"
    )
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "[no-review]" in reason
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_chain_hooks_hardening.py -k "document_only_commit or missing_path_line"` in a `--no-local` clone at `17327c53` | 4 passed |
| Same, with `and touches_code(cwd, invocations)` added to the review arm's `if` | 2 failed (both new behaviour cases), 2 passed |
| Same, with `if not touches_code(cwd, invocations): return [], git_dir` after `routed` in `judge` | 2 failed (both new behaviour cases), 2 passed |
| `tests/test_chain_hooks_hardening.py` and `tests/test_gate_judges_the_repo_it_commits_to.py`, review arm exempting non-empty commits confined to `seal/` | 140 passed: the leak is not caught |
| Same two modules, unmutated | 140 passed |
| 🟡 2's parametrised case, clean hook, then under the `seal/`-only mutation | 4 passed; then `[seal/ledger.md]` failed, the other 3 passed |
| 🟡 1's paragraph and pin swap applied, then the pin case, `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py`, `tests/test_no_real_identifiers.py` | 56 passed |
| `bin/evidence-check --strict .` at `17327c53` | exit 0, `1481 ok · 0 drifted · 0 broken` |
| The two gate modules plus `tests/test_review_axes.py` | 148 passed |
| Scratch probe over `git log f8f1c9de`: M1, M2, M4 | M1 88 items, 0 confined; M2 175 non-merge, 17 confined, 13 flow / 4 one-root / 1 neither; M4 311 records, 31 `docs/`-only (16 items), 26 ledger-only |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: not run in this round; the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

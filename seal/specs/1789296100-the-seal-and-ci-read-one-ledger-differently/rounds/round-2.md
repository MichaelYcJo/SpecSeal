# 1789296100-the-seal-and-ci-read-one-ledger-differently — review round 2

| Field | Value |
|---|---|
| Target SHA | bc70e7d90cde357247e82477a712b2447ccc907d |
| Ran by | warden on claude-opus-5 |
| PR | 378 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round: round 1's fixes were written by a fix pass and read by nobody, and this round is what fills round 1's `Fixes checked by` cell. Scope was the diff of the fixes, `37f7321..bc70e7d`, judged against round 1's findings — not a re-review of the build. Round 1's verdicts were inherited.

The reviewer was told the honest outcome is often "nothing" and that reaching for something to say is the failure mode here, not the safe option.

It was asked to run the mutation itself rather than trust the fix pass's account, and to check that each red is red for the reason it claims — the fix pass had reported one invalid red, a `NameError: ast` from a formatter hook removing an import that was not yet used.

**The round opened nothing needing a fix.** It ran six mutations of `gate()` — round 1's own, a separate-branch form, one that does not call the failure form, one that stops collecting, and one that moves the failure form outside the branch — all red, each at its own assertion, no `NameError` among them. Unmutated: 14 passed, exit 0.

It also established by execution that two of the fix pass's three reasons for rewriting round 1's paste-ready block were not merely defensible but necessary: a reinforcing branch shaped like the existing `if name == SUITE:` makes round 1's `assert "LEDGER" not in loop` go red on correct code, and moving the failure form outside the branch while leaving its name below leaves all three of round 1's assertions green. The old block would have produced a false positive in one direction and passed a gate that does not refuse in the other.

One ⬜ was opened and is not a fix-list item: the reader-count edit did not re-fold its paragraphs, leaving one over-long line in `spec.md` and an orphan line each in `overview.md` and `changelog.md`. `tests/test_docs_line_wrap.py` does not cover those paths, so nothing goes red — but the changelog fragment is concatenated verbatim at the release, so that one line reaches `CHANGELOG.md`. The orchestrator re-folded the three paragraphs after the round, which is recorded here because it is an edit the round did not read.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's finding 1 is fixed, and the AST rewrite is strictly stronger than the paste-ready block it replaced | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` · `skills/verify/scripts/broad_gate.py` | answered | executed — five mutations of `gate()`, each red on the assertion that owns it, no wrong-reason red; a reinforcing `LEDGER` branch leaves the case green while round 1's string assertion goes red; a failure form moved out of the branch passes all three of round 1's assertions and fails this one |
| 2 | Round 1's finding 2 is fixed: the row names the third shape, its five live instances and the files they sit in | `seal/follow-up.md` §*Schedulable items with nowhere else to go* | answered | executed — the checker's own `ANCHOR_RE` per ledger file returns seven dropped tokens, two of them path-less prose shorthand at `seal/ledger.md:1830` and `:1859`, so five is right; the narrowed run reports `1148 ok · 0 drifted`, exit 0 read directly |
| 3 | Round 1's finding 3 reached #379 and the divergence row now names the class rather than this work item's scheduling | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md` | answered | read — the row names all three framer commits of the release and points at #379; the fix is a shared surface and stays out of this branch |
| 4 | Round 1's finding 4 is fixed: the divergence table carries the `seal/ledger.md` row with the grounds | same file, §*Where spec and implementation diverged* | answered | read |
| 5 | Round 1's finding 5 is fixed: the contract names `gate`, and *Fed back into the spec* carries both corrections | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md` | answered | read |
| 6 | Round 1's finding 6 is fixed: the table is one row per reader and every surviving count says what it counts | `skills/evidence-check/SKILL.md` · `CONTRIBUTING.md` · `spec.md` | answered | read — a grep of every reader-count sentence in the five documents S5 lists |
| 7 | Round 1's finding 7 is closed: the four `Ran by` cells are the orchestrator's and were filled | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/phases/` | answered | read — the fix pass left the phase records untouched, which is correct |
| 8 | Round 1's finding 8 is fixed: both writers are named as writers, and both return 1 | `skills/evidence-check/SKILL.md` · `CONTRIBUTING.md` | answered | read |
| 9 | Round 1's finding 9 is fixed: the header comment and the `####` under it now say the same thing | `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` | answered | read |
| 10 | The reader-count reword left one unreflowed line in each of three files; the changelog one ships into `CHANGELOG.md` at the release | `spec.md:8` · `overview.md:11` · `changelog.md:7` | open | read — measured column widths against each file's own prose; no covered path, `tests/test_docs_line_wrap.py` is 23 passed |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q` at the target SHA | **14 passed** in 0.61 s, exit 0 read directly |
| Five mutations of `gate()` in `skills/verify/scripts/broad_gate.py`, each run against that module and each restored from bytes held in the mutating process | every one **1 failed, 13 passed**, exit 1, the new case named in the failure and the assertion that owns the mutation quoted. No `NameError` in any run |
| A sixth mutation adding a reinforcing `if name == LEDGER:` enrichment beside the existing `if name == SUITE:` | **14 passed** — the rewritten case is green, while round 1's `assert "LEDGER" not in loop` evaluates False on the same tree |
| Round 1's three paste-ready assertions evaluated against the tree where the failure form has left the `if failures:` branch | all three pass while the rewritten case fails — the measurement behind the fix pass's second reason |
| The checker's own `ANCHOR_RE` applied to `seal/ledger.md` and the fragment, against every backticked coordinate-shaped token in each | seven dropped in the shared ledger, two path-less prose shorthand; **five row anchors**, in the files the rewritten row names. The fragment drops none |
| `evidence_check.py --ledger seal/ledger.md .` | **`1148 ok · 0 drifted · 0 broken · 0 external · 0 old-format`**, exit 0 read directly — the figure the follow-up row quotes, true at this SHA |
| `bin/test tests/test_docs_line_wrap.py -q` | **23 passed** — none of the three unreflowed paths is covered, so nothing goes red |
| `git status --porcelain` after every probe and again at the end | empty each time. Each mutated file was restored from bytes held in the mutating process and compared byte for byte; no probe file was written inside the repository |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It has not been taken at any SHA on this branch, and it is not this round's to take (contract §2). With this round opening nothing that needs a fix, it is what comes due next: the sealer's spawn, not a run for the session reading this to assemble |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:251` · `skills/verify/scripts/broad_gate.py:590` | round 1's 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:65` · `seal/ledger.md:63,71,81,143` | round 1's 2 — fixed |
| round-1 | `agents/framer.md:91` · `tests/test_chain_hooks_hardening.py:1014` | round 1's 3 — deferred |
| round-1 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md` | round 1's 4 — fixed |
| round-1 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md:138` | round 1's 5 — fixed |
| round-1 | `spec.md:83` · `skills/evidence-check/SKILL.md:178` · `CONTRIBUTING.md:21` | round 1's 6 — fixed |
| round-1 | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/phases/phase-1.md` | round 1's 7 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1723` · `:2423` · `CONTRIBUTING.md:21` | round 1's 8 — fixed |
| round-1 | `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` | round 1's 9 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `ANCHOR_RE` drops a coordinate it cannot parse instead of naming it — three shapes now, five live instances in the shared ledger | `seal/follow-up.md` §*Schedulable items with nowhere else to go*, the existing row, which this diff extended. Already deferred; round 2 confirms the row's count and its instances | the repository owner |
| The framer / overview-case contradiction | #379. Already deferred by round 1's fix pass, and the divergence row now points at it | the repository owner |
| Whether `broad-gate`'s own end-to-end run shows the notice absent at exit 2 | `overview.md` §*Not verified*. Already deferred by this branch | the sealer |
| `round_record.py`'s `fix_table` cuts the SHA out of the middle of its own code span and leaves both backticks standing, so every `fixed` verdict in `round-1.md` reads *fixed at `<sha>` — `` —*. **Already ridered**, at the `note` line of that function, stamped `Verified 2026-09-08 against fix_table@884956f3`, and it predates this branch. Named here only so it is not re-reported as new | the repository owner, at the rider |

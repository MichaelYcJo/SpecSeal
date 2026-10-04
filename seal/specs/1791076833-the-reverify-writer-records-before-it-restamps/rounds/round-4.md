# 1791076833-the-reverify-writer-records-before-it-restamps — review round 4

| Field | Value |
|---|---|
| Target SHA | c4494a40f585642a672dd27d59afe840a668db34 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #756 |
| Broad gate | d2851932 against e141980a |
| Fixes checked by | no fixes to check |
| Fix range | `c4494a40f585642a672dd27d59afe840a668db34..0d6f4c54d56678718e1c6f8de05e1d2f686082a3`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 4 of work item `1791076833-the-reverify-writer-records-before-it-restamps` (#647 steps C and D, PR #756). It is the one verifying round that the round cap allows: round 3 was the cap's terminal record, and the branch fixed the finding it owned. The target is the diff of round 3's fixes, `ab8a4ecf..ec801b76`.

Round 3's two verdicts each need a check that they are closed:
- 🟡1: the vendored copy now reads `seal/config.md` with `strict=True`.
- ⬜2: the `Enforced by:` line.

The fix added no unit. Whatever this round opens, the run ends here. A finding still open after this round is deferred under the filing ladder, and the PR is labelled `chain: capped`. So give each finding its `Who answers it`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 3's yellow 1 is closed — the vendored copy reads `seal/config.md` strictly, so a config that is not UTF-8 will not read and a moved row citing no clause is left, as the plugin leaves it | `skills/evidence-check/scripts/evidence_check.py:3737` | confirmed | executed: the new row red with the argument reverted (1 failed, 13 passed) and green restored; probe Q1-Q4 and Q6, plugin and vendored both exit 1 and leave; read: `declared_pacts` and `read` with `strict=True` open the file the same way and answer None on the same exceptions |
| 🟢 | round 3's white 2 is closed — the vendored paragraph's `Enforced by:` line names the case for "or will not read" | `docs/the-pact.md:308` | confirmed | read: the line names `test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`; executed: the folded-statement module passes in the narrow run |
| 🟢 | The fix opens no disagreement that loses a record: a strict read can only make `said` None, and None only leaves rows | `skills/evidence-check/scripts/evidence_check.py:3743` | confirmed | read: `blind = said is None or ...`; executed: probe Q1-Q7, no shape where the vendored copy re-stamps and the plugin leaves; round 3's P1-P16 enumeration carried, not re-run |
| 🟢 | Ledger rows C1 and W9 hold at the new hashes | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | confirmed | executed: `bin/evidence-check --ledger` exit 0, 234 ok, 0 drifted, 0 broken; read: C1's "or will not read" now true for a non-UTF-8 config, W9's claim untouched by a read of a file the run does not write |
| ⬜ 1 | `read`'s docstring says a file the run only reads keeps the lenient read, and since round 3's fix the vendored branch reads `seal/config.md`, which the run only reads, strictly | `skills/evidence-check/scripts/evidence_check.py:1074` | answered | no change: the exception is stated where it applies. The comment above the vendored read in `record_pact_changes` says it is read strictly, as `declared_pacts` reads it, and why (round 3 of PR #756, yellow 1). `read`'s docstring states the default its callers override by passing `strict`, and every strict caller names its own grounds. Editing the docstring now would commission a fix no round reads, after a verifying round that opened nothing; read: the vendored call at `:3737` passes `strict=True` for a file nothing writes; behaviour right, the sentence wrong; the unit `read` predates the rounds (phase 2), depth 0; who answers it: the orchestrator of PR #756, a comment-only edit before the seal or deferred under the ladder |
| ⬜ 2 | The spec's W9 says a file the run only reads keeps the lenient read | `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md:236` | answered | corrected at `0d6f4c54`: `spec.md` W9 names the vendored copy's `seal/config.md` as the one exception to the lenient read; read: same sentence as ⬜ 1, in the frame; a correction to the run's paperwork, not a fix; who answers it: the orchestrator of PR #756 |
| carried | Round 1's, round 2's and round 3's earlier confirmations (PR #749's closures, W8-W10, K1, K2, the seven round-1 units, T1/T2, the 0.18.0 P1 re-read, round 2's closures) | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | carried from round 3; the fix range touches the vendored branch's one read, its comment, one test case, one doc line and two ledger hashes; executed: the narrow modules below, 260 passed |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `c4494a40` | ❓ out of verified scope | the broad gate is the sealer's, after the rounds settle; the `unverified` label it carries is honest; who answers it: the sealer |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, read(), replacing the
# last sentence of the docstring (lines 1074-1076)
    that will not decode will not read, and its caller leaves it. Code under
    a coordinate and a released ledger keep the lenient read, because nothing
    is written back to them. A vendored copy's `seal/config.md` is read
    strictly although nothing writes it, because there a byte the lenient
    read replaces can hide the `Pact notify` row (round 3 of PR #756,
    yellow 1)."""
```
```markdown
seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md:236,
replacing the sentence:

A file it only reads, such as the code under a coordinate, keeps today's
lenient read; a vendored copy's `seal/config.md` is the one exception, read
strictly since round 3 of PR #756.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the writer module, the declaration module, `tests/test_pact_check.py`, the CI print module, `tests/test_no_real_identifiers.py`, the folded-statement module and `tests/test_docs_line_wrap.py` at the target | 260 passed |
| The writer module's `vendored` cases with `strict=True` removed from the vendored read, then restored | 1 failed (`[it is not UTF-8]`), 13 passed; restored, all pass |
| Probe Q1-Q7, plugin and vendored copy, for a moved row citing no clause | Q1-Q4, Q6: both exit 1, row left, nothing recorded. Q7: plugin exit 0 and re-stamped, vendored exit 1 and left (the documented safe direction) |
| `ruff check` and `ruff format --check` on the two changed Python files | both exit 0 |
| `bin/evidence-check --ledger` over this item's fragment at the target | exit 0; 234 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

```python
# One probe file in the clone's tests/, run once, deleted. It imports the
# writer module's helpers (repo, cite, row, move_serialize, run, _vendored,
# config_text). For each seal/config.md below it cites src/orders.py#serialize
# from a row citing no clause, moves serialize, then runs
# `--reverify --into <fragment> --checked` through the plugin's script and
# through `_vendored`. It prints exit, re-stamped, recorded, first LEFT line.
# HEAD = config_text(("Mode", "shared"), ("Pact", PACT_URL))
Q1 = b"| Item | Value |\n|---|---|\n| Mode | shar\xffed |\n| Pact | URL |\n"
Q2 = HEAD + an HTML comment block holding "| Pact notify | always | \xff"
Q3 = seal/config.md replaced by a directory
Q4 = seal/config.md replaced by a dangling symlink
Q6 = b"| Item | Value |\n|---|---|\n| Note | caf\xe9 |\n"   # no Pact row
Q7 = config_text(("Mode", "shared"), ("Pact", URL), ("Pact notify", "never"))
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3717` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3737` | round 1's 🟡 2 — fixed |
| round-1 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:1` | round 1's ⬜ 3 — answered |
| round-1 | `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/plan.md:24` | round 1's ⬜ 4 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:4992` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:4962` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3821` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3813` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3133` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:848` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:240` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:1050` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:907` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1097` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-pact.md` | round 1's 🟢 — confirmed |
| round-1 | the tree at `7517df8b` | round 1's ❓ — out of verified scope |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3645` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/scripts/chain_check.py:4048` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | round 2's ⬜ 4 — answered |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3729` | round 2's 🟢 — confirmed |
| round-2 | `hooks/config.py:786` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_signatory_records_a_pact_change.py:1356` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:65` | round 2's 🟢 — confirmed |
| round-2 | the tree at `bc30a10d` | round 2's ❓ — out of verified scope |
| round-3 | `skills/evidence-check/scripts/evidence_check.py:3734` | round 3's 🟡 1 — fixed |
| round-3 | `docs/the-pact.md:308` | round 3's ⬜ 2 — answered |
| round-3 | `skills/evidence-check/scripts/evidence_check.py:3650` | round 3's 🟢 — confirmed |
| round-3 | `skills/evidence-check/scripts/evidence_check.py:3740` | round 3's 🟢 — confirmed |
| round-3 | `tests/test_pact_check.py:273` | round 3's 🟢 — confirmed |
| round-3 | the tree at `bfb7d0b7` | round 3's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

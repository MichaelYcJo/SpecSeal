# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — review round 3

| Field | Value |
|---|---|
| Target SHA | ae3e5232a170e905cc834c414c30418ea8ab163a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #758 |
| Broad gate | 68b69e7b against e141980a |
| Fixes checked by | no fixes to check |
| Fix range | `ae3e5232a170e905cc834c414c30418ea8ab163a..b9bb12cc3dc893f8db97a3c5923fb345345343b2`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item `1791076832-the-broad-gate-re-runs-the-test-command-at-the-base` (#747 and #748, PR #758). It is the verifying round for round 2's fixes, range `4e981840..55b40287`. Round 1 met the floor and round 2 was the one reopening, so this record ends the run whatever it finds. A finding left open takes the filing ladder and gets a `Who answers it`.

Check whether each round-2 verdict is closed.
- 🟡1: the trailing label now accepts one or two lowercase words, and the first label stays one word on the grounds of pytest's `KNOWN_TYPES` order. That departs from the reviewer's proposal. Judge it, and run the subtests fixture end to end under it, since the fix pass did not.
- ⬜2: `NO_RUNNER`'s reason and the four places carrying the same sentence.

No unit was added: the changes are rows on `SUMMARY_LINES` and asserts inside existing tests.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the comment over the summary regex gives "pytest lists its own categories first" as the reason the first label is one word, where pytest 9.1.1's own list holds three two-word categories; the reason is that the one-word ones come first and every test that ran is counted under one | `skills/verify/scripts/broad_gate.py:1861` | answered | no change. The behaviour is right and pinned: three regex mutations each turned exactly one rejection row red, and this round re-derived the comment's missing step from pytest 9.1.1's `KNOWN_TYPES`. The comment names that order as its ground. Editing it after the run's last round would commission a change that no round reads; read: pytest 9.1.1's terminal and subtests modules; the behaviour is right and pinned, the stated reason is not the one that holds |
| ⬜ 2 | ledger row B3's claim cell still says `NO_RUNNER` is given where no prefix printed a summary, the wording round 2's finding 2 retired everywhere else | `seal/ledger/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base.md:9` | answered | corrected at `b9bb12cc`: ledger row B3's claim now says `NO_RUNNER` is given where no prefix printed a line the gate reads as pytest's summary; read; a correction to the run's paperwork, not to the tool |
| 🟢 | round 2's finding 1 is closed — pytest 9's subtests summary is read as pytest's | `skills/verify/scripts/broad_gate.py:1867` | confirmed | executed: the subtests fixture end to end at the target gave `failing on base too` where the base fails the file and `new` where it passes, runner-first and lint-first; round 2's gate gave the `NO_RUNNER` reason in all four; the narrower first label is grounded in pytest 9.1.1's summary order |
| 🟢 | round 2's finding 2 is closed — the unmeasured reason says the gate did not read a summary | `skills/verify/scripts/broad_gate.py:1875` | confirmed | read: the reason, the docstring, the skill's bullet, rule 3 and the changelog fragment agree; executed: the pin passes at the target |
| 🟢 | round 1's findings 1 to 8 stay closed | `skills/verify/scripts/broad_gate.py:2006` | confirmed | executed: the cargo, `cd`, runner-first, lint-first, ending and counterfeit cases pass at the target; carried from round 2 for the rest, since this round's diff touches only the summary regex |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| The #747 summary, ending, reason, cargo, `cd`, runner-first, lint-first and counterfeit cases of `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in a `--no-local` scratch clone at `ae3e5232`, with the worktree's pytest 9.1.1 and no xdist | `31 passed` |
| A probe file in the clone: the gate end to end on a fixture whose `tests/test_two.py` uses the `subtests` fixture, for the base failing or passing it, and the row runner-first or lint-first | at `ae3e5232`: `failing on base too` twice and `new` twice, `4 passed`; the base runs printed `2 failed, 1 passed, 1 subtests passed in 0.03s` and `2 passed, 2 subtests passed in 0.01s` |
| The same probe with `eafc2021`'s `broad_gate.py` swapped in | `4 failed`, each with the `NO_RUNNER` reason; the file restored afterwards |
| Four forms of the regex against every `SUMMARY_LINES` row: the target's, round 2's proposal, a later label of up to three words, an optional comma, and the pre-fix form | the target's: 0 rows red; each mutation: exactly 1 row red, the constructed refusal written for it; the pre-fix form: the 2 subtests rows red |
| The target's regex against lines pytest or its plugins can print: `1 failed, 2 rerun`, `1 passed, 1 warning`, `3 deselected`, `1 xfailed, 1 subtests skipped`, and one formatter-shaped line | the pytest-shaped lines read; the formatter line refused |
| `evidence_check.py --strict` over the scratch clone | `4272 ok · 0 drifted · 0 broken`; the work item's names `0 refused` |
| The broad gate: the full suite, the repository-wide lint and the typecheck at `ae3e5232` | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:2032` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2021` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1964` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1850` | round 1's 🟡 4 — fixed |
| round-1 | `templates/config.md:333` | round 1's 🟡 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1919` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/plan.md:7` | round 1's ⬜ 8 — answered |
| round-1 | `tests/test_the_commit_gate_decides_at_the_commit.py:434` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1841` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1894` | round 1's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:1861` | round 2's 🟡 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:1869` | round 2's ⬜ 2 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2076` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2061` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:1988` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:1852` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `cd` row whose failing path the branch also adds at the root, as a different file, reads `new` unrun though the base fails the file below the `cd` | not filed; already deferred in round 2 as a design change to how absence is decided | the repository owner — whether to file it |
| A file the branch reports only as `ERROR` gets no base comparison | already deferred in round 1 (`spec.md` Out, `overview.md` *Not done*) | the repository owner, as the frame names |

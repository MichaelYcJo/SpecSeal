# Round 3 report — 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base

Target `ae3e5232` on `fix/747-the-broad-gate-re-runs-the-test-command-at-the-base`,
against `release/v0.18.1` at `e141980a`. Reviewed by warden. This is the
verifying round for round 2's fixes, fix range `4e981840..55b40287`
(`542e1122`, `cf441933`, `b2876cdb`, `55b40287`), and `ae3e5232` closes
round 2's record. It is the verifying round of the run's one reopening, so
this record ends the run.

I stayed inside that diff. The one thing I opened outside it is pytest
9.1.1's own `_pytest/terminal.py` and `_pytest/subtests.py`, because the fix
rests its grounds on them. NAME NOT IN TREE

Carried from rounds 1 and 2, not re-established: the coordinates of every
finding, round 2's pytest 9.1.1 measurements of `--no-summary`, `-rN` and a
missing path, and round 1's cargo line. Re-derived here: every verdict.

## What the account claimed, and what was checked

| Claim | Where it is made | What I found | How |
|---|---|---|---|
| A later label may be one or two lowercase words, so pytest 9's subtests line is read as pytest's summary | `skills/verify/scripts/broad_gate.py:1867`, ask 🟡1 | Holds. The gate on a subtests fixture reads `failing on base too` where the base fails the file, and `new` where the base passes it. Round 2's gate gives `new?` in all four runs | **executed** |
| The first label stays one word, because pytest lists its own categories first and every test reports one of its own | the comment at `skills/verify/scripts/broad_gate.py:1859-1866` | The conclusion holds and the stated reason is incomplete. pytest 9.1.1's KNOWN_TYPES itself ends with three two-word categories, so "its own first" alone does not give one word. Finding 1 | **read** (pytest source) and **executed** (the fixture) |
| The narrower first label departs from round 2's proposal at no cost | the ask | Holds. No line pytest 9.1.1 prints after a test has run starts with a two-word label, and the narrower regex refuses one more constructed non-pytest shape | **read** and **executed** |
| Four mutations of the label's shape each go red against the three constructed refusals | ledger row B3, *Executed* | Holds for the three I repeated: a two-word first label, a three-word later label and an optional comma each turn exactly one `SUMMARY_LINES` row red. The pre-fix regex turns both measured subtests rows red | **executed** |
| `NO_RUNNER`'s reason, the `compare_at_base` docstring, the *New?* bullet in `skills/verify/SKILL.md` and rule 3 in `templates/config.md` say the same thing | the fix commits `542e1122`, `cf441933` | Holds. All four now say the gate did not read a summary line, not that none was printed, and the changelog fragment says the same | **read** |

## Round 2's 🟡 1, judged against the departure from the proposal

Round 2 proposed letting every label be one or two words. The fix lets only
a later label be two words, and keeps the first label at one.

The fix rests on pytest's summary order. I read `_pytest/terminal.py` in
pytest 9.1.1:

- `_build_normal_summary_stats_line` walks KNOWN_TYPES in order and then NAME NOT IN TREE
  the plugins' categories in the order they first appeared.
- KNOWN_TYPES is `failed`, `passed`, `skipped`, `deselected`, `xfailed`,
  `xpassed`, `warnings`, `error`, then `subtests passed`, `subtests failed`,
  `subtests skipped`.
- `_pytest/subtests.py` gives a test that holds subtests its own `passed` or
  `failed`. A failed subtest is counted under `failed`, and only a passing
  subtest under `subtests passed`.

So every test that ran puts a count under one of the eight one-word
categories, and those come before every two-word one. The first label is
one word on any run that ran a test. A run that ran none prints
`no tests ran`, which no form of the regex reads. NAME NOT IN TREE

The narrower form is therefore safe in pytest 9.1.1, and it refuses
`2 subtests passed in 0.01s`, which no pytest prints. A pytest that one day
printed a two-word first label would get `new?`, which costs a measurement
and fakes none. I judge the departure sound.

The ask asked for the subtests fixture run end to end, which the fix pass
did not do. I ran it at the target with four shapes: the base failing or
passing the file, and the row runner-first or lint-first. pytest printed
`2 failed, 1 passed, 1 subtests passed in 0.03s` and
`2 passed, 2 subtests passed in 0.01s`. The first label is one word in both,
as the reasoning says. The gate gave `failing on base too` twice and `new`
twice, which is right. The same probe against round 2's gate gave the
`NO_RUNNER` reason all four times.

## Findings

### ⬜ 1 — the regex comment's reason for a one-word first label skips the step that makes it true

The coordinate is `skills/verify/scripts/broad_gate.py:1861-1863`. The
comment says pytest lists its own categories first and a plugin's after, and
every test reports one of its own, so the first label is one word. In pytest
9.1.1 the two-word `subtests passed` is one of pytest's own. It sits in
KNOWN_TYPES too, so "its own first" alone does not give one word.

What makes it true is narrower. The eight one-word categories come before
the three two-word ones, and every test that ran is counted under one of the
eight. The behaviour is right and the test cases pin it. A maintainer who
reads the comment to decide whether a new pytest category breaks the rule
would be reading the wrong reason, so this is ⬜. NAME NOT IN TREE

A wording that states the step:

```python
# (round 2's 🟡 1). pytest walks `KNOWN_TYPES` in `_pytest/terminal.py` in
# order, then a plugin's categories: the eight one-word ones (`failed`,
# `passed`, ... `error`) come before its own two-word `subtests …` ones, and
# every test that ran is counted under one of the eight, so the first label
# is one word and a later one is one lowercase word or two.
```

### ⬜ 2 — ledger row B3 still says `NO_RUNNER` is given where no prefix printed a summary

The coordinate is the first cell of row B3 in
`seal/ledger/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base.md:9`.
It ends "or with `NO_RUNNER` where no prefix printed a summary". The fix pass
changed that wording in the four places round 2 named and in the changelog
fragment, and re-stamped B3's anchors, but left the claim cell on the old
words. A line pytest printed in colour is the case the new words exist for.

This is the run's paperwork, not the tool, so it is a correction: ⬜, and
out of `Needs a fix`. Suggested words for the end of the cell: "or with
`NO_RUNNER` where no prefix printed a line the gate reads as pytest's
summary".

## Round 2's verdicts, answered

- **Finding 1 (subtests).** Closed. The two measured subtests rows are green
  at the target and red under the pre-fix regex. End to end, a subtests file
  the base fails reads `failing on base too`, both runner-first and
  lint-first. The departure from the proposal is sound, with finding 1 above
  on the comment that explains it.
- **Finding 2 (`NO_RUNNER`).** Closed. The reason, the docstring, the skill's
  *New?* bullet, rule 3 and the changelog fragment agree. The reason is
  pinned whole, and the skill's phrase is pinned by
  `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`. I read
  from `4e981840` that the skill's phrase was absent before the fix, so the
  new assert is red there. The ledger's own summary of it is finding 2.

## Round 1's verdicts

Round 2 confirmed all eight closed. This round's fixes touch only finding 1's
unit, the summary regex. The cargo case, the `cd` case, the runner-first and
lint-first cases, `MEASURED_ENDINGS` and the counterfeit pin all pass at the
target, so I carry the other closures forward unchanged.

## Regression tests to plant

None owed. If the owner wants an end-to-end subtests case, the probe above is
the shape: `base_then_feature` with a file that uses the `subtests` fixture,
under `SUITE_ROW`. It needs pytest 9, which this repository's virtualenv
carries.

## Facts for the evidence ledger

- pytest 9.1.1, under `-q`, prints a test that holds a failed subtest as
  `FAILED <file>::<test> - contains 1 failed subtest`, after a
  `SUBFAILED(i=1) <file>::<test>` line, and the summary reads
  `2 failed, 1 passed, 1 subtests passed in 0.03s`. Measured this round.
- In pytest 9.1.1's `_pytest/terminal.py`, KNOWN_TYPES lists the eight
  one-word categories before `subtests passed`, `subtests failed` and
  `subtests skipped`. Read this round. NAME NOT IN TREE

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the comment over the summary regex gives "pytest lists its own categories first" as the reason the first label is one word, where pytest 9.1.1's own list holds three two-word categories; the reason is that the one-word ones come first and every test that ran is counted under one | `skills/verify/scripts/broad_gate.py:1861` | open | read: pytest 9.1.1's terminal and subtests modules; the behaviour is right and pinned, the stated reason is not the one that holds |
| ⬜ 2 | ledger row B3's claim cell still says `NO_RUNNER` is given where no prefix printed a summary, the wording round 2's finding 2 retired everywhere else | `seal/ledger/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base.md:9` | open | read; a correction to the run's paperwork, not to the tool |
| 🟢 | round 2's finding 1 is closed — pytest 9's subtests summary is read as pytest's | `skills/verify/scripts/broad_gate.py:1867` | confirmed | executed: the subtests fixture end to end at the target gave `failing on base too` where the base fails the file and `new` where it passes, runner-first and lint-first; round 2's gate gave the `NO_RUNNER` reason in all four; the narrower first label is grounded in pytest 9.1.1's summary order |
| 🟢 | round 2's finding 2 is closed — the unmeasured reason says the gate did not read a summary | `skills/verify/scripts/broad_gate.py:1875` | confirmed | read: the reason, the docstring, the skill's bullet, rule 3 and the changelog fragment agree; executed: the pin passes at the target |
| 🟢 | round 1's findings 1 to 8 stay closed | `skills/verify/scripts/broad_gate.py:2006` | confirmed | executed: the cargo, `cd`, runner-first, lint-first, ending and counterfeit cases pass at the target; carried from round 2 for the rest, since this round's diff touches only the summary regex |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `cd` row whose failing path the branch also adds at the root, as a different file, reads `new` unrun though the base fails the file below the `cd` | not filed; already deferred in round 2 as a design change to how absence is decided | the repository owner — whether to file it |
| A file the branch reports only as `ERROR` gets no base comparison | already deferred in round 1 (`spec.md` Out, `overview.md` *Not done*) | the repository owner, as the frame names |

Nothing this round found needs a fix, so the broad gate has come due. The
next act is the sealer's spawn at `ae3e5232`, or at whatever SHA lands the
two ⬜ answers.

Needs a fix: no
Loses a record or crashes: no

## Proof

Files opened this round: `skills/verify/scripts/broad_gate.py` (the fix
diff, lines 1855-1885 and 2006-2030 through it),
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the fix diff, the
helpers `gate_module`, `run_gate`, `base_then_feature`, `verdict_of`, and the
cases from `SUMMARY_LINES` to `test_a_runner_first_row_runs_once_at_the_base`),
`skills/verify/SKILL.md` and `templates/config.md` through the diff, the
ledger fragment's diff in `55b40287` and its row B3, the changelog
fragment's diff, `bin/test`, the work item's `rounds/round-2.md` and
`rounds/round-2-report.md`, the README and agent lines that name `new?`, and
pytest 9.1.1's terminal and subtests modules in the worktree's virtualenv.
The asked paragraph for this round, from the orchestrator's scratchpad.

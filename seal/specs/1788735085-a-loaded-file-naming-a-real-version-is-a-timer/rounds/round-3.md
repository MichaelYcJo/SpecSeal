# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — review round 3

| Field | Value |
|---|---|
| Target SHA | 6396c2145f08c3fd69c40c7586a2454e4ae10241 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 201 |
| Broad gate | not yet |
| Fixes checked by | round-4 |
| Contract changes | none |
| New units | test_the_refusal_names_the_line_and_the_version_it_refused (depth 1) |
| Needs a fix | yes — finding 7 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the verifying round for round 2's six fixes, spawned against
`6396c21` with the fix diff `a48d27f..7349afc`.

The prompt led with one axis rather than the table, and named why: **a case
that cannot observe what its own guard removes** had produced a finding in
three consecutive passes and four times in total — round 1's `(?![\w.])`, round
2's `(?!\w)` with no case behind it, and the three the round-2 fix pass found
by mutating its own work. The round was told to assume a fifth instance and go
looking, and to put every case in the fix diff to that question.

It carried the owner's decision on the 3+ Fix Rule as settled and not to be
reopened — a prerelease of an unshipped version is a timer, so `(?!\w)` was
removed rather than narrowed — and asked only whether it was implemented.

It also carried the orchestrator's own re-execution of eight inputs at
`6396c21`, with two rows flagged for a second look rather than a tick:
`v0.9.0rc1` reported as the token `v0.9.0`, and `x0.9.0` allowed by the front
lookbehind.

Four axes: every new case against what it guards; the fix pass's own judgement
call on finding 8's second example, to be checked rather than accepted;
`refusal()` as a new unit, asking what is still unpinned after the extraction;
and the two documents the branch changed, unread since round 1 while the
check's behaviour changed three times.

Because the round sits at three of a cap of five, it was also asked to say
which of its own findings it would ship without.

The answer to the leading axis is that the class is closed in the regex and
has moved one unit sideways, into the extraction round 2 commissioned.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | round 2 finding 4 — the comment above `VERSION_TOKEN` stated disproven grounds | `tests/test_release_hygiene.py:52-68` | answered | read: the comment now states `\d+`'s greed and the prerelease decision, and agrees with the module's own comment at `:591-594` |
| 2 | round 2 finding 5 — `(?!\w)` hid a letter-suffixed prerelease | `tests/test_release_hygiene.py:68` and `:591-600` | answered | executed at running `0.9.0`: `0.9.0rc1` answers `[(1, '0.9.0')]`, `v0.9.0rc1` answers `[(1, 'v0.9.0')]`, `0.9.0-rc1` refused. `0.9.0.1`, `2.0.1.5` and `v1.2.30` unchanged |
| 3 | round 2 finding 6 — the printed token could not take the other-product route | `tests/test_release_hygiene.py:175-179` and `:517-539` | answered | executed: removing either arm turns `test_the_declared_token_is_the_one_the_refusal_printed` red, so both are pinned where round 2 found neither was |
| 4 | round 2 finding 7 — the message was inline in the `assert`, so detaching it left every case green | `tests/test_release_hygiene.py:212-227` and `:270-273` | answered | executed: replacing `+ what_to_write_instead()` with a literal turns the routes case red. What the extraction left unpinned is finding 7 below |
| 5 | round 2 finding 8 — `RECORDS_OF_A_MOMENT` was order-dependent | `tests/test_release_hygiene.py:127-144` and `:439-460` | answered | executed: reverting to the early-return loop turns the new case red |
| 6 | round 2 finding 9 — `DATED_RECORD`'s shape was unpinned | `tests/test_release_hygiene.py:124` and `:504-514` | answered | executed: the trailing `-`, the fully loosened widths and a partly loosened `\d{2,4}-\d{1,2}-\d{1,2}-` all turn the case red. Both mutations round 2 recorded as surviving are now caught |
| 7 | 🟡 no case observes `refusal()`'s offender lines, running version or explanatory paragraph, and the docstring and ledger R3 record the opposite as a measured fact | `tests/test_release_hygiene.py:210-225`, `:248-251`, the fragment's R3 notes | **fixed** `dcbb4e8` | fixed at dcbb4e8 — ``; executed: each of the three deleted on its own leaves 30 passed. `refusal` and `what_to_write_instead` are referenced nowhere outside this module. Same class as round 2's finding 7 |
| 8 | ⬜ the case pinning `x0.9.0` as allowed carries no argument for it, and `V0.9.0` is invisible to the check | `tests/test_release_hygiene.py:578-590` and `:68` | **fixed** `632260c` | fixed at 632260c — ``; executed: dropping the `\w` half adds 0 offenders to the loaded tree and no word-glued token exists there; `V0.9.0` answers `[]` and the loaded set holds no uppercase spelling |
| 9 | ⬜ the docstring's narrower-prefix example changes no answer in either implementation | `tests/test_release_hygiene.py:443-445` and `:131-132` | **fixed** `672a127` | fixed at 672a127 — ``; executed: four arrangements through `any()` and the early-return loop; only the exact-path entry differs |
| 10 | ⬜ a document states the check refuses a version whether it has shipped or is ahead, where it refuses at or above the running one | `docs/issues-and-milestones.md:63-67` | **fixed** `4be419c` | fixed at 4be419c — ``; read: line 160 of the same file is the counterexample, and `docs/release-checklist.md:80` states it correctly |
| 11 | ✅ the blind-case class is closed in this diff — all five new cases observe their own guard | the five cases in `a48d27f..7349afc` | answered | executed: 15 mutations, 12 caught. Two survivors are finding 7; the third is `DATED_RECORD`'s `^`, which the code already records at `:495-498` as redundant beside `.match()` |
| 12 | ✅ the ledger fragment's rows all resolve, unscoped | `seal/ledger/1788735085-a-loaded-file-naming-a-real-version-is-a-timer.md` | answered | executed `./bin/evidence-check .` with no narrowing: 719 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0. The fragment carries 17 anchors, one more than round 2 |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py -q` at `6396c21`, fresh `--no-local` clone | 30 passed, exit 0 |
| a 15-mutation matrix, one at a time, `tests/__pycache__` cleared between | 12 caught, 3 survived — `refusal()` losing the offender lines, the `{running}` interpolation, and the explanatory paragraph |
| `DATED_RECORD`'s `^` alone removed | survived, and the code already records at `:495-498` that it is redundant beside `.match()` |
| repository-wide references to `refusal` and `what_to_write_instead` | none outside this module, so nothing else pins them |
| the loaded set re-enumerated with the lookbehind's `\w` half removed | 0 new offenders |
| word-glued version-shaped tokens across the loaded set | none in substance — `release/v0.3.0` is preceded by `/` and already read |
| 20 token shapes through `timers_in` at running `0.9.0` and `0.8.3` | matches the orchestrator's table row for row; `V0.9.0`, `X0.9.0`, `SpecSeal0.9.0`, `py0.9.0` and `...0.9.0` all answer `[]` |
| `any()` beside the early-return loop over four entry arrangements | only the exact-path entry differs |
| the real refusal text printed for `v0.9.0rc1` | `docs/x.md:1 names v0.9.0` — the line number is there, so a person can reach the source. Not round 2 finding 6's wall |
| `./bin/evidence-check .` unscoped | 719 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |
| the branch's two changed documents re-read against `origin/release/v0.9.0...6396c21` | `docs/release-checklist.md:80` correct; `docs/issues-and-milestones.md:63-67` is finding 10 |
| `git grep -E 'V[0-9]+\.[0-9]+\.[0-9]+'` over the loaded set | 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_release_hygiene.py:56` | round 1's 1 — fixed |
| round-1 | `tests/test_release_hygiene.py:82` and `:102-107` | round 1's 2 — fixed |
| round-1 | `tests/test_release_hygiene.py:196-215` | round 1's 3 — fixed |
| round-1 | `62287e9` and `86a6e20` | round 1's 4 — answered |
| round-1 | `tests/test_the_pull_request_language_is_the_repositorys.py:764-786`, `seal/ledger.md:562`, `rounds/round-5.md:68,80` | round 1's 5 — answered |
| round-1 | `seal/ledger.md:550,562` | round 1's 6 — answered |
| round-1 | the nine `LOADED` prefixes at `579a916` | round 1's 7 — answered |
| round-2 | `tests/test_release_hygiene.py:58` | round 2's 1 — answered |
| round-2 | `tests/test_release_hygiene.py:114-125` | round 2's 2 — answered |
| round-2 | `tests/test_release_hygiene.py:159-183` | round 2's 3 — answered |
| round-2 | `tests/test_release_hygiene.py:52-58` | round 2's 4 — fixed |
| round-2 | `tests/test_release_hygiene.py:58` and `:476-482` | round 2's 5 — fixed |
| round-2 | `tests/test_release_hygiene.py:152` and `:170-171` | round 2's 6 — fixed |
| round-2 | `tests/test_release_hygiene.py:196-206` and the fragment's R3 notes | round 2's 7 — fixed |
| round-2 | `tests/test_release_hygiene.py:117-125` | round 2's 8 — fixed |
| round-2 | `tests/test_release_hygiene.py:114` | round 2's 9 — fixed |
| round-2 | `rounds/round-1.md:9,50-52` | round 2's 10 — answered |
| round-2 | `docs/review-handoff-protocol.md:124`, `tests/test_release_hygiene.py:117` | round 2's 11 — answered |
| round-2 | `seal/ledger/1788735085-a-loaded-file-naming-a-real-version-is-a-timer.md` | round 2's 12 — answered |
| round-2 | the nine `LOADED` prefixes at `27c36fe` | round 2's 13 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `Contract changes` reads `none` for a unit whose meaning changed | #194, already open and listed at `docs/flow.md:55`; round 2 deferred it and this round sees the same state | the session that takes #194 — not this branch |

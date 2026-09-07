# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — review round 4

| Field | Value |
|---|---|
| Target SHA | 7091b7cfc1ab268a963d3ea4ec0cb09798d92d29 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 201 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 5 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 4, the verifying round for round 3's four fixes, spawned against
`7091b7c` with the fix diff `e7cb019..4be419c`.

The prompt led with the run's dominant class rather than with the table: **a
case that cannot observe what its own guard removes**, six instances across
three rounds, each time one unit sideways from where the last fix landed. It
named the sixth explicitly — the round-3 fix pass found, by mutating its own
work, that deleting the separator between offender lines survived, because a
case passing a single offender cannot render a separator — and told the round
to assume a seventh.

It carried the orchestrator's own re-execution at `7091b7c` and **one
correction to what the fix pass had reported**: the module is 31 cases, not the
33 the pass claimed, counted twice with the cache cleared and agreed by
`--collect-only` and by `grep -c '^def test_'`. The figure had reached no
durable record. The round was told to take 31 and to treat the miscount as an
axis rather than a one-off, because this run had by then produced a false limit
in a ledger row twice and a false count once, all in records written by the
party that had just done the work.

One residual was declared open and not to be re-raised: `assert not offenders,
refusal(...)` handed a literal leaves every case green. The round-3 fix pass had
stopped calling it unpinnable and recorded it as the one survivor of six, with
a rule beside it — what is absent from the measured list is UNMEASURED, not
unpinnable. The round was asked to judge whether that corrected sentence is
true rather than to reopen the residual.

Five axes: every case the fix diff touched, against what it guards; figures and
claims in records checked against the tree rather than read; `[vV]?` as the
answer to the uppercase hole, and what it now admits; finding 9's repair, which
deliberately added no case; and the two documents, whose subject has changed
behaviour four times since round 1.

At four of a cap of five, the round was asked to say which findings it would
ship without and which single one it would spend the last round on.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | round 3 finding 7 — nothing observed `refusal`'s offender lines, running version or explanatory paragraph | `tests/test_release_hygiene.py:293-324` | answered | executed: all five mutations the record lists turn the new case or the routes case red, and the listed survivor survives. The residual sentence is true as written |
| 2 | round 3 finding 8 — `V0.9.0` invisible and `x0.9.0` unargued | `tests/test_release_hygiene.py:78`, `:636-662` | answered | executed: 22 token shapes at running `0.8.3`; `V0.9.0` refused, nine word-glued and dot-glued shapes allowed. Across 64 loaded files, 0 lines where `[vV]?` differs from `v?`, 0 offenders. All four lookbehind and prefix mutations turn a case red |
| 3 | round 3 finding 9 — the docstring's narrower-prefix example | `tests/test_release_hygiene.py:490-505`, `:138-144` | answered | executed: four arrangements over five paths through both implementations; only the exact-path-after-prefix cell differs, and it is already asserted |
| 4 | round 3 finding 10 — the tracker document's scope sentence | `docs/issues-and-milestones.md:63-70` | answered | read: all three documents naming the check agree with the current behaviour |
| 5 | 🟡 the separator before the FIRST offender line is unobserved; deleting it leaves all 31 cases green, and the case's own next assertion refuses the same defect for the second offender | `tests/test_release_hygiene.py:309-312` against `:233` | open | executed: one mutation at a time, cache cleared — 31 passed, exit 0. Instance seven of the blind-case class, the first inside the unit built to close it |
| 6 | ⬜ a ledger row credits itself with cases it does not name — *the 58 cases the row names*, where the row names four | `seal/ledger.md:1137` | open | executed: the two modules the four anchors sit in report 58 passed. The row's own earlier sentence keeps the two figures apart correctly |
| 7 | ⬜ the lookbehind's newly written argument covers the `\w` half and not the `.` half, which a case two lines above pins | `tests/test_release_hygiene.py:70-77` | open | executed: `(?<!\w)` in place of `(?<![\w.])` turns `test_a_number_that_is_not_a_version_is_not_read_as_one` red on `1.9.9.9` |
| 8 | ⬜ `as_release` cannot parse a token `VERSION_TOKEN` now produces | `tests/test_release_hygiene.py:119-121` | open | executed: `as_release("V0.9.0")` raises `ValueError`. No live call site reaches it |
| 9 | ✅ the ledger fragment resolves unscoped and carries the two anchors this pass added | `seal/ledger/1788735085-a-loaded-file-naming-a-real-version-is-a-timer.md` | answered | executed `./bin/evidence-check .` unscoped: 721 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0. 19 anchors, two more than round 3 |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py -q` at `7091b7c`, fresh `--no-local` clone | 31 passed, exit 0 — `--collect-only` and `grep -c '^def test_'` agree |
| a 13-mutation matrix over `refusal` and `VERSION_TOKEN`, one at a time, cache cleared between | 11 caught, 2 survived — the `assert` handed a literal (the known residual) and the separator before the first offender line |
| the six mutations the round-3 record lists, re-run independently | five caught, one survivor — the list is exact |
| all 64 loaded files enumerated under `v?` and under `[vV]?`, token set compared per line | 0 lines differ; 0 offenders at running `0.8.3` |
| 22 token shapes through `timers_in` at running `0.8.3` | `V0.9.0`, `-V0.9.0`, `*V0.9.0*`, backticked, parenthesised, `/V0.9.0`, `$V0.9.0`, `V0.9.0rc1` refused; `x0.9.0`, `X0.9.0`, `PyV0.9.0`, `aV0.9.0`, `MPEGV0.9.0`, `IV0.9.0`, `VV0.9.0`, `V.0.9.0`, `V0.9.0.1`, `py3.13.9`, `1.9.9.9`, `V1.2.3` allowed |
| `as_release("V0.9.0")` | raises `ValueError` |
| four `RECORDS_OF_A_MOMENT` arrangements over five paths, through `any()` and the early-return loop | only the exact-path-after-prefix cell differs, in one of twenty rows |
| the two modules G5's four anchors sit in | 58 passed, exit 0 |
| `uvx ruff check` and `format --check`, scoped to the one changed Python file | passed — not the repository-wide run |
| `./bin/evidence-check .` unscoped | 721 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |
| `git grep` for `33 passed` across the tree | one hit, a different work item's own true figure |
| `git grep` for every document naming the check | three, all agreeing with current behaviour |
| `git merge-base --is-ancestor 6396c21 7091b7c` | true |

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
| round-3 | `tests/test_release_hygiene.py:52-68` | round 3's 1 — answered |
| round-3 | `tests/test_release_hygiene.py:68` and `:591-600` | round 3's 2 — answered |
| round-3 | `tests/test_release_hygiene.py:175-179` and `:517-539` | round 3's 3 — answered |
| round-3 | `tests/test_release_hygiene.py:212-227` and `:270-273` | round 3's 4 — answered |
| round-3 | `tests/test_release_hygiene.py:127-144` and `:439-460` | round 3's 5 — answered |
| round-3 | `tests/test_release_hygiene.py:124` and `:504-514` | round 3's 6 — answered |
| round-3 | `tests/test_release_hygiene.py:210-225`, `:248-251`, the fragment's R3 notes | round 3's 7 — fixed |
| round-3 | `tests/test_release_hygiene.py:578-590` and `:68` | round 3's 8 — fixed |
| round-3 | `tests/test_release_hygiene.py:443-445` and `:131-132` | round 3's 9 — fixed |
| round-3 | `docs/issues-and-milestones.md:63-67` | round 3's 10 — fixed |
| round-3 | the five cases in `a48d27f..7349afc` | round 3's 11 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `Contract changes` reads `none` for a unit whose meaning changed | #194, open and listed at `docs/flow.md:55` | the session that takes #194 — not this branch |
| the empty inline code span in a `fixed at <sha>` grounds cell | the `# RIDER:` at `skills/code-review/scripts/round_record.py:1283-1295`, which owns the repair | the session that takes that rider — it predates this branch |

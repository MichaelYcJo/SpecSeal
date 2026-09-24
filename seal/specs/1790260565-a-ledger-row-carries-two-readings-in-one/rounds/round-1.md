# 1790260565-a-ledger-row-carries-two-readings-in-one — review round 1

| Field | Value |
|---|---|
| Target SHA | 59012e5d6b9a3a6c17481cc4ca47a117434b8b83 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 588 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790260565 reviews the build at 59012e5d against spec.md and plan.md (frame 04ad1e6c): the rows carrying two readings (#568), the header-less row count (#501), and the ledger rules' newer clauses (#569). The classes enumerated are every row in every ledger file carrying a second reading or an overflow cell, every row shape overwide_rows still does not count, and every sentence of the edit and conflict rules the needles do not hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The halves rule's union clause, the edit rule's re-stamp and removal outcomes, and the two arguments behind them are held by no needle, although #569 pinned their neighbours | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | open | Needle counts in the three carriers (executed). *only the notes are a union* is in all three exactly once, so a needle for it goes in green |
| ⬜ 2 | The unit case's comment says a corpus case that stops passing the width goes red, but reverting the call site to `overwide_rows` keeps every case green | `tests/test_release_hygiene.py:1296` | open | Executed a mutation at `tests/test_release_hygiene.py:1325`: 3 passed |
| ⬜ 3 | Shapes still uncounted: an indented row, a row in a `~~~` or indented fence, a trailing `\|`, a header wider than the template | `tests/test_release_hygiene.py:1255` | open | None is in any ledger file at 59012e5d (executed). The fence and trailing-pipe shapes are already in the spec's *Out* |
| ⬜ 4 | Correction: the plan's approval line carries a second sentence after *was spawned.*, so the approval regex misses it and the chain check reports the line absent | `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5` | open | Executed a dry run of `round_record.py new` in the clone. `APPROVED_RE` at `skills/code-review/scripts/chain_check.py:3806` is anchored at the end of the line. Reported, not refused |
| 🟢 | #568 — S4 and G5 are lossless unions of one merge's two sides under one Checked date, and the eleven-modules row's Notes is joined | `seal/releases/0.9.2.md:31`, `seal/releases/0.8.2.md:145`, `seal/releases/0.9.3.md` | confirmed | Byte comparison of each side's opening, marker multisets before and after, and no two-date row left in any ledger file (executed) |
| 🟢 | S4's claim is corrected to carry the tagged half | `seal/releases/0.9.2.md:31` | confirmed | `docs/issues-and-milestones.md:129-131` (read) |
| 🟢 | #501 — a row under no header is counted against the template's five columns, and the policy paragraph and C2 say so | `tests/test_release_hygiene.py:1233` | confirmed | Unit case seen red against the header-only function and green after; corpus green over 769 rows (executed) |
| 🟢 | #569 ⬜ 1 — the three needles and the owner's third-outcome assertion pin the clauses #567's review added | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | confirmed | Each needle occurs once per guide, and the owner has its own assertion (executed) |
| 🟢 | #569 ⬜ 2 — the spec's exception names the direction `chain_check.py` names, and a case holds both statements to it | `docs/round-record-spec.md:542` | confirmed | New case red against the base paragraph and green at target (executed) |
| 🟢 | No drifted or broken anchor anywhere in the ledger, and the survivor sweep is fully exempted | `seal/` | confirmed | `bin/evidence-check .` 2062 ok, 0 drifted. `bin/survivor-check` with the exemption file exits 0 (executed) |

## Paste-ready fixes

```python
    # #509: of a conflicted row only the notes are a union; the hash is the
    # side's that edited the unit and neither side's where both did, and the
    # row the checker names is re-read against every edit the merge carries.
    "only the notes are a union",
    "the side that edited the anchored unit",
    "to neither side where both did",
    "re-read against every edit the merged unit carries",
    "run `evidence-check` after the resolution",
)

# The owner of the two rules the needles above end with. The guides carry
# them and link here; the policy document states them first (#488, #509).
OWNED_SENTENCES = CONFLICT_SENTENCES[-8:]
```
```python
    # `ledger_overwide` is what the corpus case calls, so a width dropped
    # inside it goes red here. A corpus case that stops calling it does not:
    # no row in the tree is overwide, so the corpus alone stays green.
    assert ledger_overwide(fragment) == [(1, 5, 6)]
```
```
Approved 2026-09-24 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

Q1 builds on its default (a) and is filed for the owner as #585.
```

## Executed probes

| What was run | Result |
|---|---|
| A probe (named with the `test_tmp_` prefix, run once, deleted) over `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` at 59012e5d: rows with a `\|` outside a code span or an escaped date pair; `ledger_overwide` over every file; rows under no header; indented or `~~~`-fenced rows; marker multisets of every changed row before and after; the eleven-modules row at `31937b9f` | one `\|` row (`0.11.5.md:28`, a single reading); no overwide row; 769 body rows, 27 under no header; no indented or `~~~` rows; no marker lost; 7 cells at `31937b9f` |
| Rows with more than one bare date cell, splitting on every pipe, at `31937b9f`, c52e8350 and 59012e5d | 2 (G5, S4), then 2, then 0 |
| Byte comparison of the second opening against the first in G5 and S4 | shared opening identical, and the new Notes cell is the first side whole plus the second side's remainder |
| `bin/test -q tests/test_release_hygiene.py -k "ledger or pipe or header or width"` | 6 passed, exit 0 |
| `bin/test -q tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_a_record_precedes_the_fixes_it_commissions.py tests/test_a_folded_statement_names_what_enforces_it.py tests/test_a_document_has_room_for_the_next_fold.py` | 139 passed, exit 0 |
| `bin/test -q tests/test_no_real_identifiers.py tests/test_unverified_rows_close.py` | 151 passed, exit 0 |
| Mutation: base `docs/round-record-spec.md`, then the phase-4 case | red, *does not name the direction chain_check.py's other refusals take*; file restored |
| Mutation: the width reset to `None` in `overwide_rows`, then the unit case | red, `assert [] == [(1, 5, 6)]`; file restored |
| Mutation: the corpus case calls `overwide_rows` instead of `ledger_overwide` | green, 3 passed: this is ⬜ 2; file restored |
| Needle counts in `CLAUDE.md`, `CONTRIBUTING.md` and `docs/the-evidence-ledger.md`, whitespace collapsed | each new needle occurs once per guide; `` `Corrected <date>` note `` occurs twice in the owner; *only the notes are a union* occurs once in each and is not a needle |
| `bin/evidence-check --ledger` over the five touched release files and the fragment, lenient | 544 ok, 0 drifted, 0 broken |
| `bin/evidence-check .` | 2062 ok, 0 drifted, 0 broken; records 35 names read, 0 refused |
| `bin/correction-check --range c52e8350...59012e5d` | no merge commit in the range, exit 0 |
| `bin/survivor-check --range c52e8350...59012e5d --exempt seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/survivors.md` | every survivor excused (14), exit 0 |
| `round_record.py new` on this report, run as a dry run in the clone and discarded | the tables parse; `Needs a fix` and `Loses a record or crashes` both read `no`; the chain check reports the plan's approval line absent, which is ⬜ 4 |
| The broad gate: full suite, lint and format over the finished branch | not yet: it has not been run, and it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The fence toggle in `overwide_rows` misses `~~~` and indented fences (part of ⬜ 3) | spec *Out*: the #444 chain's fence helper, adopted here after it lands | the orchestrator, when it sequences #444 against this branch |
| The cell count as a shipped refusal for consumer repositories | `questions.md` Q1 → #585 | the owner |

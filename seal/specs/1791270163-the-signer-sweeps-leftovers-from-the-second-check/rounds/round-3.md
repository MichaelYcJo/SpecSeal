# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — review round 3

| Field | Value |
|---|---|
| Target SHA | eea27ad0bf1d4fd7c6be96c1cfcbfc04b989ea44 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #843 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `eea27ad0bf1d4fd7c6be96c1cfcbfc04b989ea44..eea27ad0bf1d4fd7c6be96c1cfcbfc04b989ea44`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the verifying round for round 2's fixes at `f649a21b..e3c9bc9d`, and the last round of the run: round 2 recorded the run's first fix of a fix and `round-record` said the reopening was spent. The reviewer was asked to open both fixes, inherit rounds 1 and 2, and judge the rest of `origin/release/v0.20.0..eea27ad0` without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the changed test file and the two changed test modules (2671 passed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The fix's inserted sentences left `continuation line stays inside,` as a short docstring line of its own, unreflowed | `tests/test_one_word_one_meaning.py:741` | deferred #844 | #844 — the run is capped; a cosmetic docstring wrap; read: the line and its neighbours; cosmetic, the behaviour and the stated facts are right, so it is not counted in `Needs a fix` |
| 🟢 | round 2's yellow 1 is closed — a list item starting at 1 with leading zeros ends the span | `tests/test_one_word_one_meaning.py:753` | confirmed | executed: nineteen plants through the span function at f649a21b and eea27ad0 and through cmark-gfm; eight zero-padded starts at 1 green before and red after; ten shapes cmark-gfm keeps in the paragraph green both times; all nineteen agree with cmark-gfm at HEAD; the unplanted file green; `tests/test_one_word_one_meaning.py`, 21 passed |
| 🟢 | round 2's white 2 is closed — the overview's survivor row states the tool's result | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:26` | confirmed | executed: `survivor-check` over `5bc0a48f..149ef480` exits 1 with three places, and exits 0 with `--exempt` pointing at `survivors.md`, as the row now says |
| 🟢 | round 2's fix pass excused its one survivor with true grounds | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/survivors.md:24` | confirmed | executed: `survivor-check` over `f649a21b..e3c9bc9d` names only `spec.md:173` of another work item, exit 1, and exits 0 with `--exempt`; read: the quote is the tool's own clean-run line at `skills/code-review/scripts/survivor_check.py:2197` |
| 🟢 | R6's re-read row is at the fixed unit's hash and names the zero-padded plants | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | confirmed | executed: `evidence-check --ledger` on the fragment, `--strict`, exit 0, 21 ok; the plants it names behave as it says |
| 🟢 | round 1's yellow 1 stays closed for the table and the footnote definition | `tests/test_one_word_one_meaning.py:757` | confirmed | read: the fix changed only the list alternative, and the table, footnote and break alternatives are byte for byte as round 2 executed them |
| 🟢 | round 1's whites 3, 4 and 5 stay closed or answered | `tests/test_a_signer_declares_its_pact.py:1292` | confirmed | read: no file those three name, other than the overview row above, is in round 2's fix range, so round 2's grounds stand; carried, not re-run |

## Paste-ready fixes

```python
    line over a delimiter row (#831). An ordered list interrupts a paragraph
    only when it starts at 1, and cmark reads a start number of at most nine
    digits, so `1.`, `01.` and `000000001)` end the span while `02.` and a
    ten-digit `0000000001.` stay in the paragraph (round 2 of #831). A lazy
    continuation line stays inside, and so does a pipe line over a `---` with
    no pipe in it, which GFM makes part of the statement's setext heading. The
    delimiter's cell count is not matched against the header's, so the end
    errs toward sweeping more. The cut is made before flattening, which is
    what would erase the blank line."""
```

## Executed probes

| What was run | Result |
|---|---|
| a deleted probe: nineteen list-marker plants directly under the statement's last line, each through the span function taken from f649a21b and from eea27ad0, and the statement's paragraph plus the plant through cmark-gfm | all nineteen agree with cmark-gfm at HEAD; `01.`, `001)`, `000000001.`, `00000001)`, ` 01.`, `   001)` and `01.` with a tab green before and red after; `1.` and `1)` red both times; `0000000001.`, `02.`, `10.`, `00.`, `0.`, `011.`, `001 .`, `    01.`, `01.signatory` and `01)signatory` green both times; the unplanted file green at HEAD |
| `bin/test tests/test_one_word_one_meaning.py -q -n auto` in the clone at eea27ad0 | exit 0, 21 passed |
| `bin/survivor-check --range f649a21b..e3c9bc9d`, then with `--exempt` pointing at `survivors.md` | exit 1, one place, `seal/specs/1790260564-a-moved-file-counts-as-written/spec.md:173`; then exit 0, one excused |
| `bin/survivor-check --range 5bc0a48f..149ef480`, then with `--exempt` pointing at `survivors.md` | exit 1, three places; then exit 0, three excused |
| `bin/evidence-check --ledger` on this item's fragment, `--strict` | exit 0; 21 ok · 0 drifted · 0 broken |
| `bin/round-record new` over this report in the clone, `--baseline a9d7b0e5`, then the clone reset | see the line under this table |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet; this round ran none of it, and the sealer answers it once, next |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_one_word_one_meaning.py:737` | round 1's 🟡 1 — fixed |
| round-1 | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:3` | round 1's ⬜ 2 — fixed |
| round-1 | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:24` | round 1's ⬜ 3 — fixed |
| round-1 | `tests/test_a_signer_declares_its_pact.py:1257` | round 1's ⬜ 4 — fixed |
| round-1 | `hooks/config.py:1350` | round 1's ⬜ 5 — answered |
| round-1 | `tests/test_a_signer_declares_its_pact.py:1278` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:1369` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md:2` | round 1's 🟢 — confirmed |
| round-2 | `tests/test_one_word_one_meaning.py:749` | round 2's 🟡 1 — fixed |
| round-2 | `seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/overview.md:26` | round 2's ⬜ 2 — fixed |
| round-2 | `tests/test_one_word_one_meaning.py:753` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_signer_declares_its_pact.py:1292` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

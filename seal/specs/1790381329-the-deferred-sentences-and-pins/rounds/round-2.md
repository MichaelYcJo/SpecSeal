# 1790381329-the-deferred-sentences-and-pins — review round 2

| Field | Value |
|---|---|
| Target SHA | a6f836c18a08e7d2512b1454482c38ad74cc0b79 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 623 |
| Broad gate | e63d552a against 47e32d57 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790381329 is the verifying round. It opens round 1's fixes, `e195cf09..fd22baee`, at a6f836c1. The classes are every purpose sentence each loader prints against the file it names, every twin of #613's and #616's sentences by meaning in English and Korean, every exit-2 path of `seal.py` and `payload_meter.py` against their descriptions, and the one unit the fix pass added.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's yellow finding 1 is closed — `HOOK_PURPOSES` says `hooks/config.py` reads `config.md`, and every loader's purpose sentence matches its file | `skills/implement/scripts/seal.py:104` | confirmed | executed: M1 and M2 each red on the second `seal.py` row; read: nine loaders enumerated by construction, every sentence checked against the names used |
| 🟢 | round 1's yellow finding 2 is closed — `test_the_baseline_help_names_both_places` reads the `--baseline` help alone and is pinned | `tests/test_unverified_rows_close.py:1283` | confirmed | executed: M3 and M4 each red on the new case, the documents case green under M3; anchored in C3 |
| 🟢 | round 1's finding 3 is closed at its three coordinates | `tests/test_the_fixes_close_the_record.py:469` | confirmed | read; the *before #598* clause checked against history; the class's fourth member is ⬜ 1 below |
| 🟢 | round 1's finding 4 is closed, example and class | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:216` | confirmed | read; tree-wide search in English and Korean, three expansion sentences, all bounded |
| 🟢 | round 1's finding 5 is closed — no count, and the three unheld loaders are the complete set | `tests/test_a_script_copied_alone_exits_2.py:3` | confirmed | read; nine loaders under `skills/` by construction |
| 🟢 | round 1's finding 6 is closed — both exit-code lines name every exit-2 path | `skills/implement/scripts/seal.py:77` | confirmed | read; `seal.py` three paths, `payload_meter.py` three paths |
| 🟢 | round 1's finding 7 is closed — A2's note concerns what A2 cites | `seal/releases/0.15.3.md:60` | confirmed | read; `survivor-check` places recorded in `survivors.md` |
| 🟢 | the fix pass's ledger notes say what the code does | `seal/ledger/1790381329-the-deferred-sentences-and-pins.md:3` | confirmed | read C1, C2, C3, C5 and three release re-reads; `evidence-check` 2407 ok / 0 drifted / 0 broken |
| ⬜ 1 | a test comment says a draft `close` exits 1 on the `Pass`-beside-`nobody` notice; it exits 0 | `tests/test_the_fixes_close_the_record.py:2323` | deferred #625 | executed: `code == 0` held for all three parameters; a twin of round 1's finding 3, first bullet |
| ⬜ 2 | the fix pass's docstring rewrap left three ragged lines | `tests/test_a_script_copied_alone_exits_2.py:9` | deferred #625 | read; also `tests/test_the_fixes_close_the_record.py:472`, `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:219` |
| ❓ | where `cmd.exe` resumes scanning after an undefined `%NAME%` | `skills/verify/scripts/broad_gate.py:1284` | ❓ out of verified scope | carried from round 1; macOS only; a Windows run of `cmd.exe`, by whoever next changes the broad gate's `cmd.exe` path |

## Paste-ready fixes

```python
    # 0 or 1 because the exit is not what this case judges. Judged as a
    # draft, as `round_record.run_check` tells the check on a local run,
    # `Pass` beside `Fixes checked by: nobody` prints and `close` exits 0; at
    # a ready pull request the pair is refused and it exits 1, which is what
    # #427's own reproduction reported before #598. The refusal below is
    # exit 2.
    code, out, _first = close(repo, 1, table, f"{a}..{b}")
    assert code in (0, 1), out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the five touched test modules (copied-alone, fixes-close-the-record, gate, rules-have-one-owner, unverified), at `a6f836c1` | exit 0: 440 passed, 1 skipped |
| `ruff check` and `ruff format --check` on the seven touched Python files | exit 0 both: all checks passed, 7 files already formatted |
| `evidence_check.py .` at `a6f836c1` | exit 0: 2407 ok · 0 drifted · 0 broken |
| `survivor_check.py --range e195cf09...fd22baee` | exit 1: two places, `seal/releases/0.15.3.md:59` and `spec.md:208`, both the rows `fd22baee` added to `survivors.md` |
| `correction_check.py --range e195cf09...a6f836c1` | exit 0 |
| M1: the `config.py` purpose put back to *reads and writes* | copied-alone `seal.py1` red, 7 passed |
| M2: the `config.py` purpose reworded to *it is what writes the root's config.md* | copied-alone `seal.py1` red, 7 passed |
| M3: the tip half dropped from the `--baseline` help only | `test_the_baseline_help_names_both_places` red; the documents case green (9 passed) |
| M4: the fork-point half dropped from the `--baseline` help only | `test_the_baseline_help_names_both_places` red |
| `assert code == 0` put in place of `in (0, 1)` in `test_re_closing_a_half_restored_record_is_refused_for_every_word` | held for all three parameters (⬜ 1); the file restored |
| `unverified_check.py --help` rendered | the tip phrase appears in the `--baseline` help only |
| the broad gate — full suite, repository-wide lint, typecheck | not yet — the sealer's, after the rounds settle; nothing here ran it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/implement/scripts/seal.py:104` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_unverified_rows_close.py:1238` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_the_fixes_close_the_record.py:709` | round 1's ⬜ 3 — fixed |
| round-1 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:217` | round 1's ⬜ 4 — fixed |
| round-1 | `tests/test_a_script_copied_alone_exits_2.py:4` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/implement/scripts/seal.py:77` | round 1's ⬜ 6 — fixed |
| round-1 | `seal/releases/0.15.3.md:60` | round 1's ⬜ 7 — answered |
| round-1 | `skills/implement/scripts/seal.py:112`, `skills/verify/scripts/payload_meter.py:145` | round 1's 🟢 — confirmed |
| round-1 | `skills/settle/SKILL.md:118` | round 1's 🟢 — confirmed |
| round-1 | `docs/one-root-by-lifetime.md:197` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1081` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:250` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.13.0.md:8` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1284` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

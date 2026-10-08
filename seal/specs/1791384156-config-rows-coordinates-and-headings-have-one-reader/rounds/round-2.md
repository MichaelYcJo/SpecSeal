# 1791384156-config-rows-coordinates-and-headings-have-one-reader — review round 2

| Field | Value |
|---|---|
| Target SHA | bb48b1b5acaf3e3c38d1fe7a1215cf0ab82b8038 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 882 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 2 of round 1's fixes: 9f186d2a..105d96ea (8 commits) plus the table and the close, at bb48b1b5. The job was the answers to round 1's verdicts. Round 1's seven new units were a finding surface. The spawn asked which run the Contract changes row named, and whether every caller holds. It also asked whether keeping the 0.20.0 pattern as a test oracle legitimately silences 29 survivors, and whether errors='replace' in read_record lets a corrupted record pass. It asked for plain probes. It also ran the eight guard modules once. Facts arrived labelled. Read from the smith: the 4-of-33 survivor count, the read_record change, the fence-pass count, and the module runs.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Under `--worktree`, `config_at_head`'s notice names the absolute disk path where HEAD names `seal/config.md at HEAD`, and the new case's first-word assertion fails on a path holding a space | `skills/code-review/scripts/chain_check.py:1103` | open | executed: probe calling `pact_notices` in both modes over an undecodable config; read: the case's assertion |
| ⬜ 2 | Under `--worktree`, a directory at `seal/config.md` gives no notice when there is no `seal/pact.md` and no declaration, because `pact_notices` returns before `config_at_head`; K26 says HEAD and `--worktree` alike | `skills/code-review/scripts/chain_check.py:4360` | open | executed: the same tree prints the notice at HEAD and nothing under `--worktree` |
| ⬜ 3 | `survivors.md` attributes all 29 silenced places to `settle.py`'s copy; two matched `rider_check.py`'s removed pattern, one of them the checker's own grammar | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/survivors.md:10` | open | executed: the sweep with the oracle removed names 33, 27 from `settle.py:196` and 2 from `rider_check.py:158`; a correction to a record, outside Needs a fix |
| 🟢 | round 1's blocking finding 1 is closed — the doubled freeze row's case reads the path with `os.sep` as `/` | `tests/test_a_released_row_is_read_again_in_a_fragment.py:861` | confirmed | read at c6e32946; the case passes on macOS (executed); the Windows shards were pending at bb48b1b5, see the question row |
| 🟢 | round 1's blocking finding 2 is closed — the survivor sweep names four places and `survivors.md` excuses each | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/survivors.md` | confirmed | executed: exit 1 with four places, exit 0 with the file exempting; read: the release job passes at bb48b1b5 |
| 🟢 | round 1's yellow 3 is answered — one `Corrected · C1` row replaces the two re-reads and states the exit-2 refusal | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md` | confirmed | read; `bin/evidence-check --strict .` exit 0 and `bin/correction-check` exit 0, executed |
| 🟢 | round 1's yellow 4 is closed — S7 compares `coordinate_paths` with the frozen 0.20.0 pattern | `tests/test_settle_reads_before_it_removes.py:1873` | confirmed | executed: red with `ANCHOR_QUOTED` narrowed and with `settle` altering a path; the `ANCHOR_NAME` mutant is equivalent here, since no released ledger cites a dotted name |
| 🟢 | round 1's yellow 5 is closed — the pact notices read the config through `config_at_head`, and `read_record` no longer raises | `skills/code-review/scripts/chain_check.py:1093` | confirmed | executed: the new case red with `config_at_head` bypassed (2 failed) and with `read_record` strict (1 failed) |
| 🟢 | round 1's yellow 6 is closed — `LOOSE_HEADING` asks `heading_level`, and the grep reads any counted `#` run | `skills/verify/scripts/unverified_check.py:155` | confirmed | executed: the case red with the old pattern put back; read: every other spelling a grep finds is in `HEADING_EXEMPT` or is the rule itself |
| 🟢 | round 1's white 7, 10 and 11 are closed — the twin's docstring, the garbled clause and the memo | `skills/evidence-check/scripts/evidence_check.py:579` | confirmed | read; every caller of `markdown_lines` only reads the list it gets |
| 🟢 | round 1's white 9 is answered — the generic doubled-row sentence is what the spec ordered | `hooks/config.py:977` | confirmed | read against `spec.md` §*Data & interfaces* |
| carried | round 1's white 8, which lines a reader hides before it asks the heading rule | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/spec.md:200` | deferred #872 | already deferred in round 1; `overview.md` §*Not done* now states the sentence's limit (read) |
| 🟢 | The frozen oracle silences only the 29 places round 1 read, and none reads a coordinate | `tests/test_settle_reads_before_it_removes.py:1850` | confirmed | executed: oracle removed, 33 places, the same 33; K14's case still reads every shipped script |
| 🟢 | `errors="replace"` in `read_record` makes `--worktree` read as HEAD already reads, and widens nothing | `skills/code-review/scripts/chain_check.py:1056` | confirmed | read: `git()` decodes with `errors="replace"`; the old raise came after `round_record.py` wrote the record, a crash and not a refusal |
| 🟢 | The `run` in round 1's Contract changes row is the test helper, which gained `*extra`; every caller holds | `tests/test_a_signers_ci_prints_its_pact.py:120` | confirmed | read: every call passes one argument or `*extra`, and no module imports it; the long list is other functions named `run` |
| ❓ | The pytest shards at bb48b1b5, among them the Windows shard round 1's first finding failed on | `tests/test_a_released_row_is_read_again_in_a_fragment.py:861` | ❓ out of verified scope | pending when read; the orchestrator answers it from the CI run at bb48b1b5 |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the prompt named | exit 0, 436 passed |
| `bin/test` over `test_a_signers_ci_prints_its_pact.py`, `test_unverified_rows_close.py`, `test_a_format_has_one_reader.py`, the S7 case and the doubled freeze row's case | exit 0, 218 passed |
| `survivor-check --range d712a632...HEAD`, without and with `survivors.md` exempting | exit 1 with 4 places; exit 0, 4 excused |
| the same sweep after a probe commit that empties `SETTLE_COPY_AT_0_20_0` | exit 1, 33 places: 27 against `settle.py:196`, 2 against `rider_check.py:158`, 4 others |
| S7 with `ANCHOR_QUOTED` narrowed; with `settle` stripping a leading dot; with the dot dropped from `ANCHOR_NAME`; with `/` dropped from `ANCHOR_PATH`'s middle class | red; red; green (no dotted name in the corpus, 0 counted); green (the class after it still takes `/`) |
| the new notice case with `config_at_head` bypassed; with `read_record` strict | 2 failed; 1 failed, 1 passed |
| the `LOOSE_HEADING` case with `^#{2,3}\s` put back | 1 failed, 7 passed |
| probe: `pact_notices` at HEAD and under `--worktree`, over a directory at `seal/config.md` and over an undecodable one, nothing else present | directory: a notice at HEAD, none under `--worktree`; undecodable: a notice in both, the `--worktree` one naming the disk path |
| `bin/evidence-check --strict .` | exit 0 |
| `bin/correction-check --range d712a632...HEAD` | exit 0, no merge commit, no released ledger file changed |
| read, not executed by me: `gh pr checks 882` at bb48b1b5 | release, ledger, lint and both arm-check jobs pass; every pytest shard pending |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_released_row_is_read_again_in_a_fragment.py:859` | round 1's 🔴 1 — fixed |
| round-1 | `.github/workflows/hygiene.yml:262` | round 1's 🔴 2 — fixed |
| round-1 | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md:16` | round 1's 🟡 3 — answered |
| round-1 | `tests/test_settle_reads_before_it_removes.py:1844` | round 1's 🟡 4 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:4320` | round 1's 🟡 5 — fixed |
| round-1 | `tests/test_a_format_has_one_reader.py:75` | round 1's 🟡 6 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3919` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/spec.md:200` | round 1's ⬜ 8 — deferred |
| round-1 | `hooks/config.py:977` | round 1's ⬜ 9 — answered |
| round-1 | `hooks/routing.py:165` | round 1's ⬜ 10 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:713` | round 1's ⬜ 11 — fixed |
| round-1 | `tests/test_the_mode_is_a_row_and_a_command.py:694` | round 1's 🟢 — confirmed |
| round-1 | `hooks/mode-gate.py:164` | round 1's 🟢 — confirmed |
| round-1 | `hooks/routing.py:242` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md:89` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_released_row_is_read_again_in_a_fragment.py:874` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Round 1's white 8: which lines a reader hides before it asks the heading rule | #872, already deferred in round 1 | the repository owner, who triages #872 |

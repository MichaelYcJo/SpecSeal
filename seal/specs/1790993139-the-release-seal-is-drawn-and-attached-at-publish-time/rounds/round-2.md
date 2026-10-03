# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — review round 2

| Field | Value |
|---|---|
| Target SHA | 8a8ab40e0a5f1adf16cb7810072b120937517bb6 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 731 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 is a verifying round. It targets `8a8ab40e` over round 1's fix range `e01e1b12..1d6ac895`. It was asked:
- whether each of round 1's eight fixes holds at its commit;
- what the fixes added that round 1 never read: the new cases, the widened `longest_report` and its 564 / 972 / 1,378, the ledger corrections and re-reads, and the workflow's timeouts and `persist-credentials: false` under the job-level `continue-on-error`;
- whether any fix broke a neighbour, with `chain_counts` still reading 0.17.0 as `(10, 27, 6, 12)`;
- whether the orchestrator's answer to ⬜ 6 is coherent with the seal's label.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding 1 is closed — a tree with no declaration, or a capped pull request resolving to no work item, leaves the three tree rows not read and logs why | `.github/scripts/release_seal.py#chain_counts` | verified | Executed: the guard and the `lost` check each removed alone turn their case red; `release_seal.py` at `e01e1b12` fails all five cases |
| 🟢 | round 1's finding 2 is closed — an unlistable `rounds` leaves rounds and deferred not read; a row `verdict_table` skipped leaves deferred not read | `.github/scripts/release_seal.py#chain_counts` | verified | Executed: removing `or errors`, and taking back the rounds-None return, each turn their case red; 248 records in the tree read with no skipped row |
| 🟢 | round 1's finding 3 is closed — `describe` cuts the gate's name at `NAME_CAP` and expands a load failure's group only where today's `GROUPS` puts the gate in it; 564 / 972 / 1,378 | `hooks/dispatch.py#describe` | verified | Executed: either change removed alone turns the new case and the reserve case red; a wider brute force gives the same three figures; own records still name every loading group |
| 🟢 | round 1's finding 4 is closed in the file — the job carries `timeout-minutes: 60` and `continue-on-error: true`, the suite step `timeout-minutes: 30` | `.github/workflows/publish-release.yml` | verified | Executed: each of the three lines removed turns the S5 case red; what GitHub reports at the job's timeout is the ❓ row below |
| 🟢 | round 1's finding 5 is closed — the checkout sets `persist-credentials: false` | `.github/workflows/publish-release.yml` | verified | Executed: removed, the S5 case is red; read: nothing in the job needs git credentials |
| 🟢 | round 1's finding 6 — the deferred row counts Verdicts cells only | `.github/scripts/release_seal.py#chain_counts` | answered | Read: coherent with S10, Q10, the overview and the docstring; the changelog sentence that explains the row is not (⬜ 11) |
| 🟢 | round 1's finding 7 is closed — the not-found refusal names all three causes | `.github/scripts/release_seal.py:559` | verified | Executed: the S3 case pins the sentence and fails with the old one; the checklist's paraphrase is ⬜ 12 |
| 🟢 | round 1's finding 8 is closed — the checklist's by-hand route starts at a checkout at the tag and ends at the edit | `docs/release-checklist.md:343` | verified | Executed: the box case fails against the old box; the docstring's copy is ⬜ 13 |
| 🟢 | round 1's finding 9 is closed — the comment separates a full re-run from a re-run of `seal` alone | `.github/workflows/publish-release.yml:20` | verified | Read; GitHub's re-run semantics not executed |
| 🟢 | the ledger corrections D1, C3, W3 and 0.17.0 B1, and the re-reads W2, W4, 0.11.1 S9 and 0.15.0 P1c, hold against the fixes | `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md` | verified | Executed: figures, the 0.17.0 counts and W3's four mutations reproduce; `evidence-check .` exit 0, 0 drifted, 0 broken |
| 🟢 | the neighbour holds — `chain_counts` with this branch's code reads 0.17.0's tree as 10 · 27 · 6 · 12 | `.github/scripts/release_seal.py#chain_counts` | verified | Executed over a clone at `233f0455` with the live pull request list |
| 🟢 | round 1's confirmations still stand — every exception in `seal_release` ends in exit 0; Pillow is imported by `release_seal.py` alone | `.github/scripts/release_seal.py` | verified | Executed: the three modules, 103 passed; the import grep exits 1 |
| carried | round 1's confirmation that 909 was stale at the base (538, 915, 1,289 at `233f0455`) | `skills/verify/scripts/seal_stamp.py#MESSAGE_RESERVE` | carried, not re-derived | A base measurement pinned to `233f0455`; nothing in the fix range touches the base |
| ⬜ 10 | A re-read note for `describe` sits on 0.16.0's changelog-gather G2 row, which cites no `dispatch.py` unit, while the `stop` group's G2 row that cites `describe` was re-stamped with no note | `seal/releases/0.16.0.md:35` | open | Read: correction under `seal/releases/`; the line-77 claim holds (executed over every gate in every group) |
| ⬜ 11 | The changelog says the seal counts *how many issues the rounds deferred*; under ⬜ 6's answer it counts issues a Verdicts cell defers, and 0.17.0 is the case where the two differ | `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/changelog.md:11` | open | Read: correction under `seal/specs/`; keeps the decided rule |
| ⬜ 12 | The checklist's reason list still gives a hand edit as the only way the table is missing, against the refusal `626be3ab` rewrote | `docs/release-checklist.md:341` | open | Read: round 1's ⬜ 7 class, one member left |
| ⬜ 13 | The module docstring's by-hand route names neither the checkout at the tag nor the edit | `.github/scripts/release_seal.py:45` | open | Read: round 1's ⬜ 8 class, one member left |
| ❓ | What GitHub reports for the `seal` job when its own `timeout-minutes` fires under the job-level `continue-on-error` (the workflow comment says the run stays green), and that a step's timeout is honoured by that step's `continue-on-error` | `.github/workflows/publish-release.yml:79` | ❓ out of verified scope | Nothing local runs a job timeout; the note's fallback holds either way (read). The repository owner answers, from the first run that reaches a timeout |
| ❓ | The `seal` job on GitHub's runners: Q11's font, Q9's browsers, and the suite at a tag push (carried from round 1) | `.github/workflows/publish-release.yml` | ❓ out of verified scope | The repository owner answers at 0.18.0's tag push, from the job log and the release page |

## Paste-ready fixes

```
 **Re-read 2026-10-03 in round 1's fix pass of work item 1790993139 (#722), which drifted `describe` again:** a load failure now names every group that loads the file only where today's `GROUPS` puts the gate in the group the record names, and the gate's name is cut at `NAME_CAP`; for every record this plugin writes both are unchanged, and the claim holds
```
```
  tag, the work items and their review rounds, how many runs were capped,
  and how many issues the rounds' verdicts deferred (a deferral written only
  in a round record's `## Deferred` table is not counted). A count whose
  source cannot be
```
```
      table, the `seal` job's log says why on a `::warning::` line: the
      suite at the tag did not pass, a `gh` call failed, or the glance
      table was not in the note as generated -- edited before the job
      reached it, published without one, or the pull requests moved
      between the two lists. That job never fails the release.
```
```python
    # In test_the_checklist_box_says_where_a_missing_seal_is_explained:
    # round 2's 10-13 sweep: the reasons match the refusal's three causes.
    assert "published without one" in box
    assert "the pull requests moved between the two lists" in box
```
```
`DRY_RUN=1` draws the PNG at `SEAL_PNG` (by default `seal.png` in a
temporary directory), prints the rows and the note it would write, and
uploads and edits nothing, so the seal of a release whose job did not run can
be drawn by hand from a checkout at the tag, attached with
`gh release upload` and shown with `gh release edit --notes-file`.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the release seal, release note and gate-failure modules, in the clone at `8a8ab40e` | 103 passed, exit 0 |
| `bin/evidence-check .` over the clone | exit 0; 0 drifted, 0 broken in every ledger file |
| `bin/correction-check --range 233f0455...HEAD` over the clone | exit 0; no merge commit in the range |
| `chain_counts` at `8a8ab40e` over a clone at `233f0455`, pull requests from `merged_pulls` for 0.17.0 through `tally` | `(10, 27, 6, 12)`; rows `10 . 27 rounds`, `6 of 10`, `12 issues` |
| `longest_report(d, 1..3)` over the clone's `describe` | 564, 972, 1,378 |
| A brute force over `describe`: gates × groups × phases × error and message shapes (absent, past the cap, astral, newline-bearing) | 564, 972, 1,378; longest line 405 units |
| `describe` for every gate in every group it is in, phase `load` | every loading group named for every gate |
| `verdict_table` over every round record in the tree at `8a8ab40e` | 248 records, none without a Verdict column, none with a skipped row |
| `chain_counts` for this branch's own pull request over the tree at `8a8ab40e` | `(1, 1, 0, 0)` |
| Fourteen reverts and mutations in the clone, one at a time, each restored | every one red in the cases that claim it: `release_seal.py` at `e01e1b12` (5 failed); guard removed; `lost` removed; `or errors` removed; rounds-None return taken back; `dispatch.py` at `e01e1b12` (2 failed); gate cap removed (2); group guard taken back (2); `seal_stamp.py` comment at `e01e1b12`; the job timeout, the job `continue-on-error`, `persist-credentials` and the suite timeout each removed; the checklist at `e01e1b12` |
| `grep -rnE "from PIL\|import PIL"` over `hooks`, `skills`, `bin`, `.github`, less `release_seal.py` | exit 1 |
| `gh run view` for this branch's last two `test.yml` runs | `pytest (ubuntu-latest, 3.12)` 4m36s and 4m58s |
| The broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/release_seal.py:422` | round 1's 🔴 1 — fixed |
| round-1 | `.github/scripts/release_seal.py:428` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/dispatch.py:468` | round 1's 🟡 3 — fixed |
| round-1 | `.github/workflows/publish-release.yml:69` | round 1's 🟡 4 — fixed |
| round-1 | `.github/workflows/publish-release.yml:76` | round 1's 🟡 5 — fixed |
| round-1 | `.github/scripts/release_seal.py:445` | round 1's ⬜ 6 — answered |
| round-1 | `.github/scripts/release_seal.py:526` | round 1's ⬜ 7 — fixed |
| round-1 | `docs/release-checklist.md:343` | round 1's ⬜ 8 — fixed |
| round-1 | `.github/workflows/publish-release.yml:21` | round 1's ⬜ 9 — fixed |
| round-1 | `.github/scripts/release_seal.py#chain_counts` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/release_seal.py:549` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/run_tests.py#PILLOW` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py#MESSAGE_RESERVE` | round 1's 🟢 — confirmed |
| round-1 | `.github/workflows/publish-release.yml` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

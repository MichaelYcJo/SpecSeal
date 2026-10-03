# Round 2 report — the release seal is drawn and attached at publish time

- Work item: `1790993139-the-release-seal-is-drawn-and-attached-at-publish-time` (#718 boxes 2 and 3, #721, #722), PR 731
- Target: `8a8ab40e` on `feat/718-the-release-seal-is-drawn-and-attached-at-publish-time`
- Round: 2, a verifying round over round 1's fix range `e01e1b12..1d6ac895` (nine commits); `8a8ab40e` is round 1's close commit and touches `rounds/round-1.md` alone
- Ran by: `specseal:warden on claude-opus-5-5`
- Where: a `git clone --no-local` of the worktree at `8a8ab40e` in the round's scratch directory, and a second clone at `233f0455` for the 0.17.0 tree. Nothing was written in the worktree except this file.

## Summary

Every one of round 1's nine fixes is in the code, and each case the fix pass
planted goes red when its fix is taken away. I reverted or mutated fourteen
things one at a time in the clone and ran the cases that claim to pin each;
all fourteen went red. The neighbour the prompt named holds: with this
branch's `chain_counts`, 0.17.0's tree at `233f0455` still reads
`(10, 27, 6, 12)` against the live pull request list. The widened
`longest_report` measures 564, 972 and 1,378, and a wider brute force over
field shapes it does not try (absent fields, astral and newline-bearing
text, an unknown phase, no group) gives the same three figures.

Nothing I found needs a fix. Four ⬜ rows are new:

- **⬜ 10** — a ledger re-read note landed on the wrong row of
  `seal/releases/0.16.0.md`: it describes `describe` and sits on the
  changelog-gather row, while the row that cites `describe` got only its new
  hash.
- **⬜ 11** — ⬜ 6's answer (count Verdicts cells only) is coherent with the
  code, spec S10, Q10 and the docstrings. It is not coherent with the
  changelog sentence that explains the row to a reader, which still says *how
  many issues the rounds deferred*.
- **⬜ 12, ⬜ 13** — ⬜ 7 and ⬜ 8 were each fixed at the finding's coordinate,
  and each class has one more member the fix pass did not reach: the
  checklist's reason list just above the fixed lines, and the module
  docstring's by-hand route.

One runtime question is still open: what GitHub reports for a job that hits its
own `timeout-minutes` under a job-level `continue-on-error`. Whatever it reports,
the note survives. That question is a ❓ row and not a finding.

## Each fix, at its commit

| Round 1 | Commit | What I checked | Label |
|---|---|---|---|
| 🔴 1 | `7966a9f9` | The declarations guard and the `lost` list are both in `chain_counts`. Removing either alone turns its case red. With all of `release_seal.py` taken back to `e01e1b12`, the four new chain cases and the S3 case all fail (5 failed) | executed |
| 🟡 2 | `64196684` | `rounds_unread` makes the item `continue` and returns rounds None. Removing `or errors` turns the skipped-row case red, and so does taking back the rounds-None return | executed |
| 🟡 3 | `f118f7b5` | The gate is cut at `NAME_CAP`, and the expansion is guarded by `gate in GROUPS.get(group, ())`. Removing either alone, or taking back all of `dispatch.py`, turns both the new case and the reserve case red. Every record this plugin writes still names every group that loads its gate, checked over every gate in every group | executed |
| 🟡 4 | `e91e33b9` | The job has `timeout-minutes: 60` and `continue-on-error: true`, and the suite step has `timeout-minutes: 30`. Removing any one of the three lines turns the S5 case red. `job()` returns lines, so `"    continue-on-error: true" in seal` matches the job-level line exactly and is not satisfied by the eight-space step lines | executed |
| 🟡 5 | `071c9005` | `persist-credentials: false` is on the checkout, and removing it turns the S5 case red. Nothing in the job needs git credentials. `tagged` calls only `git rev-parse`; the suite's `fetch` and `push` calls go to local fixture remotes; `fetch-depth: 0` has already fetched | executed (mutation); read (no credential use) |
| ⬜ 6 | — | Answered by the orchestrator with no code change; coherence judged below (⬜ 11) | read |
| ⬜ 7 | `626be3ab` | The refusal names the three causes, and the S3 case pins the whole sentence. Taken back, it fails. The checklist's paraphrase of the same reasons was not changed (⬜ 12) | executed |
| ⬜ 8 | `318d3426` | The box says *from a checkout at the tag* and ends at `gh release edit --notes-file`, and the box case pins both. Taken back, it fails. The module docstring's copy of the route was not changed (⬜ 13) | executed |
| ⬜ 9 | `93ff907a` | The comment now separates a full re-run from a re-run of `seal` alone | read; GitHub's re-run semantics not executed |

## What the fix pass added that round 1 never read

**The five new cases** (the record's `New units` row). I judged them as code.
Each pins a value and a log fragment, and each goes red against its own
mutation (above). The empty-tree case uses `tmp_path` as the root. That root
holds no `seal/`, so `declarations` falls back to the git common directory,
and a temporary directory has none. The astral assertion counts right:
`"y"` plus 19 astral characters is 39 units, and a twentieth would be 41.

**The widened `longest_report` and 564 / 972 / 1,378.** Executed:
`longest_report` over the clone's `describe` gives `[564, 972, 1378]`. A
brute force over every gate (known gates, three 300-character foreign names,
one astral name) × group (none, empty, every known group, a 300-character
one, an astral one, one with newlines) × phase (`load`, `run`, none, an
unknown word) × error and message each absent, ASCII past the cap, astral, or
newline-bearing gives the same 564, 972 and 1,378. The longest single line is
405 units: a foreign gate failing while running in a known group. No
reserve figure states a stale number anywhere in the tree outside the dated
history in `phases/phase-1.md` and the correction notes.

**The ledger corrections.** D1, C3, W3 and 0.17.0 B1 each say what the fix
changed and keep the old figure in a dated note. Their figures and claims
match what I executed. C3's *it still reads 10 · 27 · 6 · 12* is now executed
with this branch's code, not carried. W3's *each of the four lines removed
went red* reproduces. B1 corrects inside its existing
`Corrected 2026-10-03 by work item 1790993139 (#722)` note and records the
superseded figures in a parenthesis. That keeps the dated marker, so
`correction-check` still has something to read. The re-reads of W2, W4,
0.11.1 S9 and 0.15.0 P1c hold against the edits they name. One re-read sits
on the wrong row (⬜ 10). `evidence-check .` over the clone reports 0 drifted
and 0 broken in every ledger file (executed).

**The workflow.** The suite step's 30 minutes fires before the job's 60, so
a hung suite ends as a failed step. That step is `continue-on-error`, the
draw step runs, and `SUITE_OUTCOME` is `failure`, so `seal_release` refuses
with the note untouched. The job's own timeout is reachable only through a
hang outside the suite step: the checkout, setup-python, the pip install, or
a `gh` call in the draw, which `gh()` runs with no timeout. Whatever GitHub
then reports, the note's fallback holds. The note was published by the
`publish` job, and the seal job's only write to the note is its last call, so a
job ended at any point leaves the published note as it was. The worst case is a
`seal.png` attached that the note does not show. The script's docstring
already names that state. Whether the run then reads green is the ❓ row: the
workflow comment states it as fact (*the job's line below keeps the run green
if it is reached anyway*), and nothing local can run it. For headroom, the
`pytest (ubuntu-latest, 3.12)` job of `test.yml` ran 4m36s and 4m58s on this
branch's last two runs (executed, `gh run view`), against the step's 30
minutes.

**Whether `or errors` costs a release its deferred row.** Executed: every
one of the 248 round records in the tree at `8a8ab40e` reads through
`verdict_table` with a Verdict column and no skipped row. So the new guard
leaves today's records countable. This branch's own pull request, as the 0.18.0
seal will see it, reads `(1, 1, 0, 0)`.

## ⬜ 6's answer, against the seal's label

The answer is to count Verdicts cells only. It agrees with every document that
defines the count: spec S10, `questions.md` Q10, the overview's *Not done*,
and the `chain_counts` docstring (*the number of distinct issues named in a
Verdicts cell whose verdict is `deferred`*). The panel's label cannot carry
the narrower meaning: `deferred` is fixed at eight characters by
`{label:<8}`.

The sentence that explains the row to a reader is the changelog fragment's,
and it says something else. *How many issues the rounds deferred* is true of
0.17.0's 13 and false of the 12 the rule draws, because the rounds did
defer #722, in a `## Deferred` table. Round 1's record compounds this: its
⬜ 6 grounds say *0.17.0 reads 12 and the seal says so*. The seal does not
say so. The panel reads `deferred 12 issues`, and the alt text reads `12 issues
deferred`. Nothing on the release page says which deferrals were counted.
That is ⬜ 11. It keeps the choice and asks only that the shipped sentence
state it.

## Stage 2 — new findings

### ⬜ 10 — A re-read note for `describe` sits on a row that does not cite it

`seal/releases/0.16.0.md:35` and `seal/releases/0.16.0.md:77`, both from
`1d6ac895`. `f118f7b5` drifted `describe`, and two rows of 0.16.0 needed
attention:

- **Line 77** is the `stop` group's G2 row, and it cites
  `hooks/dispatch.py#describe`. Its anchor was re-stamped to `@3cb712c3`, but
  no note says it was re-read against the guard and the gate cap. The
  repository rule asks for exactly that note: *an edit drifts the row, which
  is re-read against that edit and re-stamped there with a dated note*.
- **Line 35** is the changelog-gather and ledger-fold refusal row, also
  labelled G2, and it cites no unit in `dispatch.py`. It received the
  note: *Re-read 2026-10-03 in round 1's fix pass of work item 1790993139
  (#722), which drifted `describe` again: a load failure now names every
  group that loads the file only where today's `GROUPS` puts the gate in the
  group the record names…*. On that row the note describes nothing the row
  claims.

The claim on line 77 still holds. A record this plugin writes names the group
that loaded the gate, so the guard is true for it, and I executed that over
every gate in every group. Only the note is in the wrong place. Nothing checks
where a note sits. `correction-check` reads markers only across a merge, and
`evidence-check` reads hashes. So the misplacement survives every gate, and a
later reader of line 35 finds a dated reading of code the row never cited.
The location is under `seal/releases/`, so this is a correction and not a fix.

### ⬜ 11 — The changelog says the rounds' deferrals; the row counts verdict cells

`seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/changelog.md:11`.
The panel's rows are described as *… how many runs were capped, and how many
issues the rounds deferred*. Under ⬜ 6's answer the row counts issues a
Verdicts cell defers. The measured case, 0.17.0, is the one where the two
differ (13 against 12). This fragment is gathered into `CHANGELOG.md` and the
release note, so the sentence ships. Its location is under `seal/specs/`, so it
is a correction. The paste-ready sentence keeps the decided rule.

### ⬜ 12 — The checklist still gives a hand edit as the only reason the table is missing

`docs/release-checklist.md:341`. This is the same class as round 1's ⬜ 7, two
lines above the lines `318d3426` changed. The box lists why the note still
shows the table: *the suite at the tag did not pass, a `gh` call failed, or
the note was edited before the job reached it*. Since `626be3ab` the
`::warning::` line names three causes for the last branch: edited, published
without one, or the pull requests moved between the two lists. A reader of
§6 whose note went out as the section alone is still sent to look for an edit.
The log line is right and only the paraphrase lags, so this is ⬜.

### ⬜ 13 — The module docstring's by-hand route still stops at the upload

`.github/scripts/release_seal.py:45`. This is the same class as round 1's ⬜ 8.
The docstring ends *so the seal of a release whose job did not run can be drawn
by hand and attached with `gh release upload`*. It names neither the checkout
at the tag, which `ROOT = CODE` and `tagged` both need, nor the edit. An upload
without the edit leaves the state the docstring's paragraph above calls a
failure: an image the note does not show. `318d3426` fixed the checklist's copy
of this route and not this one.

**One residual noted, not raised.** The by-hand route says *apply the note
it prints*. A dry run prints the rows, the `drew` line and a `DRY_RUN` header
above the note, so the person has to cut the note out by hand. A `SEAL_PNG`
named other than `seal.png` also uploads under a name the note's image URL does
not use. Both are a person following a manual route with care, and I left them
as prose.

## Regression tests to plant

| Finding | Destination | Case |
|---|---|---|
| ⬜ 12 | `tests/test_the_release_seal_is_drawn.py`, `test_the_checklist_box_says_where_a_missing_seal_is_explained` | Assert the box names *published without one* and *the pull requests moved*; fenced under ⬜ 12. Red against today's box by construction, since neither phrase is in it |

⬜ 10, ⬜ 11 and ⬜ 13 are prose with no reader to pin them.

## Facts for the evidence ledger

- `chain_counts` at `8a8ab40e` over the tree at `233f0455`, with
  `publish_release_note.merged_pulls` for 0.17.0 run through `tally`:
  10 work, 11 closed, no outside contributor; capped #696, #698, #699, #700,
  #705, #719; `(10, 27, 6, 12)`. Executed 2026-10-03.
- Every round record in the tree at `8a8ab40e` (248) reads through
  `chain_check.verdict_table` with a Verdict column and no skipped row.
  Executed 2026-10-03.
- `longest_report` and a wider brute force over `describe` at `8a8ab40e`:
  564, 972 and 1,378; longest single line 405 units. Executed 2026-10-03.

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

The probe files were deleted after one run each. The two clones, including the
clone's `.venv`, were removed with the round's scratch directory before handover.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 10

In `seal/releases/0.16.0.md`, remove this sentence from the end of line 35's
Notes cell (the cell then ends at *…so the claim holds*, as it did at
`e01e1b12`), and append it to the end of line 77's Notes cell, after
*…The claim holds*:

```
 **Re-read 2026-10-03 in round 1's fix pass of work item 1790993139 (#722), which drifted `describe` again:** a load failure now names every group that loads the file only where today's `GROUPS` puts the gate in the group the record names, and the gate's name is cut at `NAME_CAP`; for every record this plugin writes both are unchanged, and the claim holds
```

### 11

```
  tag, the work items and their review rounds, how many runs were capped,
  and how many issues the rounds' verdicts deferred (a deferral written only
  in a round record's `## Deferred` table is not counted). A count whose
  source cannot be
```

### 12

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

### 13

```
`DRY_RUN=1` draws the PNG at `SEAL_PNG` (by default `seal.png` in a
temporary directory), prints the rows and the note it would write, and
uploads and edits nothing, so the seal of a release whose job did not run can
be drawn by hand from a checkout at the tag, attached with
`gh release upload` and shown with `gh release edit --notes-file`.
```

Needs a fix: no

Loses a record or crashes: no

Nothing in this report needs a fix. Once the orchestrator answers ⬜ 10–13,
by a fix or with grounds, the sealer's spawn comes due. That spawn is the
broad gate, and it is the sealer's to run, not this session's.

## Proof block

Files opened in this round:

- `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/rounds/round-1.md`, `rounds/round-1-report.md`, `changelog.md`, `overview.md` (*Not done* and the divergence table), `spec.md` (the 0.17.0 rows and the S10 grep), `questions.md` (the deferred lines)
- `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md` (D1, C3, W2, W3, W4 as changed), `seal/releases/0.16.0.md` (lines 35 and 77), `seal/releases/0.17.0.md` (B1), `seal/releases/0.11.1.md` (S9), `seal/releases/0.15.0.md` (P1c), all through the fix diff and the rows' text
- `.github/scripts/release_seal.py` (module docstring, `release_rows`, `alt_text`, `readers`, `chain_counts`, `gh`, `tagged`, `seal_release`, `main`)
- `.github/workflows/publish-release.yml` (the `seal` job and its header comment)
- `hooks/dispatch.py` (`capped`, `read_record`, `flat`, `describe`, `draw`), `hooks/routing.py` (`declarations`, `item_dir`, `rounds`, `rounds_unreadable`)
- `skills/verify/scripts/seal_stamp.py` (the reserve comment), `skills/code-review/scripts/chain_check.py` (the verdict vocabulary), `docs/round-record-spec.md` (the no-id rows), `skills/evidence-check/scripts/correction_check.py` (the marker grammar)
- `docs/release-checklist.md` (§6's note box)
- `tests/test_the_release_seal_is_drawn.py`, `tests/test_a_release_publishes_its_note.py` (`workflow`, `job`, `steps`, the S5 case), `tests/test_a_gate_that_fails_says_so.py` (`longest_report` and the new case), through the fix diff
- `bin/test`

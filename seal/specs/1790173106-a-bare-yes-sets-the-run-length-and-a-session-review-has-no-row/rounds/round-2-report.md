# Round 2 report — the verifying round at round 1's fixes

| Field | Value |
|---|---|
| Target SHA | `097634a4b0a24aef46f24f534654b4390f184055` |
| Base | `cbb58091fddb9a02e3136156d7963dcd66798d1b` (the release branch this pull request merges into) |
| Fix range | `4f596a7719ae5757880bb9dea06555e55596d701..506b030ad911eee0bcb5fe533c3b0d4176247ecd`, three commits, plus `097634a4` which closed round 1's record |
| Round 1 target | `7604e522` |
| Ran by | specseal:warden on claude-fable-5-1 |

## Summary

Round 1's one finding is closed as its record says, and the three paperwork
rows were answered truthfully. The fix range changes no behaviour: its only
code edit is the text of one refusal message in `round_record.py`, and the
case that pins that message is green. The round opens nothing that needs a
fix. It does open one paperwork correction, and that one is not harmless to
the next step: the commit that closed round 1's record wrote the name of a
function `survivor_check.py` does not have into the record's Grounds cell,
and the evidence checker refuses the record for it — exit 2 in the form CI's
`ledger` job runs, and the form `broad-gate` runs is stricter still. The cell
has to be corrected before the sealer is spawned, or the seal comes back
NOT SEALED on a round record rather than on the tool.

## Round 1's 🟡 1 — closed as the record says (executed)

The record says the F4 note in `seal/ledger.md` no longer names the removed
F8, carries a dated `Corrected` marker pointing at fragment B2, and the CI
form of the sweep exits 0 on the committed tree. All three hold.

- `seal/ledger.md:777-778` now lists F8 as *and F8 until #138 removed it —
  see the F4 note below*, and `seal/ledger.md:786-790` carries
  `**Corrected 2026-09-24 by work item 1790173106 (#138)**` followed by the
  fragment path and `B2`. Read against the two paste-ready blocks in
  round 1's report: applied as given, byte for byte apart from the wrap.
- `F8` occurs in `seal/ledger.md` on those two lines and nowhere else
  (executed grep), so *F8 has left this file* is true.
- The fragment's B2 is the row the note points at; `fold_ledger.py:198`
  writes `### <work-item-id>` as the heading a fragment goes under, so *which
  the fold moves under this file's `### 1790173106` heading* is true of the
  fold as it stands.
- The hygiene workflow's form — `survivor_check.py --range <base>...HEAD`
  with every `seal/specs/*/survivors.md` as `--exempt`, which is what
  `.github/workflows/hygiene.yml:250-255` runs — exits 0 at `097634a4`,
  reporting one survivor, `chain_check.py:2960`, as exempt. That is the
  result the record's Grounds cell claims for `506b030a`, reproduced at the
  target.
- `correction-check --range <base>...HEAD` exits 0: the range holds no merge
  commit, so no correction could have been dropped at one. The marker is in
  the form the checker reads (verb, then date); nothing in the range
  exercised it.

## The three paperwork rows — answered truthfully

**The memo's mutation count.** `overview.md:12` now says *the thirteen
mutations M1–M13 tabled in `phases/`*, which matches the phase files round 1
counted. Read.

**`terminal_value`'s refusal sentence.** The old sentence explained
`Needs a fix`'s count under either label. The new one, at
`skills/code-review/scripts/round_record.py:1365-1376`, names each row's own
reason — `Needs a fix` because the floor's count of later records restarts
there, `Loses a record or crashes` because the cell would record that
something was found and not what. I read both reasons against
`chain_check.py#stopping_floor`: the `Needs a fix` refusal there says *it is
also the cell the count of later records restarts at*, and the floor's says
*the cell records that something was, and not what*. The sentence is now
right about both. One residue, not a defect: `stopping_floor` grandfathers
the `Needs a fix` refusal under `NEEDS_FROM` (a notice, not an error, for a
work item begun before it), and the writer's sentence says `chain_check.py`
*refuses* it in both rows without that qualifier. The writer itself is not
grandfathered, so the record it refuses to write is refused whatever the
item's age; the sentence overstates only what the reader would have done.

The re-stamps hold. `evidence-check --strict` at `506b030a` reports
`1565 ok · 0 drifted · 0 broken` with 0 names refused, so
`terminal_value@53032294` on the shared row and on the fragment's B3 is the
hash of the unit as committed. Executed. A5 is green: `bin/test` over
`tests/test_the_record_is_generated.py` and four other modules, 284 passed,
and `test_a_bare_yes_on_either_terminal_line_is_refused_at_the_writer` pins
the sentence's first clause, `carries no reason`, which the rewording kept.

**The six `survivors.md` rows.** The grounds for keeping them are the
mechanism the fix pass named, and I confirmed the mechanism by reading and
by measurement. Reading: `survivor_check.py#corrected` (line 580) returns,
as its second value, the n-grams of every sentence the range added, and
`survivor_check.py#wanted` (line 644) subtracts them from the removed
sentences' n-grams; `records_a_past_round` (line 503) keeps only paths under
`rounds/` out of that list, so a work item's `survivors.md` is inside it, and
each row's Quote cell is an added sentence that quotes the standing text it
excuses. Measurement, all in the CI form: at `b871c3c7`, where the fix pass
had dropped the five rows, the sweep reports the five places plus the one
exempt and exits 1; at `097634a4`, with the rows back, it reports one place,
exempt, and exits 0; at `097634a4` with this item's `survivors.md` withheld
from `--exempt` but still in the tree, it reports `chain_check.py:2960` alone
and exits 1. So the five rows do silence their five places through their own
quotes, whether or not the file is handed over — which is #507/#308, work
item B of this release, and not this branch's to fix. The table rows are
byte-identical across the range (executed: no table line appears in
`git diff 4f596a77..506b030a` for that file); only the header comment
changed, and what it now says is what I measured.

## What this round opened — one paperwork correction

⬜ 1 — **The record's Grounds cell and the survivors header both name a
function the sweep does not have, and the evidence checker refuses the
record for it.** `round-1.md:34` (written by `097634a4`, the record commit)
says *a row's quote is an added sentence whose n-grams `removed_sentences` subtracts* (NAME NOT IN TREE),
and `survivors.md:15` (written by `506b030a`) says
`survivor_check.py#removed_sentences` *subtracts the n-grams of every sentence the range ADDED* (NAME NOT IN TREE).
There is no such function; grep over
`skills/code-review/scripts/survivor_check.py` finds the name nowhere, and
the units that do this are `corrected` (collects the added sentences'
n-grams) and `wanted` (subtracts them).

Executed: `evidence-check --strict` at `097634a4` exits 2 with
`NOT-IN-TREE seal/specs/1790173106-…/rounds/round-1.md:34 removed_sentences`
and `1 refused`; at `506b030a` the same command exits 0 with 0 refused, so
the refusal entered with the record commit. The non-strict form CI's `ledger`
job runs (`.github/workflows/test.yml:94`, exit 2 fails the job) exits 2 as
well. The survivors header is inside an HTML comment, which the checker reads
as an aside, so only the record line is refused — but both lines say the same
false thing, and the class is the name, not the line.

Location is under `seal/specs/`, so per `agents/warden.md` this is a
correction and stays out of `Needs a fix`. It is not optional: the sealer's
`broad-gate` passes `--strict`, so a seal taken over this tree comes back NOT
SEALED on the record. The correction is a hand-edit to a closed record; the
paste-ready form is below.

## Behaviour outside the three files

The fix range touches five files. `seal/ledger.md` (the F4 note and the
`terminal_value` re-stamp), the fragment (the B3 re-stamp), `overview.md`,
`survivors.md` and `round_record.py`. The one code change is the string
inside `terminal_value`'s `Refused(...)` at lines 1365-1376; no branch,
label or return changed (read against the diff). `uvx ruff check` and
`ruff format --check` on that file: clean. Nothing else changed behaviour.

Round 1's 🟢 verdicts stand: the fix range touched none of the units they
cover (`says_reopened`, `run_reopened`, `stopping_floor`, `floor_and_fixes`,
the seven #241 places, the routing prompt, the direct-route table).

Carried from round 1 rather than re-established: the coordinates of the
units above and of the fourteen `seal/ledger.md` rows round 1 re-read;
`evidence-check` at both SHAs reports 0 drifted and 0 broken, so none of
those anchors moved.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's 🟡 1 — the F4 note in `seal/ledger.md` no longer names the removed F8, carries a dated `Corrected` marker pointing at fragment B2, and the CI form of the sweep exits 0 on the committed tree | `seal/ledger.md:777`, `seal/ledger.md:786` | answered | verified closed this round — executed: `survivor_check.py --range <base>...HEAD` with every `survivors.md` at `097634a4` — exit 0, one survivor (`chain_check.py:2960`) exempt; `correction-check` exit 0; read: both paste-ready edits applied as given, `F8` on no other line of the file |
| 🟢 | round 1's first ⬜ — `overview.md` counts thirteen mutations | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/overview.md:12` | answered | verified closed this round — read: *the thirteen mutations M1–M13 tabled in `phases/`* |
| 🟢 | round 1's second ⬜ — the six `survivors.md` rows kept, on the grounds that the sweep silenced itself through the rows' own quotes | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:3` | answered | executed: CI form at `b871c3c7` (rows dropped) — five places, exit 1; at `097634a4` (rows back) — one exempt, exit 0; with this item's file withheld from `--exempt` — `chain_check.py:2960` alone, exit 1. read: `corrected` collects the added sentences' n-grams, `wanted` subtracts them, and `records_a_past_round` excludes only `rounds/`; the six table rows are byte-identical across the range |
| 🟢 | round 1's third ⬜ — `terminal_value`'s refusal names each row's own reason, A5 green, both re-stamped rows hold | `skills/code-review/scripts/round_record.py:1365-1376` | answered | verified closed this round — read against `stopping_floor`'s two refusals; executed: 284 passed over five modules including the pin `carries no reason`; `evidence-check --strict` at `506b030a` 1565 ok, 0 refused, so `terminal_value@53032294` is the committed unit's hash |
| ⬜ 1 | the record's Grounds cell (`097634a4`) and the survivors header (`506b030a`) name `removed_sentences`, a function `survivor_check.py` does not have; the evidence checker refuses the record — exit 2 in CI's `ledger` job form and under `--strict` (NAME NOT IN TREE) | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/rounds/round-1.md:34`, `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:15` | not a defect | paperwork under `seal/specs/`, kept out of `Needs a fix` per `agents/warden.md`; executed: `evidence-check --strict` exit 0 with 0 refused at `506b030a`, exit 2 with 1 refused at `097634a4`; the units are `corrected` and `wanted`. Must be corrected before the sealer runs, because `broad-gate` passes `--strict` |
| 🟢 | the fix range changed no behaviour outside the three files: the one code edit is a message string, and lint is clean | `skills/code-review/scripts/round_record.py:1365-1376` | not a defect | read against the diff; executed: `uvx ruff check` and `ruff format --check` clean |
| ❓ | the broad gate — full suite, repository-wide lint, typecheck | — | out of verified scope | the sealer's, after the rounds settle; the prompt labelled it unverified and ordered no run. This round leaves nothing needing a fix, so the sealer's spawn is due — once ⬜ 1 is corrected, or the strict form refuses the record |

## Executed probes

| What was run | Result |
|---|---|
| `python3 skills/code-review/scripts/survivor_check.py --range cbb58091...HEAD` with all seven `seal/specs/*/survivors.md` as `--exempt`, at `097634a4` (the hygiene workflow's form) | exit 0; 403 files examined against 65 removed sentences; `exempt skills/code-review/scripts/chain_check.py:2960`; *every survivor is excused by a row above (1)* |
| the same at `097634a4` with this item's `survivors.md` withheld from `--exempt` (six exempt files, the file still in the tree) | exit 1; one place, `chain_check.py:2960` (`written_late_reason` against `run_reopened`'s old body at `:3099`, 2.00); the five F8 places do not appear |
| the same at `b871c3c7`, where the fix pass had dropped the five rows | exit 1; `chain_check.py:2960` exempt; five places reported — `docs/review-chain-spec.md:1418` (2.88), `chain_check.py:2374` (2.77), `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:356` (2.00), `seal/ledger.md:820` (2.00), `chain_check.py:2370` (1.88) |
| `bin/correction-check --range cbb58091...HEAD` at `097634a4` | exit 0; no merge commit in the range |
| `bin/evidence-check --strict` at `506b030a` | exit 0; `total: 1565 ok · 0 drifted · 0 broken`; `1 work item read · 165 names read · 0 refused` |
| `bin/evidence-check --strict` at `097634a4` | exit 2; `total: 1565 ok · 0 drifted · 0 broken`; `NOT-IN-TREE …/rounds/round-1.md:34 removed_sentences`; `167 names read · 1 refused` |
| `python3 skills/evidence-check/scripts/evidence_check.py .` at `097634a4` (the form `.github/workflows/test.yml:94` runs) | exit 2, the same refusal |
| `python3 skills/code-review/scripts/chain_check.py --baseline cbb58091…` at `097634a4` | exit 1 on this work item: `Broad gate` is `not yet` on a record judged as a ready pull request, and `Pass` is checked beside `Fixes checked by: nobody — the fixes are written and no round has opened them`. Both are the states this round's record replaces; the pull request is a draft |
| `bin/test tests/test_the_record_is_generated.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_a_merge_cannot_silently_drop_a_correction.py -q` at `097634a4` | 284 passed |
| `uvx ruff check` and `uvx ruff format --check` on `skills/code-review/scripts/round_record.py` | `All checks passed!`; `1 file already formatted` |
| `grep -n -E '\bF8\b' seal/ledger.md` at `097634a4` | two lines, 777 and 787, both inside the corrected note |
| `git diff 4f596a77..506b030a -- <survivors.md>` filtered to table lines | no table line changed; the header comment alone |
| grep for `removed_sentences` over `skills/` and `seal/` (NAME NOT IN TREE) | no definition anywhere; two mentions, `round-1.md:34` and `survivors.md:15` |
| the broad gate — full suite, repository-wide lint, typecheck | not yet |

A note on the clone. My first `git clone --no-local` was made in the
session's scratch directory under a generic name, and a parallel agent's
clone of the same name replaced it mid-round — its `HEAD` moved to another
work item's commit between my reads and my first runs. Every result above
was taken afresh in a clone named for this work item, whose `HEAD` was
verified as `097634a4` (or `b871c3c7`, `506b030a` where stated) before each
command. The reads made before the switch that fed this report were checked
again in the new clone. Both clones of mine were deleted after the run; the
other agent's directory was left alone.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the sweep silences a survivor through the `survivors.md` row that quotes it, whether or not the file is passed as `--exempt` | already deferred: #507/#308, work item B of this release (`fix/308-survivors-md-silences-what-it-quotes`) | the owner of `survivor_check.py`, in that work item |

## Paste-ready fixes

⬜ 1 — two lines, one name. The record is a closed, generated file, so this
is a hand-edit; the second is the header comment of `survivors.md`.

```
seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/rounds/round-1.md:34 — inside the 🟡 1 Grounds cell, replace
a row's quote is an added sentence whose n-grams `removed_sentences` subtracts, which is #507/#308
with
a row's quote is an added sentence whose n-grams `corrected` collects and `wanted` subtracts, which is #507/#308
```

```
seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:15-16 — replace
artefact, not a fact about the tree: `survivor_check.py#removed_sentences`
subtracts the n-grams of every sentence the range ADDED, and a row here quotes
with
artefact, not a fact about the tree: `survivor_check.py#corrected` collects the
n-grams of every sentence the range ADDED and `wanted` subtracts them, and a row here quotes
```

Needs a fix: no — the one thing opened is a paperwork correction under `seal/specs/` (⬜ 1), and it goes to the orchestrator before the sealer is spawned, because `evidence-check --strict` refuses the record at `097634a4`
Loses a record or crashes: no

## Proof block — files opened

Executed in a clone at `097634a4` (and at `b871c3c7` and `506b030a` where stated): the sweep in three forms, `bin/correction-check`, `bin/evidence-check --strict` at two SHAs and the non-strict form, `chain_check.py --baseline`, `bin/test` over five modules, `uvx ruff`, the greps above. Read: `seal/specs/1790173106-…/rounds/round-1.md` and `round-1-report.md`, the fix-range diff and the record commit's diff in full, `seal/specs/1790173106-…/survivors.md`, `overview.md:9-12` (in the diff), `seal/ledger.md:770-792` and the re-stamped `terminal_value` row (in the diff), `seal/ledger/1790173106-….md` B1–B3 (in the diff), `skills/code-review/scripts/round_record.py` (`terminal_value`, lines 1320-1378), `skills/code-review/scripts/chain_check.py` (`stopping_floor` whole, the constants at 608-663, `main`'s arguments), `skills/code-review/scripts/survivor_check.py` (`corrected`, `wanted`, `records_a_past_round` by name, `git`, `resolves`, `parse_range`, the §*What is excluded* comment), `tests/test_the_record_is_generated.py` (the writer's pin and its neighbours), `.github/workflows/hygiene.yml:220-299`, `.github/workflows/test.yml:80-100`, `skills/evidence-check/scripts/evidence_check.py` (`exit_code`, the aside rule at 2011-2031), `skills/evidence-check/scripts/correction_check.py:20-68`, `.github/scripts/fold_ledger.py:131-198`, `bin/test`

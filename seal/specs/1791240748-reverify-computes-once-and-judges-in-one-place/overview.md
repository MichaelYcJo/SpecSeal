# 1791240748-reverify-computes-once-and-judges-in-one-place — overview

📋 implement applied
· spec:     `spec.md` (D1–D7, S1–S15, *What must survive*, the two test tables), `plan.md` (Technical context, Phases, Overlap with #822), `questions.md` (Q1–Q4); `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* and §*A row is a content anchor*; `docs/the-pact.md` §*A signatory records a pact change*; `skills/evidence-check/SKILL.md` §*Re-verifying is recomputing the hash*; `seal/config.md`'s `Ledger frozen from`
· evidence: `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md`, 38 `Re-read ·` rows written by `--reverify --into` and 8 `Corrected ·` rows
· verified: executed — the phase slices, D6's three probes, sixteen mutations plus three re-runs, `--strict .`; read — the 46 released claims the re-read owed; unverified — the broad gate (the sealer)

## Why this work exists

`--reverify` read a coordinate one way and `--strict` another, and walked
files in an order that left a row drifted until a second run; now one judge
reads every coordinate and one plan, judged against the text it writes, is
written once.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The released rows taking `Corrected ·` rows | D7: *`seal/releases/0.18.0.md:24` and `0.18.1.md:417` on `current_hash`; `0.18.2.md:86` and `:90` …; `0.18.3.md:6` …; `0.18.3.md:8` …*, and `0.4.0.md:59` | Eight rows: `0.18.1:417`, `0.18.2:86`, `:87`, `:90`, `0.18.3:6`, `:8`, `:10`, `0.4.0:59` | `0.18.0:24` is superseded by `0.18.1:417`, and a second correction of it would read DRIFTED as two claims nobody reconciled. `0.18.2:87` (E4) states the walk's move-then-BROKEN fold and cites two removed cases. `0.18.3:10` (A5) says *`reverify`'s docstring says every `left` line goes through `walked_outcome`*, false after phase 2. Measured: `--into` named exactly these rows' BROKEN coordinates, and reading the 46 claims found A5 |
| S6 at the base | *red at the base (silent, exit 0)* | The case is red at the base | Measured at `e6d5a055`: the base re-stamped the row once and its family line named it `still DRIFTED … does not hold the code`, exit 1. Not silent and not 0, but the hash it wrote drifted at once and no line said why (`phases/phase-2.md`) |
| The verdict's shape | D2's sketch carries the places, which of them hold, and whether they are unsure | `Verdict(status, coord, detail, now, region, dest)` | No command reads the three once status, hash and destination are carried; `region` is carried for `on_a_cycle` (`phases/phase-1.md`) |
| A test the spec's lists missed | Neither list names `test_the_two_commands_that_must_know_ask_for_the_flag` | Rewritten: `judge` asks for the flag, `reverify` calls `judge` and no reader of a place | It pinned `classify` and `reverify` as the two callers of `resolve_unit`, which phase 1 and phase 2 each made false |
| A `left` line on a statement gone | D2: *the check's detail sentence followed by ` — left`* | Followed literally: `… — re-verify — left` | The spec's rule; a reworded check sentence would be a second reading |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck: this run ran only the phase slices the plan names | the sealer, once after the review rounds settle |
| The time a pass takes when it reaches its bound over a large ledger: no row in this repository's ledger reaches it, so only the test trees measured it | the reviewer, or a later work item that meets a real cycle |
| The rebase onto #822's rename: `docs/the-pact.md`'s one sentence and the cases appended to `tests/test_a_signatory_records_a_pact_change.py` | whichever of #822 and #824 squashes second, per `plan.md` §*Overlap with #822* |

## Not done

`skills/evidence-check/SKILL.md` §*Re-verifying* was re-read and left
(questions Q4). No permanent differential test was added; the three probes
ran once and their figures are in the phase records (spec §*Out*). The
mutation *a pass leaves nothing at its bound* has no verdict: without the
leaving the passes never end, and the run timed out at 60 s.

## Fed back into the spec

- *Inferred during implementation:* at the bound, only the coordinates whose
  naming leads back to their own row are left; a coordinate downstream of a
  cycle is recomputed, and one left on a cycle that reads OK at the end is
  named nowhere (questions Q1).
- *Inferred during implementation:* within a round a verdict is reused where
  the file its coordinate names did not change, except a BROKEN one, whose
  destination scan reads other files.
- *Inferred during implementation:* a claim row is never re-pointed, because a
  unit can reconstruct a statement's hash without being the statement.

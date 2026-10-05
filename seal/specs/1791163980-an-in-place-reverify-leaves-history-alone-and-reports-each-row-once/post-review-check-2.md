# Post-review check 2 — #810's fix: a claim tie is named by how many places hold the recorded content

| Field | Value |
|---|---|
| Pass | a second verifying pass over the post-review fixes; not a round (the run is capped) |
| Target SHA | 7e12e538 |
| Range checked | 272ffa32..7e12e538, 3 commits (2c9ae970 the fix, d0074bc0 the records, 7e12e538 the `survivors.md` rows) |
| Base | `release/v0.18.3` at a3aa139a |
| Pull request | #801 (draft, `chain: capped`) |
| Ran by | specseal:warden on claude-opus-5-5 |

## What this pass was asked, and what it found

#810 is closed. For a claim whose minor content two or more places hold,
the check's detail and both `--reverify` sites now give one reason, and it is
true: how many places hold the recorded content, and that the recorded hash
cannot break the tie.

- **The tie cells.** S1, C4 and CU were re-run at 7e12e538 beside 272ffa32.
  S1 and C4 read `2 holding` and `3 places, 2 holding` in `--reverify`, and
  `(2 hold the recorded content, a tie it cannot break)` in the check. The
  frozen `LEFT` line, which quotes the check's detail, follows it.
- **Every other cell is byte-identical.** 136 non-tie cell-arms gave the same
  `--strict` before, `--reverify` output, `--strict` after and MOVES at both
  copies. That includes the major-level shape `0.4.0.md:20` quotes.
- **The seven new `Re-read ·` claims hold** at 7e12e538. They are exactly the
  seven released rows whose newest reading cited `evidence_check.py#classify`
  at its old hash, so the class is complete.
- **The five `survivors.md` rows** each excuse a place in `post-review-check.md`
  whose wording is true of 1c3178a1, the commit it describes. 1c3178a1 and
  272ffa32 carry the same code.

Nothing regresses against the base. The fix changes words only, and only on
rows the check calls BROKEN before and after.

Three findings are new, and all three are paperwork under `seal/`, so they
are ⬜ corrections and stay out of `Needs a fix`:

- **⬜ 1.** A1 and the changelog bullet say *both commands* name how many
  places hold. In CU, a claim tie among places the declaration rule is unsure
  of, `--reverify` still names an unsure place (first pass ⬜ 2, deferred to
  #809). The records claim more than the code does in that one cell.
- **⬜ 2.** The changelog bullet says the two commands *used to say none
  did*. In 0.18.2 `--reverify` said nothing for a claim tie, which the same
  bullet's previous sentence states. The no-hit line it describes existed
  only on this branch, between #808 and #810.
- **⬜ 3.** The `survivors.md` intro paragraph describes only its first two
  rows. It says every place below shares words with sentences a helper move
  reworded and *is true as it stands*. The five new rows are about #810 and
  are true of 1c3178a1, not of the tree now.

The smith's account was read in full: the three commit messages, A1's new
clause and evidence, the changelog bullet, the phase-3 paragraph and the five
survivor rows. Each claim is answered below against the code at 7e12e538.

## Findings from execution

### #810 closed — the tie cells, old against new

Executed with a probe driver loading the 272ffa32 and 7e12e538 copies of
`evidence_check.py` side by side. Each lone cell is one fragment or released
row that carries the shape's coordinate and a drifted `other`. It ran with
and without `Ledger frozen from`, dated (`--checked 2026-04-01`) and undated,
through the CLI: `--strict` before, `--reverify`, `--strict` after. Each held
cell is round 3's structure. R1 is released, A (2026-02-01) records the
shape's hash and carries `other`, and B (2026-03-01) records what exactly one
place holds. `reverify` is called with MOVES captured, then `--strict` runs.

| Cell | 272ffa32 | 7e12e538 |
|---|---|---|
| S1, claim, 2 of 2 places hold, lone, all 8 arms | check: the no-hit detail; `--reverify`: the no-hit `left` line | check: `locator is ambiguous — 2 places: 1-3, 10-12 (2 hold the recorded content, a tie it cannot break)`; `--reverify`: `2 places, 2 holding the recorded content, a tie the recorded hash cannot break — left` |
| claim, 2 of 3 hold, lone, all 8 arms | the same no-hit wording | `3 places, 2 holding …, a tie the recorded hash cannot break — left`; check `(2 hold …, a tie it cannot break)` |
| C4, held, dated, frozen and not | the no-hit `left` line | `3 places, 2 holding the recorded content, a tie the recorded hash cannot break — left`; MOVES identical |
| C4, held, undated | no line | no line, identical |
| CU, claim over 3 unsure places, 2 hold, lone, unfrozen arms | `only a place the declaration rule is unsure of — left` | the same `--reverify` line; the check now `(2 hold …, a tie it cannot break)` |
| CU, lone, released row under the freeze | the frozen `LEFT` line quotes the no-hit detail | the frozen `LEFT` line quotes `(2 hold the recorded content, a tie it cannot break)`, then the `Corrected ·` remedy |
| CU, held, dated | `only a place … unsure of — left` | identical `--reverify`; the check's detail follows the fix |

Verdicts, exit codes and MOVES are identical in every tie cell. Only words
moved. CU's `--reverify` line is unchanged, which is first pass ⬜ 2,
deferred to #809. It is answered here only because A1 and the changelog now
claim otherwise (⬜ 1).

**Red first, executed.** The two pins
`test_a_held_claim_two_places_tie_on_a_dated_row_is_left_and_named` and
`test_reverify_names_a_claim_two_places_hold_as_the_check_does` are both red
with the 272ffa32 script swapped into the clone (2 failed) and green at
7e12e538. Three mutants, each reverted after its run, back A1's
`bin/mutation-check` claim at the sites it names:

- the ordinary path's call passing `0` for the count: the content-pointing
  case is red;
- the `unplaced` loop's call passing `0`: the dated held case is red;
- `classify`'s `if hit` made `if False`: the content-pointing case is red at
  its check-side assertion.

**Read.** `hit` reaches `left_because` non-empty only for a claim with two or
more hits. A row with no claim and any hit, or with exactly one hit, returns
before the call in all three places: `classify` narrows at `:1734`, and both
`reverify` sites `continue` from `:3406` and `:3638`. So `holding` is never 1,
and `1 holding` cannot print. The third call site, at `:3494`, is reached
only with `places` empty and no claim. `left_because` answers there before
it reads `holding`, so leaving that call without the count is correct. The
ordinary path's new `hit = []` stops a `hit` from an earlier loop iteration
reaching a later row.

### Every non-tie wording is byte-identical — executed

136 cell-arms, all identical between 272ffa32 and 7e12e538 (stdout of all
three commands, exit codes, MOVES):

| Shape | Arms |
|---|---|
| no claim: 2 places, 1 holds · 2 identical places, both hold · 2 places, none holds (the `0.4.0.md:20` shape) | lone × fragment or released × freeze or not × dated or not |
| claim: 3 places, 1 holds · 2 places, none holds | the same |
| no place · one sure place drifted, with and without a claim | the same |
| unsure, no claim: holds · none holds and no destination · heals to one destination | the same |
| unsure, claim: holds · none holds (C8's shape) · 3 places, 0 hold (CU0) · 3 places, 1 holds | the same |
| held: p1 · C6 · C5 · CU0 | freeze or not × dated or not |

In the held tie cells' `--strict` after, R1's no-claim coordinate prints
`locator is ambiguous — 3 places: … (none holds the recorded content)` at
7e12e538. That is the major-level, no-hit message `0.4.0.md:20` quotes,
still printed and unchanged.

### The narrow run and the ledger

- `bin/test -q tests/test_a_released_row_is_read_again_in_a_fragment.py
  tests/test_a_row_points_by_content.py` in the clone at 7e12e538: 710 passed.
  The orchestrator's 972 adds the hygiene modules, which this pass did not
  run.
- `bin/evidence-check --strict .` in the clone: exit 0, `5720 ok · 0 drifted
  · 0 broken`.
- `survivor_check.py --range 272ffa32..7e12e538`: without the exemption file,
  exit 1 and five places, all in `post-review-check.md`. With this item's
  `survivors.md`, exit 0 and `every survivor is excused by a row above (5)`.

## Findings from reading

### The seven new `Re-read ·` claims, against 7e12e538

The class, by construction: every row that cited
`skills/evidence-check/scripts/evidence_check.py#classify` at `7b14fd27`.
These are `0.18.0.md:21` (L1) and the six `Re-read ·` rows at `0.18.0.md:38`,
`:39`, `:40`, `:43`, `:44` and `:51`, which re-read H1 and the five 0.4.0 and
0.9.0 rows. Seven rows, and the fragment carries a `Re-read ·` row for each,
at `classify@aaf71391`. The other `classify@` citations in `seal/releases/`
name units in other scripts.

| Released row | Verdict | Grounds |
|---|---|---|
| `0.16.0.md:61` H1 | holds | the fix adds no line split; `hit` is computed by `recorded_here`, which slices `gfm_lines` |
| `0.18.0.md:21` L1 | holds | the family view is untouched; every verdict is identical old against new, in the held cells included |
| `0.4.0.md:18` | holds | the drift path is untouched; the drifted-unit cells are identical |
| `0.4.0.md:20` | holds | executed: the no-claim, no-hit message it quotes is byte-identical; a claim's tie still stands, BROKEN, now named as one |
| `0.4.0.md:58` | holds | the unsure-place BROKEN and the heal onto one destination are identical, executed |
| `0.4.0.md:66` | holds | the unsure-place detail with each place's hash is untouched; the held CU cell prints `2-2@…; 3-3@…; 4-4@…` at 7e12e538 |
| `0.9.0.md:89` R2 | holds | record stamps go through the same `classify`; only a claim tie's words changed |

The phase-3 paragraph says the same, and its sentence on `0.4.0.md:20` is
true: that wording is byte-identical, executed.

### The five `survivors.md` rows

| Excused place | True of what it describes |
|---|---|
| `post-review-check.md:38`, 🟡 1's description | yes; the line at 1c3178a1, the same code as 272ffa32, executed |
| `:77`, the executed S1 output | yes; the 272ffa32 copy printed exactly that line for S1 |
| `:129`, the p1 row | yes, and still true now: p1 has no hit and its cell is identical old against new, executed |
| `:299`, 🟡 1's verdict row | yes; it states the defect at 1c3178a1 |
| `:394`, the removed line in the paste-ready diff | yes; a diff's `-` line is the old text by construction |

Each quote is excused by grounds that hold. The file's intro paragraph does
not cover these rows (⬜ 3).

### ⬜ 1 — A1 and the changelog say both commands name the count, and in CU `--reverify` does not

`seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md:1`
(A1) and `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md:41`.

A1 now reads *a claim two places hold is named `left` with its BROKEN part
on any row, as the check calls it BROKEN, and both commands say how many
places hold the recorded content, a tie the recorded hash cannot break*. The
changelog says *Both commands now say how many places hold the content*.

Executed in CU, a claim over three places the declaration rule is unsure of,
two of which hold the recorded content. The check says `(2 hold the recorded
content, a tie it cannot break)`, and `--reverify` says `only a place the
declaration rule is unsure of — left`. `left_because` answers `resurrected`
before it reads the count (`skills/evidence-check/scripts/evidence_check.py:914`).

**Why it matters.** The code's gap is the first pass's ⬜ 2, already deferred
to #809. The new part is that a released ledger clause and a release note
assert the opposite in that cell. Whoever picks up #809 reads A1 as saying
the cell is already done. No verdict is wrong.

**Against the base.** No regression. At a3aa139a `--reverify` printed
nothing for any claim tie.

### ⬜ 2 — the changelog says `--reverify` used to say no place held the content, and in 0.18.2 it said nothing

`seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md:43`.
*Both commands now say how many places hold the content … where they used
to say none did.* The check did say that. `--reverify` printed nothing for a
claim tie at a3aa139a, which the same bullet's previous sentence states:
*`--reverify` read it as unchanged and said nothing*. The no-hit `left` line
for a tie existed only on this branch, between 2dc03a12 and 2c9ae970, and no
release carried it. A release note compares against the last release, so the
bullet contradicts itself for a reader of 0.18.3.

### ⬜ 3 — the `survivors.md` intro describes only its first two rows

`seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/survivors.md:3`.
The paragraph says the range moved a case's tree into a helper, and that
*the places below share words with the sentences that moved, and each is
true as it stands*. The five rows 7e12e538 adds are about #810's wording, not
the helper move. Four of them are true of 1c3178a1 and not of the tree now,
as their own grounds say. The rows are right, and the paragraph above them
no longer is.

## Regression tests to plant

None new. The two pins named above are the tie's tests, and both were seen
red against 272ffa32 and under the three mutants. CU's wording has no pin;
that belongs to #809, where the cell is decided.

## Facts to feed into the evidence ledger

- **A1**: narrow the tie clause to places the declaration rule is sure of,
  or name CU as #809's (⬜ 1). This changes no hash.
- **`0.4.0.md:20`**: unaffected. The message it quotes is byte-identical at
  7e12e538, executed.
- The seven `Re-read ·` rows' `classify@aaf71391` is current, and `--strict`
  exits 0.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | the first pass's yellow 1 (#810) is closed — a claim tie is named by how many places hold the recorded content, in the check and at both `reverify` sites | `skills/evidence-check/scripts/evidence_check.py:903` | confirmed | S1, the 2-of-3 claim and C4 executed at 272ffa32 and 7e12e538 in every arm; verdicts, exits and MOVES identical, only the reason changed; both pins red at 272ffa32 and under three mutants |
| 🟢 | every non-tie wording is byte-identical to 272ffa32, the major-level no-hit message `0.4.0.md:20` quotes included | `skills/evidence-check/scripts/evidence_check.py:1742` | confirmed | 136 cell-arms executed, all identical |
| 🟢 | the seven new `Re-read ·` claims hold at 7e12e538, and they are the whole class of rows citing the old `classify` hash | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md:38` | confirmed | each claim read against the code and the probe cells; the class enumerated from every `classify@7b14fd27` citation; `--strict` exit 0 |
| 🟢 | the five `survivors.md` rows each excuse a place true of the commit it describes | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/survivors.md:13` | confirmed | each place read; `survivor_check.py` over the range exit 1 without the file, 0 with it |
| ⬜ 1 | A1 and the changelog say both commands name how many places hold; in CU, a claim tie among unsure places, `--reverify` names an unsure place | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md:1` | open | CU executed: the check names the count, `--reverify` does not; a correction to the records, with the code gap already #809's |
| ⬜ 2 | the changelog says `--reverify` used to say no place held the content; in 0.18.2 it said nothing for a claim tie | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md:43` | open | the bullet's previous sentence says so; the first pass executed a3aa139a silent for S1; a correction to the release note |
| ⬜ 3 | the `survivors.md` intro describes only the helper move and calls every place true as it stands; the five new rows are #810's and true of 1c3178a1 | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/survivors.md:3` | open | read; a correction to a process record |
| carried | the first pass's white 2 — a claim tie among unsure places is described as one unsure place | `skills/evidence-check/scripts/evidence_check.py:914` | deferred #809 | already deferred in post-review-check.md; CU executed again here, unchanged |
| ❓ | the full suite, the repository lint and the typecheck at 7e12e538 | the branch | ❓ out of verified scope | not this pass's to run; the sealer answers it |

## Executed probes

| What was run | Result |
|---|---|
| a driver over 18 lone shapes × fragment or released × freeze or not × dated or not, and 6 held shapes × freeze or not × dated or not, at the 272ffa32 and 7e12e538 copies of `evidence_check.py` | 168 cell-arms: 140 identical, 28 differing, all 28 tie cells and only in the reason's words |
| the two tie pins with the 272ffa32 script swapped into the clone | 2 failed; 2 passed at 7e12e538 |
| three mutants (ordinary-path count, `unplaced` count, the check's `if hit`), each reverted after its run | each turns one pin red |
| `bin/test -q` over the two modules the prompt names, in the clone at 7e12e538 | 710 passed |
| `bin/evidence-check --strict .` in the clone at 7e12e538 | exit 0, `5720 ok · 0 drifted · 0 broken` |
| `survivor_check.py --range 272ffa32..7e12e538`, without and with this item's `survivors.md` | exit 1 with five places; exit 0 with all five excused |
| the full suite, the lint and the typecheck (the broad gate) | not yet |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a claim tie among unsure places is described as one unsure place (first pass ⬜ 2) | #809 | already deferred in post-review-check.md; the evidence-check maintainer decides #809's design |
| an unsure place with a claim is handed a BROKEN part where the check reads DRIFTED (C8) | #809 | already deferred in round 3; the evidence-check maintainer |
| a non-citation ledger coordinate whose file walks first is left drifted | #806 | already deferred in round 2; the evidence-check maintainer |

## Paste-ready fixes

### ⬜ 1

A1's clause, in the fragment's row 1, and the changelog's sentence:

```
- … as the check calls it BROKEN, and both commands say how many places hold the recorded content, a tie the recorded hash cannot break; …
+ … as the check calls it BROKEN, and among places the declaration rule is sure of both commands say how many places hold the recorded content, a tie the recorded hash cannot break; …
```

### ⬜ 1 and ⬜ 2, the changelog bullet's last sentence

```
-  line and records the BROKEN in a signatory's pact changes. Both commands
-  now say how many places hold the content, a tie the recorded hash cannot
-  break, where they used to say none did (#810).
+  line and records the BROKEN in a signatory's pact changes, saying how many
+  places hold the content, a tie the recorded hash cannot break. The check
+  says so too, where it used to say no place held it (#810).
```

### ⬜ 3

```
-moved, and each is true as it stands.
+moved, and each is true as it stands. The rows from the third on excuse
+places in this item's first verifying pass that quote the claim-tie wording
+#810 corrected; each is true of the commit it describes.
```

Needs a fix: no

Loses a record or crashes: no

The three ⬜ are corrections to records under `seal/` and commission no fix.
Nothing in this pass leaves open a finding that needs a fix, so the broad
gate comes due. The sealer's spawn is what comes due next, after the
orchestrator applies or declines the three corrections. The broad gate's
last run is `not yet`.

This report does not quote the claim-tie wording #810 removed. It names that
wording as *the no-hit line*, so a later `survivor_check.py` over the range
does not need a `survivors.md` row for this file.

## Proof block

Ran by specseal:warden on claude-opus-5-5, in a `git clone --no-local` of the
worktree checked out at 7e12e538, under this pass's scratchpad directory. The
probe driver (one file under the agent contract's probe prefix), the two
script copies, the probe trees and outputs, and the clone ran once and were
removed before handover. The three mutants were reverted with `git checkout`
in the clone after each run, and the clone was clean before it was removed.

Files opened:

- the diff 272ffa32..7e12e538, every file in it
- `post-review-check.md` of this item, in full
- `skills/evidence-check/scripts/evidence_check.py` at 7e12e538:
  `recorded_here`, `left_because`, `minor_region`, `classify`'s tie and
  unsure branch, and `reverify`'s ordinary path (`:3385-3525`) and `unplaced`
  loop (`:3600-3680`)
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: its helpers,
  `frozen`, and the held-coordinate cases from `:3209` to `:3480`;
  `tests/test_a_row_points_by_content.py`: `run`, `repo` and the content-pointing
  tie case
- `tests/test_a_corrected_sentence_survives_elsewhere.py`'s docstring;
  `skills/code-review/scripts/survivor_check.py`'s `main`
- this item's `survivors.md`, `changelog.md`, the phase-3 diff, and the
  ledger fragment's A1 and new `Re-read ·` rows
- `seal/releases/0.16.0.md:61`, `:81`; `0.18.0.md:21`, `:38`, `:51`;
  `0.4.0.md:18`, `:20`, `:58`, `:66`; `0.9.0.md:89`; `0.18.2.md:75`;
  `0.9.3.md:49`
- `bin/test`, `seal/config.md`

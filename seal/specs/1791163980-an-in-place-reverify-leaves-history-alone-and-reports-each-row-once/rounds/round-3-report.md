# Round 3 report — an in-place `--reverify` leaves history alone and reports each row once

| Field | Value |
|---|---|
| Round | 3 (verifying round 2's fixes; the item's last round) |
| Target SHA | 7f4672a3 |
| Fix range checked | 930078de..4d510880, 3 commits |
| Base | `release/v0.18.3` at a3aa139a |
| Pull request | #801 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

## What this round was asked, and what it found

The target is round 2's fix range. Round 2's yellow 1 is closed for the
shape it named. p6 is silent again at the target, with the freeze and
without it, and A alone or beside a newer holder. Round 1's p1 and p2 hold
as round 2 left them. The `still` call the smith removed was equivalent:
the target and a copy with the call put back gave identical output, MOVES,
exit codes and `--strict` verdicts in all 49 probe cells.

The `unplaced` loop was then judged by construction over what a held
coordinate's places can hold. It now agrees with the check in most cells.
It disagrees in three, and they are not all the same kind:

- **🟡 1, a regression against the base.** One place the declaration rule
  is unsure of, none holding the row's hash, no claim, and the row's content
  living as one unit elsewhere. The base heals the coordinate onto that
  destination, and `--strict` after exits 0. The target names it `left` and
  hands MOVES a BROKEN part, and `--strict` after exits 2. The cause is that
  the loop never does the destination scan the ordinary path does. This has
  been the case since phase 1, and rounds 1 and 2 missed it.
- **🟡 2, pre-existing at the base.** A claim coordinate whose minor content
  two or more places hold. The check calls it BROKEN and `reverify` says
  nothing, on any row, base included. The loop copied that rule from the
  ordinary path. On a dated row this is round 1's yellow 1 again for one
  sub-cell: the run's own date turns the family BROKEN, and the run says
  nothing.
- **⬜ 3, pre-existing, a design question.** An unsure place with a claim
  that does not hold the row's hash. The check calls it DRIFTED, while
  `reverify` leaves it and hands MOVES a BROKEN part. That follows from the
  rule that `reverify` never writes onto an unsure place.

⬜ 4 collects the paperwork that rests on these three.

The smith's account was read in full: the three fix-range commit messages,
A1 as extended, the phase-3 grounds for `0.4.0.md:59` and `0.18.2.md:129`,
the overview's changed row, the spec's D1 sentence and the changelog. Each
claim used below was checked against the code at the target.

## Findings from execution

### 🟡 1 — a held coordinate whose only place is one the declaration rule is unsure of is left BROKEN on a dated row, where the base healed it onto its destination

`skills/evidence-check/scripts/evidence_check.py:3599-3623`, the `unplaced`
loop. This is a regression against a3aa139a.

The ordinary path reads such a coordinate in two steps. At `:3394-3398` an
unsure place that does not hold the recorded hash becomes no place. Then at
`:3399-3479`, for a coordinate with no claim, it runs `content_matches`. If
exactly one unit anywhere reconstructs the recorded hash, the row is
re-pointed there (`identical content`). Only when no destination is
provable does it say `left`. The loop's comment says it reads the
coordinate *as the ordinary path reads such a coordinate*, but it stops
after `left_because` and never scans.

**Probe C10 (executed).** This is the shape resurrection exists for.
`handler` moved out of `src/lib.go` into `src/moved.go` and left
`return handler(1)` behind. B, dated 2026-03-01, recorded that unsure call
line by hand, which is what the check's own detail advises (*record one by
hand if it is still the unit*), so the family holds `src/lib.go#handler`.
A, dated 2026-02-01, recorded the unit's content, which now lives in
`src/moved.go`, and A also carries `other`, which drifted. The run was
`--reverify --checked 2026-04-01 .`.

| | base a3aa139a | round 2 fceff8ce | target 7f4672a3 |
|---|---|---|---|
| line for A's `handler` | `src/lib.go#handler -> src/moved.go#handler  (identical content)` | `its row is dated by this run, and no one place holds it — left` | `only a place the declaration rule is unsure of — left` |
| A after the run | carries `src/moved.go#handler`, dated | carries `src/lib.go#handler`, dated | the same as fceff8ce |
| MOVES for A's `handler` | no BROKEN part | a BROKEN part | a BROKEN part |
| `--strict` after | 0 | 2: A BROKEN *… identical content at src/moved.go#handler (moved?)*, B and R1 DRIFTED | 2, as fceff8ce |

A second run heals it. On that run A is the newest reading and does not
hold, so the coordinate is not held, and it goes down the ordinary path.
So one run leaves the tree red where the base left it clean, and the first
run writes a BROKEN pact-change part that the second run then contradicts.
That is the same shape round 1's yellow 2 was opened for.

In the same cell, the target's `left` line with no destination drops the
ordinary path's `, and no destination is provable` (C7 in the matrix).

**Why it matters.** In a signatory repository the BROKEN part becomes a
permanent `seal/pact-changes/` row for a coordinate the base re-pointed
cleanly (read: `record_pact_changes` keeps any part whose two hashes
differ). The check names the remedy, `(moved?)`, and the run that could
apply it declines on the first pass.

**The fix (applied in the clone).** It does in the loop what the ordinary
path does for an unsure place with no claim: scan, re-point onto one
destination, and otherwise say `, and no destination is provable`. With it,
C10 re-points A and `--strict` after exits 0, as at the base. C7's line
takes the base's wording. The other 47 probe cell-arms are byte-identical
to the target. The case under *Regression tests to plant* is red at the
target and green with the fix. The three narrow modules pass with the fix,
693 tests.

A deeper fix is to move the ordinary path's per-coordinate body into one
function that both callers use, so the loop cannot drift from it again.
That moves about 170 lines, and the targeted fix below is the smaller
change.

### 🟡 2 — a claim coordinate whose minor content two places hold is BROKEN to the check and silent to `reverify` (pre-existing)

`skills/evidence-check/scripts/evidence_check.py:3382-3393` (the ordinary
path) and `:3609-3616` (the loop, which copies it).

`classify` (`:1725-1727`) settles a tie between places by the recorded
hash, but only when exactly one place holds it for a claim row:
`hit and (len(hit) == 1 or not claim)`. Two unrelated units can share one
identical statement line, so a claim's minor hash in two places is not a
choice, and the check calls it BROKEN (`locator is ambiguous … (none holds
the recorded content)`). Both `reverify` paths ask only whether *any*
place holds the hash. They answer `still`, or in the loop just `continue`,
and print nothing.

**Probe S1 (executed), no family.** A single released row
`src/service.py#handler>"y = x"` at the hash of `    y = x + 1`, where two
`handler` units each hold that line. `--strict` before the run exits 2,
BROKEN. `--reverify --checked 2026-04-01 .` exits 0 and prints nothing for
`handler`. The output is identical at a3aa139a, fceff8ce and 7f4672a3. This
is a flagged row answered with silence, at the base.

**Probe C4 (executed), the dated row.** Three `handler` units, the first
two with `y = x + 1` and the third with `y = x + 9`. B holds the claim at
the third. A, older, records the first two's line and carries `other`,
which drifted.

| | base | fceff8ce | target |
|---|---|---|---|
| line for A's `handler` | none (no freeze: only R1's own line) | `its row is dated by this run … — left` | none |
| MOVES for A's `handler` | none | a BROKEN part | none |
| `--strict` after | 2, A BROKEN | 2, A BROKEN | 2, A BROKEN |

So the run's own date makes A the family's newest reading, and the family
turns BROKEN. Without the freeze the target says nothing about `handler`
at all and exits 0. That is round 1's yellow 1 again for this one
sub-cell. fceff8ce named it, and round 2's fix silenced it again.

For A's own row the target does what the base does, so this is not a
regression against the base. The code comment at `:3593-3598` and the
overview's grounds say that where a place holds the recorded content
*the check calls it OK*, which is false in this cell (⬜ 4).

**The fix (applied in the clone).** Apply `classify`'s rule at both sites.
With it, S1 prints `2 places, none holding the recorded content — left`.
C4 prints `3 places, …` and hands MOVES the BROKEN part, matching the
check's verdict and its wording. Every other probe cell is unchanged. The
three narrow modules and `tests/test_a_row_points_by_content.py`, which
holds the round-7 and round-8 `reverify` cases, pass with both fixes, 906
tests. Fix both sites or neither. Fixing the loop alone would make one
`reverify` answer a claim tie two ways, depending on whether a family
holds it.

### The `unplaced` loop, cell by cell

Executed in all cells: A dated 2026-02-01 carrying `other`, which drifted;
B newer where named; with the freeze and without it; dated
(`--checked 2026-04-01`) and undated. Each cell was run at a3aa139a,
0667af2e, fceff8ce, the target, and the target with `still` put back. The
check's verdict is `--strict` after the run, on A's row.

| What the held coordinate's places hold | Target, dated row | Check on A after | Agrees | Against the base |
|---|---|---|---|---|
| two places, one holds A (p6, A alone and beside B) | silent, no part | OK, exit 0 | yes | same |
| two identical places, both hold A (C3) | silent | OK | yes | same for A |
| two places, neither holds A (p1) | `2 places, none holding the recorded content — left`, BROKEN part | BROKEN `locator is ambiguous — 2 places … (none holds …)` | yes | same |
| claim, two places, one holds A (C5) | silent | OK | yes | same |
| claim, two places, none holds A (C6) | `2 places, none holding … — left`, BROKEN part | BROKEN, ambiguous | yes | same |
| claim, three places, two hold A (C4) | silent | BROKEN, ambiguous | **no** (🟡 2) | same silence for A |
| unsure place holds A, no claim (C9) and with a claim (C9b) | silent | OK | yes | same for A |
| unsure place, none holds A, no claim, no destination (C7) | `only a place the declaration rule is unsure of — left`, BROKEN part | BROKEN `the declaration rule is unsure of the only place …` | verdict yes; drops `, and no destination is provable` | wording only |
| the same, with one destination elsewhere (C10) | left, BROKEN part | BROKEN *(moved?)* | verdict yes, heal lost | **regression** (🟡 1) |
| unsure place, none holds A, with a claim (C8) | `only a place the declaration rule is unsure of — left`, BROKEN part | DRIFTED `content changed at 2-2` | **no** (⬜ 3) | same |
| no place, the file unreadable, the path escapes | unreachable as held (read) | — | — | — |
| a coordinate no family holds (C0, control) | ordinary path | BROKEN `locator not found` | yes | identical at all five copies |

- **Undated row** (executed, every cell, both freeze arms). The target
  prints no line and hands MOVES no part for A's `handler`. A stays an
  outranked reading, so the check's verdict on the family is unchanged.
- **Freeze or not.** Every cell answers the same in both arms. Only the
  family `LEFT` line differs: under the freeze it is the frozen arm's own
  line, which names the released row.
- **Why the last three cells are unreachable** (read). A coordinate is held
  only where a newest reading grades `OK` (`family_view`, `:2630`). The
  following three cases read BROKEN or EXTERNAL for every reading, so no
  family holds such a coordinate, and it never reaches `unplaced`:
  - `classify` returns BROKEN for an escaping path (`:1669`).
  - A file that will not read is BROKEN or EXTERNAL (`:1672-1705`).
  - No place at all is BROKEN (`:1740-1774`).

  Nothing in the run writes code, so a file cannot turn unreadable between
  the judgment and the loop.

### Round 2's findings, re-checked at the target

**Round 2's yellow 1 — closed** (p6 re-run, executed). Both variants, with
the freeze and without it:

| | base | 0667af2e | fceff8ce | 7f4672a3 |
|---|---|---|---|---|
| line for `handler` | none | none | `its row is dated by this run, and no one place holds it — left` | none |
| MOVES for `handler` | none | none | `('src/service.py#handler', 'd06d1b56', None)` | none |
| `--strict` after | 0 | 0 | 0 | 0 |

The planted case
`test_a_held_coordinate_one_of_whose_places_holds_it_rides_a_dated_row_silently`
and the dated arm of
`test_a_held_coordinate_with_two_places_on_a_dated_row_is_left_and_named`
are both red with 930078de's `evidence_check.py` and green at the target.
That was run by this round, six selected cases.

**The `still` call removed in c4c6a73e — equivalent, confirmed.**

- Read: a key reaches the loop on every walk or on none. `holds`, `place`
  and `current_hash` are fixed for the run. Line numbers are stable,
  because a walk rewrites cells, not lines. The coordinate's own hash is
  never rewritten, because it is never in `edits`. So the loop gives one
  key the same answer on every dated walk. The silent branch never meets a
  key that an earlier walk gave an outcome or a part. `still` then only
  writes an outcome whose `why` is None, which nothing prints, and it
  touches `parts` only where a part exists.
- Executed: a copy of the target with
  `still(key, m.group("hash"))` restored before the `continue` gave output
  identical to the target in all 49 cell-arms.

**Round 2's white 2 — answered, confirmed with a remainder** (read).

- A1 carries *unless one of its places holds what the row recorded, which
  reads as unchanged and records nothing*. That is true of the code at the
  target.
- The re-read rows cite `reverify@6c5d8937`, which
  `bin/evidence-check --strict .` reads as current.
- The phase-3 grounds for `0.4.0.md:59` and `0.18.2.md:129` carry the
  round-2 qualifier.

The remainder is ⬜ 4: A1 needs the heal clause once 🟡 1 lands, and the
`0.4.0.md:59` verdict *holds* is false in S1's cell, at the base as at the
target.

**Round 2's white 3 — carried, deferred to #806** (read: open, titled for
the walk-order shape). Nothing in this range touches `cited_first`.

### Round 1's findings, re-checked at the target

**Round 1's yellow 1 — closed** (p1 re-run, executed).

- With the freeze and without it, A's `handler` prints
  `2 places, none holding the recorded content — left`, the check's own
  terms, as at the base.
- MOVES gets `('src/service.py#handler', '96c68feb', None)`.
- Without the freeze, the family line reads *this run left
  src/service.py#handler where it stands, and the line naming it above
  says why*.
- `--strict` after exits 2 at all four SHAs, with A BROKEN in the same
  words.

**Round 1's yellow 2 — closed** (p2 re-run, executed, unnarrowed). The
target and fceff8ce exit 0 and `--strict` exits 0. They write the same
three files the base writes: B, `0.1.0.md` and `0.2.0.md`. At 0667af2e the
run exits 1 and `--strict` exits 2.

**Round 1's yellow 3 — carried** (read). This range does not touch
`docs/the-evidence-ledger.md`. The `left`-reasons sentence still covers the
loop's lines, because *no one place holding the unit* is what
`left_because` reports. After 🟡 1, a heal is a re-point, which the
sentence does not need to name.

**Round 1's white 5 — carried** (read). This range adds one `place`, one
`read` and one `resolve_unit` per held coordinate with no one place, on a
dated row only. No `family_view` pass was added.

### A1, the two re-reads, and the changelog

- **A1** (read against the code). Every clause is true of the target's
  code. With 🟡 1 the clause *named `left` and handed MOVES a BROKEN part
  where it does* needs *or re-pointed onto the one destination that
  reconstructs its hash, where the declaration rule is unsure of its only
  place*. With 🟡 2, *unless one of its places holds* needs *(for a claim,
  exactly one)*.
- **`0.4.0.md:59`** says `--reverify` *never contradicts the check's
  verdict, and never answers a flagged row with silence*. S1 shows a
  flagged row answered with silence at the base and the target. C8 shows a
  BROKEN part where the check says DRIFTED. The phase-3 grounds *every
  flagged row still gets a line* are false in S1's cell. This branch did
  not make it false, but its re-read on 2026-10-05 says the claim holds
  (⬜ 4).
- **`0.18.2.md:129` (C1)** says a record row is appended *per such row with
  a BROKEN coordinate*. That holds of what `reverify` itself calls BROKEN
  in every cell (read). Where `reverify` and the check differ (C4, C8,
  C10), the record follows `reverify`, which is 🟡 1, 🟡 2 and ⬜ 3, not a
  separate defect in C1.
- **`changelog.md`** says what ships at the target, with one exception. In
  *where no one place holds it, it is named `left` and recorded BROKEN, as
  any such coordinate is*, the words *as any such coordinate is* are false
  in C10, where any such coordinate the ordinary path reads is re-pointed.
  Once 🟡 1 lands, the sentence is exact and needs no edit.

## Findings from reading

### ⬜ 3 — an unsure place with a claim is handed a BROKEN part where the check says DRIFTED (pre-existing, deferred)

`skills/evidence-check/scripts/evidence_check.py:3394-3398` (the ordinary
path) and the loop's `left_because` call, executed as C8. The two rules
conflict:

- `classify` keeps an unsure place for a claim row and reads it DRIFTED
  (`:1720-1721`, round 8).
- `reverify` treats it as no place and refuses to write onto it, which is
  the round-6 rule `0.4.0.md:59` states first.

The printed reason is accurate. What disagrees is the kind of record: the
pact-change record gets BROKEN where the check says DRIFTED. The output is
identical at the base. Whether `reverify` should hand such a coordinate a
DRIFTED-shaped part, or no part at all, is a design question for the
evidence-check maintainer. It is not a fix this item can choose.

### ⬜ 4 — paperwork that rests on 🟡 1 and 🟡 2

These are corrections, not fixes:

- **The code comment at `evidence_check.py:3593-3598`.** It says *where one
  of its places holds what this row recorded, the check calls it OK*. That
  is false for a claim tie (🟡 2).
- **`overview.md`'s row *A held coordinate no one place holds*.** Its
  grounds say *the check calls it OK, and the run agrees*, which is false
  in the same cell.
- **`spec.md` D1's sentence.** It needs the same qualifier.
- **A1.** It needs the two clauses named above.
- **The `0.4.0.md:59` re-read.** It says the claim holds. S1 makes
  *never answers a flagged row with silence* false at the base and the
  target. Either the fix for 🟡 2 lands and the re-read stands, or the row
  becomes a `Corrected ·` naming the claim tie and the unsure claim place.

## Regression tests to plant

Destination: `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
after
`test_a_held_coordinate_one_of_whose_places_holds_it_rides_a_dated_row_silently`.

The case is in the 🟡 1 fence under *Paste-ready fixes*. I saw it red at
the target, where the assertion on the re-point line fails with
`only a place the declaration rule is unsure of — left` in the output. I
saw it green with the fix applied in the clone. The fix pass shows it red
again before committing it (§15).

For 🟡 2, S1 above is the case to plant. It goes in
`tests/test_a_row_points_by_content.py` beside the round-7 claim cases if
the fix lands, and is red at the target because nothing is printed.

## Facts to feed into the evidence ledger

- **A1**, the clause on a held coordinate with no one place: *… and named
  `left` and handed MOVES a BROKEN part where it does, or re-pointed onto
  the one destination that reconstructs its hash where its only place is
  one the declaration rule is unsure of, unless one of its places (for a
  claim, exactly one) holds what the row recorded …*. Add the 🟡 1 case to
  A1's grounds.
- **The phase-3 grounds for `0.4.0.md:59`.** They need the claim-tie cell:
  *a claim row whose minor content two places hold is BROKEN to the check
  and was silent to `--reverify` before this item too*. Alternatively,
  🟡 2's fix lands and the grounds stand.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a held coordinate whose only place is one the declaration rule is unsure of, on a row the run dates, is named `left` and handed a BROKEN part where the base re-pointed it onto its one provable destination; `--strict` after exits 2 where the base exits 0, and the loop's line drops `, and no destination is provable` | `skills/evidence-check/scripts/evidence_check.py:3599` | open | C10 executed at a3aa139a, fceff8ce and the target; a regression against the base since phase 1; the fix and its case executed in the clone, red at the target and green with the fix, 693 passed in the three narrow modules |
| 🟡 2 | a claim coordinate whose minor content two or more places hold is BROKEN to the check and silent to both `reverify` paths; on a dated held row the run's own date turns the family BROKEN with no line | `skills/evidence-check/scripts/evidence_check.py:3382` | open | S1 and C4 executed at a3aa139a, fceff8ce and the target; pre-existing at the base in the ordinary path, which the loop copies; fceff8ce named the dated cell and round 2's fix silenced it again; the fix executed in the clone, 906 passed in four modules |
| ⬜ 3 | an unsure place with a claim that does not hold the row's hash is left with a BROKEN part, where the check reads it DRIFTED | `skills/evidence-check/scripts/evidence_check.py:3394` | deferred a new issue against `reverify`'s unsure-place rule | C8 executed, identical at the base; the round-6 never-write rule against `classify`'s round-8 DRIFTED; a design question, not this item's |
| ⬜ 4 | the loop's comment, the overview's grounds, spec D1, A1 and the `0.4.0.md:59` re-read say a place holding the recorded content is OK to the check, or that every flagged row gets a line, which a claim tie contradicts | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | open | a correction to the run's paperwork; follows 🟡 1 and 🟡 2 |
| 🟢 | round 2's blocking finding is closed — a held two-place coordinate one place holds is silent on a dated row | `skills/evidence-check/scripts/evidence_check.py:3609` | confirmed | p6 re-run at four SHAs, both variants, both freeze arms; the planted cases red with 930078de's script and green at the target |
| 🟢 | the `still` call removed in c4c6a73e was equivalent | `skills/evidence-check/scripts/evidence_check.py:3613` | confirmed | read: one key takes one branch on every walk; executed: the target and a copy with the call restored identical in 49 cell-arms |
| 🟢 | round 2's white 2 was answered at 4d510880 | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | confirmed | A1's qualifier, the re-stamp at the current `reverify` hash and the phase-3 grounds read; the remainder is ⬜ 4 |
| carried | round 2's white 3, the walk-order shape | `skills/evidence-check/scripts/evidence_check.py:3080` | deferred #806 | already deferred in round 2; #806 is open; this range does not touch `cited_first` |
| 🟢 | round 1's yellow 1 is closed — a held coordinate no place holds, on a dated row, is named in the check's terms | `skills/evidence-check/scripts/evidence_check.py:3617` | confirmed | p1 re-run at four SHAs, both freeze arms |
| 🟢 | round 1's yellow 2 is closed — a held ledger-line coordinate is re-stamped as at the base | `skills/evidence-check/scripts/evidence_check.py:3358` | confirmed | p2 re-run unnarrowed at four SHAs |
| carried | round 1's yellow 3 and white 5 | `docs/the-evidence-ledger.md:189` | confirmed | this range touches neither the sentence nor the family view |
| 🟢 | `0.18.2.md:129` (C1) holds of what `reverify` calls BROKEN | `seal/releases/0.18.2.md:129` | confirmed | read in every probe cell; where `reverify` and the check differ the record follows `reverify`, which is 🟡 1, 🟡 2 and ⬜ 3 |
| 🟢 | `changelog.md` says what ships at the target, but for *as any such coordinate is* in C10 | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md` | confirmed | each bullet read against the code; exact once 🟡 1 lands |
| ❓ | the full suite, the repository lint and the typecheck at the target | the branch | ❓ out of verified scope | not this round's to run; the sealer answers it, after the fixes this round names land or are deferred |

## Executed probes

| What was run | Result |
|---|---|
| p6, round 2's: a held two-place coordinate one place holds, on a row dated for `other`; A alone and beside a newer holder; freeze and not; dated and undated; at a3aa139a, 0667af2e, fceff8ce, 7f4672a3 | target silent with no MOVES part in every arm; fceff8ce alone names it and hands `('src/service.py#handler', 'd06d1b56', None)`; `--strict` after 0 everywhere |
| p1, round 1's: a held coordinate neither of two places holds, dated, at the four SHAs | target: `2 places, none holding the recorded content — left`, BROKEN part `96c68feb`; `--strict` after 2 with A BROKEN at all four; 0667af2e alone silent |
| p2, round 1's: a held ledger-line coordinate, unnarrowed, at the four SHAs | target and fceff8ce exit 0 and `--strict` 0, writing the base's three files; 0667af2e exits 1 and 2 |
| the `unplaced` matrix: 13 cells × freeze and not × dated and undated, at the four SHAs and the target with `still` restored | as the table *The `unplaced` loop, cell by cell*; the target and the `still` copy identical in all 49 cell-arms |
| S1: a claim row two places hold, no family, at a3aa139a, fceff8ce, target | `--strict` 2 before and after, BROKEN ambiguous; `--reverify` exits 0 and prints nothing for `handler`, at all three |
| C10: an unsure place B holds, A's content one destination elsewhere, dated, at a3aa139a, fceff8ce, target | base re-points A to `src/moved.go#handler`, `--strict` after 0; fceff8ce and target leave A with a BROKEN part, `--strict` after 2 |
| the planted held-coordinate cases (`-k "held_coordinate or held_ledger"`, six cases) at the target and with 930078de's script | target: 6 passed; 930078de: the two round-2 cases red, 4 passed |
| 🟡 1's fix in the clone: the matrix, C10, the new case, and the three narrow modules | C10 heals, `--strict` 0; C7 takes the base's wording; 47 other cell-arms identical to the target; the new case red at the target, green with the fix; 693 passed |
| 🟡 2's fix on top, in the clone: the matrix, S1, and the three narrow modules with `tests/test_a_row_points_by_content.py` | S1 and C4 named with the BROKEN part; every other cell-arm unchanged; 906 passed |
| the three narrow modules at the target, unpatched | not run by this round: the orchestrator's run (754 with the three hygiene modules) is the record |
| `bin/evidence-check --strict .` in the worktree at the target, with this report on disk | exit 0 (see the proof block) |
| the full suite, the lint and the typecheck (the broad gate) | not yet |

```
C10 at the target, --reverify --checked 2026-04-01 .
  src/lib.go#handler  only a place the declaration rule is unsure of — left
  seal/ledger/2000000001-a.md:1  Re-read · R1 · handler adds one
--strict after: exit 2
  BROKEN   src/lib.go#handler  the declaration rule is unsure of the only place it found, and none holds the recorded content — 2-2@50d94e97; record one by hand if it is still the unit — identical content at src/moved.go#handler (moved?)

C10 at a3aa139a
  src/lib.go#handler -> src/moved.go#handler  (identical content)
--strict after: exit 0
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| an unsure place with a claim is handed a BROKEN part where the check reads DRIFTED (⬜ 3) | a new issue against `reverify`'s unsure-place rule beside `classify`'s round-8 DRIFTED | the orchestrator files it in the 0.18.3 triage; the evidence-check maintainer decides the design |
| a non-citation ledger coordinate whose file walks first is left drifted (round 2's white 3) | #806 | already deferred in round 2; the evidence-check maintainer |

## Paste-ready fixes

### 🟡 1

`skills/evidence-check/scripts/evidence_check.py`, `reverify`, the tail of
the `for offset, key, m in unplaced:` loop. Replace from the `walked(`
call after the recorded-here `continue` through the `pending.append`
(`:3617-3623`):

```python
            why = left_because(places, resurrected)
            if resurrected and m.group("claim") is None:
                # An unsure place with no claim is no place, and the ordinary
                # path heals it onto the one destination that reconstructs
                # the recorded hash; so does this (round 3).
                raw_path, locator = m.group("path"), m.group("locator")
                hashes, _, _ = content_matches(
                    home, at, locator, m.group("hash"), scan_cache.setdefault(home, {})
                )
                if len(hashes) == 1:
                    path, name, (a, b) = hashes[0]
                    target = body if path == at else read(os.path.join(home, path))
                    new_raw = (
                        raw_path
                        if path == at
                        else (raw_path[: len(raw_path) - len(at)] + path)
                    )
                    shown = f"#{name}" if path == at else f"{path}#{name}"
                    new_hash = content_hash(gfm_lines(target)[a - 1 : b])
                    if new_hash != m.group("hash"):
                        pending.append(
                            (offset, coordinate_of(m), m.group("hash"), new_hash)
                        )
                    else:
                        still(key, new_hash)
                    kept.append(
                        (
                            m.start("path"),
                            m.end("hash"),
                            new_raw
                            + text[m.end("path") : m.start("locator")]
                            + name
                            + text[m.end("locator") : m.start("hash")]
                            + new_hash,
                            (
                                key,
                                f"  {raw_path}#{locator} -> {shown}  "
                                "(identical content)",
                            ),
                        )
                    )
                    continue
                why += ", and no destination is provable"
            walked(key, m.group("hash"), None, f"  {coordinate_of(m)}  {why} — left")
            pending.append((offset, coordinate_of(m), m.group("hash"), None))
```

The case, in `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
after the round-2 case:

```python
LEFT_BEHIND = (
    "func main() {\n    return handler(1)\n}\n\nfunc other(x) {\n    return x * 2\n}\n"
)


def test_a_held_coordinate_with_an_unsure_place_on_a_dated_row_heals_to_its_destination(
    repo, capsys
):
    """Round 3. B holds `handler` in `src/lib.go` through the one place the
    declaration rule is unsure of, the call a move left behind; A records the
    unit itself, which now lives in `src/moved.go`, and carries `other`,
    which drifted. Dated for `other`, A becomes the newest reading of
    `handler`, and the run heals it onto the one destination that
    reconstructs A's hash, as it heals any such coordinate: `--strict` reads
    the tree clean. Red at 7f4672a3, which named it `left` and handed MOVES a
    BROKEN part."""
    lib, dest = "src/lib.go", "src/moved.go"
    (repo / "src" / "lib.go").write_text(LEFT_BEHIND, encoding="utf-8")
    unit = "func handler(x) {\n    y := x + 2\n    return y\n}\n"
    (repo / "src" / "moved.go").write_text(unit, encoding="utf-8")
    places, unsure = ec.resolve_unit(lib, "handler", LEFT_BEHIND)
    assert unsure and len(places) == 1, places
    x, y = places[0]
    held = ec.content_hash(ec.gfm_lines(LEFT_BEHIND)[x - 1 : y])
    a_at = unit_hash(repo, dest, "handler")
    o0 = unit_hash(repo, lib, "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `{lib}#handler@{line_hash('    return handler(0)')}` "
            "| read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    a = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{lib}#handler@{a_at}`, "
            f"`{lib}#other@{o0}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name=A_ITEM,
    )
    b = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{lib}#handler@{held}` "
            "| read | 2026-03-01 | Re-read 2026-03-01 |"
        ],
        name=B_ITEM,
    )
    (repo / "src" / "lib.go").write_text(
        LEFT_BEHIND.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    moves = []
    ec.reverify([str(a), str(b)], str(repo), {}, None, "2026-04-01", moves)
    out = capsys.readouterr().out
    assert f"{lib}#handler -> {dest}#handler  (identical content)" in out, out
    assert [m for m in moves if m[3] is not None and m[4] is None] == [], moves
    assert f"`{dest}#handler@{a_at}`" in a.read_text(encoding="utf-8")
    assert run(["--strict", "."], repo).returncode == 0
```

### 🟡 2

`skills/evidence-check/scripts/evidence_check.py`, `reverify`, the
ordinary path (`:3383-3387`), replacing the list-truth test before the
round-7 comment:

```python
                hit = [
                    p
                    for p in places
                    if recorded_here(rel, body, p, m.group("hash"), claim)
                ]
                if hit and (len(hit) == 1 or claim is None):
```

and the `unplaced` loop (`:3609-3612`), replacing the `any(...)` test:

```python
            hit = [
                p
                for p in places
                if recorded_here(at, body, p, m.group("hash"), m.group("claim"))
            ]
            if hit and (len(hit) == 1 or m.group("claim") is None):
```

Both follow `classify`'s rule at `:1726`, word for word: a claim's minor
hash in two places is a tie the recorded hash cannot break.

Needs a fix: yes — 🟡 1 (a regression against the base: a held coordinate whose only place is unsure is left BROKEN on a dated row where the base re-pointed it, and `--strict` goes red where the base was clean); 🟡 2 (pre-existing at the base: a claim tie is BROKEN to the check and silent to `reverify`, fixed at both sites or deferred whole)
Loses a record or crashes: no — nothing written is lost and nothing crashes; 🟡 1 writes a BROKEN pact-change part a second run contradicts, and 🟡 2 omits one, both in narrow shapes

The broad gate is not yet due. This round leaves 🟡 1 and 🟡 2 open, and
the run is capped. The sealer's spawn comes due once the orchestrator has
landed or deferred them.

## Proof block

Ran by specseal:warden on claude-opus-5-5, in a `git clone --no-local` of
the worktree at 7f4672a3 under this round's scratchpad directory. Probe
copies of `evidence_check.py` from a3aa139a, 0667af2e, fceff8ce, 930078de
and the target, plus the target with `still` restored and the two fix
variants, sat in the clone under the agent contract's probe prefix. The
probe trees, scripts, copies and clone ran once and were removed before
handover.

Files opened:

- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/rounds/round-1-report.md`,
  `rounds/round-2-report.md` and `rounds/round-2.md`
- the diff 930078de..7f4672a3 of `skills/evidence-check/scripts/evidence_check.py`,
  `tests/test_a_released_row_is_read_again_in_a_fragment.py`, the work
  item's ledger fragment, `overview.md`, `phases/phase-3.md` and `spec.md`
- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md`
- `skills/evidence-check/scripts/evidence_check.py` at the target:
  `reverify` (whole), `resolve_unit`, `generic_units`, `minor_region`,
  `literal_statements`, `recorded_here`, `left_because`, `classify`,
  `coordinate_of`, `current_hash`, `walked_move`, `owed_moves`,
  `walked_outcome`, `left_alone`, `cited_first`, and `family_view`'s grading
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: its helpers
  and the four held-coordinate cases
- the ledger fragment's A1 and the re-read rows citing `0.4.0.md` and
  `0.18.2.md`; `seal/releases/0.4.0.md:59` and `seal/releases/0.18.2.md:129`
- `bin/test`

# Post-review check — #808's fix on an in-place `--reverify` that leaves history alone

| Field | Value |
|---|---|
| Pass | a verifying pass over the post-review fix; not a round (the run is capped at round 3, closed at 0de15c70) |
| Target SHA | 1c3178a1 |
| Range checked | 0de15c70..1c3178a1, 3 commits (2dc03a12 the fix, 2870147e the renamed-move case, 1c3178a1 the records) |
| Base | `release/v0.18.3` at a3aa139a |
| Pull request | #801 (draft, `chain: capped`) |
| Ran by | specseal:warden on claude-opus-5-5 |

## What this pass was asked, and what it found

#808 is closed. Every cell round 3 named agrees with the check's verdict at
1c3178a1, and C8 is as it was at all three SHAs.

- **C10**, the regression, heals again on a dated row. A is re-pointed to
  `src/moved.go#handler`, MOVES gets no BROKEN part, and `--strict` after
  exits 0, as at the base. The renamed arm re-points to `#total`, the hash
  follows the name, and MOVES gets the move.
- **C7** takes the base's wording back: `, and no destination is provable`.
- **C4** and **S1** are named `left` with a BROKEN part, where 0de15c70 and
  the base said nothing.
- **C8** is unchanged at a3aa139a, 0de15c70 and 1c3178a1. That is #809's.

The `still` the smith dropped has nothing to undo. All 180 probe cell-arms
gave the same output, MOVES, exit codes and `--strict` verdicts with the call
restored.

The ordinary path's change is confined by construction. Of 112 cell-arms over
rows no family holds, the target differs from the base only where a claim's
minor content is held by two or more places. That holds for a sure or an
unsure place, a fragment or an unfrozen released row, dated or not, and with
the freeze or without it. The changelog states the change.

One finding is new, and it is about the words of that change:

- **🟡 1, not a regression of any verdict.** The line the fix prints for a
  claim tie reads `N places, none holding the recorded content — left`. That
  is false: a tie exists because two or more places DO hold the recorded
  content. The check's own detail says the same false thing
  (`(none holds the recorded content)`), and has since round 8 of the 0.4.0
  item. But `--reverify` printed nothing there at the base. So this branch
  ships a new line that tells the reader the opposite of what the code holds,
  and two new cases pin it.
- **⬜ 2, pre-existing wording, newly reached.** A claim whose places are all
  ones the declaration rule is unsure of, three places with two holding the
  recorded content, is named `only a place the declaration rule is unsure of
  — left`. The check calls it `locator is ambiguous — 3 places`. The verdict
  agrees, BROKEN on both sides. The same cell with no place holding the
  content reads the same way at the base. It belongs beside #809.

The smith's account was read in full: the three commit messages, A1, spec D1,
the overview's row and new paragraph, the changelog bullet, and the phase-3
grounds for `0.4.0.md:59` and `0.18.2.md:129`. Each claim was checked against
the code at 1c3178a1, and is answered below.

## Findings from execution

### 🟡 1 — a claim tie is named with a reason that says no place holds what two places hold

`skills/evidence-check/scripts/evidence_check.py:914` (`left_because`),
reached from the ordinary path at `:3503` and from the `unplaced` loop at
`:3627`. The check's matching detail is at `:1735-1739` (`classify`).

`left_because` has one sentence for several places:
`f"{len(places)} places, none holding the recorded content"`. It was written
for the shape the check reaches with no hit, and there it is true. #808 now
sends a second shape to it. That shape is a claim whose minor hash two or
more places hold, which `classify` calls BROKEN because the tie cannot be
broken (`hit and (len(hit) == 1 or not claim)`, `:1726`). In that shape
`hit` is non-empty by definition, so the sentence is false.

**Executed.** S1, a lone fragment row `src/service.py#handler>"y = x"` whose
line two `handler` units both hold:

```
--reverify at 1c3178a1:  src/service.py#handler>"y = x"  2 places, none holding the recorded content — left
--strict at 1c3178a1:    BROKEN   src/service.py#handler>"y = x"  locator is ambiguous — 2 places: 1-3, 10-12 (none holds the recorded content)
--reverify at a3aa139a:  (nothing for handler)
```

C4 on a dated held row prints `3 places, none holding the recorded content`
over three places, two of which hold A's hash.

**Why it matters.** The reader is told the content changed, re-reads both
units, and finds the recorded line in each. Nothing tells them what is
actually wrong: the claim names a statement two units share, so it cannot
pick one. Its remedy is a narrower claim or a `Corrected ·` row, not a
re-read. The sentence is also recorded. `0.4.0.md:59`'s re-read and the
changelog now say `--reverify` prints *the check's reason* for this row, and
`test_reverify_names_a_claim_two_places_hold_as_the_check_does` and
`test_a_held_claim_two_places_tie_on_a_dated_row_is_left_and_named` pin the
false words, so the next edit that corrects them reads as a regression.

**Against the base.** No verdict changes: BROKEN before and after, the record
included. The false line is new in `--reverify`'s output. The check's half is
pre-existing, and the two halves have to change together, because
`left_because`'s docstring forbids the two commands describing one row
differently.

**The fix, executed in the clone.** `left_because` takes the number of places
holding the content and names the tie, and `classify` does the same in its
own words. With it:

- S1 prints `2 places, 2 holding the recorded content, a tie the recorded
  hash cannot break — left`.
- The check prints `(2 hold the recorded content, a tie it cannot break)`.
- The no-hit wording stays byte for byte, so `0.4.0.md:20`'s quoted message
  still holds.
- With the two pins updated and a check-side assertion added, the two cases
  are red with the 1c3178a1 script and green with the fix. The four narrow
  modules pass with it: 910 passed.

### The held-coordinate loop, cell by cell

Executed for each cell: A dated 2026-02-01 and carrying `other`, which
drifted; B newer (2026-03-01) where named; R1 the released root. Each cell
ran with the freeze and without it, dated (`--checked 2026-04-01`) and
undated, at a3aa139a, 0de15c70, 1c3178a1, and 1c3178a1 with
`else: still(key, new_hash)` restored. MOVES was captured by replacing
`record_pact_changes` in a driver. The check's verdict is the target's
`--strict` after the run, read on A's row.

| What the held coordinate's places hold | 1c3178a1, dated row | Check on A after | Agrees | Against a3aa139a |
|---|---|---|---|---|
| two places, one holds A (p6, A alone and beside B) | silent, no part | OK, exit 0 | yes | same verdict |
| two identical places, both hold A (C3) | silent | OK | yes | same |
| two places, neither holds A (p1) | `2 places, none holding the recorded content — left`, BROKEN part | BROKEN, ambiguous | yes | same |
| claim, two places, one holds A (C5) | silent | OK | yes | same |
| claim, two places, none holds A (C6) | `2 places, none holding … — left`, BROKEN part | BROKEN, ambiguous | yes | same |
| claim, three places, two hold A (C4) | `3 places, none holding … — left`, BROKEN part | BROKEN, ambiguous | verdict yes; the reason is 🟡 1 | named where the base was silent |
| unsure place holds A, no claim (C9) and with a claim (C9b) | silent | OK | yes | same |
| unsure place, none holds A, no claim, no destination (C7) | `only a place the declaration rule is unsure of, and no destination is provable — left`, BROKEN part | BROKEN, unsure | yes, wording as the base | same; 0de15c70 dropped the clause |
| the same, one destination elsewhere (C10) | `src/lib.go#handler -> src/moved.go#handler  (identical content)`, no part, `--strict` 0 | clean | yes | **same** (0de15c70: left, BROKEN part, `--strict` 2) |
| the same, the unit renamed as it moved (C10r) | `-> src/moved.go#total`, MOVES `1b694937 → 5300c31e`, `--strict` 0 | clean | yes | same |
| the same, two destinations (C10d) | `…, and no destination is provable — left`, BROKEN part | BROKEN, unsure | yes | same |
| unsure place, none holds A, with a claim (C8) | `only a place the declaration rule is unsure of — left`, BROKEN part | DRIFTED `content changed at 2-2` | no — #809 | identical at all three SHAs |
| claim, three unsure places, two hold A (CU) | `only a place the declaration rule is unsure of — left`, BROKEN part | BROKEN `locator is ambiguous — 3 places` | verdict yes, wording no (⬜ 2) | named where the base was silent |
| claim, three unsure places, none holds A (CU0) | the same line | the same | verdict yes, wording no | identical at all three SHAs |
| no place, a file that will not read, an escaping path | unreachable as held (read: no family holds a coordinate that grades BROKEN or EXTERNAL for every reading, `family_view`) | — | — | — |
| a coordinate no family holds (C0) | the ordinary path: the 112 cell-arms below stand in for it | — | — | — |

- **Undated, and frozen undated.** A stays an outranked reading. It gets no
  line and no part in any cell, and its family's verdict is unchanged. In
  C10 and C10r the base re-pointed A even undated, and the target leaves it.
  `--strict` after exits 0 in both, which is #785's history rule as round 3
  recorded it, and not #808's.
- **Unfrozen arm.** The base also walks R1, the released root, and prints
  its own `left` line beside A's. That is #785's change, judged in earlier
  rounds. A's line, part and verdict match the frozen arm in every cell.
- **C10s, renamed in place** (an unsure call line and a `total` unit in the
  same file, A alone, so not held). It is identical at all three SHAs, the
  ordinary path's heal.

### The ordinary path, by construction

The axes are: claim or none × how many places hold the recorded (minor)
content (0, 1, 2 or more) × a place the rule is sure or unsure of × held or
unheld × dated or undated.

- **Held**, read: `current_hash` returns None for more than one place or an
  unsure place (`:3851`). So a held coordinate in any tie or unsure shape goes
  to the `unplaced` loop and never reaches the ordinary path's tie block. The
  loop's table above is the held half.
- **Unheld**, executed: a lone row carrying the coordinate and `other`, in a
  fragment and in a released file, 14 shapes × freeze or not × dated or not,
  at the four copies. That is 112 cell-arms.

| Shape | 1c3178a1 against a3aa139a |
|---|---|
| no claim; 1 of 2, 2 of 2, 0 of 2 places hold it | identical |
| claim; 1 of 2, 0 of 2 | identical |
| claim; 2 of 2 (S1) and 2 of 3 | **new**: `N places, none holding … — left` and a BROKEN part, where the base was silent; the check BROKEN before and after |
| unsure, no claim; holds, heals to one destination, no destination | identical |
| unsure, claim; holds, none holds | identical (the released, unfrozen C8 shape differs only in the family `LEFT` line's remedy, A4's change) |
| unsure, claim; 2 of 3 hold it | **new**: `only a place the declaration rule is unsure of — left` and a BROKEN part, where the base was silent |
| unsure, claim; 0 of 3 | identical |
| any shape on a released row under the freeze | identical: `reverify_into` handles it, and this range does not touch it |

Dated or undated changes nothing in the new cells: a `left` coordinate dates
no row. The exit code is unchanged everywhere (`left` lines do not raise it).
Two other consequences follow, both read and both intended:

- A signatory's pact-change record gains a BROKEN row for each tie, through
  `record_pact_changes`.
- The coordinate joins `left_by_run`, so an unfrozen family `LEFT` line names
  the run's own leaving.

**The changelog states it.** The new bullet says `--reverify` *names a claim
whose minor content two places hold … prints the check's reason on a `left`
line and records the BROKEN in a signatory's pact changes*. That bullet is
for every row, not only held ones. Its *the check's reason* is the sentence
🟡 1 corrects.

### The dropped `still` — nothing to undo, confirmed

- **Read.** In the heal branch the call would only run where the destination
  reconstructs the recorded hash unchanged. `still(key, h)` folds a walk into
  an outcome or a part that an earlier walk of the same key gave it. A key
  takes the `unplaced` route on every walk or on none: `holds` and
  `current_hash` are fixed for the run. On an earlier walk the key either did
  nothing, because its row was not dated there, or healed. A heal rewrites
  the coordinate's text, which changes the key on every later walk. So no
  earlier walk of the same key can have left an outcome or a part.
- **Executed.** The 1c3178a1 script and a copy with the `else` restored gave
  identical output, MOVES, exit codes and `--strict` verdicts in all 180
  cell-arms: 68 held and 112 lone. That includes C10 and C10d, where the
  branch is reached with an unchanged hash.

### The cases, red first

The three-arm heal case, the dated claim-tie case and
`test_reverify_names_a_claim_two_places_hold_as_the_check_does` are each red
with 0de15c70's `evidence_check.py` swapped into the clone, and green at
1c3178a1. Executed: 5 failed and 5 passed with the swap, 10 passed without
it, among the held-coordinate cases.

### A1, spec D1, the overview, the changelog

Each was read against the code at 1c3178a1, and each is true of it.

- **A1.** The heal clause, *(for a claim, exactly one)* and *a claim two
  places hold is named `left` with its BROKEN part on any row* match `:3391`,
  `:3622` and `:3628-3667`. `reverify@49bfd7e4` is the unit's hash at
  1c3178a1 (executed), and `bin/evidence-check --strict .` in the clone reads
  `5704 ok · 0 drifted · 0 broken`, exit 0. Not re-run: the list of mutants
  A1's evidence cell says went red.
- **Spec D1** and **the overview's row.** Both say *on a row the run dates*,
  which bounds the heal correctly. The undated C10 arm leaves A as history.
- **The overview's new paragraph** names #806 and #809 correctly. Both issues
  are open.
- **`changelog.md`.** True, but for the words *the check's reason* under 🟡
  1. Those stay true if the fix changes both commands.

### The re-read claims the smith lists, against 1c3178a1

| Released row | Verdict | Grounds |
|---|---|---|
| `0.4.0.md:22` | holds | `--reverify` is still a separate command; the check writes nothing |
| `0.4.0.md:29` | holds | the loop's heal re-points what reconstruction proves and the hash follows the name (C10r); two identical destinations are left (C10d) |
| `0.4.0.md:59` | holds, with the grounds' named exception | the heal writes onto the destination, never the unsure place; in 180 target runs no row the check flags got silence (executed, the family `LEFT` lines counted); C8's record kind is #809's and the grounds say so |
| `0.16.0.md:57` R1 | holds | a held coordinate is healed only on a row already dated; the renamed arm's hash move rides that date |
| `0.16.0.md:58` R2 | holds | a `left` tie writes nothing to its row |
| `0.18.1.md:174` W8 | holds | the heal's line goes through `said` and `told`; `left` lines print as before |
| `0.18.2.md:87` E4 | holds | the heal's move reaches `parts` through the pending list, once |
| `0.18.2.md:91` (the `Corrected ·` row over it) | holds | the heal touches no Notes cell |
| `0.18.2.md:129` C1 | holds | each tie now records a BROKEN part, which is what C1 says of a BROKEN coordinate |
| `0.8.3.md:13` | holds | the new lines print code coordinates; no ledger name |

## Findings from reading

### ⬜ 2 — a claim tie among places the rule is unsure of is named as one unsure place

`skills/evidence-check/scripts/evidence_check.py:3627` and `:3503`, by way
of `left_because`. The function answers `resurrected` first, before it
counts places. The ordinary path also empties `places` for a resurrected
coordinate (`:3398-3402`) before it asks. So a claim over three unsure call
lines reads *only a place the declaration rule is unsure of* while the check
reads *locator is ambiguous — 3 places*.

Before #808 the case where no place holds the content already read this way
(CU0, identical at the base). #808 sends the case where two places hold it
down the same line (CU). The verdict agrees, and the reason is accurate in
part, because every place is an unsure one. This is a description gap, not
a defect a release ships, and it sits with #809, the other claim-on-unsure
cell where `--reverify` and the check describe one row two ways.

## Regression tests to plant

The pins are the two cases #808 added, edited as in the 🟡 1 fence:

- `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
  `test_a_held_claim_two_places_tie_on_a_dated_row_is_left_and_named`: the
  `3 places, 2 holding …` line.
- `tests/test_a_row_points_by_content.py`,
  `test_reverify_names_a_claim_two_places_hold_as_the_check_does`: the check's
  `(2 hold the recorded content, a tie it cannot break)` and the `2 places,
  2 holding …` line.

Both were seen red with the 1c3178a1 script and green with the fix in the
clone (§15). The fix pass shows them red again before committing.

## Facts to feed into the evidence ledger

- **A1**, if 🟡 1 lands: no clause changes. A1 says what is named, not with
  which words. Its evidence cell gains the tie wording case. Its
  `reverify@` hash and the 31 `Re-read ·` rows' hashes are re-stamped after
  the fix.
- **`0.4.0.md:20`**: unaffected. The message it quotes is the no-hit one,
  kept byte for byte.
- **`changelog.md`**: the #808 bullet should say the check's own detail for
  a tie now names it, a change to `--strict` output a person reads.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a claim whose minor content two or more places hold is named `N places, none holding the recorded content — left` by both `reverify` sites, and the check says `(none holds the recorded content)`; two places do hold it, and two new cases pin the false words | `skills/evidence-check/scripts/evidence_check.py:914` | open | S1 and C4 executed at the target; no verdict changes against a3aa139a, where `--reverify` said nothing; the check's half since round 8 of the 0.4.0 item; the fix executed in the clone, the pins red at 1c3178a1 and green with it, 910 passed in the four narrow modules |
| ⬜ 2 | a claim tie among places the declaration rule is unsure of is named `only a place the declaration rule is unsure of`, where the check says `locator is ambiguous — 3 places` | `skills/evidence-check/scripts/evidence_check.py:3627` | deferred #809 | CU and CU0 executed; the verdict agrees; the wording gap is the base's for CU0 and newly reached for CU; the same claim-on-unsure family as #809 |
| 🟢 | round 3's yellow 1 is closed — a held coordinate whose only place is unsure heals onto its one destination on a dated row | `skills/evidence-check/scripts/evidence_check.py:3628` | confirmed | C10, C10r, C10d and C7 at a3aa139a, 0de15c70 and 1c3178a1, freeze and not; the target matches the base on every dated arm |
| 🟢 | round 3's yellow 2 is closed — a claim tie is named with its BROKEN part at both sites | `skills/evidence-check/scripts/evidence_check.py:3391` | confirmed | S1 and C4 executed; the verdict matches the check's; the words are 🟡 1 |
| 🟢 | C8 stays as it was | `skills/evidence-check/scripts/evidence_check.py:3627` | confirmed | identical at the three SHAs in all four arms; #809 open |
| 🟢 | the `else: still(...)` the smith dropped has nothing to undo | `skills/evidence-check/scripts/evidence_check.py:3646` | confirmed | read: a key healed once never meets the branch again; executed: 180 cell-arms identical with it restored |
| 🟢 | the ordinary path changes only where a claim's minor content two or more places hold, and the changelog says so | `skills/evidence-check/scripts/evidence_check.py:3391` | confirmed | 112 lone cell-arms against a3aa139a; the held half reaches the loop by `current_hash` (read) |
| 🟢 | A1, spec D1, the overview and the changelog say what the code does | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | confirmed | each read against 1c3178a1; `reverify@49bfd7e4` current; `--strict` exit 0; *the check's reason* follows 🟡 1 |
| 🟢 | the ten re-read claims hold at 1c3178a1 | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | confirmed | each row read against the code and the probe cells, table above |
| ❓ | the full suite, the repository lint and the typecheck at 1c3178a1 | the branch | ❓ out of verified scope | not this pass's to run; the sealer answers it, after 🟡 1 is fixed or filed |

## Executed probes

| What was run | Result |
|---|---|
| the held-coordinate matrix: 17 shapes (round 3's 13 plus C10r, C10s, C10d, CU, CU0) × freeze or not × dated or not, at a3aa139a, 0de15c70, 1c3178a1 and 1c3178a1 with `still` restored | as the table *The held-coordinate loop, cell by cell*; target and `still` copy identical in all 68 |
| the ordinary-path matrix: 14 shapes × a fragment or a released row × freeze or not × dated or not, at the same four copies | as the table *The ordinary path, by construction*; target and `still` copy identical in all 112 |
| the silence check over the 180 target runs: every row `--strict` flags after the run has a line or a family `LEFT` line | none silent |
| the three #808 cases and the held-coordinate cases, at 1c3178a1 and with 0de15c70's script swapped in (`-k`, ten selected) | 10 passed at the target; 5 failed and 5 passed with the swap |
| the four narrow modules the prompt names, at 1c3178a1 in the clone, without the hygiene modules | 910 passed (the orchestrator's 972 includes the hygiene modules) |
| `bin/evidence-check --strict .` in the clone at 1c3178a1 | exit 0, `5704 ok · 0 drifted · 0 broken` |
| `reverify`'s unit hash at 1c3178a1 | `49bfd7e4`, the hash A1 to A6 and the re-reads cite |
| 🟡 1's fix in the clone: S1 by the check, the two edited pins red at 1c3178a1 and green with it, and the four narrow modules | the check prints `(2 hold the recorded content, a tie it cannot break)`; 2 failed with the 1c3178a1 script, 2 passed with the fix; 910 passed |
| the full suite, the lint and the typecheck (the broad gate) | not yet |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a claim tie among unsure places is described as one unsure place (⬜ 2) | #809, as a comment beside its claim-on-unsure cell | the orchestrator adds the comment; the evidence-check maintainer decides #809's design |
| an unsure place with a claim is handed a BROKEN part where the check reads DRIFTED (C8) | #809 | already deferred in round 3; the evidence-check maintainer |
| a non-citation ledger coordinate whose file walks first is left drifted | #806 | already deferred in round 2; the evidence-check maintainer |

## Paste-ready fixes

### 🟡 1

`skills/evidence-check/scripts/evidence_check.py`, five hunks, applied in the
clone and run as above:

```diff
-def left_because(places, resurrected):
+def left_because(places, resurrected, holding=0):
@@
     if not places:
         return "no place — the check calls this row BROKEN"
+    if holding:
+        return (
+            f"{len(places)} places, {holding} holding the recorded content, "
+            "a tie the recorded hash cannot break"
+        )
     return f"{len(places)} places, none holding the recorded content"
@@ def classify(m, root, maps, default_repo, scan_cache):
     places, resurrected = resolve_unit(rel, locator, body)
-    unsure = []
+    unsure, hit = [], []
     if places and (resurrected or len(places) > 1):
@@
     if len(places) > 1:
         at = ", ".join(f"{a}-{b}" for a, b in places)
+        held = (
+            f"{len(hit)} hold the recorded content, a tie it cannot break"
+            if hit
+            else "none holds the recorded content"
+        )
         return (
             "BROKEN",
             coord,
-            f"locator is ambiguous — {len(places)} places: {at} "
-            "(none holds the recorded content)",
+            f"locator is ambiguous — {len(places)} places: {at} ({held})",
         )
@@ def reverify(  (the ordinary path)
             places, resurrected = (
                 resolve_unit(rel, locator, body) if body is not None else ([], False)
             )
+            hit = []
             if places and (resurrected or len(places) > 1):
@@
-                    f"  {left_as}  {left_because(places, resurrected)} — left",
+                    f"  {left_as}  {left_because(places, resurrected, len(hit))} — left",
@@ def reverify(  (the unplaced loop)
-            why = left_because(places, resurrected)
+            why = left_because(places, resurrected, len(hit))
```

In `classify`, `hit` is non-empty in the `len(places) > 1` branch only for a
claim tie. A row with no claim and any hit has already narrowed to one place,
so every other ambiguous row keeps its wording byte for byte. Run the
formatter: the ordinary path's line passes 88 columns.

The two pins, as run:

```diff
--- tests/test_a_released_row_is_read_again_in_a_fragment.py
-    assert f"  {claim}  3 places, none holding the recorded content — left" in out, out
+    assert (
+        f"  {claim}  3 places, 2 holding the recorded content, a tie the recorded "
+        "hash cannot break — left"
+    ) in out, out
--- tests/test_a_row_points_by_content.py
-    assert run(["--strict", "."], str(repo)).returncode == 2
+    check = run(["--strict", "."], str(repo))
+    assert check.returncode == 2
+    assert (
+        "(2 hold the recorded content, a tie it cannot break)" in check.stdout
+    ), check.stdout
@@
-        '  src/service.py#handler>"y = x"  2 places, none holding the recorded '
-        "content — left"
+        '  src/service.py#handler>"y = x"  2 places, 2 holding the recorded '
+        "content, a tie the recorded hash cannot break — left"
```

Needs a fix: yes — 🟡 1 (not a regression of any verdict: the claim-tie line #808 adds says no place holds the recorded content where two do, the check's detail says the same, and two new cases pin it; fix both commands together or file it)
Loses a record or crashes: no — nothing written is lost and nothing crashes; every verdict and every pact-change part matches the check's verdict

The broad gate is not yet due. 🟡 1 is open. The sealer's spawn comes due
once it is fixed post-review or filed.

## Proof block

Ran by specseal:warden on claude-opus-5-5, in a `git clone --no-local` of
the worktree at 1c3178a1 under this pass's scratchpad directory. The probe
copies of `evidence_check.py` (a3aa139a, 0de15c70, 1c3178a1, the `still`
copy, the 🟡 1 fix) sat in the clone under the agent contract's probe prefix.
The probe script, its trees, the copies and the clone ran once and were
removed before handover.

Files opened:

- `rounds/round-3-report.md` of this work item, and #808's and #809's issue
  text
- the diff 0de15c70..1c3178a1, every file in it
- `skills/evidence-check/scripts/evidence_check.py` at 1c3178a1: `reverify`
  (whole), `recorded_here`, `left_because`, `content_matches`, `classify`
  (the tie and the unsure branch), `resolve_unit`, `generic_units`,
  `current_hash`, `left_alone`, `cited_first`'s docstring,
  `record_pact_changes`'s docstring, `reverify_into`'s left lines, and
  `main`'s `--reverify` dispatch
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: its helpers and
  the held-coordinate cases; `tests/test_a_row_points_by_content.py`: the new
  case
- this item's `changelog.md`, `overview.md`, `spec.md` D1, `phases/phase-3.md`
  and the ledger fragment's A1 to A6 and re-read rows
- `seal/releases/0.4.0.md:20`, `:22`, `:29`, `:59`; `0.16.0.md:57`, `:58`;
  `0.18.1.md:174`; `0.18.2.md:87`, `:91`, `:129`; `0.8.3.md:13`
- `bin/test`

# Round 3 report — `--reverify` computes once and judges in one place

| Field | Value |
|---|---|
| Work item | 1791240748-reverify-computes-once-and-judges-in-one-place |
| Round | 3, the verifying round that ends the run |
| Target SHA | `c4c2578980f900d3a2e0a3876fd7c75d27d6cf88` |
| Base | `origin/release/v0.19.0` |
| What it opened | round 2's fix range, `96cc3e46..90fb07c4` |
| Ran by | specseal:warden on Opus 5.5 |
| Where it ran | a `git clone --no-local` of the worktree at the target SHA, in the session scratchpad, deleted afterwards |

## How the findings relate

Round 2's three fixes hold. Each one closes the shape round 2 named, and each
new case fails when its fix is taken back out. One paperwork finding is left,
and it sits in the ledger row that describes the first fix.

```
the left-whole guard back on `through` (round 2's yellow 1)
  ├─ 🟢 a loop through a row left whole is no cycle — executed, six shapes
  ├─ 🟢 every member the early leaving reads has a hash to write on a row it rewrites — read
  ├─ 🟢 the bound leaves only coordinates still moving — read
  └─ ⬜ 1  E3 says the bound reads the cycle the same guarded way, and it does not
the verb in the memo key (round 2's yellow 2)
  └─ 🟢 the key now holds every input read_citation and judge read
the unsettled arm's case (round 2's yellow 3)
  └─ 🟢 red with the arm restored
the paperwork (round 2's white 4 and 5)
  └─ 🟢 the docstring, the comment, the changelog and E4 and 0.4.0 say what the code does
```

Nothing here needs a fix in the code. The run can end on this round.

## Findings

### ⬜ 1 — E3 says the bound reads a cycle through the same guard, and the bound reads it unguarded

`seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:23`
(read). The fix range added a qualifier to E3's sentence about cycles. The
sentence now reads, in its middle:

> a coordinate on a cycle of rows naming each other or itself, read over every
> coordinate still judged that has a hash to write on a row a re-stamp
> rewrites, so that a loop through a row `--checked` leaves whole is no cycle,
> is left [...] from the second round of a pass in the first round that
> rewrites its own row, and otherwise once the pass has run as many rounds as
> there are such coordinates, plus two

The subject of the sentence carries both arms. So the row claims that the
bound's arm also reads the cycle only through `through`, and that it leaves
only coordinates on such a cycle. The code does two different things at the
bound, at `skills/evidence-check/scripts/evidence_check.py:3723`:

- `on_a_cycle(moving, by_key, verdicts)` passes no AMONG, so the naming runs
  through every coordinate still judged. A row left whole and a member with
  no hash to write are both counted.
- Where no moving coordinate is on a cycle, `or moving` leaves every
  coordinate still moving, on a cycle or not.

The code's own comment at `evidence_check.py:3698` says this correctly: *the
bound's leaving below predicts nothing: what it leaves is still moving.* The
docstring does not make E3's claim either. E3 is the one place that does.

The count has the same problem in a smaller way. *As many rounds as there are
such coordinates* now reads as the coordinates with a hash to write on a row a
re-stamp rewrites. The bound is `len(dynamic) - len(pinned) + 2`, which counts
every coordinate naming a line of a ledger the run writes, less those already
left. The docstring says *coordinates naming a ledger line*, which is right.

**Why it is ⬜ and not 🟡.** No release behavior changes. I could not build a
tree that reaches the bound with a loop through a row left whole: every real
cycle has all its members in `through`, so the early leaving takes it first.
Only an oscillation through a member with no hash to write, such as a
re-point that keeps toggling, would reach the bound. The row is paperwork, and
its location is under `seal/ledger/`, so this is a correction and is not
counted in `Needs a fix`.

**Who answers it.** The orchestrator's post-run fix, since this round ends the
run. The replacement text is under *Paste-ready fixes*.

## What round 2's fixes hold

Each question this round was asked, answered on my own grounds.

### The `rewrites` guard stops a loop through a row left whole from being read as a cycle — yes

`evidence_check.py:3650` and `:3716`.

- **Executed.** `mutation-check` replaced `and rewrites(key)` with `and True`.
  `test_a_cycle_through_a_row_left_whole_is_no_cycle` then failed, because K
  was named *does not settle*. At the target it passes.
- **Executed.** I ran one probe file once over six shapes, then deleted it.
  Three were loops through a four-cell row under `--checked`: one of three
  rows that the four-cell row starts, one of four rows, and one of two rows.
  In all three nothing was named *does not settle*. The four-cell row was
  named left whole, and every other drifted row was re-stamped. Three were
  controls. The round 2 shape without `--checked` named one row *does not
  settle*, because there the undated row is rewritten and the cycle is real.
  The four-row loop with five cells in every row named one row. A real
  two-row cycle beside a four-cell row naming it named one cycle member and
  left the four-cell row whole.
- **Read.** `rewrites` asks exactly what `plan_ledger` asks when it decides to
  leave a row whole. Both call `date_column` on the same cells of the
  original text, and both treat a line outside a table row as having no date
  cell. Without `--checked`, both rewrite every row.

### Every other member the early leaving reads has a hash to write on a row it rewrites — yes

Read. `on_a_cycle` builds `live` from AMONG, and `names` only over `live`. A
starting key that is not in `names` is skipped at `evidence_check.py:3350`.
So each member of a cycle that the early leaving finds is in `through`: its
verdict is not None, its `now` is not None, and `rewrites` holds for its row.

Two kinds of member stay out, and leaving them out costs time, not
correctness. A statement gone has `now` None and writes nothing, which round
1's case already pins. A BROKEN coordinate re-pointed onto a destination also
has `now` None, but it does rewrite its row. A cycle through such a member is
not taken early. It reaches the bound, which leaves it as still moving.
Dynamic coordinates never hold, so the held riders do not apply here.

### The fallback at the bound leaves only coordinates that are still moving — yes

Read. When the pass exhausts its range, `looping` is the empty set from the
last step, because a non-empty one would have ended the loop. So the line
`pinned |= looping or on_a_cycle(moving, by_key, verdicts) or moving` leaves
`on_a_cycle`'s answer, which is a subset of MOVING, or MOVING itself. Both are
the coordinates whose verdict changed on the last round. The range is at least
two rounds, because `pinned` never outgrows `dynamic`. A key pinned in the
previous pass is None on both sides by the last step, so it is never counted
as moving. What the bound reads as a cycle is still unguarded, which is ⬜ 1.

### The citation memo keys on everything `read_citation` and `judge` read — yes

`evidence_check.py:3603`.

- **Read.** `read_citation` reads the match, the verb, `root`, `maps`,
  `default_repo` and the loader. The match is covered by `coordinate_of` and
  the hash, because the coordinate holds the path, the locator and the claim.
  The verb is now in the key. The other three are the same for the whole run,
  and every static reading uses the one `on_disk` loader. `judge` reads the
  match and the shared scan cache, and its rows key with verb None as before.
- **Read.** Nothing else drops the verb. `--strict` reads each citing row
  through `cited_row` with that row's own verb and no memo, at
  `evidence_check.py:2570`. `--into` does the same at `:3972`. Dynamic
  citations are read per key through `verdict_of`.
- **Executed.** `mutation-check` took the verb out of the key, and
  `test_two_citing_rows_sharing_a_citation_are_named_each_in_its_own_verb`
  failed: `--reverify` named the `Corrected ·` row in `Re-read`'s words. The
  committed case also asserts `--strict`'s output, which round 2's fence did
  not.

### The unsettled arm's case pins it — yes

`tests/test_a_signatory_records_a_pact_change.py:2376`. Executed:
`mutation-check` put `pending.append((spot, None))` back into the arm at
`evidence_check.py:3174`. The case failed at its record assertion, with one
pact change recorded for the row that does not settle. At the target it
passes. The case runs through `--into`, and `--into` reaches `plan_ledger`:
the output names the row *does not settle*.

### The docstring, the comment, the changelog, E3, E4 and 0.4.0 — all true except ⬜ 1

Read against the code at the target.

- **Docstring, `evidence_check.py:3396`.** *From the second round of a pass,
  one whose own row that round rewrote, on a cycle of coordinates each with a
  hash to write on a row a re-stamp rewrites, is left* matches `step`,
  `rewrote` and `through`. `test_the_documents_say_each_outcome_is_printed_once`
  pins the new sentence and passed in the module run.
- **Comment, `:3688`.** It says what each guard is for and that the bound
  predicts nothing. True.
- **Changelog.** *From the second round on, the run leaves such a coordinate
  the first round that rewrites its own row* is true: a self-quoting row is
  rewritten in the first round and left in the second. *A loop through a row
  `--checked` leaves whole is no cycle* is true of the early leaving, which is
  the only arm the sentence describes. The bullet for #809 already says a
  citing row's citation is read by the same reader in both commands, which the
  verb in the key now makes true for two rows sharing one citation.
- **E3, line 23.** *From the second round of a pass in the first round that
  rewrites its own row* is now true, which was round 2's ⬜ 5. The bound's
  arm is ⬜ 1.
- **E4, line 24.** *One that does not settle append nothing, since nothing is
  known gone* matches the `continue` at `:3179`. It now cites the case that
  pins it.
- **0.4.0, line 41.** *A citation the check refuses is named with the check's
  sentence* is now true for two citing rows that share one citation. It cites
  the new case.
- **Executed.** `bin/evidence-check --strict --ledger` over the fragment at
  the target: 240 ok, exit 0. Every hash the fix range re-stamped
  (`reverify@996a64f6` and the three new test anchors) reads OK.

### Round 2's ⬜ 4 answer — holds

`tests/test_a_signatory_records_a_pact_change.py:2355`. Executed:
`mutation-check` replaced `return sorted(out)` in `resolve_patterns` with
`return out`, and `test_the_record_is_the_same_bytes_in_any_ledger_order`
failed, as its corrected docstring now says.

### Round 1's findings — still closed

Executed. The two modules the fix touched, the fragment module and the
pact-change module, pass at the target with 597 cases. Round 1's cases for
the downstream row, the cost at the bound, the two citation shapes, the
no-checkout shapes and the statement-gone cycle are among them. Round 2's
fixes add a condition to `through` and an element to a memo key, and neither
reaches the paths those cases drive except by narrowing the early leaving. I
carried round 1's closures from round 2's grounds and re-ran their cases. I
did not re-time the 150-row and 300-row runs.

## The account, claim by claim

| The account says | What I found |
|---|---|
| `c5b026d0`: *a loop through a row left whole is no cycle* | True for the early leaving; executed. At the bound the naming is unguarded, which the code's comment says and E3 does not (⬜ 1) |
| `c5b026d0`: *a citation's reading is memoised with its row's verb* | True; read and executed |
| `c5b026d0`: *an unsettled coordinate's empty record is pinned* | True; red with the arm restored |
| `90fb07c4`: *E3 says what the early leaving does* | True of the early leaving; ⬜ 1 is about the bound's arm of the same sentence |
| round-2.md: *Fixes checked by — nobody* | This round is the one that checks them |

## Regression tests to plant

None. Each fix of round 2 already has a case, and each case was seen red under
the mutation that undoes its fix.

## Facts for the evidence ledger

None that the fragment lacks. ⬜ 1 is a correction to E3's own wording, not a
new fact.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | E3 says the bound's arm reads the cycle through the hash-to-write and row-rewritten guard and leaves only cycle members; the bound calls on_a_cycle with no AMONG and falls back to every moving coordinate | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:23` | open | Read: evidence_check.py:3723 against the row; the code comment at :3698 says it right; a correction to the run's paperwork, answered by the orchestrator's post-run fix |
| 🟢 | round 2's finding 1 is closed — a loop through a row --checked leaves whole is no longer read as a cycle | `skills/evidence-check/scripts/evidence_check.py:3716` | confirmed | Executed: the case red with the guard replaced by True; six probe shapes, three loops through a four-cell row named nothing does not settle, three real cycles named one row each |
| 🟢 | round 2's finding 2 is closed — the static memo keys on the row's verb | `skills/evidence-check/scripts/evidence_check.py:3611` | confirmed | Read: the key covers every input of read_citation and judge; executed: the case red with the verb dropped |
| 🟢 | round 2's finding 3 is closed — a coordinate that does not settle records no pact change, and a case pins it | `tests/test_a_signatory_records_a_pact_change.py:2376` | confirmed | Executed: red at its record assertion with the arm restored, green at the target |
| 🟢 | round 2's finding 4's answer holds — the record-order case is red only with the sort removed | `tests/test_a_signatory_records_a_pact_change.py:2355` | confirmed | Executed: red with return sorted(out) replaced by return out |
| 🟢 | round 2's finding 5's answer holds — the docstring, comment, changelog and E3 say a coordinate is left at its first rewrite from the second round | `skills/evidence-check/scripts/evidence_check.py:3396` | confirmed | Read against step, rewrote and through; the pinning case passed in the module run |
| 🟢 | The early leaving reads only members with a hash to write on a row a re-stamp rewrites | `skills/evidence-check/scripts/evidence_check.py:3332` | confirmed | Read: live comes from AMONG, names only over live, a start outside names is skipped |
| 🟢 | The bound's fallback leaves only coordinates still moving | `skills/evidence-check/scripts/evidence_check.py:3723` | confirmed | Read: looping is empty at exhaustion, so what is left is a subset of MOVING or MOVING itself |
| 🟢 | E4 and the 0.4.0 Corrected row say what the code does | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:24` | confirmed | Read against plan_ledger's unsettled arm and the memo key; executed: evidence-check --strict over the fragment, 240 ok |
| 🟢 | round 1's findings 1 to 4 stay closed under round 2's fixes | `skills/evidence-check/scripts/evidence_check.py:3314` | confirmed | Carried from round 2's grounds; executed: their cases pass in the two modules, 597 passed |

## Executed probes

| What was run | Result |
|---|---|
| bin/test over the fragment module and the pact-change module at the target | 597 passed, exit 0 |
| mutation-check: `and rewrites(key)` replaced by `and True`, the left-whole case | red: K named does not settle |
| mutation-check: the verb dropped from the static memo key, the shared-citation case | red: --reverify named the Corrected row in the Re-read row's words |
| mutation-check: the unsettled arm hands MOVES a BROKEN part, the does-not-settle case | red at the record assertion: one pact change recorded |
| mutation-check: `return sorted(out)` replaced by `return out`, the record-order case | red |
| One probe file run once over six shapes at the target, then deleted: the round 2 shape without --checked; a real two-row cycle beside a four-cell row; loops of two, three and four rows through a four-cell row under --checked; the loop of four with five cells in every row | Real cycles: one row named does not settle in each. Loops through the four-cell row: nothing named does not settle, the four-cell row left whole, every other drifted row re-stamped. Exit 1 in all six, for the row left whole or the row that does not settle |
| bin/evidence-check --strict --ledger over the work item's ledger fragment at the target | 240 ok, 0 drifted, exit 0 |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet; the sealer's, and its spawn comes due with this round |

Needs a fix: no

Loses a record or crashes: no

## Paste-ready fixes

### ⬜ 1 — E3's cycle clause, split by arm

In the claim cell of E3, at the fragment's line 23, replace the clause from
*a coordinate on a cycle* to *plus two* with:

```text
a coordinate on a cycle of rows naming each other or itself is left at the hash its row recorded and named on a `LEFT` line saying it does not settle: from the second round of a pass, in the first round that rewrites its own row, where the cycle is read over every coordinate still judged that has a hash to write on a row a re-stamp rewrites, so that a loop through a row `--checked` leaves whole is no cycle; and otherwise once the pass has run as many rounds as there are coordinates naming a line of a ledger it writes and not yet left, plus two, where every coordinate still moving is left, those on a cycle read over every coordinate still judged where any is
```

## Proof block

```
📋 code-review applied (warden, round 3, verifying, ends the run)
· read:     rounds/round-2.md, rounds/round-2-report.md; the diff 96cc3e46..90fb07c4
            (code, tests, the ledger fragment, the changelog fragment);
            seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md lines 21, 23, 24, 29, 32, 41;
            changelog.md; spec.md lines 62-80; docs/the-evidence-ledger.md lines 215-232;
            skills/evidence-check/scripts/evidence_check.py at the target (146-175, 1630-1840,
            2200-2420, 2520-2585, 2620-2640, 3141-3830);
            tests/test_a_released_row_is_read_again_in_a_fragment.py (59-130, 4460-4540)
· executed: the probes in the table above, in a scratch clone at c4c25789, deleted afterwards
· unverified: the broad gate — the sealer, after the rounds settle; the 150-row and 300-row
            timings, carried from round 2 and not re-run
```

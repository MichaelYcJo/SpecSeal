# Round 2 report — `--reverify` computes once and judges in one place

| Field | Value |
|---|---|
| Work item | 1791240748-reverify-computes-once-and-judges-in-one-place |
| Round | 2, the verifying round |
| Target SHA | `2d04e34139465a82df3f8a1e93a5bc73fec8385b` |
| Base | `origin/release/v0.19.0` |
| What it opened | round 1's fix range, `935b3918..bd9f9eb8` |
| Ran by | specseal:warden on Opus 5.5 |
| Where it ran | a `git clone --no-local` of the branch at the target SHA, in the session scratchpad; the scripts of `e6d5a055`, `ca467185` and `63ca12a5` beside it for comparison |

## How the findings relate

Round 1's four fixes hold for the shapes round 1 named. Three new findings
sit inside those fixes, and two of them come from one move: each fix
narrowed what a reading depends on, and one input was dropped along the way.

```
the early pin (round 1's yellow 2 fix)
  └─ 🟡 1  a loop through a row left whole is taken for a cycle
          (the guard 8c73b19c removed as unreachable is reachable)
  └─ ⬜ 5  the words say "rewrites again"; the code pins at the first rewrite
the one citation reader (round 1's yellow 3 fix)
  └─ 🟡 2  the memo of a citation's reading drops the row's verb
the pact record (round 1's yellow 4 fix)
  └─ 🟡 3  "one that does not settle records nothing" has no case holding it
the paperwork
  └─ ⬜ 4  a new case says it was red at ca467185; it passes there
```

Each 🟡 has a paste-ready fix and a case below. I applied the two code fences
together in the clone: the two new cases turned green, and 812 cases of the
three modules that drive `--reverify` hardest passed. Each case failed at the
target SHA, or under the mutation its docstring names.

## Findings

### 🟡 1 — A loop through a row `--checked` leaves whole is taken for a cycle, and a row that settles is named "does not settle"

`skills/evidence-check/scripts/evidence_check.py:3688`. Commit `8c73b19c`
removed the `rewrites` guard of round 1's fence and called it unreachable.
Its comment says *a row `--checked` leaves whole never changes by a hash, so a
coordinate naming it never moves twice and is never here*. That is true of
the coordinate naming the row. It is not true of the cycle search, which
passes through the row's own coordinate.

Take three rows of one release file:

- S quotes L's line at a stale hash;
- K quotes S's line and holds;
- L has four cells, so `--checked` leaves it whole, and it quotes K's line.

Round 1 re-stamps S. Round 2 re-stamps K, so K is in `rewrote`. `through`
holds S, K and L, because all three have a hash to write. The search finds
K → S → L → K and pins K. But L's line never moves, so the loop cannot
propagate, and K would settle.

| Script | What `--reverify --checked` did | `--strict` after |
|---|---|---|
| target `2d04e341` | K left at its stale hash and named *does not settle* | K DRIFTED, exit 2 |
| `63ca12a5`, with the guard | S and K re-stamped, L named *its hash moved and the row has no date cell* | L DRIFTED, exit 2 |

Both runs exit 1, but the target names the wrong row and gives the wrong
reason. Spec D1 says reaching the bound *names the rows that still move and
nothing else*, and K does not still move. This is round 1's 🟡 1 class
returning through a second door.

The fix puts the guard back on `through` only. A key on a row left whole is
never in `rewrote`, because its row never changes, so `through` is the one
place that needs it.

### 🟡 2 — Two citing rows that share one citation are named in the first row's verb

`skills/evidence-check/scripts/evidence_check.py:3602`. The static memo keys
a reading on `(coordinate, hash, citation)`. `read_citation`'s sentence for a
citation that names no released ledger also carries the row's verb, through
`citing_verb`. So the second row with the same citation gets the first row's
sentence.

I ran a `Re-read ·` row and a `Corrected ·` row, both citing one line of
`docs/x.md`:

- `--strict` names the first *a `Re-read ·` row's first coordinate…* and the
  second *a `Corrected ·` row's first coordinate…*;
- `--reverify` names both *a `Re-read ·` row's first coordinate…*.

Round 1's 🟡 3 was this class: the two commands describe one row two ways.
This item's own `Corrected ·` row for `seal/releases/0.4.0.md:59`
(`seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:41`)
says *a citation the check refuses is named with the check's sentence*. The
second row falsifies it.

The shape needs two citing rows with one citation and one hash, so it is
rare. The fix adds the verb to the memo key.

### 🟡 3 — Nothing holds that a coordinate that does not settle records no pact change

`skills/evidence-check/scripts/evidence_check.py:3174`. `63ca12a5` stopped
handing MOVES a BROKEN part for a coordinate that does not settle. Round 1
left that shape to the smith. The change is right, and three documents now
state it: `docs/the-pact.md`, the changelog fragment, and the E4 `Corrected ·`
row at the fragment's line 24.

No case holds it:

- **Executed.** Restoring `pending.append((spot, None))` in that arm left the
  fragment module and the pact-change module at 594 passed.
- **Executed.** A pact-citing row beside a self-quoting coordinate recorded
  that coordinate BROKEN through the `ca467185` script, and nothing through
  the target.

The record is permanent and a pact review takes each row of it. Contract §14
asks the commit that changes it to pin it. The case below is red with the arm
restored and green at the target.

### ⬜ 4 — A round 1 case says it was red at `ca467185`, and it passes there

`tests/test_a_signatory_records_a_pact_change.py:2358`.
`test_the_record_is_the_same_bytes_in_any_ledger_order` says *Red at ca467185,
which wrote its rows in that order*. I ran it against the scripts of `e6d5a055`
and `ca467185`, and it passes on both. `resolve_patterns` has returned
`sorted(out)` since `e27c1976`, which is the reason round 1's ⬜ 5 was
answered. The case is red only with the sort removed, which round-1.md's
grounds already say. The docstring should say that instead.

### ⬜ 5 — The words say a coordinate is left when its row is rewritten "again", and the code leaves it at the first rewrite

`skills/evidence-check/scripts/evidence_check.py:3397` (read). `reverify`'s
docstring says *one whose own row a round rewrites again*. The comment at
`:3667` and the E3 `Corrected ·` row (fragment line 23) say the same, and the
changelog says *the round it rewrites its own row a second time*.

`rewrote` compares the row before and after this round only. It never asks
whether an earlier round rewrote it. In a two-row cycle that one stale row
starts, the member that held is pinned in round 2, at its row's first
rewrite. That is sound on a real cycle, and it is the reason 🟡 1 could
happen at all.

The words should say *from a pass's second round, a coordinate whose own row
that round rewrote*. The sentence is pinned in
`test_the_documents_say_each_outcome_is_printed_once`, so the pin moves with
it. The fragment and the changelog are paperwork, which is why this is ⬜.

## What round 1's fixes hold

Each round 1 finding, answered on my own grounds:

- **🟡 1, a downstream row whatever the bound's parity — closed.** Executed:
  cycles of two and three rows, each started by one stale row, with a
  downstream row D and 0, 1, 2 or 3 unrelated coordinates naming a written
  ledger. In all eight trees, one cycle member was named, D was re-stamped,
  and `--strict` showed one DRIFTED row. Read: `on_a_cycle` builds `names`
  over `among`, or every key of `spots`, whose verdict is not None.
- **🟡 2, the cost at the bound — closed.** Executed: a release file of 150
  rows, each cited from a fragment, beside one self-quoting row, took 20.4 s
  through the `ca467185` script and 0.9 s through the target. At 300 rows the
  target took 4.8 s with no cycle, 7.1 s with a self-quoting row, 8.7 s with
  a two-row cycle and 8.0 s with a three-row cycle. Each run named one row.
  Round 1's case for this failed at `ca467185` and passes at the target.
- **🟡 3, one reader for a citation — closed, apart from 🟡 2 above.** Read:
  `cited_row` returns `read_citation`'s finding, and `reverify`'s
  `verdict_of` calls `read_citation` for every citation, static or judged
  against the plan. Executed: both of round 1's shapes failed at `ca467185`
  and pass at the target.
- **What changed for a citation of a fragment row.** Executed, with a
  fragment row under a heading and a citation of it naming the heading. The
  base and `ca467185` re-stamped the citation silently (`cfdf0cd2 →
  69e79229`), and `--strict` still called it MALFORMED. The target leaves it,
  with the MALFORMED sentence and its repair followed by ` — left`. All three
  exit 0, as the home's *five things* list says for a refused citing row.
  Where the citation names no heading, the base and `ca467185` already left
  it, as *no place* and *locator not found*. The changelog's *rather than
  re-stamped* holds for the first shape.
- **🟡 4, `known_gone` — closed.** Executed: round 1's case for EXTERNAL and
  escaping coordinates failed at `ca467185` and passes at the target. A
  coordinate whose unit is gone still records BROKEN through the target. A
  coordinate that does not settle records nothing (🟡 3 is about its pin).
  The statement-gone case `test_a_claim_whose_statement_is_gone_from_an_unsure_place_is_recorded_broken`
  passed in the module run.
- **The `rewrites` guard removed as unreachable — not unreachable.** See
  🟡 1.
- **Round 1's ⬜ 5 answer — true.** Executed: the pinning case passes against
  the base and `ca467185`, and fails with `return sorted(out)` replaced by
  `return out`.
- **Round 1's ⬜ 6 answer, and the ledger corrections.** Read against the
  code at the target:
  - E1 (line 21) holds: `plan_ledger` records a move from the row's own hash
    to the hash the plan writes, once per coordinate.
  - A4 (line 32) holds: `left_here` takes `plan.left`, `plan.whole` and every
    coordinate that does not settle.
  - E4 (line 24) holds; 🟡 3 is about its pin, not its truth.
  - A1 (line 29) holds. Its *a citation is re-stamped as before* is the
    released row's own wording, and it is about the held rule, which never
    applies to a citation.
  - E3 (line 23) holds, except its *rewrote its own row again* (⬜ 5).
  - 0.4.0 (line 41) holds, except the verb corner (🟡 2).
  - Executed: `bin/evidence-check --strict .` at the target exits 0.
- **The cases round 1's fixes planted.** Executed against `ca467185`. Red
  there, as each says: the downstream case's `one` parameter, the cost case,
  both citation shapes, and both no-checkout shapes. The statement-gone cycle
  case is red under its named mutation, which counts a member with no hash
  to write on the cycle. The record-order case is ⬜ 4.

## The account, claim by claim

| The account says | What I found |
|---|---|
| `8c73b19c`: *the left-whole guard nothing could reach goes* | Reachable: three rows, one of four cells (🟡 1) |
| `63ca12a5`: *a citation has one reader* | One reader; its memo drops the verb the reader's sentence carries (🟡 2) |
| `63ca12a5`: *one that does not settle hands MOVES nothing* | True when executed; no case holds it (🟡 3) |
| `reverify`'s docstring: *one whose own row a round rewrites again* | The code pins at the first rewrite in a round after the first (⬜ 5) |
| `tests/…pact_change.py:2358`: *Red at ca467185* | Passes at `ca467185` and at the base (⬜ 4) |
| changelog: *costs seconds rather than minutes* | 0.9 s against 20.4 s at 150 rows; 7.1 s at 300 |

## Regression tests to plant

- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the loop
  through a row left whole (🟡 1) and two citing rows sharing one citation
  (🟡 2). Both are in the fences below.
- `tests/test_a_signatory_records_a_pact_change.py`: the coordinate that does
  not settle and records nothing (🟡 3).

## Facts for the evidence ledger

None that this round verified and the fragment lacks. 🟡 1's and 🟡 2's
fixes will change `reverify`'s hash, and the rows that cite it are re-read
then.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A naming loop through a row --checked leaves whole is taken for a cycle, so a row that settles is left and named does not settle | `skills/evidence-check/scripts/evidence_check.py:3688` | open | Executed: three rows S, K and a four-cell L; the target left K named does not settle, and 63ca12a5, with the guard, re-stamped K and named L left whole; spec D1 says only rows that still move are named |
| 🟡 2 | The static memo of a citation's reading keys on coordinate, hash and citation, not the row's verb, so a second citing row is named in the first row's verb | `skills/evidence-check/scripts/evidence_check.py:3602` | open | Executed: --strict names Re-read and Corrected, --reverify names Re-read twice; falsifies the 0.4.0 Corrected row at the fragment's line 41 |
| 🟡 3 | No case holds that a coordinate that does not settle records no pact change | `skills/evidence-check/scripts/evidence_check.py:3174` | open | Executed: the arm restored, 594 passed in the two modules; ca467185 recorded it BROKEN and the target nothing; contract §14 |
| ⬜ 4 | The record-order case says it was red at ca467185, and it passes there and at the base | `tests/test_a_signatory_records_a_pact_change.py:2358` | open | Executed against both scripts; red only with the sort removed |
| ⬜ 5 | The docstring, a comment, the E3 Corrected row and the changelog say rewritten again or a second time; the code pins at the first rewrite in a round after the first | `skills/evidence-check/scripts/evidence_check.py:3397` | open | Read: rewrote compares this round's before and after only |
| 🟢 | round 1's finding 1 is closed — a row downstream of an alternating cycle is re-stamped whatever the bound's parity | `skills/evidence-check/scripts/evidence_check.py:3314` | confirmed | Executed: cycles of two and three rows, 0 to 3 unrelated coordinates, eight trees, D never named; round 1's case red at ca467185 |
| 🟢 | round 1's finding 2 is closed — a pass at its bound costs seconds | `skills/evidence-check/scripts/evidence_check.py:3666` | confirmed | Executed: 150 rows 20.4 s at ca467185 and 0.9 s at the target; 300 rows 7.1 to 8.7 s with a cycle |
| 🟢 | round 1's finding 3 is closed — read_citation is the one reader of a citation for --strict and --reverify | `skills/evidence-check/scripts/evidence_check.py:2271` | confirmed | Read: cited_row and verdict_of; executed: both shapes red at ca467185, green at the target; the verb corner is finding 2 |
| 🟢 | round 1's finding 4 is closed — EXTERNAL and escaping coordinates hand MOVES nothing, and a gone unit still records BROKEN | `skills/evidence-check/scripts/evidence_check.py:3132` | confirmed | Executed: the case red at ca467185; a gone unit recorded BROKEN through the target |
| 🟢 | round 1's finding 5's answer holds — resolve_patterns sorts | `skills/evidence-check/scripts/evidence_check.py:1401` | confirmed | Executed: the case passes at the base and ca467185, fails with the sort removed |
| 🟢 | round 1's finding 6's answer holds — E1 and A4 are Corrected rows without the walk | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:21` | confirmed | Read against plan_ledger and left_here |
| 🟢 | A citation of a fragment row is left with the MALFORMED sentence where the base re-stamped it silently | `skills/evidence-check/scripts/evidence_check.py:2290` | confirmed | Executed through the base, ca467185 and the target |
| 🟢 | The E1, A4, E3, E4, A1 and 0.4.0 corrections hold, apart from the details findings 2 and 5 name | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:19` | confirmed | Read; executed: bin/evidence-check --strict . exits 0 at the target |

## Executed probes

| What was run | Result |
|---|---|
| Three rows S, K and a four-cell L naming each other in a loop, --reverify --checked through the target and through 63ca12a5 | Target: K named does not settle, K DRIFTED after; 63ca12a5: S and K re-stamped, L named left whole, L DRIFTED after |
| Cycles of two and three rows started by one stale row, a downstream row D, 0 to 3 unrelated coordinates naming a written ledger | Eight trees: one cycle member named, D re-stamped, one DRIFTED row in --strict |
| 150 and 300 cited release rows with no cycle, a self-quoting row, a two-row and a three-row cycle, unfrozen --reverify --checked | 150: 1.0, 1.7, 2.3, 2.5 s; 300: 4.8, 7.1, 8.7, 8.0 s; 150 with a self-quoting row through ca467185: 20.4 s against 0.9 s |
| A citation of a fragment row, with and without a heading, through the base, ca467185 and the target | With a heading, the base and ca467185 re-stamped it and the target left it with the MALFORMED sentence; without one, all three left it; exit 0 throughout |
| A pact-citing row beside a self-quoting coordinate, a gone unit and a gone file with --into, through ca467185 and the target | Does not settle: BROKEN at ca467185, nothing at the target; gone unit: BROKEN on both; gone file: re-pointed on both |
| The unsettled arm restored to hand MOVES a BROKEN part, the fragment and pact-change modules | 594 passed |
| Round 1's planted cases against the ca467185 script | 6 failed as their docstrings say; the record-order case passed |
| The record-order case against the base, ca467185, the target and the target with the sort removed | Passes, passes, passes, fails |
| The statement-gone cycle case with the hash-to-write condition removed from through | Fails, as its docstring says |
| A Re-read and a Corrected row sharing one citation of docs/x.md, --strict and --reverify at the target | --strict names each verb; --reverify names Re-read twice |
| The fences for findings 1 and 2 applied together, the three new cases, then the fragment, pact-change and row-points modules | 812 passed; at the target the cases for 1 and 2 fail; the case for 3 fails with the arm restored |
| bin/evidence-check --strict . at the target | exit 0 |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet; the sealer's, after the rounds settle |

Needs a fix: yes — 🟡 1 (a loop through a row left whole is taken for a cycle), 🟡 2 (a citation's memo drops the row's verb), 🟡 3 (the unsettled arm's record has no case)

Loses a record or crashes: no

## Paste-ready fixes

### 🟡 1 — put the left-whole guard back on `through`

In `reverify`, before `texts = {ledger.home: ledger.text for ledger in parsed}`:

```python
    def rewrites(key):
        """Whether a re-stamp of KEY rewrites its row: not where `--checked`
        leaves the row whole for want of a date cell. Such a row breaks a
        cycle as a member with no hash to write does: its line never moves,
        so nothing naming it moves twice."""
        spot = by_key[key]
        header, cells = parsed[spot.key[0]].rows.get(spot.number, (None, []))
        return checked is None or (
            bool(cells) and date_column(header, cells) is not None
        )
```

```diff
                 # to write, a statement gone, rewrites nothing and breaks the
                 # cycle, so the naming passes only through ones that have
-                # one. A row `--checked` leaves whole never changes by a hash,
-                # so a coordinate naming it never moves twice and is never
-                # here.
+                # one, on a row the re-stamp rewrites: a row `--checked`
+                # leaves whole never changes, so a loop through it is no
+                # cycle (round 2 of #824, yellow 1).
@@
                     through = {
                         key
                         for key in by_key
-                        if verdicts[key] is not None and verdicts[key].now is not None
+                        if verdicts[key] is not None
+                        and verdicts[key].now is not None
+                        and rewrites(key)
                     }
```

The case, in `tests/test_a_released_row_is_read_again_in_a_fragment.py`:

```python
def test_a_cycle_through_a_row_left_whole_is_no_cycle(repo):
    """Round 2, yellow 1. S quotes L's line at a stale hash, K quotes S's,
    and L -- four cells, no date cell -- quotes K's. Under `--checked` L's
    row is left whole, so its line never moves and the naming S, K, L is no
    cycle: S and K are re-stamped, L is named as left whole, and nothing is
    named `does not settle`. Red at 2d04e341, which left K at its stale hash
    as a row that does not settle."""

    def names(label):
        return f'{R_FILE}#"{SECTION}">"\\| {label}"'

    s = f"| S · names L | `{names('L · names')}@0000beef` | read | 2026-01-01 | |"
    k = f"| K · names S | `{names('S · names')}@{line_hash(s)}` | read | 2026-01-01 | |"
    whole = f"| L · names K | `{names('K · names')}@{line_hash(k)}` | read | 2026-01-01 |"
    released(repo, [s, k, whole])
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert "does not settle" not in fix.stdout, fix.stdout
    assert f"  LEFT  {R_FILE}:7  its hash moved and the row has no date cell" in (
        fix.stdout
    )
    lines = (repo / R_FILE).read_text(encoding="utf-8").splitlines()
    assert f"@{line_hash(lines[4])}`" in lines[5], (lines, fix.stdout)
```

### 🟡 2 — key a citation's reading on its row's verb too

```diff
             if spot.target in writes:
                 dynamic.append(spot)
                 continue
-            index = (coordinate_of(spot.m), spot.m.group("hash"), spot.citation)
+            # A citation's sentence names its row's verb, so two citing rows
+            # share one reading only where they share the verb too.
+            verb = (
+                citing_verb(ledger.rows.get(spot.number, (None, []))[1])
+                if spot.citation
+                else None
+            )
+            index = (coordinate_of(spot.m), spot.m.group("hash"), spot.citation, verb)
             if index not in memo:
                 memo[index] = verdict_of(spot, on_disk)
```

The case, in `tests/test_a_released_row_is_read_again_in_a_fragment.py`:

```python
def test_two_citing_rows_sharing_a_citation_are_named_each_in_its_own_verb(repo):
    """Round 2, yellow 2. A `Re-read ·` and a `Corrected ·` row carry one
    citation of a file that is no released ledger. `--strict` names each in
    its own row's verb, and `--reverify` names each `left` in the same words.
    Red at 2d04e341, whose memo of a citation's reading kept the first row's
    verb."""
    (repo / "docs").mkdir()
    (repo / "docs" / "x.md").write_text("## H\n\nfoo bar\n", encoding="utf-8")
    h = unit_hash(repo, "src/service.py", "handler")
    cite = 'docs/x.md#"## H">"foo"@00000000'
    fragment(
        repo,
        [
            f"| Re-read · one | `{cite}`, `src/service.py#handler@{h}` | read "
            "| 2026-02-01 | Re-read 2026-02-01 |",
            f"| Corrected · two | `{cite}`, `src/service.py#handler@{h}` | read "
            "| 2026-02-01 | Corrected 2026-02-01 |",
        ],
    )
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    for verb in ("Re-read", "Corrected"):
        assert f"a `{verb} ·` row's first coordinate names a row" in fix.stdout, (
            verb,
            fix.stdout,
        )
```

### 🟡 3 — pin that a coordinate that does not settle records nothing

The case, in `tests/test_a_signatory_records_a_pact_change.py`. I ran it on
a tree built as the module's `repo` fixture builds it:

```python
def test_a_coordinate_that_does_not_settle_records_no_pact_change(repo):
    """Round 2, yellow 3. A row citing a clause beside a coordinate quoting
    its own line: the run names it `does not settle` and records nothing,
    because one place holds what it names and nothing is known gone. Red with
    the unsettled arm of `plan_ledger` handing MOVES a BROKEN part, as
    ca467185 did."""
    coord = f'{FRAGMENT}#"### sec">"\\| O1 · the field"@0000beef'
    cite(repo, ["### sec\n\n", row("O1", f"`{CLAUSE}`, ", coord)])
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "does not settle" in out, out
    assert record_rows(repo) == [], out
```

## Proof block

```
📋 code-review applied (warden, round 2, verifying)
· read:     rounds/round-1.md, rounds/round-1-report.md, routing.md, spec.md (D1), changelog.md;
            the diff 935b3918..bd9f9eb8 (code, tests, docs/the-pact.md, the fragment, the changelog);
            seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md lines 11-41;
            seal/releases/0.18.2.md:84-87, 0.18.3.md:6 and :9, 0.4.0.md:59;
            skills/evidence-check/scripts/evidence_check.py at the target (1060-1075, 1366-1401,
            1660-1832, 2999-3010, 3099-3362, 3455-3790);
            tests/test_a_released_row_is_read_again_in_a_fragment.py (1-125, 2500-2560, 3690-3740, 4323-4482);
            tests/test_a_signatory_records_a_pact_change.py (20-125, 2306-2370)
· executed: the probes in the table above, in a scratch clone at 2d04e341, deleted afterwards;
            bin/evidence-check --strict .
· unverified: the broad gate — the sealer, after the rounds settle
```

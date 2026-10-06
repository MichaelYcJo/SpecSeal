# 1791240748-reverify-computes-once-and-judges-in-one-place — review round 2

| Field | Value |
|---|---|
| Target SHA | 2d04e34139465a82df3f8a1e93a5bc73fec8385b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #829 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `96cc3e46949f382f988753980ce22f421aeaf76c..90fb07c44269e2bc835eec6e665619d98f7e4188`, 2 commits |
| Contract changes | none |
| New units | test_a_cycle_through_a_row_left_whole_is_no_cycle (depth 1); test_two_citing_rows_sharing_a_citation_are_named_each_in_its_own_verb (depth 1); test_a_coordinate_that_does_not_settle_records_no_pact_change (depth 1) |
| Needs a fix | yes — 🟡 1 (a loop through a row left whole is taken for a cycle), 🟡 2 (a citation's memo drops the row's verb), 🟡 3 (the unsettled arm's record has no case) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round for round 1's fix range `935b3918..bd9f9eb8`: whether `on_a_cycle` now reads the naming over every coordinate still judged and leaves a cycle the round it loops, with the downstream row restamped whatever the bound's parity, and the 300-row pass at the bound back to seconds; whether a citation now has one reader, `read_citation`, for `--strict` and `--reverify` alike, and what changed for a citation of a fragment row that now reads MALFORMED; whether `known_gone` keeps EXTERNAL, escaping and unsettled coordinates out of MOVES while a coordinate whose unit or statement is gone still records BROKEN; the removal of the `rewrites` guard as unreachable; and whether the ⬜ 5 answer (`resolve_patterns` sorts) and the E1, A4, E3, E4, A1 and 0.4.0 ledger corrections are true.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A naming loop through a row --checked leaves whole is taken for a cycle, so a row that settles is left and named does not settle | `skills/evidence-check/scripts/evidence_check.py:3688` | **fixed** `c5b026d0` | fixed at c5b026d0; Executed: three rows S, K and a four-cell L; the target left K named does not settle, and 63ca12a5, with the guard, re-stamped K and named L left whole; spec D1 says only rows that still move are named |
| 🟡 2 | The static memo of a citation's reading keys on coordinate, hash and citation, not the row's verb, so a second citing row is named in the first row's verb | `skills/evidence-check/scripts/evidence_check.py:3602` | **fixed** `c5b026d0` | fixed at c5b026d0; Executed: --strict names Re-read and Corrected, --reverify names Re-read twice; falsifies the 0.4.0 Corrected row at the fragment's line 41 |
| 🟡 3 | No case holds that a coordinate that does not settle records no pact change | `skills/evidence-check/scripts/evidence_check.py:3174` | **fixed** `c5b026d0` | fixed at c5b026d0; Executed: the arm restored, 594 passed in the two modules; ca467185 recorded it BROKEN and the target nothing; contract §14 |
| ⬜ 4 | The record-order case says it was red at ca467185, and it passes there and at the base | `tests/test_a_signatory_records_a_pact_change.py:2358` | answered | corrected at c5b026d0 — the docstring says the case passes at e6d5a055 and ca467185 and fails with the sort removed; Executed against both scripts; red only with the sort removed |
| ⬜ 5 | The docstring, a comment, the E3 Corrected row and the changelog say rewritten again or a second time; the code pins at the first rewrite in a round after the first | `skills/evidence-check/scripts/evidence_check.py:3397` | answered | corrected at 90fb07c4 — the sentence now says what the code does: a cycle coordinate is left at its first rewrite from the second round on, which already proves it cannot settle; Read: rewrote compares this round's before and after only |
| 🟢 | round 1's finding 1 is closed — a row downstream of an alternating cycle is re-stamped whatever the bound's parity | `skills/evidence-check/scripts/evidence_check.py:3314` | confirmed | Executed: cycles of two and three rows, 0 to 3 unrelated coordinates, eight trees, D never named; round 1's case red at ca467185 |
| 🟢 | round 1's finding 2 is closed — a pass at its bound costs seconds | `skills/evidence-check/scripts/evidence_check.py:3666` | confirmed | Executed: 150 rows 20.4 s at ca467185 and 0.9 s at the target; 300 rows 7.1 to 8.7 s with a cycle |
| 🟢 | round 1's finding 3 is closed — read_citation is the one reader of a citation for --strict and --reverify | `skills/evidence-check/scripts/evidence_check.py:2271` | confirmed | Read: cited_row and verdict_of; executed: both shapes red at ca467185, green at the target; the verb corner is finding 2 |
| 🟢 | round 1's finding 4 is closed — EXTERNAL and escaping coordinates hand MOVES nothing, and a gone unit still records BROKEN | `skills/evidence-check/scripts/evidence_check.py:3132` | confirmed | Executed: the case red at ca467185; a gone unit recorded BROKEN through the target |
| 🟢 | round 1's finding 5's answer holds — resolve_patterns sorts | `skills/evidence-check/scripts/evidence_check.py:1401` | confirmed | Executed: the case passes at the base and ca467185, fails with the sort removed |
| 🟢 | round 1's finding 6's answer holds — E1 and A4 are Corrected rows without the walk | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:21` | confirmed | Read against plan_ledger and left_here |
| 🟢 | A citation of a fragment row is left with the MALFORMED sentence where the base re-stamped it silently | `skills/evidence-check/scripts/evidence_check.py:2290` | confirmed | Executed through the base, ca467185 and the target |
| 🟢 | The E1, A4, E3, E4, A1 and 0.4.0 corrections hold, apart from the details findings 2 and 5 name | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:19` | confirmed | Read; executed: bin/evidence-check --strict . exits 0 at the target |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3293` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3554` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3509` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3182` | round 1's 🟡 4 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3599` | round 1's ⬜ 5 — answered |
| round-1 | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:21` | round 1's ⬜ 6 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1669` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3549` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1827` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3653` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-2.md:80` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-4.md:21` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:19` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain

# Review round 3 — the verifying round of #774, #772 and #775 (PR #786), the last round of the run

Target SHA `32d0acea` on `fix/774-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move`,
base `release/v0.18.2` at `94d7b2e0`. Target of this round: round 2's fix
range `89ca97ee..44e6f417` (three commits) and the close commit `32d0acea`.
Ran by: specseal:warden on claude-opus-5-5. Worked in a `git clone --no-local`
at the target under `<scratchpad>/<work-item-id>/round-3/clone`; nothing was
written in the checkout but this file. The clone, its probe file and its
scripts are deleted.

This round ends the run. Round 2 closed on a fix after round 1 met the floor,
so this is the reading of the one reopening, and what it finds is reported for
the ladder rather than for a fix pass.

## Summary

Round 2's two findings are closed. Every hash line, re-point line and the
`N rows re-verified` count are now keyed by ledger, row, coordinate and
spelling. Each coordinate is named once, from the hash the ledger held before
the run to the hash it takes. The case round 2 did not plant, two citing rows
citing each other's lines, now names each citation once as well. Every guard
of the fix is held by a case: five mutants each turned a planted case red,
and the checker as it stood before the fix turned the new case red on all
four parameters.

The smith's table of what `reverify` prints missed one output: the MOVES list
that `record_pact_changes` writes the pact-change record from. The round-2
grounds say *"the moves list needs no change: code does not move between
walks, citations append nothing"*. That holds for code coordinates and for a
citing row's citation. It does not hold for a ledger coordinate that is not a
row's citation. Such a coordinate is re-stamped on each walk the line it names
moves, and it appends one move per walk. The permanent pact-change record then
carries two parts for one coordinate, and the first ends at a hash no file
ever held (🟡 1).

Two corrections to the run's paperwork follow from round 2's white 2. The
hand edit to `rounds/round-1.md` row 1 left row 6 of the same table pointing
at a sentence that is no longer there (⬜ 2). The fragment's E3 row still says
*two short-circuits survive as equivalent*, which round 2 showed is false for
one of them (⬜ 3).

## How each round-2 fix was judged

### Round 2, yellow 1 — closed (executed)

The account claimed that every per-coordinate line and the count are now
emitted once per coordinate, keyed by ledger, row, coordinate and which
spelling of it the row holds, never by offset. It also claimed the line runs
from the hash the ledger held before the run to the hash it takes.

What the code does at `evidence_check.py:3188` is build that key from
`planned_key(ledger)`, the line number from `starts`, `coordinate_of(m)` and a
per-row count. The hash line's old hash comes from `first_old.setdefault`
(`:3116`, `:3328`). `report` collects `said_here` into a dict, so the last
walk's line wins and keeps the first walk's position (`:3407`). Line numbers
are stable across walks, because every splice `reverify` makes is a hash or a
date cell inside one line and none adds a line.

Executed, at the target and under mutation (all in the clone):

- the planted cases at the target: 10 passed;
- the key without the per-row count: `test_a_row_naming_one_coordinate_twice_is_named_twice` red;
- the key built from the offset rather than the line: the two dated parameters of `test_one_unfrozen_run_names_each_coordinate_it_restamps_once` red, so the date written between walks is what the dated parameters hold;
- the hash line printing the walk's own old hash instead of `first_old`: all four parameters red;
- `report` keeping every walk's line instead of one per key: all four red;
- `evidence_check.py` as it stood at `89ca97ee`, before the fix: all four red. This is the §15 showing, and it agrees with the smith's.

The case round 2 did not plant, two citing rows in one release file citing
each other's lines: `--strict` exits 2 before the run, because no write makes
that shape legal. The run walks four times, as it did in round 2. It now prints
one line per citation (`5b1acb94 -> 26879fe7`, `406f009c -> 90edd347`) and
`4 rows re-verified` for four coordinates, against four lines each and 11 in
round 2. The new hash on each line is the one the file holds after the run.
`--strict` still exits 2 after it. That is the shape `cited_first`'s docstring
leaves for `--strict` to name, and round 2 recorded the same exits, so it is
not new.

The smith enumerated the outputs as hash lines, re-point lines and the count
(keyed now). The other outputs are the `say` lines and the unreadable,
malformed and overflow lists (first walk only), and the dated, undated and
undatable lists (de-duplicated). I checked the rest of what the run prints
against the code. `recorded` lines group by ledger row in
`record_pact_changes`, so one per row. The refusal line and the narrowed
`LEFT` lines (`citations_left`, `released_drift`) are printed once by `main`
and are not walk-driven. The `could not be written` line is one per planned
file. The enumeration missed one output, and it is not a printed line: the
MOVES list. That is finding 1 below.

### Round 2, white 2 — closed (executed)

`test_one_unfrozen_run_names_a_citing_row_it_left_whole_once` holds the
walked-file skip at `evidence_check.py:3612`. It is green at the target and
red with the two-line skip removed. The overview's proof block now says one
equivalent short-circuit survives (`planned_key`) and the `read_here` skip is
load-bearing. Read against `phases/phase-2.md:66-72` and round 1's white 6,
that is accurate.

The two other places the claim was corrected or left are corrections 2 and 3
below.

### E3's new wording and the re-stamped fragment

E3 now says the run names *"each coordinate it re-stamps once, from the hash it
held before the run to the hash it takes, and each row it dates, leaves undated
or leaves whole once"*. The probes above and the planted cases bear that out
for the printed lines. E3 says nothing about the moves list, so finding 1 does
not contradict E3. It does contradict E1's last clause, *"the in-place
re-stamp records each row's move from that row's own hash"*, and the same
sentence at `docs/the-pact.md:132`. It also contradicts `reverify`'s own
docstring at `evidence_check.py:3070`, which promises one MOVES entry *per
coordinate*.

The fragment: a hash-masked comparison of `89ca97ee` against `44e6f417` shows
15 rows changed by `reverify@999bffa4 → @9038b161` and nothing else. E3 is
rewritten and carries the sixteenth such coordinate and three new case
coordinates, so 19 coordinates were written, matching the orchestrator's
count. No `@999bffa4` remains. `bin/evidence-check --strict .` at the
worktree's HEAD (`32d0acea`) exits 0. The fix proposed for finding 1 moves
`reverify` again, so those 16 coordinates take another re-stamp if it lands.

## Finding 1 — a ledger coordinate that is not a citation records a move per walk, and the record names a hash no file held

`skills/evidence-check/scripts/evidence_check.py:3386`. 🟡, from execution.

The shape is a row that is not a citing row, or a citing row's second or later
coordinate, naming a ledger line among its Code grounds. The line it names is a
citing row in a file `cited_first` leaves unplaced. That line moves on two
walks: first by its own code re-stamp and date, then by its citation. So the
coordinate is re-stamped on each of the two walks.

It is not a citation in the sense of `row_citation`, which takes only a citing
row's first coordinate. It is therefore not in the walk's `citations` set, and
each walk's `pending` entry for it is appended to MOVES. `record_pact_changes`
removes only identical parts (`dict.fromkeys`). The two parts differ, so both
are written.

Executed in the clone with `Pact notify | always`, a declared branch and a
self-citing `0.1.0.md`: R1, a `Re-read ·` row citing R1, and X1 whose second
coordinate names the `Re-read ·` line. `--strict` exits 0 before the run. The
run prints one hash line for X1's coordinate, `5127adb5 -> 46e82957`, so the
round-2 fix holds for the printed line. The record it writes says:

```
| — | seal/releases/0.1.0.md · X1 | `seal/releases/0.1.0.md#"### 1000000001-the-first-item">"Re-read · the row it cites \|"@5127adb5` → `@07b2ad6b`, `seal/releases/0.1.0.md#"### 1000000001-the-first-item">"Re-read · the row it cites \|"@07b2ad6b` → `@46e82957` | 2026-03-01 |
```

`07b2ad6b` is the hash of the `Re-read ·` line after the first walk, which no
file ever held. It is the same hash round 2's yellow 1 found on a printed
line. The record is the file a pact review takes by content hash and that
nothing edits by hand. So the false part outlives the run, where the printed
line did not.

Why it matters: the shape is legal and uncommon. It takes a row naming a
ledger line as code grounds beside a self-citing or mutually citing release
file, and a record is written only where the row cites a pact clause or
`Pact notify` is `always`. Before this branch the coordinate was hashed on one
walk, so it appended at most one part. The second part comes from round 1's
repeated walk, a unit this branch created.

The fix is the one round 2 applied to the printed line, applied to MOVES. Keep
one part per coordinate across walks, under the same key, from the first
walk's old hash to the last walk's new one, and hand the parts to MOVES once
the walks end. In the clone, the fix and the case below gave this result. The
case was red at the target (two parts) and green with the fix. The record
names X1 once, `@5127adb5 → @46e82957`. The fragment, pact-change and
`tests/test_evidence_check.py` modules passed (509), and ruff check and format
were clean on both touched files.

A different altitude is a decision this report does not make. D3's reasoning
is that a citation is a ledger line and not code under the row. That reasoning
reaches every coordinate whose path is under the `seal/` root, not only a
citing row's first coordinate. Skipping all of those from MOVES would remove
the shape rather than collapse it, and it changes what a pact change is, so it
belongs to whoever owns D3.

## Correction 2 — round 1's record now contradicts itself

`seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md:27`.
⬜, a correction, from reading.

`44e6f417` rewrote the Grounds cell of row 1 in round 1's closed record. It now
says the `read_here` skip *"was called equivalent here, and it is not"*. Row 6
of the same table, at line 32, still says *"row 1 above states that the
`read_here` short-circuit is equivalent only after the fix"*. Row 6 also states
the principle the edit set aside: *"A phase record is a record of its moment
… left as written; the round-1 report holds the correction."*

The record is generated. `docs/round-record-spec.md` §*A record is derived,
not typed* names the round paragraph as the one thing written by hand, and
the Grounds cell was written by `close` from round 1's fix table. The
correction already has two homes that are this round's to write: round 2's
record (white 2's row and its grounds) and `overview.md`'s proof block.

Acceptable or a note elsewhere: elsewhere. Restore round 1's row 1 as `close`
wrote it, and let round 2's record carry the correction, as round 1 itself did
for `phases/phase-2.md`. The sentence the edit wrote is true, so nothing ships
wrong. That makes it ⬜, and it stays out of `Needs a fix`.

## Correction 3 — E3 still calls both short-circuits equivalent

`seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:3`.
⬜, a correction, from reading.

E3's Executed cell still reads *"two short-circuits survive as equivalent
(`phases/phase-2.md`)"*. Round 2 appended *"the walked-file skip held by a
case red with it removed"* and did not withdraw the claim. The overview was
corrected and E3 was not. E3 is the row that folds into the release file at
0.18.2 and is frozen there. Fixed now, it is one cell. Fixed later, it is a
`Corrected ·` row.

## Regression tests to plant

- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the case in
  `## Paste-ready fixes` under finding 1. It was red at `32d0acea` (two parts
  for X1's coordinate) and green with the fix.

## Facts for the evidence ledger

- If finding 1's fix lands, E1's last clause and E4 gain a coordinate: the new
  case, and `reverify` at its new hash. Add to E3 or E4 one clause: *a ledger
  coordinate that is not a row's citation appends one move however many walks
  re-stamp it, from the hash the ledger held before the run*.
- E3's Executed cell: correction 3.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A ledger coordinate that is not a row's citation, naming a line a walk of AGAIN moves twice, appends one MOVES part per walk, and the pact-change record writes both: the first ends at a hash no file ever held | `skills/evidence-check/scripts/evidence_check.py:3386` | open | Executed in the clone at 32d0acea: `Pact notify` always, self-citing `0.1.0.md` plus X1 naming the `Re-read ·` line, `--strict` 0 before; record row X1 carries `@5127adb5 → @07b2ad6b` and `@07b2ad6b → @46e82957` while the printed line is one; contradicts round 2's grounds (*the moves list needs no change*), E1's in-place clause, `docs/the-pact.md:132` and the MOVES docstring at `:3070`; the unit is round 1's repeated walk; the fix below gave one part and 509 passed |
| ⬜ 2 | Round 1's closed record was hand-edited in a generated Grounds cell, and row 6 of the same table now points at a sentence row 1 no longer holds | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md:27` | open | Read: row 6 (line 32) says row 1 states the skip is equivalent only after the fix, and that a record of its moment is left as written; `docs/round-record-spec.md` §A record is derived, not typed; the correction already lives in round 2's record and `overview.md`; paperwork, a correction, not on the fix list |
| ⬜ 3 | E3's Executed cell still says two short-circuits survive as equivalent, one of which round 2 showed load-bearing | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:3` | open | Read: the overview was corrected and E3 was not; E3 folds into the frozen 0.18.2 release file; paperwork, a correction, not on the fix list |
| 🟢 | round 2's finding 1 is closed — every hash line, re-point line and the count are keyed by ledger, row, coordinate and spelling, each coordinate named once from the hash the ledger held to the one it takes, the two-citing-rows cycle included | `skills/evidence-check/scripts/evidence_check.py:3188` | confirmed | Executed in the clone: planted cases green at 32d0acea; five mutants (no per-row count, offset key, no `first_old`, every walk's line kept, the checker at 89ca97ee) each red; the cycle shape names each citation once with the hash the file holds after the run, `4 rows re-verified` for four coordinates |
| 🟢 | round 2's finding 2 is closed — a case holds the walked-file skip in `citations_left`, and the overview no longer calls it equivalent | `skills/evidence-check/scripts/evidence_check.py:3612` | confirmed | Executed: `test_one_unfrozen_run_names_a_citing_row_it_left_whole_once` green at 32d0acea and red with the skip removed; read `overview.md:12` against `phases/phase-2.md:66-72` |
| 🟢 | the fragment re-stamp is a hash move and nothing else, and the strict check reads it clean | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md` | confirmed | Executed: hash-masked comparison 89ca97ee..44e6f417, 15 rows moved only `reverify@999bffa4 → @9038b161`, E3 rewritten with the sixteenth and three new case coordinates (19 written); `bin/evidence-check --strict .` exit 0 at 32d0acea |
| carried | rounds 1 and 2's 🟢 verdicts — the walk terminates within its bound, the in-place writer records from the row's own hash for code coordinates, the narrowed `LEFT` waits in `told`, the pact sentences are pinned | `skills/evidence-check/scripts/evidence_check.py:3112`, `docs/the-pact.md:130`, `skills/evidence-check/scripts/evidence_check.py:5415` | confirmed | carried, not re-derived: round 2's fixes touch none of these units except `reverify`'s output collection, which the first 🟢 above re-derived; finding 1 narrows the in-place clause to code coordinates |

## Executed probes

| What was run | Result |
|---|---|
| The planted round-2 cases and the self-citation cases (`bin/test` with `-k` over the four names) at 32d0acea | 10 passed |
| The same cases under five mutants of the fix (no per-row count; offset key; walk's own old hash; every walk's line kept; `evidence_check.py` from 89ca97ee) | each red: 1, 2, 4, 4 and 4 failed respectively |
| The walked-file skip in `citations_left` removed | `test_one_unfrozen_run_names_a_citing_row_it_left_whole_once` red |
| Two citing rows citing each other's lines in one release file, `--reverify --checked 2026-03-01 .` then `--strict .` | `--strict` 2 before; run exit 0, each citation on one line, `4 rows re-verified`; `--strict` 2 after (an illegal shape, as in round 2) |
| Round 2's fragment-to-released-chain shape undated, through `main` | `--strict` 0 before; one line per coordinate, `5 rows re-verified`, three rows named undated once each; `--strict` 0 after |
| Self-citing `0.1.0.md` plus X1 naming the `Re-read ·` line as a second coordinate; `reverify` called with a MOVES list | X1's coordinate appended twice: `5127adb5 → 07b2ad6b`, `07b2ad6b → 46e82957`; printed line one |
| The same through `main` with `Pact notify` always and a declared branch | exit 0; record row X1 holds both parts (quoted under finding 1) |
| Finding 1's fix and case applied in the clone | case red at 32d0acea and green with the fix; record row X1 `@5127adb5 → @46e82957`; the fragment, pact-change and `tests/test_evidence_check.py` modules 509 passed; `uvx ruff check` and `ruff format --check` clean on both files |
| Hash-masked comparison of the fragment over 89ca97ee..44e6f417, and `bin/evidence-check --strict .` at 32d0acea | 15 rows moved only `reverify`'s hash, E3 rewritten; exit 0 |
| The full suite, the repository lint and the typecheck at this branch's head | not yet — not run by this round; the sealer's, once the run's closing record is written |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — a ledger coordinate that is not a citation records one pact-change part per walk | candidate: a new `from-review` issue (rung 3); no open issue owns this ground, and #785 is a different mechanism (outranked in-place re-reads) | the orchestrator of this run, for the 0.18.2 milestone: the unit is this branch's own repeated walk, and the fix and its case below are verified in a clone |

## Paste-ready fixes

### Finding 1 — one MOVES part per coordinate across walks

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ -3114,6 +3114,12 @@ def reverify(
     # a coordinate is one line, from the hash the ledger held to the one it
     # takes (round 2, yellow 1).
     first_old = {}
+    # The move each coordinate owes, one per coordinate across walks, from
+    # the hash the ledger held before the run to the one it takes: a ledger
+    # line among a row's Code grounds that is not its citation moves on each
+    # walk the line it names moves (round 3). Handed to MOVES once the walks
+    # end.
+    parts = {}
 
     def walks():
         for ledger in once:
@@ -3177,7 +3183,7 @@ def reverify(
         # Matched in `unquoted(text)` and spliced from `text`: the two have
         # the same offsets, and an example row in a closed fence is never
         # rewritten (#444).
-        nth = {}
+        nth, key_at = {}, {}
         for m in ANCHOR_RE.finditer(unquoted(text)):
             # What names this coordinate on every walk: its ledger, its row,
             # its coordinate and which of that row's spellings of it this is.
@@ -3185,7 +3191,7 @@ def reverify(
             # walk moves every offset after it.
             spot = (bisect.bisect_right(starts, m.start()), coordinate_of(m))
             nth[spot] = nth.get(spot, 0) + 1
-            key = (planned_key(ledger), *spot, nth[spot])
+            key = key_at[m.start()] = (planned_key(ledger), *spot, nth[spot])
             raw_path = m.group("path")
             locator, claim = m.group("locator"), m.group("claim")
             repo, rel = place(root, maps, default_repo, raw_path)
@@ -3383,7 +3389,14 @@ def reverify(
                     continue
                 number = bisect.bisect_right(starts, offset)
                 if new is None or number not in left_whole:
-                    moves.append((ledger, number, coord, old, new))
+                    held = parts.get(key_at[offset])
+                    parts[key_at[offset]] = (
+                        ledger,
+                        number,
+                        coord,
+                        held[3] if held else old,
+                        new,
+                    )
         out, at, said_here = [], 0, []
         for start, end, replacement, said in sorted(kept):
             out.append(text[at:start])
@@ -3398,6 +3411,9 @@ def reverify(
             put(ledger, "".join(out))
             written.append((ledger, said_here, dated, undated))
 
+    if moves is not None:
+        moves.extend(parts.values())
+
     def report(landed):
         said, dated, undated = {}, [], []
         for ledger, said_here, dated_here, undated_here in written:
```

```python
def test_a_ledger_coordinate_restamped_on_two_walks_is_one_move(repo, capsys):
    """Round 3 of #786. A row that is not a citing row can name a ledger line
    among its Code grounds. Where that line is a citing row of a file walked
    again, it moves on two walks, and the move `reverify` appends for it is
    one part, from the hash the ledger held before the run to the hash it
    takes: the pact-change record is written from it, and a part ending at
    the hash of the first walk names a hash no file holds."""
    h = unit_hash(repo, "src/service.py", "handler")
    o = unit_hash(repo, "src/service.py", "other")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"

    def reread(cite):
        return (
            f"| Re-read · the row it cites | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    released(repo, [r1, reread(citation(r1, "R1 · handler adds one"))])
    cite = ec.citation_for(str(repo), str(repo / R_FILE), 5)
    ledger = citation(reread(cite), "Re-read · the row it cites \\|")
    released(
        repo,
        [
            r1,
            reread(cite),
            f"| X1 · other, beside the re-read | `src/service.py#other@{o}`, "
            f"`{ledger}` | read | 2026-01-01 | |",
        ],
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    moves = []
    ec.reverify([str(repo / R_FILE)], str(repo), {}, None, "2026-03-01", moves)
    out = capsys.readouterr().out
    after = (repo / R_FILE).read_text(encoding="utf-8")
    x = [m for m in moves if m[1] == 7]
    assert len(x) == 1, (moves, out)
    old, new = x[0][3], x[0][4]
    assert old == ledger.rsplit("@", 1)[1] and f"@{new}`" in after, (moves, out)
    assert run(["--strict", "."], repo).returncode == 0
```

### Correction 2 — restore round 1's row 1 as `close` wrote it

```sh
git -C <worktree> checkout 89ca97ee -- seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md
```

### Correction 3 — E3's Executed cell

```
old: two short-circuits survive as equivalent (`phases/phase-2.md`);
new: one short-circuit survives as equivalent (`planned_key`), and the `read_here` skip `phases/phase-2.md` called equivalent is load-bearing (round 2, white 2);
```

Needs a fix: yes — 🟡 1 (a ledger coordinate that is not a citation records one pact-change part per walk, the first naming a hash no file held)
Loses a record or crashes: no

The two corrections are paperwork under `seal/` and count toward neither line.
Nothing else is open. Once the orchestrator has placed 🟡 1 on the ladder and
applied the two corrections, the broad gate comes due, and with it the
sealer's spawn.

## Proof block

```
🔎 review applied
· target:   32d0acea (fix range 89ca97ee..44e6f417 and close 32d0acea), base release/v0.18.2 at 94d7b2e0
· opened:   skills/evidence-check/scripts/evidence_check.py (cited_first, reverify, citations_left, record_pact_changes, main's in-place arm, planned_key, read, put, told_now, landed_at, coordinate_of, citation_for, row_citation, citing_verb);
            tests/test_a_released_row_is_read_again_in_a_fragment.py (helpers, the round-1 self-citation case, the three round-2 cases);
            tests/test_a_signatory_records_a_pact_change.py (fixtures, S10, the in-place case);
            seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md, round-2.md, round-2-report.md, overview.md, survivors.md, phases/phase-2.md (lines 66-72);
            seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md;
            docs/review-chain-spec.md (the cap, the reopening, the ladder); docs/round-record-spec.md (a record is derived); docs/the-pact.md (line 132); issue #785
· executed: the probes in the table above, in the clone; bin/evidence-check --strict . at 32d0acea (read-only)
· unverified: the full suite, lint and typecheck — the sealer's, once the run's closing record is written
```

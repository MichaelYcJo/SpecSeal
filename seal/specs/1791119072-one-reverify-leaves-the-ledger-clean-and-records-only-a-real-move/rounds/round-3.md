# 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move — review round 3

| Field | Value |
|---|---|
| Target SHA | 32d0acea3ec0caaa1e9fdd3037c98948606593d2 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #786 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `c05d93ecf2f815e79fd228320e8377dd2ebf8ba5..98e8ba3931e4ed0bb46d6f8e7478ed3e3c56ae7b`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a ledger coordinate that is not a citation records one pact-change part per walk, the first naming a hash no file held) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of #774/#772/#775 (PR #786), the verifying round and the run's last, at 32d0acea: open round 2's fixes (range 89ca97ee..44e6f417) and judge whether each closes its finding with no regression — every line and count `reverify` prints emitted once per coordinate, keyed by ledger, row, coordinate and spelling; the planted `read_here` case and the corrected equivalence claims, including the hand edit to round 1's record; E3's wording and the re-stamped fragment.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A ledger coordinate that is not a row's citation, naming a line a walk of AGAIN moves twice, appends one MOVES part per walk, and the pact-change record writes both: the first ends at a hash no file ever held | `skills/evidence-check/scripts/evidence_check.py:3386` | deferred #791 | #791 — The run is capped: round 2 was its one reopening and this record ends it. The unit is this branch's own repeated walk, so #791 is in milestone 54 and closes by a post-review fix on this pull request, read by a verifying pass; Executed in the clone at 32d0acea: `Pact notify` always, self-citing `0.1.0.md` plus X1 naming the `Re-read ·` line, `--strict` 0 before; record row X1 carries `@5127adb5 → @07b2ad6b` and `@07b2ad6b → @46e82957` while the printed line is one; contradicts round 2's grounds (*the moves list needs no change*), E1's in-place clause, `docs/the-pact.md:132` and the MOVES docstring at `:3070`; the unit is round 1's repeated walk; the fix below gave one part and 509 passed |
| ⬜ 2 | Round 1's closed record was hand-edited in a generated Grounds cell, and row 6 of the same table now points at a sentence row 1 no longer holds | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md:27` | answered | A correction to a record: round 1's record is restored as `close` wrote it (98e8ba39); round 2's record and `overview.md` carry the correction.; Read: row 6 (line 32) says row 1 states the skip is equivalent only after the fix, and that a record of its moment is left as written; `docs/round-record-spec.md` §A record is derived, not typed; the correction already lives in round 2's record and `overview.md`; paperwork, a correction, not on the fix list |
| ⬜ 3 | E3's Executed cell still says two short-circuits survive as equivalent, one of which round 2 showed load-bearing | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:3` | answered | A correction to a record: E3's Executed cell withdraws the equivalence round 2 disproved (98e8ba39).; Read: the overview was corrected and E3 was not; E3 folds into the frozen 0.18.2 release file; paperwork, a correction, not on the fix list |
| 🟢 | round 2's finding 1 is closed — every hash line, re-point line and the count are keyed by ledger, row, coordinate and spelling, each coordinate named once from the hash the ledger held to the one it takes, the two-citing-rows cycle included | `skills/evidence-check/scripts/evidence_check.py:3188` | confirmed | Executed in the clone: planted cases green at 32d0acea; five mutants (no per-row count, offset key, no `first_old`, every walk's line kept, the checker at 89ca97ee) each red; the cycle shape names each citation once with the hash the file holds after the run, `4 rows re-verified` for four coordinates |
| 🟢 | round 2's finding 2 is closed — a case holds the walked-file skip in `citations_left`, and the overview no longer calls it equivalent | `skills/evidence-check/scripts/evidence_check.py:3612` | confirmed | Executed: `test_one_unfrozen_run_names_a_citing_row_it_left_whole_once` green at 32d0acea and red with the skip removed; read `overview.md:12` against `phases/phase-2.md:66-72` |
| 🟢 | the fragment re-stamp is a hash move and nothing else, and the strict check reads it clean | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md` | confirmed | Executed: hash-masked comparison 89ca97ee..44e6f417, 15 rows moved only `reverify@999bffa4 → @9038b161`, E3 rewritten with the sixteenth and three new case coordinates (19 written); `bin/evidence-check --strict .` exit 0 at 32d0acea |
| carried | rounds 1 and 2's 🟢 verdicts — the walk terminates within its bound, the in-place writer records from the row's own hash for code coordinates, the narrowed `LEFT` waits in `told`, the pact sentences are pinned | `skills/evidence-check/scripts/evidence_check.py:3112`, `docs/the-pact.md:130`, `skills/evidence-check/scripts/evidence_check.py:5415` | confirmed | carried, not re-derived: round 2's fixes touch none of these units except `reverify`'s output collection, which the first 🟢 above re-derived; finding 1 narrows the in-place clause to code coordinates |

## Paste-ready fixes

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
```sh
git -C <worktree> checkout 89ca97ee -- seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md
```
```
old: two short-circuits survive as equivalent (`phases/phase-2.md`);
new: one short-circuit survives as equivalent (`planned_key`), and the `read_here` skip `phases/phase-2.md` called equivalent is load-bearing (round 2, white 2);
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3028` | round 1's 🟡 1 — fixed |
| round-1 | `docs/the-pact.md:126` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:5359` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2608` | round 1's ⬜ 4 — answered |
| round-1 | `docs/the-pact.md:117` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/phases/phase-2.md:191` | round 1's ⬜ 6 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3482` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3309` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3549` | round 1's 🟢 — confirmed |
| round-1 | `templates/config.md`, `docs/the-pact.md:146` | round 1's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3308` | round 2's 🟡 1 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3587` | round 2's ⬜ 2 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3112` | round 2's 🟢 — confirmed |
| round-2 | `docs/the-pact.md:130` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:5415` | round 2's 🟢 — confirmed |
| round-2 | `docs/the-pact.md:120` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:9` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md:30` | round 2's carried — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — a ledger coordinate that is not a citation records one pact-change part per walk | candidate: a new `from-review` issue (rung 3); no open issue owns this ground, and #785 is a different mechanism (outranked in-place re-reads) | the orchestrator of this run, for the 0.18.2 milestone: the unit is this branch's own repeated walk, and the fix and its case below are verified in a clone |

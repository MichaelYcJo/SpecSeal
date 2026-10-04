# 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move — review round 2

| Field | Value |
|---|---|
| Target SHA | 2a4ed251f6ca117f3226c0c6c5b625b0d8c9dac9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #786 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `89ca97ee0028cedad7d8c65e206bbbd07383aa15..44e6f417e02a2c87b36e8018331a8aadf3047df4`, 3 commits |
| Contract changes | none |
| New units | HASH_LINE (depth 1); ledger_texts (depth 1); test_one_unfrozen_run_names_each_coordinate_it_restamps_once (depth 1); test_a_row_naming_one_coordinate_twice_is_named_twice (depth 1); test_one_unfrozen_run_names_a_citing_row_it_left_whole_once (depth 1) |
| Needs a fix | yes — 🟡 1 (a citation re-stamped on two walks is named twice, the first line naming a hash no file holds, and counted twice) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #774/#772/#775 (PR #786), the verifying round, at 2a4ed251: open round 1's fixes (range 00736476..6ded9bdd) and judge whether each closes its finding with no regression — the bounded re-walk over files no order can place (termination, bound, output neither duplicated nor lost, one unfrozen run clean for self-citation and cycles, the `moved` mutation's equivalence), the pact sentence split between `--into` and in-place, the narrowed `LEFT` line waiting on the write, the D3 clause — and the fragment's re-stamped `Re-read ·` rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A citation re-stamped on two walks of AGAIN — any citation of a citing row in a file `cited_first` leaves unplaced — is named on two hash lines, the first naming a hash the file never holds, and `N rows re-verified` counts both | `skills/evidence-check/scripts/evidence_check.py:3308` | **fixed** `93803305` | fixed at 93803305 — 1c5fb46d, 44e6f417 — the class is every line or count a repeated walk can say twice. Enumerated over `reverify`'s output: the immediate `say` lines and the `unreadable`, `malformed` and `overflow` lists come from the first walk only; `undatable`, `dated` and `undated` were already de-duplicated; the hash lines, the identical-content re-point lines and the `N rows re-verified` count were not, and those are now keyed by coordinate. The key is the ledger, the row, the coordinate and which of the row's spellings of it this is, never an offset, because a date written on an earlier walk moves every later offset. Each coordinate's line runs from the hash the ledger held before the run to the hash it takes, and the count counts coordinates. The moves list needs no change: code does not move between walks, citations append nothing, and a BROKEN part repeated across walks is dropped by `record_pact_changes`. `test_one_unfrozen_run_names_each_coordinate_it_restamps_once` covers two walks and three walks, dated and undated, red at 2a4ed251 (6 and 10 lines). Its fragment row is dated between two re-stamps, so an offset key goes red. `test_a_row_naming_one_coordinate_twice_is_named_twice` keeps a row's two spellings apart. E3 now says each coordinate is named once; Executed at 2a4ed251: legal tree, `--strict` 0 before; output `5127adb5 -> 07b2ad6b` then `07b2ad6b -> 46e82957`, `6 rows re-verified` for five coordinates written; contradicts W8, E3's *naming nothing twice* and round 1's grounds; the fix below printed one line and 5, and three modules passed (502) |
| ⬜ 2 | The `read_here` skip in `citations_left` is load-bearing, not equivalent: without it an unnarrowed run names a walked file's undatable citing row a second time with a false *the narrowing left this row's file out* line; no case holds it | `skills/evidence-check/scripts/evidence_check.py:3587` | **fixed** `93803305` | fixed at 93803305 — 44e6f417 — `test_one_unfrozen_run_names_a_citing_row_it_left_whole_once` holds the walked-file skip in `citations_left`: green with it, red with it removed. The claim that the skip was equivalent is corrected in this work item's own records: the round-1 record's row 1 grounds and `overview.md`'s proof block. The round-1 report and `phases/phase-2.md` are left as written; Executed at 2a4ed251: headed release table with no date column, `--strict` 0 before; real prints the `undatable` line alone, the mutant adds the false `LEFT`; behaviour correct, so white; the case below is red under the mutant |
| 🟢 | round 1's finding 1 is closed — one unfrozen run leaves `--strict` at 0 for a self-citing release and for two files citing each other, the repeated walk terminates within `chain + 2`, which covers the deepest chain, and every `say` and `LEFT` list is named once | `skills/evidence-check/scripts/evidence_check.py:3112` | confirmed | Executed: four probe shapes plus the shipped cases at 2a4ed251; the `moved[0]` always-true mutant byte-identical on seven shapes, and equivalent by reading; the duplicated hash line is finding 1 above, a new defect in the same walk, not a reopening of this one |
| 🟢 | round 1's finding 2 is closed — `docs/the-pact.md` says `--into` starts at the newest reading and the in-place writer at the row's own hash, both pinned, and the in-place writer records from `m.group("hash")` | `docs/the-pact.md:130` | confirmed | Read `evidence_check.py:3302`; executed: moves list held each row's own hash; the in-place and documents cases passed at 2a4ed251 |
| 🟢 | round 1's finding 3 is closed — the narrowed `LEFT` line waits in `told`, filtered on the cited file landing, and is absent where the record is refused or R's write fails | `skills/evidence-check/scripts/evidence_check.py:5415` | confirmed | Read; the three parameters of the S6 case passed at 2a4ed251; the unfiltered exit agrees because both silent paths already exit 1 |
| 🟢 | round 1's finding 5 is closed — the pact trigger says a citation's re-stamp records nothing, and the skip it describes now rebuilds its offsets on every walk | `docs/the-pact.md:120` | confirmed | Read `evidence_check.py:3143-3147`, `:3359-3361`; executed: no citation part in the moves list |
| 🟢 | The fix pass re-stamped 25 of the fragment's 29 `Re-read ·` rows in place: only code hashes moved, every citation, date and Notes cell is byte-identical, no released file changed, and the claims the moved hashes vouch for hold at the target | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:9` | confirmed | Executed: a hash-masked row comparison over the range; read: P2-1, MALFORMED, O4, R1, R2, H1, C1, W8, W9 and the never-rewrites claim against the code; the prompt's *29* is the row count, 25 moved |
| carried | Round 1's white 4 and white 6 (answered) and its four confirmations — D1 at all four arms, D3's skip, the `planned_key` survivor, #775's pointer and pins | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md:30` | confirmed | Carried, not re-derived: the fix range does not touch `newest_hash`, `released_drift`, `reverify_into`, the `planned_key` loader or #775's files; D3's skip was re-derived above |

## Paste-ready fixes

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ def reverify(
     once, again, bound = cited_first(ledgers, root, maps, default_repo)
     # Whether the last walk of AGAIN changed what it plans (`cited_first`).
     moved = [False]
+    # The hash each coordinate held before the run first re-stamped it, by
+    # ledger, row and coordinate: a citation of a citing row is re-stamped
+    # again on a later walk, and the run names one move for it, first to last.
+    first_old = {}
@@
                             + text[m.end("locator") : m.start("hash")]
                             + new_hash,
-                            f"  {raw_path}#{locator} -> {shown}  (identical content)",
+                            (
+                                (planned_key(ledger), m.start(), raw_path, locator),
+                                f"  {raw_path}#{locator} -> {shown}  "
+                                "(identical content)",
+                            ),
                             # A file moved whole reconstructs with the recorded
@@
             shown = f"{raw_path}#{locator}" + (f">{claim}" if claim else "")
+            key = (planned_key(ledger), bisect.bisect_right(starts, m.start()), shown)
+            was = first_old.setdefault(key, m.group("hash"))
             pending.append((m.start(), shown, m.group("hash"), got))
             edits.append(
                 (
                     m.start("hash"),
                     m.end("hash"),
                     got,
-                    f"  {shown}  {m.group('hash')} -> {got}",
+                    (key, f"  {shown}  {was} -> {got}"),
                     True,
                 )
             )
@@ def reverify(
     def report(landed):
-        lines, dated, undated = [], [], []
+        said, dated, undated = {}, [], []
         for ledger, said_here, dated_here, undated_here in written:
             if landed_at(landed, ledger):
-                lines.extend(said_here)
+                # A coordinate re-stamped on two walks is named once, from
+                # the hash it held to the one it took (`cited_first`).
+                said.update(said_here)
                 # A file walked more than once (`cited_first`) lists a row
                 # both walks dated once.
                 dated.extend(d for d in dated_here if d not in dated)
                 undated.extend(u for u in undated_here if u not in undated)
+        lines = list(said.values())
         changed = len(lines)
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_one_unfrozen_run_names_a_citation_it_restamps_twice_once(repo):
    """Round 2, yellow 1. A fragment cites a released `Re-read ·` row of a
    self-citing release, so the line it cites moves on two walks: its code
    hash and date on the first, its own citation on the second. The run
    names the citation once, with the hash the fragment holds, and counts it
    once. Red at 2a4ed251, which printed it twice, the first line naming a
    hash no file holds, and counted 6."""
    h = unit_hash(repo, "src/service.py", "handler")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"

    def reread(cite, label):
        return (
            f"| Re-read · {label} | `{cite}`, `src/service.py#handler@{h}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        )

    released(repo, [r1, reread(citation(r1, "R1 · handler adds one"), "the row it cites")])
    first = ec.citation_for(str(repo), str(repo / R_FILE), 5)
    released(repo, [r1, reread(first, "the row it cites")])
    frag = fragment(
        repo, [reread(ec.citation_for(str(repo), str(repo / R_FILE), 6), "the re-read")]
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    cited = [
        line
        for line in fix.stdout.splitlines()
        if line.startswith("  seal/") and '>"Re-read · the row"' in line
    ]
    assert len(cited) == 1, fix.stdout
    assert f"@{cited[0].rsplit(' -> ', 1)[1]}`" in frag.read_text(encoding="utf-8")
    assert "5 rows re-verified" in fix.stdout, fix.stdout
    assert run(["--strict", "."], repo).returncode == 0
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_one_unfrozen_run_names_a_citing_row_it_left_whole_once(repo):
    """The walked-file skip in `citations_left` (round 2, white 2). A citing
    row in a table with no date column is left whole by `--checked`, so its
    citation of the line the run re-stamped stays DRIFTED; the `undatable`
    line names it, and no line says a narrowing left its file out. Red with
    the skip disabled."""
    h = unit_hash(repo, "src/service.py", "handler")
    released(
        repo,
        [f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"],
    )
    cite = ec.citation_for(str(repo), str(repo / R_FILE), 5)
    (repo / "seal" / "releases" / "0.2.0.md").write_text(
        "## 0.2.0 — 2026-01-02\n\n### 1000000002-the-second\n\n"
        "| Claim | Code grounds | Verified by | Notes |\n|---|---|---|---|\n"
        f"| Re-read · the row it cites | `{cite}`, `src/service.py#handler@{h}` "
        "| read | Re-read 2026-02-01 |\n",
        encoding="utf-8",
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 1, fix.stdout
    assert (
        "seal/releases/0.2.0.md:7  its hash moved and the row has no date cell"
        in fix.stdout
    ), fix.stdout
    assert "the narrowing left this row's file out" not in fix.stdout, fix.stdout
```

## Executed probes

| What was run | Result |
|---|---|
| Self-citing `0.1.0.md` (R1 and a `Re-read ·` row citing R1), code edited, `--reverify --checked 2026-03-01 .` then `--strict .` at 2a4ed251 | exit 0, `3 rows re-verified`, each dated row once; `--strict` exit 0 |
| The same file plus a fragment whose `Re-read ·` row cites the released `Re-read ·` row; `--strict` before, then the same run | `--strict` 0 before; run exit 0 with the citation named on two lines (`5127adb5 -> 07b2ad6b`, `07b2ad6b -> 46e82957`) and `6 rows re-verified`; `--strict` 0 after |
| Two hand-written citing rows citing each other's lines in one release file | `--strict` 2 before; run exit 0 after four walks, each citation on four lines, `11 rows re-verified`; `--strict` 2 after, both citations DRIFTED |
| Headed release `0.2.0.md` with no date column, its `Re-read ·` row citing `0.1.0.md`'s R1 | `--strict` 0 before; run exit 1, the `undatable` `LEFT` line alone; `--strict` 2 after (the row left whole) |
| The checker with the `moved[0]` test made always-true, on seven shapes | stdout, exit and every ledger file byte-identical to the real checker |
| The checker with the `read_here` skip disabled, on seven shapes | identical on six; on the headed no-date shape it adds `LEFT  seal/releases/0.2.0.md:7  Re-read · the row it cites — its citation of seal/releases/0.1.0.md:5 is DRIFTED: … the narrowing left this row's file out` |
| `reverify` called directly with a `moves` list on the self-citing file | two parts, one per row's code coordinate (`d06d1b56 → 96c68feb`), none for the citation |
| The fix in finding 1 applied in the clone: the four shapes, then the three touched modules (`bin/test` on the fragment, pact-change and `tests/test_evidence_check.py` modules) | one hash line per coordinate (`5127adb5 -> 46e82957`, `5 rows re-verified`); 502 passed |
| The two cases in the paste-ready section: at 2a4ed251, with the `read_here` skip disabled, and with the fix applied | at the target, finding 1's case red (`len(cited) == 1`) and finding 2's case green; with the skip disabled both red; with the fix both green |
| Round 1's new cases at 2a4ed251 (`bin/test` with `-k` over the walk, LEAVINGS, S6, in-place, documents and home cases) | 29 passed |
| Hash-masked before/after comparison of the fragment over `00736476..6ded9bdd` | 29 `Re-read ·` rows, 25 changed, only code hashes in each |
| The full suite, the repository lint and the typecheck at this branch's head | not yet — the sealer's, once the rounds settle; not run by this round |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

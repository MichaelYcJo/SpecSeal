# Review round 2 — the verifying round of #774, #772 and #775 (PR #786)

Target SHA `2a4ed251` on `fix/774-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move`,
base `release/v0.18.2` at `94d7b2e0`. Target of this round: round 1's fix
range `00736476..6ded9bdd` (four commits) and the close commit `2a4ed251`.
Ran by: specseal:warden on claude-opus-5-5. Worked in a `git clone --no-local`
at the target under the session scratchpad; nothing was written in the
checkout but this file.

## Summary

Round 1's three yellows and its one white closed. One unfrozen run now leaves
`--strict` at 0 for a self-citing release file and for two files citing each
other. The walk terminates, the bound is enough for every chain the citations
can form, and the narrowed `LEFT` line prints only after its write lands. The
pact sentences are true and pinned.

The repeated walk opened one new defect. Its suppression covers `say` and
the four `LEFT` lists, but not the hash lines a later walk adds. So a
citation re-stamped on two walks is named twice, and the first of the two
lines names a hash the file never holds (🟡 1). The smith's claim that the
`read_here` shortcut in `citations_left` is equivalent is also false: the
guard is load-bearing and no case holds it (⬜ 2).

## How each round-1 fix was judged

### Round 1, yellow 1 — closed (executed)

The account claimed that the repeated walk terminates, stays inside its
bound, neither duplicates nor loses output, and leaves `--strict` at 0. I
checked each claim against the code and in a probe.

- **Termination.** `walks()` (`evidence_check.py:3112-3120`) runs at most
  `bound` walks of AGAIN, so it terminates in every case. When `moved[0]` is
  False after a walk, it stops early. Executed: a hand-written pair of
  citing rows citing each other's lines never settles. The run stopped after
  four walks (two citations + 2) with exit 0.
- **The bound.** `cited_first` (`:3050-3056`) counts the citations from one
  unplaced file to another. A citation at depth d along a chain of citations
  settles on walk d at the latest (walk 0 re-stamps code), and d is at most
  that count. So `chain + 1` walks always settle the run, and `+ 2` adds the
  walk that observes it settled. Read, then executed on four shapes (below).
- **`--strict` after one run.** Executed, exit 0 for these shapes: a
  self-citing release, a fragment citing that file's released `Re-read ·`
  row, and the shipped two-files-citing-each-other and LEAVINGS cases. The
  only shape left DRIFTED is the hand-written mutual pair, and no writer
  produces it. It was DRIFTED before the run as well (`--strict` exit 2),
  because two lines that each hold the other's hash cannot both be OK.
- **Output not lost.** `say` is silenced on a repeat walk, so a line that
  appeared only on a later walk would be lost. I traced which `say` arms a
  later walk can newly reach. Re-stamping a ledger line never changes its
  first cell or its heading, which are what a citation resolves by. Code
  does not change between walks. So no arm becomes newly reachable. Read.
  `unreadable`, `malformed` and `overflow` are filled on the first walk only.
  `undatable`, `dated` and `undated` are de-duplicated (`:3335`,
  `:3386-3387`). Executed: the LEAVINGS case asserts each once, and my
  probes showed each dated row once.
- **Output not duplicated.** This half fails. See 🟡 1.
- **Moves.** Executed (direct `reverify` call with a `moves` list on a
  self-citing file): two code moves, one per row, and no part for the
  citation. A BROKEN coordinate in a file walked twice appends the same
  `(coord, old, None)` part twice. `record_pact_changes` drops it through
  `dict.fromkeys(coords)` (`:4048`), so nothing is recorded twice. Read.
- **The `moved[0]` test mutated to always-true.** The smith says it is
  equivalent. I confirm it. The mutant differs only when a walk's splices
  reproduce their own text. A hash edit exists only where `got` differs, a
  date-cell edit only where `dated_cell` changes the cell, and a re-point
  that reproduced its span would have resolved through `recorded_here` and
  never reached the splice. Read; executed on seven shapes, where stdout,
  exit and every ledger file were byte-identical to the real checker.
- **The `read_here` shortcut.** The smith calls it equivalent. It is not.
  See ⬜ 2.

### Round 1, yellow 2 — closed (read and executed)

The in-place arm records `(m.start(), shown, m.group("hash"), got)`
(`:3302`), which is the row's own hash. Executed: on a self-citing file the
moves list held `d06d1b56 → 96c68feb` for each row's own coordinate.
`docs/the-pact.md:130-134` says the `--into` writer starts at the newest
reading and the in-place writer starts at the row's own hash. Both
sentences are pinned in the documents case, and
`test_an_in_place_move_starts_at_the_rows_own_hash` passed at the target.
The phrase *whether it writes the row's `Re-read ·` row or refuses it* leaves
out the no-one-place arm and the BROKEN list. Both start at the newest
reading too (`newest_hash` at `:3878`, and `released_drift`'s recorded hash
at `:3903`), and the bold sentence before the phrase covers every move
`--into` records. So the sentence is true.

### Round 1, yellow 3 — closed (read)

`left_cited` waits in `told` and filters on `landed_at(landed, target)`
(`:5415-5425`). When a record is refused, `recorded_then_applied` returns
before `told` is read, so the line never prints. When R's write fails, R's
key is not in `landed`, so the line is filtered out. The exit still counts
`left` unfiltered, but in both of those cases the exit is already 1 (from
the refused record or from `failed`), so the code and the printed lines
agree. The three parameters of
`test_a_narrowed_unfrozen_run_names_the_citation_it_moved_and_left` passed
at the target.

### Round 1, white 5 — closed (read)

`docs/the-pact.md:120-121` states that a citation's re-stamp records nothing.
The in-place arm skips the citation offset (`:3359-3361`). That offset set is
now rebuilt on every walk from the text of that walk (`:3143-3147`), so a
date cell a first walk inserts cannot misalign it. The sentence is pinned.

### The fragment's re-stamped `Re-read ·` rows — allowed, and the claims hold

The fragment holds 29 `Re-read ·` rows, and 25 of them changed in the fix
range, not 29. In each changed row only code-coordinate hashes moved
(`reverify`, `main`, the two doc sections, one test). Every citation of a
released row, every date (2026-10-04) and every Notes cell is
byte-identical. Executed: a script compared each row before and after with
its hashes masked. A fragment is the branch's own and is re-stamped in place
(`docs/the-evidence-ledger.md`, the freeze paragraph), and no released file
changed. I checked the claims the moved hashes vouch for against the code
at the target: P2-1, MALFORMED, O4, R1 (dated once per row), R2, H1, C1, W8,
W9, and the never-rewrites row. All of them hold. W8 says its `LEFT` lines
print as before. The narrowed citation line is the one `LEFT` line that now
waits, and it does so because it claims a write. That is W8's first clause,
so the row stands. Read.

## Findings

### 🟡 1 — A citation re-stamped on two walks is named twice, and the first line names a hash nobody wrote

`skills/evidence-check/scripts/evidence_check.py:3308` (the hash line) and
`:3383` (where `report` joins every walk's `said_here`).

**What is wrong.** A repeat walk silences `say`, but the hash lines its
edits carry go into `written` as on the first walk. `report` concatenates
them without de-duplicating. A citation re-stamps on two walks when the line
it cites changes on two walks, and that is what a citing row's line does:
its code coordinate and date move on walk 0, and its own citation moves on
walk 1. So a citation of a released `Re-read ·` row in a file that
`cited_first` leaves unplaced is re-stamped against the walk-0 line first,
and then against the final line.

**Executed at `2a4ed251`.** The tree held a self-citing `0.1.0.md` (R1, and a
`Re-read ·` row citing R1) and a fragment whose `Re-read ·` row cites that
released `Re-read ·` row. The tree was legal, with `--strict` at exit 0
before the run. The run printed:

```
  seal/releases/0.1.0.md#"### 1000000001-the-first-item">"Re-read · the row"  5127adb5 -> 07b2ad6b
  ...
  seal/releases/0.1.0.md#"### 1000000001-the-first-item">"Re-read · the row"  07b2ad6b -> 46e82957
6 rows re-verified
```

Only five coordinates were written. `07b2ad6b` is a hash no file ever
holds. The ledger file holds `46e82957`.

**Why it matters.** W8 says every hash line names a write that landed. The
first line names a write that never happened, and the count overstates what
moved. The fragment's E3 says this run is *naming nothing twice*, and
round 1's grounds say *a repeated walk names nothing the first named*. Both
are false for this shape. A citation of a citing row is legal: `cited_row`
accepts any ledger row of a released file. It is also reachable without a
hand-made cycle, since a second fold makes the release self-citing. No
record is lost and nothing crashes.

**The class.** I enumerated by construction what makes a line change on two
walks. A row's line changes on walk 0 (a code hash, a date cell) and on the
walk where its own citation moves. Only a citing row has both. So every
instance is a citation of a citing row, in a file AGAIN walks or cites, at
any depth. One more instance follows from the same reading: a hand-written
pair of citing rows citing each other, which never settles, printed each
coordinate four times (`11 rows re-verified` for five coordinates). The fix
below collapses every instance, because it keys the line by coordinate and
not by walk.

**Fix.** Name each coordinate once, from the hash it held before the run to
the hash it took (paste-ready block below). With the fix applied in the
clone, the shape above printed one line, `5127adb5 -> 46e82957`, and
`5 rows re-verified`. The mutual pair printed one line per coordinate. The
three touched modules passed (502).

### ⬜ 2 — The `read_here` shortcut is load-bearing, not equivalent, and no case holds it

`skills/evidence-check/scripts/evidence_check.py:3587`.

**Claimed** (round-1 record, row 1 grounds, and the fix pass): with the
repeated walk, a walked file's citations settle, a row that `--checked` leaves
whole is already named `undatable`, so the guard is equivalent, and the
mutation survived.

**Found.** The second half of that argument is the guard's effect, not its
equivalence. A walked file's citing row in a headed table with no `Checked`
or `Date` column is left whole by `--checked`. Its citation stays DRIFTED
against the plan, and it was OK before the run. With the guard removed, an
**unnarrowed** run prints a second `LEFT` line for that row, which says *the
narrowing left this row's file out; run it without `--ledger`*. Both halves
of that sentence are false. Executed at `2a4ed251` on a legal tree
(`--strict` exit 0 before the run): the real checker printed only the
`undatable` line, and the mutant printed both. The mutation survives because
no case has a citing row without a date cell. It is not equivalent.

**Why white.** The shipped code behaves correctly, so the release ships no
defect. What is missing is the case that keeps the next edit from removing
the guard, and a record that calls a load-bearing line equivalent. The case
is in the paste-ready section (red under the mutation, green at the target).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A citation re-stamped on two walks of AGAIN — any citation of a citing row in a file `cited_first` leaves unplaced — is named on two hash lines, the first naming a hash the file never holds, and `N rows re-verified` counts both | `skills/evidence-check/scripts/evidence_check.py:3308` | open | Executed at 2a4ed251: legal tree, `--strict` 0 before; output `5127adb5 -> 07b2ad6b` then `07b2ad6b -> 46e82957`, `6 rows re-verified` for five coordinates written; contradicts W8, E3's *naming nothing twice* and round 1's grounds; the fix below printed one line and 5, and three modules passed (502) |
| ⬜ 2 | The `read_here` skip in `citations_left` is load-bearing, not equivalent: without it an unnarrowed run names a walked file's undatable citing row a second time with a false *the narrowing left this row's file out* line; no case holds it | `skills/evidence-check/scripts/evidence_check.py:3587` | open | Executed at 2a4ed251: headed release table with no date column, `--strict` 0 before; real prints the `undatable` line alone, the mutant adds the false `LEFT`; behaviour correct, so white; the case below is red under the mutant |
| 🟢 | round 1's finding 1 is closed — one unfrozen run leaves `--strict` at 0 for a self-citing release and for two files citing each other, the repeated walk terminates within `chain + 2`, which covers the deepest chain, and every `say` and `LEFT` list is named once | `skills/evidence-check/scripts/evidence_check.py:3112` | confirmed | Executed: four probe shapes plus the shipped cases at 2a4ed251; the `moved[0]` always-true mutant byte-identical on seven shapes, and equivalent by reading; the duplicated hash line is finding 1 above, a new defect in the same walk, not a reopening of this one |
| 🟢 | round 1's finding 2 is closed — `docs/the-pact.md` says `--into` starts at the newest reading and the in-place writer at the row's own hash, both pinned, and the in-place writer records from `m.group("hash")` | `docs/the-pact.md:130` | confirmed | Read `evidence_check.py:3302`; executed: moves list held each row's own hash; the in-place and documents cases passed at 2a4ed251 |
| 🟢 | round 1's finding 3 is closed — the narrowed `LEFT` line waits in `told`, filtered on the cited file landing, and is absent where the record is refused or R's write fails | `skills/evidence-check/scripts/evidence_check.py:5415` | confirmed | Read; the three parameters of the S6 case passed at 2a4ed251; the unfiltered exit agrees because both silent paths already exit 1 |
| 🟢 | round 1's finding 5 is closed — the pact trigger says a citation's re-stamp records nothing, and the skip it describes now rebuilds its offsets on every walk | `docs/the-pact.md:120` | confirmed | Read `evidence_check.py:3143-3147`, `:3359-3361`; executed: no citation part in the moves list |
| 🟢 | The fix pass re-stamped 25 of the fragment's 29 `Re-read ·` rows in place: only code hashes moved, every citation, date and Notes cell is byte-identical, no released file changed, and the claims the moved hashes vouch for hold at the target | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:9` | confirmed | Executed: a hash-masked row comparison over the range; read: P2-1, MALFORMED, O4, R1, R2, H1, C1, W8, W9 and the never-rewrites claim against the code; the prompt's *29* is the row count, 25 moved |
| carried | Round 1's white 4 and white 6 (answered) and its four confirmations — D1 at all four arms, D3's skip, the `planned_key` survivor, #775's pointer and pins | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md:30` | confirmed | Carried, not re-derived: the fix range does not touch `newest_hash`, `released_drift`, `reverify_into`, the `planned_key` loader or #775's files; D3's skip was re-derived above |

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

## Regression tests to plant

Both go to `tests/test_a_released_row_is_read_again_in_a_fragment.py`, after
the case `test_one_unfrozen_run_restamps_a_citation_no_order_places`. Their
bodies are the fenced blocks under the paste-ready section, and each was seen
in the state it guards against, as the probes table says.

- finding 1: a citation of a released `Re-read ·` row in a self-citing
  release is named once, with the hash the fragment holds, and the count is
  5. Red at 2a4ed251.
- finding 2: a walked file's citing row with no date cell is named by the
  `undatable` line alone. Red with the `read_here` skip disabled, green at
  2a4ed251.

## Facts for the evidence ledger

- E3 in the work item's fragment says *naming nothing twice*. That is false
  at 2a4ed251 for a citation of a citing row (finding 1). Once the fix lands,
  E3 should cite finding 1's case beside `reverify`.
- Round 1's record, row 1 grounds, says the `read_here` short-circuit is
  equivalent. It is load-bearing (finding 2). That is a correction to the
  record, and the case planted for finding 2 is what holds the guard.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 — name each coordinate once across walks

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

### ⬜ 2 — the case that holds the `read_here` skip

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

Needs a fix: yes — 🟡 1 (a citation re-stamped on two walks is named twice, the first line naming a hash no file holds, and counted twice)
Loses a record or crashes: no

## Proof block

Opened at `2a4ed251` (in the clone unless noted):

- `skills/evidence-check/scripts/evidence_check.py`: `read`, `put`,
  `told_now`, `landed_at` (1069-1145); `cited_row`, `citation_for`
  (2214-2390); `row_citation`, `cited_first`, `reverify` (2981-3427);
  `citations_left` (3540-3619); `reverify_into` (3800-3910);
  `record_pact_changes` (4006-4120); `main`'s in-place branch (5330-5440)
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the helpers
  (1-140), and the fix-range diff of the S6, LEAVINGS and walk-order cases
- `tests/test_a_signatory_records_a_pact_change.py`: the fix-range diff
  (the pins, and the in-place case)
- `docs/the-pact.md` 105-145; `docs/the-evidence-ledger.md`: the fix-range
  diff (199-205)
- `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md`:
  the whole range diff, rows 9-37 at 6ded9bdd, and the released rows its
  `Re-read ·` rows cite in `seal/releases/0.4.0.md`, `0.8.3.md`, `0.15.3.md`,
  `0.16.0.md` and `0.18.1.md`
- `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-1.md`
  and `round-1-report.md`; `survivors.md`; `phases/phase-2.md` (grep for the
  equivalence grounds)
- `bin/test`

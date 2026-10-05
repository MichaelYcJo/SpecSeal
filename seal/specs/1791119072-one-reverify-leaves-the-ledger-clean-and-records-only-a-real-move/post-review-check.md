# Post-review check — the #791 fix on PR #786

Target SHA `5ef5d315` on `fix/774-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move`,
base `release/v0.18.2` at `94d7b2e0`. Range read: `baeafe10..5ef5d315`
(`14c24300` the fix, its case, the pact sentence and its pin; `5ef5d315` E1,
E4 and the fragment re-stamped with `--checked 2026-10-05`). This is not a
numbered round: the chain ended capped at round 3, and this pass reads the
post-review fix once. Ran by: specseal:warden on claude-opus-5-5. Worked in a
`git clone --no-local` at the target under
`<scratchpad>/<work-item-id>/post-review/clone`. Nothing was written in the
checkout but this file. The clone, the probe file and its outputs are deleted.

## Summary

The fix closes the shape #791 names. Round 3's probe shape, driven through
`main` with `Pact notify | always`, now records one part for X1,
`@5127adb5 → @46e82957`. A second run records nothing, and `--strict` reads
0 after. The new case is red at `baeafe10` and red when the kept first hash
is mutated to the walk's own.

The collapse has one shape it gets wrong, which `baeafe10` got right. A
coordinate can be re-stamped by one walk and then left by the next walk,
because its claim quotes text the later walk rewrites. The fix keeps the
first walk's old hash and the last walk's `None`. The record then says
BROKEN at the hash the ledger held before the run. It drops the re-stamp
that landed, and it contradicts the line the run printed. A second identical
run appends the same BROKEN again at the hash the file now holds (🟡 1). The
shape is legal (`--strict` 0 before), though contrived.

E1, E4, `docs/the-pact.md` and the MOVES docstring say what the code does for
every shape they name. The docstring's *to the hash it takes* is false only
in 🟡 1's shape. No row of the re-stamped fragment vouches for a claim the
code contradicts. Whether a person re-read the fourteen `Re-read ·` rows on
2026-10-05 is not something the tree records (❓).

## What the account claimed, and what the code does

**Claimed** (commit `14c24300`, #791's checklist): moves are kept one per
coordinate under the key the printed lines use, from the hash the ledger held
before the run to the one it takes, and handed to MOVES once the walks end.

**The code** at `skills/evidence-check/scripts/evidence_check.py:3394-3401`
keeps `parts[key] = (ledger, number, coord, first old, this walk's new)` and
extends MOVES once at `:3415-3416`. The key is `key_at[m.start()]`, built
from the same `(planned_key, row, coordinate, nth)` as `first_old`. Every
`pending.append` uses `m.start()` as its offset, so `key_at[offset]` cannot
miss. Walk order and a row's line number are stable, because no splice adds
a line. That is the claim, and it holds for every walk whose last part is a
real move.

What the claim does not cover is a coordinate whose last walk leaves it.
`new` is then `None`, and the part becomes `(first old, None)` whatever an
earlier walk wrote. Round 2's table said *"a BROKEN part repeated across
walks is dropped by `record_pact_changes`"*. That table covered BROKEN
repeated. It did not cover a move followed by BROKEN, and before this fix
that sequence was handed over part by part, correctly.

## Finding 1 — a re-stamp a later walk leaves is recorded as BROKEN from the pre-run hash, and a second run records it again

**Executed.** In the clone, `seal/releases/0.1.0.md` held R1, a `Re-read ·`
row citing R1, and, under a second `###` heading, X1. X1's ledger coordinate
names the `Re-read ·` line with the claim `"@<the citation's hash>"`. The
second heading keeps X1's own copy of the run outside the region its claim is
read in. `--strict` exited 0 before the run. `handler` was then edited, and
`main` ran `--reverify --checked 2026-03-01 .` with `Pact notify | always`.

- Walk 0 re-stamps R1 and the `Re-read ·` row's code coordinate. X1 still
  matches.
- Walk 1 moves X1 from `5127adb5` to `07b2ad6b` and writes it. It also
  re-stamps the citation, which removes the run X1's claim quotes.
- Walk 2 finds the claim gone, leaves X1 DRIFTED, and appends `(07b2ad6b, None)`.

| | `baeafe10` | `5ef5d315` |
|---|---|---|
| Printed line for X1 | `5127adb5 -> 07b2ad6b` | `5127adb5 -> 07b2ad6b` |
| X1 in the file after run 1 | `@07b2ad6b` | `@07b2ad6b` |
| Record row X1 after run 1 | `…@5127adb5` → `@07b2ad6b`, `…@07b2ad6b` BROKEN | `…@5127adb5` BROKEN |
| Run 2 appends | nothing | a second X1 row, `…@07b2ad6b` BROKEN |

This matters for three reasons:

- **The record contradicts the run.** The permanent record says the
  coordinate went BROKEN at `5127adb5`. The run printed a move to
  `07b2ad6b`, and that move landed.
- **A second run records nothing twice no longer holds for this shape.**
  `record_pact_changes` compares each part with the record's last word for
  the coordinate, and that word is now `(5127adb5, None)`. The next run's
  part is `(07b2ad6b, None)`, so the record gains a duplicate row on every
  later run until somebody repairs X1. The record is permanent and never
  edited by hand, so the duplicate cannot be taken back.
- **The new docstring says the part runs to *the hash it takes*.** Here the
  ledger takes `07b2ad6b`, and the part says `None`.

The defect sits in units created by the post-review fix (`parts` and its
hand-over), so it is this pull request's. Nothing is lost: X1's row is
still recorded and still triggers. So the floor answer is no.

The fix keeps, per coordinate, the first old hash, the last hash a walk
wrote, and whether the last walk left it. It hands over the move when one
landed, then BROKEN at the hash the file holds when the last walk left it.
That collapses round 3's shape to one part (`@5127adb5 → @46e82957`). It
keeps `baeafe10`'s two parts for this one, and a BROKEN repeated across
walks stays one part. Executed in the clone: the case below was red at
`5ef5d315` (`[('5127adb5', None)]`) and green with the fix. The probe's
record became `@5127adb5 → @07b2ad6b, @07b2ad6b BROKEN`, and the second run
added nothing. The three touched modules plus the case gave 510 passed.
`uvx ruff check` and `ruff format --check` were clean on `evidence_check.py`.

## Finding 2 — an unnarrowed run tells the person to run it without `--ledger`

**Executed, in the same probe, at both `baeafe10` and `5ef5d315`.** The run
had no `--ledger`. It still printed `LEFT  seal/releases/0.1.0.md:10  X1 · …
— still DRIFTED: the newest reading of … in its family sits in a file this
run did not write; run it without `--ledger``. That remedy cannot clear X1,
because the run itself moved the line X1's claim quotes. The line comes from
`main` at `evidence_check.py:5441-5447`, released with #743. It is outside
the post-review range and not this fix's regression, so it is reported for
the orchestrator to file, not for this pull request's fix list.

## How each question in the prompt was answered

- **MOVES one part per coordinate across walks.** Executed. True for round
  3's shape: one part through `main` with `Pact notify | always`, nothing on
  a second run, `--strict` 0 after. True for a BROKEN repeated across walks
  (read: last-wins on `None` with the first old hash). False for a move
  followed by BROKEN (🟡 1). A BROKEN followed by a move collapses to the
  move, from the first old hash (read), which is right.
- **The new case red at `baeafe10`.** Executed: red there (`assert 2 == 1`,
  parts `5127adb5 → 07b2ad6b` and `07b2ad6b → 46e82957`). It is also red with
  `held[3] if held else old` mutated to `old`, and green at `5ef5d315`.
- **E1, E4, `docs/the-pact.md:132-133`, the MOVES docstring at
  `evidence_check.py:3074-3077`.** Read. Each says one part per coordinate
  from the hash the ledger held before the run. That is what the code does,
  except that the docstring's *to the hash it takes* is false in 🟡 1's shape.
  `tests/test_docs_line_wrap.py` and
  `tests/test_a_folded_statement_names_what_enforces_it.py` passed (67).
- **The fragment re-stamp.** Read, by a word-level diff over
  `baeafe10..5ef5d315`. Nineteen rows gained `· 2026-10-05`. The hash moves
  are `reverify@9038b161 → @c228822f` (fifteen coordinates), the
  `docs/the-pact.md` section `5b9bc01c → a07d7285`, and its pin `7984447a →
  e1217a3b`. E1 and E4 are rewritten, and E4's Executed cell carries the
  2026-10-05 reading. The fourteen dated `Re-read ·` rows vouch for released
  claims about walking, dating, naming, strict reads and re-anchoring. The
  diff changes none of those. Only C1 says anything about the record: *the
  same move or the same BROKEN is not appended again*. It still holds
  literally, though 🟡 1 defeats its purpose. A date cell beside Notes that
  still say `Re-read 2026-10-04` is the shape the fragment's own `Corrected ·`
  row (line 8) documents for an in-place re-stamp. So no row's date vouches
  for a claim the code contradicts. Whether a person read each of the
  fourteen on 2026-10-05 is not recorded anywhere, because `5ef5d315`'s
  message says only that the fragment was re-stamped (❓).

## Regression test to plant

Destination: `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
beside `test_a_ledger_coordinate_restamped_on_two_walks_is_one_move`. It is
the case under `## Paste-ready fixes`, seen red at `5ef5d315`.

## Facts for the evidence ledger

- If finding 1's fix lands, E4's clause gains a second half: a coordinate
  one walk re-stamps and a later walk leaves appends that move and then BROKEN
  at the hash it holds. E4 then gains the new case as a coordinate, and E1's
  `reverify` coordinate moves.
- The pact sentence at `docs/the-pact.md:132-133` and its pin in
  `tests/test_a_signatory_records_a_pact_change.py` change together, per the
  block below.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A coordinate one walk re-stamps and a later walk leaves is handed to MOVES as BROKEN from the hash the ledger held before the run: the record drops the re-stamp that landed, contradicts the printed line, and a second identical run appends the same BROKEN again at the hash the file holds | `skills/evidence-check/scripts/evidence_check.py:3394` | open | Executed in the clone at 5ef5d315, legal tree (`--strict` 0 before): X1 under a second heading of a self-citing release file, its claim quoting the citation hash; printed `5127adb5 -> 07b2ad6b`, file holds `@07b2ad6b`, record `@5127adb5` BROKEN, run 2 appends `@07b2ad6b` BROKEN; at baeafe10 the record held the move and BROKEN at `07b2ad6b` and run 2 added nothing; units created by 14c24300; the fix below was green, with 510 passed over the three touched modules plus the case |
| ⬜ 2 | An unnarrowed `--reverify` names a coordinate it left DRIFTED with the remedy *run it without `--ledger`* | `skills/evidence-check/scripts/evidence_check.py:5441` | open | Executed in the same probe at baeafe10 and 5ef5d315, no `--ledger` passed; a released unit (#743), outside the post-review range and not this fix's regression; for the orchestrator to file |
| 🟢 | #791's shape is closed — round 3's probe shape records one part for X1, from the hash the ledger held to the one it takes, and a second run records nothing | `skills/evidence-check/scripts/evidence_check.py:3394` | confirmed | Executed through `main` with `Pact notify` always at 5ef5d315: record row X1 `@5127adb5 → @46e82957`, run 2 nothing, `--strict` 0 after; at baeafe10 the same probe recorded two parts |
| 🟢 | the new case is a case — red at baeafe10, red with the first hash mutated, green at the target | `tests/test_a_released_row_is_read_again_in_a_fragment.py:2658` | confirmed | Executed: baeafe10's checker in the clone gave `assert 2 == 1`; `held[3] if held else old` replaced by `old` gave 1 failed |
| 🟢 | E1, E4, the pact sentence and its pin, and the MOVES docstring say what the code does for the shapes they name | `docs/the-pact.md:132` | confirmed | Read against `evidence_check.py:3074`, `:3394`, `:3415`; the docstring's *to the hash it takes* is false only in finding 1's shape, and its fix below carries the sentence; executed: the line-wrap and folded-statement modules, 67 passed |
| 🟢 | the fragment re-stamp moved hashes and dates and nothing else, and no date vouches for a claim the code contradicts | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:9` | confirmed | Read: word diff baeafe10..5ef5d315, 19 rows `· 2026-10-05`, coordinates moved `reverify` (15), the pact section and its pin; E1 and E4 rewritten; the fourteen `Re-read ·` claims checked by subject against the diff, which changes only MOVES collection; the date-cell-without-Notes shape is the one the fragment's line 8 documents |
| ❓ | Whether a person re-read each of the fourteen `Re-read ·` rows on 2026-10-05, as their date cells now say | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:9` | ❓ out of verified scope | No record carries that reading: 5ef5d315's message names the re-stamp only, and the rows' Notes still say 2026-10-04; the orchestrator answers it from the smith's handover |

## Executed probes

| What was run | Result |
|---|---|
| Round 3's shape (X1 naming the `Re-read ·` line by its label) through `main`, `Pact notify` always, `handler` edited, `--reverify --checked 2026-03-01 .` twice, `--strict` between | at 5ef5d315: X1 one part `@5127adb5 → @46e82957`, run 2 nothing, `--strict` 0; at baeafe10: two parts, `→ @07b2ad6b` and `@07b2ad6b → @46e82957` |
| The same with X1 under a second heading, its claim quoting the citation hash, `--strict` 0 before | at 5ef5d315: printed `5127adb5 -> 07b2ad6b`, record `@5127adb5` BROKEN, `--strict` 2 after, run 2 appends `@07b2ad6b` BROKEN; at baeafe10: record holds the move and `@07b2ad6b` BROKEN, run 2 nothing; both print the `run it without --ledger` LEFT line |
| `test_a_ledger_coordinate_restamped_on_two_walks_is_one_move` against baeafe10's `evidence_check.py`, and against `held[3] if held else old` mutated to `old` | red both times (2 parts; 1 failed) |
| Finding 1's case at 5ef5d315, then with finding 1's fix | red (`[('5127adb5', None)]`), then green |
| Finding 1's fix: the three touched modules plus the case; `uvx ruff check`, `ruff format --check` on `evidence_check.py` | 510 passed; clean |
| `tests/test_docs_line_wrap.py` and `tests/test_a_folded_statement_names_what_enforces_it.py` at 5ef5d315 | 67 passed |
| The full suite, the repository lint and the typecheck at this branch's head | not yet — not run by this pass; the sealer's, once the post-review fix settles |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 2 — an unnarrowed `--reverify` prints *run it without `--ledger`* for a coordinate it left DRIFTED itself | candidate: a new `from-review` issue; the unit is released (#743) and outside this range | the orchestrator of this run, filing it for the next milestone |

## Paste-ready fixes

### Finding 1 — hand over the move that landed, then BROKEN at the hash the file holds

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ -3074,8 +3074,9 @@ def reverify(
     whole under `--checked` moved nothing and appends nothing. A coordinate
     re-stamped on more than one walk (`cited_first`) appends one part, from
     the hash the ledger held before the run to the hash it takes, once the
-    walks end (#791). It is what `record_pact_changes` writes a signatory's
-    pact changes from, before the hash it read is gone.
+    walks end (#791); one a later walk leaves then appends BROKEN at the
+    hash an earlier walk wrote. It is what `record_pact_changes` writes a
+    signatory's pact changes from, before the hash it read is gone.
 
     Re-verifying is recomputing the hash, which is a person saying they have
     re-read the code. It is deliberately a separate command: a check that
@@ -3391,13 +3392,18 @@ def reverify(
                     continue
                 number = bisect.bisect_right(starts, offset)
                 if new is None or number not in left_whole:
-                    held = parts.get(key_at[offset])
+                    # The hash the ledger held before the run, the last hash
+                    # a walk wrote, and whether the last walk left it BROKEN:
+                    # a re-stamp an earlier walk landed stays a move, and a
+                    # BROKEN after it is recorded at the hash the file holds.
+                    _where, first, landed, _broken = parts.get(
+                        key_at[offset], (None, old, None, False)
+                    )
                     parts[key_at[offset]] = (
-                        ledger,
-                        number,
-                        coord,
-                        held[3] if held else old,
-                        new,
+                        (ledger, number, coord),
+                        first,
+                        landed if new is None else new,
+                        new is None,
                     )
         out, at, said_here = [], 0, []
         for start, end, replacement, said in sorted(kept):
@@ -3413,7 +3419,11 @@ def reverify(
             put(ledger, "".join(out))
             written.append((ledger, said_here, dated, undated))
     if moves is not None:
-        moves.extend(parts.values())
+        for where, first, landed, broken in parts.values():
+            if landed is not None:
+                moves.append((*where, first, landed))
+            if broken:
+                moves.append((*where, landed or first, None))
 
     def report(landed):
         said, dated, undated = {}, [], []
```

```python
def test_a_restamp_a_later_walk_leaves_is_a_move_and_then_broken(repo):
    """Post-review of #791. X1's coordinate quotes, as its claim, the hash of
    a citation the second walk re-stamps. The first walk that reaches X1
    moves it to the hash of the line as that walk found it, and the walk
    after finds the quoted run gone and leaves it. The file keeps the first
    hash, so MOVES holds that move and then BROKEN at the hash the file
    holds: a BROKEN from the hash the ledger held before the run drops a
    re-stamp that landed, and a second run records the same BROKEN again.
    Red at 5ef5d315, which handed over BROKEN from the pre-run hash alone."""
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
    # Under a second heading, so X1's own copy of the run is outside the
    # region its claim is read in.
    line = citation(reread(cite), f"@{cite.rsplit('@', 1)[1]}")
    (repo / R_FILE).write_text(
        f"## 0.1.0 — 2026-01-01\n\n{SECTION}\n\n{r1}\n{reread(cite)}\n\n"
        "### 1000000002-the-second-item\n\n"
        f"| X1 · other, beside the re-read | `src/service.py#other@{o}`, "
        f"`{line}` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    moves = []
    ec.reverify([str(repo / R_FILE)], str(repo), {}, None, "2026-03-01", moves)
    after = (repo / R_FILE).read_text(encoding="utf-8")
    held = re.search(r'"@[0-9a-f]+"@([0-9a-f]+)`', after).group(1)
    x = [(old, new) for _l, number, _c, old, new in moves if number == 10]
    assert x == [(line.rsplit("@", 1)[1], held), (held, None)], (moves, held)
```

```
docs/the-pact.md:132-133, and its pin in tests/test_a_signatory_records_a_pact_change.py:
old: A re-stamp in place records each row's move from that row's own hash,
     one move per coordinate however many walks re-stamp it (#791).
new: A re-stamp in place records each row's move from that row's own hash,
     one move per coordinate however many walks re-stamp it, and BROKEN
     after it at the hash it holds where a later walk leaves it (#791).
E4, appended to its clause:
     ; one a later walk leaves after an earlier walk re-stamped it appends that move and then BROKEN at the hash it holds
```

Needs a fix: yes — 🟡 1 (a coordinate one walk re-stamps and a later walk
leaves is recorded BROKEN from the pre-run hash, and a second run records it
again)
Loses a record or crashes: no

## Proof block

Files opened in this pass:

- `skills/evidence-check/scripts/evidence_check.py` — `reverify` (`:3059-3468`),
  `record_pact_changes` (`:4048-4255`), `pact_change_item`, `minor_region`,
  `literal_statements`, `unescape`, `ANCHOR_RE`, `main` (`:5405-5455`)
- `tests/test_a_released_row_is_read_again_in_a_fragment.py` — helpers
  (`:1-140`), `:1365-1380`, `:2370-2450`, the new case (diff)
- `tests/test_a_signatory_records_a_pact_change.py` — the pin (diff), the
  index of cases
- `docs/the-pact.md:126-140`
- `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md`
  — every row's first, date and Notes cells; E1 to E4 whole
- `seal/releases/0.18.1.md` — rows C1, W9 and R2 (grep)
- `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/rounds/round-3.md`,
  `rounds/round-3-report.md`, `rounds/round-2.md` (rows 27-32),
  `phases/phase-3.md`
- issue #791 (body); commit messages of `14c24300` and `5ef5d315`
- `bin/test`

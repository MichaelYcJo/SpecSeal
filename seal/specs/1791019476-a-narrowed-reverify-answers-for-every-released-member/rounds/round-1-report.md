# Round 1 report — #740, a narrowed `--reverify` answers for every family a file it read holds a member of

Ran by: `specseal:warden on claude-opus-5-5`.

| Field | Value |
|---|---|
| Work item | `1791019476-a-narrowed-reverify-answers-for-every-released-member` |
| Branch | `fix/740-a-narrowed-reverify-answers-for-every-released-member` |
| Target SHA | `a7ba069f` |
| Base | `origin/release/v0.18.0` at `2b1dcb1f` |
| Diff | `2b1dcb1f..a7ba069f` |
| Where it ran | a `git clone --no-local` of the worktree at `a7ba069f`, under the session scratchpad; the worktree's HEAD was never moved |

## Summary

One finding needs a fix. The 72-cell grid holds one axis fixed that the
property depends on: **which members carry the coordinate**. Where a
coordinate is carried only by fragment members — a `Re-read ·` row that adds
a unit its root does not cite, as several rows of #736's own fragment do —
a run narrowed to the fragment holding the older reading still writes
nothing and exits 0, while `--strict` with the same narrowing exits 2. That
is the class this item closes, one axis over. It is red in all three modes at
`a7ba069f`. A paste-ready fix closes all three, and it keeps the module and
its two siblings green (154 passed).

The other eight findings are ⬜: wording, docstrings, one unpinned scenario
and two record corrections. The integration claim holds: merging #742 into
the clone and resolving the two hunks by hash leaves `evidence-check
--strict .` at 0 drifted.

## Stage 1 — spec compliance

### D1, D2 and the grid (S1–S5)

**Read.** `released_drift` now tests every member of a family against every
file LEDGERS names (`read_here`). The freeze branch of `main` hands the whole
narrowed list to `reverify_into`. Both match D1 and D2.

**Executed.** The module passes at `a7ba069f`: 126 passed, which includes S1,
S2, the 72 cells and the control.

**Axes the prompt asked about, executed.** Each of these runs in all three
modes (warden probes P2–P4):

- **A family with members in four files.** R is in 0.1.0, M1 in 0.2.0, M2 in
  0.3.0, and N in a fragment; the run is narrowed to 0.3.0. It holds:
  `--reverify` exits 1 where it should, and with `--into` it writes the row
  and the whole tree checks clean.
- **`seal/ledger.md` as the narrowed file.** Two placements were run: R there
  with M in 0.2.0, and M there with R in 0.1.0. Both hold, because
  `ledger_kind` returns `released` for it.
- **A family rooted at a folded `Corrected ·` row.** C is in 0.2.0 and
  corrects R in 0.1.0. M re-reads C in 0.3.0, and N re-reads C in a
  fragment. Narrowed to 0.1.0, nothing is owed: R is superseded, and both
  `--strict` and `--reverify` exit 0. Narrowed to 0.2.0 or 0.3.0, the
  narrowing holds.

**The cell outside the grid where the rule fails — 🟡 1, executed.** Here is
the setup:

- R in `seal/releases/0.1.0.md` cites `handler` alone.
- M, in fragment A, re-reads R and adds `other` at o1, dated 2026-02-01.
- N, in fragment B, re-reads R with `other` at o2, dated 2026-03-01.
- The code holds `other` at o1.

The run is narrowed to fragment A. Every mode gives the same result:
`--reverify` exits 0, writes nothing and names nothing, while `--strict
--ledger <A>` exits 2 and reads M DRIFTED as outranked. With N folded into
a release the cell holds, because N is a released member. At `2b1dcb1f` both
placements of N fail, so this item fixed half of this cell's class and left
the other half.

The cause is `evidence_check.py:3292`. The second loop of `released_drift`
grades a coordinate from **released members only**:

```
for key, m, status, detail in graded:
    if ledger_kind(root, view.files[key[0]][0]) != "released":
        continue
```

When no released member carries the coordinate, the family is skipped,
though the filter above it has just admitted it because a fragment member
sits in a file the run read. The in-place re-stamp cannot reach N, because
N's file is outside the narrowing. So nothing answers for the family.

**Is it real here?** It is. #736's fragment holds rows of exactly this shape:
the `Re-read ·` rows whose Verified cell reads "now rests on both" add
`classify`, which the released row they cite does not carry. Two unfolded
fragments re-reading one released row on two days, as the freeze invites,
is this cell.

**What it makes false.** Each of these sentences is false in that cell:

- the home's new sentence at `docs/the-evidence-ledger.md:137`, *either form
  answers for every family that a file it read holds a member of, released
  or fragment*;
- the rewritten sentence at `docs/the-evidence-ledger.md:163`;
- L4's corrected claim and N1's first clause;
- the changelog fragment's first entry.

N1's last clause is scoped to the 72 cells and stays true.

### D3 — the root claim

**Read.** D3 says *every family's root is released*. That is false:

- `root_of` stops at any verb but `Re-read`, so a `Corrected ·` row in a
  fragment roots its own family.
- `cited_row` returns no target for a citation into a fragment, so a citing
  row whose citation does not resolve also roots its own.

**Does it matter at `a7ba069f`?** No. The second loop of `released_drift`
skips every member that is not released, so a fragment-rooted family adds
nothing. Such families are singletons, because a citation into a fragment
joins nothing. The overview records this divergence, and its conclusion is
right.

**It does matter for any fix that widens the loop.** At the base,
`if top[0] not in wanted` kept fragment-rooted families out entirely. Now
the new filter admits them, and only the released-member filter keeps them
inert. 🟡 1's fix has to widen exactly that filter, so the fix has to guard
on the root's kind, or a fragment `Corrected ·` row would be named as a
released row and cited by a `Re-read ·` row, which the checker refuses as
MALFORMED. The fix below carries the guard. ⬜ 9 asks that the spec's
sentence say so, because the next widening will read D3 first.

### D4 — the root is named

**Executed.** S2 pins the no-freeze `LEFT` line naming
`seal/releases/0.1.0.md:5`, and S1 pins `citing seal/releases/0.1.0.md:5`
under `--into`.

**S3 is not pinned.** S3 requires the run under the freeze without `--into`
to name the root together with the `--into` repair. The enumeration asserts
only the exit code and the digests, and accepts exit 1 whatever the run
printed. The probes show that the code names the root (warden probe
CONTROL, `freeze without --into`), but no case holds it. That is ⬜ 7.

### D5 and ⬜ 17 — the wording and the plural

**Executed.** The case passes at `a7ba069f` for all three cells.

- **⬜ 2 — the home says the singular.**
  `docs/the-evidence-ledger.md:103` says *a reading dated only by one is
  named with that date as written*. The code names every date-shaped string
  in the cell (`evidence_check.py:2501-2508`), and the case pins a cell
  holding two. Read literally, the home describes a different message from
  the one the code prints.
- **⬜ 3 — the plural message reads as a list of three.** The text is *the
  reading dated 2026-13-45, 2026-02-30, dates the calendar does not have*. A
  comma list followed by a comma clause makes the third item look like part
  of the list. A repeated string is also named twice and counted as plural.
  D5 fixed the `, ` join only for its one-string example, and phase 2 records
  that the plural form was the smith's choice.
- **⬜ 4 and ⬜ 5 — the rejected wording describes the new message.** The
  `reading` docstring (`evidence_check.py:2495`) and N2 (this item's
  fragment, line 2) both describe the message as *said to be no date the
  calendar has*. That is Q2(a)'s wording, which the frame rejected. The
  printed message reads *a date the calendar does not have*. A reader of N2
  would look for the wording the code does not print.

### The ledger

**Executed.** `git diff --name-only 2b1dcb1f...HEAD -- seal/releases
seal/ledger.md` is empty, so S8's second half holds.

**Executed.** At `a7ba069f`, `evidence-check --strict .` reads 4,017 ok and 9
drifted, with exit 2. That matches the build's account.

**Executed — the integration claim.** I merged
`origin/chore/0-18-0-the-four-items-read-each-other-after-the-squash`, at
`5463fd82`, into the clone with `--no-commit`. Only #736's fragment
conflicted, in two hunks: lines 17–18 and 29–30.

- I resolved each line anchor by anchor against the merge base. Where one
  side moved a hash, that side's hash was kept.
- No anchor was moved by both sides, and no non-hash text differed.
- The four lines split as follows: one moved by this branch alone, two by
  the integration branch alone, and one with one anchor moved by each.

After the resolution `evidence-check --strict .` reads 4,026 ok, 0 drifted,
exit 0. I aborted the merge afterwards.

**Read — the ten rows of #736's fragment re-stamped by the build.** Each claim
was checked against the edit.

| Row | Unit moved | Holds? |
|---|---|---|
| L1 | `#family_view` | Holds. The family rule and the ordering are unchanged, and `reading` changes words only |
| L4 | `#released_drift`, `#reverify_into`, `#main` | Corrected in place, with a `Corrected 2026-10-03 by work item 1791019476 (#740)` note and the earlier notes kept. The narrowing clause is false in 🟡 1's cell; otherwise it describes the code |
| L9 | the home's section | Holds. The two added sentences restate nothing a carrier must not restate, and the one-home module passes (executed) |
| `Re-read · O3` (line 15) | `#main` | Holds. `OVERFLOW` grading is untouched |
| `Re-read · R4` (line 17) | `#main` | Holds. `--checked` validation is untouched |
| `Corrected ·` the de-duplication (line 25) | `#family_view` | Holds. The de-duplication and the per-row family grading are unchanged |
| `Re-read ·` the checker and the unverified reader (line 26) | `#main` | Holds. The edit is a comment and the freeze branch's argument |
| `Re-read ·` every place a ledger path becomes a name (line 30) | `#main` | Holds. The `LEFT` lines print through `built_name`, which calls `display_name` |
| `Re-read · R5` (line 32) | `#main` | Holds. The records arm is untouched |
| `Corrected ·` the freeze rule's home (line 57) | the home's section | Holds |

**The notes.** No Notes cell gained a trace of #740's re-read. That matches
the integration branch's own re-stamps of the same fragment in `bb2f3400`,
so it is not a finding.

**N1 and N2.**

- N1's coordinates resolve.
- N1's first clause is false in 🟡 1's cell, and N1's scoped clause is true.
- N2's claim is right apart from ⬜ 5's quotation.

### The rules: UTF-8 and `os.sep`

**Read.** The checker gains no file I/O. The new cases pass
`encoding="utf-8"` on every read and write. Their printed-path comparisons go
through `built_name`, which replaces the separator with `/` on every
platform, or through `ledger_section`, which normalises with
`.replace(os.sep, "/")`.

**Not executed.** The Windows leg was not run, so the separator rule rests on
reading. The ❓ row below says who answers it.

## Stage 2 — quality

- **⬜ 6 — two docstring sentences in the new cases are not held.**
  - The control's docstring (`tests/…_in_a_fragment.py:1489`) says *Without
    the correction the same narrowing exits 1.* No assertion holds it, and
    under `freeze with --into` it is false: the run writes the row and exits 0
    (executed, warden probe CONTROL).
  - The enumeration's docstring (`:1457-1458`) says a run that read no member
    *says which files it skipped*. Nothing asserts that either.
- **⬜ 8 — a double correction is a DRIFTED that no `--reverify` names,
  narrowed or not.** Here is the setup: two fragment `Corrected ·` rows both
  correct R. `--strict` exits 2, naming each row as *corrected by 2 rows*.
  `--reverify` exits 0 in every mode, both narrowed to one of the two rows
  and unnarrowed (executed, warden probe P5). This behaviour comes from #736
  and is not a narrowing defect. A re-read cannot clear it, because a person
  has to choose the claim. But the home's rewritten sentence at `:163` now
  says the run names *each family … where no in-place re-stamp of the files
  it read clears that family*, and this family is not named. One sentence
  scopes the promise to what a re-read can clear.
- **⬜ 9 — spec D3's premise.** See D3 above. This is a correction to a
  record.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A coordinate carried only by fragment members escapes a narrowed `--reverify`. Narrowed to the fragment holding the older reading, with the newest in another fragment, the run exits 0 and writes nothing in all three modes, while the narrowed `--strict` exits 2. The home's two new sentences, L4, N1's first clause and the changelog entry are false there | `skills/evidence-check/scripts/evidence_check.py:3292` | open | Executed. Red at `a7ba069f` in 3 of 3 modes and at `2b1dcb1f` for both placements of N. Green in 3 of 3 with the paste-ready fix, which keeps 154 cases of the module and two siblings passing |
| ⬜ 2 | The home says a reading dated only by one impossible date is named with that date; the code names every date-shaped string, and the case pins two | `docs/the-evidence-ledger.md:103` | open | Read against `evidence_check.py:2501-2508` and the case's second cell |
| ⬜ 3 | The plural message joins the dates with `, ` and then adds `, dates …`, which reads as three items; a repeated string is named twice | `skills/evidence-check/scripts/evidence_check.py:2505` | open | Read. Phase 2 records that the plural form was the smith's choice, so D5 did not decide it |
| ⬜ 4 | The `reading` docstring describes the message with Q2(a)'s rejected wording, *no date the calendar has* | `skills/evidence-check/scripts/evidence_check.py:2495` | open | Read against the f-string four lines below it |
| ⬜ 5 | N2 quotes the message as *said to be no date the calendar has*, the rejected wording, not the text the code prints | `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md:2` | open | Read. This is a correction to the run's records |
| ⬜ 6 | The control's docstring says the uncorrected narrowing exits 1, which is false under `freeze with --into`; the enumeration's docstring promises a skipped-files notice nothing asserts | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1489` | open | Executed: the uncorrected narrowing exits 1, 1 and 0 across the three modes |
| ⬜ 7 | S3's root naming under the freeze without `--into` is not pinned; the enumeration accepts any exit-1 output | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1445` | open | Read. The code names the root today (executed, CONTROL), and nothing holds it |
| ⬜ 8 | A double correction is DRIFTED under `--strict` and named by no `--reverify`, narrowed or not, while the rewritten home sentence promises every family no re-stamp clears | `docs/the-evidence-ledger.md:163` | open | Executed (P5): `--reverify` exits 0 and `--strict` exits 2, narrowed and unnarrowed. The behaviour comes from #736; the sentence is this item's |
| ⬜ 9 | Spec D3's premise, *every family's root is released*, is false; the conclusion holds only through the released-member filter, which 🟡 1's fix has to widen | `seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/spec.md:72` | open | Read: `root_of` and `cited_row`. This is a correction to the run's records |
| 🟢 | The integration claim: with #742 merged and the two hunks resolved by hash, `--strict .` reads 0 drifted | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Executed: 4,026 ok and 0 drifted after the merge; 4,017 ok and 9 drifted at `a7ba069f` |
| 🟢 | S8's second half: no released ledger file changed | `seal/releases`, `seal/ledger.md` | confirmed | Executed: the name-only diff is empty |
| 🟢 | The ten re-stamped rows of #736's fragment hold against the edit, except L4's narrowing clause, which is 🟡 1 | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Read, row by row; table above |
| 🟢 | The grid holds for four-file families, for `seal/ledger.md` in either placement, and for a family rooted at a folded `Corrected ·` row | `skills/evidence-check/scripts/evidence_check.py:3286` | confirmed | Executed, P2–P4, 24 runs, no violation |
| ❓ | The Windows leg: the separator handling of the new cases | `tests/test_a_released_row_is_read_again_in_a_fragment.py` | ❓ out of verified scope | Read only: `built_name` and `ledger_section` normalise. The pull request's Windows CI leg answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py -q` at `a7ba069f` | 126 passed |
| `bin/test` over the one-home, docs line-wrap, no-real-identifiers, one-word-one-meaning and merge-correction modules at `a7ba069f` | 134 passed |
| `evidence-check --strict .` at `a7ba069f` | 4,017 ok, 9 drifted, exit 2 |
| `git diff --name-only 2b1dcb1f...HEAD -- seal/releases seal/ledger.md` | empty |
| merge of `5463fd82` with `--no-commit`, two hunks resolved anchor by anchor, then `evidence-check --strict .`, then `git merge --abort` | 4,026 ok, 0 drifted, exit 0 |
| Warden probe P1: coordinate carried by fragment members only, N in a fragment, 3 modes, at `a7ba069f` | 3 of 3 violate: `--reverify` 0, narrowed `--strict` 2 |
| Warden probe P1 with N folded into 0.3.0, 3 modes, at `a7ba069f` | 3 of 3 hold |
| Warden probe P1, both placements, against `2b1dcb1f`'s checker | 6 of 6 violate |
| Warden probe P1 with the paste-ready fix applied | 6 of 6 hold |
| Warden probes P2–P4: four-file family, `seal/ledger.md`, `Corrected ·` root, 3 modes each | 24 of 24 hold |
| Warden probe P5: double correction, narrowed and unnarrowed, 3 modes | 6 of 6: `--reverify` 0, `--strict` 2 |
| Warden probe CONTROL: the uncorrected superseded-control family narrowed to R's file | exit 1, 1, 0 for no freeze, freeze without `--into`, freeze with `--into` |
| The paste-ready 🟡 1 case at `a7ba069f`, then with the fix | 3 failed, then 3 passed |
| The module and two siblings (`test_two_branches_re_read_one_released_row.py`, `test_a_narrowed_ledger_read_says_what_it_skipped.py`) with the paste-ready fix | 154 passed |
| ⬜ 7's paste-ready case at `a7ba069f` | 2 passed; not yet seen red |
| `evidence-check --strict .` records arm, with this report copied into the clone | no refusal from this report; the 4 refusals are the base's, in `1790993137`'s records |
| `bin/test tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py` with this report tracked in the clone | 24 passed |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, once the rounds settle |
| `bin/survivor-check --range 2b1dcb1f...HEAD` (S9) | not run by this round; the builder's account only |

```
# P1's family, as the probe built it (warden probe, deleted)
R  seal/releases/0.1.0.md                   | R1 · handler adds one | `src/service.py#handler@h1` | read | 2026-01-01 | |
M  seal/ledger/2000000002-the-older-re-read.md | Re-read · R1 · … | `<cite R>`, `src/service.py#other@o1` | read | 2026-02-01 | Re-read 2026-02-01 |
N  seal/ledger/3000000003-the-newer-re-read.md | Re-read · R1 · … | `<cite R>`, `src/service.py#other@o2` | read | 2026-03-01 | Re-read 2026-03-01 |
code: other at o1
evidence-check --reverify [--into …] --ledger seal/ledger/2000000002-the-older-re-read.md .   -> exit 0, "0 rows re-verified" / "0 citing rows written · 0 released rows left"
evidence-check --strict --ledger seal/ledger/2000000002-the-older-re-read.md .               -> exit 2, M DRIFTED (outranked)
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Regression tests to plant

- **🟡 1.** Plant the case in the first fence of 🟡 1 below into
  `tests/test_a_released_row_is_read_again_in_a_fragment.py`, after the
  enumeration. It was seen red at `a7ba069f` in all three modes and green
  with the fix.
- **⬜ 7.** Plant the case in ⬜ 7's fence into the same module. It passes
  at `a7ba069f` (executed, 2 passed), because it pins behaviour the code
  already has. So it has to be seen red by breaking the root naming in
  `reverify_into` before it is committed (agent contract §15).
- **⬜ 3.** The changed expectation in ⬜ 3's second fence was not run by this
  round.

## Facts for the evidence ledger

- **After 🟡 1's fix, N1's claim gains one clause:** *whichever members carry
  the coordinate, released or fragment only*. N1 and L4 then cite the new
  case and re-stamp `#released_drift`.
- **N1's 72 cells become 75**, or N1 names the extra case beside them.

## Paste-ready fixes

### 🟡 1 — the second loop grades a fragment-only coordinate, under a released root

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ def released_drift(ledgers, view_paths, root, maps, default_repo):
     owes: a released row of a released file in LEDGERS that sits outside
     every family and has a drifted coordinate, and the root of each family
     that is not superseded and has a member, released or fragment, in a file
     LEDGERS names, where no newest reading holds a coordinate's current
-    content and a released member's reading either drifted or is outranked
-    by a newer reading holding other content. The root is named even where
-    LEDGERS left its file out, because a `Re-read ·` row cites the root.
+    content and a member's reading -- a released member's where one carries
+    the coordinate, else any member's under a released root -- either
+    drifted or is outranked by a newer reading holding other content. The
+    root is named even where LEDGERS left its file out, because a
+    `Re-read ·` row cites the root.
@@
         for coord, graded in by_coord.items():
             if view.held[top][coord]:
                 continue
-            for key, m, status, detail in graded:
-                if ledger_kind(root, view.files[key[0]][0]) != "released":
-                    continue
-                if status == "BROKEN":
-                    broken.append((where(key), coord, detail))
-                    break
-                # DRIFTED, or OK and outranked by a newer reading holding
-                # other content: the family owes a re-read either way. That
-                # newer reading may sit in a fragment LEDGERS left out, which
-                # nothing re-stamped (round 2, 🟡 12).
-                drifted.setdefault(top, {}).setdefault(coord, m)
-                break
+            pick = next(
+                (
+                    g
+                    for g in graded
+                    if ledger_kind(root, view.files[g[0][0]][0]) == "released"
+                ),
+                None,
+            )
+            if pick is None:
+                # A coordinate only fragment members carry -- a re-read that
+                # added a unit its root does not cite -- is owed a re-read all
+                # the same: the fragment holding its newest reading may be one
+                # LEDGERS left out, which nothing re-stamped. Only where the
+                # root is released: a `Re-read ·` cites nothing else, and a
+                # family rooted in a fragment is re-stamped in place.
+                if ledger_kind(root, view.files[top[0]][0]) != "released":
+                    continue
+                pick = next((g for g in graded if g[2] != "BROKEN"), None)
+                if pick is None:
+                    continue
+            key, m, status, detail = pick
+            if status == "BROKEN":
+                broken.append((where(key), coord, detail))
+                continue
+            # DRIFTED, or OK and outranked by a newer reading holding other
+            # content: the family owes a re-read either way. That newer
+            # reading may sit in a fragment LEDGERS left out, which nothing
+            # re-stamped (round 2, 🟡 12).
+            drifted.setdefault(top, {}).setdefault(coord, m)
     return view, drifted, broken
```

```python
@pytest.mark.parametrize("mode", MODES)
def test_a_narrowed_reverify_answers_for_a_coordinate_only_fragments_carry(repo, mode):
    """The axis the 72 cells hold fixed: which members carry the coordinate.
    R cites `handler` alone; an older fragment re-read M adds `other` as it
    is, a newer re-read N in another fragment holds other content, and no
    released member carries `other`. A run narrowed to M's fragment exits 0
    only where `--strict` with the same narrowing does, and names or writes
    for the family's root otherwise."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    o1 = unit_hash(repo, "src/service.py", "other")
    (r,) = released(
        repo,
        [f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"],
    )
    cite = citation(r, "R1 · handler adds one")
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    o2 = unit_hash(repo, "src/service.py", "other")
    for name, h, date in (
        ("2000000002-the-older-re-read", o1, "2026-02-01"),
        ("3000000003-the-newer-re-read", o2, "2026-03-01"),
    ):
        fragment(
            repo,
            [
                f"| Re-read · R1 · handler adds one | `{cite}`, "
                f"`src/service.py#other@{h}` | read | {date} | Re-read {date} |"
            ],
            name=name,
        )
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    flags = ["--ledger", "seal/ledger/2000000002-the-older-re-read.md"]
    if mode != "no freeze":
        frozen(repo, "0")
    into = ["--into", MEMBER_INTO, "--checked", "2026-04-01"]
    fix = run(
        ["--reverify", *(into if mode == "freeze with --into" else []), *flags, "."],
        repo,
    )
    assert fix.returncode in (0, 1), fix.stdout + fix.stderr
    check = run(["--strict", *flags, "."], repo)
    if fix.returncode == 0:
        assert check.returncode == 0, fix.stdout + "\n---\n" + check.stdout
    if mode == "freeze with --into":
        assert "citing seal/releases/0.1.0.md:5" in fix.stdout, fix.stdout
        assert run(["--strict", "."], repo).returncode == 0
    else:
        assert fix.returncode == 1, fix.stdout
        assert "LEFT  seal/releases/0.1.0.md:5" in fix.stdout, fix.stdout
```

### ⬜ 2 — the home names every impossible date, not one

```diff
--- a/docs/the-evidence-ledger.md
+++ b/docs/the-evidence-ledger.md
@@
 when none did, and BROKEN by the rules above. A `Checked` date the calendar
-does not have, such as `2026-13-45`, orders nothing, and a reading dated only
-by one is named with that date as written, because fixing it is the repair.
+does not have, such as `2026-13-45`, orders nothing, and a reading dated only
+by such dates is named with each of them as written, because fixing them is
+the repair.
```

### ⬜ 3 — the plural reads as one list, and a repeat is named once

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ def family_view(paths, root, maps, default_repo=None, scan_cache=None):
-        typed = CHECKED_RE.findall(cells[column[0]]) if column else []
+        typed = list(
+            dict.fromkeys(CHECKED_RE.findall(cells[column[0]]) if column else [])
+        )
         if not typed:
             return "the reading of no date"
-        what = "a date" if len(typed) == 1 else "dates"
-        return (
-            f"the reading dated {', '.join(typed)}, {what} the calendar does not have"
-        )
+        if len(typed) == 1:
+            return f"the reading dated {typed[0]}, a date the calendar does not have"
+        listed = ", ".join(typed[:-1]) + f" and {typed[-1]}"
+        return f"the reading dated {listed}, dates the calendar does not have"
```

```diff
--- a/tests/test_a_released_row_is_read_again_in_a_fragment.py
+++ b/tests/test_a_released_row_is_read_again_in_a_fragment.py
@@
         (
             "2026-13-45, 2026-02-30",
-            "the reading dated 2026-13-45, 2026-02-30, dates the calendar does not have",
+            "the reading dated 2026-13-45 and 2026-02-30, dates the calendar does not have",
         ),
```

Phase 2 records the `, ` join as the smith's choice, and D5 states it for
its one-string example only. The overview's divergence table takes one row
for the `and`.

### ⬜ 4 — the docstring says what the code prints

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ def family_view(paths, root, maps, default_repo=None, scan_cache=None):
         """KEY's reading as the DRIFTED line names it: by its newest calendar
         date; else by every date-shaped string its `Checked` cell holds, in
-        cell order, said to be no date the calendar has, because fixing that
-        typo is the person's repair; else as the reading of no date (round
-        3, ⬜ 17). The ordering is `checked`'s, unchanged."""
+        cell order, said to be a date (or dates) the calendar does not have,
+        because fixing that typo is the person's repair; else as the reading
+        of no date (round 3, ⬜ 17). The ordering is `checked`'s, unchanged."""
```

### ⬜ 5 — N2 quotes the printed message

```
N2's claim, replacing its middle clause:

  … where its `Checked` cell holds only date-shaped strings the calendar does not have, by each of them in cell order, said to be a date (or dates) the calendar does not have; …
```

### ⬜ 6 — the two docstring sentences say only what is held

```diff
--- a/tests/test_a_released_row_is_read_again_in_a_fragment.py
+++ b/tests/test_a_released_row_is_read_again_in_a_fragment.py
@@ def test_a_narrowed_reverify_exits_0_only_where_the_narrowed_strict_does(
     narrowing that exits 0 too. Under the freeze no released byte moves, and
     with `--into`, wherever the narrowing holds a member, the whole tree then
-    checks clean. A run that read no member answers for nothing, and says
-    which files it skipped."""
+    checks clean."""
@@ def test_a_narrowing_to_a_superseded_root_answers_nothing(repo, mode):
     """The control outside the product: R is superseded by a `Corrected ·`
     row, so nothing in R's family is graded, and a run narrowed to R's file
-    owes nothing. Without the correction the same narrowing exits 1."""
+    owes nothing. Without the correction the same narrowing exits 1, or,
+    with `--into`, writes the row R's family owes."""
```

### ⬜ 7 — S3, the root and the `--into` repair under the freeze

```python
@pytest.mark.parametrize("member", ("release", "fragment"))
def test_a_frozen_reverify_narrowed_to_a_member_names_the_root_with_into(repo, member):
    """S3: under the freeze and without `--into`, a run narrowed to the file
    holding the older reading M names the family's root, not M, with the
    `--into` repair, and writes no released byte."""
    files = three_readings(repo, member, "fragment")
    frozen(repo, "0")
    before = digests(repo)
    out = run(["--reverify", "--ledger", files["M"], "."], repo)
    assert out.returncode == 1, out.stdout
    left = [line for line in out.stdout.splitlines() if "LEFT" in line]
    assert len(left) == 1, out.stdout
    assert left[0].split()[:2] == ["LEFT", "seal/releases/0.1.0.md:5"], left[0]
    assert "--reverify --into seal/ledger/<work-item-id>.md" in left[0], left[0]
    assert digests(repo) == before
```

### ⬜ 8 — the home's promise is scoped to what a re-read clears

```diff
--- a/docs/the-evidence-ledger.md
+++ b/docs/the-evidence-ledger.md
@@
 `--ledger` names, by its root row, each family that a file it read holds a
 member of, released or fragment, where no in-place re-stamp of the files it
 read clears that family, and exits 1. The root is named even where the
 narrowing left its file out, because the root is the row a `Re-read ·` cites.
+A row corrected by two rows is not a re-read's to clear: `--strict` names
+each correcting row, and `--reverify` leaves the choice of claim to a person.
```

### ⬜ 9 — spec D3 says why unnarrowed runs do not change

```
spec.md, D3, replacing its second sentence:

  Every released file is already in `wanted` there. A family rooted in a fragment — a `Corrected ·` row there, or a citing row whose citation resolves to nothing — holds no released member, because a citation into a fragment joins nothing, and `released_drift` grades a family's coordinate only from a member under a released root; so every family that can owe a re-read is already answered. A change that widens which members grade a coordinate keeps that guard on the root's kind.
```

Needs a fix: yes — 🟡 1, a coordinate only fragment members carry escapes a
narrowed `--reverify` in all three modes.
Loses a record or crashes: no

## Proof block

Files opened in the clone at `a7ba069f`, or by diff over `2b1dcb1f..a7ba069f`:

- `skills/evidence-check/scripts/evidence_check.py`: `family_view` whole,
  `released_drift`, `reverify_into`, `main`'s `--reverify` branch,
  `cited_row`, `ledger_kind`, `file_identity`, `built_name`, `CHECKED_RE`
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the helpers at
  lines 1–160 and 669–692, the double-correction case, and the whole #740
  block
- `docs/the-evidence-ledger.md`: the three hunks
- `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md`:
  the diff, all ten rows
- `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md`
- this work item's `spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `changelog.md`, and `phases/phase-1.md` to `phase-3.md`
- `skills/evidence-check/SKILL.md` §*Re-verifying is recomputing the hash*
- `bin/test`, and `bb2f3400`'s commit message and fragment diff

Every probe file and the clone were deleted before hand-over.

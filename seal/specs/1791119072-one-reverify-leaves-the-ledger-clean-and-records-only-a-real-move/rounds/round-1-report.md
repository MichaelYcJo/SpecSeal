# Round 1 report — one `--reverify` leaves the ledger clean and records only a real move

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | ef3bf06d |
| Base | `release/v0.18.2` at 94d7b2e0 |
| Pull request | #786 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

Reviewed in a `git clone --no-local` at the target, under the session
scratchpad's `<work-item-id>/round-1/`, removed at the end of the round. No
earlier `round-N.md` exists for this work item, so the account (`spec.md`,
`plan.md`, `overview.md`, `phases/phase-2.md`, `survivors.md`, the ledger
fragment) was the only voice besides the code. Every claim below that it
makes was opened against the code before it was used.

## Summary

Three findings need a fix, and all three are in the #772/#774 surface:

- **🟡 1.** One unfrozen run still leaves a citation DRIFTED in one legal
  shape: a released file that cites a row of itself. A second fold for the
  newest version joins its file (`docs/release-checklist.md`, the fold
  paragraph), so a `Re-read ·` row folded late can cite a row in its own
  release file. `cited_first` drops the self-edge, the file's own re-stamp is
  not in the plan while that file is walked, and `citations_left` skips every
  walked file. The run exits 0 and `--strict` exits 2. This also answers
  question 3: the `read_here` survivor is not equivalent, because this shape
  is the one it silences.
- **🟡 2.** The new pact-doc sentence says *a recorded move starts at the hash
  the coordinate's newest reading holds*. That holds for `--into` and its
  refusal, but not for the in-place writer, which still records from each
  row's own hash. I executed this.
- **🟡 3.** The new narrowed `LEFT` line says *this run re-stamps the line it
  cites*. It prints before the record step, so a run whose record fails
  prints it next to *nothing was re-stamped*. I executed this.

D1's choice of the newest reading matches what `--strict` uses. D3 drops no
code move. The `planned_key` survivor is equivalent. #775's sentences, pins
and both `Corrected ·` rows hold as written, apart from the one clause of
the 0.18.1:416 correction that finding 1 makes false.

## Stage 1 — spec compliance

### D1 (#774): the newest reading is `--strict`'s own, at all four arms — read

`newest_hash` (`evidence_check.py:3482`) reads `view.newest`. That is
`newest_by`, built in `family_view` at `evidence_check.py:2628`, and it is
the same structure `--strict`'s DRIFTED line names *the newest reading of
this coordinate* from. So no second ranking exists that could disagree with
the first. I enumerated the family shapes by construction from `family_view`:

| Shape | What `newest_hash` returns | Same as `--strict`? |
|---|---|---|
| Released row outside every family (`released_drift`'s first loop) | its own hash: the key is not in `view.newest`, and the BROKEN append there still uses `m.group("hash")` | yes, it is its own only reading |
| Family rooted at a released row, newest reading in a fragment or a later release | the first reading of the coordinate on the row `last[0]` names | yes, the same `last` |
| A tie on the newest date | the first member in `sorted(members, key=(str(identity), line))` that carries the date | yes, but see ⬜ 4 |
| A family a `Corrected ·` row supersedes | no readings: `released_drift` never selects it, so no move is appended | yes, `--strict` skips it too |
| A `Corrected ·` row as a root (`root_of` stops at a non-`Re-read` verb) | its own family's newest | yes |
| A newer member that does not carry the coordinate | ignored: `newest` is computed per coordinate, over the rows that carry it | yes |

All four arms read it: the written arm (`evidence_check.py:3823`), the
refusal arm (`:3776`), the `new is None` arm (`:3814`), and the BROKEN list
`released_drift` builds (`:3646`, keyed on `top`). The overview's divergence,
which moved the fourth arm into `released_drift`, is sound. The loop's `key`
there is the picked member, and only `top` keys `view.newest`. Its other
caller, `main`'s unfrozen arm, discards the list.

The D1 guard at `evidence_check.py:3996` is sound. A BROKEN part has
`new=None`, so the guard never drops one. `reverify` never produces
`old == new`, because it appends only where `got != hash`. So the guard is a
safety check, as the spec frames it.

### D2 (#772): the order, every citing shape — executed and read

| Shape | One unfrozen, unnarrowed run, then `--strict` |
|---|---|
| Fragment `Re-read ·` citing a release | 0. Pinned by the case for S4 |
| Release citing an older release (`0.10.0` → `0.9.0`) | 0. Pinned by the case for S5 |
| `Corrected ·` citing a release | 0 by the same edge (`row_citation` takes both verbs). Read, not executed |
| A chain, fragment → `Re-read` in a release → its root | 0. The order is transitive. Read |
| Fragment citing a fragment | `MALFORMED` either way. The edge only orders two fragments. Read |
| **Self-citation in one released file** | **2. Executed. This is 🟡 1** |
| A cycle across files | Cannot be written legally (a fold cites only older or same releases). The fallback keeps the given order. Read |

**Narrowed `--ledger`, `LEFT` and exit 1 — read and executed.**
`citations_left` compares each left-out citing row's citation before and
after the plan. That comparison is correct, and the case for S6 pins it. Its
print site has the W8 problem in 🟡 3.

### D3: a re-stamped citation is not a pact change — read

The skip at `evidence_check.py:3309-3316` matches the offset of the first
`Code grounds` anchor of a citing row, found on the line exactly as
`family_view` finds it, so the D3 skip and the family grading agree on which
anchor is the citation. A citing row's code coordinates sit at other offsets
and are still appended. A `Corrected ·` row's citation, a BROKEN citation
(`new=None`) and a citation into a fragment are all ledger lines, so dropping
them loses no code move. One edge, not a finding: a citing row whose first
`Code grounds` coordinate is code rather than a citation is `MALFORMED`
under `--strict` already, and its move is now skipped too.

### Question 3: the two survivors

- **`planned_key(target) not in held`: equivalent. Read.** Where the plan does
  not hold the target, `read` answers the disk for both loaders, so the two
  statuses are equal and the row is never DRIFTED now and OK before.
- **`file_identity(path) in read_here`: not equivalent. Executed.**
  `phases/phase-2.md:191` says a walked file *has its citations re-stamped by
  `cited_first`'s order*. That is false for a file that cites itself (🟡 1).
  With the guard removed, the self-citation tree prints a `LEFT` line and
  exits 1. With the guard, it exits 0 silently. The test suite has no case of
  this shape, which is why the mutation survived.

### #775: sentences, pins and the two `Corrected ·` rows — read

- `templates/config.md` §Pact points at the pact doc's first sentence, which
  is the bold trigger ending *that test is the whole trigger*. Holds.
- The section comment over `record_pact_changes` names the refused stale row.
  Holds.
- The usage (`evidence_check.py:77-78`) and the skill clause
  (`SKILL.md:328-330`) are pinned through
  `test_the_home_and_the_usage_say_a_stale_row_is_left`. The pact sentence is
  pinned through `test_the_documents_say_what_the_writer_does`.
- The `Enforced by:` line names the two #746 cases and the two #774 cases.
  `tests/test_a_folded_statement_names_what_enforces_it.py` passed (executed).
- The `Corrected ·` row over `seal/releases/0.18.0.md:79` holds against the
  code. `reverify_into` writes `Re-read <checked> by work item <item>` in the
  Notes (`:3835`). `reverify` splices only hash spans and `dated_cell` into the
  date cell (`:3249-3292`). The *Without the row* paragraph names *a dated
  note* (`docs/the-evidence-ledger.md:170`).
- The `Corrected ·` row over `seal/releases/0.18.1.md:416` holds except its
  clause *Without the freeze a changed citation is not among them: one run
  re-stamps it*. That clause is false for 🟡 1's shape. The same clause stands
  in `docs/the-evidence-ledger.md:199-201` and in E3 of the fragment. All
  three are fixed by 🟡 1's code fix, and none of them needs rewording if
  that fix lands.

## Findings

### 🟡 1 — A released file citing a row of itself still needs a second unfrozen run

`skills/evidence-check/scripts/evidence_check.py:3028` (`cited_first`), and
`:3538` (`citations_left`'s `read_here` skip).

**What is wrong.** `fold_ledger.py --version X.Y.Z` run a second time joins
the newest release's file. So a `Re-read ·` row written after the first fold,
citing a row of that release, folds into the same file it cites. That shape
is legal. `cited_first` deliberately drops the self-edge (`cited != n`).
`reverify` hashes a citation through `read`, but a file's own re-stamp only
enters the plan when its walk ends (`put` at `:3329`). So a citation of the
same file is hashed against the bytes on disk and is left at the old hash.
`citations_left` then skips every walked file, so nothing names it.

**Executed** at ef3bf06d, unfrozen: `0.1.0.md` holds R1 at `handler@h` and
a `Re-read ·` row citing R1 with `citation_for`'s literal. The code moved.
`--reverify --checked 2026-03-01 .` exited 0 with `2 rows re-verified`.
`--strict .` then exited 2: `DRIFTED … "R1 · handler adds one \|" the
released file changed under the row it cites`. A second run cleared it. With
`if file_identity(path) in read_here: continue` deleted, the same tree
printed `LEFT  seal/releases/0.1.0.md:6 …` and exited 1.

**Why it matters.** #772 is *one unfrozen run leaves `--strict` at 0*, and
this is a shape in which it does not. Three things now in the tree say the
opposite: the rewritten fifth item at `docs/the-evidence-ledger.md:199-201`,
E3 (*a self-citation ignored … `--strict` reads it clean*), and the new
`Corrected ·` row over 0.18.1:416. The spec's class table (§12) lists (i)–(iii)
and does not list this instance. The mutation report recorded the guard that
hides it as an equivalent shortcut.

**The fix.** `cited_first` walks a file that cites itself twice in a row, so
the second walk hashes its citations against the plan. The second walk names
nothing the first one named. The candidate was tried in the clone: the probe
tree then read `--strict` 0 after one run. The two touched modules and
`tests/test_evidence_check.py` passed 491 tests, and the one failure was the
order assertion of
`test_the_walk_order_survives_a_self_citation_and_a_cycle`, which this fix
changes on purpose. It covers one level of in-file citation. A chain inside
one file (a row citing a `Re-read ·` row of its own file) would need a pass
per level, and nothing I found can write that shape today.

### 🟡 2 — The pact doc's new sentence is false for the in-place writer

`docs/the-pact.md:126-130`.

**What is wrong.** The sentence says, unqualified, *A recorded move starts at
the hash the coordinate's newest reading holds*. Only `reverify_into` reads
`newest_hash`. `reverify`, the in-place writer that the same paragraph names
as *a re-stamp in place*, appends `(ledger, number, coord, old, new)` with
`old` taken from the row's own anchor (`evidence_check.py:3319`).

**Executed** at ef3bf06d with no freeze, a declared branch and the default
`Pact notify`. Released R1 cites the clause at `serialize@57f678c6`, read
2026-09-01. Another item's fragment re-reads R1 at `@7069baf7`, read
2026-09-02. The code then moved to `@b2c84dd7`. `--strict` exited 2 before
the run. One `--reverify --checked 2026-09-04` recorded
a row for `seal/releases/0.1.0.md · R1` whose `serialize` part moves from
`57f678c6` to `b2c84dd7`.
That move starts at the released row's hash, not at the newest reading's
`7069baf7`.

**Why it matters.** The paragraph is the trigger's home. A pact reviewer who
reads it will take R1's old hash as the content last read, and here it is
not. This branch did not change the in-place behaviour. That behaviour is in
#785's family-blind class and is out of scope. The finding is the new
sentence, which states otherwise. Either the sentence names the form it
holds for, or the in-place writer adopts the rule. The second option is
#785's frame, so the fix below narrows the sentence and pins the in-place
half.

### 🟡 3 — The narrowed `LEFT` line claims a re-stamp the run may not make

`skills/evidence-check/scripts/evidence_check.py:5359-5366`.

**What is wrong.** The line prints before `recorded_then_applied`. When the
record step refuses, it prints *this run re-stamps the line it cites* and,
below it, *so this run wrote no ledger file: nothing was re-stamped*. The
two lines contradict each other, and the first is false.

**Executed** at ef3bf06d with `unfrozen_r_and_m`, plus `Pact` and
`Pact notify | always`, no work item and no `--into`. Command:
`--reverify --checked 2026-03-01 --ledger seal/releases/0.1.0.md .`. The run
exited 1 and printed both lines. R's file was byte-identical afterwards, and
M's citation was not DRIFTED.

**Why it matters.** `docs/the-pact.md` §*A line saying the run wrote a ledger
file prints only once that file is written* (W8) exists for exactly this
case: *a run that writes none claims none*. Every other write-claiming line
waits in `told` for that reason. The exit stays 1 either way, so this is a
message defect and not a lost record. The same holds where the apply step
fails to write the cited file, since the line names a re-stamp that did not
land.

### ⬜ 4 — On a tie, the recorded old hash depends on inode order

`skills/evidence-check/scripts/evidence_check.py:2608, 2628`. Read only.
Members sort by `str(file_identity)`, which is `(st_dev, st_ino)`. On a tie
between two readings with different hashes, two checkouts can therefore
name different newest rows. `--strict` already names a row this way, so this
is not D1's departure. The difference is that the hash now lands in a
permanent record. That is harmless while the second run's `last` check holds
on one machine. Nothing needs a fix here. A path-based tiebreak
(`built_name`) would make the choice stable across checkouts.

### ⬜ 5 — The pact trigger does not say that a citation's re-stamp is excluded

`docs/the-pact.md:117-121`. Read only. The trigger says *moves the hash of a
ledger row* and *that test is the whole trigger*. After D3, a citing row
whose only moved hash is its citation is not recorded. The next sentence
(*code under a row moved*) carries the intent, so the behaviour and the fact
both hold. One clause, *(a citing row's citation is a ledger line and not
code under it)*, would make the trigger whole.

### ⬜ 6 — The equivalence grounds in phase 2 are wrong (paperwork, a correction)

`seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/phases/phase-2.md:191`.
The second survivor's grounds (*a file the run walked has its citations
re-stamped by `cited_first`'s order … No case builds that row*) miss the
self-citation shape (🟡 1). Correct the line when 🟡 1 is fixed. This is not
on the fix list.

## Regression tests to plant

- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the
  self-citation case in the fix for 🟡 1, which is red at ef3bf06d (executed,
  `--strict` 2). Also change the order assertion in
  `test_the_walk_order_survives_a_self_citation_and_a_cycle`.
- `tests/test_a_signatory_records_a_pact_change.py`: the in-place case in the
  fix for 🟡 2, which pins the in-place half of the narrowed sentence. Its
  assertion holds at ef3bf06d, because it pins current behaviour. Show it red
  (§15) by deleting the new sentence's pin parameter's words, or by switching
  `reverify`'s `old` to `newest_hash`.
- The case for S6, extended per 🟡 3: under a record that refuses, no
  `its citation of` line. That is red at ef3bf06d (executed).

## Facts for the evidence ledger

- E3's claim needs the self-citation case added to its coordinates once 🟡 1
  lands. Until then, its *a self-citation ignored … `--strict` reads it
  clean* is false at ef3bf06d (executed).
- E2's sentence coordinate moves with 🟡 2's rewording. Re-stamp it then.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A released file citing a row of itself (a second fold joins its file) keeps its citation DRIFTED after one unfrozen run, and `citations_left`'s walked-file skip names nothing | `skills/evidence-check/scripts/evidence_check.py:3028` | open | Executed: one run exit 0, `--strict` exit 2, second run clears; guard removed → `LEFT` and exit 1. Contradicts `docs/the-evidence-ledger.md:199-201`, E3, and the 0.18.1:416 `Corrected ·` row |
| 🟡 2 | The pact doc says every recorded move starts at the newest reading's hash; the in-place writer records from the row's own | `docs/the-pact.md:126` | open | Executed: unfrozen, R1 recorded `@57f678c6 → @b2c84dd7` while the newest reading held `7069baf7`; `reverify` appends the anchor's own hash at `evidence_check.py:3319` |
| 🟡 3 | The narrowed `LEFT` line says the run re-stamps the cited line before the record step, and prints beside "nothing was re-stamped" | `skills/evidence-check/scripts/evidence_check.py:5359` | open | Executed: record refused, both lines printed, R's file unchanged; W8 in `docs/the-pact.md` |
| ⬜ 4 | On a tie the newest reading, and so a recorded old hash, follows inode order | `skills/evidence-check/scripts/evidence_check.py:2608` | open | Read: same row `--strict` names; stable on one checkout |
| ⬜ 5 | The pact trigger does not state that a citation's re-stamp is excluded (D3) | `docs/the-pact.md:117` | open | Read: the next sentence's *code under a row* carries the intent |
| ⬜ 6 | phase 2's equivalence grounds for the `read_here` survivor miss the self-citation shape | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/phases/phase-2.md:191` | open | Paperwork: a correction, not on the fix list |
| 🟢 | D1 takes the newest reading `--strict` grades by, at all four arms, across every family shape | `skills/evidence-check/scripts/evidence_check.py:3482` | confirmed | Read: `newest_hash` reads `newest_by`, the same `last` the DRIFTED line names; superseded families yield no move |
| 🟢 | D3's skip drops only a citing row's citation offset, never a code coordinate | `skills/evidence-check/scripts/evidence_check.py:3309` | confirmed | Read: the offset is the first `Code grounds` anchor, matched as `family_view` matches it |
| 🟢 | The `planned_key` survivor is an equivalent shortcut | `skills/evidence-check/scripts/evidence_check.py:3549` | confirmed | Read: an unplanned target reads the same bytes in both loaders |
| 🟢 | #775's pointer, section comment, pins, `Enforced by:` targets and the 0.18.0:79 `Corrected ·` row hold against the code | `templates/config.md`, `docs/the-pact.md:146` | confirmed | Read; the folded-statement module executed and passed |

## Executed probes

| What was run | Result |
|---|---|
| Self-citation probe at ef3bf06d: `0.1.0.md` holds R1 and a `Re-read ·` row citing R1, no freeze, code moved; `--reverify --checked 2026-03-01 .`, then `--strict .`, then both again | first run exit 0 (`2 rows re-verified`); `--strict` exit 2, the citation DRIFTED; second run exit 0, `--strict` exit 0 |
| Same tree, a copy of the checker with `if file_identity(path) in read_here: continue` deleted | exit 1, `LEFT  seal/releases/0.1.0.md:6  Re-read · the first row — its citation of seal/releases/0.1.0.md:5 is DRIFTED …` |
| Same tree, the candidate fix in 🟡 1's block applied in the clone | one run exit 0 (`3 rows re-verified`), `--strict` exit 0 |
| Narrow modules with the candidate fix applied: the two touched modules and `tests/test_evidence_check.py` | 491 passed, 1 failed: the order assertion the fix changes on purpose |
| In-place probe at ef3bf06d: no freeze, declared branch, R1@`57f678c6` (2026-09-01), fragment re-read @`7069baf7` (2026-09-02), code at `b2c84dd7`; `--reverify --checked 2026-09-04 .` | exit 0; the record row's `serialize` part moves from `57f678c6` to `b2c84dd7` |
| Narrowed `LEFT` probe at ef3bf06d: `unfrozen_r_and_m` + `Pact` + `Pact notify \| always`, no work item; `--reverify --checked 2026-03-01 --ledger seal/releases/0.1.0.md .` | exit 1; printed the `its citation of … this run re-stamps the line it cites` line, then `nothing was re-stamped`; R's file byte-identical |
| `bin/test tests/test_a_folded_statement_names_what_enforces_it.py -q` at ef3bf06d (S10) | 29 passed |
| The full suite, the repository lint and the typecheck at this branch's head | not yet: the sealer's, after the rounds settle |

Every probe file, the mutated checker copy and the clone, including its
runner-built `.venv`, were deleted before handover.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The in-place writer records a move from an outranked row's own hash (the behaviour behind 🟡 2) | #785, the family-blind in-place walk, already filed | the orchestrator, who files #785's frame |

## Paste-ready fixes

### 🟡 1 — walk a file that cites itself twice

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ def cited_first(ledgers, root, maps, default_repo):
     index = {file_identity(path): n for n, path in enumerate(ledgers)}
     needs = [set() for _ in ledgers]
+    # A file citing a row of itself -- a second fold joins the newest
+    # release's file -- is walked twice in a row: its own re-stamp is in the
+    # plan only once its first walk ends, so the second hashes its citations
+    # against it.
+    again = set()
     for n, path in enumerate(ledgers):
         text = read(path)
@@
             target, _ = citation_target(root, maps, default_repo, cite.group("path"))
             cited = index.get(file_identity(target)) if target else None
-            if cited is not None and cited != n:
+            if cited == n:
+                again.add(n)
+            elif cited is not None:
                 needs[n].add(cited)
     order, done = [], set()
@@
         done.add(ready)
         order.append(ready)
-    return [ledgers[n] for n in order]
+    return [ledgers[n] for n in order for _ in range(2 if n in again else 1)]
@@ def reverify(
     written = []
     scan_cache = {}
+    walked = set()
     for ledger in cited_first(ledgers, root, maps, default_repo):
+        # The second walk of a file citing itself (`cited_first`) re-stamps
+        # its citations alone, and names nothing the first walk named.
+        again = planned_key(ledger) in walked
+        walked.add(planned_key(ledger))
         text = read(ledger, strict=True)
         if text is None:
             # `/` on every platform, as every path the writer prints.
-            unreadable.append(built_name(ledger, root))
+            if not again:
+                unreadable.append(built_name(ledger, root))
             continue
+        if again:
+            text_malformed, text_overflow = [], []
+        else:
+            text_malformed, text_overflow = malformed_rows(text), overflow_rows(text)
@@
-        malformed.extend((coord, why) for _, coord, why in malformed_rows(text))
+        malformed.extend((coord, why) for _, coord, why in text_malformed)
@@
         overflow.extend(
             (f"{built_name(ledger, root)} {coord}", why)
-            for _, coord, why in overflow_rows(text)
+            for _, coord, why in text_overflow
         )
@@
             if checked is not None:
                 if column is None:
-                    undatable.append(where)
+                    if where not in undatable:
+                        undatable.append(where)
                     left_whole.add(number)
                     continue
@@     def report(landed):
             if landed_at(landed, ledger):
                 lines.extend(said_here)
-                dated.extend(dated_here)
-                undated.extend(undated_here)
+                # A file citing itself is walked twice (`cited_first`), and a
+                # row both walks date is listed once.
+                dated.extend(d for d in dated_here if d not in dated)
+                undated.extend(u for u in undated_here if u not in undated)
```

```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
# In test_the_walk_order_survives_a_self_citation_and_a_cycle, 0.1.0.md cites
# itself and is now walked twice in a row:
    assert order == [paths[1], paths[1], paths[0], paths[2], paths[3]], order


def test_one_unfrozen_run_restamps_a_citation_of_its_own_file(repo):
    """#772, a file citing itself. A second fold for the newest version joins
    its file, so 0.1.0.md holds R1 and a `Re-read ·` row citing R1. One run
    re-stamps R1 and then the citation, and `--strict` exits 0. Red at
    ef3bf06d: `--strict` exits 2 until a second run."""
    h = unit_hash(repo, "src/service.py", "handler")
    r = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
    m = (
        f"| Re-read · the first row | `{citation(r, 'R1 · handler adds one')}`, "
        f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
    )
    released(repo, [r, m])
    cite = ec.citation_for(str(repo), str(repo / R_FILE), 5)
    m = m.replace(citation(r, "R1 · handler adds one"), cite)
    released(repo, [r, m])
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    check = run(["--strict", "."], repo)
    assert check.returncode == 0, check.stdout
```

### 🟡 2 — say which writer the newest-reading rule binds, and pin the in-place half

```diff
--- a/docs/the-pact.md
+++ b/docs/the-pact.md
@@
-re-read reaches (#746). **A recorded move starts at the hash the
-coordinate's newest reading holds**, which under the freeze can be a later
-`Re-read ·` row's rather than the released row's, so code that went back to
-the released hash records the move back; a move whose two hashes agree is no
-move and is not recorded (#774). `Pact
+re-read reaches (#746). **A move `--into` records starts at the hash the
+coordinate's newest reading holds**, whether it writes the `Re-read ·` row or
+refuses it, and that can be a later `Re-read ·` row's rather than the
+released row's, so code that went back to the released hash records the move
+back. A re-stamp in place records each row's move from that row's own hash.
+A move whose two hashes agree is no move and is not recorded (#774). `Pact
```

```python
# tests/test_a_signatory_records_a_pact_change.py
# The pin parameter in test_the_documents_say_what_the_writer_does becomes:
        (
            "docs/the-pact.md",
            "**A move `--into` records starts at the hash the coordinate's newest "
            "reading holds**, whether it writes the `Re-read ·` row or refuses it",
        ),
        (
            "docs/the-pact.md",
            "A re-stamp in place records each row's move from that row's own hash.",
        ),


def test_an_in_place_move_starts_at_the_rows_own_hash(repo):
    """#774's other writer. No freeze: released R1 read at `h0`, another item's
    fragment re-reading it at `h1`, and the code then at `h2`. The in-place
    re-stamp records R1's move from R1's own hash, `h0 → h2`, as the pact doc
    says; the newest-reading rule is `--into`'s."""
    git(repo, "init", "-q", "-b", "feat/x")
    (repo / "seal" / "specs" / ITEM).mkdir(parents=True)
    (repo / "seal" / "specs" / ITEM / "routing.md").write_text(
        "| Axis | Answer |\n|---|---|\n| Review | straight to the PR |\n"
        "| Destination | open the pull request |\n| Branch | feat/x |\n",
        encoding="utf-8",
    )
    h0 = unit_hash(repo, "src/orders.py", "serialize")
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + row("R1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{h0}"),
        encoding="utf-8",
    )
    h1 = move_serialize(repo)
    citation = ec.citation_for(str(repo), str(released), 5)
    (repo / OTHER_ITEM).parent.mkdir(parents=True, exist_ok=True)
    (repo / OTHER_ITEM).write_text(
        f"| Re-read · R1 · the field list | `{citation}`, "
        f"`src/orders.py#serialize@{h1}` | read | 2026-09-02 | Re-read 2026-09-02 |\n",
        encoding="utf-8",
    )
    git(repo, "add", "-A")
    git(repo, "-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "x")
    (repo / "src" / "orders.py").write_text(
        SOURCE.replace("'id': order.id", "'id': order.id, 'n': 1"), encoding="utf-8"
    )
    h2 = unit_hash(repo, "src/orders.py", "serialize")
    code, out = run(repo, "--checked", "2026-09-04")
    assert code == 0, out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/releases/0.1.0.md · R1 | "
        f"`src/orders.py#serialize@{h0}` → `@{h2}` | 2026-09-04 |"
    ], out
```

### 🟡 3 — the narrowed `LEFT` waits for the write it names

```diff
--- a/skills/evidence-check/scripts/evidence_check.py
+++ b/skills/evidence-check/scripts/evidence_check.py
@@ def citations_left(ledgers, view_paths, root, maps, default_repo):
-    """`[(where, label, cited)]` for each citing row in a file of VIEW_PATHS
+    """`[(where, label, cited, target)]` for each citing row in a file of VIEW_PATHS
@@
             if was == "OK":
                 found.append(
                     (
                         f"{built_name(path, root)}:{number}",
                         row_label(cells),
                         f"{built_name(target, root)}:{at[1]}",
+                        target,
                     )
                 )
@@ def main():
                 # A citation of a line this run re-stamped, in a file the
                 # narrowing left out, is left DRIFTED: named, never silent
-                # (#772). Read before the plan is applied, against it.
+                # (#772). Read before the plan is applied, against it, and
+                # said only once the cited file's re-stamp landed: a run that
+                # writes nothing claims nothing (W8).
                 left = citations_left(ledgers, view, root, maps, default_repo)
-                for where, label, cited in left:
-                    print(
-                        f"  LEFT  {where}  {label} — its citation of {cited} is "
-                        "DRIFTED: this run re-stamps the line it cites, and the "
-                        "narrowing left this row's file out; run it without "
-                        "`--ledger`"
-                    )
+
+                def left_cited(landed):
+                    return [
+                        f"  LEFT  {where}  {label} — its citation of {cited} is "
+                        "DRIFTED: this run re-stamps the line it cites, and the "
+                        "narrowing left this row's file out; run it without "
+                        "`--ledger`"
+                        for where, label, cited, target in left
+                        if landed_at(landed, target)
+                    ]
+
+                told.append(left_cited)
                 return recorded_then_applied(max(code, 1 if owed or left else 0))
```

```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_a_narrowed_run_that_records_nothing_names_no_citation_it_moved(repo):
    """S6 under a record that refuses (W8): `Pact notify | always` and no work
    item, so nothing is written, R's line does not move, and no line says the
    run re-stamps it. Red at ef3bf06d, which printed the line beside
    `nothing was re-stamped`."""
    unfrozen_r_and_m(repo)
    (repo / "seal" / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Mode | shared |\n"
        "| Pact | git@example.com:org/orders-api.git |\n| Pact notify | always |\n",
        encoding="utf-8",
    )
    fix = run(["--reverify", "--checked", "2026-03-01", "--ledger", R_FILE, "."], repo)
    assert fix.returncode == 1, fix.stdout
    assert "nothing was re-stamped" in fix.stdout, fix.stdout
    assert "its citation of" not in fix.stdout, fix.stdout
```

Needs a fix: yes — 🟡 1 (a self-citing release file keeps its citation DRIFTED after one unfrozen run), 🟡 2 (the pact doc's newest-reading sentence is false for the in-place writer), 🟡 3 (the narrowed `LEFT` line claims a re-stamp before the record step)
Loses a record or crashes: no

## Proof block

Files opened at ef3bf06d: `skills/evidence-check/scripts/evidence_check.py`
(`read`/`put`/`apply_plan`/`told_now`/`landed_at`, `file_identity`,
`citing_verb` through `family_view`, `checked_refusal` through `dated_cell`,
`row_citation`, `cited_first`, `reverify`, `newest_hash`, `citations_left`,
`released_drift`, `later_reading`, `reverify_into`, `record_pact_changes`,
`main`'s `--reverify` arm, the usage at lines 70-82),
`docs/the-pact.md` §A signatory records a pact change and the W8 paragraph,
`docs/the-evidence-ledger.md` lines 160-205, `docs/release-checklist.md`
lines 95-135, `docs/the-record-layout.md` (ledger rows), `templates/config.md`
(diff), `skills/evidence-check/SKILL.md` lines 320-335 and §Re-verifying,
`seal/releases/0.18.0.md:79`, `seal/releases/0.18.1.md:416`, the fragment
`seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md`,
the work item's `spec.md`, `overview.md`, `survivors.md`, `phases/phase-2.md`,
and the diffs of `tests/test_a_released_row_is_read_again_in_a_fragment.py`
and `tests/test_a_signatory_records_a_pact_change.py` with their helper
sections.

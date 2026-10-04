# 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move — review round 1

| Field | Value |
|---|---|
| Target SHA | ef3bf06d189a9c8b43279113873792dae381e77c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #786 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `007364767d61e41f0a88a1e3d974d4f2ace10477..6ded9bdddc41fddba1145700e51a93323b458dfd`, 4 commits |
| Contract changes | cited_first → round-1-report.md, round-1.md, reverify, pytest; test_a_narrowed_unfrozen_run_names_the_citation_it_moved_and_left → pytest only |
| New units | LEAVINGS (depth 1); test_one_unfrozen_run_restamps_a_citation_no_order_places (depth 1); test_an_in_place_move_starts_at_the_rows_own_hash (depth 1) |
| Needs a fix | yes — 🟡 1 (a self-citing release file keeps its citation DRIFTED after one unfrozen run), 🟡 2 (the pact doc's newest-reading sentence is false for the in-place writer), 🟡 3 (the narrowed `LEFT` line claims a re-stamp before the record step) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #774/#772/#775 (PR #786), at ef3bf06d against `release/v0.18.2` (94d7b2e0): spec compliance first (D1–D7, S1–S11), then quality. Judge whether a recorded move's old hash is the newest reading's as `--strict` chooses it, at every arm of `reverify_into` and the BROKEN list; whether `cited_first` leaves one unfrozen run clean for every citing shape, and the narrowed run's `LEFT` path; whether D3 drops a real change; whether the two surviving mutations are equivalent; and #775's sentences, pins and two `Corrected ·` rows against the code.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A released file citing a row of itself (a second fold joins its file) keeps its citation DRIFTED after one unfrozen run, and `citations_left`'s walked-file skip names nothing | `skills/evidence-check/scripts/evidence_check.py:3028` | **fixed** `15fab40e` | fixed at 15fab40e — 42ec98a7, cf503cd4, 6ded9bdd — `cited_first` keeps the self-edge, so a file citing itself, files citing each other, and every file citing one of them are left unplaced, and `reverify` walks them again until a walk changes nothing it plans, at most two more times than the citations among them; a repeated walk names nothing the first named. The cross-file cycle had the same hole (the fallback walked it once in the given order) and is closed by the same walk; red at ef3bf06d for both shapes. `docs/the-evidence-ledger.md`'s fifth item gained one sentence for the self-citing file, pinned; E3 and the `Corrected ·` row over 0.18.1:416 hold again and cite the new case. The `read_here` short-circuit is now equivalent: a walked file's citations settle, and a row `--checked` leaves whole is named `undatable` already (mutation re-run, survived); Executed: one run exit 0, `--strict` exit 2, second run clears; guard removed → `LEFT` and exit 1. Contradicts `docs/the-evidence-ledger.md:199-201`, E3, and the 0.18.1:416 `Corrected ·` row |
| 🟡 2 | The pact doc says every recorded move starts at the newest reading's hash; the in-place writer records from the row's own | `docs/the-pact.md:126` | **fixed** `15fab40e` | fixed at 15fab40e — the pact sentence now says a move `--into` records starts at the newest reading, written or refused, and a re-stamp in place records from the row's own hash; both halves pinned. `test_an_in_place_move_starts_at_the_rows_own_hash` pins the in-place behaviour unchanged (red under a mutation of `reverify`'s old hash). E1 and E2 say the same; Executed: unfrozen, R1 recorded `@57f678c6 → @b2c84dd7` while the newest reading held `7069baf7`; `reverify` appends the anchor's own hash at `evidence_check.py:3319` |
| 🟡 3 | The narrowed `LEFT` line says the run re-stamps the cited line before the record step, and prints beside "nothing was re-stamped" | `skills/evidence-check/scripts/evidence_check.py:5359` | **fixed** `15fab40e` | fixed at 15fab40e — 42ec98a7 — the narrowed `LEFT` line waits in `told` and prints only where the cited file landed; S6 gained a refused-record row (red at ef3bf06d) and a failed-write row (the landed filter red under mutation); Executed: record refused, both lines printed, R's file unchanged; W8 in `docs/the-pact.md` |
| ⬜ 4 | On a tie the newest reading, and so a recorded old hash, follows inode order | `skills/evidence-check/scripts/evidence_check.py:2608` | answered | The tie order is the one `--strict` names its newest reading by (`family_view`'s `newest_by`), so the writer records the old hash of the reading the checker grades against; writer and checker agree, and on one checkout a second run finds the same move the record's last word; Read: same row `--strict` names; stable on one checkout |
| ⬜ 5 | The pact trigger does not state that a citation's re-stamp is excluded (D3) | `docs/the-pact.md:117` | **fixed** `15fab40e` | fixed at 15fab40e — `docs/the-pact.md` adds, right after the bold trigger, that its hash is a code coordinate's and a citing row's citation re-stamp records nothing (#772); pinned; Read: the next sentence's *code under a row* carries the intent |
| ⬜ 6 | phase 2's equivalence grounds for the `read_here` survivor miss the self-citation shape | `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/phases/phase-2.md:191` | answered | A phase record is a record of its moment, so `phases/phase-2.md` is left as written; the round-1 report holds the correction, and row 1 above states that the `read_here` short-circuit is equivalent only after the fix; Paperwork: a correction, not on the fix list |
| 🟢 | D1 takes the newest reading `--strict` grades by, at all four arms, across every family shape | `skills/evidence-check/scripts/evidence_check.py:3482` | confirmed | Read: `newest_hash` reads `newest_by`, the same `last` the DRIFTED line names; superseded families yield no move |
| 🟢 | D3's skip drops only a citing row's citation offset, never a code coordinate | `skills/evidence-check/scripts/evidence_check.py:3309` | confirmed | Read: the offset is the first `Code grounds` anchor, matched as `family_view` matches it |
| 🟢 | The `planned_key` survivor is an equivalent shortcut | `skills/evidence-check/scripts/evidence_check.py:3549` | confirmed | Read: an unplanned target reads the same bytes in both loaders |
| 🟢 | #775's pointer, section comment, pins, `Enforced by:` targets and the 0.18.0:79 `Corrected ·` row hold against the code | `templates/config.md`, `docs/the-pact.md:146` | confirmed | Read; the folded-statement module executed and passed |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The in-place writer records a move from an outranked row's own hash (the behaviour behind 🟡 2) | #785, the family-blind in-place walk, already filed | the orchestrator, who files #785's frame |

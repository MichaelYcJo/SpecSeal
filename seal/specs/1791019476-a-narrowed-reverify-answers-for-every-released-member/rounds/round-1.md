# 1791019476-a-narrowed-reverify-answers-for-every-released-member — review round 1

| Field | Value |
|---|---|
| Target SHA | a7ba069f2bcb19d8987696184df3abbb7bb1854d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 743 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `465adf3325b0ac6070ddc80484d8068ba1f25da6..604f8969f9aad34099706c59541415a0c9787082`, 10 commits |
| Contract changes | three_readings → round-1-report.md, round-1.md, pytest; test_a_narrowed_reverify_exits_0_only_where_the_narrowed_strict_does → round-1-report.md, round-1.md |
| New units | test_a_narrowed_reverify_answers_for_a_coordinate_only_fragments_carry (depth 1); test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read (depth 1); test_a_frozen_reverify_narrowed_to_a_member_names_the_root_with_into (depth 1) |
| Needs a fix | yes — 🟡 1, a coordinate only fragment members carry escapes a narrowed `--reverify` in all three modes. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 targets `a7ba069f`, over the build's diff `2b1dcb1f..a7ba069f`. It was asked to check #740 against `spec.md` D1–D5 and S1–S9 and the approved plan, then quality. Five things were named for close checking:
- whether the 72-cell enumeration's axes are the whole class;
- whether D3's root claim, reported false as written, matters;
- ⬜ 17's wording and its plural;
- the ledger: L4 corrected in place, N1 and N2, and ten re-stamped rows of #736's fragment;
- the encoding and path-separator rules.
The 9 rows the integration chore #742 re-stamps were named as expected, to be confirmed by merging it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A coordinate carried only by fragment members escapes a narrowed `--reverify`. Narrowed to the fragment holding the older reading, with the newest in another fragment, the run exits 0 and writes nothing in all three modes, while the narrowed `--strict` exits 2. The home's two new sentences, L4, N1's first clause and the changelog entry are false there | `skills/evidence-check/scripts/evidence_check.py:3292` | **fixed** `27b6991e` | fixed at 27b6991e; Executed. Red at `a7ba069f` in 3 of 3 modes and at `2b1dcb1f` for both placements of N. Green in 3 of 3 with the paste-ready fix, which keeps 154 cases of the module and two siblings passing |
| ⬜ 2 | The home says a reading dated only by one impossible date is named with that date; the code names every date-shaped string, and the case pins two | `docs/the-evidence-ledger.md:103` | **fixed** `5c8baa17` | fixed at 5c8baa17; Read against `evidence_check.py:2501-2508` and the case's second cell |
| ⬜ 3 | The plural message joins the dates with `, ` and then adds `, dates …`, which reads as three items; a repeated string is named twice | `skills/evidence-check/scripts/evidence_check.py:2505` | **fixed** `bf9d833a` | fixed at bf9d833a; Read. Phase 2 records that the plural form was the smith's choice, so D5 did not decide it |
| ⬜ 4 | The `reading` docstring describes the message with Q2(a)'s rejected wording, *no date the calendar has* | `skills/evidence-check/scripts/evidence_check.py:2495` | **fixed** `14a56599` | fixed at 14a56599; Read against the f-string four lines below it |
| ⬜ 5 | N2 quotes the message as *said to be no date the calendar has*, the rejected wording, not the text the code prints | `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md:2` | answered | corrected at `da825ff1`; Read. This is a correction to the run's records |
| ⬜ 6 | The control's docstring says the uncorrected narrowing exits 1, which is false under `freeze with --into`; the enumeration's docstring promises a skipped-files notice nothing asserts | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1489` | **fixed** `e17069fa` | fixed at e17069fa; Executed: the uncorrected narrowing exits 1, 1 and 0 across the three modes |
| ⬜ 7 | S3's root naming under the freeze without `--into` is not pinned; the enumeration accepts any exit-1 output | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1445` | **fixed** `bf27f5f5` | fixed at bf27f5f5; Read. The code names the root today (executed, CONTROL), and nothing holds it |
| ⬜ 8 | A double correction is DRIFTED under `--strict` and named by no `--reverify`, narrowed or not, while the rewritten home sentence promises every family no re-stamp clears | `docs/the-evidence-ledger.md:163` | **fixed** `9c93f814` | fixed at 9c93f814; Executed (P5): `--reverify` exits 0 and `--strict` exits 2, narrowed and unnarrowed. The behaviour comes from #736; the sentence is this item's |
| ⬜ 9 | Spec D3's premise, *every family's root is released*, is false; the conclusion holds only through the released-member filter, which 🟡 1's fix has to widen | `seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/spec.md:72` | answered | corrected at `b0a41a09`; Read: `root_of` and `cited_row`. This is a correction to the run's records |
| 🟢 | The integration claim: with #742 merged and the two hunks resolved by hash, `--strict .` reads 0 drifted | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Executed: 4,026 ok and 0 drifted after the merge; 4,017 ok and 9 drifted at `a7ba069f` |
| 🟢 | S8's second half: no released ledger file changed | `seal/releases`, `seal/ledger.md` | confirmed | Executed: the name-only diff is empty |
| 🟢 | The ten re-stamped rows of #736's fragment hold against the edit, except L4's narrowing clause, which is 🟡 1 | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Read, row by row; table above |
| 🟢 | The grid holds for four-file families, for `seal/ledger.md` in either placement, and for a family rooted at a folded `Corrected ·` row | `skills/evidence-check/scripts/evidence_check.py:3286` | confirmed | Executed, P2–P4, 24 runs, no violation |
| ❓ | The Windows leg: the separator handling of the new cases | `tests/test_a_released_row_is_read_again_in_a_fragment.py` | ❓ out of verified scope | Read only: `built_name` and `ledger_section` normalise. The pull request's Windows CI leg answers it |

## Paste-ready fixes

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
```
N2's claim, replacing its middle clause:

  … where its `Checked` cell holds only date-shaped strings the calendar does not have, by each of them in cell order, said to be a date (or dates) the calendar does not have; …
```
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
```
spec.md, D3, replacing its second sentence:

  Every released file is already in `wanted` there. A family rooted in a fragment — a `Corrected ·` row there, or a citing row whose citation resolves to nothing — holds no released member, because a citation into a fragment joins nothing, and `released_drift` grades a family's coordinate only from a member under a released root; so every family that can owe a re-read is already answered. A change that widens which members grade a coordinate keeps that guard on the root's kind.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

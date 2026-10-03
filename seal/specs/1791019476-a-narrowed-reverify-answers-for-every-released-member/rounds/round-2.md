# 1791019476-a-narrowed-reverify-answers-for-every-released-member — review round 2

| Field | Value |
|---|---|
| Target SHA | 2e595b8e61ed0786637685a3e58c85486b55a41a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 743 |
| Broad gate | a96d98a6 against 9511f6cd |
| Fixes checked by | no fixes to check |
| Fix range | `c715c475a71db94f7e4124334512765997412a3e..c715c475a71db94f7e4124334512765997412a3e`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round. It targets `2e595b8e` over round 1's fix range `465adf33..604f8969`, the release merge `5e7e75de` (#742 only) and the close commit. It was asked:
- whether each of round 1's fixes holds;
- whether the units the fix pass created are correct: the released-root guard, the grid's new axis, the fragment-root case, ⬜ 3's join-and-dedupe, ⬜ 6's pinned notice, ⬜ 7's two-carrier case;
- whether any configuration outside the 144 cells lets a narrowed `--reverify` exit 0 while the narrowed `--strict` does not;
- whether the merge lost anything;
- whether the re-stamped and corrected ledger rows hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — a coordinate only fragment re-reads carry is now graded under a released root, and the narrowed run names or writes for the root in all three modes | `skills/evidence-check/scripts/evidence_check.py:3298` | confirmed | Executed: HEAD's new cases against `465adf33`'s checker fail 7 grid cells, the round's case in 3 modes and 1 S3 cell; all pass at HEAD, 236 cases with the two siblings; probes P1, P2a and P3 red before and green after |
| 🟢 | round 1's finding 2 is closed — the home names every impossible date | `docs/the-evidence-ledger.md:103` | confirmed | Read against `reading` |
| 🟢 | round 1's finding 3 is closed — one list joined with "and", each string once | `skills/evidence-check/scripts/evidence_check.py:2505` | confirmed | Executed: the three-date and repeated-date cells red at `465adf33`, green at HEAD |
| 🟢 | round 1's finding 4 is closed — the docstring says what the code prints | `skills/evidence-check/scripts/evidence_check.py:2492` | confirmed | Read |
| 🟢 | round 1's finding 5 — N2 quotes the printed message | `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md:2` | answered | Read; hashes current under `--strict` |
| 🟢 | round 1's finding 6 is closed — the notice is pinned and the control's docstring is true | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1598` | confirmed | Executed: at least 12 grid cells red with the notice's wording broken |
| 🟢 | round 1's finding 7 is closed — S3's root naming is pinned over both carriers | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1631` | confirmed | Executed: both re-reads-only cells red with the entry keyed on the picked member |
| 🟢 | round 1's finding 8 is closed — the home states the double correction's exit codes | `docs/the-evidence-ledger.md:171` | confirmed | Executed, P8: `--strict` 2, `--reverify` 0, narrowed and not, 3 modes; the class is ⬜ 11 |
| 🟢 | round 1's finding 9 — D3 says why a fragment-rooted family adds nothing | `seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/spec.md:72` | answered | Read; the headline is ⬜ 10 |
| 🟢 | the released-root guard holds and its case is a real pin | `skills/evidence-check/scripts/evidence_check.py:3314` | confirmed | Executed: red with the guard deleted, green restored |
| 🟢 | the merge lost no correction and kept every moved hash | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Executed: `correction-check` none dropped; 20 anchors compared, none moved on both sides; `--strict .` 4,029 ok, 0 drifted, 0 refused |
| 🟢 | the five rows `604f8969` re-stamped hold against the edit | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Read row by row; table above |
| 🟢 | the class round 1 opened is closed outside the 144 cells | `skills/evidence-check/scripts/evidence_check.py:3292` | confirmed | Executed: 105 runs, P1–P4 hold in every cell; the remaining disagreements are ⬜ 11 and ⬜ 12, and behave the same at `465adf33` |
| ⬜ 10 | A run without `--ledger` now exits 1 and names the released root where a coordinate only fragment re-reads carry has lost its anchored statement; it exited 0 before. N1, the changelog fragment and spec D3 say unnarrowed runs behave as before | `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md:1` | answered | corrected at `c715c475`; Executed, P7: exit 0 in 3 modes at `465adf33`, exit 1 at HEAD; the paste-ready case is red at `465adf33` and green at HEAD. A correction to the run's records |
| ⬜ 11 | The home's narrowed-run promise names one family no re-read can clear, the double correction; a BROKEN anchor and a statement gone from a fragment-rooted family also exit 0 against `--strict` 2 | `docs/the-evidence-ledger.md:171` | deferred #746 | #746 — Predates #740: the home names one family no re-read can clear, and the reviewer executed two more; filed with the report wording; Executed, P6, P10, P11: the same at HEAD and `465adf33`; the sentence is this item's |
| ⬜ 12 | `--into` with a `--checked` date older than the family's newest reading writes a row that does not outrank it and exits 0, while `--strict` still exits 2 | `skills/evidence-check/scripts/evidence_check.py:3348` | deferred #746 | #746 — Predates #740: #736 `--into` writes a row a stale `--checked` date cannot count; filed beside ⬜ 11; Executed, P5: both carriers, at HEAD and `465adf33`. #736's behaviour, not this item's class; its home is the orchestrator's call |
| ❓ | The Windows leg: the separator handling of the cases the fix pass added | `tests/test_a_released_row_is_read_again_in_a_fragment.py` | ❓ out of verified scope | Read only: the new cases compare printed names, which `built_name` writes with `/`. The pull request's Windows CI leg answers it |

## Paste-ready fixes

```python
@pytest.mark.parametrize("mode", MODES)
def test_an_unnarrowed_reverify_names_a_root_whose_fragment_only_statement_is_gone(
    repo, mode
):
    """Round 2, finding 10: a coordinate only a fragment re-read carries, whose
    anchored statement is gone, is one no in-place re-stamp clears. A run
    without `--ledger` names the family's released root and exits 1, as it
    does where a released row carries the coordinate."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    text = (repo / "src" / "service.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/service.py", "other", text)
    (inside,) = ec.minor_region("src/service.py", text, places[0], '"x * 2"')
    stated = ec.content_hash(ec.gfm_lines(text)[inside[0] - 1 : inside[1]])
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f'`src/service.py#other>"x * 2"@{stated}` | read | 2026-02-01 | '
            "Re-read 2026-02-01 |"
        ],
        name="2000000002-the-older-re-read",
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    if mode != "no freeze":
        frozen(repo, "0")
    into = ["--into", MEMBER_INTO, "--checked", "2026-04-01"]
    out = run(
        ["--reverify", *(into if mode == "freeze with --into" else []), "."], repo
    )
    assert out.returncode == 1, out.stdout
    assert "LEFT  seal/releases/0.1.0.md:5" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 2
```
```diff
--- a/seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/changelog.md
+++ b/seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/changelog.md
@@
   names it with the `--into` form. That holds whichever rows carry the
-  drifted coordinate, including one only fragment re-reads record. A
-  narrowing to a file that holds no member of the family, and a run without
-  `--ledger`, behave as before.
+  drifted coordinate, including one only fragment re-reads record. A
+  narrowing to a file that holds no member of the family behaves as before,
+  and so does a run without `--ledger`, with one exception: where a
+  coordinate only fragment re-reads record has lost the statement its anchor
+  names, the run now names the family's first row and exits 1, as it
+  already did where a released row recorded that coordinate.
```
```
N1's claim, replacing "a narrowing to a file holding no member, and a run without `--ledger`, answer as before":

  a narrowing to a file holding no member answers as before, and so does a run without `--ledger` except where a coordinate only fragment re-reads carry has lost its anchored statement, which it now names by the released root and exits 1 for, as it did where a released row carried it

N1's Notes, appended:

  **Corrected <date> by round 2's fix pass (⬜ 10):** the fragment-only branch reaches a run without `--ledger` where no re-stamp clears the coordinate; red at 465adf33 in all three modes.

spec.md, D3, appended after the paragraph:

  *Corrected <date> by round 2's fix pass (⬜ 10): one unnarrowed run does change. A coordinate only fragment re-reads carry whose anchored statement is gone is one no in-place re-stamp clears; it used to exit 0 while `--strict` exited 2, and it now names the released root and exits 1, as a released carrier already did.*
```
```diff
--- a/docs/the-evidence-ledger.md
+++ b/docs/the-evidence-ledger.md
@@
 narrowing left its file out, because the root is the row a `Re-read ·` cites.
-A row corrected by two rows is not a re-read's to clear: `--strict` names
-each correcting row and exits 2, while `--reverify`, narrowed or not, exits
-0 and leaves the choice of claim to a person.
+Three things are not a re-read's to clear, and `--strict` exits 2 on each.
+A row corrected by two rows leaves the choice of claim to a person, and
+`--reverify`, narrowed or not, exits 0. A BROKEN anchor takes a
+`Corrected ·` row, or an edit where its row sits in a fragment: `--reverify`
+names it left where the run read it and exits 0, except under the freeze,
+where a released row carrying it is named with that repair and the run
+exits 1. A statement gone from a row in a family a fragment roots is that
+fragment's to repair in place, and `--reverify` exits 0.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the module, `test_two_branches_re_read_one_released_row.py` and `test_a_narrowed_ledger_read_says_what_it_skipped.py` at `2e595b8e` | 236 passed |
| HEAD's module copied into a clone at `465adf33`, the four new or changed case families selected | 11 failed, 141 passed: 7 grid cells, the round's case in 3 modes, 1 S3 cell |
| the released-root guard deleted in the clone, its case run | 1 failed, naming `seal/ledger/2000000001-a-later-item.md:1` LEFT; restored |
| `released_drift` keying the owed entry on the picked member, the S3 case and the grid run | 5 failed: both re-reads-only S3 cells, 3 grid cells; restored |
| the narrowing notice's wording changed, the S3 case and the grid run | at least 12 grid cells failed; restored |
| Warden probes P1–P8, 105 runs, against HEAD | 11 disagreements: P5 under `--into` (2), P6 unnarrowed (3), P8 (6) |
| the same 105 runs against `465adf33` | 37 disagreements |
| Warden probe P9: a released singleton and a folded re-read whose statement is gone, both checkers | exit 1 in all 12 runs at both |
| Warden probe P10: BROKEN carried by a fragment only, by a released singleton, and by both, both checkers | identical at both; exit 0 against `--strict` 2 except under the freeze where a released row carries it |
| Warden probe P11: a fragment `Corrected ·` root whose statement is gone, narrowed and not, both checkers | exit 0 against `--strict` 2 in all 6 runs at both |
| ⬜ 10's paste-ready case, at HEAD and at `465adf33` | 3 passed at HEAD; 3 failed at `465adf33` |
| `bin/correction-check --range 9511f6cd...HEAD` | 1 merge examined, no marker dropped, no released ledger file changed, exit 0 |
| `bin/evidence-check --strict .` at `2e595b8e` | 4,029 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted; exit 0 |
| every anchor of #736's fragment across `2b1dcb1f`, `604f8969`, `9511f6cd` and `5e7e75de` | 20 moved, none on both sides, each kept the side that moved it |
| `bin/test` over the one-home, docs line-wrap, no-real-identifiers, one-word-one-meaning and merge-correction modules at `2e595b8e` | 134 passed |
| `bin/test tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_docs_line_wrap.py`, and `evidence-check --strict .`, with this report staged in the clone | 60 passed; 4,029 ok, records arm 0 refused, exit 0 |
| `round-record new` over this report, in the clone only, the record it wrote then discarded with the clone | exit 0; `Needs a fix` and `Loses a record or crashes` read `no`; `Pass` unchecked over ⬜ 10–12 |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, once the rounds settle |
| `bin/survivor-check` over the fix range | not yet — not run by this round |

```
# P7, as the probe built it (warden probe, deleted)
R  seal/releases/0.1.0.md                         | R1 · handler adds one | `src/service.py#handler@<h>` | read | 2026-01-01 | |
M  seal/ledger/2000000002-m.md                    | Re-read · R1 · … | `<cite R>`, `src/service.py#other>"x * 2"@<stated>` | read | 2026-02-01 | Re-read 2026-02-01 |
code: other now returns x * 3
evidence-check --reverify .                        -> 465adf33: exit 0 · HEAD: exit 1, LEFT seal/releases/0.1.0.md:5
evidence-check --strict .                          -> exit 2 at both, M DRIFTED (the anchored statement is gone)

# P5 (warden probe, deleted)
three_readings(repo, "fragment", "fragment", <either carrier>), freeze declared
evidence-check --reverify --into seal/ledger/4000000001-the-re-reading-item.md --checked 2026-02-15 --ledger <M> .
                                                   -> exit 0, "1 citing row written"
evidence-check --strict --ledger <M> .             -> exit 2, M DRIFTED: the newest reading, 2026-03-01 at N, holds other content
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3292` | round 1's 🟡 1 — fixed |
| round-1 | `docs/the-evidence-ledger.md:103` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2505` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2495` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md:2` | round 1's ⬜ 5 — answered |
| round-1 | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1489` | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1445` | round 1's ⬜ 7 — fixed |
| round-1 | `docs/the-evidence-ledger.md:163` | round 1's ⬜ 8 — fixed |
| round-1 | `seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/spec.md:72` | round 1's ⬜ 9 — answered |
| round-1 | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases`, `seal/ledger.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3286` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_released_row_is_read_again_in_a_fragment.py` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

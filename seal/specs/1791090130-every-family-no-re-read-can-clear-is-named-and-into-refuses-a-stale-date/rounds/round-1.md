# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — review round 1

| Field | Value |
|---|---|
| Target SHA | 91787daccd45c7f23c3244aa4e2c216adb66a5e5 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #771 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the stale-date line, the ledger home, the changelog, F1 and the L4 correction say nothing is recorded for a refused row while the same run records its BROKEN coordinates), 🟡 2 (the after-today arm's Corrected repair leaves the owed pact change unrecorded for good) |
| Loses a record or crashes | yes — 🟡 2: a row whose newest reading is dated after today has its move under a pact clause dropped by the refusing run, and the Corrected row the line asks for takes it out of every later re-read, so the pact change is never recorded and the tree checks clean |

- [ ] Pass

## What this round was asked

Round 1 of work item `1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date` (#746, PR #771). Target `91787dac`, against `release/v0.18.1` at `edee5ca2`.

Spec compliance first:
- The per-row refusal in `reverify_into` at step 1: a stale row leaves the plan and the moves, and it is named on a `LEFT` line with exit 1. A tie writes. A future newest date names a `Corrected ·` repair.
- The shared date rule (`reading_date` and `family_view`'s `newest`).
- That #756's record-first order and its kill-safety still hold for a refused row: no record and no move.
- The policy paragraph naming the five families no re-read can clear, each held by a case.

Then judge the departures the build made:
- L4 and N1 written as `Corrected ·` rather than re-read.
- Two hash-only edits to #756's fragment rows C1 and W8.
- A pact fixture's `row()` date moved from 2026-10-01 to 2026-09-01, because five cases passed by the defect.

Quality second.

The orchestrator verified the changed modules plus hygiene (782 passed) and ruff on the changed Python files at the target. The release head carries 10 drifted rows from the wave-one squashes; #766 re-reads them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The stale-date `LEFT` line, the ledger home, the changelog, F1 and the L4 correction all say nothing is recorded for a refused row, while the same run records that row's BROKEN coordinates from `released_drift`'s `broken` list | `skills/evidence-check/scripts/evidence_check.py:3645` | open | executed, P1: the line *nothing was written or recorded for this row* prints two lines above *recorded … a pact change for seal/releases/0.1.0.md:5*, and the record holds the `evict` BROKEN row; `docs/the-evidence-ledger.md:148`, `changelog.md:8` read |
| 🟡 2 | A row refused because its newest reading is dated after today is sent to a `Corrected ·` repair, which takes it out of every later re-read, so its move under a pact clause is never recorded and the tree then checks clean | `skills/evidence-check/scripts/evidence_check.py:3591` | open | executed, P2: run 1 exit 1 and no record, the `Corrected ·` row written as the line says, run 2 exit 0 and no record, `--strict` exit 0; at the base the move was recorded |
| ⬜ 3 | The changelog says a case holds each of the five things *in every mode, narrowed and not*; the fifth is held under the two freeze modes for a folded citing row and by one unnarrowed run without the freeze | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/changelog.md:21` | open | read against `test_a_folded_citation_whose_released_line_changed_is_left_at_exit_0` and `test_an_unfrozen_restamp_of_a_released_row_moves_the_line_its_re_read_cites`; the ledger home's paragraph states the fifth's modes correctly; a correction to the run's paperwork |
| ⬜ 4 | Spec A10 says to extend `test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read`; the build wrote a sibling, and `overview.md`'s divergence table does not list it | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/overview.md:18` | open | read: `phases/phase-2.md` records the choice and its reason; the sibling covers the axes; a correction to the run's paperwork |
| 🟢 | S1 to S3: the per-row refusal, the strict comparison and the `LEFT` line's elements | `skills/evidence-check/scripts/evidence_check.py:3506` | confirmed | executed: the two modules pass at the target (437); with `edee5ca2`'s checker 27 of the stale-date cases fail; read: the check precedes every `moves.append` in the loop |
| 🟢 | The shared date rule: `family_view` grades and `later_reading` refuses by `reading_date` and one `newest` field | `skills/evidence-check/scripts/evidence_check.py:2924` | confirmed | read: `newest_by` is filled from the `newest` and `last` that grade the coordinate; the unit case passes |
| 🟢 | S4 and S5: five things named, each with a case | `docs/the-evidence-ledger.md:178` | confirmed | executed: every case passes at the target; the mutation reds are `phases/phase-2.md`'s account, not re-run |
| 🟢 | L4 and N1 corrected rather than re-read, each carrying every coordinate its released row rested on | `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md:4` | confirmed | read: L4's 14 and N1's 11 coordinates each found in the correcting row; `INTO_VERIFIED` would claim the unconditional write holds; L4's *nothing is recorded* clause is 🟡 1's |
| 🟢 | C1 and W8 of #756's fragment re-stamped by hash alone | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | confirmed | read: both claims hold against the new `reverify_into`; executed: `--strict` narrowed to that fragment reads only the chore's three units DRIFTED |
| 🟢 | The pact fixture's `row()` dated 2026-09-01 | `tests/test_a_signatory_records_a_pact_change.py:74` | confirmed | read: every `--checked` the module passes is 2026-09-04 or later; no record assertion changed; the remaining 2026-10-01 rows are fragment rows re-stamped in place |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py
STALE_NOTHING = "no `Re-read ·` row was written for this row"
```
```python
# skills/evidence-check/scripts/evidence_check.py, reverify_into, the stale
# branch: the moves are appended before the line is built
        stale = later_reading(view, key, drifted[key], checked)
        if stale is not None:
            # No `Re-read ·` row: dated CHECKED it would clear nothing (#746).
            # The code under the row moved whatever the reading's date, and
            # the repair named below -- a reading dated again, or a
            # `Corrected ·` row, which takes the row out of every later
            # re-read -- may never pass through here again, so the moves are
            # recorded now. A second run finds each the record's last word
            # and appends nothing (#756 W4). Round 1 of #746, yellow 2.
            if moves is not None:
                for coord, m in drifted[key].items():
                    moves.append(
                        (
                            path,
                            key[1],
                            coord,
                            m.group("hash"),
                            current_hash(m, root, maps, default_repo),
                        )
                    )
            date, coord, at = stale
```
```text
docs/the-evidence-ledger.md, the --into paragraph, replace
  "clear nothing: the run writes and records nothing for that row, names it with
   both dates and the place of the later reading, and exits 1."
with
  "clear nothing: the run writes no row for it, records the moves of the
   coordinates it would carry, names it with both dates and the place of the
   later reading, and exits 1."
Re-wrap to the line width. Then update the pins that quote the old words:
  tests/test_a_released_row_is_read_again_in_a_fragment.py:1801 and :1901
    ("nothing was written or recorded for this row" -> "no `Re-read ·` row was
     written for this row")
  test_the_home_and_the_usage_say_a_stale_row_is_left, the first sentence
  changelog.md:8, F1 and the L4 correction in this item's fragment
    ("Nothing is written or recorded for it" / "nothing is recorded for it"
     -> "no row is written for it, and its moves are recorded")
```
```python
# tests/test_a_signatory_records_a_pact_change.py, replacing
# test_a_row_refused_for_a_stale_date_records_nothing
def test_a_row_refused_for_a_stale_date_records_its_move_once(repo):
    """A5, revised by round 1 of #746 (yellow 2). The released row was read on
    2026-09-10, after `--checked 2026-09-04`, so no `Re-read ·` row is
    written. The code under the clause moved all the same, so the move is
    recorded, and a second identical run leaves the record byte for byte."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}", "2026-09-10"),
        encoding="utf-8",
    )
    fragment = cite(repo, [])
    new = move_serialize(repo)
    states = []
    for _ in range(2):
        code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
        assert code == 1, out
        assert "Re-read · O1" not in fragment.read_text(encoding="utf-8"), out
        assert "no `Re-read ·` row was written for this row" in out, out
        assert record_rows(repo) == [
            f"| {CLAUSE} | seal/releases/0.1.0.md · O1 | "
            f"`src/orders.py#serialize@{old}` → `@{new}` | 2026-09-04 |"
        ], out
        states.append((repo / RECORD).read_bytes())
    assert states[0] == states[1]


def test_a_row_dated_after_today_has_its_move_recorded_before_its_correction(repo):
    """Round 1 of #746, yellow 2. The line sends a reading dated after today to
    a `Corrected ·` row, which no later re-read reaches, so the move under the
    clause is recorded by the run that refused the row, or never."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}", "2999-01-01"),
        encoding="utf-8",
    )
    cite(repo, [])
    new = move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "a `Corrected ·` row" in out, out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/releases/0.1.0.md · O1 | "
        f"`src/orders.py#serialize@{old}` → `@{new}` | 2026-09-04 |"
    ], out
```
```python
# skills/evidence-check/scripts/evidence_check.py, only if yellow 2 is declined
STALE_NOTHING = (
    "no `Re-read ·` row was written for this row and none of its drifted "
    "coordinates was recorded"
)
```
```python
# tests/test_a_signatory_records_a_pact_change.py, appended
def test_a_stale_row_with_a_broken_coordinate_says_what_was_recorded(repo):
    """Round 1 of #746, yellow 1. A refused row's BROKEN coordinate comes
    from `released_drift`'s BROKEN list and is recorded beside the refusal,
    so the refusal's line may not say nothing was recorded for the row."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    s = unit_hash(repo, "src/orders.py", "serialize")
    e = unit_hash(repo, "src/orders.py", "evict")
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        f"| O1 · x | `{CLAUSE}`, `src/orders.py#serialize@{s}`, "
        f"`src/orders.py#evict@{e}` | read | 2026-09-10 | |\n",
        encoding="utf-8",
    )
    cite(repo, [])
    src = SOURCE.replace("'id': order.id", "'id': order.id, 'tax': 0")
    (repo / "src" / "orders.py").write_text(
        src.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert "is older than the newest reading" in out, out
    assert "nothing was written or recorded" not in out, out
    assert any(f"`src/orders.py#evict@{e}` BROKEN" in r for r in record_rows(repo))
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py tests/test_a_signatory_records_a_pact_change.py -q` in the round's clone at `91787dac` | exit 0, 437 passed |
| The same two modules, `-k` on the stale-date cases and A5, with `edee5ca2`'s `evidence_check.py` checked out in the clone, then restored | exit 1, 27 failed and 32 passed |
| `bin/evidence-check --strict` narrowed with `--ledger` to this item's fragment and to #756's fragment | exit 2: this item's fragment 73 ok and 0 drifted; #756's fragment 3 DRIFTED, the chore's units `VERSIONS_OF_ANOTHER_PRODUCT`, `templates/config.md` and `fake_venv` |
| P1, one `test_tmp_*` case: stale row with a BROKEN coordinate | exit 1; the stale line says nothing was recorded for `seal/releases/0.1.0.md:5`; a `recorded` line names the same row; the record holds one `evict` BROKEN row |
| P2, one `test_tmp_*` case: row dated after today, then the `Corrected ·` repair | run 1 exit 1, record empty; run 2 exit 0, record empty; `--strict` exit 0 |
| The broad gate (full suite, repository lint, typecheck) | not yet; the sealer's, after the rounds settle |

```python
# tests/test_tmp_746_probe.py in the round's clone, run once, deleted.
# Helpers imported from tests/test_a_signatory_records_a_pact_change.py.
# P1: freeze, a released row dated 2026-09-10 citing CLAUSE with
#     serialize@<old> and evict@<old>; serialize edited, evict deleted;
#     run --into FRAGMENT --checked 2026-09-04; print exit, output, record_rows.
# P2: freeze, a released row dated 2999-01-01 citing CLAUSE with
#     serialize@<old>; serialize edited; run --into --checked 2026-10-04;
#     then write into FRAGMENT
#     | Corrected · x | `<citation of O1>`, `CLAUSE`, `src/orders.py#serialize@<new>` | read | 2026-10-04 | Corrected 2026-10-04 |
#     run --into again; then --strict; print each exit and record_rows.
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Without the freeze, one `--reverify` over every ledger re-stamps a released row in place and so moves the line its fragment's citing rows cite; `--strict` reads those citations DRIFTED until a second run (found by the build, pinned by a case) | `overview.md` §*Not done*; no issue filed yet | the orchestrator, who decides whether to file it |

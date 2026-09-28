# 1790635412-an-overflow-cell-is-refused-in-every-repository — review round 2

| Field | Value |
|---|---|
| Target SHA | 853600fab2a6b0a6cd5734751ee5b7aab13a4f76 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #659 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `b5a41796c072d686c94f55b6db80efd60f39bea2..b934c84758ae06e26af647ee2fe18a7ee512f537`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, the new `gfm_lines` docstring gives a false reason for leaving the hash side on `splitlines` |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, verifying, over round 1's fix diff `6bf504c3..0659e395` at HEAD `853600fa`. Asked whether each verdict round 1 closed is closed, with the fixes' new units (`GFM_LINE_RE`, `gfm_lines`, `NOT_A_LINE_END` and five cases) as a finding surface, and whether the line the smith drew between the walks it moved and the `splitlines` calls feeding `content_hash` is drawn where it should be.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The new `gfm_lines` docstring says the hash side's line ends are "a separate question" from GFM's; for a `.py` anchor `ast` numbers lines where GFM does, so a form feed above a unit shifts the hashed region and an edit to the unit's last line passes as OK | `skills/evidence-check/scripts/evidence_check.py:278` | **fixed** `b934c847` | fixed at b934c847 — the docstring says the hash side still splits with `splitlines` here, that this is a known defect, and that #664 fixes it; Executed at `853600fa`: unit at lines 3 to 5, region hashed was lines 2 to 4, check said `1 ok` after the edit. The line the fix drew is right for this branch; the reason given for it is not |
| ⬜ 2 | `round-1.md` still defers the `unquoted` fence item to work item B and the `old_format_rows` item to this branch's fix pass, both fixed in `17e8f667`; its 🟡 1 grounds say the hash-side change "moves every hash" | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | answered | a record correction, made by the orchestrator in `b5a41796` before the fix pass: round-1.md's two deferrals now say fixed at `17e8f667`, and the false reason is replaced by #664; Read against the fix diff; a correction to the run's paperwork, not counted in Needs a fix |
| ⬜ 3 | `round-1.md`'s fenced case has a line break where the report has U+2028, so the record's case does not parse | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | answered | a record correction in `b5a41796`: round-1.md's case carries U+2028 as the `\u2028` escape; Executed: one U+2028 in the report, none in the record, a `"\n"` in its place. A correction to the run's paperwork; the tool cause is deferred |
| 🟢 | round 1's blocking finding is closed — the five walks split where GFM does, and each has a case that goes red when it alone is reverted | `skills/evidence-check/scripts/evidence_check.py:274` | confirmed | Executed: module 38 passed; 15 instances red against `6bf504c3`; five single-walk reverts each red on their own case; `gfm_lines` equals `splitlines` on 20,000 strings without the eight characters |
| 🟢 | round 1's ⬜ 2 is answered on grounds that hold | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md:198` | confirmed | Read: A7 holds `MALFORMED` unchanged, which the proposed skip would break |
| 🟢 | round 1's ⬜ 3 is answered on grounds that hold | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md:161` | confirmed | Read: the walk reads the shared `split_row`, the rule the reset comes from |
| 🟢 | The eight rows the fix drifted are re-read and true | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | confirmed | Read: each has a dated `Re-read` note naming the change. Executed: `bin/evidence-check .` exit 0, 0 drifted; `correction-check` over the fix range exit 0 |

## Paste-ready fixes

```python
def gfm_lines(text, keepends=False):
    """TEXT's lines as GFM reads them, the way `str.splitlines` returns them
    otherwise: no trailing empty line, and each line's end kept only when
    KEEPENDS asks.

    For every walk of markdown lines that reads a table or a fence. The
    lines a hash covers and an anchor spans are still `splitlines`', and
    that is a deferral rather than a different answer: `ast` ends a `.py`
    line at LF, CR and CRLF too, so a form feed above a unit already shifts
    the region hashed off the unit it names. Switching moves the recorded
    hash of every region that holds or follows one of those characters, so
    it is a migration of its own (round 2 of 1790635412, deferred)."""
    lines = GFM_LINE_RE.findall(text)
    return lines if keepends else [line.rstrip("\r\n") for line in lines]
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_row_wider_than_its_header_is_named.py` at `853600fa` | exit 0, 38 passed |
| the same module's fifteen new instances against `evidence_check.py` from `6bf504c3` | exit 1, 15 failed (12 in one run, the record case's 3 in a second) |
| probe file test_tmp_r2.py (deleted): each of the five walks reverted to `splitlines` alone, then the new cases | each walk's own case red; the first pass reported the wrong case for `ledger_table_rows` because a stale bytecode file of equal size was reused, and the rerun with `__pycache__` cleared and `PYTHONDONTWRITEBYTECODE` set is the result recorded here |
| the same probe: `gfm_lines` against `str.splitlines` on 20,000 random strings with LF, CR and CRLF, both `keepends` values | 0 mismatches |
| the same probe: a `.py` unit after a form-feed line, `--reverify`, then an edit to the unit's last line, then the check | the region hashed was lines 2 to 4 for a unit at 3 to 5; the check exited 0 with `1 ok · 0 drifted` after the edit |
| a scan of every tracked file for U+2028, U+2029, NEL, VT, FF and FS, GS, RS | one file: round 1's report, one U+2028 |
| a byte count of U+2028 in `round-1-report.md` and `round-1.md` | 1 and 0; the record's case holds a line break in its place |
| `bin/evidence-check .` at `853600fa` | exit 0; `2662 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow`; records arm 0 refused |
| `bin/correction-check --range 6bf504c3...0659e395` | exit 0 |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet run by anyone; `unverified`, answered by the sealer after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1714` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1798` | round 1's ⬜ 2 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1722` | round 1's ⬜ 3 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1609` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2089` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | round 1's 🟢 — confirmed |
| round-1 | `README.md:270` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Every hash-side split in `evidence_check.py` (`content_hash` callers, `py_spans` slices, `heading_path`, `text_regions`, `file_units`, `migrate`'s cited-body lines) uses `str.splitlines`, so a form feed or U+2028 above a unit shifts the hashed region and an edit can pass as OK. `arm_check.py`'s `_lines` is the splitter to share. Pre-existing; changing it moves the hash of any region holding or following such a character | a new issue | the orchestrator, by opening it; it needs a work item of its own because it moves recorded hashes in other repositories |
| The same class outside `evidence_check.py`: `correction_check.py`'s `rows` reads the same ledgers with `splitlines`, so a `Corrected` note after such a character is invisible on both sides of a merge; `round_record.py:2215` rewrote round 1's fence (⬜ 3); `survivor_check.py`, `fold_check.py`, `hooks/config.py` and `gather_changelog.py` also split markdown with `splitlines` and were not checked one by one | a new issue, or the same one as the row above | the orchestrator, by opening it |

# Round 2 report — 1790635412-an-overflow-cell-is-refused-in-every-repository

Reviewer: warden. A verifying round. Target: the diff of round 1's fixes,
`6bf504c3..0659e395` (`17e8f667` the fix, `0659e395` the rows it drifted
re-read), read with the branch at `853600fa`. Read and run in a
`git clone --no-local` of the orchestrator's tree, never in that tree.

Carried from round 1 rather than re-established: the coordinates of the five
walks and of `ledger_table_rows`, and the fact that `spec.md` A7 holds
`MALFORMED` unchanged. Every verdict below is re-derived.

## What this round found, in one view

Round 1's 🟡 1 is closed. The five walks now split where GFM splits, each walk
has a case of its own that goes red when that walk alone is reverted, and the
ledger stays true. What is left is about the line the fix drew:

```
the fix leaves every hash-side split on str.splitlines            (right place)
  └─ its stated reason, in the new gfm_lines docstring and in the
     round-1 record, is false                                          (🟡 1)
       ├─ ast numbers a .py file's lines where GFM does, so the hash
       │  side already covers the wrong lines after a form feed        (deferred)
       └─ switching would move no hash in this repository              (measured)
the same class outside evidence_check.py                               (deferred)
  └─ round_record.py rewrote a U+2028 in round 1's report as a line
     break, so round-1.md's fenced case is not the report's            (⬜ 3)
round-1.md still defers two items the fix pass took                     (⬜ 2)
```

## Round 1's verdicts

**🟡 1 is closed.** `gfm_lines` (`skills/evidence-check/scripts/evidence_check.py:274`)
ends a line at LF, CR and CRLF only, and `unquoted`, `old_format_rows`,
`ledger_table_rows`, `migrate` and `check_records` read through it. Executed:

- The changed module is green at `853600fa` (38 passed).
- Against the checker at `6bf504c3`, all fifteen new case instances fail.
- Each walk was reverted alone, with the bytecode cache cleared, and each time
  its own case went red: `unquoted` the fence case, `old_format_rows` the
  old-coordinate case, `ledger_table_rows` the row case (and the fence case,
  which reads through it), `migrate` the migrate case, `check_records` the
  record case. So "one case per walk" holds.
- On 20,000 random strings built from `a`, `|`, space, tab, a backtick, LF, CR
  and CRLF, `gfm_lines` returned what `str.splitlines` returns, with and
  without `keepends`. On a ledger without the eight characters, nothing moves.
- `bin/evidence-check .` exits 0 with `0 drifted · 0 overflow`, and
  `correction-check` over the fix range exits 0.

**⬜ 2 and ⬜ 3 are answered on grounds that hold.** Read: `spec.md` A7 is
"`MALFORMED` is unchanged", so skipping a wider row in `grounds_cells` would
break an acceptance row, and `spec.md` states the walk reads the shared
`split_row`, which is the rule ⬜ 3's reset comes from.

**The eight rows `0659e395` touched are true.** Read: each carries a dated
`Re-read 2026-09-29` note that names what moved and why the claim still holds,
and O2 now also cites the new row case. Executed: 0 drifted.

## The fix draws the line in the right place, for a reason that is false (🟡 1)

The smith left every `splitlines` call that feeds `content_hash` or an anchor
span. For this branch that is the right line. Changing it moves recorded
hashes in other repositories, and that is a migration of its own, not part of
an overflow verdict.

The reason written beside it is not true, though. The new docstring says
"which characters end a line there is a separate question from where a table
row or a fence ends" (`evidence_check.py:278`). The round-1 record's grounds
say "changing them moves every hash". Both were checked:

- **It is not a separate question for a `.py` anchor.** `py_spans` takes its
  line numbers from `ast`, and the tokenizer ends a line at LF, CR and CRLF,
  exactly where GFM does. The region is then sliced from `body.splitlines()`.
  After a form feed on its own line, `splitlines` counts one line more, so the
  slice is shifted by one. Executed: for a unit `ast` places at lines 3 to 5,
  the hash covered `['', 'def f():', '    a = 1']`, and after editing the
  unit's last line the check still said `1 ok · 0 drifted`. That is a silent
  pass on a real edit. `skills/verify/scripts/arm_check.py` already documents
  the same shift in its `_lines` docstring and splits with the same regex.
- **Switching would move no hash here.** Executed: no tracked file in this
  repository holds any of the eight characters, except round 1's report. In
  another repository it moves only the hash of a region that holds or follows
  one of them, and a moved hash reads DRIFTED, which is the documented
  degrade.

Why it matters: the docstring sits on the helper that "every walk" is told to
use. The next author who has to choose between `gfm_lines` and `splitlines`
for a hash path will read "a separate question" and keep the defect. The
defect itself predates this branch, so it goes to *Deferred*. The sentence is
new, so it is this branch's to correct.

## Round 1's record still defers two items the fix took (⬜ 2)

`round-1.md`'s *Deferred* table sends the `unquoted` fence item to work item B
(#584), via milestone 49's orchestrator. It sends the `old_format_rows` item to
"this branch, if the smith takes 🟡 1's constant". `17e8f667` fixed both, and
the 🟡 1 grounds cell of the same record says so. Left as it is, B's smith is
handed an item that is already closed. The same record's grounds also say
"changing them moves every hash", which 🟡 1 measured as untrue. This is a
correction to the run's paperwork, not to the tool.

## round_record.py rewrote a character in round 1's fenced case (⬜ 3)

Round 1's report has one U+2028 inside its paste-ready case, as the first
parameter of `NOT_A_LINE_END`'s predecessor. Executed: the report holds one
U+2028, and `round-1.md` holds none; in its place is a line break, so the
record's fenced case is a string literal broken across two lines and does not
parse. The cause is `skills/code-review/scripts/round_record.py:2215`, which
reads the report with `report.splitlines()` and writes lines back joined by LF.
The record promises that fenced blocks are copied verbatim.

This is the same class as round 1's 🟡 1, one script over. The case the smith
planted spells the character as `"\u2028"`, so no code was harmed. The record
is what is wrong, and the tool defect goes to *Deferred*.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The new `gfm_lines` docstring says the hash side's line ends are "a separate question" from GFM's; for a `.py` anchor `ast` numbers lines where GFM does, so a form feed above a unit shifts the hashed region and an edit to the unit's last line passes as OK | `skills/evidence-check/scripts/evidence_check.py:278` | open | Executed at `853600fa`: unit at lines 3 to 5, region hashed was lines 2 to 4, check said `1 ok` after the edit. The line the fix drew is right for this branch; the reason given for it is not |
| ⬜ 2 | `round-1.md` still defers the `unquoted` fence item to work item B and the `old_format_rows` item to this branch's fix pass, both fixed in `17e8f667`; its 🟡 1 grounds say the hash-side change "moves every hash" | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | open | Read against the fix diff; a correction to the run's paperwork, not counted in Needs a fix |
| ⬜ 3 | `round-1.md`'s fenced case has a line break where the report has U+2028, so the record's case does not parse | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/rounds/round-1.md` | open | Executed: one U+2028 in the report, none in the record, a `"\n"` in its place. A correction to the run's paperwork; the tool cause is deferred |
| 🟢 | round 1's blocking finding is closed — the five walks split where GFM does, and each has a case that goes red when it alone is reverted | `skills/evidence-check/scripts/evidence_check.py:274` | confirmed | Executed: module 38 passed; 15 instances red against `6bf504c3`; five single-walk reverts each red on their own case; `gfm_lines` equals `splitlines` on 20,000 strings without the eight characters |
| 🟢 | round 1's ⬜ 2 is answered on grounds that hold | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md:198` | confirmed | Read: A7 holds `MALFORMED` unchanged, which the proposed skip would break |
| 🟢 | round 1's ⬜ 3 is answered on grounds that hold | `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md:161` | confirmed | Read: the walk reads the shared `split_row`, the rule the reset comes from |
| 🟢 | The eight rows the fix drifted are re-read and true | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` | confirmed | Read: each has a dated `Re-read` note naming the change. Executed: `bin/evidence-check .` exit 0, 0 drifted; `correction-check` over the fix range exit 0 |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Every hash-side split in `evidence_check.py` (`content_hash` callers, `py_spans` slices, `heading_path`, `text_regions`, `file_units`, `migrate`'s cited-body lines) uses `str.splitlines`, so a form feed or U+2028 above a unit shifts the hashed region and an edit can pass as OK. `arm_check.py`'s `_lines` is the splitter to share. Pre-existing; changing it moves the hash of any region holding or following such a character | a new issue | the orchestrator, by opening it; it needs a work item of its own because it moves recorded hashes in other repositories |
| The same class outside `evidence_check.py`: `correction_check.py`'s `rows` reads the same ledgers with `splitlines`, so a `Corrected` note after such a character is invisible on both sides of a merge; `round_record.py:2215` rewrote round 1's fence (⬜ 3); `survivor_check.py`, `fold_check.py`, `hooks/config.py` and `gather_changelog.py` also split markdown with `splitlines` and were not checked one by one | a new issue, or the same one as the row above | the orchestrator, by opening it |

## Paste-ready fixes

### 🟡 1 — say why the hash side keeps `splitlines`, truthfully

In `skills/evidence-check/scripts/evidence_check.py`, the whole of `gfm_lines`:

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

## Regression tests to plant

- None for 🟡 1, which is a docstring.
- For the deferred hash-side item, in `tests/test_a_row_points_by_content.py`:
  a `.py` file with a form-feed line above a function, a row reverified onto
  it, then an edit to the function's last line, expecting DRIFTED. It fails at
  `853600fa` (executed above as a probe, not planted).

## Facts for the evidence ledger

- Rows O2 and P2-1 could say that each of the five walks has its own case,
  red when that walk alone is reverted. Executed in this round.

Needs a fix: yes — 🟡 1, the new `gfm_lines` docstring gives a false reason for leaving the hash side on `splitlines`
Loses a record or crashes: no

The broad gate has not run. Once 🟡 1 is fixed and a round leaves nothing
open, the sealer's spawn comes due. The two ⬜ corrections are the
orchestrator's, to `round-1.md`, and the two deferred rows need an issue each
or one between them.

## Proof block

Files opened in the clone at `853600fa`:
`skills/evidence-check/scripts/evidence_check.py` (225–320, 505–540, 740–830,
900–935, 1570–1600, 1720–1790, 1935–2030, 2095–2135, 2760–2860, and the fix
diff), `tests/test_a_row_wider_than_its_header_is_named.py` (the fix diff),
`skills/verify/scripts/arm_check.py` (540–580),
`skills/verify/scripts/unverified_check.py` (160–185, 590–610, 1100–1135),
`.github/scripts/fold_ledger.py` (245–275, 385–410),
`skills/evidence-check/scripts/correction_check.py` (345–375),
`skills/code-review/scripts/round_record.py` (2205–2235), `bin/test`, this
work item's `rounds/round-1.md`, `rounds/round-1-report.md` and `spec.md`
(lines 161, 178, 197, 198), and the diff of `0659e395` over `seal/`.
